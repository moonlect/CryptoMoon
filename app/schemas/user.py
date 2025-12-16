"""User service schemas."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserProfileResponse(BaseModel):
    """User profile response schema."""

    id: int
    email: str
    created_at: datetime
    subscription_plan: str
    subscription_end_date: Optional[datetime] = None
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserPreferencesResponse(BaseModel):
    """User preferences response schema."""

    theme: str = "auto"
    font_size: str = "normal"
    notifications_enabled: bool = True
    email_notifications: bool = False

    # MEXC Spot & Futures
    mexc_spot_futures_enabled: bool = True
    mexc_spot_futures_min_spread: str = "0"
    mexc_spot_futures_sound: bool = True
    mexc_spot_futures_browser_notif: bool = True
    mexc_spot_futures_email_notif: bool = False

    # Funding Rate
    funding_rate_enabled: bool = True
    funding_rate_min_profit: str = "0"
    funding_rate_sound: bool = True
    funding_rate_browser_notif: bool = True
    funding_rate_email_notif: bool = False

    # MEXC & DEX
    mexc_dex_enabled: bool = True
    mexc_dex_min_spread: str = "0"
    mexc_dex_sound: bool = True
    mexc_dex_browser_notif: bool = True
    mexc_dex_email_notif: bool = False

    class Config:
        from_attributes = True


class UserPreferencesUpdate(BaseModel):
    """User preferences update schema."""

    theme: Optional[str] = None
    font_size: Optional[str] = None
    notifications_enabled: Optional[bool] = None
    email_notifications: Optional[bool] = None

    # MEXC Spot & Futures
    mexc_spot_futures_enabled: Optional[bool] = None
    mexc_spot_futures_min_spread: Optional[str] = None
    mexc_spot_futures_sound: Optional[bool] = None
    mexc_spot_futures_browser_notif: Optional[bool] = None
    mexc_spot_futures_email_notif: Optional[bool] = None

    # Funding Rate
    funding_rate_enabled: Optional[bool] = None
    funding_rate_min_profit: Optional[str] = None
    funding_rate_sound: Optional[bool] = None
    funding_rate_browser_notif: Optional[bool] = None
    funding_rate_email_notif: Optional[bool] = None

    # MEXC & DEX
    mexc_dex_enabled: Optional[bool] = None
    mexc_dex_min_spread: Optional[str] = None
    mexc_dex_sound: Optional[bool] = None
    mexc_dex_browser_notif: Optional[bool] = None
    mexc_dex_email_notif: Optional[bool] = None


class ChangePasswordRequest(BaseModel):
    """Change password request schema."""

    current_password: str
    new_password: str = Field(..., min_length=8, description="Password must be at least 8 characters")


class SubscriptionResponse(BaseModel):
    """Subscription response schema."""

    plan: str
    status: str
    start_date: datetime
    end_date: Optional[datetime] = None

    class Config:
        from_attributes = True


class SubscriptionUpdate(BaseModel):
    """Subscription update schema."""

    plan: str = Field(..., description="Plan: 'free' or 'vip'")


class LoginHistoryResponse(BaseModel):
    """Login history response schema."""

    id: int
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True



