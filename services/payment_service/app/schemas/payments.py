from pydantic import BaseModel, Field
from enum import Enum

class ProviderEnum(str, Enum):
    mock = "mock"

class CheckoutRequest(BaseModel):
    plan_id: str
    duration_days: int = Field(ge=1, le=365)
    provider: ProviderEnum = ProviderEnum.mock
    success_url: str | None = None
    cancel_url: str | None = None

class CheckoutResponse(BaseModel):
    attempt_id: int
    payment_url: str

class WebhookEvent(BaseModel):
    event: str
    attempt_id: int | None = None
    user_id: int | None = None
    provider_payment_id: str | None = None
    provider_session_id: str | None = None
    status: str | None = None  # succeeded/failed/canceled

class ChargeRequest(BaseModel):
    user_id: int
    plan_id: str
    duration_days: int

class OK(BaseModel):
    ok: bool = True
