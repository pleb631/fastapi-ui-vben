from sqlmodel import SQLModel, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import Annotated
from fastapi import Depends

from core.config import settings
from db.models.base import User

# ⚠️ 确认 settings.DATABASE_URL 用的是异步驱动，比如：
# MySQL:  mysql+aiomysql://user:password@localhost:3306/mydb
# Postgres: postgresql+asyncpg://user:password@localhost:5432/mydb
# SQLite: sqlite+aiosqlite:///./test.db

DATABASE_URL = str(settings.DATABASE_URL)
print("DATABASE_URL:", DATABASE_URL)


engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_size=20,
    max_overflow=40,
    pool_timeout=30,
    pool_recycle=1800
)


async_session_maker = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session():
    async with async_session_maker() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]

async def init_db():
    async with engine.begin() as conn:

        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

    async with async_session_maker() as session:
        result = await session.execute(select(User).where(User.username == "root"))
        user = result.scalars().first()
        if not user:
            user = User(
                username="root",
                password="123456",
                type=True,
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
        else:
            print("检测到用户已存在")
