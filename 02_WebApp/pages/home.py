import dash
from dash import html, callback, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go

dash.register_page(__name__, path='/', order = 1, name='Insights', title='Michelin WebApp | Insights')

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

    ## Maps on Row 1
     dbc.Row([
        dbc.Col([
            html.Div([
                html.H2(id='title-001', className='titles-h2'),
                html.P(id='p-001', className = 'charts-p'),
                dcc.Loading(id='loading-001', type='default',
                        children = dcc.Graph(id = 'fig-001'))
            ], className = 'chart-div')
        ], width = 12)
    ], className = 'chart-row'),   

    ## Maps on Row 2
     dbc.Row([
        dbc.Col([
            html.Div([
                html.H2(id='title-002', className='titles-h2'),
                html.P(id='p-002', className = 'charts-p'),
                dcc.Loading(id='loading-002', type='default',
                        children = dcc.Graph(id = 'fig-002'))
            ], className = 'chart-div')
        ], width = 12)
    ], className = 'chart-row'),   

    ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
    ### ### ### ### ### Awards Section
    ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
    dbc.Row([
        dbc.Col([
            html.Button([html.I(id='reveal-awards-icon')], id='reveal-awards', n_clicks=0, className='my-button'),
            html.H2("Insights by Award", className='titles-expand-h2'),
        ], className = 'button-col', width = 11),
        dbc.Col(width = 1)
    ], className = 'expanding-title-row'),

    ## Award 001 - Stars by country
     dbc.Row([
        dbc.Col([
            html.Div([
                html.H2(id='award-title-001', className='titles-h2'),
                html.P(id='award-p-001', className = 'charts-p'),
                dcc.Loading(id='award-loading-001', type='default',
                        children = dcc.Graph(id = 'award-fig-001'))
            ], className = 'chart-div')
        ], width = 12)
    ], className = 'chart-row', id = 'award-001-row'),    
    
    ## Award 002 - Star Propensity by country
     dbc.Row([
        dbc.Col([
            html.Div([
                html.H2(id='award-title-002', className='titles-h2'),
                html.P(id='award-p-002', className = 'charts-p'),
                dcc.Loading(id='award-loading-002', type='default',
                        children = dcc.Graph(id = 'award-fig-002'))
            ], className = 'chart-div')
        ], width = 12)
    ], className = 'chart-row', id = 'award-002-row'),    

    ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
    ### ### ### ### ### Cuisine Section
    ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
    dbc.Row([
        dbc.Col([
            html.Button([html.I(id='reveal-cuisines-icon')], id='reveal-cuisines', n_clicks=0, className='my-button'),
            html.H2("Insights by Cuisines", className='titles-expand-h2'),
        ], className = 'button-col', width = 11),
        dbc.Col(width = 1)
    ], className = 'expanding-title-row'),

    ## Cuisine 001 - Cuisines by country
     dbc.Row([
        dbc.Col([
            html.Div([
                html.H2(id='cuisine-title-001', className='titles-h2'),
                html.P(id='cuisine-p-001', className = 'charts-p'),
                dcc.Loading(id='cuisine-loading-001', type='default',
                        children = dcc.Graph(id = 'cuisine-fig-001'))
            ], className = 'chart-div')
        ], width = 12)
    ], className = 'chart-row', id = 'cuisine-001-row'),

    ## Cuisine 002 - Popular Cuisines
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H2(id='cuisine-title-002', className='titles-h2'),
                html.P(id='cuisine-p-002', className = 'charts-p'),
                dcc.Loading(id='cuisine-loading-002', type='default',
                        children = dcc.Graph(id = 'cuisine-fig-002'))
            ], className = 'chart-div')
        ], width = 12)
    ], className = 'chart-row', id = 'cuisine-002-row'),

    ## Cuisine 003 - Star Propensity by Cuisine
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H2(id='cuisine-title-003', className='titles-h2'),
                html.P(id='cuisine-p-003', className = 'charts-p'),
                dcc.Loading(id='cuisine-loading-003', type='default',
                        children = dcc.Graph(id = 'cuisine-fig-003'))
            ], className = 'chart-div')
        ], width = 12)
    ], className = 'chart-row', id = 'cuisine-003-row'),

    ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
    ### ### ### ### ### Price Section
    ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
    dbc.Row([
        dbc.Col([
            html.Button([html.I(id='reveal-prices-icon')], id='reveal-prices', n_clicks=0, className='my-button'),
            html.H2("Insights by Price", className='titles-expand-h2'),
        ], className = 'button-col', width = 11),
        dbc.Col(width = 1)
    ], className = 'expanding-title-row'),

    ## Price 001 - Price Score by Country
     dbc.Row([
        dbc.Col([
            html.Div([
                html.H2(id='price-title-001', className='titles-h2'),
                html.P(id='price-p-001', className = 'charts-p'),
                dcc.Loading(id='price-loading-001', type='default',
                        children = dcc.Graph(id = 'price-fig-001'))
            ], className = 'chart-div')
        ], width = 12)
    ], className = 'chart-row', id = 'price-001-row'),

    ## Price 002 - Price Ratio by Cuisine
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H2(id='price-title-002', className='titles-h2'),
                html.P(id='price-p-002', className = 'charts-p'),
                dcc.Loading(id='price-loading-002', type='default',
                        children = dcc.Graph(id = 'price-fig-002'))
            ], className = 'chart-div')
        ], width = 12)
    ], className = 'chart-row', id = 'price-002-row'),

    ## Price 003 - Price Ratio by Cuisine
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H2(id='price-title-003', className='titles-h2'),
                html.P(id='price-p-003', className = 'charts-p'),
                dcc.Loading(id='price-loading-003', type='default',
                        children = dcc.Graph(id = 'price-fig-003'))
            ], className = 'chart-div')
        ], width = 12)
    ], className = 'chart-row', id = 'price-003-row'),    

])

