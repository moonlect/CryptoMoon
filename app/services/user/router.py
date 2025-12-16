"""User Service API routes."""
from datetime import datetime, timedelta
from typing import Tuple
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.dependencies import get_current_user, get_current_user_subscription
from app.core.security import verify_password, get_password_hash
from app.models.user import User, Subscription, UserPreferences
from app.schemas.user import (
    UserProfileResponse,
    UserPreferencesResponse,
    UserPreferencesUpdate,
    ChangePasswordRequest,
    SubscriptionResponse,
    SubscriptionUpdate,
)

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.get("/me", response_model=UserProfileResponse)
async def get_current_user_profile(
    user_and_plan: Tuple = Depends(get_current_user_subscription),
    db: AsyncSession = Depends(get_db),
):
    """Get current user profile."""
    user, plan = user_and_plan

    # Get subscription details
    result = await db.execute(
        select(Subscription).where(Subscription.user_id == user.id)
    )
    subscription = result.scalar_one_or_none()

    return UserProfileResponse(
        id=user.id,
        email=user.email,
        created_at=user.created_at,
        subscription_plan=plan,
        subscription_end_date=subscription.end_date if subscription else None,
        last_login=user.last_login,
    )


@router.get("/me/preferences", response_model=UserPreferencesResponse)
async def get_user_preferences(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get user preferences."""
    result = await db.execute(
        select(UserPreferences).where(UserPreferences.user_id == user.id)
    )
    preferences = result.scalar_one_or_none()

    if not preferences:
        # Create default preferences if they don't exist
        preferences = UserPreferences(user_id=user.id)
        db.add(preferences)
        await db.commit()
        await db.refresh(preferences)

    return UserPreferencesResponse(
        theme=preferences.theme,
        font_size=preferences.font_size,
        notifications_enabled=preferences.notifications_enabled,
        email_notifications=preferences.email_notifications,
        mexc_spot_futures_enabled=preferences.mexc_spot_futures_enabled,
        mexc_spot_futures_min_spread=str(preferences.mexc_spot_futures_min_spread),
        mexc_spot_futures_sound=preferences.mexc_spot_futures_sound,
        mexc_spot_futures_browser_notif=preferences.mexc_spot_futures_browser_notif,
        mexc_spot_futures_email_notif=preferences.mexc_spot_futures_email_notif,
        funding_rate_enabled=preferences.funding_rate_enabled,
        funding_rate_min_profit=str(preferences.funding_rate_min_profit),
        funding_rate_sound=preferences.funding_rate_sound,
        funding_rate_browser_notif=preferences.funding_rate_browser_notif,
        funding_rate_email_notif=preferences.funding_rate_email_notif,
        mexc_dex_enabled=preferences.mexc_dex_enabled,
        mexc_dex_min_spread=str(preferences.mexc_dex_min_spread),
        mexc_dex_sound=preferences.mexc_dex_sound,
        mexc_dex_browser_notif=preferences.mexc_dex_browser_notif,
        mexc_dex_email_notif=preferences.mexc_dex_email_notif,
    )


@router.put("/me/preferences", response_model=UserPreferencesResponse)
async def update_user_preferences(
    preferences_update: UserPreferencesUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update user preferences."""
    result = await db.execute(
        select(UserPreferences).where(UserPreferences.user_id == user.id)
    )
    preferences = result.scalar_one_or_none()

    if not preferences:
        preferences = UserPreferences(user_id=user.id)
        db.add(preferences)
        await db.flush()

    # Update only provided fields
    update_data = preferences_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(preferences, field, value)

    await db.commit()
    await db.refresh(preferences)

    return UserPreferencesResponse(
        theme=preferences.theme,
        font_size=preferences.font_size,
        notifications_enabled=preferences.notifications_enabled,
        email_notifications=preferences.email_notifications,
        mexc_spot_futures_enabled=preferences.mexc_spot_futures_enabled,
        mexc_spot_futures_min_spread=str(preferences.mexc_spot_futures_min_spread),
        mexc_spot_futures_sound=preferences.mexc_spot_futures_sound,
        mexc_spot_futures_browser_notif=preferences.mexc_spot_futures_browser_notif,
        mexc_spot_futures_email_notif=preferences.mexc_spot_futures_email_notif,
        funding_rate_enabled=preferences.funding_rate_enabled,
        funding_rate_min_profit=str(preferences.funding_rate_min_profit),
        funding_rate_sound=preferences.funding_rate_sound,
        funding_rate_browser_notif=preferences.funding_rate_browser_notif,
        funding_rate_email_notif=preferences.funding_rate_email_notif,
        mexc_dex_enabled=preferences.mexc_dex_enabled,
        mexc_dex_min_spread=str(preferences.mexc_dex_min_spread),
        mexc_dex_sound=preferences.mexc_dex_sound,
        mexc_dex_browser_notif=preferences.mexc_dex_browser_notif,
        mexc_dex_email_notif=preferences.mexc_dex_email_notif,
    )


@router.post("/me/change-password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    password_data: ChangePasswordRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Change user password."""
    # Verify current password
    if not verify_password(password_data.current_password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect",
        )

    # Update password
    user.password_hash = get_password_hash(password_data.new_password)
    await db.commit()


@router.get("/me/subscription", response_model=SubscriptionResponse)
async def get_user_subscription(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get user subscription."""
    result = await db.execute(
        select(Subscription).where(Subscription.user_id == user.id)
    )
    subscription = result.scalar_one_or_none()

    if not subscription:
        # Create free subscription if it doesn't exist
        subscription = Subscription(user_id=user.id, plan="free", status="active")
        db.add(subscription)
        await db.commit()
        await db.refresh(subscription)

    return SubscriptionResponse(
        plan=subscription.plan,
        status=subscription.status,
        start_date=subscription.start_date,
        end_date=subscription.end_date,
    )


@router.put("/me/subscription", response_model=SubscriptionResponse)
async def update_user_subscription(
    subscription_update: SubscriptionUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update user subscription plan."""
    if subscription_update.plan not in ["free", "vip"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid plan. Must be 'free' or 'vip'",
        )

    result = await db.execute(
        select(Subscription).where(Subscription.user_id == user.id)
    )
    subscription = result.scalar_one_or_none()

    if not subscription:
        subscription = Subscription(
            user_id=user.id,
            plan=subscription_update.plan,
            status="active",
        )
        db.add(subscription)
    else:
        # In MVP: instant activation (no payment processing)
        subscription.plan = subscription_update.plan
        subscription.status = "active"
        # For free plan, allow downgrade only at midnight UTC (simplified for MVP)
        if subscription_update.plan == "free":
            subscription.end_date = None
        else:
            # For VIP, set end_date to 30 days from now (MVP)
            subscription.end_date = datetime.utcnow() + timedelta(days=30)

    await db.commit()
    await db.refresh(subscription)

    return SubscriptionResponse(
        plan=subscription.plan,
        status=subscription.status,
        start_date=subscription.start_date,
        end_date=subscription.end_date,
    )

