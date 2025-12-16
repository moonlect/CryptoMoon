"""Background task scheduler."""
import asyncio
from datetime import datetime, timedelta
from app.tasks.market_data import sync_coinmarketcap_task
from app.core.config import settings


async def run_periodic_tasks():
    """Run periodic background tasks."""
    while True:
        try:
            # Sync CoinMarketCap data every 5 minutes
            await sync_coinmarketcap_task()
            print(f"CoinMarketCap sync completed at {datetime.utcnow()}")
        except Exception as e:
            print(f"Error in periodic task: {e}")

        # Wait 5 minutes before next sync
        await asyncio.sleep(300)  # 5 minutes


async def start_background_tasks():
    """Start all background tasks."""
    # Start periodic tasks in background
    task = asyncio.create_task(run_periodic_tasks())
    return task


async def stop_background_tasks(task):
    """Stop background tasks."""
    if task:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass



