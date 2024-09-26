import dash
from dash import html, callback, dcc, Input, Output
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/', name='Home', title='Michelin WebApp | Home')

############################################################################################
# Import functions, settings

############################################################################################
# Upload data

############################################################################################
# Page layout
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Data Insights")
        ], width=12)
    ])
])