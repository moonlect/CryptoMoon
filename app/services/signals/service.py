"""Signals Service business logic."""
from typing import Optional, Dict, Any
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.signal import (
    SignalMEXCSpotFutures,
    SignalFundingRate,
    SignalMEXCDEX,
)
from app.services.websocket.router import broadcast_new_signal, broadcast_signal_update
from app.services.notifications.service import notification_service


async def create_mexc_spot_futures_signal(
    db: AsyncSession,
    coin_name: str,
    position: Optional[str] = None,
    spread: Optional[Decimal] = None,
    mexc_spot_price: Optional[Decimal] = None,
    mexc_futures_price: Optional[Decimal] = None,
    spot_url: Optional[str] = None,
    futures_url: Optional[str] = None,
    deposit_enabled: bool = True,
    withdrawal_enabled: bool = True,
    dex_url: Optional[str] = None,
) -> SignalMEXCSpotFutures:
    """Create a new MEXC Spot & Futures signal."""
    signal = SignalMEXCSpotFutures(
        coin_name=coin_name,
        position=position,
        spread=spread,
        mexc_spot_price=mexc_spot_price,
        mexc_futures_price=mexc_futures_price,
        spot_url=spot_url,
        futures_url=futures_url,
        deposit_enabled=deposit_enabled,
        withdrawal_enabled=withdrawal_enabled,
        dex_url=dex_url,
    )
    db.add(signal)
    await db.commit()
    await db.refresh(signal)

    # Prepare signal data for notifications
    signal_data = {
        "id": signal.id,
        "coin_name": signal.coin_name,
        "position": signal.position,
        "spread": float(signal.spread) if signal.spread else None,
        "mexc_spot_price": float(signal.mexc_spot_price) if signal.mexc_spot_price else None,
        "mexc_futures_price": float(signal.mexc_futures_price) if signal.mexc_futures_price else None,
        "created_at": signal.created_at.isoformat() if signal.created_at else None,
    }

    # Broadcast to WebSocket clients
    await broadcast_new_signal("mexc_spot_futures", signal_data)

    # Send notifications to users
    await notification_service.notify_users_about_signal(
        db, "mexc_spot_futures", signal.id, signal_data
    )

    return signal


async def create_funding_rate_signal(
    db: AsyncSession,
    coin_name: str,
    hourly_profit: Optional[Decimal] = None,
    **kwargs,
) -> SignalFundingRate:
    """Create a new Funding Rate signal."""
    signal = SignalFundingRate(coin_name=coin_name, hourly_profit=hourly_profit, **kwargs)
    db.add(signal)
    await db.commit()
    await db.refresh(signal)

    # Prepare signal data for notifications
    signal_data = {
        "id": signal.id,
        "coin_name": signal.coin_name,
        "hourly_profit": float(signal.hourly_profit) if signal.hourly_profit else None,
        "created_at": signal.created_at.isoformat() if signal.created_at else None,
    }

    # Broadcast to WebSocket clients
    await broadcast_new_signal("funding_rate", signal_data)

    # Send notifications to users
    await notification_service.notify_users_about_signal(
        db, "funding_rate", signal.id, signal_data
    )

    return signal


async def create_mexc_dex_signal(
    db: AsyncSession,
    coin_name: str,
    spread_percent: Optional[Decimal] = None,
    mexc_price: Optional[Decimal] = None,
    dex_price: Optional[Decimal] = None,
    **kwargs,
) -> SignalMEXCDEX:
    """Create a new MEXC & DEX signal."""
    signal = SignalMEXCDEX(
        coin_name=coin_name,
        spread_percent=spread_percent,
        mexc_price=mexc_price,
        dex_price=dex_price,
        **kwargs,
    )
    db.add(signal)
    await db.commit()
    await db.refresh(signal)

    # Prepare signal data for notifications
    signal_data = {
        "id": signal.id,
        "coin_name": signal.coin_name,
        "spread_percent": float(signal.spread_percent) if signal.spread_percent else None,
        "mexc_price": float(signal.mexc_price) if signal.mexc_price else None,
        "dex_price": float(signal.dex_price) if signal.dex_price else None,
        "created_at": signal.created_at.isoformat() if signal.created_at else None,
    }

    # Broadcast to WebSocket clients
    await broadcast_new_signal("mexc_dex", signal_data)

    # Send notifications to users
    await notification_service.notify_users_about_signal(
        db, "mexc_dex", signal.id, signal_data
    )

    return signal

