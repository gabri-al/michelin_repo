import dash
from dash import html, callback, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go

dash.register_page(__name__, path='/', name='Home', title='Michelin WebApp | Home')

############################################################################################
# Import functions, settings
from assets.fig_layout import my_figlayout, colorscale_, my_colorbar

############################################################################################
# Upload data
import pandas as pd
silver_df = pd.read_parquet("data/silver_data.parquet", engine='pyarrow')

############################################################################################
# Define page objects that don't depends on callbacks

######################## Row 1, Col 1
def generate_row1_col1():
    map_df = silver_df.groupby(silver_df['Country']).agg(Res_count = ('Res_ID', 'count')).reset_index()
    fig_ = go.Figure(
            layout=my_figlayout,
            data=go.Choropleth(
                locations=map_df['Country'],  # Spatial coordinates
                z=map_df['Res_count'],  # Data to be color-coded
                locationmode='country names', 
                colorscale=colorscale_,  # Color scale for the map
                colorbar = my_colorbar
            )
        )
    # Generate chart metadata
    title_ = 'Restaurants per country'
    p_ = 'Michelin guide entries count per country'
    return title_, p_, fig_

r1_c1_title, r1_c1_p, r1_c1_fig = generate_row1_col1()

######################## Row 1, Col 2
def generate_row1_col2():
    map_df = silver_df.groupby(silver_df['Country']).agg(Star_sum = ('Stars_score', 'sum')).reset_index()
    fig_ = go.Figure(
            layout=my_figlayout,
            data=go.Choropleth(
                locations=map_df['Country'],  # Spatial coordinates
                z=map_df['Star_sum'],  # Data to be color-coded
                locationmode='country names', 
                colorscale=colorscale_,  # Color scale for the map
                colorbar = my_colorbar
            )
        )
    # Generate chart metadata
    title_ = 'Stars per country'
    p_ = 'Sum of Michelin Stars per country'
    return title_, p_, fig_

r1_c2_title, r1_c2_p, r1_c2_fig = generate_row1_col2()

############################################################################################
# Page layout
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Data Insights", className='titles-h1')
        ], width=12)
    ]),

    ## Map with main overviews
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H2(r1_c1_title, id='title-r1c1', className='titles-h2'),
                html.P(r1_c1_p, id='p-r1c1', className = 'charts-p'),
                dcc.Loading(id='loading_1', type='default',
                        children = dcc.Graph(figure = r1_c1_fig, id = 'fig-r1c1'))
            ], className = 'chart-div')
        ], width = 6),
        dbc.Col([
            html.Div([
                html.H2(r1_c2_title, id='title-r1c2', className='titles-h2'),
                html.P(r1_c2_p, id='p-r1c2', className = 'charts-p'),
                dcc.Loading(id='loading_2', type='default',
                            children = dcc.Graph(figure = r1_c2_fig, id = 'fig-r1c2'))
            ], className = 'chart-div')
        ], width = 6)
    ]),
])

### PAGE CALLBACKS ###############################################################################################################

# Update fig
'''
@callback(
    Output(component_id='title-r1c1', component_property='children'),
    Output(component_id='p-r1c1', component_property='children'),
    Output(component_id='fig-r1c1', component_property='figure')
)
def plot_data():
    fig_ = None

    # Generate map data
    mad_df = silver_df.groupby(silver_df['Country']).agg(Res_count = ('Res_ID', 'count')).reset_index()
    fig_ = go.Figure(
            layout=my_figlayout,
            data=go.Choropleth(
                locations=mad_df['Country'],  # Spatial coordinates
                z=mad_df['Res_count'],  # Data to be color-coded
                locationmode='country names', 
                colorscale=colorscale_,  # Color scale for the map
            )
        )

    # Generate chart metadata
    title_ = 'Restaurants per country'
    p_ = 'Global overivew of Michelin guide entries count per country'

    return title_, p_, fig_
'''