from fastapi import APIRouter, Request,Cookie
from starlette.responses import HTMLResponse
from sqlmodel import select
from typing import Optional

from db.models.base import User
from db.schemas.user import UserCreate
from core.session import SessionDep


user_router = APIRouter()


@user_router.get("/", response_class=HTMLResponse)
async def home(request: Request, session_id: Optional[str] = Cookie(None)):
    cookie = session_id
    session = request.session.get("session")
    page_data = {
        "cookie": cookie,
        "session": session
    }
    # request.session.setdefault("55555", "hdaldais")
    return request.app.state.views.TemplateResponse("index.html", {"request": request, **page_data})


@user_router.get("/reg", response_class=HTMLResponse)
async def reg_page(req: Request):
    return req.app.state.views.TemplateResponse("reg_page.html", {"request": req})

@user_router.get("/login", response_class=HTMLResponse)
async def login_page(req: Request):
    return req.app.state.views.TemplateResponse("login.html", {"request": req})

@user_router.post("/reg/form", response_class=HTMLResponse)
async def result_page(
    *,
    req: Request,
    userinfo: UserCreate,
    session: SessionDep,
):

    user = User(username=userinfo.username, password=userinfo.password)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    print("插入的自增ID", user.id)
    print("插入的用户名", user.username)

    user_list = await session.execute(select(User))
    user_list = user_list.scalars().all()
    for user in user_list:
        print(f"用户:{user.username}", user)

    result = await session.execute(
        select(User).where(User.username == userinfo.username)
    )
    user = result.scalars().first()

    if not user:
        print("")
        return {"info": "没有查询到用户"}

    return req.app.state.views.TemplateResponse(
        "reg_result.html",
        {"request": req, "username": user.username, "password": user.password},
    )


@user_router.get("/get")
async def get_all_user(*, session: SessionDep):

    user = await session.execute(select(User))
    user = user.scalars().all()
    return user
