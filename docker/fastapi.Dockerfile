FROM python:3.12-slim

WORKDIR /app
COPY ../backend/fastapi_app /app

RUN pip install --no-cache-dir fastapi[all] aiokafka sqlalchemy asyncpg python-dotenv

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
