"""Market Data Service schemas."""
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel


class CryptocurrencyResponse(BaseModel):
    """Cryptocurrency response schema."""

    id: int
    name: str
    symbol: str
    rank: int
    price_usd: Decimal
    change_24h: Decimal
    change_7d: Decimal
    market_cap_usd: Decimal
    volume_24h_usd: Decimal
    market_cap_dominance: Decimal

    class Config:
        from_attributes = True


class CryptocurrencyListResponse(BaseModel):
    """Cryptocurrency list response schema."""

    data: list[CryptocurrencyResponse]
    pagination: dict


class GlobalMarketDataResponse(BaseModel):
    """Global market data response schema."""

    total_market_cap: Decimal
    total_volume_24h: Decimal
    bitcoin_dominance: Decimal
    ethereum_dominance: Decimal
    active_cryptocurrencies: int



