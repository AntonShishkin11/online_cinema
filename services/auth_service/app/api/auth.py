from fastapi import Request, APIRouter, Depends, HTTPException, status, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from jose import jwt, JWTError

from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserRead
from app.core.config import SECRET_KEY, ALGORITHM
from app.core.security import (
    get_password_hash, verify_password,
    create_access_token, create_refresh_token,
    verify_refresh_token, create_email_verification_token,
    verify_email_verification_token,
    create_password_reset_token, verify_password_reset_token
)
from app.services.email_client import send_email_async
from app.core.redis import set_refresh_token, get_refresh_token, delete_refresh_token

router = APIRouter()
security = HTTPBearer()


@router.post("/register", response_model=UserRead, summary="Регистрация пользователя",
             description="Создаёт нового пользователя и отправляет письмо с подтверждением почты.")
async def register(user: UserCreate, session: AsyncSession = Depends(get_db)):
    token = create_email_verification_token(user.email)
    send_email_async(
        user.email,
        "Подтверждение почты",
        "verify",
        token
    )

    result = await session.execute(select(User).where(User.email == user.email))
    if result.scalar():
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        name=user.name,
        email=user.email,
        password_hash=get_password_hash(user.password)
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


@router.post("/login", summary="Аутентификация пользователя",
             description="Позволяет пользователю войти по email и паролю. Возвращает access и refresh токены.")
async def login(data: UserLogin, session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(User).where(User.email == data.email))
    user = result.scalar()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Email not verified")

    access_token = create_access_token(user.email, user.role)
    refresh_token = create_refresh_token(user.email)
    await set_refresh_token(user.email, refresh_token)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.get("/verify-email", summary="Подтверждение почты",
            description="Подтверждает email по токену из письма. Активирует пользователя.")
async def verify_email(token: str, session: AsyncSession = Depends(get_db)):
    try:
        email = verify_email_verification_token(token)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    result = await session.execute(select(User).where(User.email == email))
    user = result.scalar()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.is_verified:
        return {"message": "Email already verified"}

    user.is_verified = True
    await session.commit()
    return {"message": "Email successfully verified"}


@router.post("/refresh", summary="Обновление токенов",
             description="Обновляет access и refresh токены при валидном refresh токене.")
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_db)
):
    token = credentials.credentials
    try:
        email = verify_refresh_token(token)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    stored = await get_refresh_token(email)
    if stored != token:
        raise HTTPException(status_code=401, detail="Refresh token mismatch")

    result = await session.execute(select(User).where(User.email == email))
    user = result.scalar()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_access_token = create_access_token(email, user.role)
    new_refresh_token = create_refresh_token(email)
    await set_refresh_token(email, new_refresh_token)

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }


@router.get("/me", summary="Информация о текущем пользователе",
            description="Возвращает email и роль текущего пользователя по access токену.")
def get_me(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    return {
        "email": payload.get("sub"),
        "role": payload.get("role", "user")
    }


@router.post("/request-password-reset", summary="Запрос на сброс пароля",
             description="Отправляет письмо с ссылкой на сброс пароля пользователю.")
async def request_password_reset(email: str = Form(...), session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(User).where(User.email == email))
    user = result.scalar()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = create_password_reset_token(email)
    send_email_async(
        email,
        "Сброс пароля",
        "reset",
        token
    )
    return {"message": "Password reset email sent"}


@router.post("/reset-password", summary="Сброс пароля",
             description="Сбрасывает пароль по токену из письма.")
async def reset_password(token: str = Form(...), new_password: str = Form(...), session: AsyncSession = Depends(get_db)):
    try:
        email = verify_password_reset_token(token)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    result = await session.execute(select(User).where(User.email == email))
    user = result.scalar()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password_hash = get_password_hash(new_password)
    await session.commit()
    return {"message": "Password has been reset successfully"}


@router.post("/logout", summary="Выход из системы",
             description="Удаляет refresh токен и завершает сессию пользователя.")
async def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        email = verify_refresh_token(token)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    await delete_refresh_token(email)
    return {"message": "Logged out"}
