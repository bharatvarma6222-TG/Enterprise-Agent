from app.cache.redis_client import get_redis

r = get_redis()

r.set("status", "alive")

print(r.get("status"))
