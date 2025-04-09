#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo "Activating virtual environment..."
source server/venv/Scripts/activate
if [ $? -ne 0 ]; then
  echo -e "${RED}Failed to activate virtual environment.${NC}"
  exit 1
fi

echo "Virtual environment activated."

# Run the Python server in the background
echo "Starting Python server..."
python server/main.py &

# Optionally capture its PID if you need to manage it later
PYTHON_PID=$!

# Wait a little for the server to start up if necessary
echo "Waiting for the Python server to initialize..."
sleep 0.3

if ! kill -0 $PYTHON_PID 2>/dev/null; then
  echo -e "\n${RED}❌ Python server failed to start.\n\nRun: pip install -r requirements.txt${NC}"
  exit 1
fi

sleep 2

# Navigate to the npm project directory (replace with your directory)
echo "Changing directory to the npm project folder..."
cd client || { echo "Failed to change directory"; exit 1; }

# Start the npm process
echo "Starting web server..."
npm run dev

# Optional: When npm stops, you might want to stop the Python server:
# echo "Stopping Python server..."
# kill $PYTHON_PID
