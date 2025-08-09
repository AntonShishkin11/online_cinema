from pydantic import BaseModel, Field
from datetime import datetime
class SubscriptionStatusResponse(BaseModel):
    status: str
    expires_at: datetime
class ActivateSubscriptionRequest(BaseModel):
    duration_days: int = Field(ge=1, le=365)
class AccessCheckResponse(BaseModel):
    access: bool


class PlanBase(BaseModel):
    name: str
    description: str | None = None
    price: float
    duration_days: int


class PlanCreate(PlanBase):
    pass


class PlanUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    duration_days: int | None = None


class PlanOut(PlanBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True
