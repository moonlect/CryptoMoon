"""Market Data Service business logic."""
import aiohttp
from typing import List, Optional
from decimal import Decimal
from app.core.config import settings
from app.models.signal import CoinMarketCapData
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta


class MarketDataService:
    """Service for fetching and caching market data."""

    BASE_URL = "https://pro-api.coinmarketcap.com/v1"

    async def fetch_from_coinmarketcap(
        self, limit: int = 100
    ) -> Optional[List[dict]]:
        """Fetch cryptocurrency data from CoinMarketCap API."""
        if not settings.coinmarketcap_api_key:
            return None

        url = f"{self.BASE_URL}/cryptocurrency/listings/latest"
        headers = {
            "X-CMC_PRO_API_KEY": settings.coinmarketcap_api_key,
            "Accept": "application/json",
        }
        params = {
            "start": 1,
            "limit": limit,
            "convert": "USD",
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("data", [])
                    else:
                        return None
        except Exception:
            return None

    async def sync_coinmarketcap_data(self, db: AsyncSession) -> int:
        """Sync CoinMarketCap data to database."""
        data = await self.fetch_from_coinmarketcap(limit=100)
        if not data:
            return 0

        count = 0
        expires_at = datetime.utcnow() + timedelta(minutes=5)

        for item in data:
            quote = item.get("quote", {}).get("USD", {})
            crypto_id = item.get("id")
            if not crypto_id:
                continue

            # Check if exists
            result = await db.execute(
                select(CoinMarketCapData).where(
                    CoinMarketCapData.crypto_id == crypto_id
                )
            )
            existing = result.scalar_one_or_none()

            data_dict = {
                "crypto_id": crypto_id,
                "name": item.get("name"),
                "symbol": item.get("symbol"),
                "rank": item.get("cmc_rank"),
                "price_usd": Decimal(str(quote.get("price", 0))),
                "change_24h": Decimal(str(quote.get("percent_change_24h", 0))),
                "change_7d": Decimal(str(quote.get("percent_change_7d", 0))),
                "market_cap_usd": Decimal(str(quote.get("market_cap", 0))),
                "volume_24h_usd": Decimal(str(quote.get("volume_24h", 0))),
                "market_cap_dominance": Decimal(
                    str(quote.get("market_cap_dominance", 0))
                ),
                "expires_at": expires_at,
            }

            if existing:
                for key, value in data_dict.items():
                    setattr(existing, key, value)
            else:
                new_data = CoinMarketCapData(**data_dict)
                db.add(new_data)
            count += 1

        await db.commit()
        return count

    async def get_cryptocurrencies(
        self,
        db: AsyncSession,
        limit: int = 50,
        offset: int = 0,
        sort: str = "rank",
        order: str = "asc",
        search: Optional[str] = None,
    ) -> tuple[List[CoinMarketCapData], int]:
        """Get cryptocurrencies from database."""
        query = select(CoinMarketCapData).where(
            CoinMarketCapData.expires_at > datetime.utcnow()
        )

        if search:
            search_lower = search.lower()
            query = query.where(
                (CoinMarketCapData.name.ilike(f"%{search_lower}%"))
                | (CoinMarketCapData.symbol.ilike(f"%{search_lower}%"))
            )

        # Sorting
        sort_column = getattr(CoinMarketCapData, sort, CoinMarketCapData.rank)
        if order == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())

        # Count total
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar() or 0

        # Pagination
        query = query.offset(offset).limit(limit)

        result = await db.execute(query)
        items = result.scalars().all()

        return list(items), total



