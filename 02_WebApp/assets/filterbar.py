from dash import html, dcc
import dash_bootstrap_components as dbc
import dash

######################## Upload data
import pandas as pd
_value_for_any = '_Any'
silver_df = pd.read_parquet("data/silver_data.parquet", engine='pyarrow')
_Countries = list(silver_df['Country'].unique())
_Countries.append(_value_for_any)
_Countries.sort()
_Cuisines = list(silver_df['Cuisine'].unique())
_Cuisines.append(_value_for_any)
_Cuisines.sort()
_Awards = list(silver_df['Award'].unique())
_Awards.sort()
_Prices = [
    {'label': '$', 'value': 1},
    {'label': '$$', 'value': 2},
    {'label': '$$$', 'value': 3},
    {'label': '$$$$', 'value': 4}
]

######################## Define filters

_filters = html.Div([
    # Country filter
    dbc.Row([
            dbc.Col([html.P(["Select country:"], className = 'filter-p')], width = 1),
            dbc.Col([
                dcc.Dropdown(options=_Countries, value=[_value_for_any], searchable=True, persistence=True, 
                        persistence_type='session', id='country-dropdown', multi=True)
            ], width = 10),
            dbc.Col([], width = 1),
    ]),
    # Cuisine Filter
    dbc.Row([
            dbc.Col([html.P(["Select cuisine:"], className = 'filter-p')], width = 1),
            dbc.Col([
                dcc.Dropdown(options=_Cuisines, value=[_value_for_any], searchable=True, persistence=True, 
                        persistence_type='session', id='cuisine-dropdown', multi=True)
            ], width = 10),
            dbc.Col([], width = 1),
    ]),
    # Award (Stars) & Price Filters
    dbc.Row([
            dbc.Col([html.P(["Select Award:"], className = 'filter-p')], width = 1),
            dbc.Col([
                dcc.Dropdown(options=_Awards, value=_Awards, searchable=True, persistence=True, 
                        persistence_type='session', id='award-dropdown', multi=True)
            ], width = 5),
            dbc.Col([html.P(["Select Price:"], className = 'filter-p')], width = 1),
            dbc.Col([
                dcc.Dropdown(options=_Prices, value=[1, 2, 3, 4], searchable=True, persistence=True, 
                        persistence_type='session', id='price-dropdown', multi=True)
            ], width = 4),
            dbc.Col([], width = 1),
    ]),

], className = 'filter-div')