import os
from dotenv import load_dotenv
load_dotenv()

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()
DATABASE_URL = os.getenv("DATABASE_URL")

# не создаём engine сразу — пусть делает env.py
def get_async_sessionmaker():
    from sqlalchemy.ext.asyncio import create_async_engine
    engine = create_async_engine(DATABASE_URL, echo=True)
    return sessionmaker(bind=engine, class_=AsyncSession, autoflush=False, autocommit=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async_session = get_async_sessionmaker()
    async with async_session() as session:
        yield session
