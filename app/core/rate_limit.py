from fastapi import HTTPException, status
from redis import Redis
from datetime import datetime
from app.core.config import MAX_DOWNLOADS_PER_DAY, RATE_LIMIT_EXPIRY, REDIS_URL

# Ensure Redis client is initialized only once
redis_client = Redis.from_url(REDIS_URL)

async def check_rate_limit(ip: str):
    """
    Enforces a rate limit of MAX_DOWNLOADS_PER_DAY per IP.
    Increments the counter in Redis and sets expiry if it's the first request today.
    """
    date_key = datetime.utcnow().strftime("%Y-%m-%d")
    redis_key = f"downloads:{ip}:{date_key}"

    # Get count from Redis (as bytes), decode it, and convert to int
    count_bytes = redis_client.get(redis_key)
    count = int(count_bytes.decode()) if count_bytes else 0

    # Convert MAX_DOWNLOADS_PER_DAY to int in case it's a string (from .env)
    max_limit = int(MAX_DOWNLOADS_PER_DAY)

    if count >= max_limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Download limit reached for today. Max {max_limit} per IP."
        )

    # Increment and set expiry if this is the first download today
    new_count = redis_client.incr(redis_key)
    if new_count == 1:
        redis_client.expire(redis_key, int(RATE_LIMIT_EXPIRY))
