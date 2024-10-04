import dash
from dash import html, callback, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go

dash.register_page(__name__, path='/', name='Home', title='Michelin WebApp | Home')

############################################################################################
# Import functions, settings
from assets.fig_layout import my_figlayout, colorscale_, my_colorbar, chart_colours_
from assets.filterbar import _filters, _value_for_any

############################################################################################
# Upload data
import pandas as pd
silver_df = pd.read_parquet("data/silver_data.parquet", engine='pyarrow')

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
        ], width = 6),
        dbc.Col([
            html.Div([
                html.H2(id='title-r1c2', className='titles-h2'),
                html.P(id='p-r1c2', className = 'charts-p'),
                dcc.Loading(id='loading_r1c2', type='default',
                            children = dcc.Graph(id = 'fig-r1c2'))
            ], className = 'chart-div')
        ], width = 6)
    ], className = 'chart-row'),

    ## Hist on Row 2
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H2(id='title-r2c1', className='titles-h2'),
                html.P(id='p-r2c1', className = 'charts-p'),
                dcc.Loading(id='loading_r2c1', type='default',
                        children = dcc.Graph(id = 'fig-r2c1'))
            ], className = 'chart-div')
        ], width = 12)

    ], className = 'chart-row')

])

### PAGE CALLBACKS ###############################################################################################################

# Update figs
@callback(
    # Outputs for Row 1, Col 1
    Output(component_id='title-r1c1', component_property='children'),
    Output(component_id='p-r1c1', component_property='children'),
    Output(component_id='fig-r1c1', component_property='figure'),
    # Outputs for Row 1, Col 2
    Output(component_id='title-r1c2', component_property='children'),
    Output(component_id='p-r1c2', component_property='children'),
    Output(component_id='fig-r1c2', component_property='figure'),
    # Outputs for Row 2, Col 1
    Output(component_id='title-r2c1', component_property='children'),
    Output(component_id='p-r2c1', component_property='children'),
    Output(component_id='fig-r2c1', component_property='figure'),
    # Inputs
    Input(component_id='country-dropdown', component_property='value'),
    Input(component_id='cuisine-dropdown', component_property='value'),
    Input(component_id='award-dropdown', component_property='value'),
    Input(component_id='price-dropdown', component_property='value')
)
def plot_data(_countries, _cuisines, _awards, _prices):
    ## Filter data
    if _value_for_any in _countries:
        _countries = list(silver_df['Country'].unique())
    if _value_for_any in _cuisines:
        _cuisines = list(silver_df['Cuisine'].unique())
    plot_df = silver_df.loc[
        (silver_df['Country'].isin(_countries)) & (silver_df['Cuisine'].isin(_cuisines))
        & (silver_df['Award'].isin(_awards)) & (silver_df['Price_score'].isin(_prices)), :]
    # print(len(plot_df))

    ## Generate map Row1 Col1
    map_df = plot_df.groupby(plot_df['Country']).agg(Res_count = ('Res_ID', 'count')).reset_index()
    fig_r1c1 = go.Figure(
                layout=my_figlayout,
                data=go.Choropleth(
                    locations=map_df['Country'],  # Spatial coordinates
                    z=map_df['Res_count'],  # Data to be color-coded
                    locationmode='country names', 
                    colorscale=colorscale_,  # Color scale for the map
                    colorbar = my_colorbar
                )
        )
    title_r1c1 = 'Restaurants per country'
    p_r1c1 = 'Michelin guide entries count per country'

    ## Generate map Row1 Col2
    map_df = plot_df.groupby(plot_df['Country']).agg(Star_sum = ('Stars_score', 'sum')).reset_index()
    fig_r1c2 = go.Figure(
                layout=my_figlayout,
                data=go.Choropleth(
                    locations=map_df['Country'],  # Spatial coordinates
                    z=map_df['Star_sum'],  # Data to be color-coded
                    locationmode='country names', 
                    colorscale=colorscale_,  # Color scale for the map
                    colorbar = my_colorbar
                )
        )
    title_r1c2 = 'Stars per country'
    p_r1c2 = 'Sum of Michelin Stars per country'

    ## Generate histogram Row2 Col1
    data_grouped = plot_df.groupby(plot_df['Cuisine_l1']).agg(Stars_count = ('Stars_score', 'sum'),
                                                              Restaurant_count = ('Res_ID', 'count')).reset_index()
    data_grouped['Star Ratio'] = data_grouped['Stars_count'] / data_grouped['Restaurant_count']
    data_grouped = data_grouped.loc[(data_grouped['Star Ratio'] >= 0.03) & (data_grouped['Restaurant_count'] >= 5), :] # Filter outliers
    data_grouped = data_grouped.sort_values(by = 'Star Ratio', ascending = False) # Filter outliers
    hover_text=[]
    for idx, row in data_grouped.iterrows():
        hover_text.append(("<i>Cuisine</i>: {}<br>"+
                           "<i>Restaurants Count</i>: {}<br>"+
                           "<i>Tot Stars</i>: {}<br>"+
                            "<i>Stars/Restaurant Ratio</i>: {:.2%}"+
                            "<extra></extra>").format(row['Cuisine_l1'], row['Restaurant_count'], row['Stars_count'], row['Star Ratio']))
    data_grouped['Hovertemplate'] = hover_text
    fig_r2c1 = go.Figure(layout=my_figlayout)
    fig_r2c1.add_trace(
        go.Histogram(
            x=data_grouped['Cuisine_l1'],
            y=data_grouped['Star Ratio'],
            marker_color=chart_colours_['dark-pink'],
            histfunc="sum",
            name='Stars/Restaurants',
            hovertemplate = data_grouped['Hovertemplate'])
    )
    fig_r2c1.update_layout(
        bargap=.6, # gap between bars of adjacent location coordinates
    )
    title_r2c1 = 'Stars Propensity by Cuisine'
    p_r2c1 = 'Sum of Stars over Nr. of Restaurants per cuisine'

    return (title_r1c1, p_r1c1, fig_r1c1, 
            title_r1c2, p_r1c2, fig_r1c2,
            title_r2c1, p_r2c1, fig_r2c1)