from abc import ABC, abstractmethod

class BaseProvider(ABC):
    @abstractmethod
    async def create_checkout(self, *, user_id: int, plan_id: str, duration_days: int, success_url: str, cancel_url: str) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def parse_webhook(self, body: bytes, headers: dict) -> dict:
        raise NotImplementedError
