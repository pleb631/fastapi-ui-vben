from typing import List
from pydantic import BaseModel
from fastapi import APIRouter


login_router = APIRouter()

class Login(BaseModel):
    username: str
    password: str
    user: List[int]
@login_router.get('/input')
async def home(num: int):
    return {"num": num, "data": [{"num": num, "data": []}, {"num": num, "data": []}]}

@login_router.get("/index", tags=["api路由"], summary="注册接口")
def index(age: int = 80):
    return {"fun": "/index", "age": age}

@login_router.post("/login", tags=["api路由"], summary="登陆接口")
def login(data: Login):
    return data
