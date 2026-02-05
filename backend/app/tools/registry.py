"""Tool registry for managing available tools."""

from typing import Any

from app.tools.base import BaseTool


class ToolRegistry:
    """Registry for managing and accessing tools."""

    def __init__(self) -> None:
        """Initialize the registry."""
        self._tools: dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        """Register a tool."""
        self._tools[tool.name] = tool

    def get(self, name: str) -> BaseTool | None:
        """Get a tool by name."""
        return self._tools.get(name)

    def get_all(self) -> list[BaseTool]:
        """Get all registered tools."""
        return list(self._tools.values())

    def get_openai_tools(self) -> list[dict[str, Any]]:
        """Get all tools in OpenAI format."""
        return [tool.to_openai_format() for tool in self._tools.values()]

    async def execute(self, name: str, **kwargs: Any) -> str:
        """Execute a tool by name."""
        tool = self.get(name)
        if tool is None:
            return f"Error: Tool '{name}' not found"
        try:
            return await tool.execute(**kwargs)
        except Exception as e:
            return f"Error executing tool '{name}': {str(e)}"


# Global registry instance
tool_registry = ToolRegistry()
