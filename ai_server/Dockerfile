# fastapi/Dockerfile
FROM python:3.10-slim

WORKDIR /ai_server

# 시스템 라이브러리 설치 (컴파일러 및 공유 라이브러리)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# pip 최신화
RUN pip install --no-cache-dir --upgrade pip

# 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 복사
COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]