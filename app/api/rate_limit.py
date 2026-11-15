import logging

from fastapi import Header, HTTPException
from upstash_ratelimit import Ratelimit, SlidingWindow
from upstash_redis import Redis

from app.config import settings

logger = logging.getLogger("uvicorn.error")

_limiter = None
if settings.upstash_redis_rest_url and settings.upstash_redis_rest_token:
    _limiter = Ratelimit(
        redis=Redis(url=settings.upstash_redis_rest_url, token=settings.upstash_redis_rest_token),
        limiter=SlidingWindow(max_requests=60, window=60),
        prefix="squad-forge",
    )

_warned = False


async def rate_limit(x_api_key: str = Header(default="")) -> None:
    """FastAPI dependency: 429s a caller over budget. Persistent across cold starts (Upstash
    Redis), unlike an in-memory counter. Fails open with a logged warning when Upstash isn't
    configured - the x-api-key check (require_api_key) is the primary defense, this is secondary."""
    global _warned
    if _limiter is None:
        if not _warned:
            logger.warning("UPSTASH_REDIS_REST_URL/TOKEN not set: rate limiting is disabled (fail-open)")
            _warned = True
        return
    response = _limiter.limit(x_api_key or "anonymous")
    if not response.allowed:
        raise HTTPException(status_code=429, detail="Too many requests")
