# Backend - FastAPI

## 개요
vLLM 기반 Tool-using Agent의 백엔드 서버입니다.

## 기술 스택
- Python 3.11+
- FastAPI
- Pydantic v2
- httpx (비동기 HTTP 클라이언트)
- uvicorn (ASGI 서버)

## 디렉토리 구조
```
app/
├── main.py           # FastAPI 앱 진입점
├── config.py         # 설정 관리
├── api/              # API 라우터
│   └── v1/           # v1 API 엔드포인트
├── agent/            # 에이전트 코어 로직
│   ├── executor.py   # 에이전트 실행기
│   ├── memory.py     # 대화 메모리
│   └── prompts/      # 프롬프트 템플릿
├── tools/            # 도구 정의
│   ├── base.py       # BaseTool 클래스
│   ├── registry.py   # 도구 레지스트리
│   └── builtin/      # 내장 도구들
├── llm/              # vLLM 연동
│   ├── client.py     # vLLM 클라이언트
│   └── parser.py     # 응답 파서
├── models/           # 데이터베이스 모델 (필요시)
├── schemas/          # Pydantic 스키마
└── services/         # 비즈니스 로직
```

## FastAPI 앱 구조

### main.py
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import router as api_router
from app.config import settings

app = FastAPI(
    title="vLLM Agent Service",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")
```

### config.py
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    vllm_base_url: str = "http://localhost:8000"
    vllm_model: str = "Qwen/Qwen2.5-7B-Instruct"
    allowed_origins: list[str] = ["http://localhost:5173"]

    class Config:
        env_file = ".env"

settings = Settings()
```

## 비동기 패턴

### 기본 비동기 엔드포인트
```python
@router.post("/chat")
async def chat(request: ChatRequest) -> ChatResponse:
    result = await agent_executor.run(request.content)
    return ChatResponse(content=result)
```

### 스트리밍 응답
```python
from fastapi.responses import StreamingResponse

@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    async def generate():
        async for chunk in agent_executor.run_stream(request.content):
            yield f"data: {chunk}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )
```

## Pydantic 스키마

### 요청/응답 스키마
```python
# schemas/chat.py
from pydantic import BaseModel

class ChatRequest(BaseModel):
    content: str
    conversation_id: str | None = None

class ChatResponse(BaseModel):
    content: str
    tool_calls: list[ToolCallResult] | None = None
```

## 에러 핸들링

```python
from fastapi import HTTPException

@router.post("/chat")
async def chat(request: ChatRequest):
    try:
        result = await agent_executor.run(request.content)
        return ChatResponse(content=result)
    except LLMError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except ToolExecutionError as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## 코딩 규칙

### 타입 힌트
- 모든 함수에 타입 힌트 필수
- `list`, `dict` 등 내장 타입 사용 (Python 3.9+ 스타일)

### 명명 규칙
- 함수/변수: snake_case
- 클래스: PascalCase
- 상수: UPPER_SNAKE_CASE

### Import 순서
1. 표준 라이브러리
2. 서드파티 라이브러리
3. 로컬 모듈

## 실행 방법
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8080
```

## 테스트
```bash
pytest tests/ -v
```
