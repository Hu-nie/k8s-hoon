from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python_operator import PythonVirtualenvOperator
# data_scraper.py에서 main 함수를 가져옵니다.
from data_scraper import main

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
    
    start = Dummyoperator(task_id = 'start')
    # 파이썬 함수 실행
    run_scraper = PythonVirtualenvOperator(
        task_id='run_data_scraper',
        python_callable=main,
        requirements=["basketball_reference_web_scraper"], # 필요한 패키지와 버전
        system_site_packages=True,
    )

    end = Dummyoperator(task_id = 'start')

start >> run_scraper >> end 
