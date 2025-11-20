import openmeteo_requests
import requests_cache
import pandas as pd
from geopy.geocoders import Nominatim
import geonamescache



import pandas as pd

def list_cities():
    url = "https://raw.githubusercontent.com/kelvins/Municipios-Brasileiros/master/csv/municipios.csv"
    df = pd.read_csv(url)
    df['nome'] = df["nome"].str.lower().str.replace(" ", "_").tolist()
    return df[['nome', 'latitude', 'longitude']]


def fetch_weather_data(latitude, longitude):
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    openmeteo = openmeteo_requests.Client(session=cache_session)
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": [
            "temperature_2m", "relative_humidity_2m", "dew_point_2m",
            "apparent_temperature", "precipitation_probability", "precipitation",
            "rain", "showers", "vapour_pressure_deficit", "evapotranspiration",
            "et0_fao_evapotranspiration", "uv_index", "wet_bulb_temperature_2m",
            "total_column_integrated_water_vapour", "boundary_layer_height"
        ],
        "start_date": "2025-08-19",
        "end_date": "2025-11-17",
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
    hourly_dew_point_2m = hourly.Variables(2).ValuesAsNumpy()
    hourly_apparent_temperature = hourly.Variables(3).ValuesAsNumpy()
    hourly_precipitation_probability = hourly.Variables(4).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(5).ValuesAsNumpy()
    hourly_rain = hourly.Variables(6).ValuesAsNumpy()
    hourly_showers = hourly.Variables(7).ValuesAsNumpy()
    hourly_vapour_pressure_deficit = hourly.Variables(8).ValuesAsNumpy()
    hourly_evapotranspiration = hourly.Variables(9).ValuesAsNumpy()
    hourly_et0_fao_evapotranspiration = hourly.Variables(10).ValuesAsNumpy()
    hourly_uv_index = hourly.Variables(11).ValuesAsNumpy()
    hourly_wet_bulb_temperature_2m = hourly.Variables(12).ValuesAsNumpy()
    hourly_total_column_integrated_water_vapour = hourly.Variables(13).ValuesAsNumpy()
    hourly_boundary_layer_height = hourly.Variables(14).ValuesAsNumpy()
    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        ),
        "temperature_2m": hourly_temperature_2m,
        "relative_humidity_2m": hourly_relative_humidity_2m,
        "dew_point_2m": hourly_dew_point_2m,
        "apparent_temperature": hourly_apparent_temperature,
        "precipitation_probability": hourly_precipitation_probability,
        "precipitation": hourly_precipitation,
        "rain": hourly_rain,
        "showers": hourly_showers,
        "vapour_pressure_deficit": hourly_vapour_pressure_deficit,
        "evapotranspiration": hourly_evapotranspiration,
        "et0_fao_evapotranspiration": hourly_et0_fao_evapotranspiration,
        "uv_index": hourly_uv_index,
        "wet_bulb_temperature_2m": hourly_wet_bulb_temperature_2m,
        "total_column_integrated_water_vapour": hourly_total_column_integrated_water_vapour,
        "boundary_layer_height": hourly_boundary_layer_height
    }
    hourly_dataframe = pd.DataFrame(hourly_data)
    return hourly_dataframe


cities = list_cities().values
for city in cities:
    print(fetch_weather_data(city[1], city[2]))