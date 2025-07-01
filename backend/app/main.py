# Main FastAPI application entry point and configuration
import os
import pathlib
import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import (get_swagger_ui_html,
                                  get_swagger_ui_oauth2_redirect_html)
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles


from app.api.v1.routers import api_router
from app.core.config import settings
from app.utils.log import LOGGING_CONFIG, set_app_logger

logger = set_app_logger("app")

backend_root = pathlib.Path(__file__).parent.parent.resolve()
logger.info(f"Root path: {backend_root}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Async context manager for application lifecycle events"""
    logger.info("Starting up application")
    yield  # This is where the application runs
    logger.info("Shutting down application")


def create_app() -> FastAPI:
    """Factory function to create and configure the FastAPI application"""
    fastapp = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url="/api/v1/openapi.json",
        docs_url=None,
        redoc_url=None,
        lifespan=lifespan,
    )

    if settings.ENVIRONMENT == "dev":
        from scripts.migrate_db import run_migrations

        run_migrations()

    fastapp.include_router(api_router, prefix="/api/v1")
    return fastapp


fastapp = create_app()

# Setup CORS - Configure cross-origin resource sharing
# In production, only allow specified origins
# In development, allow all origins for easier testing
fastapp.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.ALLOWED_ORIGINS]
    if settings.ENVIRONMENT == "production"
    else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


STATIC_DIR = os.path.join(backend_root, "static")


@fastapp.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=fastapp.openapi_url,
        title=fastapp.title + " - Swagger UI",
        oauth2_redirect_url=fastapp.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/swagger/swagger-ui-bundle.js",
        swagger_css_url="/swagger/swagger-ui.css",
    )


fastapp.mount("/static", StaticFiles(directory=STATIC_DIR, html=True), name="static")

SWAGGER_DIR = os.path.join(backend_root, "swagger")
fastapp.mount("/swagger", StaticFiles(directory=SWAGGER_DIR, html=True), name="swagger")


@fastapp.get(fastapp.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@fastapp.get("/")
async def root():
    return RedirectResponse(url="/static/index.html")


# Start the FastAPI application using uvicorn
# Auto-reloads in development mode based on settings
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:fastapp",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGING_CONFIG,
        reload=settings.ENVIRONMENT == "dev",
    )
