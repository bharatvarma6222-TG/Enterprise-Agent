import json

from app.cache.redis_client import get_redis

redis_client = get_redis()

MEMORY_LIMIT = 10


def add_message(session_id: str, role: str, content: str):

    key = f"chat:{session_id}"

    redis_client.rpush(
        key,
        json.dumps(
            {
                "role": role,
                "content": content
            }
        )
    )

    redis_client.ltrim(
        key,
        -MEMORY_LIMIT,
        -1
    )


def get_messages(session_id: str):

    key = f"chat:{session_id}"

    messages = redis_client.lrange(
        key,
        0,
        -1
    )

    return [
        json.loads(m)
        for m in messages
    ]
