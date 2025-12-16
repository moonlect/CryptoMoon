"""User models."""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class User(Base):
    """User model."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    subscription = relationship("Subscription", back_populates="user", uselist=False)
    preferences = relationship("UserPreferences", back_populates="user", uselist=False)


class Subscription(Base):
    """Subscription model."""

    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    plan = Column(String(50), default="free")  # 'free', 'vip'
    status = Column(String(50), default="active")  # 'active', 'cancelled', 'expired'
    start_date = Column(DateTime(timezone=True), server_default=func.now())
    end_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="subscription")


class UserPreferences(Base):
    """User preferences model."""

    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)

    # General preferences
    theme = Column(String(20), default="auto")  # 'light', 'dark', 'auto'
    font_size = Column(String(20), default="normal")  # 'small', 'normal', 'large'
    notifications_enabled = Column(Boolean, default=True)
    email_notifications = Column(Boolean, default=False)

    # MEXC Spot & Futures
    mexc_spot_futures_enabled = Column(Boolean, default=True)
    mexc_spot_futures_min_spread = Column(String(10), default="0")
    mexc_spot_futures_sound = Column(Boolean, default=True)
    mexc_spot_futures_browser_notif = Column(Boolean, default=True)
    mexc_spot_futures_email_notif = Column(Boolean, default=False)

    # Funding Rate
    funding_rate_enabled = Column(Boolean, default=True)
    funding_rate_min_profit = Column(String(10), default="0")
    funding_rate_sound = Column(Boolean, default=True)
    funding_rate_browser_notif = Column(Boolean, default=True)
    funding_rate_email_notif = Column(Boolean, default=False)

    # MEXC & DEX
    mexc_dex_enabled = Column(Boolean, default=True)
    mexc_dex_min_spread = Column(String(10), default="0")
    mexc_dex_sound = Column(Boolean, default=True)
    mexc_dex_browser_notif = Column(Boolean, default=True)
    mexc_dex_email_notif = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="preferences")


