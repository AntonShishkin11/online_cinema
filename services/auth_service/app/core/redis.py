from redis.asyncio import Redis
from app.core.config import REDIS_URL

redis = Redis.from_url(REDIS_URL, decode_responses=True)

REFRESH_PREFIX = "refresh_token:"


async def set_refresh_token(email: str, token: str, expires_in: int = 7 * 24 * 3600):
    key = f"{REFRESH_PREFIX}{email}"
    await redis.set(key, token, ex=expires_in)


async def get_refresh_token(email: str) -> str | None:
    key = f"{REFRESH_PREFIX}{email}"
    return await redis.get(key)


async def delete_refresh_token(email: str):
    key = f"{REFRESH_PREFIX}{email}"
    await redis.delete(key)
