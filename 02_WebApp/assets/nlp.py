from dash import html
import dash_bootstrap_components as dbc
import requests

## Function to call model from Huggingface API
def embed_from_api(sentence_):
    model_name = 'BAAI/bge-base-en-v1.5'
    api_url = f"https://api-inference.huggingface.co/models/{model_name}"

    # Prepare API call info
    hf_token = None ###
    headers = {"Authorization": f"Bearer {hf_token}"}
    payload = {
        "inputs": sentence_
    }

    # Call to API
    response = requests.post(api_url, headers=headers, json=payload)

    # Process response
    if response.status_code == 200:
      embedded_data = response.json()
    else:
      embedded_data = None
      print("Failed! Status code: %s" % (response.status_code))

    return response.status_code, embedded_data

# Function to generate list of dbc.Row, dbc.Col, dbc.Card to be displayed as search results
def generate_cards(Results_DF, n_per_row):
    """The function creates a row component containing n_per_row columns. Each column contains a dbc.Card with restaurant info"""
    Results_ = []
    for i_row in range(0, len(Results_DF), n_per_row):
       new_Cols = []
       j_col = i_row
       while(j_col < len(Results_DF)) & (j_col < i_row+n_per_row):
          
          ##############################
          ### Create card body
          ##############################
          card_body_ = [
             html.P([
                html.I(className = 'fa-solid fa-utensils', style = {'display':'inline'})," ",str(list(Results_DF['Name'])[j_col])
             ]),
             html.P([
                html.I(className = 'fa-solid fa-location-pin', style = {'display':'inline'})," ",str(list(Results_DF['Address'])[j_col])
             ]),
             html.P([
                html.I(className = 'fa-solid fa-star', style = {'display':'inline'})," ",str(list(Results_DF['Award'])[j_col])
             ]),
             html.P([
                html.I(className = 'fa-solid fa-coins', style = {'display':'inline'})," ",str(list(Results_DF['Price'])[j_col])
             ])             
          ]

          ##############################
          ### Create card header
          ##############################
          card_header_ = [
             html.I(className="fa fa-briefcase", style={'display':'inline'}),
             html.P(["  #"+str(j_col+1)+" | "], style={'display':'inline'}),
             html.A("Website", href = str(list(Results_DF['WebsiteUrl'])[j_col]), style={'display':'inline'})
          ]

          ##############################
          ### Create card object
          ##############################
          card_ = dbc.Card([
             dbc.CardHeader(card_header_),
             dbc.CardBody(card_body_)
          ])

          # Append as new column
          new_Cols.append(dbc.Col(card_, width=int(12/n_per_row)))

          j_col += 1

       # Insert cols into Row
       Results_.append(dbc.Row(new_Cols))
    
    return Results_