### PAGE CALLBACKS ###############################################################################################################

##################### UPDATES BASED ON EXPANDING BUTTONS
### Award
@callback(
        Output(component_id='award-001-row', component_property='style'),
        Output(component_id='award-002-row', component_property='style'),
        Output(component_id='reveal-awards-icon', component_property='className'),
        Input(component_id='reveal-awards', component_property='n_clicks')
)
def display_award_section(_nclicks):
    if _nclicks is None or _nclicks == 0 or _nclicks % 2 == 0:
        return {'display': 'None'}, {'display': 'None'}, 'fa-solid fa-chevron-right me-3 fa-1x'
    else:
        return {}, {}, 'fa-solid fa-chevron-down me-3 fa-1x'

### Cuisines
@callback(
        Output(component_id='cuisine-001-row', component_property='style'),
        Output(component_id='cuisine-002-row', component_property='style'),
        Output(component_id='cuisine-003-row', component_property='style'),
        Output(component_id='reveal-cuisines-icon', component_property='className'),
        Input(component_id='reveal-cuisines', component_property='n_clicks')
)
def display_cuisine_section(_nclicks):
    if _nclicks is None or _nclicks == 0 or _nclicks % 2 == 0:
        return {'display': 'None'}, {'display': 'None'}, {'display': 'None'}, 'fa-solid fa-chevron-right me-3 fa-1x'
    else:
        return {}, {}, {}, 'fa-solid fa-chevron-down me-3 fa-1x'

### Prices
@callback(
        Output(component_id='price-001-row', component_property='style'),
        Output(component_id='price-002-row', component_property='style'),
        Output(component_id='price-003-row', component_property='style'),
        Output(component_id='reveal-prices-icon', component_property='className'),
        Input(component_id='reveal-prices', component_property='n_clicks')
)
def display_price_section(_nclicks):
    if _nclicks is None or _nclicks == 0 or _nclicks % 2 == 0:
        return {'display': 'None'}, {'display': 'None'}, {'display': 'None'}, 'fa-solid fa-chevron-right me-3 fa-1x'
    else:
        return {}, {}, {}, 'fa-solid fa-chevron-down me-3 fa-1x'

