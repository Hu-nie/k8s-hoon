from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python_operator import PythonVirtualenvOperator
from airflow.operators.python_operator import PythonOperator

def my_python_function():
    print("Hello, Airflow!")
    print("Current date:", datetime.now())

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email': ['your_email@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# DAG 정의
with DAG(
    'run_data_scraper',
    default_args=default_args,
    description='A simple DAG to run data_scraper.py',
    schedule_interval=timedelta(days=1),
    catchup=False,
) as dag:
    
    start = DummyOperator(task_id = 'start')
    # 파이썬 함수 실행
    run_scraper = PythonOperator(
        task_id='test',
        python_callable=my_python_function,
    )

    end = DummyOperator(task_id = 'end')

start >> run_scraper >> end 
