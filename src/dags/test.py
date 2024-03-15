from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

# data_scraper.py에서 main 함수를 가져옵니다.
from data_scraper import main

default_args = {
    'owner': 'hoon',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email': ['ehdgns8227@naver.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
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

    # 파이썬 함수 실행
    run_scraper = PythonOperator(
        task_id='run_data_scraper',
        python_callable=main,
    )

run_scraper
