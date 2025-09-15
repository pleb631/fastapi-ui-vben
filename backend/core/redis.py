import redis.asyncio as redis
from config import settings

redis_client: redis.Redis | None = None


async def close_redis():
    global redis_client
    print("close redis")
    if redis_client:
        await redis_client.close()


def get_redis():
    return redis_client


async def init_redis(max_connections: int = 20):
    global redis_client
    print("load redis")
    redis_client = await redis.from_url(
        settings.REDIS_URL,
        encoding="utf-8",
        decode_responses=True,
        max_connections=max_connections,
    )
