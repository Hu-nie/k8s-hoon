from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python_operator import PythonVirtualenvOperator
from airflow.operators.python_operator import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

import requests

def fetch_data():
    url = "http://api.hu-nie.com/data_collect"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        with open('/tmp/my_data.json', 'w') as f:
            f.write(str(data))
    else:
        raise Exception("API 요청 실패")


def upload_to_s3():
    hook = S3Hook(aws_conn_id='test')
    hook.load_file(filename='/tmp/my_data.json', key='my_data.json', bucket_name='hoon-s3-bucket', replace=True)

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
        task_id='fetch_data',
        python_callable=fetch_data,
    )
    s3_upload = PythonOperator(
        task_id='upload_to_s3',
        python_callable=upload_to_s3,
    )

    end = DummyOperator(task_id = 'end')

start >> run_scraper >> s3_upload >> end 
