# fastapi/Dockerfile
FROM python:3.10-slim

WORKDIR /ai_server

# 시스템 의존성 설치 (AI 라이브러리 빌드에 필수적인 도구들)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# pip 업그레이드 및 필수 빌드 도구 설치
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]