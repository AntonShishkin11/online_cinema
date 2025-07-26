
from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()

celery_app = Celery(
    'email_service',
    broker=os.getenv('REDIS_BROKER_URL'),
    backend=os.getenv('REDIS_BACKEND_URL')
)

celery_app.conf.task_routes = {
    'app.tasks.send_email_task': {'queue': 'emails'}
}
