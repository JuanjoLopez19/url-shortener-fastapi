import json
from datetime import date

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from src.app.api import templates
from src.app.database.schemas.url import UrlSchema

router = APIRouter(tags=["Views"])


@router.get("/", response_class=HTMLResponse)
async def read_root(
    request: Request,
):
    return templates.TemplateResponse(
        "index.html",
        request=request,
        context={"request": request, "title": "URL Shortener"},
    )


@router.get("/{token}")
async def get_url(request: Request, token: str):
    if not token:
        return templates.TemplateResponse(
            "error.html",
            context={
                "request": request,
                "message": "Token not found",
                "error": {
                    "status": 400,
                    "stack": json.dumps({"message": "Token not found"}),
                },
            },
        )

    url_doc = await UrlSchema.find_one(UrlSchema.shortened == token)

    if not url_doc:
        return templates.TemplateResponse(
            "error.html",
            context={
                "request": request,
                "message": "URL no encontrada",
                "error": {
                    "status": 404,
                    "stack": json.dumps(
                        {"message": f"No se encontró ninguna URL con el token: {token}"}
                    ),
                },
            },
        )

    url_doc.access_count += 1
    url_doc.last_accessed = date.today()
    await url_doc.save()

    return RedirectResponse(url=url_doc.original)
