from sqlmodel import select, delete
from models.base import Access, RoleAccessLink,Role
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession


async def get_all_access(session: AsyncSession) -> List[Access]:
    access = await session.execute(select(Access))
    return access.scalars().all()


async def get_role_access(session: AsyncSession, role_id: int) -> List[int]:
    access = await session.execute(
        select(RoleAccessLink.access_id).where(RoleAccessLink.role_id == role_id)
    )
    return access.scalars().all()


async def update_role_access(session: AsyncSession, role_id: int, access: List[int]):

    role = await session.get(Role, role_id)
    if not role:
        return None
    await session.execute(
        delete(RoleAccessLink).where(RoleAccessLink.role_id == role_id)
    )
    links = [RoleAccessLink(role_id=role_id, access_id=i) for i in access]
    session.add_all(links)
    await session.commit()

    return role
    

    
