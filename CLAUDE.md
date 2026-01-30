# vLLM Tool-using Agent Service

## 프로젝트 개요
vLLM과 Python을 사용한 도구 사용(Tool-using) 에이전트 서비스입니다.

## 기술 스택
- **Frontend**: React + TypeScript + Vite
- **Backend**: FastAPI (Python 3.11+)
- **LLM**: vLLM (OpenAI-compatible API)
- **Agent Type**: Tool-using Agent

## 아키텍처

### 에이전트 실행 흐름
```
User Request → AgentExecutor → vLLM (Tool Calling)
                    ↓
              Tool Call 있음?
                 ↓ Yes
              도구 실행 → 결과를 vLLM에 전달 (반복)
                 ↓ No
              최종 응답 반환
```

### 핵심 컴포넌트
- `backend/app/agent/`: 에이전트 코어 로직 (실행기, 메모리)
- `backend/app/tools/`: 도구 정의 및 레지스트리
- `backend/app/llm/`: vLLM 클라이언트 및 응답 파서
- `frontend/`: React 기반 채팅 인터페이스

## 실행 방법

### 개발 환경 설정
```bash
# 환경 변수 설정
cp .env.example .env

# 전체 서비스 실행
docker-compose up -d

# 또는 개별 실행
./scripts/run_local.sh
```

### 개별 서비스 실행
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev

# vLLM
cd vllm-service
./scripts/start_server.sh
```

## 디렉토리 구조
```
agent-semi-project/
├── frontend/          # React 프론트엔드
├── backend/           # FastAPI 백엔드
├── vllm-service/      # vLLM 서비스 설정
├── shared/            # 공유 리소스
└── scripts/           # 개발 스크립트
```

## 코딩 규칙

### 공통
- 모든 코드는 영어로 작성 (주석, 변수명, 함수명)
- 타입 힌트 필수 (Python, TypeScript)
- 에러 핸들링은 명시적으로

### Python (Backend)
- Python 3.11+ 문법 사용
- Pydantic v2 스키마 사용
- async/await 패턴 권장
- Black + isort 포맷팅

### TypeScript (Frontend)
- 함수형 컴포넌트 사용
- Zustand로 상태 관리
- 절대 경로 import 사용 (`@/`)

## 환경 변수
`.env.example` 파일 참조. 필수 변수:
- `VLLM_BASE_URL`: vLLM 서버 주소
- `VLLM_MODEL`: 사용할 모델명
- `BACKEND_PORT`: 백엔드 포트
- `FRONTEND_PORT`: 프론트엔드 포트
