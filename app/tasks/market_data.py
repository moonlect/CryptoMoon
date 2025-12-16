"""Market data background tasks."""
from app.services.market.service import MarketDataService
from app.core.database import AsyncSessionLocal

market_service = MarketDataService()


async def sync_coinmarketcap_task():
    """Background task to sync CoinMarketCap data."""
    async with AsyncSessionLocal() as db:
        try:
            count = await market_service.sync_coinmarketcap_data(db)
            print(f"Synced {count} cryptocurrencies from CoinMarketCap")
        except Exception as e:
            print(f"Error syncing CoinMarketCap data: {e}")



