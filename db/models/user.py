from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime, timezone


class User(SQLModel, table=True):
    __tablename__ = "user"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, max_length=20, description="用户名")
    type: bool = Field(
        default=False, description="用户类型 True:超级管理员 False:普通管理员"
    )
    password: str = Field(max_length=255, description="密码")
    nickname: str = Field(default="pleb", max_length=255, description="昵称")
    u_phone: Optional[str] = Field(default=None, max_length=11, description="手机号")
    u_email: Optional[str] = Field(default=None, max_length=255, description="邮箱")
    full_name: Optional[str] = Field(default=None, max_length=255, description="姓名")
    u_status: int = Field(default=0, description="0未激活 1正常 2禁用")
    head_img: Optional[str] = Field(default=None, max_length=255, description="头像")
    gender: int = Field(default=0, description="0未知 1男 2女")
    remarks: Optional[str] = Field(default=None, max_length=30, description="备注")
    client_host: Optional[str] = Field(
        default=None, max_length=19, description="访问IP"
    )
    create_time: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="创建时间",
    )
    update_time: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="更新时间",
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
    )
