from fastapi import FastAPI


async def startup(app: FastAPI):
    print("启动")


async def stopping(app: FastAPI):
    print("停止")
