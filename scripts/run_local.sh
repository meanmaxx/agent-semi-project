#!/bin/bash

# ===========================================
# Local Development Runner Script
# ===========================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Default ports
BACKEND_PORT=${BACKEND_PORT:-8080}
FRONTEND_PORT=${FRONTEND_PORT:-5173}
VLLM_PORT=${VLLM_PORT:-8000}

# Function to cleanup background processes
cleanup() {
    echo ""
    echo -e "${YELLOW}Shutting down services...${NC}"

    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi

    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi

    echo -e "${GREEN}Services stopped.${NC}"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Print banner
echo -e "${BLUE}"
echo "==========================================="
echo " vLLM Tool-using Agent Service"
echo " Local Development Mode"
echo "==========================================="
echo -e "${NC}"

# Check if vLLM is running
echo -e "${YELLOW}Checking vLLM server...${NC}"
if curl -s "http://localhost:${VLLM_PORT}/health" > /dev/null 2>&1; then
    echo -e "${GREEN}vLLM server is running on port ${VLLM_PORT}${NC}"
else
    echo -e "${RED}Warning: vLLM server is not running on port ${VLLM_PORT}${NC}"
    echo -e "${YELLOW}Please start vLLM server manually:${NC}"
    echo "  cd vllm-service && ./scripts/start_server.sh"
    echo ""
fi

# Start Backend
echo ""
echo -e "${YELLOW}Starting backend server...${NC}"
cd backend
if [ -d "venv" ]; then
    source venv/bin/activate
fi
uvicorn app.main:app --reload --host 0.0.0.0 --port $BACKEND_PORT &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "Waiting for backend to start..."
sleep 3

# Start Frontend
echo ""
echo -e "${YELLOW}Starting frontend server...${NC}"
cd frontend
npm run dev -- --host 0.0.0.0 --port $FRONTEND_PORT &
FRONTEND_PID=$!
cd ..

# Print status
echo ""
echo -e "${GREEN}==========================================="
echo " Services are running!"
echo "==========================================="
echo -e "${NC}"
echo "  Frontend: http://localhost:${FRONTEND_PORT}"
echo "  Backend:  http://localhost:${BACKEND_PORT}"
echo "  vLLM:     http://localhost:${VLLM_PORT}"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop all services${NC}"

# Wait for processes
wait
