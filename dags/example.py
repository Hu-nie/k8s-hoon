from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python_operator import PythonOperator
from lib.get_data import fetch_and_upload_player_stats


default_args = {
    'owner': 'hoon',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email': ['ehdgns8227@naver.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'Basketball_Data_Scraper',
    default_args=default_args,
    description='A simple DAG to run Basketball_Data_Scraper.py',
    schedule_interval='0 0 * * *',  # 매일 자정에 실행
    catchup=False,
) as dag:
    
    start = DummyOperator(task_id='start')
    
    # 'yesterday_ds'는 Airflow가 제공하는 기본 변수 중 하나로,
    # DAG이 실행되는 날짜(즉, 실행일 기준 '어제')를 'YYYY-MM-DD' 형식의 문자열로 제공합니다.
    run_scraper = PythonOperator(
        task_id='fetch_and_upload_data',
        python_callable=fetch_and_upload_player_stats,
        op_kwargs={
            'date': '{{ ds }}'
        },
    )

    end = DummyOperator(task_id='end')

    start >> run_scraper >> end
