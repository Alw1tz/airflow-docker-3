"""Simple test DAG to verify Airflow is working."""

from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator


def hello_world():
    print("Hello World!")
    return "Success"


with DAG(
    'simple_test',
    description='Simple test DAG',
    schedule=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['test'],
) as dag:

    task = PythonOperator(
        task_id='hello_task',
        python_callable=hello_world,
    )
