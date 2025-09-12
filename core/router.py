from fastapi import APIRouter

from api import api_router
from views import views_router

all_router = APIRouter()

all_router.include_router(views_router)
all_router.include_router(api_router)
