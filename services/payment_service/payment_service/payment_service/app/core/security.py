# payment_service/app/core/security.py
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, APIKeyQuery
from jose import jwt, JWTError
from app.settings import SECRET_KEY, ALGORITHM

bearer_scheme = HTTPBearer(auto_error=False)
access_token_query = APIKeyQuery(name="access_token", auto_error=False)

def _decode(token: str) -> int:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return int(payload.get("sub"))
    except (JWTError, ValueError, TypeError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

def get_current_user_id(
    creds: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    token_q: str | None = Depends(access_token_query),
) -> int:
    token = None
    if creds and creds.scheme.lower() == "bearer":
        token = creds.credentials
    if not token and token_q:
        token = token_q
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return _decode(token)
