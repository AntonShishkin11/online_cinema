
from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()

celery_app = Celery(
    'auth_service',
    broker=os.getenv('REDIS_URL')
)
