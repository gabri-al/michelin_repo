import dash
from dash import html, callback, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go

dash.register_page(__name__, path='/info', order = 3, name='Info', title='Michelin WebApp | How does it work?')

############################################################################################
# Page layout
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Info", className='titles-h1')
        ], width=12)
    ]),

])