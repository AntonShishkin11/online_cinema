from fastapi import APIRouter
from app.schemas.payments import OK, ChargeRequest

router = APIRouter()

@router.post("/billing/run", response_model=OK)
async def run_billing_job():
    # Placeholder: connect scheduler/cron later
    return OK()
