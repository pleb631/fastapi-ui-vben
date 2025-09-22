from fastapi import APIRouter, Security

from core.auth import check_permissions
from core.response import success
from schemas.role import updateAccess
import curd
from core.session import SessionDep
from core.utils import build_tree

access_router = APIRouter(prefix="/access", tags=["权限管理"])


# @access_router.post("/", summary="权限创建")
# async def add_access(post: CreateAccess, session: SessionDep):

#     result = await curd.access.add_access(session,scopes=post.scopes)
#     if result:
#         return fail(msg=f"scopes:{post.scopes} 已经存在!")

#     return success(msg=f"权限 {result.pk} 创建成功!")


@access_router.get(
    "",
    summary="权限查询",
    dependencies=[Security(check_permissions, scopes=["role_access"])],
)
async def get_all_access(role_id: int, session: SessionDep):
    result = await curd.access.get_all_access(session)

    role_access = await curd.access.get_role_access(session, role_id)
    result = [
        {
            "key": i.id,
            "access_name": i.access_name,
            "parent_id": i.parent_id,
            "scopes": i.scopes,
            "access_desc": i.access_desc,
        }
        for i in result
    ]
    tree_data = build_tree(result)

    data = {"all_access": tree_data, "role_access": role_access}

    return success(msg="当前用户可以下发的权限", data=data)


@access_router.put(
    "",
    summary="权限设置",
    dependencies=[Security(check_permissions, scopes=["role_access"])],
)
async def update_role_access(post: updateAccess, session: SessionDep):

    role_data = await curd.access.update_role_access(
        session, role_id=post.role_id, access=post.access
    )

    return success(msg="保存成功!")
