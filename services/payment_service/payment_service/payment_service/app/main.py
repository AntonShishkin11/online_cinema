from fastapi import FastAPI
from app.api.v1.payments import router as payments_router
from app.api.v1.webhooks import router as webhooks_router
from app.api.v1.internal import router as internal_router

app = FastAPI(title="Payment Service", version="1.1.0")
app.include_router(payments_router, prefix="/api/v1/payments", tags=["payments"])
app.include_router(webhooks_router, prefix="/webhooks", tags=["webhooks"])
app.include_router(internal_router, prefix="/internal", tags=["internal"])
