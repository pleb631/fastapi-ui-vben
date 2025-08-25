from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse


views_router = APIRouter()


@views_router.get("/items/{id}", response_class=HTMLResponse)
async def home(request: Request, id: str):

    return request.app.state.views.TemplateResponse(
        "index.html", {"request": request, "id": id}
    )
