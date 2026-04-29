# fastapi/Dockerfile
FROM python:3.10-slim

WORKDIR /ai_server

# 필수 라이브러리 설치 (AI 모델 관련 패키지가 있다면 여기에 추가)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# FastAPI 실행 (Uvicorn 활용)
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]