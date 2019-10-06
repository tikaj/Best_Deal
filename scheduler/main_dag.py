from airflow import DAG
import datetime

from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python_operator import PythonOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.datetime(2015, 6, 1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': datetime.timedelta(minutes=5),
}

dag = DAG(
    dag_id='tutorial',
    default_args=default_args,
    schedule_interval=datetime.timedelta(days=1)
)

t1 = PythonOperator(
    task_id='do something',
    python_callable=lambda x: print(x),
    retries=3,
    dag=dag)

