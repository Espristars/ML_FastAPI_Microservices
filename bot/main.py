import os
import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from handlers import router
from kafka_consumer import start_consumer_loop


load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)


async def main():
    start_consumer_loop()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
