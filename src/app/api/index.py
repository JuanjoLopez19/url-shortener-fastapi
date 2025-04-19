from fastapi import APIRouter

from src.app.api.endpoints.routes import router as endpoints_router
from src.app.api.views.routes import router as views_router

router = APIRouter()


router.include_router(views_router)
router.include_router(endpoints_router, prefix="/api/v1")
