FROM python:3.12-slim

WORKDIR /app
COPY ../bot /app

RUN pip install --no-cache-dir aiogram aiokafka python-dotenv itsdangerous httpx

CMD ["python", "main.py"]
