import json
import logging
import traceback
from datetime import date

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from src.app.api import templates
from src.app.database.mongo import ensure_db_connected
from src.app.database.schemas.url import UrlSchema

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    try:
        await ensure_db_connected()

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

        url_doc = await UrlSchema.find_one({"shortened": token})

        if not url_doc:
            return templates.TemplateResponse(
                "error.html",
                context={
                    "request": request,
                    "message": "URL no encontrada",
                    "error": {
                        "status": 404,
                        "stack": json.dumps(
                            {
                                "message": f"No se encontró ninguna URL con el token: {token}"
                            }
                        ),
                    },
                },
            )

        url_doc.access_count += 1
        url_doc.last_accessed = date.today()
        await url_doc.save()

        logger.info(f"Redirecting to: {url_doc.original}")
        return RedirectResponse(url=url_doc.original)
    except Exception as e:
        error_details = traceback.format_exc()
        logger.error(f"Error processing request: {str(e)}\n{error_details}")

        return templates.TemplateResponse(
            "error.html",
            context={
                "request": request,
                "message": "Error interno del servidor",
                "error": {
                    "status": 500,
                    "stack": error_details,
                },
            },
        )
