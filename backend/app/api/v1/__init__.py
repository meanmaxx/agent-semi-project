"""API v1 router."""

from fastapi import APIRouter

from app.api.v1.chat import router as chat_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.health import router as health_router

router = APIRouter()
router.include_router(chat_router, tags=["chat"])
router.include_router(dashboard_router, prefix="/dashboard", tags=["dashboard"])
router.include_router(health_router, tags=["health"])
