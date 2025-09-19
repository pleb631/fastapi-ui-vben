from fastapi import APIRouter

from .user import user_router
from .test import test_router
from .role import role_router
from .access import access_router

api_router = APIRouter(prefix="/api/v1", tags=["api路由"])
api_router.include_router(user_router)
api_router.include_router(test_router)
api_router.include_router(role_router)
api_router.include_router(access_router)