from fastapi import APIRouter, Depends
from datetime import datetime, timedelta
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import SubscriptionStatusResponse, ActivateSubscriptionRequest
from app.models import Subscription, SubscriptionStatus
from app.database import get_db
from app.core.security import get_current_user_id
router = APIRouter()
@router.get("/status", response_model=SubscriptionStatusResponse)
async def get_subscription_status(user_id: int = Depends(get_current_user_id), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Subscription).where(Subscription.user_id == user_id))
    sub = result.scalar_one_or_none()
    if not sub:
        return {"status":"inactive","expires_at": datetime.utcnow()}
    return {"status": sub.status.value, "expires_at": sub.expires_at}
@router.post("/activate")
async def activate_subscription(payload: ActivateSubscriptionRequest, user_id: int = Depends(get_current_user_id), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Subscription).where(Subscription.user_id == user_id))
    sub = result.scalar_one_or_none()
    now = datetime.utcnow()
    base = max(now, sub.expires_at) if sub and sub.status == SubscriptionStatus.active else now
    new_exp = base + timedelta(days=payload.duration_days)
    if sub:
        sub.status = SubscriptionStatus.active
        sub.expires_at = new_exp
    else:
        sub = Subscription(user_id=user_id, status=SubscriptionStatus.active, expires_at=new_exp)
        db.add(sub)
    await db.commit()
    return {"message":"Subscription activated","expires_at": new_exp}
@router.delete("/deactivate", status_code=204)
async def deactivate_subscription(user_id: int = Depends(get_current_user_id), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Subscription).where(Subscription.user_id == user_id))
    sub = result.scalar_one_or_none()
    if sub:
        sub.status = SubscriptionStatus.inactive
        sub.expires_at = datetime.utcnow()
        await db.commit()
    return

from app.api import plans
api_router.include_router(plans.router, prefix='/plans', tags=['plans'])
