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
            html.H1("Welcome to the Michelin Restaurants WebApp!", className='titles-h1-info')
        ], width=12)
    ], className = 'info-title-row'),

    ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
    ### ### ### ### ### Info
    ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Br(),
                html.P([
                    "This WebApp is designed to showcase several features of Plotly Dash, primarily including: Maplibre Maps, integration with third-party APIs, and Reports.",
                    html.Br(),
                    "The data used in the app is sourced from the 2021 ",
                    html.A('Michelin Restaurants dataset.', href='https://www.kaggle.com/datasets/ngshiheng/michelin-guide-restaurants-2021'),
                    html.Br(),
                    "For further information, please check out the ",
                    html.A('GitHub repository', href=''),
                    " or ",
                    html.A('contact the author.', href='https://www.linkedin.com/in/gabriele-albini-85100549/'),
                    html.Br(),html.Br(),
                    "The app consists of two pages that share the same filters but provide different functionalities:",
                    html.Br()
                ], className = 'info-p'),
                html.Br(),
                html.H2("Search Page", className='titles-h2'),
                html.P([
                    "The Search page allows users to look for restaurants based on a search query and apply optional filters.",
                    html.Br(),
                    "The search query will be embedded via API, using the ",
                    html.A('bge-base-en-v1.5 model', href='https://huggingface.co/BAAI/bge-base-en-v1.5'),
                    html.Br(),
                    "Results, displayed on the map and in the results tiles, are ranked by the cosine similarity of the restaurant descriptions.",
                    html.Br(),html.Br(),html.Br(),
                ], className = 'info-p'),
                html.H2("Insights Page", className='titles-h2'),
                html.P([
                    "The Insights page presents pre-built maps and charts based on KPIs that can be extracted from the dataset.",
                    html.Br(),
                    "Insights are organized in the following sections:",
                    html.Br(),
                    html.Ul([
                        html.Li([
                            "Restaurants by Country",
                        ]),
                        html.Li([
                            "Insights by Award, showing: stars and star propensity by country",
                        ]),
                        html.Li([
                            "Insights by Cuisines, showing: Cuisines by Country, Popular Cuisines, Star Propensity by Cuisine",
                        ]),
                        html.Li([
                            "Insights by Price, showing: Price Score by Country, Price Category by Cuisine, Price Category by Award",
                        ]),
                    ]),
                    html.Br(),
                ], className = 'info-p')
            ], className = 'info-div')
        ], width = 12)
    ])


])