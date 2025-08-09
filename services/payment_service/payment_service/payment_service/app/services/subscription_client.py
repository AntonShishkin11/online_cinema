import httpx
from app.settings import SUBSCRIPTION_SERVICE_URL, INTERNAL_SECRET

async def activate_subscription_for_user(user_id: int, duration_days: int) -> None:
    url = f"{SUBSCRIPTION_SERVICE_URL}/internal/subscription/activate/{user_id}"
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post(url, json={ "duration_days": duration_days }, headers={"X-Internal-Secret": INTERNAL_SECRET})
        r.raise_for_status()

async def access_check(user_id: int) -> bool:
    url = f"{SUBSCRIPTION_SERVICE_URL}/internal/subscription/access-check/{user_id}"
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(url, headers={"X-Internal-Secret": INTERNAL_SECRET})
        r.raise_for_status()
        data = r.json()
        return bool(data.get("access"))
