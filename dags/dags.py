from airflow import DAG
from airflow.operators.python import PythonOperator 
from datetime import datetime, timedelta
from scripts.meteo_api import list_cities

def task_run():
    for city in list_cities().values:
        print(city[0], city[1], city[2])
    

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2015, 12, 1),
    'email': ['xlp67@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'schedule_interval': '@hourly',
}

with DAG(
    dag_id='write_tables',               
    default_args = default_args,                     
    start_date=datetime(2025, 11, 20),  
) as dag:
    task_run = PythonOperator(
        task_id='task_filha_da_puta',          
        python_callable=task_run,  
    )
