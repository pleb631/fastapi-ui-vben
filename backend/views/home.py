from fastapi import APIRouter, Request,Cookie
from starlette.responses import HTMLResponse
from typing import Optional


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
