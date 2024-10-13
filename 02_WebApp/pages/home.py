import dash
from dash import html, callback, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go

dash.register_page(__name__, path='/', name='Insights', title='Michelin WebApp | Insights')

############################################################################################
# Import functions, settings
from assets.fig_layout import (country_geojson, my_figlayout, my_map_layout, my_Choroplethmap_layout, my_map_trace, my_colorscale, my_colorbar2,
                               chart_colours_, my_legend, center_map_on_data, map_boundaries, countries__)
from assets.filterbar import _filters, _value_for_any

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
        dbc.Col([
            html.H1("Data Insights", className='titles-h1')
        ], width=12)
    ]),

    ## Filters
    _filters,

    ## Maps on Row 1
     dbc.Row([
        dbc.Col([
            html.Div([
                html.H2(id='title-r1c1', className='titles-h2'),
                html.P(id='p-r1c1', className = 'charts-p'),
                dcc.Loading(id='loading_r1c1', type='default',
                        children = dcc.Graph(id = 'fig-r1c1'))
            ], className = 'chart-div')
        ], width = 12)
    ], className = 'chart-row'),   

    ## Maps on Row 2
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H2(id='title-r2c1', className='titles-h2'),
                html.P(id='p-r2c1', className = 'charts-p'),
                dcc.Loading(id='loading_r2c1', type='default',
                        children = dcc.Graph(id = 'fig-r2c1'))
            ], className = 'chart-div')
        ], width = 6),
        dbc.Col([
            html.Div([
                html.H2(id='title-r2c2', className='titles-h2'),
                html.P(id='p-r2c2', className = 'charts-p'),
                dcc.Loading(id='loading_r2c2', type='default',
                            children = dcc.Graph(id = 'fig-r2c2'))
            ], className = 'chart-div')
        ], width = 6)
    ], className = 'chart-row'),

    ## Hist on Row 3
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H2(id='title-r3c1', className='titles-h2'),
                html.P(id='p-r3c1', className = 'charts-p'),
                dcc.Loading(id='loading_r3c1', type='default',
                        children = dcc.Graph(id = 'fig-r3c1'))
            ], className = 'chart-div')
        ], width = 12)
    ], className = 'chart-row'),

    ## Hist on Row 4
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H2(id='title-r4c1', className='titles-h2'),
                html.P(id='p-r4c1', className = 'charts-p'),
                dcc.Loading(id='loading_r4c1', type='default',
                        children = dcc.Graph(id = 'fig-r4c1'))
            ], className = 'chart-div')
        ], width = 12)
    ], className = 'chart-row'),

    ## Hist on Row 5
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H2(id='title-r5c1', className='titles-h2'),
                html.P(id='p-r5c1', className = 'charts-p'),
                dcc.Loading(id='loading_r5c1', type='default',
                        children = dcc.Graph(id = 'fig-r5c1'))
            ], className = 'chart-div')
        ], width = 12)
    ], className = 'chart-row'),    

])

### PAGE CALLBACKS ###############################################################################################################

# Update city dropdown depending on country selection
@callback(
    Output(component_id='city-dropdown', component_property='options'),
    Input(component_id='country-dropdown', component_property='value')
)
def plot_data(_countries):
    if _value_for_any in _countries or _countries is None:
        _Cities = list(silver_df['City'].unique())
        _Cities.append(_value_for_any)
        _Cities.sort()
    else:
        _Cities = list(silver_df.loc[silver_df['Country'].isin(_countries), 'City'].unique())
        _Cities.append(_value_for_any)
        _Cities.sort()
    return _Cities

