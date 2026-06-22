import redis
from app.core.config import settings

redis_client = redis.from_url(
    settings.REDIS_URL,
    decode_responses=True,
    ssl_cert_reqs=None
)


def get_redis():
    return redis_client
