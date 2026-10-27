"""LangChain client for the OpenAI API."""

from fastapi import HTTPException, status
from langchain_openai import ChatOpenAI

from app.core.config import settings


def get_chat_model() -> ChatOpenAI:
    """Build an OpenAI chat model from the server-side environment."""
    if not settings.openai_api_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="OPENAI_API_KEY is not configured on the server.",
        )

    return ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
    )
