import dash
from dash import html, callback, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go

dash.register_page(__name__, path='/info', order = 3, name='Info', title='Michelin WebApp | How does it work?')

############################################################################################
# Page layout
layout = dbc.Container([
    dbc.Row([]),

    ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
    ### ### ### ### ### Title
    ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
    dbc.Row([
        dbc.Col([
            html.H2("Welcome to this Michelin Restaurants WebApp!", className='titles-h2')
        ], width=12)
    ], className = 'info-title-row'),

    ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
    ### ### ### ### ### Info
    ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H2("Search Mode", className='titles-h2'),
                html.P([
                    "The Search page allows users to look for restaurants based on a search query and apply optional filters.",
                    html.Br(),
                    "The search query will be embedded via API, using the ",
                    html.A('bge-base-en-v1.5 model', href='https://huggingface.co/BAAI/bge-base-en-v1.5'),
                    html.Br(),
                    "Results, displayed on the map and in the results tiles, are ranked by the cosine similarity of the restaurant descriptions."
                ], className = 'charts-p'),

                html.H2("Insights Mode", className='titles-h2'),
                html.P([
                    "The Insights page shows some pre-built figures based on the ",
                    html.A('Michelin Restaurants dataset.', href='https://www.kaggle.com/datasets/ngshiheng/michelin-guide-restaurants-2021'),
                    html.Br(),
                    "Insights are organized in the following sections:",
                    html.Br(),
                    "Restaurants by Country",
                    html.Br(),
                    "Insights by Award, showing: stars by countryand star propensity by country",
                    html.Br(),
                    "Insights by Cuisines, showing: Cuisines by Country, Popular Cuisines, Star Propensity by Cuisine",
                    html.Br(),
                    "Insights by Price, showing: Price Score by Country, Price Category by Cuisine, Price Category by Award"
                ], className = 'charts-p')
            ], className = 'chart-div')
        ], width = 12)
    ])


])