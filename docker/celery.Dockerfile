FROM python:3.12-slim

WORKDIR /app
COPY ../backend/celery_worker /app

RUN pip install --no-cache-dir celery[redis] aiokafka sqlalchemy asyncpg python-dotenv

CMD ["celery", "-A", "worker", "worker", "--loglevel=info"]
