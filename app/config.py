from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Typed env config, same pattern as the sibling TypeScript services' env.ts."""

    squad_api_shared_secret: str
    """Checked against the caller's `x-api-key` header on every /api/v2/* route."""

    upstash_redis_rest_url: Optional[str] = None
    upstash_redis_rest_token: Optional[str] = None
    """Enables rate limiting. Unset: rate limiting is skipped (fail-open) - the shared secret
    above is the primary defense, this is a secondary layer."""


settings = Settings()
