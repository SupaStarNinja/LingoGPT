#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${GREEN}🔧 Installing Python dependencies...${NC}"

# Check if virtual environment exists
if [ -f "server/venv/Scripts/activate" ]; then
  source server/venv/Scripts/activate
  echo -e "${GREEN}✅ Virtual environment activated.${NC}"
else
  echo -e "${RED}❌ Virtual environment not found at server/venv. Please create one first.${NC}"
  exit 1
fi

# Install Python requirements
if [ -f "requirements.txt" ]; then
  pip install -r requirements.txt
  echo -e "${GREEN}✅ Python dependencies installed.${NC}"
else
  echo -e "${RED}❌ requirements.txt not found.${NC}"
  exit 1
fi

# Install npm dependencies
echo -e "${GREEN}📦 Installing npm packages...${NC}"

if [ -d "client" ]; then
  cd client || exit 1
  npm install
  echo -e "${GREEN}✅ npm packages installed.${NC}"
else
  echo -e "${RED}❌ client directory not found.${NC}"
  exit 1
fi

echo -e "${GREEN}🎉 Installation complete!${NC}"
