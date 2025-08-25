from typing import List
from pydantic import BaseModel
from fastapi import APIRouter


api_router = APIRouter(prefix="/v1", tags=["api路由"])

class Login(BaseModel):
    username: str
    password: str
    user: List[int]
@api_router.get('/input')
async def home(num: int):
    return {"num": num, "data": [{"num": num, "data": []}, {"num": num, "data": []}]}

@api_router.get("/index", tags=["api路由"], summary="注册接口")
def index(age: int = 80):
    return {"fun": "/index", "age": age}

@api_router.post("/login", tags=["api路由"], summary="登陆接口")
def login(data: Login):
    return data
