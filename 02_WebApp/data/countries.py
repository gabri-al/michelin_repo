### File not needed by the app, but used to print the list of countries in the Michelin dataset
import pandas as pd
silver_df = pd.read_parquet("data/silver_data.parquet", engine='pyarrow')

countries__ = silver_df['Country_Code_ISO3'].unique().tolist()
countries__.sort()

print(countries__)
