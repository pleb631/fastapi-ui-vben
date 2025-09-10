from fastapi import APIRouter

from .user import login_router

api_router = APIRouter()
api_router.include_router(login_router)