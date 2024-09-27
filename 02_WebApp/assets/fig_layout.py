import plotly.graph_objects as go

###### MAP COLORSCALES
colorscale_min = '#f9f7f4'
colorscale_mid = '#c10341'
colorscale_max = '#3F0716' # '#8B0830'
colorscale_ = [[0.0, colorscale_min],
               [0.5, colorscale_mid],
               [1.0, colorscale_max]]
#colorscale_ = 'reds' # Other cool options: brwnyl, rdpu, sunset, amp, dense, matter - https://plotly.com/python/colorscales/

###### FIG LAYOUT
font_style = {
    'color' : '#f6f6f6'
}

margin_style = {
    'b': 10,
    'l': 10,
    'r': 10,
    't': 10,
    'pad': 0
}

xaxis_style = {
    'linewidth' : 1,
    'linecolor' : 'rgba(0, 0, 0, 0.35%)',
    'showgrid' : False,
    'zeroline' : False
}

yaxis_style = {
    'linewidth' : 1,
    'linecolor' : 'rgba(0, 0, 0, 0.35%)',
    'showgrid' : True,
    'gridwidth' : 1,
    'gridcolor' : 'rgba(0, 0, 0, 0.11%)',
    'zeroline' : False
}

my_figlayout = go.Layout(
    paper_bgcolor='rgba(0,0,0,0)', # Figure background is transparend and controll by css on dcc.Graph() components
    plot_bgcolor='rgba(0,0,0,0)',
    font = font_style,
    margin = margin_style,
    xaxis = xaxis_style,
    yaxis = yaxis_style,
    height = 380,
    # Map layout through geo parameter - https://plotly.com/python-api-reference/generated/plotly.graph_objects.layout.html#plotly.graph_objects.layout.Geo
    geo=dict(
        bgcolor='rgba(0,0,0,0)',  # Set to transparent
        resolution=50,
        showcoastlines=True,
        showcountries=True,
        showframe=False,
        countrycolor='rgba(0,0,0,0.80%)',
        coastlinecolor='rgba(0,0,0,0.35%)',
        landcolor='rgba(0,0,0,0.35%)'
    )
)

# Stile of the color sidebar on choropleth maps - https://plotly.com/python-api-reference/generated/plotly.graph_objects.choropleth.html?highlight=choropleth#module-plotly.graph_objects.choropleth 
my_colorbar = go.choropleth.ColorBar(
    thickness=4,
    orientation = 'h',
    x = 0.5,
    y = -0.1,
    len = 0.5,
    tickfont=dict(size=10)
)