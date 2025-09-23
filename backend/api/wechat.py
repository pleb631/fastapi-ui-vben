import json
import time
from wechatpy.oauth import WeChatOAuth
from wechatpy.exceptions import WeChatOAuthException
from fastapi import Request, APIRouter, Depends
from core.auth import create_access_token
from core.response import fail, success
from models.base import SystemParams
from sqlmodel import select

from config import settings
from schemas.base import WechatOAuthData, WechatUserInfo
from models.base import User,UserWechat
from core.redis import get_redis, redis
from core.session import SessionDep

wechat_router = APIRouter(prefix='/wechat', tags=["微信授权"])


@wechat_router.get("/auth/url")
async def get_authorize_url(
    *, req: Request, redis: redis.Redis = Depends(get_redis), session: SessionDep
):

    state = req.session.get("session")
    print(state)
    if not state:
        return fail(msg="非法请求")
    result = (await session.execute(select(SystemParams).where(SystemParams.params_name == "wechat_auth"))).scalars().one_or_none()
    if not result:
        return fail(msg="请配置微信开发者参数")

    oauth = WeChatOAuth(
        app_id=result.params.get("appid"),
        secret=result.params.get("secret"),
        scope="snsapi_userinfo",  # snsapi_base or snsapi_userinfo
        state=state,
        redirect_uri=result.params.get("redirect_uri"),
    )
    data = {"status": 0}

    await redis.set(
        name=f"auth_{state}", value=json.dumps(data), ex=settings.QRCODE_EXPIRE
    )

    return success(
        data={"authorize_url": oauth.authorize_url + "&t=" + str(int(time.time()))}
    )


@wechat_router.get("/auth/call")
async def call(req: Request, code: str, state: str,session: SessionDep,redis: redis.Redis = Depends(get_redis)):

    data = await redis.get(f"auth_{state}")
    if not data:
        return req.app.state.views.TemplateResponse(
            "wechat.html", {"request": req, "errmsg": "二维码已过期!"}
        )

    result = (await session.execute(select(SystemParams).where(SystemParams.params_name == "wechat_auth"))).scalars().one_or_none()
    if not result:
        return req.app.state.views.TemplateResponse(
            "wechat.html", {"request": req, "errmsg": "请配置微信开发者参数!"}
        )


    oauth = WeChatOAuth(
        app_id=result.params.get("appid"),
        secret=result.params.get("secret"),
        redirect_uri=result.params.get("redirect_uri"),
    )

    try:
        # 拉取用户信息
        auth_data = WechatOAuthData(**oauth.fetch_access_token(code))

        # access_token
        time.sleep(0.5)
        # openid – 可选，微信
        # openid，默认获取当前授权用户信息
        #
        # access_token – 可选，
        # access_token，默认使用当前授权用户的access_token
        userinfo = WechatUserInfo(
            **oauth.get_user_info(
                openid=auth_data.openid, access_token=auth_data.access_token
            )
        )
        print(userinfo.model_dump())

        data = {"status": 1, "userinfo": userinfo.model_dump()}
        await redis.set(
            name=f"auth_{state}", value=json.dumps(data), ex=settings.QRCODE_EXPIRE
        )
        return req.app.state.views.TemplateResponse(
            "wechat.html",
            {
                "request": req,
                "client_ip": req.headers.get("x-forwarded-for"),
                **userinfo.model_dump(),
            },
        )

    except WeChatOAuthException as e:
        return req.app.state.views.TemplateResponse(
            "wechat.html", {"request": req, "errmsg": e.errmsg}
        )


@wechat_router.get("/auth/check")
async def scan_check(*,req: Request, redis: redis.Redis = Depends(get_redis), session: SessionDep):

    state = req.session.get("session")

    data = await redis.get(f"auth_{state}")
    if not data:
        return fail(code=201, msg="二维码已经过期!")

    result: dict = json.loads(data)
    if result.get("status") == 1:
        userinfo = WechatUserInfo(**result.get("userinfo"))
        user = (await session.execute(select(User).join(UserWechat).where(UserWechat.openid == userinfo.openid))).scalars().one_or_none()
        if not user:
            return fail(code=202, msg="当前微信未绑定,前往个人中心绑定!")
        jwt_data = {"user_id": user.id, "user_type": user.user_type}
        jwt_token = create_access_token(data=jwt_data)
        data = {
            "token": jwt_token,
            "expires_in": settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        }
        await redis.delete(f"auth_{state}")
        return success(msg="登陆成功!", data=data)

    return fail(msg="等待扫码...")
