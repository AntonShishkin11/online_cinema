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


class Plan(Base):
    __tablename__ = "plans"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    duration_days = Column(Integer, nullable=False)  # сколько дней действует подписка
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
