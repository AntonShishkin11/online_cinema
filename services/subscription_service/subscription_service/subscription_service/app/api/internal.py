from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from app.database import get_db
from app.models import Subscription, SubscriptionStatus
from app.schemas import AccessCheckResponse, ActivateSubscriptionRequest
import os

router = APIRouter()
INTERNAL_SECRET = os.getenv("INTERNAL_SECRET", "")

def require_internal_secret(x_internal_secret: str = Header(..., alias="X-Internal-Secret")):
    if not INTERNAL_SECRET or x_internal_secret != INTERNAL_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True

@router.get("/subscription/access-check/{user_id}", response_model=AccessCheckResponse)
async def access_check(user_id: int, _: bool = Depends(require_internal_secret), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Subscription).where(Subscription.user_id == user_id))
    sub = result.scalar_one_or_none()
    has_access = bool(sub and sub.status == SubscriptionStatus.active and (sub.expires_at is not None) and sub.expires_at > datetime.utcnow())
    return {"access": has_access}

@router.post("/subscription/activate/{user_id}")
async def activate_internal(user_id: int, req: ActivateSubscriptionRequest, _: bool = Depends(require_internal_secret), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Subscription).where(Subscription.user_id == user_id))
    sub = result.scalar_one_or_none()
    new_exp = datetime.utcnow() + timedelta(days=req.duration_days)
    if sub:
        sub.status = SubscriptionStatus.active
        # продлеваем от текущей даты, можно поменять на max(expires_at, now) по бизнес-правилу
        sub.expires_at = new_exp if (not sub.expires_at or sub.expires_at < datetime.utcnow()) else sub.expires_at + timedelta(days=req.duration_days)
    else:
        sub = Subscription(user_id=user_id, status=SubscriptionStatus.active, expires_at=new_exp)
        db.add(sub)
    await db.commit()
    return {"message": "Subscription activated", "expires_at": (sub.expires_at or new_exp)}
