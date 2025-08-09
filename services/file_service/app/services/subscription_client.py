import os, httpx

SUBSCRIPTION_URL = os.getenv("SUBSCRIPTION_SERVICE_URL", "http://subscription_service:8000")
INTERNAL_SECRET = os.getenv("INTERNAL_SECRET", "dev-internal")

async def has_access(user_id: int) -> bool:
    url = f"{SUBSCRIPTION_URL}/internal/subscription/access-check/{user_id}"
    async with httpx.AsyncClient(timeout=5) as client:
        r = await client.get(url, headers={"X-Internal-Secret": INTERNAL_SECRET})
        r.raise_for_status()
        return bool(r.json().get("access"))
