from sqlmodel import Field, SQLModel
from typing import Dict, List, Optional
from .base import BaseResp


class UserCreate(SQLModel):
    id: Optional[int] = Field(default=None)
    username: str = Field(index=True, min_length=3, max_length=10, description="用户名")
    password: str = Field(min_length=6, max_length=12, description="密码")


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


class UserListItem(SQLModel):
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
    remarks: Optional[str]


class UserList(SQLModel):
    total: int
    items: List[UserListItem]


class UserListResp(BaseResp):
    data: Optional[UserList]


class UpdateUserReq(SQLModel):
    id: int
    username: str = Field(min_length=3, max_length=10)
    nickname: Optional[str] = Field(default=None,)
    password: Optional[str] = Field(default=None,min_length=6, max_length=12)
    user_phone: Optional[str] = Field(default=None,regex="^1[34567890]\\d{9}$")
    user_email: Optional[str] = Field(default=None,)
