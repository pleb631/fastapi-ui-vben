from fastapi import FastAPI

from db.session import engine, get_session, init_db
async def startup(app: FastAPI):
    print("启动")
    await init_db()


async def stopping(app: FastAPI):
    print("停止")
