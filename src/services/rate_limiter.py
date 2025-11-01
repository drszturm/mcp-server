import asyncio
from typing import Optional
import time
import redis.asyncio as redis
from src.config.settings import settings


class RateLimiter:
    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
        self.requests_per_minute = settings.RATE_LIMIT_REQUESTS_PER_MINUTE

    async def init_redis(self):
        if settings.REDIS_URL:
            self.redis_client = redis.from_url(settings.REDIS_URL)
        else:
            # Fallback to in-memory rate limiting
            self.redis_client = None
            self._local_requests = []

    async def is_rate_limited(self, identifier: str) -> bool:
        if self.redis_client:
            # Redis-based rate limiting
            key = f"rate_limit:{identifier}"
            current = await self.redis_client.get(key)

            if current and int(current) >= self.requests_per_minute:
                return True

            async with self.redis_client.pipeline() as pipe:
                pipe.incr(key, 1)
                pipe.expire(key, 60)
                results = await pipe.execute()

            return False
        else:
            # In-memory rate limiting
            now = time.time()
            self._local_requests = [
                req_time for req_time in self._local_requests if now - req_time < 60
            ]

            if len(self._local_requests) >= self.requests_per_minute:
                return True

            self._local_requests.append(now)
            return False


rate_limiter = RateLimiter()
