
FROM python:3.11-slim

WORKDIR /app

COPY ./app /app/app
COPY .env /app/.env
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

CMD ["celery", "-A", "app.worker_main:celery_app", "worker", "--loglevel=info", "-Q", "emails"]
