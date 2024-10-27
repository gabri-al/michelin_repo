import dash
from dash import html, callback, dcc, Input, Output, State, ctx
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate
import numpy as np
from numpy.linalg import norm
import json

dash.register_page(__name__, path='/', order = 1, name='Search', title='Michelin WebApp | Find Your Restaurant')

############################################################################################
# Import functions, settings
from assets.fig_layout import (my_figlayout, my_map_layout, my_map_trace, my_colorscale, my_colorbar3,
                               chart_colours_, center_map_on_data, create_marker_sizes)
from assets.filterbar import _value_for_any
from assets.nlp import embed_from_api, generate_cards

############################################################################################
# Upload data
import pandas as pd
silver_df = pd.read_parquet("data/silver_data.parquet", engine='pyarrow')
rest_descr_df = pd.read_parquet("data/gold_embedded_data.parquet", engine='pyarrow')
TopN = 30 # Nr. or results retrieved

############################################################################################
# Page layout
layout = dbc.Container([
    dbc.Row([]),

    ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
    ### ### ### ### ### Main Search Bar
    ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
    dbc.Row([
        dbc.Col([
            dcc.Textarea(id = 'search-input', placeholder="Describe the restaurant that you are looking for: cuisine, atmosphere, type of chef, etc.",
                         className= 'search-area', persistence = True, persistence_type = 'session')            
        ], width = 10),
        dbc.Col([
            html.Button(["Search"], id='submit-button', n_clicks=0, className='submit-button'),
        ], className = 'search-bar-row', width = 2)
    
    ]),

    ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
    ### ### ### ### ### Alert Row
    ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
    dbc.Row([
        dbc.Col([], width = 3),
        dbc.Col([], id = 'alert-col', className = 'alert-col', width = 4),
        dbc.Col([], width = 5)
    ], id = 'alert-row', className = 'alert-row'),

    ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
    ### ### ### ### ### Results Section
    ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
     dbc.Row([
        dbc.Col([
            html.Div([
                html.H2(id='title-101', className='titles-h2'),
                html.P(id='p-101', className = 'charts-p'),
                dcc.Loading(id='loading-101', type='default', children = dcc.Graph(id = 'fig-101')),
                html.Div([], id = 'result-tiles', className = 'results-tiles-div-empty')
            ], className = 'chart-div')
        ], width = 12)
    ], className = 'search-results-row'),


    ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
    ### ### ### ### ### Data Useful for clicks on map
    ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
     dbc.Row([dbc.Col([html.P([], id = 'clicks-output')], width = 12)], style = {'display': 'None'}), # Invisible row

    ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
    ### ### ### ### ### Checker for page init
    ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
    dbc.Row([dbc.Col(html.P("Page Loading", id = 'init-checker-search'))], style = {'display':'None'}) # Invisible row to check for page opening

])

### PAGE CALLBACKS ###############################################################################################################

##################### SEMANTIC SEARCH
@callback(
    ## Search Embeddings
    Output(component_id='alert-col', component_property='children'),
    ## Map Output
    Output(component_id='title-101', component_property='children'),
    Output(component_id='p-101', component_property='children'),
    Output(component_id='fig-101', component_property='figure'),
    ## Result Tiles Output
    Output(component_id='result-tiles', component_property='children'),
    Output(component_id='result-tiles', component_property='className'),
    ## Checker for page loading
    Output(component_id='init-checker-search', component_property='children'),

    ## Search Inputs
    Input(component_id='submit-button', component_property='n_clicks'),
    Input(component_id='search-input', component_property='value'),

    ## Filter Inputs
    Input(component_id='country-dropdown', component_property='value'),
    Input(component_id='city-dropdown', component_property='value'),
    Input(component_id='cuisine-dropdown', component_property='value'),
    Input(component_id='award-dropdown', component_property='value'),
    Input(component_id='price-dropdown', component_property='value'),
    
    ## Checker for page loading
    State(component_id='init-checker-search', component_property='children'))
