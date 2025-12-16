"""Signal models."""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric, func
from app.core.database import Base


class SignalMEXCSpotFutures(Base):
    """MEXC Spot & Futures signal model."""

    __tablename__ = "signals_mexc_spot_futures"

    id = Column(Integer, primary_key=True, index=True)
    coin_name = Column(String(100), nullable=False, index=True)
    position = Column(String(10))  # 'LONG', 'SHORT'
    spread = Column(Numeric(10, 2))
    mexc_spot_price = Column(Numeric(20, 8))
    mexc_futures_price = Column(Numeric(20, 8))
    spot_url = Column(String(500))
    futures_url = Column(String(500))
    deposit_enabled = Column(Boolean, default=True)
    withdrawal_enabled = Column(Boolean, default=True)
    dex_url = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class SignalFundingRate(Base):
    """Funding Rate Spread signal model."""

    __tablename__ = "signals_funding_rate"

    id = Column(Integer, primary_key=True, index=True)
    coin_name = Column(String(100), nullable=False, index=True)
    hourly_profit = Column(Numeric(10, 4))

    # Exchange rates with URLs
    gate_rate = Column(Numeric(10, 4))
    gate_url = Column(String(500))
    gate_interval = Column(String(10))

    binance_rate = Column(Numeric(10, 4))
    binance_url = Column(String(500))
    binance_interval = Column(String(10))

    mexc_rate = Column(Numeric(10, 4))
    mexc_url = Column(String(500))
    mexc_interval = Column(String(10))

    ourbit_rate = Column(Numeric(10, 4))
    ourbit_url = Column(String(500))
    ourbit_interval = Column(String(10))

    bitget_rate = Column(Numeric(10, 4))
    bitget_url = Column(String(500))
    bitget_interval = Column(String(10))
    bitget_position = Column(String(10))  # 'LONG', 'SHORT'

    bybit_rate = Column(Numeric(10, 4))
    bybit_url = Column(String(500))
    bybit_interval = Column(String(10))
    bybit_position = Column(String(10))

    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class SignalMEXCDEX(Base):
    """MEXC & DEX Price Spread signal model."""

    __tablename__ = "signals_mexc_dex"

    id = Column(Integer, primary_key=True, index=True)
    coin_name = Column(String(100), nullable=False, index=True)
    spread_percent = Column(Numeric(10, 2))

    mexc_price = Column(Numeric(20, 8))
    mexc_url = Column(String(500))

    dex_price = Column(Numeric(20, 8))
    dexscreener_url = Column(String(500))

    max_size_usd = Column(Numeric(15, 2))
    deposit_enabled = Column(Boolean, default=True)
    withdrawal_enabled = Column(Boolean, default=True)

    deposit_url = Column(String(500))
    withdrawal_url = Column(String(500))

    token_contract = Column(String(100))
    token_chain = Column(String(50))  # 'ETH', 'BSC', etc.

    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Notification(Base):
    """Notification model."""

    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    signal_type = Column(String(50))  # 'mexc_spot_futures', 'funding_rate', 'mexc_dex'
    signal_id = Column(Integer)
    title = Column(String(255))
    body = Column(String)
    is_read = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    read_at = Column(DateTime(timezone=True), nullable=True)


class CoinMarketCapData(Base):
    """CoinMarketCap data cache model."""

    __tablename__ = "coinmarketcap_data"

    id = Column(Integer, primary_key=True, index=True)
    crypto_id = Column(Integer, unique=True, nullable=False)
    name = Column(String(100))
    symbol = Column(String(20), index=True)
    rank = Column(Integer)
    price_usd = Column(Numeric(20, 8))
    change_24h = Column(Numeric(10, 4))
    change_7d = Column(Numeric(10, 4))
    market_cap_usd = Column(Numeric(20, 2))
    volume_24h_usd = Column(Numeric(20, 2))
    market_cap_dominance = Column(Numeric(10, 4))
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), index=True)


class AuditLog(Base):
    """Audit log model."""

    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=True)
    action = Column(String(100))
    resource_type = Column(String(50))
    resource_id = Column(String(100))
    old_values = Column(String)  # JSONB in PostgreSQL
    new_values = Column(String)  # JSONB in PostgreSQL
    ip_address = Column(String(50))
    user_agent = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)



