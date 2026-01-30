# LLM Module (vLLM Integration)

## 개요
vLLM 서버와의 통신을 담당하는 클라이언트 모듈입니다.

## 디렉토리 구조
```
llm/
├── __init__.py
├── client.py        # vLLM HTTP 클라이언트
└── parser.py        # Tool Call 응답 파서
```

## vLLM Tool Calling

### OpenAI-compatible API 형식
vLLM은 OpenAI 호환 API를 제공합니다. Tool Calling을 사용하려면 서버 시작 시 특정 플래그가 필요합니다.

### 요청 형식
```python
{
    "model": "Qwen/Qwen2.5-7B-Instruct",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is 2 + 2?"}
    ],
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "calculator",
                "description": "Perform calculations",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description": "Math expression"
                        }
                    },
                    "required": ["expression"]
                }
            }
        }
    ],
    "tool_choice": "auto"
}
```

### 응답 형식 (Tool Call 포함)
```python
{
    "choices": [
        {
            "message": {
                "role": "assistant",
                "content": null,
                "tool_calls": [
                    {
                        "id": "call_abc123",
                        "type": "function",
                        "function": {
                            "name": "calculator",
                            "arguments": "{\"expression\": \"2 + 2\"}"
                        }
                    }
                ]
            }
        }
    ]
}
```

## VLLMClient

### 구현
```python
# client.py
import httpx
from pydantic import BaseModel

from app.config import settings

class ToolCall(BaseModel):
    id: str
    name: str
    arguments: dict

class LLMResponse(BaseModel):
    content: str | None
    tool_calls: list[ToolCall] | None

    def to_message(self) -> dict:
        """Convert to message format for history."""
        msg = {"role": "assistant"}
        if self.content:
            msg["content"] = self.content
        if self.tool_calls:
            msg["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.name,
                        "arguments": json.dumps(tc.arguments),
                    },
                }
                for tc in self.tool_calls
            ]
        return msg

class VLLMClient:
    def __init__(
        self,
        base_url: str = settings.vllm_base_url,
        model: str = settings.vllm_model,
        timeout: float = 60.0,
    ):
        self.base_url = base_url
        self.model = model
        self.timeout = timeout
        self._client = httpx.AsyncClient(timeout=timeout)

    async def chat(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
        tool_choice: str = "auto",
        temperature: float = 0.7,
    ) -> LLMResponse:
        """Send chat completion request to vLLM."""
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }

        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = tool_choice

        response = await self._client.post(
            f"{self.base_url}/v1/chat/completions",
            json=payload,
        )
        response.raise_for_status()

        return self._parse_response(response.json())

    def _parse_response(self, data: dict) -> LLMResponse:
        """Parse vLLM response."""
        message = data["choices"][0]["message"]

        tool_calls = None
        if "tool_calls" in message and message["tool_calls"]:
            tool_calls = [
                ToolCall(
                    id=tc["id"],
                    name=tc["function"]["name"],
                    arguments=json.loads(tc["function"]["arguments"]),
                )
                for tc in message["tool_calls"]
            ]

        return LLMResponse(
            content=message.get("content"),
            tool_calls=tool_calls,
        )
```

### 스트리밍 지원
```python
async def chat_stream(
    self,
    messages: list[dict],
    tools: list[dict] | None = None,
) -> AsyncGenerator[dict, None]:
    """Stream chat completion from vLLM."""
    payload = {
        "model": self.model,
        "messages": messages,
        "stream": True,
    }

    if tools:
        payload["tools"] = tools

    async with self._client.stream(
        "POST",
        f"{self.base_url}/v1/chat/completions",
        json=payload,
    ) as response:
        async for line in response.aiter_lines():
            if line.startswith("data: "):
                data = line[6:]
                if data == "[DONE]":
                    break
                yield json.loads(data)
```

## Tool Call 응답 파서

### Hermes 파서
```python
# parser.py
import re
import json

def parse_hermes_tool_call(content: str) -> list[dict] | None:
    """Parse Hermes-style tool calls from content.

    Hermes format:
    <tool_call>
    {"name": "calculator", "arguments": {"expression": "2+2"}}
    </tool_call>
    """
    pattern = r"<tool_call>\s*(.*?)\s*</tool_call>"
    matches = re.findall(pattern, content, re.DOTALL)

    if not matches:
        return None

    tool_calls = []
    for match in matches:
        try:
            data = json.loads(match)
            tool_calls.append({
                "id": f"call_{uuid.uuid4().hex[:8]}",
                "name": data["name"],
                "arguments": data.get("arguments", {}),
            })
        except json.JSONDecodeError:
            continue

    return tool_calls if tool_calls else None
```

## 에러 처리

```python
# exceptions.py
class LLMError(Exception):
    """Base LLM exception."""
    pass

class LLMConnectionError(LLMError):
    """Raised when cannot connect to vLLM."""
    pass

class LLMResponseError(LLMError):
    """Raised when vLLM returns an error."""
    pass
```

### 재시도 로직
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
)
async def chat_with_retry(self, messages, tools=None):
    return await self.chat(messages, tools)
```

## 코딩 규칙

### HTTP 클라이언트
- `httpx.AsyncClient` 사용 (비동기)
- 타임아웃 설정 필수
- 연결 풀 재사용

### 응답 파싱
- Pydantic 모델로 검증
- JSON 파싱 에러 처리
- Tool Call 인자는 항상 dict로 변환
