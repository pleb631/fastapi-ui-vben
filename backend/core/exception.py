from typing import Union
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from sqlalchemy.exc import NoResultFound,MultipleResultsFound


async def http_error_handler(_: Request, exc: HTTPException):
    if exc.status_code == 401:
        return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)

    return JSONResponse(
        {"code": exc.status_code, "message": exc.detail, "data": exc.detail},
        status_code=exc.status_code,
    )


class UnicornException(Exception):

    def __init__(self, code, errmsg, data=None):
        if data is None:
            data = {}
        self.code = code
        self.errmsg = errmsg
        self.data = data


async def unicorn_exception_handler(_: Request, exc: UnicornException):

    return JSONResponse(
        {
            "code": exc.code,
            "message": exc.errmsg,
            "data": exc.data,
        }
    )


async def http422_error_handler(
    _: Request,
    exc: Union[RequestValidationError, ValidationError],
) -> JSONResponse:

    return JSONResponse(
        {
            "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "message": f"数据校验错误 {exc.errors()}",
            "data": exc.errors(),
        },
        status_code=422,
    )


async def mysql_does_not_exist(_: Request, exc: NoResultFound):
    print("DoesNotExist", exc)
    return JSONResponse(
        {
            "code": -1,
            "message": "发出的请求针对的是不存在的记录，服务器没有进行操作。",
            "data": [],
        },
        status_code=404,
    )

async def mysql_multiple_exist(_: Request, exc: MultipleResultsFound):
    print("MultipleResultsFound", exc)
    return JSONResponse(
        {
            "code": -1,
            "message": "发出的请求针对的是不唯一的记录，服务器没有进行操作。",
            "data": [],
        },
        status_code=404,
    )