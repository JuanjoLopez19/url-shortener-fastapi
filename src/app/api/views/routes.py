from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from src.app.api import templates

router = APIRouter(tags=["Views"])


@router.get("/", response_class=HTMLResponse)
async def read_root(
    request: Request,
):
    return templates.TemplateResponse(
        "index.html", request=request, context={"request": request}
    )
