from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.models import Variable
from datetime import datetime
from py_spark import url_propriet



def task_run():
    from scripts.meteo_api import read_csv_path, fetch_weather_data
    from py_spark import write_table_sql, session_spark
    cities = read_csv_path('/opt/airflow/dags/datasets/municipios.csv')
    nomes = cities['nome'].values
    latitudes = cities['latitude'].values
    longitudes = cities['longitude'].values
    url, propriet = url_propriet()
    session = session_spark()
    weather_data = fetch_weather_data(session, latitudes[0], longitudes[0])
    write_table_sql(nomes[0],weather_data, url, propriet)


default_args = {
    'owner': 'airflow',
    'email': ['xlp67@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

with DAG(
    dag_id='dag',
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule='@hourly',
    catchup=False,
) as dag:
    task_run = PythonOperator(
        task_id='task',
        python_callable=task_run,
    )

