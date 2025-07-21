from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.services.auth_client import get_user_info

security = HTTPBearer()

def get_current_user_with_role(required_roles: tuple[str, ...]):
    async def _verify(credentials: HTTPAuthorizationCredentials = Depends(security)):
        token = credentials.credentials
        try:
            user_data = await get_user_info(token)
            if user_data["role"] not in required_roles:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")
            return user_data
        except Exception:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный токен или ошибка при получении пользователя")
    return _verify