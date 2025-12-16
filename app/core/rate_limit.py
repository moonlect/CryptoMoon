"""Rate limiting middleware."""
from typing import Callable
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from app.core.redis_client import get_redis
from app.core.config import settings
from app.core.logging_config import get_logger

logger = get_logger(__name__)


async def get_rate_limit_key(request: Request) -> tuple[str, int]:
    """Get rate limit key and limit based on user subscription."""
    # Simplified version: use IP for anonymous, token for authenticated
    # For MVP, we'll use a simple approach
    auth_header = request.headers.get("Authorization")
    
    if auth_header and auth_header.startswith("Bearer "):
        # Authenticated user - use token hash as key
        token = auth_header.split(" ")[1]
        # Use first 16 chars of token as identifier
        token_id = token[:16] if len(token) > 16 else token
        key = f"rate_limit:token:{token_id}:{request.url.path}"
        # Default to free plan limit (can be enhanced later)
        limit = settings.rate_limit_free
    else:
        # Anonymous user - use IP
        client_ip = request.client.host if request.client else "unknown"
        key = f"rate_limit:ip:{client_ip}:{request.url.path}"
        limit = settings.rate_limit_anonymous

    return key, limit


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Check rate limit before processing request."""
        # Skip rate limiting for health check and docs
        if request.url.path in ["/health", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        try:
            redis = await get_redis()
            key, limit = await get_rate_limit_key(request)

            # Check current count
            current = await redis.get(key)
            if current and int(current) >= limit:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Rate limit exceeded: {limit} requests per hour",
                    headers={"Retry-After": "3600"},
                )

            # Increment counter
            await redis.incr(key)
            await redis.expire(key, 3600)  # 1 hour TTL
        except HTTPException:
            # Re-raise HTTP exceptions (rate limit exceeded)
            raise
        except Exception as e:
            # If Redis is unavailable or any other error occurs,
            # log the error but allow the request to proceed
            logger.warning(f"Rate limiting error: {e}. Allowing request to proceed.")
        
        response = await call_next(request)
        return response

