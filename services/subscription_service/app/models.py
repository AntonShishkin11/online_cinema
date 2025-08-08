
import enum
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, Enum, Index
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class SubscriptionStatus(str, enum.Enum):
    active = "active"
    inactive = "inactive"

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, unique=True, nullable=False, index=True)
    status = Column(Enum(SubscriptionStatus), nullable=False, default=SubscriptionStatus.active)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

Index("ix_subscriptions_user_status", Subscription.user_id, Subscription.status)
