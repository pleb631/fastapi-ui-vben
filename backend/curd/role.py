from sqlmodel import select
from models.base import User, Role, Access, RoleAccessLink, UserRoleLink
from typing import List, Optional, Dict, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.role import CreateRole


async def get_all_role(session: AsyncSession) -> List[Role]:
    role = await session.execute(select(Role))
    return role.scalars().all()


async def get_user_role(session: AsyncSession, user_id: int) -> List[str]:
    role = await session.execute(
        select(Role).join(UserRoleLink).where(UserRoleLink.user_id == user_id)
    )
    return [i.role_name for i in role.scalars().all()]


async def add_role(session: AsyncSession, data:Dict) -> Optional[Role]:
    search_role = await session.execute(
        select(Role).where(Role.role_name == data["role_name"])
    )
    if search_role.scalars().first():
        return None
    role = Role(**data)
    session.add(role)
    await session.commit()
    return role


async def delete_role(session: AsyncSession, role_id: int) -> Optional[Role]:
    role = await session.execute(select(Role).where(Role.id == role_id))
    role = role.scalars().first()
    if not role:
        return None
    await session.delete(role)
    await session.commit()
    return role


async def update_role(session: AsyncSession, role_id: int, data) -> Optional[Role]:
    role = await session.execute(select(Role).where(Role.id == role_id))
    role: Role | None = role.scalars().first()
    if not role:
        return None
    for key, value in data.items():
        if hasattr(role, key):
            setattr(role, key, value)

    session.add(role)
    await session.commit()
    return role


async def get_role_list(
    session: AsyncSession,
    size: int,
    current: int,
    keyword: str = None,
) -> Tuple[List[Role], int]:
    query = select(Role)
    if keyword:
        query = query.where(Role.role_name.like(f"%{keyword}%"))
    total = await session.execute(
        select(Role).where(Role.role_name.like(f"%{keyword}%"))
    )
    total = total.scalars().all()
    role = await session.execute(
        query.offset((current - 1) * size)
        .limit(size)
    )
    return role.scalars().all(), len(total) if total else 0
