from app.services.email_service import send_verification_email
from fastapi import Request, APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.database import get_session
from jose import jwt, JWTError
from app.core.config import SECRET_KEY, ALGORITHM
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserRead
from app.core.security import get_password_hash, verify_password, create_access_token, verify_refresh_token, \
    create_refresh_token, create_email_verification_token, verify_email_verification_token

router = APIRouter()


@router.post("/register", response_model=UserRead)
async def register(user: UserCreate, session: AsyncSession = Depends(get_session)):
    token = create_email_verification_token(user.email)
    await send_verification_email(user.email, token)
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


@router.post("/login")
async def login(data: UserLogin, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).where(User.email == data.email))
    user = result.scalar()
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Email not verified")
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(user.email, user.role)
    refresh_token = create_refresh_token(user.email)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
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


@router.get("/verify-email")
async def verify_email(token: str, session: AsyncSession = Depends(get_session)):
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


@router.post("/refresh")
async def refresh_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing refresh token")

    token = auth_header.split(" ")[1]
    try:
        email = verify_refresh_token(token)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    new_access_token = create_access_token(email)
    return {"access_token": new_access_token, "token_type": "bearer"}


from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
security = HTTPBearer()

@router.get("/me")
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
