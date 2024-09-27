import dash
from dash import html, callback, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go

dash.register_page(__name__, path='/', name='Home', title='Michelin WebApp | Home')

############################################################################################
# Import functions, settings
from assets.fig_layout import my_figlayout, colorscale_

############################################################################################
# Upload data
import pandas as pd
silver_df = pd.read_parquet("data/silver_data.parquet", engine='pyarrow')

# Generate a testing map
mad_df = silver_df.groupby(silver_df['Country']).agg(Res_count = ('Res_ID', 'count')).reset_index()
map_test_ = go.Figure(
        layout=my_figlayout,
        data=go.Choropleth(
            locations=mad_df['Country'],  # Spatial coordinates (state codes)
            z=mad_df['Res_count'],  # Data to be color-coded
            locationmode='country names', 
            colorscale=colorscale_,  # Color scale for the map
            colorbar_title="Nr. Restaurants",  # Title for the color bar
        )
    )
map_test_.update_layout(title = 'Restaurants by Country')

############################################################################################
# Page layout
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Data Insights")
        ], width=12)
    ]),

    ## Testing Map
    dbc.Row([
        dbc.Col([
        ], width=2),
        dbc.Col([
            dcc.Loading(id='loading_1', type='circle',
                        children = dcc.Graph(figure = map_test_, className='my-graph'))
            ], width = 8
        ),
        dbc.Col([
        ], width=2)
    ]),
])