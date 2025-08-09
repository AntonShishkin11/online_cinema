from .base import BaseProvider
import json, urllib.parse, uuid

class MockProvider(BaseProvider):
    async def create_checkout(self, *, user_id: int, plan_id: str, duration_days: int, success_url: str, cancel_url: str) -> dict:
        provider_payment_id = str(uuid.uuid4())
        provider_session_id = f"mock_{user_id}_{plan_id}_{provider_payment_id[:8]}"
        query = urllib.parse.urlencode({ "user_id": user_id, "plan_id": plan_id, "duration_days": duration_days, "pid": provider_payment_id })
        return {
            "provider_payment_id": provider_payment_id,
            "provider_session_id": provider_session_id,
            "payment_url": f"/mock-pay?{query}"
        }

    async def parse_webhook(self, body: bytes, headers: dict) -> dict:
        return json.loads(body.decode("utf-8"))
