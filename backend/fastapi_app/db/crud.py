from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Task

async def create_task(session: AsyncSession, user_id: str, payload: dict) -> Task:
    task = Task(user_id=user_id, payload=payload)
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task

async def get_task(session: AsyncSession, task_id: int) -> Task | None:
    result = await session.execute(select(Task).where(Task.id == task_id))
    return result.scalars().first()

async def set_task_result(session: AsyncSession, task_id: int, result: dict) -> Task | None:
    stmt = (
        update(Task)
        .where(Task.id == task_id)
        .values(status="done", result=result)
        .execution_options(synchronize_session="fetch")
    )
    await session.execute(stmt)
    await session.commit()
    return await get_task(session, task_id)
