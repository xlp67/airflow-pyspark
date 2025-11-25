from pyspark.sql import SparkSession, DataFrame
import os 
from dotenv import load_dotenv
from scripts.meteo_api import read_csv_path, fetch_weather_data

load_dotenv('/opt/airflow/config/.env')
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

def url_propriet():
    return f"jdbc:mysql://{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_NAME}", \
        {
    "user": MYSQL_USER,
    "password": MYSQL_PASSWORD,
    "driver": MYSQL_DRIVER
    }

def read_csv(path: str):
    spark = session_spark()
    return spark.read.csv(path, header=True, inferSchema=True)

def write_table_from_csv(files_name, mode):
    url, propert = url_propriet()
    df = read_csv(f'./datasets/{files_name}.csv').groupBy('ano').mean().drop('avg(ano)')
    df.write.jdbc(url, files_name, mode=mode, properties=propert)

def write_table_sql(name: str, table: DataFrame, url, propriet):
    table.write \
        .mode("append") \
        .jdbc(url=url, table=name, properties=propriet)


def get_table(table_name: str):
    url, propert = url_propriet()
    spark = session_spark()
    df = spark.read.jdbc(url, table_name, properties=propert)
    df.write.mode("overwrite").parquet(f"{table_name}.parquet")

