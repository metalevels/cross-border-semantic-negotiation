#!/bin/bash

# Cross-Border Semantic Negotiation - Run Script
# This script activates the virtual environment and starts the application

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🌐 Cross-Border Semantic Negotiation${NC}"
echo -e "${BLUE}======================================${NC}"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${RED}❌ Virtual environment not found!${NC}"
    echo -e "${YELLOW}Please run: python3 -m venv venv${NC}"
    exit 1
fi

# Activate virtual environment
echo -e "${YELLOW}🔧 Activating virtual environment...${NC}"
source venv/bin/activate

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo -e "${RED}❌ Python not found in virtual environment!${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Virtual environment activated${NC}"
echo -e "${BLUE}Python version: $(python --version)${NC}"

# Display available run options
echo -e "\n${BLUE}Available run options:${NC}"
echo -e "${YELLOW}1. Run main demo (Italy-Germany birth certificate)${NC}"
echo -e "${YELLOW}2. Run example demo${NC}"
echo -e "${YELLOW}3. Run tests${NC}"
echo -e "${YELLOW}4. Start Jupyter notebook${NC}"
echo -e "${YELLOW}5. Start FastAPI server${NC}"

# Default to main demo if no argument provided
RUN_MODE=${1:-"demo"}

case $RUN_MODE in
    "demo"|"1")
        echo -e "\n${GREEN}🚀 Starting main demo...${NC}"
        python src/cross_border_implementation.py
        ;;
    "example"|"2")
        echo -e "\n${GREEN}🚀 Starting example demo...${NC}"
        python examples/italy_germany_demo.py
        ;;
    "test"|"tests"|"3")
        echo -e "\n${GREEN}🧪 Running tests...${NC}"
        if command -v pytest &> /dev/null; then
            pytest tests/ -v
        else
            python -m pytest tests/ -v
        fi
        ;;
    "notebook"|"jupyter"|"4")
        echo -e "\n${GREEN}📓 Starting Jupyter notebook...${NC}"
        if command -v jupyter &> /dev/null; then
            jupyter notebook
        else
            echo -e "${RED}❌ Jupyter not installed. Install with: pip install jupyter${NC}"
            exit 1
        fi
        ;;
    "server"|"api"|"5")
        echo -e "\n${GREEN}🌐 Starting FastAPI server...${NC}"
        if command -v uvicorn &> /dev/null; then
            echo -e "${BLUE}Server will be available at: http://localhost:8000${NC}"
            uvicorn src.api:app --host 0.0.0.0 --port 8000 --reload
        else
            echo -e "${RED}❌ FastAPI/uvicorn not installed. Install with: pip install fastapi uvicorn${NC}"
            exit 1
        fi
        ;;
    "help"|"-h"|"--help")
        echo -e "\n${BLUE}Usage: ./run.sh [option]${NC}"
        echo -e "${YELLOW}Options:${NC}"
        echo -e "  demo, 1     - Run main demo (default)"
        echo -e "  example, 2  - Run example demo"
        echo -e "  test, 3     - Run tests"
        echo -e "  notebook, 4 - Start Jupyter notebook"
        echo -e "  server, 5   - Start FastAPI server"
        echo -e "  help        - Show this help message"
        ;;
    *)
        echo -e "${RED}❌ Unknown option: $RUN_MODE${NC}"
        echo -e "${YELLOW}Run './run.sh help' for available options${NC}"
        exit 1
        ;;
esac

echo -e "\n${GREEN}✨ Done!${NC}"