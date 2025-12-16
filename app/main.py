"""Main FastAPI application."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.redis_client import get_redis, close_redis
from app.core.exceptions import setup_exception_handlers
from app.core.rate_limit import RateLimitMiddleware
from app.core.logging_config import setup_logging, get_logger
from app.services.auth.router import router as auth_router
from app.services.user.router import router as user_router
from app.services.market.router import router as market_router
from app.services.signals.router import router as signals_router
from app.services.websocket.router import router as websocket_router
from app.services.notifications.router import router as notifications_router

# Setup logging
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events."""
    import asyncio
    
    logger.info("Starting CryptoTracker application")
    
    # Startup
    try:
        await get_redis()
        logger.info("Redis connection established")
    except Exception as e:
        logger.warning(f"Failed to connect to Redis: {e}. Application will continue without rate limiting.")
    
    # Start Telegram bot in background
    from app.services.telegram.bot import start_telegram_bot
    telegram_task = asyncio.create_task(start_telegram_bot())
    logger.info("Telegram bot task started")
    
    # Start background tasks (CoinMarketCap sync)
    from app.tasks.scheduler import start_background_tasks, stop_background_tasks
    background_task = await start_background_tasks()
    logger.info("Background tasks started")
    
    yield
    
    # Shutdown
    logger.info("Shutting down CryptoTracker application")
    
    from app.services.telegram.bot import stop_telegram_bot
    await stop_telegram_bot()
    telegram_task.cancel()
    try:
        await telegram_task
    except asyncio.CancelledError:
        pass
    logger.info("Telegram bot stopped")
    
    await stop_background_tasks(background_task)
    logger.info("Background tasks stopped")
    
    await close_redis()
    logger.info("Redis connection closed")

app = FastAPI(
    title="CryptoTracker API",
    description="Веб-платформа криптоаналитики",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Setup exception handlers
setup_exception_handlers(app)

# Rate limiting middleware (before CORS)
app.add_middleware(RateLimitMiddleware)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(market_router)
app.include_router(signals_router)
app.include_router(websocket_router)
app.include_router(notifications_router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "CryptoTracker API",
        "version": "0.1.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

