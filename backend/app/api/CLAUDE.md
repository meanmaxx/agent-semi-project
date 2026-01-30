# API Layer

## 개요
FastAPI 라우터를 통한 REST API 및 WebSocket 엔드포인트 정의입니다.

## 디렉토리 구조
```
api/
├── __init__.py
└── v1/
    ├── __init__.py      # 라우터 통합
    ├── chat.py          # 채팅 엔드포인트
    ├── tools.py         # 도구 관련 엔드포인트
    └── health.py        # 헬스체크
```

## API 엔드포인트

### Chat API
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/chat` | 단일 메시지 전송 |
| POST | `/api/v1/chat/stream` | 스트리밍 응답 |
| GET | `/api/v1/chat/history/{conversation_id}` | 대화 기록 조회 |

### Tools API
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/tools` | 사용 가능한 도구 목록 |
| GET | `/api/v1/tools/{tool_name}` | 특정 도구 상세 정보 |

### Health API
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/health` | 서버 상태 확인 |
| GET | `/api/v1/health/llm` | vLLM 연결 상태 |

## 라우터 구성

### v1/__init__.py
```python
from fastapi import APIRouter

from .chat import router as chat_router
from .tools import router as tools_router
from .health import router as health_router

router = APIRouter()
router.include_router(chat_router, prefix="/chat", tags=["chat"])
router.include_router(tools_router, prefix="/tools", tags=["tools"])
router.include_router(health_router, prefix="/health", tags=["health"])
```

### 엔드포인트 예시
```python
# v1/chat.py
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.agent.executor import AgentExecutor
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter()

@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    executor: AgentExecutor = Depends(get_executor),
) -> ChatResponse:
    """Send a message and get agent response."""
    result = await executor.run(
        message=request.content,
        conversation_id=request.conversation_id,
    )
    return ChatResponse(
        content=result.content,
        tool_calls=result.tool_calls,
    )

@router.post("/stream")
async def chat_stream(
    request: ChatRequest,
    executor: AgentExecutor = Depends(get_executor),
):
    """Send a message and get streaming response."""
    async def generate():
        async for chunk in executor.run_stream(
            message=request.content,
            conversation_id=request.conversation_id,
        ):
            yield f"data: {chunk.model_dump_json()}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
    )
```

## WebSocket 패턴

### 실시간 채팅
```python
# v1/chat.py
from fastapi import WebSocket, WebSocketDisconnect

@router.websocket("/ws/{conversation_id}")
async def websocket_chat(
    websocket: WebSocket,
    conversation_id: str,
    executor: AgentExecutor = Depends(get_executor),
):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_json()

            async for chunk in executor.run_stream(
                message=data["content"],
                conversation_id=conversation_id,
            ):
                await websocket.send_json(chunk.model_dump())

            await websocket.send_json({"type": "done"})
    except WebSocketDisconnect:
        pass
```

## 의존성 주입

### Executor 의존성
```python
# v1/dependencies.py
from app.agent.executor import AgentExecutor
from app.llm.client import VLLMClient
from app.tools.registry import ToolRegistry

def get_executor() -> AgentExecutor:
    client = VLLMClient()
    registry = ToolRegistry()
    return AgentExecutor(client=client, registry=registry)
```

## 에러 응답 형식

```python
# schemas/error.py
from pydantic import BaseModel

class ErrorResponse(BaseModel):
    detail: str
    code: str | None = None
```

### HTTP 상태 코드
- `200`: 성공
- `400`: 잘못된 요청
- `500`: 서버 내부 오류
- `502`: vLLM 서버 오류

## 코딩 규칙

### 라우터 데코레이터
- `response_model` 명시 권장
- `tags` 설정으로 Swagger 문서 그룹화
- docstring으로 API 설명 추가

### 요청 검증
- Pydantic 스키마로 자동 검증
- 추가 검증은 `Depends`로 처리
