from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi import Header, HTTPException
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: str, role: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": str(user_id), "role": role, "type": "access", "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_email_verification_token(email: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode = {"sub": email, "type": "verify", "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_email_verification_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "verify":
            raise ValueError("Invalid token type")
        return payload.get("sub")
    except JWTError:
        raise ValueError("Invalid or expired token")


def create_refresh_token(user_id: str) -> str:
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode = {"sub": str(user_id), "type": "refresh", "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_refresh_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise ValueError("Invalid token type")
        return payload.get("sub")
    except JWTError:
        raise ValueError("Invalid or expired refresh token")


def create_password_reset_token(email: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode = {"sub": email, "type": "reset", "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_password_reset_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "reset":
            raise ValueError("Invalid token type")
        return payload.get("sub")
    except JWTError:
        raise ValueError("Invalid or expired token")


async def verify_internal_secret(x_internal_secret: str = Header(...)):
    expected_secret = os.getenv("INTERNAL_SECRET")
    if not expected_secret or x_internal_secret != expected_secret:
        raise HTTPException(status_code=403, detail="Forbidden: invalid internal token")
