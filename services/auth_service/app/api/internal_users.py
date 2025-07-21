from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import String, cast
from typing import Optional

from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserRead, UserUpdate, UserListResponse

router = APIRouter(prefix="/internal/users", tags=["internal-users"])

@router.get("", response_model=UserListResponse)
async def list_users(
    query: Optional[str] = None,
    role: Optional[str] = Query(None, pattern="^(user|moderator|admin)$"),
    is_blocked: Optional[bool] = None,
    limit: int = 20,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    base_stmt = select(User)
    if query:
        base_stmt = base_stmt.where(
            (User.email.ilike(f"%{query}%")) |
            (User.name.ilike(f"%{query}%")) |
            cast(User.id, String).ilike(f"%{query}%")
        )
    if role:
        base_stmt = base_stmt.where(User.role == role)
    if is_blocked is not None:
        base_stmt = base_stmt.where(User.is_blocked == is_blocked)

    # Получаем пользователей
    result = await db.execute(base_stmt.offset(offset).limit(limit))
    users = result.scalars().all()

    total = len(users)

    return UserListResponse(users=users, total=total)

@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.patch("/{user_id}", response_model=UserRead)
async def update_user(user_id: int, update: UserUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    data = update.dict(exclude_unset=True)
    for key, value in data.items():
        setattr(user, key, value)
    await db.commit()
    await db.refresh(user)
    return user
