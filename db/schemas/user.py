from sqlmodel import Field, SQLModel
from fastapi import Form
from typing import Optional
from .base import BaseResp
class UserCreate(SQLModel):

    username: str = Field(index=True, max_length=20, description="用户名")
    password: str = Field(max_length=255, description="密码")
    user_type: bool = Field(
        default=False, description="用户类型 True:超级管理员 False:普通管理员"
    )


class AccountLogin(SQLModel):
    username: str = Field(min_length=3, max_length=10)
    password: str = Field(min_length=8, max_length=12)



class UserInfo(SQLModel):
    id: int
    username: str
    age: Optional[int]
    user_type: bool
    nickname: Optional[str]
    user_phone: Optional[str]
    user_email: Optional[str]
    full_name: Optional[str]
    user_status: bool
    header_img: Optional[str]
    sex: int


class CurrentUser(BaseResp):
    data: UserInfo

class AccessToken(SQLModel):
    token: Optional[str]
    expires_in: Optional[int]


class UserLogin(BaseResp):
    data: AccessToken