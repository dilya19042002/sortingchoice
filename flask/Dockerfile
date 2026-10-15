# 파이썬 가벼운 공식 이미지 사용
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 라이브러리 목록 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# Gunicorn 서버를 이용해 앱 실행 (포트 8080 바인딩)
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]
