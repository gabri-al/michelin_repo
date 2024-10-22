import dash
from dash import html, callback, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate
import numpy as np
from numpy.linalg import norm

dash.register_page(__name__, path='/search', order = 2, name='Search', title='Michelin WebApp | Find Your Restaurant')

############################################################################################
# Import functions, settings
from assets.fig_layout import (country_geojson, my_figlayout, my_map_layout, my_map_trace, my_colorscale, my_colorbar2,
                               chart_colours_, my_legend, center_map_on_data, countries__, create_colorscale, create_marker_sizes)
from assets.filterbar import _value_for_any
from assets.nlp import embed_from_api, generate_cards

############################################################################################
# Upload data
import pandas as pd
silver_df = pd.read_parquet("data/silver_data.parquet", engine='pyarrow')
#print(silver_df.columns)
# Print out any country which is not compatible with names on the geoJson dataset
for c in silver_df['Country_Code_ISO3'].unique():
    if c not in countries__:
        print("Found an incompatible country: %s" % c)

rest_descr_df = pd.read_parquet("data/gold_embedded_data.parquet", engine='pyarrow')

############################################################################################
# Define page objects that don't depends on callbacks

######################## Generate Data for filters

############################################################################################
# Page layout
layout = dbc.Container([
    dbc.Row([
        #dbc.Col([
            #html.H1("Data Insights", className='titles-h1')
        #], width=12)
    ]),

    ## Main Search bar
    dbc.Row([
        dbc.Col([
            dcc.Textarea(id = 'search-input', placeholder="Describe the restaurant that you are looking for: cuisine, atmosphere, type of chef, etc.",
                         className= 'search-area', persistence = True, persistence_type = 'session')            
        ], width = 10),
        dbc.Col([
            html.Button(["Search"], id='search-button', n_clicks=0, className='search-button'),
        ], className = 'search-bar-row', width = 2)
    
    ]),

    ## Alert Row
    dbc.Row([
        dbc.Col([], width = 3),
        dbc.Col([], id = 'alert-col', className = 'alert-col', width = 4),
        dbc.Col([], width = 5)
    ], id = 'alert-row', className = 'alert-row'),

    ## Results
     dbc.Row([
        dbc.Col([
            html.Div([
                html.H2(id='title-101', className='titles-h2'),
                html.P(id='p-101', className = 'charts-p'),
                dcc.Loading(id='loading-101', type='default', children = dcc.Graph(id = 'fig-101')),
                html.Div([], id = 'result-tiles')
            ], className = 'chart-div')
        ], width = 12)
    ], className = 'chart-row'),

])

### PAGE CALLBACKS ###############################################################################################################

##################### EMBED SEARCH INPUTS
# Save Search Button Clicks into Store
@callback(
          ## Search Embeddings
          Output(component_id='browser-memo', component_property='data'),
          Output(component_id='alert-col', component_property='children'),
          ## Map Output
          Output(component_id='title-101', component_property='children'),
          Output(component_id='p-101', component_property='children'),
          Output(component_id='fig-101', component_property='figure'),
          ## Result Tiles Output
          Output(component_id='result-tiles', component_property='children'),

          ## Search Inputs
          Input(component_id='search-button', component_property='n_clicks'),
          Input(component_id='search-input', component_property='value'),

          ## Filter Inputs
          Input(component_id='country-dropdown', component_property='value'),
          Input(component_id='city-dropdown', component_property='value'),
          Input(component_id='cuisine-dropdown', component_property='value'),
          Input(component_id='award-dropdown', component_property='value'),
          Input(component_id='price-dropdown', component_property='value'),

          State(component_id='browser-memo', component_property='data'),
          prevent_initial_call=True)
