from dash import html, dcc
import dash_bootstrap_components as dbc
import dash

_pages_tmp = [html.A(page["name"], href=page["path"], className = 'nav-a') for page in dash.page_registry.values()]
_pages = []

# Add a breaker after each page
for i in range(0, len(_pages_tmp), 1):
    if len(_pages_tmp) > 1 and i != len(_pages_tmp)-1:
        _pages.append(_pages_tmp[i])
        _pages.append(
            html.A("|", href="#", className = 'nav-a')
        )
    else:
        _pages.append(_pages_tmp[i])

_nav = dbc.Row([
        dbc.Col([], width = 1),
        dbc.Col([
            html.Img(src="assets/img/Michelin_Logo4.png", alt="image", disable_n_clicks = True, className = 'nav-img')
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