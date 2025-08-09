from sqlalchemy import Column, Integer, String, Enum, DateTime, Numeric, UniqueConstraint, Boolean
from sqlalchemy.sql import func
import enum
from app.db.session import Base

class PaymentStatus(str, enum.Enum):
    pending = "pending"
    succeeded = "succeeded"
    failed = "failed"
    canceled = "canceled"

class PaymentAttempt(Base):
    __tablename__ = "payment_attempts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    plan_id = Column(String, nullable=False)
    provider = Column(String, nullable=False)
    provider_payment_id = Column(String, index=True)            # e.g., YooKassa payment.id
    provider_session_id = Column(String, index=True)            # for hosted checkout sessions
    payment_method_id = Column(String, index=True)              # for recurring
    idempotence_key = Column(String, index=True)                # for retries
    status = Column(Enum(PaymentStatus), default=PaymentStatus.pending, nullable=False)
    amount = Column(Numeric(10, 2), nullable=True)
    currency = Column(String, nullable=True)
    duration_days = Column(Integer, nullable=False)             # subscription prolongation
    capture_required = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("provider", "provider_payment_id", name="uq_provider_payment"),
    )
