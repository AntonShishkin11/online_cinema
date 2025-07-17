from typing import Optional, List
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    is_blocked: bool

class UserUpdate(BaseModel):
    role: Optional[str] = None
    is_blocked: Optional[bool] = None

class UserListResponse(BaseModel):
    users: List[UserBase]
    total: int
