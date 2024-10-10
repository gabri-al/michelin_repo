import dash
from dash import html, callback, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go

dash.register_page(__name__, path='/', name='Insights', title='Michelin WebApp | Insights')

############################################################################################
# Import functions, settings
from assets.fig_layout import my_figlayout, colorscale_, my_colorbar, chart_colours_, my_legend, center_map_on_data
from assets.filterbar import _filters, _value_for_any

############################################################################################
# Upload data
import pandas as pd
silver_df = pd.read_parquet("data/silver_data.parquet", engine='pyarrow')
#print(silver_df.columns)

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
    center_map = True; zoomed = 1.50
    if _value_for_any in _countries:
        _countries = list(silver_df['Country'].unique())
        center_map = False
    if _value_for_any in _cities:
        _cities = list(silver_df['City'].unique())
    if _value_for_any in _cuisines:
        _cuisines = list(silver_df['Cuisine'].unique())
    plot_df = silver_df.loc[
        (silver_df['Country'].isin(_countries)) & (silver_df['City'].isin(_cities)) & (silver_df['Cuisine'].isin(_cuisines))
        & (silver_df['Award'].isin(_awards)) & (silver_df['Price_score'].isin(_prices)), :]
    # print(len(plot_df))

    ## Generate main Scatter Map Row1 Col1
    title_r1c1 = 'Restaurants Overview'
    p_r1c1 = ''
    fig_r1c1 = go.Figure(
                layout=my_figlayout,
                data = go.Scattergeo( # https://plotly.com/python/scatter-plots-on-maps/
                    lat = plot_df['Latitude'],
                    lon = plot_df['Longitude'],
                )
        )
    if center_map:
        fig_r1c1.update_geos(center={"lat": center_map_on_data(plot_df)[0],"lon": center_map_on_data(plot_df)[1]}, projection = {"scale": zoomed + 20})

    ## Generate map Row1 Col1
    title_r2c1 = 'Restaurants by country'
    p_r2c1 = 'Michelin guide entries count by country'    
    map_df = plot_df.groupby(plot_df['Country']).agg(Res_count = ('Res_ID', 'count')).reset_index()
    fig_r2c1 = go.Figure(
                layout=my_figlayout,
                data=go.Choropleth(
                    locations=map_df['Country'],  # Spatial coordinates
                    z=map_df['Res_count'],  # Data to be color-coded
                    locationmode='country names', 
                    colorscale=colorscale_,  # Color scale for the map
                    colorbar = my_colorbar
                )
        )
    if center_map:
        fig_r2c1.update_geos(center={"lat": center_map_on_data(plot_df)[0],"lon": center_map_on_data(plot_df)[1]}, projection = {"scale": zoomed})

    ## Generate map Row1 Col2
    title_r2c2 = 'Stars by country'
    p_r2c2 = 'Sum of Michelin Stars by country'    
    map_df = plot_df.groupby(plot_df['Country']).agg(Star_sum = ('Stars_score', 'sum')).reset_index()
    fig_r2c2 = go.Figure(
                layout=my_figlayout,
                data=go.Choropleth(
                    locations=map_df['Country'],  # Spatial coordinates
                    z=map_df['Star_sum'],  # Data to be color-coded
                    locationmode='country names', 
                    colorscale=colorscale_,  # Color scale for the map
                    colorbar = my_colorbar
                )
        )
    if center_map:
        fig_r2c2.update_geos(center={"lat": center_map_on_data(plot_df)[0],"lon": center_map_on_data(plot_df)[1]}, projection = {"scale": zoomed})

    ## Generate histogram Row3 Col1
    title_r3c1 = 'Popular Cuisines'
    p_r3c1 = 'Count of Restaurants by Awards and Cuisine - Showing top 50 cuisines'
    data_grouped = plot_df.groupby(['Cuisine_l1', 'Award']).agg(Count = ('Res_ID', 'count')).reset_index()
    data_grouped = data_grouped.pivot(columns = 'Award', index = 'Cuisine_l1', values = 'Count').fillna(0.).reset_index()
    zeros_ = [0.] * len(data_grouped)
    columns_ = ['Selected Restaurants', 'Bib Gourmand', '1 Star', '2 Stars', '3 Stars']
    for c in columns_:
        if c not in data_grouped.columns:
            data_grouped[c] = zeros_
    data_grouped['Restaurant_count'] = data_grouped['1 Star'] + data_grouped['2 Stars'] + data_grouped['3 Stars'] + data_grouped['Bib Gourmand'] + data_grouped['Selected Restaurants']
    data_grouped = data_grouped.sort_values(by = 'Restaurant_count', ascending = False).iloc[:50]
    fig_r3c1 = go.Figure(layout=my_figlayout)
    fig_r3c1_traces = dict() # Dictionary with traces names and colours
    for i in enumerate(columns_):
        fig_r3c1_traces[i[1]] = 'gradient-red-0' + str( i[0] + 1 )
    for key, value in fig_r3c1_traces.items():
        fig_r3c1.add_trace(
            go.Histogram(
                x=data_grouped['Cuisine_l1'],
                y=data_grouped[key],
                marker_color=chart_colours_[value],
                histfunc="sum",
                name=key)
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
            marker_color=chart_colours_['dark-pink'],
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
    #print(data_grouped.head())
    fig_r5c1 = go.Figure(layout=my_figlayout)
    fig_r5c1_traces = dict() # Dictionary with traces names and colours
    for i in enumerate(columns_):
        fig_r5c1_traces[i[1] + ' Ratio'] = 'gradient-red-0' + str( i[0] + 2 )
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