"""Conversation memory management."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Message:
    """Chat message."""

    role: str
    content: str | None
    tool_calls: list[dict[str, Any]] | None = None
    tool_call_id: str | None = None
    name: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for API calls."""
        msg: dict[str, Any] = {"role": self.role}

        if self.content is not None:
            msg["content"] = self.content

        if self.tool_calls:
            msg["tool_calls"] = self.tool_calls

        if self.tool_call_id:
            msg["tool_call_id"] = self.tool_call_id

        if self.name:
            msg["name"] = self.name

        return msg


@dataclass
class ConversationMemory:
    """Manages conversation history."""

    system_prompt: str
    messages: list[Message] = field(default_factory=list)
    max_messages: int = 50

    def add_user_message(self, content: str) -> None:
        """Add a user message."""
        self.messages.append(Message(role="user", content=content))
        self._trim_if_needed()

    def add_assistant_message(
        self,
        content: str | None,
        tool_calls: list[dict[str, Any]] | None = None,
    ) -> None:
        """Add an assistant message."""
        self.messages.append(
            Message(role="assistant", content=content, tool_calls=tool_calls)
        )
        self._trim_if_needed()

    def add_tool_result(
        self,
        tool_call_id: str,
        name: str,
        content: str,
    ) -> None:
        """Add a tool result message."""
        self.messages.append(
            Message(
                role="tool",
                content=content,
                tool_call_id=tool_call_id,
                name=name,
            )
        )
        self._trim_if_needed()

    def get_messages(self) -> list[dict[str, Any]]:
        """Get all messages for API call."""
        result = [{"role": "system", "content": self.system_prompt}]
        result.extend(msg.to_dict() for msg in self.messages)
        return result

    def clear(self) -> None:
        """Clear all messages except system prompt."""
        self.messages = []

    def _trim_if_needed(self) -> None:
        """Trim old messages if exceeding max."""
        if len(self.messages) > self.max_messages:
            # Keep last max_messages
            self.messages = self.messages[-self.max_messages :]
