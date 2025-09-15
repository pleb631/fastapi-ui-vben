import hashlib
import uuid
import json
import functools
from typing import Callable, Any
from core.redis import redis_client
from passlib.handlers.pbkdf2 import pbkdf2_sha256
def random_str():
    only = hashlib.md5(str(uuid.uuid1()).encode(encoding='UTF-8')).hexdigest()
    return str(only)

def cacheable(ttl: int = 3600, key_prefix: str = "cache"):
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


def en_password(psw: str):

    password = pbkdf2_sha256.hash(psw)
    return password


def check_password(password: str, old: str):

    check = pbkdf2_sha256.verify(password, old)
    if check:
        return True
    else:
        return False