##################### UPDATES ON FIGS
@callback(
    # Outputs for Row 1
    Output(component_id='title-001', component_property='children'),
    Output(component_id='p-001', component_property='children'),
    Output(component_id='fig-001', component_property='figure'),
    # Outputs for Row 2
    Output(component_id='title-002', component_property='children'),
    Output(component_id='p-002', component_property='children'),
    Output(component_id='fig-002', component_property='figure'),

    # Outputs for Award 1
    Output(component_id='award-title-001', component_property='children'),
    Output(component_id='award-p-001', component_property='children'),
    Output(component_id='award-fig-001', component_property='figure'),
    # Outputs for Award 2
    Output(component_id='award-title-002', component_property='children'),
    Output(component_id='award-p-002', component_property='children'),
    Output(component_id='award-fig-002', component_property='figure'),    

    # Outputs for Cuisine 1
    Output(component_id='cuisine-title-001', component_property='children'),
    Output(component_id='cuisine-p-001', component_property='children'),
    Output(component_id='cuisine-fig-001', component_property='figure'),
    # Outputs for Cuisine 2
    Output(component_id='cuisine-title-002', component_property='children'),
    Output(component_id='cuisine-p-002', component_property='children'),
    Output(component_id='cuisine-fig-002', component_property='figure'),
    # Outputs for Cuisine 3
    Output(component_id='cuisine-title-003', component_property='children'),
    Output(component_id='cuisine-p-003', component_property='children'),
    Output(component_id='cuisine-fig-003', component_property='figure'),   

    # Outputs for Price 1
    Output(component_id='price-title-001', component_property='children'),
    Output(component_id='price-p-001', component_property='children'),
    Output(component_id='price-fig-001', component_property='figure'),
    # Outputs for Price 2
    Output(component_id='price-title-002', component_property='children'),
    Output(component_id='price-p-002', component_property='children'),
    Output(component_id='price-fig-002', component_property='figure'),
    # Outputs for Price 3
    Output(component_id='price-title-003', component_property='children'),
    Output(component_id='price-p-003', component_property='children'),
    Output(component_id='price-fig-003', component_property='figure'),            
    
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
    title_001 = 'Restaurants Overview'
    p_001 = ''
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
    fig_001 = go.Figure(layout = my_figlayout)
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
            fig_001.add_trace(go.Scattermap(my_map_trace_here))
    fig_001.update_maps(my_map_layout)
    fig_001.update_maps(center={"lat": center_map_on_data(plot_df)[0],"lon": center_map_on_data(plot_df)[1]})
    if zoom_map:
        fig_001.update_maps(zoom = zoomed)

    ## Generate map2
    title_002 = 'Restaurants by country'
    p_002 = 'What countries have the most resturants? This map counts Michelin guide entries by country'    
    map_df = plot_df.groupby(['Country','Country_Code_ISO3']).agg(Res_count = ('Res_ID', 'count')).reset_index().sort_values(by='Res_count', ascending=False)
    hover_text=[]; rank_ = 1
    for idx, row in map_df.iterrows():
        hover_text.append(("<i>Country</i>: {}<br>"+
                           "<i>Restaurants</i>: {}<br>"+
                           "<i>Rank</i>: {}"+
                            "<extra></extra>").format(row['Country'], row['Res_count'], rank_))
        rank_ += 1
    map_df['Hovertemplate'] = hover_text
    fig_002 = go.Figure(
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
    fig_002.update_maps(my_map_layout)
    fig_002.update_maps(center={"lat": center_map_on_data(plot_df)[0],"lon": center_map_on_data(plot_df)[1]})
    if zoom_map:
        fig_002.update_maps(zoom = zoomed)

    ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
    ### ### ### ### ### Awards Section
    ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
    ## Award 1
    award_title_001 = 'Stars by country'
    award_p_001 = 'What are the countries with most stars? This map shows the sum of Michelin Stars by country'    
    map_df = plot_df.groupby(['Country','Country_Code_ISO3']).agg(Star_sum = ('Stars_score', 'sum')).reset_index().sort_values(by='Star_sum', ascending=False)
    hover_text=[]; rank_ = 1
    for idx, row in map_df.iterrows():
        hover_text.append(("<i>Country</i>: {}<br>"+
                           "<i>Tot Stars</i>: {}<br>"+
                           "<i>Rank</i>: {}"+
                            "<extra></extra>").format(row['Country'], row['Star_sum'], rank_))
        rank_ += 1
    map_df['Hovertemplate'] = hover_text
    award_fig_001 = go.Figure(
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
    award_fig_001.update_maps(my_map_layout)
    award_fig_001.update_maps(center={"lat": center_map_on_data(plot_df)[0],"lon": center_map_on_data(plot_df)[1]})
    if zoom_map:
        award_fig_001.update_maps(zoom = zoomed)
    
    ## Award 2
    award_title_002 = 'Star Propensity by country'
    award_p_002 = 'Where do restaurants get awarded more? This map shows the ratio of Michelin Stars over Nr. of Restaurants, by country'    
    map_df = plot_df.groupby(['Country','Country_Code_ISO3']).agg(Res_count = ('Res_ID', 'count'), Star_sum = ('Stars_score', 'sum')).reset_index()
    map_df['Star_Ratio'] = map_df['Star_sum'] / map_df['Res_count']
    map_df.sort_values(by='Star_Ratio', ascending=False, inplace=True)
    hover_text=[]; rank_ = 1
    for idx, row in map_df.iterrows():
        hover_text.append(("<i>Country</i>: {}<br>"+
                           "<i>Restaurants</i>: {}<br>"+
                           "<i>Tot Stars</i>: {}<br>"+
                           "<i>Ratio</i>: {:.2%}<br>"+
                           "<i>Rank</i>: {}"+
                            "<extra></extra>").format(row['Country'], row['Res_count'], row['Star_sum'], row['Star_Ratio'], rank_))
        rank_ += 1
    map_df['Hovertemplate'] = hover_text
    award_fig_002 = go.Figure(
        layout = my_figlayout,
        data = go.Choroplethmap( # Using same arguments as https://plotly.com/python-api-reference/generated/plotly.graph_objects.Choroplethmapbox.html
            geojson = country_geojson,
            featureidkey = 'properties.ISO_A3',
            locations = map_df['Country_Code_ISO3'],
            z=map_df['Star_Ratio'],
            colorscale = my_colorscale,
            colorbar = my_colorbar2,
            hovertemplate = map_df['Hovertemplate']
        ))
    award_fig_002.update_maps(my_map_layout)
    award_fig_002.update_maps(center={"lat": center_map_on_data(plot_df)[0],"lon": center_map_on_data(plot_df)[1]})
    if zoom_map:
        award_fig_002.update_maps(zoom = zoomed)

    ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
    ### ### ### ### ### Cuisine Section
    ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
    ## Cuisine 1
    cuisine_title_001 = 'Cuisines by country'
    cuisine_p_001 = 'What countries have most cuisines? This map shows a score, calculated as the ratio of distinct cuisines by the nr. of restaurants'
    cuisine_df1 = plot_df.groupby(['Country','Country_Code_ISO3','Cuisine_l1']).agg(Res_count = ('Res_ID', 'count')).reset_index().rename(columns={"Cuisine_l1": "Cuisine"})
    cuisine_df2 = plot_df.groupby(['Country','Country_Code_ISO3','Cuisine_l2']).agg(Res_count = ('Res_ID', 'count')).reset_index().rename(columns={"Cuisine_l2": "Cuisine"})
    cuisine_df3 = pd.concat([cuisine_df1, cuisine_df2], ignore_index=True)
    cuisine_df = cuisine_df3.groupby(['Country','Country_Code_ISO3']).agg(Cuisine_count = ('Cuisine', 'nunique')).reset_index().sort_values(by='Cuisine_count', ascending=False)
    res_df = plot_df.groupby(['Country','Country_Code_ISO3']).agg(Res_count = ('Res_ID', 'count')).reset_index()
    map_df = cuisine_df.merge(res_df, left_on='Country_Code_ISO3', right_on='Country_Code_ISO3', suffixes=('', '_b')).reset_index()
    map_df['Ratio'] = map_df['Cuisine_count'] / map_df['Res_count']
    map_df.sort_values(by='Ratio', ascending=False, inplace=True)
    hover_text=[]; rank_ = 1
    for idx, row in map_df.iterrows():
        hover_text.append(("<i>Country</i>: {}<br>"+
                           "<i>Distinct Cuisines</i>: {}<br>"+
                           "<i>Restaurants</i>: {}<br>"+
                           "<i>Ratio</i>: {:.2}<br>"+
                           "<i>Rank</i>: {}"+
                           "<extra></extra>").format(row['Country'], row['Cuisine_count'], row['Res_count'], row['Ratio'], rank_))
        rank_ += 1
    map_df['Hovertemplate'] = hover_text
    cuisine_fig_001 = go.Figure(
        layout = my_figlayout,
        data = go.Choroplethmap( # Using same arguments as https://plotly.com/python-api-reference/generated/plotly.graph_objects.Choroplethmapbox.html
            geojson = country_geojson,
            featureidkey = 'properties.ISO_A3',
            locations = map_df['Country_Code_ISO3'],
            z=map_df['Ratio'],
            colorscale = my_colorscale,
            colorbar = my_colorbar2,
            hovertemplate = map_df['Hovertemplate']
        ))
    cuisine_fig_001.update_maps(my_map_layout)
    cuisine_fig_001.update_maps(center={"lat": center_map_on_data(plot_df)[0],"lon": center_map_on_data(plot_df)[1]})
    if zoom_map:
        cuisine_fig_001.update_maps(zoom = zoomed)

    ## Cuisine 2
    cuisine_title_002 = 'Popular Cuisines'
    cuisine_p_002 = 'This barchart shows the total count of restaurants by cuisine split by award type, for the most frequent 50 cuisines'
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
    cuisine_fig_002 = go.Figure(layout=my_figlayout)
    cuisine_fig_002_traces = dict() # Dictionary with traces names and colours
    for i in enumerate(columns_):
        cuisine_fig_002_traces[i[1]] = 'my-palette-0' + str( i[0] + 1 )
    for key, value in cuisine_fig_002_traces.items():
        cuisine_fig_002.add_trace(
            go.Histogram(
                x=data_grouped['Cuisine_l1'],
                y=data_grouped[key],
                marker_color=chart_colours_[value],
                histfunc="sum",
                name=key,
                hovertemplate = data_grouped['Hovertemplate'])
        )
    cuisine_fig_002.update_layout(
        bargap=.6, # gap between bars of adjacent location coordinates
        barmode='stack',
        legend = my_legend,
    )

    ## Cuisine 3
    cuisine_title_003 = 'Star Propensity by Cuisine'
    cuisine_p_003 = 'Which cuisines are the most awarded? This barchart shows the ratio between the sum of stars and the nr. of restaurants, for the most frequent 50 cuisines'
    data_grouped = plot_df.groupby(plot_df['Cuisine_l1']).agg(Stars_count = ('Stars_score', 'sum'),
                                                              Restaurant_count = ('Res_ID', 'count')).reset_index()
    data_grouped['Star Ratio'] = data_grouped['Stars_count'] / data_grouped['Restaurant_count']
    if len(data_grouped) > 50:  # Filter outliers if it makes sense
        data_grouped = data_grouped.loc[data_grouped['Restaurant_count'] >= 5, :]
    data_grouped = data_grouped.sort_values(by = 'Star Ratio', ascending = False).iloc[:50]
    hover_text=[]
    for idx, row in data_grouped.iterrows():
        hover_text.append(("<i>Cuisine</i>: {}<br>"+
                           "<i>Restaurants Count</i>: {}<br>"+
                           "<i>Tot Stars</i>: {}<br>"+
                            "<i>Stars/Restaurant Ratio</i>: {:.2%}"+
                            "<extra></extra>").format(row['Cuisine_l1'], row['Restaurant_count'], row['Stars_count'], row['Star Ratio']))
    data_grouped['Hovertemplate'] = hover_text
    cuisine_fig_003 = go.Figure(layout=my_figlayout)
    cuisine_fig_003.add_trace(
        go.Histogram(
            x=data_grouped['Cuisine_l1'],
            y=data_grouped['Star Ratio'],
            marker_color=chart_colours_['my-palette-02'],
            histfunc="sum",
            name='Stars/Restaurants',
            hovertemplate = data_grouped['Hovertemplate'])
    )
    cuisine_fig_003.update_layout(
        bargap=.6, # gap between bars of adjacent location coordinates
    )

    ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
    ### ### ### ### ### Price Section
    ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
    ## Price 1
    price_title_001 = 'Price Score by Country'
    price_p_001 = 'How expensive are different countries? This map shows a score, calculated as a weigthed average of restaurant counts in each price category. A higher scoring country will have more higher-priced restaurants'
    data_grouped = plot_df.groupby(['Country','Country_Code_ISO3','Price_score']).agg(Count = ('Res_ID', 'count')).reset_index()
    data_grouped = data_grouped.pivot(columns = 'Price_score', index = ['Country','Country_Code_ISO3'], values = 'Count').fillna(0.).reset_index()
    zeros_ = [0.] * len(data_grouped)
    columns_ = ['$', '$$', '$$$', '$$$$']
    data_grouped = data_grouped.rename(columns = {i+1: columns_[i] for i in range(4)})
    for c in columns_:
        if c not in data_grouped.columns:
            data_grouped[c] = zeros_
    for c in columns_:
        data_grouped[c] = data_grouped[c].astype(int)            
    data_grouped['Restaurant_count'] = (data_grouped['$'] + data_grouped['$$'] + data_grouped['$$$'] + data_grouped['$$$$']).astype(int)
    data_grouped['Price_Score'] = ((data_grouped['$']*1/10) + (data_grouped['$$']*2/10) + (data_grouped['$$$']*3/10) + (data_grouped['$$$$']*4/10)) / data_grouped['Restaurant_count']
    map_df = data_grouped.sort_values(by='Price_Score', ascending=False)
    hover_text=[]; rank_ = 1
    for idx, row in map_df.iterrows():
        hover_text.append(("<i>Country</i>: {}<br>"+
                           "<i>Tot Restaurants</i>: {}<br>"+
                           "<i>$ Restaurants</i>: {}<br>"+
                           "<i>$$ Restaurants</i>: {}<br>"+
                           "<i>$$$ Restaurants</i>: {}<br>"+
                           "<i>$$$$ Restaurants</i>: {}<br>"+
                           "<i>Price Score</i>: {:.2}<br>"+
                           "<i>Rank</i>: {}"+
                           "<extra></extra>").format(row['Country'], row['Restaurant_count'], row['$'], row['$$'], row['$$$'], row['$$$$'], row['Price_Score'], rank_))
        rank_ += 1
    map_df['Hovertemplate'] = hover_text
    price_fig_001 = go.Figure(
        layout = my_figlayout,
        data = go.Choroplethmap( # Using same arguments as https://plotly.com/python-api-reference/generated/plotly.graph_objects.Choroplethmapbox.html
            geojson = country_geojson,
            featureidkey = 'properties.ISO_A3',
            locations = map_df['Country_Code_ISO3'],
            z=map_df['Price_Score'],
            colorscale = my_colorscale,
            colorbar = my_colorbar2,
            hovertemplate = map_df['Hovertemplate']
        ))
    price_fig_001.update_maps(my_map_layout)
    price_fig_001.update_maps(center={"lat": center_map_on_data(plot_df)[0],"lon": center_map_on_data(plot_df)[1]})
    if zoom_map:
        price_fig_001.update_maps(zoom = zoomed)

    ## Price 2
    price_title_002 = 'Price Category by Cuisine'
    price_p_002 = 'Which cuisines are the most expensive? This barchart shows the percentage of restaurants in each price category, for the most frequent 50 cuisines'
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
    price_fig_002 = go.Figure(layout=my_figlayout)
    price_fig_002_traces = dict() # Dictionary with traces names and colours
    for i in enumerate(columns_):
        price_fig_002_traces[i[1] + ' Ratio'] = 'my-palette-0' + str( i[0] + 2 )
    for key, value in price_fig_002_traces.items():
        price_fig_002.add_trace(
            go.Histogram(
                x=data_grouped['Cuisine_l1'],
                y=data_grouped[key],
                marker_color=chart_colours_[value],
                histfunc="sum",
                name=key,
                hovertemplate = data_grouped['Hovertemplate'])
        )
    price_fig_002.update_layout(
        bargap=.6, # gap between bars of adjacent location coordinates
        barmode='stack',
        legend = my_legend,
    )

    ## Price 3
    price_title_003 = 'Price Category by Award'
    price_p_003 = 'Are top-awarded restaurants the most expensive? This barchart shows the percentage of restaurants in each price category, by award'
    data_grouped = plot_df.groupby(['Award', 'Price_score']).agg(Count = ('Res_ID', 'count')).reset_index()
    data_grouped = data_grouped.pivot(columns = 'Price_score', index = 'Award', values = 'Count').fillna(0.).reset_index()
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
        hover_text.append(("<i>Award</i>: {}<br>"+
                           "<i>Restaurants Count</i>: {}<br>"+
                           "<i>$ Restaurants</i>: {}  ({:.2%})<br>"+
                           "<i>$$ Restaurants</i>: {}  ({:.2%})<br>"+
                           "<i>$$$ Restaurants</i>: {}  ({:.2%})<br>"+
                           "<i>$$$$ Restaurants</i>: {}  ({:.2%})<br>"+
                           "<extra></extra>").format(row['Award'], row['Restaurant_count'], row['$'], row['$ Ratio'], row['$$'], row['$$ Ratio'],
                                                     row['$$$'], row['$$$ Ratio'], row['$$$$'], row['$$$$ Ratio']))
    data_grouped['Hovertemplate'] = hover_text
    awards_ = ['Selected Restaurants', 'Bib Gourmand', '1 Star', '2 Stars', '3 Stars']
    data_grouped['Award'] = pd.Categorical(data_grouped['Award'], categories = awards_) # apply custom sorting
    data_grouped.sort_values(by='Award', inplace=True)
    price_fig_003 = go.Figure(layout=my_figlayout)
    price_fig_003_traces = dict() # Dictionary with traces names and colours
    for i in enumerate(columns_):
        price_fig_003_traces[i[1] + ' Ratio'] = 'my-palette-0' + str( i[0] + 2 )
    for key, value in price_fig_003_traces.items():
        price_fig_003.add_trace(
            go.Histogram(
                x=data_grouped['Award'],
                y=data_grouped[key],
                marker_color=chart_colours_[value],
                histfunc="sum",
                name=key,
                hovertemplate = data_grouped['Hovertemplate'])
        )
    price_fig_003.update_layout(
        bargap=.6, # gap between bars of adjacent location coordinates
        barmode='stack',
        legend = my_legend,
    )

    return (title_001, p_001, fig_001,
            title_002, p_002, fig_002, 
            award_title_001, award_p_001, award_fig_001,
            award_title_002, award_p_002, award_fig_002,
            cuisine_title_001, cuisine_p_001, cuisine_fig_001,
            cuisine_title_002, cuisine_p_002, cuisine_fig_002,
            cuisine_title_003, cuisine_p_003, cuisine_fig_003,
            price_title_001, price_p_001, price_fig_001,
            price_title_002, price_p_002, price_fig_002,
            price_title_003, price_p_003, price_fig_003)