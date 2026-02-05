"""vLLM client for making API calls."""

import logging
from typing import Any

import httpx

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class VLLMClient:
    """Client for vLLM OpenAI-compatible API."""

    def __init__(
        self,
        base_url: str | None = None,
        model: str | None = None,
    ) -> None:
        """Initialize the client."""
        self.base_url = (base_url or settings.vllm_base_url).rstrip("/")
        self.model = model or settings.vllm_model
        self.client = httpx.AsyncClient(timeout=120.0)

    async def chat_completion(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> dict[str, Any]:
        """Make a chat completion request."""
        url = f"{self.base_url}/v1/chat/completions"

        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"

        logger.debug(f"Sending request to {url}")
        logger.debug(f"Payload: {payload}")

        response = await self.client.post(url, json=payload)
        response.raise_for_status()

        result = response.json()
        logger.debug(f"Response: {result}")

        return result

    async def close(self) -> None:
        """Close the client."""
        await self.client.aclose()


# Global client instance
vllm_client = VLLMClient()
