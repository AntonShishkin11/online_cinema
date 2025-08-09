import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="auth/login")
SECRET_KEY = os.getenv("SECRET_KEY", "")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ISSUER = os.getenv("JWT_ISSUER", None)
AUDIENCE = os.getenv("JWT_AUDIENCE", None)
def _verify_claims(payload: dict):
    if ISSUER and payload.get("iss") != ISSUER:
        raise HTTPException(status_code=401, detail="Invalid issuer")
    if AUDIENCE:
        aud = payload.get("aud")
        if isinstance(aud, list):
            if AUDIENCE not in aud:
                raise HTTPException(status_code=401, detail="Invalid audience")
        elif aud != AUDIENCE:
            raise HTTPException(status_code=401, detail="Invalid audience")
async def get_current_user_id(token: str = Depends(OAUTH2_SCHEME)) -> int:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"},
    )
    if not SECRET_KEY:
        raise HTTPException(status_code=500, detail="SECRET_KEY is not configured")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_aud": False})
        _verify_claims(payload)
        sub = payload.get("sub")
        if sub is None:
            raise credentials_exception
        return int(sub)
    except (JWTError, ValueError):
        raise credentials_exception
