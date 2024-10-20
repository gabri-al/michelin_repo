import dash
from dash import html, callback, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate

dash.register_page(__name__, path='/search', order = 2, name='Search', title='Michelin WebApp | Find Your Restaurant')

############################################################################################
# Import functions, settings
from assets.fig_layout import (country_geojson, my_figlayout, my_map_layout, my_map_trace, my_colorscale, my_colorbar2,
                               chart_colours_, my_legend, center_map_on_data, countries__)
from assets.filterbar import _value_for_any

############################################################################################
# Upload data
import pandas as pd
silver_df = pd.read_parquet("data/silver_data.parquet", engine='pyarrow')
#print(silver_df.columns)
# Print out any country which is not compatible with names on the geoJson dataset
for c in silver_df['Country_Code_ISO3'].unique():
    if c not in countries__:
        print("Found an incompatible country: %s" % c)

############################################################################################
# Define page objects that don't depends on callbacks

######################## Generate Data for filters

############################################################################################
# Page layout
layout = dbc.Container([
    dbc.Row([
        #dbc.Col([
            #html.H1("Data Insights", className='titles-h1')
        #], width=12)
    ]),

    ## Main Search bar
    dbc.Row([
        dbc.Col([
            dcc.Textarea(id = 'search-input', placeholder="Describe the restaurant that you are looking for: cuisine, atmosphere, type of chef, etc.",
                         className= 'search-area', persistence = True, persistence_type = 'session')            
        ], width = 10),
        dbc.Col([
            html.Button(["Search"], id='search-button', n_clicks=0, className='search-button'),
        ], className = 'search-bar-row', width = 2)
    
    ]),

    ## Maps on Row 1
     dbc.Row([
        dbc.Col([
            html.Div([
                html.H2(id='title-101', className='titles-h2'),
                html.P(id='p-101', className = 'charts-p'),
                dcc.Loading(id='loading-101', type='default',
                        children = dcc.Graph(id = 'fig-101'))
            ], className = 'chart-div')
        ], width = 12)
    ], className = 'chart-row'),

])

### PAGE CALLBACKS ###############################################################################################################

##################### EMBED SEARCH INPUTS
# Save Search Button Clicks into Store --> this will be part of the main callback!
@callback(Output('browser-memo', 'data'),
          Input('search-button', 'n_clicks'),
          State('browser-memo', 'data'))
def store_input(n_clicks, store_data):
    if n_clicks is None or n_clicks == 0:
        raise PreventUpdate
    #Initialize
    if 'search_clicks' in store_data.keys():
         curr_clicks = store_data['search_clicks']
    else:
         curr_clicks = 0
    #Update
    if int(n_clicks) != int(curr_clicks):
         store_data['search_clicks'] = n_clicks
    else:
         raise PreventUpdate
    return store_data

##################### UPDATES ON FIGS
@callback(
    # Outputs for Row 1
    Output(component_id='title-101', component_property='children'),
    Output(component_id='p-101', component_property='children'),
    Output(component_id='fig-101', component_property='figure'),
    
    # Inputs
    Input(component_id='country-dropdown', component_property='value'),
    Input(component_id='city-dropdown', component_property='value'),
    Input(component_id='cuisine-dropdown', component_property='value'),
    Input(component_id='award-dropdown', component_property='value'),
    Input(component_id='price-dropdown', component_property='value')
)
def plot_data(_countries, _cities, _cuisines, _awards, _prices):
    ## Filter data
    zoom_map = True; zoomed = 1
    if _value_for_any in _countries:
        _countries = list(silver_df['Country'].unique())
        zoom_map = False
    if _value_for_any in _cities:
        _cities = list(silver_df['City'].unique())
    if _value_for_any in _cuisines:
        _cuisines = list(silver_df['Cuisine'].unique())
    plot_df = silver_df.loc[
        (silver_df['Country'].isin(_countries)) & (silver_df['City'].isin(_cities)) & (silver_df['Cuisine'].isin(_cuisines))
        & (silver_df['Award'].isin(_awards)) & (silver_df['Price_score'].isin(_prices)), :]

    ## Generate main Scatter Map1
    title_101 = 'Restaurants Overview'
    p_101 = ''
    map_elements = {
        'Awards': ['Selected Restaurants', 'Bib Gourmand', '1 Star', '2 Stars', '3 Stars'],
        'Color': [chart_colours_['my-palette-00'], chart_colours_['my-palette-01'], chart_colours_['my-palette-03'], chart_colours_['my-palette-04'], chart_colours_['my-palette-05']],
        #'Sizes': range(6,19,3),
        'Price_score': [1, 2, 3, 4],
        #'Color': [chart_colours_['my-palette-02'], chart_colours_['my-palette-03'], chart_colours_['my-palette-04'], chart_colours_['my-palette-05']],
        'Sizes': range(4,15,3),
    }
    hover_text=[]
    for idx, row in plot_df.iterrows():
        hover_text.append(("<i>Name</i>: {}<br>"+
                           "<i>Address</i>: {}<br>"+
                           "<i>Cuisine</i>: {}<br>"+
                           "<i>Award</i>: {}<br>"+
                           "<i>Price</i>: {}"
                            "<extra></extra>").format(row['Name'], row['Address'], row['Cuisine'], row['Award'], row['Price']))
    plot_df['Hovertemplate'] = hover_text
    fig_101 = go.Figure(layout = my_figlayout)
    for aw in enumerate(map_elements['Awards']):
        for pr in enumerate(map_elements['Price_score']):
            my_map_trace_here = my_map_trace # Importing basic trace layout
            my_map_trace_here['lat'] = plot_df.loc[(plot_df['Award'] == aw[1]) & (plot_df['Price_score'] == pr[1]), 'Latitude']
            my_map_trace_here['lon'] = plot_df.loc[(plot_df['Award'] == aw[1]) & (plot_df['Price_score'] == pr[1]), 'Longitude']
            #my_map_trace_here['marker']['size'] = map_elements['Sizes'][aw[0]] # Award determines the marker size
            my_map_trace_here['marker']['color'] = map_elements['Color'][aw[0]] # Award determines the marker color
            #my_map_trace_here['marker']['color'] = map_elements['Color'][pr[0]] # Price determines the marker color
            my_map_trace_here['marker']['size'] = map_elements['Sizes'][pr[0]] # Price determines the marker size
            my_map_trace_here['name'] = aw[1] + ' ' + str('$')*pr[1]
            my_map_trace_here['hovertemplate'] = plot_df.loc[(plot_df['Award'] == aw[1]) & (plot_df['Price_score'] == pr[1]), 'Hovertemplate']
            fig_101.add_trace(go.Scattermap(my_map_trace_here))
    fig_101.update_maps(my_map_layout)
    fig_101.update_maps(center={"lat": center_map_on_data(plot_df)[0],"lon": center_map_on_data(plot_df)[1]})
    if zoom_map:
        fig_101.update_maps(zoom = zoomed)

    return (title_101, p_101, fig_101)