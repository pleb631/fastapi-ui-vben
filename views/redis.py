from fastapi import APIRouter, Request, Depends
from starlette.responses import HTMLResponse, JSONResponse
import redis.asyncio as redis


from core.redis import get_redis


redis_router = APIRouter()


@redis_router.get("/redis", response_class=HTMLResponse)
async def redis_page(req: Request):
    return req.app.state.views.TemplateResponse("test_redis.html", {"request": req})


@redis_router.get("/redis/get/{key}", response_class=JSONResponse)
async def redis_get(key: str, redis: redis.Redis = Depends(get_redis)):
    value = await redis.get(key)
    print("get data", value)
    return {"key": key, "value": value}


@redis_router.post("/redis/set", response_class=HTMLResponse)
async def redis_set(req: Request, redis: redis.Redis = Depends(get_redis)):
    data = await req.json()
    key = data.get("key")
    value = data.get("value")
    await redis.set(key, value)
    return "ok"
