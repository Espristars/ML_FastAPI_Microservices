import os
import asyncio
import json
from aiokafka import AIOKafkaConsumer
from aiogram import Bot
from dotenv import load_dotenv
from link_generator import parse_task_token


load_dotenv()

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
RESULTS_TOPIC = "tasks_results"
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)


async def consume_results():
    consumer = AIOKafkaConsumer(
        RESULTS_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP,
        group_id="bot-consumer-group",
        auto_offset_reset="earliest",
    )
    await consumer.start()
    try:
        async for msg in consumer:
            payload = json.loads(msg.value.decode())
            user_id = int(payload["user_id"])
            result = payload["result"]
            text = f"Ваша задача #{payload['task_id']} завершена! Результат:\n{result}"
            await bot.send_message(user_id, text)
    finally:
        await consumer.stop()


def start_consumer_loop():
    loop = asyncio.get_event_loop()
    loop.create_task(consume_results())
