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
_Cities = list(silver_df['City'].unique())
_Cities.append(_value_for_any)
_Cities.sort()

######################## Define individual filters
_country_filter = dcc.Dropdown(options=_Countries, value=[_value_for_any], searchable=True, persistence=True, 
                               persistence_type='session', id='country-dropdown', multi=True)

_city_filter = dcc.Dropdown(options=_Cities, value=[_value_for_any], searchable=True, persistence=True, 
                            persistence_type='session', id='city-dropdown', multi=True)

_cuisine_filter = dcc.Dropdown(options=_Cuisines, value=[_value_for_any], searchable=True, persistence=True,
                               persistence_type='session', id='cuisine-dropdown', multi=True)

_award_filter = dcc.Dropdown(options=_Awards, value=_Awards, searchable=True, persistence=True,
                             persistence_type='session', id='award-dropdown', multi=True)

_price_filter = dcc.Dropdown(options=_Prices, value=[1, 2, 3, 4], searchable=True, persistence=True, 
                             persistence_type='session', id='price-dropdown', multi=True)

_submit_button = html.Button(["Apply Filters"], id='submit-button', n_clicks=0, className='submit-button')

######################## Create filter div
_filters = list([
    dbc.Row([ # Country filter
        dbc.Col([html.P(["Country:"], className = 'filter-p')], width = 1),
        dbc.Col([_country_filter], width = 5),
        # City
        dbc.Col([html.P(["City:"], className = 'filter-p')], width = 1),
        dbc.Col([_city_filter], width = 5),
    ], className = 'filter-row'),
    dbc.Row([ # Cuisine Filter
        dbc.Col([html.P(["Cuisine:"], className = 'filter-p')], width = 1),
        dbc.Col([_cuisine_filter], width = 11)
    ], className = 'filter-row'),
    dbc.Row([ # Award (Stars) & Price Filters
        dbc.Col([html.P(["Award:"], className = 'filter-p')], width = 1),
        dbc.Col([_award_filter], width = 5),
        dbc.Col([html.P(["Price:"], className = 'filter-p')], width = 1),
        dbc.Col([_price_filter], width = 5)
    ], className = 'filter-row')
])

_filters_search = html.Div(children=_filters, className = 'filter-div', id = 'filter-div')


_filters_with_submit_button = _filters.copy()
_filters_with_submit_button.append(
    dbc.Row([# Submit Button
        dbc.Col([], width = 5),
        dbc.Col(_submit_button, width = 2),
        dbc.Col([], width = 5)
    ], className = 'filter-row')
)

_filters_insights = html.Div(children=_filters_with_submit_button, className = 'filter-div', id = 'filter-div')




