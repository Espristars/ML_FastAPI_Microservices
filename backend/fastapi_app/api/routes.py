from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from uuid import uuid4

from ..db import crud
from ..db.session import get_session
from ..kafka.producer import send_task_message
from ..db.models import Task as TaskModel


router = APIRouter()


class TaskCreate(BaseModel):
    user_id: str
    payload: dict


class TaskResponse(BaseModel):
    task_id: int
    status: str


class TaskStatus(BaseModel):
    task_id: int
    status: str
    result: dict | None = None


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    body: TaskCreate,
    session=Depends(get_session),
):
    task: TaskModel = await crud.create_task(session, user_id=body.user_id, payload=body.payload)
    message_key = str(uuid4()).encode()
    await send_task_message(
        topic="tasks",
        key=message_key,
        value={"task_id": task.id, "payload": body.payload},
    )
    return TaskResponse(task_id=task.id, status=task.status)


@router.get("/{task_id}", response_model=TaskStatus)
async def get_task(task_id: int, session=Depends(get_session)):
    task = await crud.get_task(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskStatus(task_id=task.id, status=task.status, result=task.result)
