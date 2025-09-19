from typing import List, Annotated, Optional
from fastapi import Query, APIRouter, Security, Query

from core.session import SessionDep
from core.auth import check_permissions
from core.response import success, fail
from schemas.role import CreateRole, UpdateRole, RoleListResp, RoleItem
from models.base import Role
import curd

role_router = APIRouter(prefix="/role",tags=["角色管理"])


@role_router.get(
    "/all",
    summary="所有角色下拉选项接口",
    dependencies=[Security(check_permissions, scopes=["user_role"])],
)
async def all_roles_options(*, user_id: int = Query(None), session: SessionDep):

    roles: List[Role] = await curd.role.get_all_role(session)
    user_roles: List[str] = await curd.role.get_user_role(session, user_id)
    data = {"all_role": roles, "user_roles": user_roles}
    return success(msg="所有角色下拉选项", data=data)


@role_router.post(
    "/",
    summary="角色添加",
    dependencies=[Security(check_permissions, scopes=["role_add"])],
)
async def create_role(post: CreateRole, session: SessionDep):

    result: Optional[Role] = await curd.role.add_role(session, post)
    if not result:
        return fail(msg="创建失败!")
    return success(msg="创建成功!")


@role_router.delete(
    "/",
    summary="角色删除",
    dependencies=[Security(check_permissions, scopes=["role_delete"])],
)
async def delete_role(role_id: int, session: SessionDep):

    role: Optional[Role] = await curd.role.delete_role(session, role_id=role_id)
    if not role:
        return fail(msg="角色不存在!")
    return success(msg="删除成功!")


@role_router.put(
    "/",
    summary="角色修改",
    dependencies=[Security(check_permissions, scopes=["role_update"])],
)
async def update_role(post: UpdateRole, session: SessionDep):

    data = post.model_dump()
    data.pop("id")
    result: Optional[Role] = await curd.role.update_role(session, post.id, data)
    if not result:
        return fail(msg="更新失败!")
    return success(msg="更新成功!")


@role_router.get(
    "/list",
    summary="角色列表",
    dependencies=[Security(check_permissions, scopes=["role_query"])],
    response_model=RoleListResp,
)
async def get_role_list(
    *,
    size: Annotated[int, Query(gt=0)] = 10,
    current: Annotated[int, Query(ge=1)] = 1,
    keyword: str = Query(None),
    session: SessionDep
):

    roles, total = await curd.role.get_role_list(session, size, current, keyword)

    role_list = [RoleItem(**r.model_dump()) for r in roles]

    return success(data=dict(items=role_list, total=total), msg="角色列表")
