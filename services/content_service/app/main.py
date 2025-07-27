
from fastapi import FastAPI
from app.api.v1 import movies

app = FastAPI(title="Content Service")

app.include_router(movies.router, prefix="/api/v1")
