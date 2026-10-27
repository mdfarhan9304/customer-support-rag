"""FastAPI entry point."""

from fastapi import FastAPI

from app.api.routes import router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="FastAPI service for LangGraph-powered workflows.",
)

app.include_router(router)


@app.get("/", tags=["system"])
async def root() -> dict[str, str]:
    """Provide a small service discovery response."""
    return {"message": f"Welcome to {settings.app_name}", "docs": "/docs"}
