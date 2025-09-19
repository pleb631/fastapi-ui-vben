from sqlmodel import SQLModel, Field
from typing import List, Optional
from datetime import datetime

from .base import BaseResp


class CreateRole(SQLModel):
    role_name: str = Field(min_length=3, max_length=10)
    role_status: Optional[bool] = False
    role_desc: Optional[str] = Field(max_length=255)


class UpdateRole(SQLModel):
    id: int
    role_name: str
    role_status: Optional[bool]
    role_desc: Optional[str]


class RoleItem(SQLModel):
    id: int
    role_name: str
    role_status: Optional[bool]
    role_desc: Optional[str]
    create_time: datetime
    update_time: datetime


class RoleList(SQLModel):
    items: List[RoleItem]
    total: int

class RoleListResp(BaseResp):
    data: RoleList


class updateAccess(SQLModel):
    role_id: int
    access: List[int] = Field(default=[], description="权限集合")


class CreateAccess(SQLModel):
    access_name: str = Field(description="权限名称")
    scopes: str = Field(description="权限标识")
    parent_id: int = 0
    is_check: bool = False
    is_menu: bool = False
