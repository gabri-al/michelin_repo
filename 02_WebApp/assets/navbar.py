from dash import html, dcc
import dash_bootstrap_components as dbc
import dash

_pages = [html.A(page["name"], href=page["path"], className = 'nav-a') for page in dash.page_registry.values()]

_nav = dbc.Row([
        dbc.Col([], width = 1),
        dbc.Col([
            html.Img(src="assets/img/Michelin_Logo.png", alt="image", disable_n_clicks = True, className = 'nav-img')
        ], width = 1, className = 'nav-img-col'),
        dbc.Col([
            dbc.Row([html.P(["Michelin Restaurants", html.Br(), "WebApp"], className = 'nav-p')])
        ], width = 3),
        dbc.Col([], width = 3),
        dbc.Col([
                dbc.Row(html.Div(_pages, className = 'nav-div'))
        ], width = 4)
    ], className="nav-row"
)