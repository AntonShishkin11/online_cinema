from fastapi import APIRouter, Depends, HTTPException
from app.core.security import get_current_user_admin_or_moderator

router = APIRouter()

@router.get("/")
async def get_films(user=Depends(get_current_user_admin_or_moderator)):
    return []

@router.post("/")
async def add_film(user=Depends(get_current_user_admin_or_moderator)):
    return {"message": "Film created"}

@router.delete("/{film_id}")
async def delete_film(film_id: int, user=Depends(get_current_user_admin_or_moderator)):
    return {"message": f"Film {film_id} deleted"}