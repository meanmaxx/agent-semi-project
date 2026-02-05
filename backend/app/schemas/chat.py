"""Chat-related Pydantic schemas."""

from pydantic import BaseModel


class ChatRequest(BaseModel):
    """Schema for chat request."""

    content: str
    conversation_id: str | None = None


class ChatResponse(BaseModel):
    """Schema for chat response."""

    content: str
    conversation_id: str | None = None
