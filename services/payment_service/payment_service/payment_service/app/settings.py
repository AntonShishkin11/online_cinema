import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@postgres:5432/payments")
SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
SUBSCRIPTION_SERVICE_URL = os.getenv("SUBSCRIPTION_SERVICE_URL", "http://subscription_service:8000")
INTERNAL_SECRET = os.getenv("INTERNAL_SECRET", "dev-internal")
PROVIDER = os.getenv("PAYMENT_PROVIDER", "mock")

# recurring / scheduler
ENABLE_BILLING_SCHEDULER = os.getenv("ENABLE_BILLING_SCHEDULER", "false").lower() in {"1","true","yes"}
