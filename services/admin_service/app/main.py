from fastapi import FastAPI
from app.api.v1 import films_b2c, users

app = FastAPI(title="Admin Service")

app.include_router(films_b2c.router, prefix="/admin/films/b2c", tags=["Films B2C"])
app.include_router(users.router, prefix="/admin/users", tags=["Users"])