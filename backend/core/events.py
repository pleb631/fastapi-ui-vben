from fastapi import FastAPI

from core.redis import init_redis, close_redis
async def startup(app: FastAPI):
    print("启动")
    await init_redis()


async def stopping(app: FastAPI):
    print("停止")
    await close_redis()
