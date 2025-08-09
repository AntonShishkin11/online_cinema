from fastapi import FastAPI
from app.api import internal_users
from app.api import auth
from app.models.user import Base
from app.db.database import engine

app = FastAPI(title="Auth Service")
app.include_router(internal_users.router)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
