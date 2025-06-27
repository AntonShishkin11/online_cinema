from fastapi import FastAPI
from app.api import auth, movies

app = FastAPI()

app.include_router(auth.router, prefix="/auth")
app.include_router(movies.router, prefix="/movies")

@app.get("/")
def root():
    return {"message": "Online Cinema API"}