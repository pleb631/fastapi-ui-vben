from fastapi import APIRouter

from .home import user_router


views_router = APIRouter(prefix="/views", tags=["视图"])

views_router.include_router(user_router)