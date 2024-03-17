from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python_operator import PythonVirtualenvOperator
from airflow.operators.python_operator import PythonOperator

import requests

def fetch_and_print_api_data():
    url = "http://api.hu-nie.com/data_collect"
    
    # API 요청
    response = requests.get(url)
    
    if response.status_code == 200:
        # 성공적으로 데이터를 받아왔을 때
        data = response.json()
        print(data)
    else:
        # 요청이 실패했을 때
        print("API 요청에 실패했습니다. 상태 코드:", response.status_code)

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
        task_id='fetch_and_print_api_data',
        python_callable=fetch_and_print_api_data,
    )

    end = DummyOperator(task_id = 'end')

start >> run_scraper >> end 
