"""Signals Service API routes."""
from typing import Optional
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, delete
from datetime import datetime
from app.core.database import get_db
from app.core.dependencies import require_vip
from app.models.user import User
from app.models.signal import (
    SignalMEXCSpotFutures,
    SignalFundingRate,
    SignalMEXCDEX,
)
from app.schemas.signal import (
    MEXCSpotFuturesSignalResponse,
    FundingRateSignalResponse,
    MEXCDEXSignalResponse,
    SignalListResponse,
)

router = APIRouter(prefix="/api/v1/signals", tags=["signals"])


@router.get("/mexc-spot-futures", response_model=SignalListResponse)
async def get_mexc_spot_futures_signals(
    limit: int = Query(30, ge=1, le=100),
    offset: int = Query(0, ge=0),
    min_spread: Optional[float] = Query(None, ge=0),
    position: Optional[str] = Query(None, regex="^(LONG|SHORT|ALL)$"),
    search: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_vip),
):
    """Get MEXC Spot & Futures signals (VIP only)."""
    query = select(SignalMEXCSpotFutures)

    if min_spread is not None:
        query = query.where(SignalMEXCSpotFutures.spread >= Decimal(str(min_spread)))

    if position and position != "ALL":
        query = query.where(SignalMEXCSpotFutures.position == position)

    if search:
        search_lower = search.lower()
        query = query.where(SignalMEXCSpotFutures.coin_name.ilike(f"%{search_lower}%"))

    # Sort by created_at DESC (newest first)
    query = query.order_by(desc(SignalMEXCSpotFutures.created_at))

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # Pagination
    query = query.offset(offset).limit(limit)

    result = await db.execute(query)
    items = result.scalars().all()

    return SignalListResponse(
        data=[
            MEXCSpotFuturesSignalResponse(
                id=item.id,
                coin_name=item.coin_name,
                position=item.position,
                spread=item.spread,
                mexc_spot_price=item.mexc_spot_price,
                mexc_futures_price=item.mexc_futures_price,
                spot_url=item.spot_url,
                futures_url=item.futures_url,
                deposit_enabled=item.deposit_enabled,
                withdrawal_enabled=item.withdrawal_enabled,
                dex_url=item.dex_url,
                created_at=item.created_at,
            )
            for item in items
        ],
        pagination={"total": total, "limit": limit, "offset": offset},
    )


@router.get("/funding-rate", response_model=SignalListResponse)
async def get_funding_rate_signals(
    limit: int = Query(30, ge=1, le=100),
    offset: int = Query(0, ge=0),
    min_profit: Optional[float] = Query(None, ge=0),
    search: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_vip),
):
    """Get Funding Rate Spread signals (VIP only)."""
    query = select(SignalFundingRate)

    if min_profit is not None:
        query = query.where(
            SignalFundingRate.hourly_profit >= Decimal(str(min_profit))
        )

    if search:
        search_lower = search.lower()
        query = query.where(SignalFundingRate.coin_name.ilike(f"%{search_lower}%"))

    # Sort by created_at DESC (newest first)
    query = query.order_by(desc(SignalFundingRate.created_at))

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # Pagination
    query = query.offset(offset).limit(limit)

    result = await db.execute(query)
    items = result.scalars().all()

    return SignalListResponse(
        data=[
            FundingRateSignalResponse(
                id=item.id,
                coin_name=item.coin_name,
                hourly_profit=item.hourly_profit,
                gate_rate=item.gate_rate,
                gate_url=item.gate_url,
                gate_interval=item.gate_interval,
                binance_rate=item.binance_rate,
                binance_url=item.binance_url,
                binance_interval=item.binance_interval,
                mexc_rate=item.mexc_rate,
                mexc_url=item.mexc_url,
                mexc_interval=item.mexc_interval,
                ourbit_rate=item.ourbit_rate,
                ourbit_url=item.ourbit_url,
                ourbit_interval=item.ourbit_interval,
                bitget_rate=item.bitget_rate,
                bitget_url=item.bitget_url,
                bitget_interval=item.bitget_interval,
                bitget_position=item.bitget_position,
                bybit_rate=item.bybit_rate,
                bybit_url=item.bybit_url,
                bybit_interval=item.bybit_interval,
                bybit_position=item.bybit_position,
                created_at=item.created_at,
            )
            for item in items
        ],
        pagination={"total": total, "limit": limit, "offset": offset},
    )


@router.get("/mexc-dex", response_model=SignalListResponse)
async def get_mexc_dex_signals(
    limit: int = Query(30, ge=1, le=100),
    offset: int = Query(0, ge=0),
    min_spread: Optional[float] = Query(None, ge=0),
    search: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_vip),
):
    """Get MEXC & DEX Price Spread signals (VIP only)."""
    query = select(SignalMEXCDEX)

    if min_spread is not None:
        query = query.where(
            SignalMEXCDEX.spread_percent >= Decimal(str(min_spread))
        )

    if search:
        search_lower = search.lower()
        query = query.where(SignalMEXCDEX.coin_name.ilike(f"%{search_lower}%"))

    # Sort by created_at DESC (newest first)
    query = query.order_by(desc(SignalMEXCDEX.created_at))

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # Pagination
    query = query.offset(offset).limit(limit)

    result = await db.execute(query)
    items = result.scalars().all()

    return SignalListResponse(
        data=[
            MEXCDEXSignalResponse(
                id=item.id,
                coin_name=item.coin_name,
                spread_percent=item.spread_percent,
                mexc_price=item.mexc_price,
                mexc_url=item.mexc_url,
                dex_price=item.dex_price,
                dexscreener_url=item.dexscreener_url,
                max_size_usd=item.max_size_usd,
                deposit_enabled=item.deposit_enabled,
                withdrawal_enabled=item.withdrawal_enabled,
                deposit_url=item.deposit_url,
                withdrawal_url=item.withdrawal_url,
                token_contract=item.token_contract,
                token_chain=item.token_chain,
                created_at=item.created_at,
            )
            for item in items
        ],
        pagination={"total": total, "limit": limit, "offset": offset},
    )


@router.delete("/{signal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_signal(
    signal_id: int,
    signal_type: str = Query(..., regex="^(mexc_spot_futures|funding_rate|mexc_dex)$"),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_vip),
):
    """Delete a signal (VIP only)."""
    # Map signal types to models
    model_map = {
        "mexc_spot_futures": SignalMEXCSpotFutures,
        "funding_rate": SignalFundingRate,
        "mexc_dex": SignalMEXCDEX,
    }

    model = model_map.get(signal_type)
    if not model:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid signal type",
        )

    result = await db.execute(select(model).where(model.id == signal_id))
    signal = result.scalar_one_or_none()

    if not signal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Signal not found",
        )

    # Delete the signal (SQLAlchemy 2.0 async)
    await db.execute(delete(model).where(model.id == signal_id))
    await db.commit()

