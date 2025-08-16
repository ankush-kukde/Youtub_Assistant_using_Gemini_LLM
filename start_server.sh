#!/bin/bash

# YouTube RAG API Startup Script
echo "Starting YouTube RAG API..."

# Check if required packages are installed
python3 -c "import fastapi, uvicorn" 2>/dev/null || {
    echo "Installing required packages..."
    pip install --break-system-packages -r requirements.txt
}

# Check for environment file
if [ ! -f .env ]; then
    echo "Warning: .env file not found. Using .env.example as template."
    echo "Please edit .env with your actual API keys."
    cp .env.example .env
fi

# Start the server
echo "Starting server on http://localhost:8000"
echo "API Documentation available at http://localhost:8000/docs"
echo "Health check: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the server"

python3 main.py