def search_input(n_clicks, search_query, _countries, _cities, _cuisines, _awards, _prices, init_checker_):

    ##########################################
    ### Check if Updates are needed --- https://dash.plotly.com/determining-which-callback-input-changed
    ##########################################
    if init_checker_ == 'Page Loading':
        isLoading = True # Page is opening (app initializing or page transitioned)
    else:
        isLoading = False # Page loaded already
    
    trigger_ = ctx.triggered_id
    if (trigger_ != 'submit-button' or search_query is None or len(search_query) == 0) and not isLoading:
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

    if isLoading:
        ##########################################
        ### Initialize all Outputs for paging loading (chart will be a basic scatterplot)
        ##########################################
        embed_response = None; res_tiles = None; res_tiles_class = 'results-tiles-div-empty'
        title_101 = 'Restaurants Overview'; p_101 = ''; hover_text = []
        for idx, row in plot_df.iterrows():
            hover_text.append((
                            "<i>Name</i>: {}<br>"+
                            "<i>Address</i>: {}"+
                            "<extra></extra>").format(row['Name'], row['Address']))
        plot_df['Hovertemplate'] = hover_text
        my_map_trace_here = my_map_trace # Importing basic trace layout
        my_map_trace_here['lat'] = plot_df['Latitude']
        my_map_trace_here['lon'] = plot_df['Longitude']
        my_map_trace_here['marker']['color'] = chart_colours_['my-palette-02']
        my_map_trace_here['marker']['opacity'] = 0.65
        my_map_trace_here['marker']['size'] = 5
        fig_101 = go.Figure(layout = my_figlayout)
        fig_101.add_trace(go.Scattermap(my_map_trace_here))
        fig_101.update_maps(my_map_layout)
        fig_101.update_maps(center={"lat": center_map_on_data(plot_df)[0],"lon": center_map_on_data(plot_df)[1]})

    else:
        ##########################################
        ### Embed Input Query
        ##########################################  
        try:
            ##########################################
            ### Embed query via API
            ##########################################
            api_response, embedded_query = embed_from_api(search_query)
            embed_response = dbc.Alert(
                children=['Query embedded via API, vector length: ', str(len(embedded_query))], color='success', class_name='alert-style', style = {'display': 'None'})
            
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
            Final_df = pd.merge(left = plot_df, right = Cosine_sim_df, left_on = 'Res_ID', right_on = 'Res_IDs', how = 'inner')
            Final_df = Final_df.sort_values(by = 'Cosine_Similarity_Max', ascending = False).iloc[:TopN]

            ## Add colors and sizes
            sizes_ = create_marker_sizes(TopN)
            Final_df['Size'] = sizes_
            Final_df = Final_df.sort_values(by = 'Cosine_Similarity_Max', ascending = True) # Resort the data to plot main restaurants on top

            ##########################################
            ### Present Results on Map
            ##########################################
            title_101 = 'Search Results'
            p_101 = 'Restaurants with descriptions semantically close to the search query (results are colored based on cosine similarity) - Top '+str(TopN)+' Restaurants displayed.'
            hover_text=[]; rank_ = TopN; rank_list = []
            for idx, row in Final_df.iterrows():
                hover_text.append(("<i>Rank</i>: {}<br>"+
                                "<i>Name</i>: {}<br>"+
                                "<i>Address</i>: {}"+
                                "<extra></extra>").format(rank_, row['Name'], row['Address']))
                rank_list.append(rank_)
                rank_ -= 1
            Final_df['Hovertemplate'] = hover_text
            Final_df['Ranks'] = rank_list
            fig_101 = go.Figure(layout = my_figlayout)
            my_map_trace_here = my_map_trace # Importing basic trace layout
            my_map_trace_here['lat'] = Final_df['Latitude']
            my_map_trace_here['lon'] = Final_df['Longitude']
            my_map_trace_here['marker']['color'] = Final_df['Cosine_Similarity_Max']
            my_map_trace_here['marker']['size'] = Final_df['Size']
            my_map_trace_here['marker']['opacity'] = 0.98
            my_map_trace_here['marker']['colorbar'] = my_colorbar3
            my_map_trace_here['marker']['colorscale'] = my_colorscale
            my_map_trace_here['customdata'] = Final_df['Ranks']
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
                res_tiles_class = 'results-tiles-div'
            except:
                res_tiles = None

        except:
            embed_response = dbc.Alert(
                children=['Error! Calling the embedding API returned this response code: ', str(api_response)], color='danger', class_name='alert-style')

    ### Update the checker value
    init_checker_ = 'Page Loaded Already'

    return (
        ## Search Embeddings
        embed_response,
        ## Map Output
        title_101, p_101, fig_101,
        ## Result Tiles Output
        res_tiles, res_tiles_class,
        ## Checker for page loading
        init_checker_
        )

##################### CLICKS ON MAP
Outputs_ = [Output(component_id='clicks-output', component_property='children')]
for i in range(TopN):
    Outputs_.append(Output(component_id=str(i+1)+'-header', component_property='className'))
    Outputs_.append(Output(component_id=str(i+1)+'-body', component_property='className'))

@callback(
    Outputs_,

    ## Map Click Inputs
    Input(component_id='fig-101', component_property='clickData'),
    Input(component_id='title-101', component_property='children'),
    prevent_initial_call=True)
def search_input(click_data_, title_):
    if click_data_ is None or title_ != 'Search Results':
        raise PreventUpdate
    
    Id_clicked_ = int(click_data_['points'][0]['customdata'])
    res_str = 'Clicked Restaurant ranked #'+str(Id_clicked_)

    header_base_class = 'card-header'; header_highlighted_class = 'card-header-highlighted'
    body_base_class = 'card-body'; body_highlighted_class = 'card-body-highlighted' 
    results_ = [str(res_str)]
    for i in range(TopN):
        if i+1 == Id_clicked_:
            results_.append(header_highlighted_class)
            results_.append(body_highlighted_class)
        else:
            results_.append(header_base_class)
            results_.append(body_base_class)

    return results_