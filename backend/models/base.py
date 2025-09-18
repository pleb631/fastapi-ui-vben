from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from sqlalchemy import Column, ForeignKey, func, DateTime, Text, Integer


def create_time_col():
    return Field(
        description="创建时间",
        sa_column=Column(
            DateTime(timezone=True), nullable=False, server_default=func.now()
        ),
    )


def update_time_col():
    return Field(
        description="更新时间",
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=func.now(),
            onupdate=func.now(),
        ),
    )


class UserRoleLink(SQLModel, table=True):
    __tablename__ = "user_role_link"
    user_id: int = Field(
        sa_column=Column(
            ForeignKey("user.id", ondelete="CASCADE"),
            primary_key=True,
        )
    )
    role_id: int = Field(
        sa_column=Column(
            ForeignKey("role.id", ondelete="CASCADE"),
            primary_key=True,
        )
    )


class RoleAccessLink(SQLModel, table=True):
    __tablename__ = "role_access_link"
    role_id: int = Field(
        sa_column=Column(ForeignKey("role.id", ondelete="CASCADE"), primary_key=True)
    )
    access_id: int = Field(
        sa_column=Column(ForeignKey("access.id", ondelete="CASCADE"), primary_key=True)
    )


class Role(SQLModel, table=True):
    __tablename__ = "role"
    __table_args__ = ({"comment": "角色表"},)
    id: Optional[int] = Field(default=None, primary_key=True)
    role_name: str = Field(unique=True, max_length=15, description="角色名称")

    role_status: bool = Field(default=False, description="True:启用 False:禁用")
    role_desc: Optional[str] = Field(
        default=None, max_length=255, description="角色描述"
    )

    users: List["User"] = Relationship(
        back_populates="roles",
        link_model=UserRoleLink,
        sa_relationship_kwargs={"passive_deletes": True},
    )
    accesses: List["Access"] = Relationship(
        back_populates="roles",
        link_model=RoleAccessLink,
        sa_relationship_kwargs={
            "passive_deletes": True,
        },
    )

    create_time: datetime = create_time_col()
    update_time: datetime = update_time_col()


class User(SQLModel, table=True):
    __tablename__ = "user"
    __table_args__ = ({"comment": "用户表"},)
    id: Optional[int] = Field(default=None, primary_key=True)
    roles: List["Role"] = Relationship(
        back_populates="users",
        link_model=UserRoleLink,
        sa_relationship_kwargs={"passive_deletes": True},
    )
    username: str = Field(unique=True, max_length=20, description="用户名")
    user_type: bool = Field(
        default=False, description="用户类型 True:超级管理员 False:普通管理员"
    )
    password: str = Field(max_length=255, description="密码")
    nickname: str = Field(default="pleb", max_length=255, description="昵称")
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

    create_time: datetime = create_time_col()
    update_time: datetime = update_time_col()


class Access(SQLModel, table=True):
    __tablename__ = "access"
    __table_args__ = ({"comment": "权限表"},)
    id: Optional[int] = Field(default=None, primary_key=True)
    access_name: str = Field(unique=True, max_length=15, description="权限名称")

    parent_id: Optional[int] = Field(
        default=None,
        description="父级权限ID",
        sa_column=Column(Integer, ForeignKey("access.id", ondelete="CASCADE"), index=True, nullable=True),
    )

    parent: Optional["Access"] = Relationship(
        sa_relationship_kwargs={
            "remote_side": "Access.id",
            "passive_deletes": True,
        },
        back_populates="children",
    )
    children: List["Access"] = Relationship(
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "passive_deletes": True,
            "single_parent": True,
        },
        back_populates="parent",
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
        sa_relationship_kwargs={"passive_deletes": True},
    )

    create_time: datetime = create_time_col()
    update_time: datetime = update_time_col()


class AccessLog(SQLModel, table=True):
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

    create_time: datetime = create_time_col()
    update_time: datetime = update_time_col()
