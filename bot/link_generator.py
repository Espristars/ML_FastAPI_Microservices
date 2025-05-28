import os
from itsdangerous import URLSafeSerializer

SECRET_KEY = os.getenv("LINK_SECRET", "change_me")
BASE_URL = os.getenv("FRONTEND_URL", "http://frontend:3000")

serializer = URLSafeSerializer(SECRET_KEY, salt="task-link")


def make_task_link(user_id: str, task_id: int) -> str:
    token = serializer.dumps({"user_id": user_id, "task_id": task_id})
    return f"{BASE_URL}/tasks/{token}"


def parse_task_token(token: str) -> dict:
    return serializer.loads(token)
