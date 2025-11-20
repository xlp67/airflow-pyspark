import openmeteo_requests
import requests_cache
import pandas as pd
from geopy.geocoders import Nominatim
import geonamescache
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, DoubleType, TimestampType
from datetime import datetime, timedelta, timezone 



import pandas as pd

def list_cities():
    url = "https://raw.githubusercontent.com/kelvins/Municipios-Brasileiros/master/csv/municipios.csv"
    df = pd.read_csv(url)
    df['nome'] = df["nome"].str.lower().str.replace(" ", "_").tolist()
    return df[['nome', 'latitude', 'longitude']]


def fetch_weather_data(latitude, longitude):
    spark = SparkSession.builder \
        .config("spark.jars", '/opt/spark/jars/mysql-connector-j-8.4.0.jar') \
        .appName("WeatherApp") \
        .getOrCreate()
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
    start = datetime.fromtimestamp(hourly.Time(), tz=timezone.utc)
    interval = timedelta(seconds=hourly.Interval())
    steps = hourly.Variables(0).ValuesAsNumpy().shape[0]
    dates = [start + i * interval for i in range(steps)]
    variables = {
        "temperature_2m": hourly.Variables(0).ValuesAsNumpy().tolist(),
        "relative_humidity_2m": hourly.Variables(1).ValuesAsNumpy().tolist(),
        "dew_point_2m": hourly.Variables(2).ValuesAsNumpy().tolist(),
        "apparent_temperature": hourly.Variables(3).ValuesAsNumpy().tolist(),
        "precipitation_probability": hourly.Variables(4).ValuesAsNumpy().tolist(),
        "precipitation": hourly.Variables(5).ValuesAsNumpy().tolist(),
        "rain": hourly.Variables(6).ValuesAsNumpy().tolist(),
        "showers": hourly.Variables(7).ValuesAsNumpy().tolist(),
        "vapour_pressure_deficit": hourly.Variables(8).ValuesAsNumpy().tolist(),
        "evapotranspiration": hourly.Variables(9).ValuesAsNumpy().tolist(),
        "et0_fao_evapotranspiration": hourly.Variables(10).ValuesAsNumpy().tolist(),
        "uv_index": hourly.Variables(11).ValuesAsNumpy().tolist(),
        "wet_bulb_temperature_2m": hourly.Variables(12).ValuesAsNumpy().tolist(),
        "total_column_integrated_water_vapour": hourly.Variables(13).ValuesAsNumpy().tolist(),
        "boundary_layer_height": hourly.Variables(14).ValuesAsNumpy().tolist(),
    }
    rows = []
    for i in range(steps):
        row = [dates[i]] + [variables[k][i] for k in variables]
        rows.append(tuple(row))
    schema = StructType([
        StructField("date", TimestampType(), False),
        StructField("temperature_2m", DoubleType(), True),
        StructField("relative_humidity_2m", DoubleType(), True),
        StructField("dew_point_2m", DoubleType(), True),
        StructField("apparent_temperature", DoubleType(), True),
        StructField("precipitation_probability", DoubleType(), True),
        StructField("precipitation", DoubleType(), True),
        StructField("rain", DoubleType(), True),
        StructField("showers", DoubleType(), True),
        StructField("vapour_pressure_deficit", DoubleType(), True),
        StructField("evapotranspiration", DoubleType(), True),
        StructField("et0_fao_evapotranspiration", DoubleType(), True),
        StructField("uv_index", DoubleType(), True),
        StructField("wet_bulb_temperature_2m", DoubleType(), True),
        StructField("total_column_integrated_water_vapour", DoubleType(), True),
        StructField("boundary_layer_height", DoubleType(), True),
    ])
    return spark.createDataFrame(rows, schema).dropna()

