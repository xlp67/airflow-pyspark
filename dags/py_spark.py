from pyspark.sql import SparkSession, DataFrame
import pymysql
import os 
from dotenv import load_dotenv
from scripts.meteo_api import fetch_weather_data, list_cities

load_dotenv('../config')
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_PORT = os.getenv('MYSQL_PORT')
MYSQL_NAME = os.getenv('MYSQL_NAME')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_DRIVER = os.getenv('MYSQL_DRIVER')
JAR_PATH = os.getenv('JAR_PATH')


def session_spark():
    return SparkSession.builder \
        .appName("CSV para MySQL") \
        .config("spark.jars", '/opt/spark/jars/mysql-connector-j-8.4.0.jar') \
        .getOrCreate()

def db_data():
    url = f"jdbc:mysql://{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_NAME}"
    properties = {"user": MYSQL_USER, "password": MYSQL_PASSWORD, "driver": MYSQL_DRIVER}
    return url, properties

def read_csv(path: str):
    spark = session_spark()
    return spark.read.csv(path, header=True, inferSchema=True)

def write_table_from_csv(files_name, mode):
    url, propert = db_data()
    df = read_csv(f'./datasets/{files_name}.csv').groupBy('ano').mean().drop('avg(ano)')
    df.write.jdbc(url, files_name, mode=mode, properties=propert)

def write_table_sql(name: str, table: DataFrame):
    url, propriet = db_data()
    table.write.jdbc(url=url, table=name, properties=propriet)


def get_table(table_name: str):
    url, propert = db_data()
    spark = session_spark()
    df = spark.read.jdbc(url, table_name, properties=propert)
    df.write.mode("overwrite").parquet(f"{table_name}.parquet")


