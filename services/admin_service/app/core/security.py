import os
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

bearer_scheme = HTTPBearer(auto_error=True)

def get_current_user_with_role(roles: tuple):
    async def wrapper(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
        token = credentials.credentials

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        sub = payload.get("sub")
        if not sub:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token: no sub")

        # ⚠️ Больше НЕ валидируем как UUID — принимаем как строку/число
        user_id = str(sub)

        user_role = payload.get("role")
        if user_role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

        return {"user_id": user_id, "role": user_role}
    return wrapper
