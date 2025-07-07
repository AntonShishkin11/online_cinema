from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def decode_token(token: str):
    if token == "admin_token":
        return {"role": "admin"}
    elif token == "moderator_token":
        return {"role": "moderator"}
    else:
        return {"role": "user"}

def get_current_user_admin_or_moderator(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user = decode_token(token)
    if user["role"] not in ("admin", "moderator"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return user