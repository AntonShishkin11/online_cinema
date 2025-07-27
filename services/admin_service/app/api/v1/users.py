from fastapi import APIRouter, Query, HTTPException, Depends
from typing import Optional

from app.core.security import get_current_user_with_role
from app.schemas.user import UserBase, UserListResponse, UserUpdate
from app.services import auth_client

router = APIRouter()


@router.get(
    "/users",
    response_model=UserListResponse,
    summary="Список пользователей",
    description="Получает список пользователей с возможностью фильтрации по имени, роли и блокировке. Только для админов и модераторов.",
)
async def list_users(
    query: Optional[str] = None,
    role: Optional[str] = Query(None, pattern="^(user|moderator|admin)$"),
    is_blocked: Optional[bool] = None,
    limit: int = 20,
    offset: int = 0,
    _: dict = Depends(get_current_user_with_role(("admin", "moderator")))
):
    return await auth_client.get_users(query, role, is_blocked, limit, offset)


@router.get(
    "/users/{user_id}",
    response_model=UserBase,
    summary="Получить пользователя по ID",
    description="Возвращает информацию о пользователе по его ID. Только для админов и модераторов.",
)
async def get_user(
    user_id: int,
    _: dict = Depends(get_current_user_with_role(("admin", "moderator")))
):
    return await auth_client.get_user_by_id(user_id)


@router.patch(
    "/users/{user_id}",
    response_model=UserBase,
    summary="Обновить пользователя",
    description="Позволяет изменить данные пользователя (роль, блокировка). Только для ролей admin и moderator.",
)
async def patch_user(
    user_id: int,
    update: UserUpdate,
    _: dict = Depends(get_current_user_with_role(("admin", "moderator")))
):
    if not update.dict(exclude_unset=True):
        raise HTTPException(status_code=400, detail="No fields to update")
    return await auth_client.update_user(user_id, update.dict(exclude_unset=True))

