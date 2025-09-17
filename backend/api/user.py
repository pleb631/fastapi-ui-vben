from fastapi import APIRouter, Security, Request
from starlette.responses import JSONResponse

from core.session import SessionDep
import curd
from core.response import fail, success
from schemas.user import UserCreate, AccountLogin
from core.utils import en_password, check_password
from core.auth import check_permissions, create_access_token
from models.base import User
from schemas.user import UserLoginResp, UserInfo, UserInfoResp,UserCodesResp

user_router = APIRouter(prefix="/user")


@user_router.get(
    "/info",
    response_model=UserInfoResp,
    summary="用户信息接口",
    dependencies=[Security(check_permissions)],
)
async def get_user_info(req: Request, session: SessionDep):
    user_id = req.state.user_id
    user_data = await curd.user.get_user(session, user_id=user_id)
    if not user_data:
        return fail(msg=f"用户ID{user_id}不存在!")
    user_info = UserInfo(**user_data.model_dump())

    return success(msg="用户信息", data=user_info)


@user_router.post(
    "/add",
    summary="用户添加接口",
    response_class=JSONResponse,
    dependencies=[Security(check_permissions, scopes=["user_add"])],
)
async def user_add(
    post: UserCreate,
    session: SessionDep,
):
    password = en_password(post.password)
    create_user = await curd.user.create_user(session, post.username, password)
    if not create_user:
        return fail(msg=f"用户{post.username}创建失败!")

    return success(msg=f"用户{create_user.username}创建成功")


@user_router.post(
    "/del",
    summary="删除用户接口",
    response_class=JSONResponse,
    dependencies=[Security(check_permissions, scopes=["user_delete"])],
)
async def user_del(user_id: int, session: SessionDep):
    delete_user = await curd.user.delete_user(session, user_id)
    if not delete_user:
        return fail(msg=f"用户{user_id}删除失败!")
    return success(msg="删除成功")


@user_router.get(
    "/rule/{user_id}", summary="获取用户权限接口", response_class=JSONResponse
)
async def get_user_rules(user_id: int, session: SessionDep):

    user_access_list = await curd.user.get_user_rules(session, user_id)

    data = {"user_access_list": user_access_list}
    return success(msg="用户权限", data=data)


@user_router.post(
    "/login",
    summary="用户登陆接口",
    response_model=UserLoginResp,
)
async def account_login(post: AccountLogin, session: SessionDep):

    get_user: User = await curd.user.get_user(session, username=post.username)
    if not get_user:
        return fail(msg=f"用户{post.username}密码验证失败!")
    if not check_password(post.password, get_user.password):
        return fail(msg=f"用户{post.username}密码验证失败!")
    if not get_user.user_status:
        return fail(msg=f"用户{post.username}已被管理员禁用!")
    jwt_data = {"user_id": get_user.id, "user_type": get_user.user_type}
    jwt_token = create_access_token(data=jwt_data)

    return success(
        msg="登陆成功😄",
        data={"access_token": "Bearer " + jwt_token, "expires_in": 3600},
    )


@user_router.get(
    "/codes",
    tags=["获取用户信息"],
    dependencies=[Security(check_permissions)],
    response_model=UserCodesResp,
)
async def get_user_codes(req: Request, session: SessionDep):
    user_id = req.state.user_id
    user_data = await curd.user.get_user(session, user_id=user_id)
    if not user_data:
        return fail(msg=f"用户ID{user_id}不存在!")
    else:
        codes = "admin" if user_data.user_type else "user"
        return success(msg="用户权限", data=[codes])
