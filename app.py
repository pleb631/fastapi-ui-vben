from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError

from core.config import settings
from core.events import startup, stopping
from core.router import all_router
from core.middleware import Middleware
from core.exception import (
    http_error_handler,
    http422_error_handler,
    unicorn_exception_handler,
    UnicornException,
)


# 事件监听
@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup(app)
    yield
    await stopping(app)


app = FastAPI(
    debug=settings.APP_DEBUG,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
)


app.add_exception_handler(HTTPException, http_error_handler)
app.add_exception_handler(RequestValidationError, http422_error_handler)
app.add_exception_handler(UnicornException, unicorn_exception_handler)


app.include_router(all_router)

# 中间件
app.add_middleware(Middleware)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    session_cookie=settings.SESSION_COOKIE,
    max_age=settings.SESSION_MAX_AGE
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# 静态资源目录
app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")
app.state.views = Jinja2Templates(directory=settings.TEMPLATE_DIR)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000,reload=True)