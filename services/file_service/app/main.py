from fastapi import FastAPI
from app.api.v1.stream import router as stream_router

app = FastAPI(title="File Service")

app.include_router(stream_router, prefix="/api/v1/stream")
