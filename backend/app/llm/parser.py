"""Response parser for vLLM responses."""

import json
import logging
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class ToolCall:
    """Parsed tool call."""

    id: str
    name: str
    arguments: dict[str, Any]


@dataclass
class ParsedResponse:
    """Parsed LLM response."""

    content: str | None
    tool_calls: list[ToolCall]
    finish_reason: str


def parse_response(response: dict[str, Any]) -> ParsedResponse:
    """Parse vLLM response into structured format."""
    choices = response.get("choices", [])
    if not choices:
        return ParsedResponse(content=None, tool_calls=[], finish_reason="error")

    choice = choices[0]
    message = choice.get("message", {})
    finish_reason = choice.get("finish_reason", "stop")

    content = message.get("content")
    tool_calls_raw = message.get("tool_calls", [])

    tool_calls = []
    for tc in tool_calls_raw:
        try:
            function = tc.get("function", {})
            arguments_str = function.get("arguments", "{}")

            # Parse arguments JSON
            if isinstance(arguments_str, str):
                arguments = json.loads(arguments_str)
            else:
                arguments = arguments_str

            tool_calls.append(
                ToolCall(
                    id=tc.get("id", ""),
                    name=function.get("name", ""),
                    arguments=arguments,
                )
            )
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse tool call arguments: {e}")
            continue

    return ParsedResponse(
        content=content,
        tool_calls=tool_calls,
        finish_reason=finish_reason,
    )
