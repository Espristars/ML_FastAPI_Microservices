import os
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError

from .db.session import engine, SessionLocal, Base
from .api.routes import router as api_router
from .kafka.producer import init_kafka_producer, kafka_producer


app = FastAPI(title="Task Service")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router, prefix="/api/tasks", tags=["tasks"])


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await init_kafka_producer()


@app.on_event("shutdown")
async def on_shutdown():
    if kafka_producer:
        await kafka_producer.stop()
