from typing import List
from pydantic import BaseModel
from fastapi import APIRouter
from starlette.responses import JSONResponse

from core.session import SessionDep
from db import curd
from core.response import fail, success
from db.schemas.user import UserCreate
from core.utils import en_password


login_router = APIRouter(prefix="/user")


class Login(BaseModel):
    username: str
    password: str
    user: List[int]


@login_router.get(
    "/info/{user_id}", response_class=JSONResponse, summary="用户信息接口"
)
async def get_user_info(user_id: int, session: SessionDep):
    user_data = await curd.user.get_user_by_id(session, user_id)
    if not user_data:
        return fail(msg=f"用户ID{user_id}不存在!")
    return success(msg="用户信息", data=user_data)


@login_router.post("/add", summary="注册接口")
async def user_add(post: UserCreate, session: SessionDep):
    password = en_password(post.password)
    create_user = await curd.user.create_user(session, post.username, password)
    if not create_user:
        return fail(msg=f"用户{post.username}创建失败!")
    return success(msg=f"用户{create_user.username}创建成功")


@login_router.post("/del", summary="删除用户接口")
async def user_del(user_id: int, session: SessionDep):
    delete_user = await curd.user.delete_user(session, user_id)
    if not delete_user:
        return fail(msg=f"用户{user_id}删除失败!")
    return success(msg="删除成功")


@login_router.get("/rule/{user_id}", summary="获取用户权限接口")
async def get_user_rules(user_id: int, session: SessionDep):

    user_access_list = await curd.user.get_user_rules(session, user_id)

    data = {"user_access_list": user_access_list}
    return success(msg="用户权限", data=data)
