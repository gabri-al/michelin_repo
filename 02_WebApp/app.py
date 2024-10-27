from dash import Dash, dcc, callback, Input, Output, State, html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate

_font = "https://fonts.googleapis.com/css2?family=Lato&display=swap"
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME, _font],
	   suppress_callback_exceptions=True, prevent_initial_callbacks=True)
server = app.server

############################################################################################
# Import shared components
from assets.navbar import _nav
from assets.footer import _footer
from assets.filterbar import _filters, _value_for_any, _filters_insights, _filters_search

############################################################################################
# Upload data
import pandas as pd
silver_df = pd.read_parquet("data/silver_data.parquet", engine='pyarrow')

############################################################################################
# App Layout
app.layout = dbc.Container([
	## Page Nav
	dbc.Row([
        dbc.Col([
            _nav
        ], width = 12)
    ]),

    ## Page Location to determine current URL
    dcc.Location(
         id = 'page-location'
    ),

	## Page content
    dbc.Row([
        dbc.Col([
             
            html.Div(children = [],
            className = 'container', id = 'app-filter-div'), # Same class as page content below

            ## Page Content
            dash.page_container,

            ## Footer
			_footer
               
	    ], className = 'page-content', width = 12),
    ]),
	
    dcc.Store(id='browser-memo', data=dict(), storage_type='session')
	
], fluid=True)

############################################################################################
# Callbacks

##################### UPDATE FILTER DIV DEPENDING ON PAGE URL
@callback(
    Output(component_id='app-filter-div', component_property='children'),
    Output(component_id='app-filter-div', component_property='style'),
    Input(component_id='page-location', component_property='pathname')
)
def create_filters(path_):
    ## Create a first row with the expanding button
    _expanding_row = dbc.Row([
        dbc.Col([
            html.Button([html.I(id='reveal-filters-icon')], id='reveal-filters', n_clicks=0, className='my-button'),
            html.H2("Apply Filters", className='titles-expand-h2'),
        ], className = 'button-col', width = 11),
        dbc.Col(width = 1)
    ], className = 'expanding-title-row')
    ## Create return object
    if 'search' in path_:
        filter_div_fin = [_expanding_row, dbc.Row([_filters_search])]
        return filter_div_fin, {}
    elif 'info' in path_:
        filter_div_fin = [_expanding_row, dbc.Row([_filters_insights])]
        return filter_div_fin, {'display': 'None'}
    else:
        filter_div_fin = [_expanding_row, dbc.Row([_filters_insights])]
        return filter_div_fin, {}

##################### UPDATES BASED ON EXPANDING BUTTONS
### Filters
@callback(
    Output(component_id='filter-div', component_property='style'),
    Output(component_id='reveal-filters-icon', component_property='className'),
    Input(component_id='reveal-filters', component_property='n_clicks')
)
def display_filters(_nclicks):
    if _nclicks is None or _nclicks == 0 or _nclicks % 2 == 0:
        return {'display': 'None'}, 'fa-solid fa-filter me-3 fa-1x'
    else:
        return {}, 'fa-solid fa-chevron-down me-3 fa-1x'
    
##################### UPDATES ON DROPDOWN LISTS
@callback(
    Output(component_id='city-dropdown', component_property='options'),
    Input(component_id='country-dropdown', component_property='value')
)
def plot_data(_countries):
    if _value_for_any in _countries or _countries is None:
        _Cities = list(silver_df['City'].unique())
        _Cities.append(_value_for_any)
        _Cities.sort()
    else:
        _Cities = list(silver_df.loc[silver_df['Country'].isin(_countries), 'City'].unique())
        _Cities.append(_value_for_any)
        _Cities.sort()
    return _Cities

############################################################################################
# Run App
if __name__ == '__main__':
	app.run_server(debug=True, port='8855')