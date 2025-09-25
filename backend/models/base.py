from typing import Optional, List, Dict, Any
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from sqlalchemy import Column, func, Text, JSON


class TimestampMixin(SQLModel, table=False):
    create_time: datetime = Field(
        description="创建时间",
        nullable=False,
        sa_column_kwargs={"server_default": func.now()},
    )
    update_time: datetime = Field(
        description="更新时间",
        nullable=False,
        sa_column_kwargs={
            "server_default": func.now(),
            "onupdate": func.now(),
        },
    )


class UserRoleLink(SQLModel, table=True):
    __tablename__ = "user_role_link"

    user_id: int = Field(
        ondelete="CASCADE",
        foreign_key="user.id",
        primary_key=True,
    )
    role_id: int = Field(
        ondelete="CASCADE",
        foreign_key="role.id",
        primary_key=True,
    )


class RoleAccessLink(SQLModel, table=True):
    __tablename__ = "role_access_link"

    role_id: int = Field(
        ondelete="CASCADE",
        foreign_key="role.id",
        primary_key=True,
    )
    access_id: int = Field(
        ondelete="CASCADE",
        foreign_key="access.id",
        primary_key=True,
    )


class Role(TimestampMixin, table=True):
    __tablename__ = "role"
    __table_args__ = {"comment": "角色表"}

    id: Optional[int] = Field(default=None, primary_key=True)
    role_name: str = Field(unique=True, max_length=15, description="角色名称")

    role_status: bool = Field(default=True, description="True:启用 False:禁用")
    role_desc: Optional[str] = Field(
        default=None, max_length=255, description="角色描述"
    )

    users: List["User"] = Relationship(
        back_populates="roles",
        link_model=UserRoleLink,
        passive_deletes="all",
        sa_relationship_kwargs={"lazy": "raise_on_sql"},
    )
    accesses: List["Access"] = Relationship(
        back_populates="roles",
        link_model=RoleAccessLink,
        passive_deletes="all",
        sa_relationship_kwargs={"lazy": "raise_on_sql"},
    )


class User(TimestampMixin, table=True):
    __tablename__ = "user"
    __table_args__ = ({"comment": "用户表"},)

    id: Optional[int] = Field(default=None, primary_key=True)
    roles: List["Role"] = Relationship(
        back_populates="users",
        link_model=UserRoleLink,
        passive_deletes="all",
        sa_relationship_kwargs={"lazy": "raise_on_sql"},
    )
    username: str = Field(
        unique=True, min_length=3, max_length=10, description="用户名"
    )
    user_type: bool = Field(
        default=False, description="用户类型 True:超级管理员 False:普通管理员"
    )
    password: str = Field(max_length=255, description="密码")
    nickname: Optional[str] = Field(max_length=255, description="昵称")
    user_phone: Optional[str] = Field(default=None, max_length=11, description="手机号")
    user_email: Optional[str] = Field(default=None, max_length=255, description="邮箱")
    full_name: Optional[str] = Field(default=None, max_length=255, description="姓名")
    user_status: int = Field(default=0, description="0未激活 1正常 2禁用")
    avatar: Optional[str] = Field(default=None, max_length=255, description="头像")
    gender: int = Field(default=0, description="0未知 1男 2女")
    remarks: Optional[str] = Field(default=None, max_length=30, description="备注")
    client_host: Optional[str] = Field(
        default=None, max_length=64, description="访问IP"
    )

    wechat: Optional["UserWechat"] = Relationship(
        back_populates="user",
        cascade_delete=True,
    )


class Access(TimestampMixin, table=True):
    __tablename__ = "access"
    __table_args__ = {"comment": "权限表"}

    id: Optional[int] = Field(default=None, primary_key=True)
    access_name: str = Field(unique=True, max_length=15, description="权限名称")

    parent_id: Optional[int] = Field(
        default=None,
        description="父级权限ID",
        foreign_key="access.id",
        ondelete="CASCADE",
        index=True,
        nullable=True,
    )

    parent: Optional["Access"] = Relationship(
        back_populates="children",
        sa_relationship_kwargs={
            "remote_side": "Access.id",
        },
    )
    children: List["Access"] = Relationship(
        passive_deletes="all",
        back_populates="parent",
        sa_relationship_kwargs={
            "single_parent": True,
        },
    )
    scopes: str = Field(unique=True, max_length=255, description="权限范围")
    access_desc: Optional[str] = Field(
        default=None, max_length=255, description="权限描述"
    )
    menu_icon: Optional[str] = Field(
        default=None, max_length=255, description="菜单图标"
    )
    is_check: bool = Field(default=False, description="是否启用验证权限")
    is_menu: bool = Field(default=False, description="是否是菜单")

    roles: List[Role] = Relationship(
        back_populates="accesses",
        link_model=RoleAccessLink,
        passive_deletes="all",
        sa_relationship_kwargs={"lazy": "raise_on_sql"},
    )


class AccessLog(TimestampMixin, table=True):
    __tablename__ = "access_log"
    __table_args__ = ({"comment": "用户操作记录表"},)
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(
        default=None, description="用户ID", foreign_key="user.id"
    )
    target_url: Optional[str] = Field(
        default=None, max_length=255, description="访问的URL"
    )
    user_agent: Optional[str] = Field(
        default=None, max_length=255, description="用户ua"
    )
    request_params: Optional[str] = Field(Column(Text), description="请求参数")
    ip: Optional[str] = Field(default=None, max_length=32, description="访问IP")
    note: Optional[str] = Field(default=None, max_length=255, description="备注")


class SystemParams(TimestampMixin, table=True):
    __tablename__ = "system_params"
    __table_args__ = ({"comment": "系统参数表"},)

    id: Optional[int] = Field(default=None, primary_key=True)
    params_name: str = Field(unique=True, max_length=255, description="参数名")
    params: Dict[str, Any] = Field(
        default_factory=dict, sa_column=Column(JSON, nullable=False)
    )


class UserWechat(TimestampMixin, table=True):
    __tablename__ = "user_wechat"
    __table_args__ = ({"comment": "用户微信"},)

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True, nullable=False,ondelete="CASCADE")
    city: Optional[str] = Field(default=None, max_length=255, description="城市")
    country: Optional[str] = Field(default=None, max_length=255, description="国家")
    headimgurl: Optional[str] = Field(
        default=None, max_length=255, description="微信头像"
    )
    nickname: Optional[str] = Field(
        default=None, max_length=255, description="微信昵称"
    )
    openid: Optional[str] = Field(default=None, max_length=255, description="openid")
    unionid: Optional[str] = Field(default=None, max_length=255, description="unionid")
    province: Optional[str] = Field(default=None, max_length=255, description="省份")
    gender: Optional[str] = Field(default=None, description="性别")
    user: Optional["User"] = Relationship(
        back_populates="wechat",
    )
