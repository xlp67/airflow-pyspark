k3d cluster create --api-port 6550 -p "8081:80@loadbalancer" --agents 2 --volume /home/thiago/Documentos/Code/airflow-pyspark/dags:/var/lib/dags@all

helm install airflow apache-airflow/airflow --namespace airflow --create-namespace --set postgresql.image.tag="latest" -f values.yaml