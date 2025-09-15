from sqlmodel import select
from models.base import User, Role, Access, RoleAccessLink, UserRoleLink
from typing import List, Optional


async def create_user(session, username, password) -> Optional[User]:
    result = await session.execute(select(User).where(User.username == username))
    if result.scalars().first():
        return None
    new_user = User(username=username, password=password)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


async def get_user(
    session, user_id: Optional[int] = None, username: Optional[str] = None
) -> Optional[User]:
    if user_id is None and username is None:
        return None
    stmt = select(User)
    if user_id is not None:
        stmt = stmt.where(User.id == user_id)
    if username is not None:
        stmt = stmt.where(User.username == username)

    result = await session.execute(stmt)
    user = result.scalars().first()
    return user


async def delete_user(session, user_id: int) -> Optional[User]:
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        return None
    await session.delete(user)
    await session.commit()
    return user


async def get_user_rules(session, user_id: int) -> List[Access]:
    stmt = (
        select(Access)
        .join(RoleAccessLink, RoleAccessLink.access_id == Access.id)
        .join(Role, Role.id == RoleAccessLink.role_id)
        .join(UserRoleLink, UserRoleLink.role_id == Role.id)
        .join(User, User.id == UserRoleLink.user_id)
        .where(User.id == user_id, Access.is_check.is_(True))
        .distinct()
    )
    result = await session.execute(stmt)
    return result.scalars().all()
