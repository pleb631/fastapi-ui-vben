from sqlmodel import select, SQLModel
import asyncio


from core.session import async_session_maker, engine
from models.base import User, Access, Role, UserRoleLink, RoleAccessLink
from core.utils import en_password
from config import settings


async def main():

    async with engine.begin() as conn:

        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

    async with async_session_maker() as session:

        user = User(
            username=settings.SUPERUSER,
            password=en_password("12345678"),
            user_type=True,
            user_status=True,
        )
        admin = User(
            username="user1",
            password=en_password("12345678"),
            user_type=False,
            user_status=False,
        )
        session.add(user)
        session.add(admin)
        name = ["id", "access_name", "parent_id", "scopes", "is_check", "is_menu"]
        access_arr = [
            [
                0,
                "系统管理",
                0,
                "system",
                0,
                0,
            ],
            [
                1,
                "用户中心",
                0,
                "user",
                0,
                1,
            ],
            [
                2,
                "用户管理",
                1,
                "user_m",
                0,
                1,
            ],
            [3, "角色管理", 1, "role_m", 0, 1],
            [4, "用户查询", 2, "user_query", 1, 0],
            [5, "用户添加", 2, "user_add", 1, 0],
            [6, "用户编辑", 2, "user_update", 1, 0],
            [7, "用户删除", 2, "user_delete", 1, 0],
            [8, "角色分配", 2, "user_role", 1, 0],
            [9, "角色查询", 3, "role_query", 1, 0],
            [10, "角色添加", 3, "role_add", 1, 0],
            [11, "角色编辑", 3, "role_update", 1, 0],
            [12, "角色删除", 3, "role_delete", 1, 0],
            [13, "权限分配", 3, "role_access", 1, 0],
        ]
        for row in access_arr:
            data = dict(zip(name, row))
            if not data["parent_id"]:
                data["parent_id"] = None
            if data["parent_id"] is not None:
                continue
            data["is_check"] = bool(data["is_check"])
            data["is_menu"] = bool(data["is_menu"])
            if not (
                await session.execute(select(Access).where(Access.id == data["id"]))
            ).first():
                session.add(Access(**data))
        for row in access_arr:
            data = dict(zip(name, row))
            if not data["parent_id"]:
                continue
            data["is_check"] = bool(data["is_check"])
            data["is_menu"] = bool(data["is_menu"])

            parent = await session.execute(
                select(Access).where(Access.id == data["parent_id"])
            )
            if not parent.first():
                raise ValueError(f"父节点 {data['parent_id']} 不存在")
            if not (
                await session.execute(select(Access).where(Access.id == data["id"]))
            ).first():
                session.add(Access(**data))

        await session.commit()

        admin_role = Role(role_name="admin", description="管理员角色")
        session.add(admin_role)

        await session.flush()

        existing_access_ids = (
            (await session.execute(select(Access.id))).scalars().all()
        )

        for ac in existing_access_ids:
            session.add(RoleAccessLink(role_id=admin_role.id, access_id=ac))

        root_user = (
            await session.execute(select(User).where(User.username == "root"))
        ).scalar_one_or_none()
        user1 = (
            await session.execute(select(User).where(User.username == "user1"))
        ).scalar_one_or_none()

        session.add(UserRoleLink(user_id=root_user.id, role_id=admin_role.id))
        session.add(UserRoleLink(user_id=user1.id, role_id=admin_role.id))
        await session.commit()


if __name__ == "__main__":
    asyncio.run(main())
