
from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.schemas import AccessCheckResponse
from app.models import Subscription, SubscriptionStatus
from app.database import get_db
import os

router = APIRouter()

INTERNAL_SECRET = os.getenv("INTERNAL_SECRET", "")

@router.get("/access-check/{user_id}", response_model=AccessCheckResponse)
async def access_check(
    user_id: int,
    x_internal_secret: str | None = Header(default=None, convert_underscores=False),
    db: AsyncSession = Depends(get_db),
):
    if not INTERNAL_SECRET or x_internal_secret != INTERNAL_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")
    result = await db.execute(select(Subscription).where(Subscription.user_id == user_id))
    sub = result.scalar_one_or_none()
    has_access = bool(sub and sub.status == SubscriptionStatus.active and sub.expires_at > datetime.utcnow())
    return {"access": has_access}
