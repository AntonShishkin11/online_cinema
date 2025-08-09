
import httpx
from app.core.config import settings

async def fetch_plan(plan_id: int):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{settings.SUBSCRIPTION_SERVICE_URL}/plans/{plan_id}")
        if r.status_code != 200:
            return None
        return r.json()

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models import PaymentAttempt, PaymentStatus
from app.schemas.payments import CheckoutRequest, CheckoutResponse, ChargeRequest, OK
from app.services.providers.mock_provider import MockProvider
from app.core.security import get_current_user_id
from fastapi import HTTPException
from sqlalchemy import select
from app.schemas.payments import OK
from app.services.subscription_client import activate_subscription_for_user
from app.services.plans_client import get_plan
from app.models import PaymentAttempt

router = APIRouter()

@router.post("/checkout", response_model=CheckoutResponse)
async def create_checkout(req: CheckoutRequest, user_id: int = Depends(get_current_user_id), db: AsyncSession = Depends(get_db)):
    provider = MockProvider()  # swap by env later
    checkout = await provider.create_checkout(user_id=user_id, plan_id=req.plan_id, duration_days=req.duration_days, success_url=req.success_url or "", cancel_url=req.cancel_url or "")
    attempt = PaymentAttempt(
        user_id=user_id,
        plan_id=req.plan_id,
        provider=req.provider.value,
        provider_payment_id=checkout.get("provider_payment_id"),
        provider_session_id=checkout.get("provider_session_id"),
        status=PaymentStatus.pending,
        duration_days=req.duration_days
    )
    db.add(attempt)
    await db.commit()
    await db.refresh(attempt)
    return CheckoutResponse(
        attempt_id=attempt.id,
        payment_url=f"/payments/api/v1/payments/mock/confirm?attempt_id={attempt.id}&user_id={user_id}"
    )


@router.get("/mock/confirm", response_model=OK)
async def mock_confirm(attempt_id: int, user_id: int, db: AsyncSession = Depends(get_db)):
    """Имитация редиректа с успешной оплаты от провайдера.
       Дергаем наш же вебхук-обработчик логики (без подписи, т.к. mock)."""
    from app.models import PaymentAttempt, PaymentStatus

    res = await db.execute(select(PaymentAttempt).where(PaymentAttempt.id == attempt_id))
    attempt = res.scalar_one_or_none()
    if not attempt:
        raise HTTPException(status_code=404, detail="attempt not found")

    if attempt.status != PaymentStatus.pending:
        return OK()  # идемпотентно

    attempt.status = PaymentStatus.succeeded
    await db.commit()

    # Активируем/продлеваем подписку пользователю
    await activate_subscription_for_user(user_id, attempt.duration_days)
    return OK()

@router.get("/attempts/{attempt_id}")
async def get_attempt(attempt_id: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(PaymentAttempt).where(PaymentAttempt.id == attempt_id))
    a = res.scalar_one_or_none()
    if not a:
        raise HTTPException(status_code=404, detail="not found")
    return {
        "id": a.id,
        "status": a.status.value,
        "plan_id": a.plan_id,
        "duration_days": a.duration_days,
        "provider": a.provider,
        "created_at": a.created_at
    }
