from pydantic import BaseModel, EmailStr
from typing import Optional, List


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    is_blocked: bool
    is_verified: bool

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    role: Optional[str] = None
    is_blocked: Optional[bool] = None


class UserListResponse(BaseModel):
    users: List[UserRead]
    total: int
