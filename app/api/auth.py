import hmac

from fastapi import Header, HTTPException

from app.config import settings


async def require_api_key(x_api_key: str = Header(default="")) -> None:
    """FastAPI dependency: 401s any request without a valid `x-api-key`. `hmac.compare_digest`
    is constant-time and safe for unequal-length inputs, so no pre-hashing is needed."""
    if not hmac.compare_digest(x_api_key, settings.squad_api_shared_secret):
        raise HTTPException(status_code=401, detail="Unauthorized")
