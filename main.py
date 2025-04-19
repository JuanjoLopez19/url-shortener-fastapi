import logging
import os
import traceback
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException

from src.app import settings
from src.app.api import templates
from src.app.api.index import router
from src.app.database.mongo import mongodb

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        if not settings.is_vercel:
            await mongodb.initialize()
        yield
        if not settings.is_vercel and mongodb._initialized:
            await mongodb.close()
    except Exception as e:
        logger.error(
            f"Error in application lifecycle: {str(e)}\n{traceback.format_exc()}"
        )
        raise


# Exception handlers
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP error: {exc.status_code} - {exc.detail}")
    return templates.TemplateResponse(
        "error.html",
        {
            "request": request,
            "message": str(exc.detail),
            "error": {"status": exc.status_code, "stack": "HTTP Error"},
        },
        status_code=exc.status_code,
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_detail = str(exc)
    logger.error(f"Validation error: {error_detail}")
    return templates.TemplateResponse(
        "error.html",
        {
            "request": request,
            "message": "Error de validación",
            "error": {"status": 422, "stack": error_detail},
        },
        status_code=422,
    )


async def general_exception_handler(request: Request, exc: Exception):
    error_detail = traceback.format_exc()
    logger.error(f"Unhandled exception: {str(exc)}\n{error_detail}")
    return templates.TemplateResponse(
        "error.html",
        {
            "request": request,
            "message": "Error interno del servidor",
            "error": {"status": 500, "stack": error_detail},
        },
        status_code=500,
    )


app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None)

# Add exception handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

static_dir = os.path.join(
    os.path.dirname(__file__),
    "src",
    "static",
)

app.include_router(router)

app.mount("/static", StaticFiles(directory=static_dir), name="static")


def main():
    import uvicorn

    if settings.development:
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
