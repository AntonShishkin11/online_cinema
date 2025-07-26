from app.core.celery import celery_app
from app import tasks  # это принудительно регистрирует таски

# можно добавить лог для проверки
print("[Celery Worker] Tasks loaded.")
