# 기본 이미지 설정
FROM python:3.8-slim

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 현재 디렉토리의 모든 파일을 컨테이너의 작업 디렉토리로 복사
COPY . .

EXPOSE 5000
# Gunicorn으로 Flask 애플리케이션 실행
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:create_app()"]