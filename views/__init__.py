from fastapi import APIRouter

from .user import user_router
from .redis import redis_router

views_router = APIRouter()
views_router.include_router(redis_router)
views_router.include_router(user_router)