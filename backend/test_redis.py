import redis
from app.core.config import settings

print(settings.REDIS_URL)

try:
    client = redis.from_url(
        settings.REDIS_URL,
        decode_responses=True,
        ssl_cert_reqs=None,
    )

    print(client.ping())

except Exception as e:
    print(type(e).__name__)
    print(e)
    