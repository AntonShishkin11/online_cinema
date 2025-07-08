import asyncio
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
import os
import sys

# Добавляем путь к app, чтобы импорты работали
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))

from db.session import Base, DATABASE_URL
from models.film_b2c import FilmB2C  # ⬅️ импорт модели, чтобы Alembic её видел

# Alembic Config
config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata

# Создание async engine
def get_engine():
    return create_async_engine(DATABASE_URL, echo=True)

# Конфигурация Alembic
def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()

# Запуск в online-режиме
async def run_migrations_online():
    engine = get_engine()
    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)
        await connection.commit()

# Точка входа
if context.is_offline_mode():
    raise NotImplementedError("❌ Offline mode not supported in async setup.")
else:
    asyncio.run(run_migrations_online())
