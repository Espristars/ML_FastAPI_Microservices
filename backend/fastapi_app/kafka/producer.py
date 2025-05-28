import os
import json
from aiokafka import AIOKafkaProducer


kafka_producer: AIOKafkaProducer | None = None


async def init_kafka_producer():
    global kafka_producer
    if kafka_producer is None:
        bootstrap = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
        kafka_producer = AIOKafkaProducer(bootstrap_servers=bootstrap)
        await kafka_producer.start()


async def send_task_message(topic: str, key: bytes, value: dict):
    if kafka_producer is None:
        raise RuntimeError("Kafka producer is not initialized")
    await kafka_producer.send_and_wait(
        topic,
        key=key,
        value=json.dumps(value).encode("utf-8")
    )
