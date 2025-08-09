
import httpx
from app.settings import SUBSCRIPTION_SERVICE_URL

async def get_plan(plan_id: str) -> dict:
    url = f"{SUBSCRIPTION_SERVICE_URL}/api/v1/subscription/plans/{plan_id}"
    async with httpx.AsyncClient(timeout=5) as client:
        r = await client.get(url)
        r.raise_for_status()
        return r.json()