def search_input(n_clicks, search_query, _countries, _cities, _cuisines, _awards, _prices, store_data):

    ##########################################
    ### Check if Updates are needed --- replace this part based on https://dash.plotly.com/determining-which-callback-input-changed
    ##########################################
    if n_clicks is None or n_clicks == 0:
        raise PreventUpdate
    #Initialize
    if 'search_clicks' in store_data.keys():
         curr_clicks = store_data['search_clicks']
    else:
         curr_clicks = 0
    #Update
    if int(n_clicks) != int(curr_clicks):
         store_data['search_clicks'] = n_clicks
    else:
         raise PreventUpdate

    ##########################################
    ### Filter Data
    ##########################################
    if _value_for_any in _countries:
        _countries = list(silver_df['Country'].unique())
    if _value_for_any in _cities:
        _cities = list(silver_df['City'].unique())
    if _value_for_any in _cuisines:
        _cuisines = list(silver_df['Cuisine'].unique())
    plot_df = silver_df.loc[
        (silver_df['Country'].isin(_countries)) & (silver_df['City'].isin(_cities)) & (silver_df['Cuisine'].isin(_cuisines))
        & (silver_df['Award'].isin(_awards)) & (silver_df['Price_score'].isin(_prices)), :]    
    embedded_df = rest_descr_df.loc[rest_descr_df['Res_ID'].isin(plot_df['Res_ID']), :]
    #print('Tot count of embedded_df: %d' % len(embedded_df))
    #print('Unique restaurants in embedded_df: %d' % len(set(embedded_df['Res_ID']))) # This df has more than 1 record per restaurant

    ##########################################
    ### Embed Input Query
    ##########################################
    if search_query is None or search_query == '':
        raise PreventUpdate
    
    try:
        ##########################################
        ### Embed query via API
        ##########################################
        api_response, embedded_query = embed_from_api(search_query)
        embed_response = dbc.Alert(
            children=['Query embedded via API, vector length: ', str(len(embedded_query))], color='success', class_name='alert-style')
        
        ##########################################
        ### Compute Similarities
        ##########################################
        # Create Matrix with Restaurant Embeddings
        emb_len = 768; res_ids = []; i = 0
        res_emb = np.zeros((len(embedded_df), emb_len), dtype=float)
        for index, row in embedded_df.iterrows():
            res_ids.append(row['Res_ID'])
            res_emb[i] = row['Descr_Embedded']
            i += 1

        # Calculate similarities
        Cosine_sim = np.dot(res_emb, np.array(embedded_query)) / (norm(res_emb, axis=1) * norm(np.array(embedded_query)))
        Cosine_sim_df = pd.DataFrame({'Res_IDs': res_ids, 'Cosine_Similarity': Cosine_sim})
        Cosine_sim_df = Cosine_sim_df.groupby('Res_IDs').agg(Cosine_Similarity_Max = ('Cosine_Similarity', 'max')).reset_index()

        ## Join similarities with the original Dataframe
        TopN = 20
        Final_df = pd.merge(left = plot_df, right = Cosine_sim_df, left_on = 'Res_ID', right_on = 'Res_IDs', how = 'inner')
        Final_df = Final_df.sort_values(by = 'Cosine_Similarity_Max', ascending = False).iloc[:TopN]

        ## Add colors and sizes
        coloscale_ = create_colorscale(TopN)
        sizes_ = create_marker_sizes(TopN)
        Final_df['Color'] = coloscale_
        Final_df['Size'] = sizes_
        Final_df = Final_df.sort_values(by = 'Cosine_Similarity_Max', ascending = True) # Resort the data to plot main restaurants on top
        #print(Final_df.head(3))

        ##########################################
        ### Present Results on Map
        ##########################################
        title_101 = 'Search Results'
        p_101 = 'Restaurants with description sematically close to the Search Query - Top '+str(TopN)+' Restaurants shown'
        hover_text=[]; rank_ = TopN
        for idx, row in Final_df.iterrows():
            hover_text.append(("<i>Name</i>: {}<br>"+
                            "<i>Address</i>: {}<br>"+
                            "<i>Rank</i>: {}"+
                            "<extra></extra>").format(row['Name'], row['Address'], rank_))
            rank_ -= 1
        Final_df['Hovertemplate'] = hover_text
        fig_101 = go.Figure(layout = my_figlayout)
        my_map_trace_here = my_map_trace # Importing basic trace layout
        my_map_trace_here['lat'] = Final_df['Latitude']
        my_map_trace_here['lon'] = Final_df['Longitude']
        my_map_trace_here['marker']['color'] = Final_df['Color']
        my_map_trace_here['marker']['size'] = Final_df['Size']
        my_map_trace_here['marker']['opacity'] = 0.90
        my_map_trace_here['hovertemplate'] = Final_df['Hovertemplate']
        fig_101.add_trace(go.Scattermap(my_map_trace_here))
        fig_101.update_maps(my_map_layout)
        fig_101.update_maps(center={"lat": center_map_on_data(Final_df)[0],"lon": center_map_on_data(Final_df)[1]})

        ##########################################
        ### Prepare Results Tiles
        ##########################################
        Final_df = Final_df.sort_values(by = 'Cosine_Similarity_Max', ascending = False)
        try:
            res_tiles = generate_cards(Final_df, 3)
        except:
            res_tiles = None

    except:
        embed_response = dbc.Alert(
            children=['Error! Calling the embedding API returned this response code: ', str(api_response)], color='danger', class_name='alert-style') 

    return (
        ## Search Embeddings
        store_data, embed_response,
        ## Map Output
        title_101, p_101, fig_101,
        ## Result Tiles Output
        res_tiles
        )