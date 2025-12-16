"""Market Data Service API routes."""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.market import CryptocurrencyListResponse, CryptocurrencyResponse
from app.services.market.service import MarketDataService

router = APIRouter(prefix="/api/v1/market", tags=["market"])

market_service = MarketDataService()


@router.get("/cryptocurrencies", response_model=CryptocurrencyListResponse)
async def get_cryptocurrencies(
    limit: int = Query(50, ge=1, le=100, description="Number of items per page"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    sort: str = Query("rank", description="Sort field"),
    order: str = Query("asc", regex="^(asc|desc)$", description="Sort order"),
    search: Optional[str] = Query(None, description="Search by name or symbol"),
    db: AsyncSession = Depends(get_db),
    user: Optional[User] = Depends(get_current_user),  # Optional for free users
):
    """Get list of cryptocurrencies."""
    items, total = await market_service.get_cryptocurrencies(
        db=db, limit=limit, offset=offset, sort=sort, order=order, search=search
    )

    return CryptocurrencyListResponse(
        data=[
            CryptocurrencyResponse(
                id=item.crypto_id,
                name=item.name,
                symbol=item.symbol,
                rank=item.rank,
                price_usd=item.price_usd,
                change_24h=item.change_24h,
                change_7d=item.change_7d,
                market_cap_usd=item.market_cap_usd,
                volume_24h_usd=item.volume_24h_usd,
                market_cap_dominance=item.market_cap_dominance,
            )
            for item in items
        ],
        pagination={"total": total, "limit": limit, "offset": offset},
    )


@router.get("/cryptocurrencies/{crypto_id}", response_model=CryptocurrencyResponse)
async def get_cryptocurrency(
    crypto_id: int,
    db: AsyncSession = Depends(get_db),
    user: Optional[User] = Depends(get_current_user),
):
    """Get cryptocurrency by ID."""
    from sqlalchemy import select
    from app.models.signal import CoinMarketCapData
    from datetime import datetime
    from fastapi import HTTPException, status

    result = await db.execute(
        select(CoinMarketCapData).where(
            CoinMarketCapData.crypto_id == crypto_id,
            CoinMarketCapData.expires_at > datetime.utcnow(),
        )
    )
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cryptocurrency not found",
        )

    return CryptocurrencyResponse(
        id=item.crypto_id,
        name=item.name,
        symbol=item.symbol,
        rank=item.rank,
        price_usd=item.price_usd,
        change_24h=item.change_24h,
        change_7d=item.change_7d,
        market_cap_usd=item.market_cap_usd,
        volume_24h_usd=item.volume_24h_usd,
        market_cap_dominance=item.market_cap_dominance,
    )



