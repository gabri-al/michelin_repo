import dash
from dash import html, callback, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd

dash.register_page(__name__, path='/', name='Home', title='Michelin WebApp | Home')

############################################################################################
# Import functions, settings

############################################################################################
# Upload data
import pandas as pd
silver_df = pd.read_parquet(f'data/silver_data.parquet')
print(silver_df.head(2))

############################################################################################
# Page layout
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Data Insights")
        ], width=12)
    ])
])