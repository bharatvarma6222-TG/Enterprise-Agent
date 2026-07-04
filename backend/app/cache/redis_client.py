import redis
from app.core.config import settings

redis_client = None

if settings.REDIS_URL:
    redis_client = redis.from_url(
        settings.REDIS_URL,
        decode_responses=True,
        ssl_cert_reqs=None,
    )


def get_redis():
    if redis_client is None:
        raise RuntimeError(
            "REDIS_URL is not configured."
        )
    return redis_client
