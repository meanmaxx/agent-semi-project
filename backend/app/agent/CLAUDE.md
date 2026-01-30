# Agent Core

## 개요
에이전트의 핵심 실행 로직, 메모리 관리, 프롬프트 템플릿을 담당합니다.

## 디렉토리 구조
```
agent/
├── __init__.py
├── executor.py      # 에이전트 실행기
├── memory.py        # 대화 메모리 관리
└── prompts/         # 프롬프트 템플릿
    ├── __init__.py
    └── system.py    # 시스템 프롬프트
```

## 에이전트 실행 흐름

```
1. 사용자 메시지 수신
2. 대화 히스토리 로드 (Memory)
3. vLLM에 요청 (with tools)
4. 응답 분석
   ├─ Tool Call 있음 → 도구 실행 → 결과와 함께 3번으로
   └─ Tool Call 없음 → 최종 응답 반환
5. 대화 히스토리 저장
```

## AgentExecutor

### 기본 구조
```python
# executor.py
from app.llm.client import VLLMClient
from app.tools.registry import ToolRegistry
from app.agent.memory import ConversationMemory

class AgentExecutor:
    def __init__(
        self,
        client: VLLMClient,
        registry: ToolRegistry,
        max_iterations: int = 10,
    ):
        self.client = client
        self.registry = registry
        self.max_iterations = max_iterations
        self.memory = ConversationMemory()

    async def run(
        self,
        message: str,
        conversation_id: str | None = None,
    ) -> AgentResult:
        """Execute agent with the given message."""
        messages = self.memory.get_messages(conversation_id)
        messages.append({"role": "user", "content": message})

        tools = self.registry.get_tool_definitions()

        for _ in range(self.max_iterations):
            response = await self.client.chat(
                messages=messages,
                tools=tools,
            )

            if not response.tool_calls:
                # No more tool calls, return final response
                self.memory.save_messages(conversation_id, messages)
                return AgentResult(content=response.content)

            # Execute tool calls
            messages.append(response.to_message())

            for tool_call in response.tool_calls:
                result = await self._execute_tool(tool_call)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                })

        raise MaxIterationsExceeded()

    async def _execute_tool(self, tool_call: ToolCall) -> str:
        """Execute a single tool call."""
        tool = self.registry.get_tool(tool_call.name)
        return await tool.execute(**tool_call.arguments)
```

### 스트리밍 실행
```python
async def run_stream(
    self,
    message: str,
    conversation_id: str | None = None,
) -> AsyncGenerator[StreamChunk, None]:
    """Execute agent with streaming response."""
    # Similar to run() but yields chunks
    async for chunk in self.client.chat_stream(...):
        yield StreamChunk(
            type="content" if chunk.content else "tool_call",
            data=chunk,
        )
```

## ConversationMemory

### 인터페이스
```python
# memory.py
from abc import ABC, abstractmethod

class BaseMemory(ABC):
    @abstractmethod
    def get_messages(self, conversation_id: str | None) -> list[dict]:
        """Retrieve conversation history."""
        pass

    @abstractmethod
    def save_messages(
        self,
        conversation_id: str | None,
        messages: list[dict],
    ) -> None:
        """Save conversation history."""
        pass

    @abstractmethod
    def clear(self, conversation_id: str | None) -> None:
        """Clear conversation history."""
        pass
```

### 인메모리 구현
```python
class ConversationMemory(BaseMemory):
    def __init__(self, max_messages: int = 50):
        self._storage: dict[str, list[dict]] = {}
        self.max_messages = max_messages

    def get_messages(self, conversation_id: str | None) -> list[dict]:
        if not conversation_id:
            return []
        return self._storage.get(conversation_id, [])[-self.max_messages:]

    def save_messages(
        self,
        conversation_id: str | None,
        messages: list[dict],
    ) -> None:
        if conversation_id:
            self._storage[conversation_id] = messages[-self.max_messages:]
```

## 프롬프트 관리

### 시스템 프롬프트
```python
# prompts/system.py
SYSTEM_PROMPT = """You are a helpful AI assistant with access to various tools.

When you need to perform actions or get information, use the available tools.
Always explain what you're doing and why.

Guidelines:
- Use tools when they can help answer the user's question
- Provide clear, concise responses
- If a tool fails, explain the error and suggest alternatives
"""

def get_system_prompt(tools: list[dict]) -> str:
    """Generate system prompt with tool descriptions."""
    tool_list = "\n".join(
        f"- {t['function']['name']}: {t['function']['description']}"
        for t in tools
    )
    return f"{SYSTEM_PROMPT}\n\nAvailable tools:\n{tool_list}"
```

## 데이터 모델

```python
# schemas/agent.py
from pydantic import BaseModel

class AgentResult(BaseModel):
    content: str
    tool_calls: list[ToolCallResult] | None = None

class ToolCallResult(BaseModel):
    tool_name: str
    arguments: dict
    result: str

class StreamChunk(BaseModel):
    type: Literal["content", "tool_call", "tool_result"]
    data: dict
```

## 에러 처리

```python
# exceptions.py
class AgentError(Exception):
    """Base agent exception."""
    pass

class MaxIterationsExceeded(AgentError):
    """Raised when agent exceeds max iterations."""
    pass

class ToolExecutionError(AgentError):
    """Raised when tool execution fails."""
    pass
```

## 코딩 규칙

### 비동기 패턴
- 모든 I/O 작업은 `async/await` 사용
- `AsyncGenerator`로 스트리밍 구현

### 의존성 주입
- 생성자를 통한 의존성 주입
- 테스트 용이성 확보

### 로깅
```python
import logging

logger = logging.getLogger(__name__)

async def run(self, message: str, ...):
    logger.info(f"Starting agent execution: {message[:50]}...")
```
