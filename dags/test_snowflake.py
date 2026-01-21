"""
Test Snowflake Connection DAG

This DAG tests the Snowflake connection by running a simple query.
Make sure to configure the 'conn_id_snowflake' connection in Airflow UI first.
"""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

try:
    from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
    SNOWFLAKE_AVAILABLE = True
except ImportError:
    SNOWFLAKE_AVAILABLE = False


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


def check_snowflake_provider():
    """Check if Snowflake provider is installed."""
    if not SNOWFLAKE_AVAILABLE:
        raise ImportError(
            "Snowflake provider not installed. "
            "Run: pip install apache-airflow-providers-snowflake"
        )
    print("Snowflake provider is available!")
    return True


with DAG(
    'test_snowflake_connection',
    default_args=default_args,
    description='Test Snowflake connection with a simple query',
    schedule=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['snowflake', 'test'],
) as dag:

    check_provider = PythonOperator(
        task_id='check_snowflake_provider',
        python_callable=check_snowflake_provider,
    )

    if SNOWFLAKE_AVAILABLE:
        test_connection = SnowflakeOperator(
            task_id='test_snowflake_query',
            snowflake_conn_id='conn_id_snowflake',
            sql="SELECT CURRENT_TIMESTAMP(), CURRENT_USER(), CURRENT_ROLE();",
        )

        get_version = SnowflakeOperator(
            task_id='get_snowflake_version',
            snowflake_conn_id='conn_id_snowflake',
            sql="SELECT CURRENT_VERSION();",
        )

        check_provider >> test_connection >> get_version
