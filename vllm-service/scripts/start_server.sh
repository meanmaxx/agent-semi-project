#!/bin/bash

# ===========================================
# vLLM Server Startup Script
# ===========================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default values (can be overridden by environment variables)
MODEL=${VLLM_MODEL:-"Qwen/Qwen2.5-7B-Instruct"}
HOST=${VLLM_HOST:-"0.0.0.0"}
PORT=${VLLM_PORT:-8000}
GPU_MEMORY=${GPU_MEMORY_UTILIZATION:-0.9}
PARSER=${TOOL_CALL_PARSER:-"hermes"}

# Print configuration
echo -e "${GREEN}==========================================="
echo " vLLM Server Configuration"
echo "==========================================="
echo -e "${NC}"
echo "  Model:          $MODEL"
echo "  Host:           $HOST"
echo "  Port:           $PORT"
echo "  GPU Memory:     $GPU_MEMORY"
echo "  Tool Parser:    $PARSER"
echo ""

# Check for HF_TOKEN if needed
if [ ! -z "$HF_TOKEN" ]; then
    echo -e "${GREEN}Hugging Face token is set${NC}"
    export HUGGING_FACE_HUB_TOKEN=$HF_TOKEN
fi

# Start vLLM server
echo -e "${YELLOW}Starting vLLM server...${NC}"
echo ""

python -m vllm.entrypoints.openai.api_server \
    --model "$MODEL" \
    --host "$HOST" \
    --port "$PORT" \
    --gpu-memory-utilization "$GPU_MEMORY" \
    --enable-auto-tool-choice \
    --tool-call-parser "$PARSER" \
    --trust-remote-code
