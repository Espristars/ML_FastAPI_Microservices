import os
import json
import time
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from backend.fastapi_app.db.session import SessionLocal
from backend.fastapi_app.db.crud import set_task_result


KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
TASKS_TOPIC   = os.getenv("KAFKA_TASKS_TOPIC", "tasks")
RESULTS_TOPIC = os.getenv("KAFKA_RESULTS_TOPIC", "tasks_results")


async def consume_tasks():
    consumer = AIOKafkaConsumer(
        TASKS_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP,
        group_id="celery-worker-group",
        auto_offset_reset="earliest",
    )
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP)

    await consumer.start()
    await producer.start()
    try:
        async for msg in consumer:
            data = json.loads(msg.value.decode("utf-8"))
            task_id = data["task_id"]
            payload = data.get("payload", {})

            async with SessionLocal() as session:
                await set_task_result(session, task_id, {"status": "processing"})

            result = process_ml(payload)

            async with SessionLocal() as session:
                await set_task_result(session, task_id, {"status": "done", "result": result})

            out_msg = {
                "task_id": task_id,
                "user_id": data.get("user_id"),
                "result": result,
            }
            await producer.send_and_wait(
                RESULTS_TOPIC,
                key=str(task_id).encode(),
                value=json.dumps(out_msg).encode("utf-8"),
            )

    finally:
        await consumer.stop()
        await producer.stop()


def process_ml(payload: dict) -> dict:
    time.sleep(5)
    return {"echo": payload}
