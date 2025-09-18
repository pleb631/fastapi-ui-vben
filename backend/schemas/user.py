from sqlmodel import Field, SQLModel
from typing import Dict, List, Optional
from .base import BaseResp


class UserCreate(SQLModel):

    username: str = Field(
        index=True, max_length=20, description="用户名")
    password: str = Field(max_length=255, description="密码")
    user_type: bool = Field(
        default=False,
        description="用户类型 True:超级管理员 False:普通管理员",
        alias="userType",
    )


class AccountLogin(SQLModel):
    username: str = Field(min_length=3, max_length=10)
    password: str = Field(min_length=6, max_length=12)
    captcha: bool = Field(alias="captcha")


class UserInfo(SQLModel):
    id: int
    username: str
    user_type: bool
    nickname: Optional[str]
    user_phone: Optional[str]
    user_email: Optional[str]
    full_name: Optional[str]
    user_status: bool
    avatar: Optional[str]
    gender: int


class UserInfoResp(BaseResp):
    data: Optional[UserInfo]


class AccessToken(SQLModel):
    access_token: Optional[str]


class UserLoginResp(BaseResp):
    data: Optional[AccessToken]


class UserCodesResp(BaseResp):
    data: Optional[List[str]]
