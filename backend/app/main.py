"""FastAPI application entry point."""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import router as api_router
from app.config import get_settings
from app.db.database import init_db

# Import to trigger tool registration
import app.tools.builtin  # noqa: F401

settings = get_settings()

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Budget Chatbot API",
    description="vLLM Tool-using Agent for Budget Management",
    version="1.0.0",
)

# CORS middleware
allowed_origins = [origin.strip() for origin in settings.allowed_origins.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event() -> None:
    """Initialize application on startup."""
    logger.info("Starting Budget Chatbot API...")
    init_db()
    logger.info("Database initialized")
    logger.info(f"vLLM URL: {settings.vllm_base_url}")
    logger.info(f"vLLM Model: {settings.vllm_model}")


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint."""
    return {
        "message": "Budget Chatbot API",
        "docs": "/docs",
        "health": "/api/v1/health",
    }
