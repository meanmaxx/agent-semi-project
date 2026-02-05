"""Chat endpoint."""

import logging
import uuid

from fastapi import APIRouter, HTTPException

from app.agent.executor import AgentExecutor
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter()
logger = logging.getLogger(__name__)

# Store agent executors by conversation_id for session continuity
_executors: dict[str, AgentExecutor] = {}


def get_executor(conversation_id: str | None) -> tuple[AgentExecutor, str]:
    """Get or create an agent executor for the conversation."""
    if conversation_id and conversation_id in _executors:
        return _executors[conversation_id], conversation_id

    # Create new executor
    new_id = conversation_id or str(uuid.uuid4())
    executor = AgentExecutor()
    _executors[new_id] = executor
    return executor, new_id


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """Process a chat message."""
    logger.info(f"Received chat request: {request.content[:100]}...")

    try:
        executor, conversation_id = get_executor(request.conversation_id)
        response = await executor.run(request.content)

        return ChatResponse(
            content=response,
            conversation_id=conversation_id,
        )
    except Exception as e:
        logger.error(f"Error processing chat: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error processing message: {str(e)}",
        )


@router.post("/chat/reset")
async def reset_chat(conversation_id: str | None = None) -> dict[str, str]:
    """Reset a conversation."""
    if conversation_id and conversation_id in _executors:
        _executors[conversation_id].reset()
        return {"status": "reset", "conversation_id": conversation_id}

    return {"status": "no_conversation_found"}
