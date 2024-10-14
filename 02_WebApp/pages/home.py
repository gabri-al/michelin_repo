import dash
from dash import html, callback, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go

dash.register_page(__name__, path='/', name='Insights', title='Michelin WebApp | Insights')

############################################################################################
# Import functions, settings
from assets.fig_layout import (country_geojson, my_figlayout, my_map_layout, my_map_trace, my_colorscale, my_colorbar2,
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

    ## Maps on Row 3
     dbc.Row([
        dbc.Col([
            html.Div([
                html.H2(id='title-003', className='titles-h2'),
                html.P(id='p-003', className = 'charts-p'),
                dcc.Loading(id='loading-003', type='default',
                        children = dcc.Graph(id = 'fig-003'))
            ], className = 'chart-div')
        ], width = 12)
    ], className = 'chart-row'),

    ## Maps on Row 4
     dbc.Row([
        dbc.Col([
            html.Div([
                html.H2(id='title-004', className='titles-h2'),
                html.P(id='p-004', className = 'charts-p'),
                dcc.Loading(id='loading-004', type='default',
                        children = dcc.Graph(id = 'fig-004'))
            ], className = 'chart-div')
        ], width = 12)
    ], className = 'chart-row'),

    ## Maps on Row 5
     dbc.Row([
        dbc.Col([
            html.Div([
                html.H2(id='title-005', className='titles-h2'),
                html.P(id='p-005', className = 'charts-p'),
                dcc.Loading(id='loading-005', type='default',
                        children = dcc.Graph(id = 'fig-005'))
            ], className = 'chart-div')
        ], width = 12)
    ], className = 'chart-row'),

    ## Hist on Row 6
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H2(id='title-006', className='titles-h2'),
                html.P(id='p-006', className = 'charts-p'),
                dcc.Loading(id='loading_r3c1', type='default',
                        children = dcc.Graph(id = 'fig-006'))
            ], className = 'chart-div')
        ], width = 12)
    ], className = 'chart-row'),

    ## Hist on Row 7
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H2(id='title-007', className='titles-h2'),
                html.P(id='p-007', className = 'charts-p'),
                dcc.Loading(id='loading_r4c1', type='default',
                        children = dcc.Graph(id = 'fig-007'))
            ], className = 'chart-div')
        ], width = 12)
    ], className = 'chart-row'),

    ## Hist on Row 5
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H2(id='title-008', className='titles-h2'),
                html.P(id='p-008', className = 'charts-p'),
                dcc.Loading(id='loading_r5c1', type='default',
                        children = dcc.Graph(id = 'fig-008'))
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
    # Outputs for Row 1
    Output(component_id='title-001', component_property='children'),
    Output(component_id='p-001', component_property='children'),
    Output(component_id='fig-001', component_property='figure'),
    # Outputs for Row 2
    Output(component_id='title-002', component_property='children'),
    Output(component_id='p-002', component_property='children'),
    Output(component_id='fig-002', component_property='figure'),
    # Outputs for Row 3
    Output(component_id='title-003', component_property='children'),
    Output(component_id='p-003', component_property='children'),
    Output(component_id='fig-003', component_property='figure'),
    # Outputs for Row 4
    Output(component_id='title-004', component_property='children'),
    Output(component_id='p-004', component_property='children'),
    Output(component_id='fig-004', component_property='figure'),    
    # Outputs for Row 5
    Output(component_id='title-005', component_property='children'),
    Output(component_id='p-005', component_property='children'),
    Output(component_id='fig-005', component_property='figure'),
    # Outputs for Row 6
    Output(component_id='title-006', component_property='children'),
    Output(component_id='p-006', component_property='children'),
    Output(component_id='fig-006', component_property='figure'),
    # Outputs for Row 7
    Output(component_id='title-007', component_property='children'),
    Output(component_id='p-007', component_property='children'),
    Output(component_id='fig-007', component_property='figure'),   
    # Outputs for Row 8
    Output(component_id='title-008', component_property='children'),
    Output(component_id='p-008', component_property='children'),
    Output(component_id='fig-008', component_property='figure'),        
    # Inputs
    Input(component_id='country-dropdown', component_property='value'),
    Input(component_id='city-dropdown', component_property='value'),
    Input(component_id='cuisine-dropdown', component_property='value'),
    Input(component_id='award-dropdown', component_property='value'),
    Input(component_id='price-dropdown', component_property='value')
)
def plot_data(_countries, _cities, _cuisines, _awards, _prices):
    ## Filter data
    zoom_map = True; zoomed = 2
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

    ## Generate map3
    title_003 = 'Stars by country'
    p_003 = 'What are the countries with most stars? This map shows the sum of Michelin Stars by country'    
    map_df = plot_df.groupby(['Country','Country_Code_ISO3']).agg(Star_sum = ('Stars_score', 'sum')).reset_index().sort_values(by='Star_sum', ascending=False)
    hover_text=[]; rank_ = 1
    for idx, row in map_df.iterrows():
        hover_text.append(("<i>Country</i>: {}<br>"+
                           "<i>Tot Stars</i>: {}<br>"+
                           "<i>Rank</i>: {}"+
                            "<extra></extra>").format(row['Country'], row['Star_sum'], rank_))
        rank_ += 1
    map_df['Hovertemplate'] = hover_text
    fig_003 = go.Figure(
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
    fig_003.update_maps(my_map_layout)
    fig_003.update_maps(center={"lat": center_map_on_data(plot_df)[0],"lon": center_map_on_data(plot_df)[1]})
    if zoom_map:
        fig_003.update_maps(zoom = zoomed)

    ## Generate map4
    title_004 = 'Cuisines by country'
    p_004 = 'What countries have most cuisines? This map shows a score, calculated as the ratio of distinct cuisines by the nr. of restaurants'
    cuisine_df1 = plot_df.groupby(['Country','Country_Code_ISO3','Cuisine_l1']).agg(Res_count = ('Res_ID', 'count')).reset_index().rename(columns={"Cuisine_l1": "Cuisine"})
    cuisine_df2 = plot_df.groupby(['Country','Country_Code_ISO3','Cuisine_l2']).agg(Res_count = ('Res_ID', 'count')).reset_index().rename(columns={"Cuisine_l2": "Cuisine"})
    cuisine_df3 = pd.concat([cuisine_df1, cuisine_df2], ignore_index=True)
    cuisine_df = cuisine_df3.groupby(['Country','Country_Code_ISO3']).agg(Cuisine_count = ('Cuisine', 'nunique')).reset_index().sort_values(by='Cuisine_count', ascending=False)
    res_df = plot_df.groupby(['Country','Country_Code_ISO3']).agg(Res_count = ('Res_ID', 'count')).reset_index()
    map_df = cuisine_df.merge(res_df, left_on='Country_Code_ISO3', right_on='Country_Code_ISO3', suffixes=('', '_b')).reset_index()
    map_df['Ratio'] = map_df['Cuisine_count'] / map_df['Res_count']
    map_df.sort_values(by='Ratio', ascending=False, inplace=True)
    #print(len(cuisine_df)); print(len(map_df))
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
    fig_004 = go.Figure(
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
    fig_004.update_maps(my_map_layout)
    fig_004.update_maps(center={"lat": center_map_on_data(plot_df)[0],"lon": center_map_on_data(plot_df)[1]})
    if zoom_map:
        fig_004.update_maps(zoom = zoomed)

    ## Generate map5
    title_005 = 'Price Score by Country'
    p_005 = 'How expensive are different countries? This map shows a score, calculated as a weigthed average of restaurant counts in each price category. A higher scoring country will have more higher-priced restaurants'
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
    fig_005 = go.Figure(
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
    fig_005.update_maps(my_map_layout)
    fig_005.update_maps(center={"lat": center_map_on_data(plot_df)[0],"lon": center_map_on_data(plot_df)[1]})
    if zoom_map:
        fig_005.update_maps(zoom = zoomed)    

    ## Generate histogram6
    title_006 = 'Popular Cuisines'
    p_006 = 'This barchart shows the total count of restaurants by cuisine split by award type, for the most frequent 50 cuisines'
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
    fig_006 = go.Figure(layout=my_figlayout)
    fig_006_traces = dict() # Dictionary with traces names and colours
    for i in enumerate(columns_):
        fig_006_traces[i[1]] = 'my-palette-0' + str( i[0] + 1 )
    for key, value in fig_006_traces.items():
        fig_006.add_trace(
            go.Histogram(
                x=data_grouped['Cuisine_l1'],
                y=data_grouped[key],
                marker_color=chart_colours_[value],
                histfunc="sum",
                name=key,
                hovertemplate = data_grouped['Hovertemplate'])
        )
    fig_006.update_layout(
        bargap=.6, # gap between bars of adjacent location coordinates
        barmode='stack',
        legend = my_legend,
    )

    ## Generate histogram Row4 Col1
    title_007 = 'Stars Propensity by Cuisine'
    p_007 = 'What are the most awarded cuisines? This barchart shows the ratio between the sum of stars and the nr. of restaurants, for the most frequent 50 cuisines'
    data_grouped = plot_df.groupby(plot_df['Cuisine_l1']).agg(Stars_count = ('Stars_score', 'sum'),
                                                              Restaurant_count = ('Res_ID', 'count')).reset_index()
    data_grouped['Star Ratio'] = data_grouped['Stars_count'] / data_grouped['Restaurant_count']
    data_grouped = data_grouped.loc[data_grouped['Restaurant_count'] >= 10, :] # Filter outliers    
    data_grouped = data_grouped.sort_values(by = 'Star Ratio', ascending = False).iloc[:50]
    hover_text=[]
    for idx, row in data_grouped.iterrows():
        hover_text.append(("<i>Cuisine</i>: {}<br>"+
                           "<i>Restaurants Count</i>: {}<br>"+
                           "<i>Tot Stars</i>: {}<br>"+
                            "<i>Stars/Restaurant Ratio</i>: {:.2%}"+
                            "<extra></extra>").format(row['Cuisine_l1'], row['Restaurant_count'], row['Stars_count'], row['Star Ratio']))
    data_grouped['Hovertemplate'] = hover_text
    fig_007 = go.Figure(layout=my_figlayout)
    fig_007.add_trace(
        go.Histogram(
            x=data_grouped['Cuisine_l1'],
            y=data_grouped['Star Ratio'],
            marker_color=chart_colours_['my-palette-02'],
            histfunc="sum",
            name='Stars/Restaurants',
            hovertemplate = data_grouped['Hovertemplate'])
    )
    fig_007.update_layout(
        bargap=.6, # gap between bars of adjacent location coordinates
    )

    ## Generate histogram Row5 Col1
    title_008 = 'Price ratio by Cuisine'
    p_008 = 'What are the most expensive cuisines? This barchart shows the percentage of restaurants in each price category, for the most frequent 50 cuisines'
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
    fig_008 = go.Figure(layout=my_figlayout)
    fig_008_traces = dict() # Dictionary with traces names and colours
    for i in enumerate(columns_):
        fig_008_traces[i[1] + ' Ratio'] = 'my-palette-0' + str( i[0] + 2 )
    for key, value in fig_008_traces.items():
        fig_008.add_trace(
            go.Histogram(
                x=data_grouped['Cuisine_l1'],
                y=data_grouped[key],
                marker_color=chart_colours_[value],
                histfunc="sum",
                name=key,
                hovertemplate = data_grouped['Hovertemplate'])
        )
    fig_008.update_layout(
        bargap=.6, # gap between bars of adjacent location coordinates
        barmode='stack',
        legend = my_legend,
    )

    return (title_001, p_001, fig_001,
            title_002, p_002, fig_002, 
            title_003, p_003, fig_003,
            title_004, p_004, fig_004,
            title_005, p_005, fig_005,
            title_006, p_006, fig_006,
            title_007, p_007, fig_007,
            title_008, p_008, fig_008)