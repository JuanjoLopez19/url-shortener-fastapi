from typing import Annotated

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse

from src.app import settings
from src.app.api import templates
from src.app.api.endpoints.controller import shorten_url_controller

router = APIRouter(tags=["API"])


@router.post("/shorten", response_class=HTMLResponse)
async def shorten_url(request: Request, url: Annotated[str, Form()]):
    try:
        host = request.base_url.hostname
        port = request.base_url.port
        protocol = request.base_url.scheme

        base_url = (
            f"{protocol}://{host}:{port}"
            if settings.development
            else f"{protocol}://{host}"
        )

        result = await shorten_url_controller(url, base_url)

        if result.success:
            return templates.TemplateResponse(
                "result.html",
                {
                    "request": request,
                    "title": "URL Acortada",
                    "longUrl": url,
                    "shortUrl": result.url,
                },
            )
        else:
            return templates.TemplateResponse(
                "error.html",
                {
                    "request": request,
                    "message": "Error al acortar URL",
                    "error": {"status": 500, "stack": result.error},
                },
            )
    except Exception as e:
        print(e)

        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "message": "Error del servidor",
                "error": {"status": 500, "stack": str(e)},
            },
        )
