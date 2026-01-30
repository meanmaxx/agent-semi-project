# vLLM Service

## 개요
vLLM 서버 설정 및 Docker 구성을 담당합니다.

## 디렉토리 구조
```
vllm-service/
├── Dockerfile
└── scripts/
    └── start_server.sh
```

## vLLM Tool Calling 설정

### 필수 플래그
Tool Calling을 사용하려면 반드시 다음 플래그를 설정해야 합니다:

```bash
python -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen2.5-7B-Instruct \
    --enable-auto-tool-choice \
    --tool-call-parser hermes
```

### 플래그 설명
| 플래그 | 설명 |
|--------|------|
| `--model` | 사용할 모델 (Tool Calling 지원 모델 필요) |
| `--enable-auto-tool-choice` | 자동 도구 선택 활성화 |
| `--tool-call-parser` | 도구 호출 파서 지정 (hermes, mistral 등) |

### 지원 모델 및 파서
| 모델 | 파서 |
|------|------|
| Qwen/Qwen2.5-*-Instruct | hermes |
| mistralai/Mistral-* | mistral |
| NousResearch/Hermes-* | hermes |

## start_server.sh

```bash
#!/bin/bash

# Default values
MODEL=${VLLM_MODEL:-"Qwen/Qwen2.5-7B-Instruct"}
HOST=${VLLM_HOST:-"0.0.0.0"}
PORT=${VLLM_PORT:-8000}
GPU_MEMORY=${GPU_MEMORY_UTILIZATION:-0.9}
PARSER=${TOOL_CALL_PARSER:-"hermes"}

echo "Starting vLLM server..."
echo "Model: $MODEL"
echo "Host: $HOST:$PORT"

python -m vllm.entrypoints.openai.api_server \
    --model "$MODEL" \
    --host "$HOST" \
    --port "$PORT" \
    --gpu-memory-utilization "$GPU_MEMORY" \
    --enable-auto-tool-choice \
    --tool-call-parser "$PARSER" \
    --trust-remote-code
```

## Dockerfile

```dockerfile
FROM nvidia/cuda:12.1-runtime-ubuntu22.04

# Install Python
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install vLLM
RUN pip install vllm

# Copy scripts
COPY scripts/ /app/scripts/
RUN chmod +x /app/scripts/*.sh

WORKDIR /app

# Environment variables
ENV VLLM_MODEL=Qwen/Qwen2.5-7B-Instruct
ENV VLLM_HOST=0.0.0.0
ENV VLLM_PORT=8000

EXPOSE 8000

CMD ["/app/scripts/start_server.sh"]
```

## Docker Compose 설정

```yaml
# docker-compose.yml (vllm 서비스 부분)
vllm:
  build:
    context: ./vllm-service
    dockerfile: Dockerfile
  ports:
    - "8000:8000"
  environment:
    - VLLM_MODEL=${VLLM_MODEL:-Qwen/Qwen2.5-7B-Instruct}
    - GPU_MEMORY_UTILIZATION=0.9
    - TOOL_CALL_PARSER=hermes
  deploy:
    resources:
      reservations:
        devices:
          - driver: nvidia
            count: 1
            capabilities: [gpu]
  volumes:
    - ~/.cache/huggingface:/root/.cache/huggingface
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
    interval: 30s
    timeout: 10s
    retries: 3
```

## API 엔드포인트

vLLM 서버가 제공하는 OpenAI 호환 엔드포인트:

| 엔드포인트 | 설명 |
|-----------|------|
| `GET /health` | 서버 상태 확인 |
| `GET /v1/models` | 사용 가능한 모델 목록 |
| `POST /v1/chat/completions` | 채팅 완성 (Tool Calling 포함) |
| `POST /v1/completions` | 텍스트 완성 |

## 추가 설정 옵션

### 성능 최적화
```bash
# 텐서 병렬화 (멀티 GPU)
--tensor-parallel-size 2

# KV 캐시 설정
--max-model-len 4096

# 배치 설정
--max-num-batched-tokens 8192
```

### 로깅
```bash
# 상세 로그
--log-level debug

# 요청/응답 로깅
--disable-log-requests  # 프로덕션에서는 비활성화 권장
```

## 트러블슈팅

### Tool Calling이 작동하지 않는 경우
1. `--enable-auto-tool-choice` 플래그 확인
2. `--tool-call-parser` 플래그 확인
3. 모델이 Tool Calling을 지원하는지 확인

### GPU 메모리 부족
```bash
# GPU 메모리 사용률 조정
--gpu-memory-utilization 0.7

# 더 작은 모델 사용
--model Qwen/Qwen2.5-3B-Instruct
```

### 모델 다운로드 실패
```bash
# Hugging Face 토큰 설정
export HF_TOKEN=your_token_here

# 또는 환경 변수로 전달
docker run -e HF_TOKEN=$HF_TOKEN ...
```
