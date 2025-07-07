from fastapi import APIRouter, Depends
from app.core.security import get_current_user_admin_or_moderator

router = APIRouter()

@router.get("/")
async def get_users(user=Depends(get_current_user_admin_or_moderator)):
    return []

@router.patch("/{user_id}/block")
async def block_user(user_id: int, user=Depends(get_current_user_admin_or_moderator)):
    return {"message": f"User {user_id} blocked"}

@router.patch("/{user_id}/unblock")
async def unblock_user(user_id: int, user=Depends(get_current_user_admin_or_moderator)):
    return {"message": f"User {user_id} unblocked"}