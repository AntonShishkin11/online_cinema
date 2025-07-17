from fastapi import APIRouter, Query, HTTPException
from typing import Optional

from app.schemas.user import UserBase, UserListResponse, UserUpdate
from app.services import auth_client

router = APIRouter()

@router.get("/users", response_model=UserListResponse)
async def list_users(
    query: Optional[str] = None,
    role: Optional[str] = Query(None, pattern="^(user|moderator|admin)$"),
    is_blocked: Optional[bool] = None,
    limit: int = 20,
    offset: int = 0
):
    return await auth_client.get_users(query, role, is_blocked, limit, offset)

@router.get("/users/{user_id}", response_model=UserBase)
async def get_user(user_id: int):
    return await auth_client.get_user_by_id(user_id)

@router.patch("/users/{user_id}", response_model=UserBase)
async def patch_user(user_id: int, update: UserUpdate):
    if not update.dict(exclude_unset=True):
        raise HTTPException(status_code=400, detail="No fields to update")
    return await auth_client.update_user(user_id, update.dict(exclude_unset=True))
