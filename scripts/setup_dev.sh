#!/bin/bash

# ===========================================
# Development Environment Setup Script
# ===========================================

set -e

echo "Setting up development environment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env file from .env.example...${NC}"
    cp .env.example .env
    echo -e "${GREEN}.env file created. Please update it with your configuration.${NC}"
else
    echo -e "${GREEN}.env file already exists.${NC}"
fi

# Setup Backend
echo ""
echo -e "${YELLOW}Setting up backend...${NC}"
cd backend

if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment and installing dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

cd ..

# Setup Frontend
echo ""
echo -e "${YELLOW}Setting up frontend...${NC}"
cd frontend

if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
else
    echo "Node modules already installed. Running npm install to update..."
    npm install
fi

cd ..

# Make scripts executable
echo ""
echo -e "${YELLOW}Making scripts executable...${NC}"
chmod +x scripts/*.sh
chmod +x vllm-service/scripts/*.sh 2>/dev/null || true

echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}Development environment setup complete!${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo "Next steps:"
echo "1. Update .env file with your configuration"
echo "2. Run './scripts/run_local.sh' to start all services"
echo "   Or run services individually:"
echo "   - Backend: cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
echo "   - Frontend: cd frontend && npm run dev"
echo "   - vLLM: cd vllm-service && ./scripts/start_server.sh"
