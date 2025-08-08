
from pydantic import BaseModel, Field
from datetime import datetime

class SubscriptionStatusResponse(BaseModel):
    status: str
    expires_at: datetime

class ActivateSubscriptionRequest(BaseModel):
    duration_days: int = Field(ge=1, le=365)

class AccessCheckResponse(BaseModel):
    access: bool
