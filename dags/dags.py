from scripts.meteo_api import fetch_weather_data, list_cities
from py_spark import write_table_sql
from py_spark import JAR_PATH


cities = list_cities()
nomes = cities['nome'].values
latitudes = cities['latitude'].values
longitudes = cities['longitude'].values

data = fetch_weather_data(latitudes[0], longitudes[0])

write_table_sql(nomes[0], data)

