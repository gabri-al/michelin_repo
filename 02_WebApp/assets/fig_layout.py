import plotly.graph_objects as go
from urllib.request import urlopen
import json
import ssl

###### DOWNLOAD WORLWIDE geoJSON DATASET - https://datahub.io/core/geo-countries#countries
url_ = 'https://r2.datahub.io/clvyjaryy0000la0cxieg4o8o/main/raw/data/countries.geojson'
ssl._create_default_https_context = ssl._create_unverified_context # Disabling SSL Verification
with urlopen(url_) as response:
    country_geojson = json.load(response)
## Extract list of valid country IDs form the geojson file (the country standard naming convention is here https://github.com/datasets/country-codes/blob/main/data/country-codes.csv)
countries__ = []
for d in country_geojson['features']:
    countries__.append(d['properties']['ISO_A3'])

###### COLOURS
chart_colours_ = {
    'white' : '#f6f6f6',
    'grey': '#999',
    'dark-grey': '#2C363B',
    'my-palette-00': '#f1c8a1',
    'my-palette-01': '#d69254',
    'my-palette-02': '#cd722d',
    'my-palette-03': '#b16e5d',
    'my-palette-04': '#7a5f96',
    'my-palette-05': '#593e63',
    'my-palette-06': '#0f2a47',
}

###### FIG LAYOUT
font_style = {
    'color' : chart_colours_['white']
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
    'zeroline' : False,
    'tickangle' : 315,
    'tickfont' : {
        'size' : 9
    }
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
    height = 550,
    #geo=dict() # defined below
)

my_map_layout = dict(
    # layout.map object on MapLibre maps (same arguments as former layout.mapbox: https://plotly.com/python/reference/layout/mapbox/)
    # Maplibre layouts https://plotly.com/python/tile-map-layers/
    style = 'dark',
    zoom = 1,
)

my_map_trace = dict( # https://plotly.com/python-api-reference/generated/plotly.graph_objects.Scattermapbox.html
    mode='markers',
    opacity = 0.70,
    marker = dict( #https://plotly.com/python-api-reference/generated/plotly.graph_objects.scattermapbox.html#plotly.graph_objects.scattermapbox.Marker
        allowoverlap = True,
        symbol = 'circle', # https://labs.mapbox.com/maki-icons/
        opacity = 0.70,
    ),
    showlegend = False,
    hoverlabel = dict(
        bgcolor = chart_colours_['dark-grey'],
        bordercolor = 'rgba(0,0,0,0)', # transparent
        font = dict(
            color = chart_colours_['grey'],
            size = 9,
        )
    )
)

my_colorscale = [[0, chart_colours_['my-palette-00']], [1, chart_colours_['my-palette-05']]]

# Stile of the color sidebar on choropleth maps - https://plotly.com/python-api-reference/generated/plotly.graph_objects.choropleth.html?highlight=choropleth#module-plotly.graph_objects.choropleth 
my_colorbar2 = go.choroplethmap.ColorBar( # https://plotly.com/python-api-reference/generated/plotly.graph_objects.choroplethmapbox.html#plotly.graph_objects.choroplethmapbox.ColorBar
    thickness=4,
    orientation = 'h',
    x = 0.5,
    y = -0.1,
    len = 0.5,
    tickfont=dict(size=10)
)

my_colorbar3 = go.scattermap.marker.ColorBar(
    thickness=4,
    orientation = 'h',
    x = 0.5,
    y = -0.1,
    len = 0.5,
    tickfont=dict(size=10)
)

my_legend = {
    "font" : {"size": 9},
    "orientation" : "h",
    "x" : 0.60,
    "y" : 1.10,
}

# Functions to calculate map bounds or center info
def map_boundaries(df_):
    """ Given the filtered df, the function returns the map's boundaries """
    max_lat = df_['Latitude'].max(); min_lat = df_['Latitude'].min()
    max_lon = df_['Longitude'].max(); min_lon = df_['Longitude'].min()
    return dict(south = min_lat, north = max_lat, west = min_lon, east = max_lon)

def center_map_on_data(df_):
    """ Given the filtered df, the function returns the average Latitude and Longitude to center the map """
    max_lat = df_['Latitude'].max(); min_lat = df_['Latitude'].min()
    max_lon = df_['Longitude'].max(); min_lon = df_['Longitude'].min()
    return [(max_lat+min_lat)/2, (max_lon+min_lon)/2]

"""
my_fig_geo = dict(
    # Map layout through geo parameter - https://plotly.com/python-api-reference/generated/plotly.graph_objects.layout.html#plotly.graph_objects.layout.Geo
    bgcolor='rgba(0,0,0,0)',  # Set to transparent
    resolution=50,
    showcoastlines=False,
    showcountries=True,
    showframe=False,
    showlakes=False,
    showocean=True,
    oceancolor='rgba(52, 88, 86, 0.60%)' , #'rgba(143, 218, 208, 0.70%)',
    landcolor='rgba(244, 241, 215, 0.70%)', #'rgba(0,0,0,0.35%)',
    countrycolor='rgba(27, 40, 34, 0.70%)',
    projection = {"scale": 1.10} # Default Zoom
)
"""

# Function to generate a colorscale between two extremes:
"""
def create_colorscale(N,
                      min = [241, 200, 161], # my-palette-00
                      max = [89, 62, 99]): #my-palette-05
    #Input are RGB (0-255) colors, based on https://www.rapidtables.com/convert/color/hex-to-rgb.html
    min_r = min[0]; min_g = min[1]; min_b = min[2]
    max_r = max[0]; max_g = max[1]; max_b = max[2]
    incr_r = abs((min_r - max_r)) / N
    incr_g = abs((min_g - max_g)) / N
    incr_b = abs((min_b - max_b)) / N
    color_ = [max_r, max_g, max_b]
    colorscale_fin = []
    for i in range(N):
        if min_r > max_r:
            new_r = color_[0] + incr_r
        else:
            new_r = color_[0] - incr_r
        if min_g > max_g:
            new_g = color_[1] + incr_g
        else:
            new_g = color_[1] - incr_g
        if min_b > max_b:
            new_b = color_[2] + incr_b
        else:
            new_b = color_[2] - incr_b
        colorscale_fin.append( str('rgb(') + str(int(new_r)) + ', ' + str(int(new_g)) + ', ' + str(int(new_b)) + ')' )
        color_ = [new_r, new_g, new_b]
    
    return colorscale_fin
"""

# Function to generate marker sizes:
def create_marker_sizes(N, min = 5, max = 25):
    sizes_ = []
    value_ = max
    while value_ > min:
        sizes_.append(round(value_,2))
        value_ -= (max-min)/N
    if len(sizes_) < N:
        sizes_.append(min)

    return sizes_