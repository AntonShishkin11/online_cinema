import httpx
import os
from typing import Optional
from uuid import UUID

AUTH_SERVICE_URL = "http://auth_service:8000/internal/users"
AUTH_ME_URL = "http://auth_service:8000/auth/me"

INTERNAL_SECRET = os.getenv("INTERNAL_SECRET")
INTERNAL_HEADERS = {"X-Internal-Secret": INTERNAL_SECRET}


async def get_users(query: Optional[str] = None,
                    role: Optional[str] = None,
                    is_blocked: Optional[bool] = None,
                    limit: int = 20,
                    offset: int = 0):
    params = {
        "query": query,
        "role": role,
        "is_blocked": is_blocked,
        "limit": limit,
        "offset": offset,
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(
            AUTH_SERVICE_URL,
            params={k: v for k, v in params.items() if v is not None},
            headers=INTERNAL_HEADERS
        )
        response.raise_for_status()
        return response.json()


async def get_user_by_id(user_id: UUID):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{AUTH_SERVICE_URL}/{user_id}",
            headers=INTERNAL_HEADERS
        )
        response.raise_for_status()
        return response.json()


async def update_user(user_id: UUID, data: dict):
    async with httpx.AsyncClient() as client:
        response = await client.patch(
            f"{AUTH_SERVICE_URL}/{user_id}",
            json=data,
            headers=INTERNAL_HEADERS
        )
        response.raise_for_status()
        return response.json()


async def get_user_info(token: str) -> dict:
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(AUTH_ME_URL, headers=headers)
        response.raise_for_status()
        return response.json()
