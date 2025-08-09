from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models import PaymentAttempt, PaymentStatus
from app.schemas.payments import WebhookEvent
from app.services.subscription_client import activate_subscription_for_user

router = APIRouter()

@router.post("/mock")
async def mock_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    payload = await request.json()
    event = WebhookEvent(**payload)
    attempt = None
    if event.attempt_id:
        result = await db.execute(select(PaymentAttempt).where(PaymentAttempt.id == event.attempt_id))
        attempt = result.scalar_one_or_none()
    elif event.provider_payment_id:
        result = await db.execute(select(PaymentAttempt).where(PaymentAttempt.provider_payment_id == event.provider_payment_id))
        attempt = result.scalar_one_or_none()

    if not attempt:
        return {"ok": True}

    if event.event == "payment_succeeded" and attempt.status == PaymentStatus.pending and event.user_id:
        attempt.status = PaymentStatus.succeeded
        await db.commit()
        await activate_subscription_for_user(event.user_id, attempt.duration_days)
    elif event.event in {"payment_failed", "payment_canceled"}:
        attempt.status = PaymentStatus.failed if event.event == "payment_failed" else PaymentStatus.canceled
        await db.commit()

    return {"ok": True}
