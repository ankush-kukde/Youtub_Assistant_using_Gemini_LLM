#!/bin/bash

# YouTube AI Chatbot - RAG API Server Startup Script

echo "🚀 Starting YouTube AI Chatbot RAG API Server..."
echo "================================================"

# Check if server is already running
if pgrep -f "python.*main.py" > /dev/null; then
    echo "⚠️  Server is already running!"
    echo "   Use 'pkill -f python.*main.py' to stop it first"
    echo "   Or run 'python3 check_server.py' to check status"
    exit 1
fi

# Check if dependencies are installed
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install --break-system-packages -r requirements.txt
fi

# Check API key configuration
echo "🔑 Checking API key..."
if python3 -c "
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key or api_key == 'your_google_api_key_here':
    print('⚠️  API key not configured - AI responses will be disabled')
    print('   Edit .env file to configure your Google Gemini API key')
else:
    print('✅ API key configured')
"; then
    echo
fi

echo "🌟 Starting server on http://localhost:8000..."
echo "   Press Ctrl+C to stop the server"
echo "   Server logs will appear below:"
echo

# Start the server
python3 main.py