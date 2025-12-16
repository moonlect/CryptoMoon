"""Signals Service schemas."""
from decimal import Decimal
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class MEXCSpotFuturesSignalResponse(BaseModel):
    """MEXC Spot & Futures signal response schema."""

    id: int
    coin_name: str
    position: Optional[str] = None
    spread: Optional[Decimal] = None
    mexc_spot_price: Optional[Decimal] = None
    mexc_futures_price: Optional[Decimal] = None
    spot_url: Optional[str] = None
    futures_url: Optional[str] = None
    deposit_enabled: bool = True
    withdrawal_enabled: bool = True
    dex_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class FundingRateSignalResponse(BaseModel):
    """Funding Rate Spread signal response schema."""

    id: int
    coin_name: str
    hourly_profit: Optional[Decimal] = None
    gate_rate: Optional[Decimal] = None
    gate_url: Optional[str] = None
    gate_interval: Optional[str] = None
    gate_position: Optional[str] = None
    binance_rate: Optional[Decimal] = None
    binance_url: Optional[str] = None
    binance_interval: Optional[str] = None
    binance_position: Optional[str] = None
    mexc_rate: Optional[Decimal] = None
    mexc_url: Optional[str] = None
    mexc_interval: Optional[str] = None
    mexc_position: Optional[str] = None
    ourbit_rate: Optional[Decimal] = None
    ourbit_url: Optional[str] = None
    ourbit_interval: Optional[str] = None
    ourbit_position: Optional[str] = None
    bitget_rate: Optional[Decimal] = None
    bitget_url: Optional[str] = None
    bitget_interval: Optional[str] = None
    bitget_position: Optional[str] = None
    bybit_rate: Optional[Decimal] = None
    bybit_url: Optional[str] = None
    bybit_interval: Optional[str] = None
    bybit_position: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class MEXCDEXSignalResponse(BaseModel):
    """MEXC & DEX Price Spread signal response schema."""

    id: int
    coin_name: str
    spread_percent: Optional[Decimal] = None
    mexc_price: Optional[Decimal] = None
    mexc_url: Optional[str] = None
    dex_price: Optional[Decimal] = None
    dexscreener_url: Optional[str] = None
    max_size_usd: Optional[Decimal] = None
    deposit_enabled: bool = True
    withdrawal_enabled: bool = True
    deposit_url: Optional[str] = None
    withdrawal_url: Optional[str] = None
    token_contract: Optional[str] = None
    token_chain: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class SignalListResponse(BaseModel):
    """Signal list response schema."""

    data: list
    pagination: dict



