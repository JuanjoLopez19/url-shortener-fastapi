from fastapi import APIRouter

from src.app.api.views.routes import router as views_router

router = APIRouter()


router.include_router(views_router)
