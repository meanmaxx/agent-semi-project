# Tools Module

## 개요
에이전트가 사용할 수 있는 도구(Tool)를 정의하고 관리합니다.

## 디렉토리 구조
```
tools/
├── __init__.py
├── base.py          # BaseTool 추상 클래스
├── registry.py      # 도구 레지스트리
└── builtin/         # 내장 도구들
    ├── __init__.py
    ├── calculator.py
    ├── web_search.py
    └── file_reader.py
```

## BaseTool 클래스

### 정의
```python
# base.py
from abc import ABC, abstractmethod
from pydantic import BaseModel

class ToolParameter(BaseModel):
    name: str
    type: str
    description: str
    required: bool = True
    enum: list[str] | None = None

class BaseTool(ABC):
    """Base class for all tools."""

    name: str
    description: str
    parameters: list[ToolParameter]

    @abstractmethod
    async def execute(self, **kwargs) -> str:
        """Execute the tool with given arguments."""
        pass

    def to_openai_tool(self) -> dict:
        """Convert to OpenAI tool format."""
        properties = {}
        required = []

        for param in self.parameters:
            properties[param.name] = {
                "type": param.type,
                "description": param.description,
            }
            if param.enum:
                properties[param.name]["enum"] = param.enum
            if param.required:
                required.append(param.name)

        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required,
                },
            },
        }
```

## 도구 구현 예시

### Calculator Tool
```python
# builtin/calculator.py
from app.tools.base import BaseTool, ToolParameter

class CalculatorTool(BaseTool):
    name = "calculator"
    description = "Perform basic mathematical calculations"
    parameters = [
        ToolParameter(
            name="expression",
            type="string",
            description="Mathematical expression to evaluate (e.g., '2 + 2')",
        ),
    ]

    async def execute(self, expression: str) -> str:
        try:
            # Safe evaluation (only allow basic math)
            allowed_chars = set("0123456789+-*/.() ")
            if not all(c in allowed_chars for c in expression):
                return "Error: Invalid characters in expression"

            result = eval(expression)
            return str(result)
        except Exception as e:
            return f"Error: {str(e)}"
```

### Web Search Tool
```python
# builtin/web_search.py
import httpx
from app.tools.base import BaseTool, ToolParameter

class WebSearchTool(BaseTool):
    name = "web_search"
    description = "Search the web for information"
    parameters = [
        ToolParameter(
            name="query",
            type="string",
            description="Search query",
        ),
        ToolParameter(
            name="num_results",
            type="integer",
            description="Number of results to return",
            required=False,
        ),
    ]

    async def execute(
        self,
        query: str,
        num_results: int = 5,
    ) -> str:
        async with httpx.AsyncClient() as client:
            # Implement actual search API call
            response = await client.get(
                "https://api.search.com/search",
                params={"q": query, "limit": num_results},
            )
            return response.text
```

## ToolRegistry

### 레지스트리 구현
```python
# registry.py
from typing import Type
from app.tools.base import BaseTool

class ToolRegistry:
    """Registry for managing available tools."""

    def __init__(self):
        self._tools: dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        """Register a tool."""
        self._tools[tool.name] = tool

    def register_class(self, tool_class: Type[BaseTool]) -> None:
        """Register a tool class (instantiates it)."""
        tool = tool_class()
        self.register(tool)

    def get_tool(self, name: str) -> BaseTool:
        """Get a tool by name."""
        if name not in self._tools:
            raise ToolNotFoundError(f"Tool not found: {name}")
        return self._tools[name]

    def get_tool_definitions(self) -> list[dict]:
        """Get all tool definitions in OpenAI format."""
        return [tool.to_openai_tool() for tool in self._tools.values()]

    def list_tools(self) -> list[str]:
        """List all registered tool names."""
        return list(self._tools.keys())
```

### 기본 레지스트리 설정
```python
# __init__.py
from app.tools.registry import ToolRegistry
from app.tools.builtin.calculator import CalculatorTool
from app.tools.builtin.web_search import WebSearchTool

def create_default_registry() -> ToolRegistry:
    """Create registry with default tools."""
    registry = ToolRegistry()
    registry.register_class(CalculatorTool)
    registry.register_class(WebSearchTool)
    return registry
```

## 도구 정의 JSON 형식

`shared/constants/tool_definitions.json`과 동기화:
```json
{
  "tools": [
    {
      "name": "calculator",
      "description": "Perform basic mathematical calculations",
      "parameters": [
        {
          "name": "expression",
          "type": "string",
          "description": "Mathematical expression to evaluate",
          "required": true
        }
      ]
    }
  ]
}
```

## 새 도구 추가 방법

1. `builtin/` 디렉토리에 새 파일 생성
2. `BaseTool` 상속하여 클래스 정의
3. `name`, `description`, `parameters` 설정
4. `execute()` 메서드 구현
5. `__init__.py`에서 레지스트리에 등록

### 체크리스트
- [ ] 도구 이름은 snake_case
- [ ] 설명은 명확하고 간결하게
- [ ] 파라미터 타입은 JSON Schema 타입
- [ ] 에러 처리 구현
- [ ] 비동기 I/O 사용

## 에러 처리

```python
# exceptions.py
class ToolError(Exception):
    """Base tool exception."""
    pass

class ToolNotFoundError(ToolError):
    """Raised when tool is not found."""
    pass

class ToolExecutionError(ToolError):
    """Raised when tool execution fails."""
    pass
```
