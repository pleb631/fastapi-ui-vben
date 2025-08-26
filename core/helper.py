import hashlib
import uuid
import json
import functools
from typing import Callable, Any
from core.redis import redis_client

def random_str():
    only = hashlib.md5(str(uuid.uuid1()).encode(encoding='UTF-8')).hexdigest()
    return str(only)

def cacheable(ttl: int = 3600, key_prefix: str = "cache"):
    """
    Redis 缓存装饰器
    :param ttl: 缓存过期时间（秒）
    :param key_prefix: 缓存 key 前缀
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            key = f"{key_prefix}:{func.__name__}:{args}:{kwargs}"

            cached = await redis_client.get(key)
            if cached:
                return json.loads(cached)

            result = await func(*args, **kwargs)

            if result is not None:
                await redis_client.set(key, json.dumps(result, default=str), ex=ttl)

            return result
        return wrapper
    return decorator