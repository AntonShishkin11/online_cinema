#!/bin/sh

echo "📦 Ждём базу данных..."
sleep 5

echo "🔄 Применяем миграции..."
alembic upgrade head

echo "🚀 Запускаем сервис..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000