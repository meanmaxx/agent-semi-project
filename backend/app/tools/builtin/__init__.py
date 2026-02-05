"""Built-in tools module."""

from app.tools.builtin.budget import get_all_budget_tools
from app.tools.registry import tool_registry


def register_all_tools() -> None:
    """Register all built-in tools to the global registry."""
    for tool in get_all_budget_tools():
        tool_registry.register(tool)


# Auto-register on import
register_all_tools()