# Update figs
@callback(
    # Outputs for Row 1, Col 1
    Output(component_id='title-r1c1', component_property='children'),
    Output(component_id='p-r1c1', component_property='children'),
    Output(component_id='fig-r1c1', component_property='figure'),
    # Outputs for Row 2, Col 1
    Output(component_id='title-r2c1', component_property='children'),
    Output(component_id='p-r2c1', component_property='children'),
    Output(component_id='fig-r2c1', component_property='figure'),
    # Outputs for Row 2, Col 2
    Output(component_id='title-r2c2', component_property='children'),
    Output(component_id='p-r2c2', component_property='children'),
    Output(component_id='fig-r2c2', component_property='figure'),
    # Outputs for Row 3, Col 1
    Output(component_id='title-r3c1', component_property='children'),
    Output(component_id='p-r3c1', component_property='children'),
    Output(component_id='fig-r3c1', component_property='figure'),
    # Outputs for Row 4, Col 1
    Output(component_id='title-r4c1', component_property='children'),
    Output(component_id='p-r4c1', component_property='children'),
    Output(component_id='fig-r4c1', component_property='figure'),   
    # Outputs for Row 5, Col 1
    Output(component_id='title-r5c1', component_property='children'),
    Output(component_id='p-r5c1', component_property='children'),
    Output(component_id='fig-r5c1', component_property='figure'),        
    # Inputs
    Input(component_id='country-dropdown', component_property='value'),
    Input(component_id='city-dropdown', component_property='value'),
    Input(component_id='cuisine-dropdown', component_property='value'),
    Input(component_id='award-dropdown', component_property='value'),
    Input(component_id='price-dropdown', component_property='value')
)
def plot_data(_countries, _cities, _cuisines, _awards, _prices):
    ## Filter data
    zoom_map = True; zoomed = 5
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

    ## Generate main Scatter Map Row1 Col1
    title_r1c1 = 'Restaurants Overview'
    p_r1c1 = ''
    map_elements = {
        'Awards': ['Selected Restaurants', 'Bib Gourmand', '1 Star', '2 Stars', '3 Stars'],
        'Color': [chart_colours_['my-palette-01'], chart_colours_['my-palette-02'], chart_colours_['my-palette-03'], chart_colours_['my-palette-04'], chart_colours_['my-palette-05']],
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
    fig_r1c1 = go.Figure(layout = my_figlayout)
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
            fig_r1c1.add_trace(go.Scattermap(my_map_trace_here))
    fig_r1c1.update_maps(my_map_layout)
    fig_r1c1.update_maps(center={"lat": center_map_on_data(plot_df)[0],"lon": center_map_on_data(plot_df)[1]})
    if zoom_map:
        fig_r1c1.update_maps(zoom = zoomed)

    ## Generate map Row1 Col1
    title_r2c1 = 'Restaurants by country'
    p_r2c1 = 'Michelin guide entries count by country'    
    map_df = plot_df.groupby(['Country','Country_Code_ISO3']).agg(Res_count = ('Res_ID', 'count')).reset_index()
    hover_text=[]
    for idx, row in map_df.iterrows():
        hover_text.append(("<i>Country</i>: {}<br>"+
                           "<i>Restaurants</i>: {}"
                            "<extra></extra>").format(row['Country'], row['Res_count']))
    map_df['Hovertemplate'] = hover_text
    fig_r2c1 = go.Figure(
        layout = my_figlayout,
        data = go.Choroplethmap( # Using same arguments as https://plotly.com/python-api-reference/generated/plotly.graph_objects.Choroplethmapbox.html
            geojson = country_geojson,
            featureidkey = 'properties.ISO_A3',
            locations = map_df['Country_Code_ISO3'],
            z=map_df['Res_count'],
            colorscale = my_colorscale,
            colorbar = my_colorbar2,
            hovertemplate = map_df['Hovertemplate']
        ))
    fig_r2c1.update_maps(my_Choroplethmap_layout)
    fig_r2c1.update_maps(center={"lat": center_map_on_data(plot_df)[0],"lon": center_map_on_data(plot_df)[1]})
    if zoom_map:
        fig_r2c1.update_maps(zoom = zoomed)

    ## Generate map Row1 Col2
    title_r2c2 = 'Stars by country'
    p_r2c2 = 'Sum of Michelin Stars by country'    
    map_df = plot_df.groupby(['Country','Country_Code_ISO3']).agg(Star_sum = ('Stars_score', 'sum')).reset_index()
    hover_text=[]
    for idx, row in map_df.iterrows():
        hover_text.append(("<i>Country</i>: {}<br>"+
                           "<i>Tot Stars</i>: {}"
                            "<extra></extra>").format(row['Country'], row['Star_sum']))
    map_df['Hovertemplate'] = hover_text
    fig_r2c2 = go.Figure(
        layout = my_figlayout,
        data = go.Choroplethmap( # Using same arguments as https://plotly.com/python-api-reference/generated/plotly.graph_objects.Choroplethmapbox.html
            geojson = country_geojson,
            featureidkey = 'properties.ISO_A3',
            locations = map_df['Country_Code_ISO3'],
            z=map_df['Star_sum'],
            colorscale = my_colorscale,
            colorbar = my_colorbar2,
            hovertemplate = map_df['Hovertemplate']
        ))
    fig_r2c2.update_maps(my_Choroplethmap_layout)
    fig_r2c2.update_maps(center={"lat": center_map_on_data(plot_df)[0],"lon": center_map_on_data(plot_df)[1]})
    if zoom_map:
        fig_r2c2.update_maps(zoom = zoomed)

    ## Generate histogram Row3 Col1
    title_r3c1 = 'Popular Cuisines'
    p_r3c1 = 'Count of Restaurants by Awards and Cuisine - Showing top 50 cuisines'
    data_grouped = plot_df.groupby(['Cuisine_l1', 'Award']).agg(Count = ('Res_ID', 'count')).reset_index()
    data_grouped = data_grouped.pivot(columns = 'Award', index = 'Cuisine_l1', values = 'Count').fillna(0).reset_index()
    zeros_ = [0] * len(data_grouped)
    columns_ = ['Selected Restaurants', 'Bib Gourmand', '1 Star', '2 Stars', '3 Stars']
    for c in columns_:
        if c not in data_grouped.columns:
            data_grouped[c] = zeros_
    data_grouped['Restaurant_count'] = data_grouped['1 Star'] + data_grouped['2 Stars'] + data_grouped['3 Stars'] + data_grouped['Bib Gourmand'] + data_grouped['Selected Restaurants']
    hover_text=[]
    for idx, row in data_grouped.iterrows():
        hover_text.append(("<i>Cuisine</i>: {}<br>"+
                           "<i>Restaurants with 3 Stars</i>: {}<br>"+
                           "<i>Restaurants with 2 Stars</i>: {}<br>"+
                           "<i>Restaurants with 1 Star</i>: {}<br>"+
                           "<i>Bib Gourmand Restaurants</i>: {}<br>"+
                           "<i>Selected Restaurants</i>: {}"
                            "<extra></extra>").format(row['Cuisine_l1'], row['3 Stars'], row['2 Stars'], row['1 Star'], row['Bib Gourmand'], row['Selected Restaurants']))
    data_grouped['Hovertemplate'] = hover_text    
    data_grouped = data_grouped.sort_values(by = 'Restaurant_count', ascending = False).iloc[:50]
    fig_r3c1 = go.Figure(layout=my_figlayout)
    fig_r3c1_traces = dict() # Dictionary with traces names and colours
    for i in enumerate(columns_):
        fig_r3c1_traces[i[1]] = 'my-palette-0' + str( i[0] + 1 )
    for key, value in fig_r3c1_traces.items():
        fig_r3c1.add_trace(
            go.Histogram(
                x=data_grouped['Cuisine_l1'],
                y=data_grouped[key],
                marker_color=chart_colours_[value],
                histfunc="sum",
                name=key,
                hovertemplate = data_grouped['Hovertemplate'])
        )
    fig_r3c1.update_layout(
        bargap=.6, # gap between bars of adjacent location coordinates
        barmode='stack',
        legend = my_legend,
    )

    ## Generate histogram Row4 Col1
    title_r4c1 = 'Stars Propensity by Cuisine'
    p_r4c1 = 'Sum of Stars over Nr. of Restaurants, by cuisine - Showing top 50 cuisines and cuisines represented by min 5 restaurants'
    data_grouped = plot_df.groupby(plot_df['Cuisine_l1']).agg(Stars_count = ('Stars_score', 'sum'),
                                                              Restaurant_count = ('Res_ID', 'count')).reset_index()
    data_grouped['Star Ratio'] = data_grouped['Stars_count'] / data_grouped['Restaurant_count']
    data_grouped = data_grouped.loc[data_grouped['Restaurant_count'] >= 5, :] # Filter outliers    
    data_grouped = data_grouped.sort_values(by = 'Star Ratio', ascending = False).iloc[:50]
    hover_text=[]
    for idx, row in data_grouped.iterrows():
        hover_text.append(("<i>Cuisine</i>: {}<br>"+
                           "<i>Restaurants Count</i>: {}<br>"+
                           "<i>Tot Stars</i>: {}<br>"+
                            "<i>Stars/Restaurant Ratio</i>: {:.2%}"+
                            "<extra></extra>").format(row['Cuisine_l1'], row['Restaurant_count'], row['Stars_count'], row['Star Ratio']))
    data_grouped['Hovertemplate'] = hover_text
    fig_r4c1 = go.Figure(layout=my_figlayout)
    fig_r4c1.add_trace(
        go.Histogram(
            x=data_grouped['Cuisine_l1'],
            y=data_grouped['Star Ratio'],
            marker_color=chart_colours_['my-palette-02'],
            histfunc="sum",
            name='Stars/Restaurants',
            hovertemplate = data_grouped['Hovertemplate'])
    )
    fig_r4c1.update_layout(
        bargap=.6, # gap between bars of adjacent location coordinates
    )

    ## Generate histogram Row5 Col1
    title_r5c1 = 'Price ratio by Cuisine'
    p_r5c1 = 'Percentage of Restaurants in each Price category, by cuisine'
    data_grouped = plot_df.groupby(['Cuisine_l1', 'Price_score']).agg(Count = ('Res_ID', 'count')).reset_index()
    data_grouped = data_grouped.pivot(columns = 'Price_score', index = 'Cuisine_l1', values = 'Count').fillna(0.).reset_index()
    zeros_ = [0.] * len(data_grouped)
    columns_ = ['$', '$$', '$$$', '$$$$']
    data_grouped = data_grouped.rename(columns = {i+1: columns_[i] for i in range(4)})
    for c in columns_:
        if c not in data_grouped.columns:
            data_grouped[c] = zeros_
    for c in columns_:
        data_grouped[c] = data_grouped[c].astype(int)            
    data_grouped['Restaurant_count'] = (data_grouped['$'] + data_grouped['$$'] + data_grouped['$$$'] + data_grouped['$$$$']).astype(int)
    for c in columns_:
        data_grouped[c+' Ratio'] = data_grouped[c] / data_grouped['Restaurant_count']
    hover_text=[]
    for idx, row in data_grouped.iterrows():
        hover_text.append(("<i>Cuisine</i>: {}<br>"+
                           "<i>Restaurants Count</i>: {}<br>"+
                           "<i>$ Restaurants</i>: {}  ({:.2%})<br>"+
                           "<i>$$ Restaurants</i>: {}  ({:.2%})<br>"+
                           "<i>$$$ Restaurants</i>: {}  ({:.2%})<br>"+
                           "<i>$$$$ Restaurants</i>: {}  ({:.2%})<br>"+
                           "<extra></extra>").format(row['Cuisine_l1'], row['Restaurant_count'], row['$'], row['$ Ratio'], row['$$'], row['$$ Ratio'],
                                                     row['$$$'], row['$$$ Ratio'], row['$$$$'], row['$$$$ Ratio']))
    data_grouped['Hovertemplate'] = hover_text        
    data_grouped = data_grouped.sort_values(by = 'Restaurant_count', ascending = False).iloc[:50]
    fig_r5c1 = go.Figure(layout=my_figlayout)
    fig_r5c1_traces = dict() # Dictionary with traces names and colours
    for i in enumerate(columns_):
        fig_r5c1_traces[i[1] + ' Ratio'] = 'my-palette-0' + str( i[0] + 2 )
    for key, value in fig_r5c1_traces.items():
        fig_r5c1.add_trace(
            go.Histogram(
                x=data_grouped['Cuisine_l1'],
                y=data_grouped[key],
                marker_color=chart_colours_[value],
                histfunc="sum",
                name=key,
                hovertemplate = data_grouped['Hovertemplate'])
        )
    fig_r5c1.update_layout(
        bargap=.6, # gap between bars of adjacent location coordinates
        barmode='stack',
        legend = my_legend,
    )

    return (title_r1c1, p_r1c1, fig_r1c1,
            title_r2c1, p_r2c1, fig_r2c1, 
            title_r2c2, p_r2c2, fig_r2c2,
            title_r3c1, p_r3c1, fig_r3c1,
            title_r4c1, p_r4c1, fig_r4c1,
            title_r5c1, p_r5c1, fig_r5c1)