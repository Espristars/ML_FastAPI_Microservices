from aiogram import Router
from aiogram.types import Message
from link_generator import make_task_link
import httpx, os


router = Router()


@router.message(commands=["start"])
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Отправь мне команду /newtask, чтобы создать новую задачу."
    )


@router.message(commands=["newtask"])
async def cmd_newtask(message: Message):

    FASTAPI_URL = os.getenv("FASTAPI_URL", "http://fastapi:8000")
    user_id = str(message.from_user.id)

    resp = await httpx.AsyncClient().post(
        f"{FASTAPI_URL}/api/tasks/",
        json={"user_id": user_id, "payload": {}},
        timeout=5.0,
    )
    data = resp.json()
    task_id = data["task_id"]

    link = make_task_link(user_id, task_id)
    await message.answer(f"Задача создана! Следи за прогрессом здесь:\n{link}")
