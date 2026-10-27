"""Base API routes."""

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.core.config import settings
from app.services.openai import get_chat_model

router = APIRouter(tags=["system"])


class ChatRequest(BaseModel):
    """The text passed to the configured OpenAI model."""

    message: str = Field(min_length=1, max_length=16_000)


class ChatResponse(BaseModel):
    """A normalized chat response."""

    model: str
    message: str


@router.get("/health")
async def health_check() -> dict[str, str]:
    """Return application liveness information."""
    return {
        "status": "ok",
        "environment": settings.environment,
        "version": settings.version,
    }


@router.post("/chat", response_model=ChatResponse, tags=["chat"])
async def chat(request: ChatRequest) -> ChatResponse:
    """Generate a response with the configured LangChain OpenAI model."""
    model = get_chat_model()
    response = await model.ainvoke(request.message)
    content = response.content
    return ChatResponse(
        model=settings.openai_model,
        message=content if isinstance(content, str) else str(content),
    )
