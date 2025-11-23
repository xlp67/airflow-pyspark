from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime

def task_run():
    from scripts.meteo_api import list_cities, fetch_weather_data
    cities = list_cities()
    nomes = cities['nome'].values
    latitudes = cities['latitude'].values
    longitudes = cities['longitude'].values
    fetch_weather_data(latitudes[0], longitudes[0]).show()


default_args = {
    'owner': 'airflow',
    'email': ['xlp67@gmail.com'],
    # 'email_on_failure': False,
    # 'email_on_retry': False,
    # 'retries': 1,
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

