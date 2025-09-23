from sqlmodel import SQLModel, Field
from typing import Optional, Any

class BaseResp(SQLModel):
    code: int = Field(description="状态码")
    message: str = Field(description="信息")


class WebsocketMessage(SQLModel):
    action: Optional[str]
    user: Optional[int] = None
    data: Optional[Any] = None
    content: Optional[str] = None
    t: Optional[int] = None


class WechatOAuthData(SQLModel):
    access_token: str
    expires_in: int
    refresh_token: str
    unionid: Optional[str]
    scope: str
    openid: str


class WechatUserInfo(SQLModel):
    openid: str
    nickname: str
    sex: int
    city: str
    province: str
    country: str
    headimgurl: str
    unionid: Optional[str]