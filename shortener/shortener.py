from typing import Optional

import structlog
from aioredis import Redis

from .clients.s3 import S3Client
from .settings import KEY_COUNTER, KEY_URL_ID, REDIRECT_BASE_URL, URL_CACHE_SECONDS
from .url_id import generate_url_id

LOG = structlog.get_logger(__name__)


class Shortener:
    def __init__(self, redis: Redis, s3: S3Client) -> None:
        print("created shortener")
        self.redis = redis
        self.s3 = s3

    async def shorten(self, long_url: str) -> str:
        url_id = await self._compute_url_id()
        LOG.info("shorten.computed_id", url_id=url_id)
        await self.s3.save_url(url_id=url_id, long_url=long_url)
        LOG.info("shorten.saved_url", url_id=url_id)
        short_url = f"{REDIRECT_BASE_URL}/{url_id}"
        return short_url

    async def _compute_url_id(self) -> str:
        counter = await self.redis.incr(KEY_COUNTER)
        return generate_url_id(counter)

    async def get_long_url(self, short_url: str) -> Optional[str]:
        url_id = short_url.replace(f"{REDIRECT_BASE_URL}/", "")
        url_redis_key = f"{KEY_URL_ID}:{url_id}"
        long_url = await self.redis.get(url_redis_key)
        if long_url:
            LOG.info("get_long_url.from_redis", url_id=url_id)
            return long_url
        long_url = await self.s3.get_url(url_id)
        if long_url:
            await self.redis.set(url_redis_key, long_url, expire=URL_CACHE_SECONDS)
            LOG.info("get_long_url.from_s3", url_id=url_id)
            return long_url
        LOG.warning("get_long_url.not_found", url_id=url_id)
        return None
