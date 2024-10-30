## Michelin Restaurant WebApp
This multi-page webapp, deployed [here](https://webapp3dash.pythonanywhere.com/), offers two main functionalities, with data based on this Michelin Restaurant [dataset](https://www.kaggle.com/datasets/ngshiheng/michelin-guide-restaurants-2021)

#### Semantic Search
The Search page allows users to look for restaurants based on a search query and some optional filters.
The search query will be embedded via API, using the [bge-base-en-v1.5 model](https://huggingface.co/BAAI/bge-base-en-v1.5)
The descriptions of restaurants meeting the filter criteria are then compared with the search query and ranked by their cosine similarity.
Results are displayed in interactive tiles which gets highlighted depending on the on-map clicks.
![](https://github.com/gabri-al/michelin_repo/blob/main/20241030_App_Search.gif)


#### Insights
The Insights page presents pre-built maps and charts, based on KPIs that can be extracted from the dataset.

Insights, targeting specific KPIs mentioned above each figure, are organized in the following sections:
- Restaurants by Country
- Insights by Award, showing: stars and star propensity by country
- Insights by Cuisines, showing: Cuisines by Country, Popular Cuisines, Star Propensity by Cuisine
- Insights by Price, showing: Price Score by Country, Price Category by Cuisine, Price Category by Award

