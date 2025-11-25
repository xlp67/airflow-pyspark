from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime
from py_spark import url_propriet



def bronze_layer():
    from scripts.meteo_api import read_csv_path, fetch_weather_data
    from py_spark import write_table_sql, session_spark

    count = 0

    url, propriet = url_propriet()
    session = session_spark()
    cities = read_csv_path('/opt/airflow/dags/datasets/municipios.csv').values
    for city in cities:
        count += 1
        remaining = len(cities) - count
        name = city[0]
        lat = city[1]
        lon = city[2]
        weather_data = fetch_weather_data(session, lat, lon)
        write_table_sql(name,weather_data, url, propriet)

        print(f'Tabela {name} salva! | Tabelas Restantes: {remaining}')


default_args = {
    'owner': 'airflow',
    'email': ['xlp67@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

with DAG(
    dag_id='medallion_architecture',
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule='@hourly',
    catchup=False,
) as dag:
    
    bronze_layer = PythonOperator(
        task_id='bronze_layer',
        python_callable=bronze_layer,
    )

    bronze_layer