from airflow.providers.amazon.aws.hooks.s3 import S3Hook
import json
import requests

def fetch_player_stats(date):
    url = f"http://api.hu-nie.com/basketball/player-stats?date={date}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        file_path = f'/tmp/player_stats.json'
        with open(file_path, 'w') as f:
            json.dump(data, f)
        print(f"데이터가 성공적으로 저장되었습니다: /tmp/player_stats.json")
        return file_path
    else:
        raise Exception(f"API 요청 실패: 상태 코드 {response.status_code}")

def upload_data_s3(file_path, date):
    hook = S3Hook(aws_conn_id='test')
    hook.load_file(filename=file_path, key= f'{date}_player-stats.json', bucket_name='hoon-s3-bucket', replace=True)

def fetch_and_upload_player_stats(date):

    file_path = fetch_player_stats(date)
    upload_data_s3(file_path, date)
    
    print(f"{date}의 농구 선수 통계가 성공적으로 업로드되었습니다.")
