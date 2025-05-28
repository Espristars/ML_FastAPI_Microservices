import os
import asyncio
from celery import Celery
from celery.signals import worker_ready
from backend.celery_worker.tasks import consume_tasks


celery_app = Celery(
    "celery_worker",
    broker=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0"),
)


celery_app.conf.worker_prefetch_multiplier = 1
celery_app.conf.task_acks_late = True


@worker_ready.connect
def start_kafka_consumer(**kwargs):
    loop = asyncio.get_event_loop()
    loop.create_task(consume_tasks())
