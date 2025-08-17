#!/usr/bin/env python3
"""
RAG API Server Status Checker
This script checks if the RAG API server is running and accessible.
"""

import requests
import subprocess
import sys
import time
import json
from datetime import datetime

def check_process():
    """Check if the server process is running"""
    print("🔍 Checking server process...")
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        if 'python3 main.py' in result.stdout or 'python main.py' in result.stdout:
            lines = [line for line in result.stdout.split('\n') if 'main.py' in line and 'grep' not in line]
            if lines:
                print("   ✅ Server process found:")
                for line in lines:
                    parts = line.split()
                    if len(parts) >= 2:
                        print(f"      PID: {parts[1]}, Command: {' '.join(parts[10:])}")
                return True
        
        print("   ❌ Server process not found")
        return False
    except Exception as e:
        print(f"   ❌ Error checking process: {e}")
        return False

def check_port():
    """Check if port 8000 is accessible"""
    print("\n🌐 Checking port accessibility...")
    try:
        response = requests.get('http://localhost:8000/health', timeout=5)
        print(f"   ✅ Port 8000 is accessible (Status: {response.status_code})")
        return True
    except requests.exceptions.ConnectionError:
        print("   ❌ Cannot connect to port 8000")
        return False
    except requests.exceptions.Timeout:
        print("   ❌ Connection to port 8000 timed out")
        return False
    except Exception as e:
        print(f"   ❌ Error connecting to port 8000: {e}")
        return False

def test_health_endpoint():
    """Test the health endpoint"""
    print("\n🏥 Testing health endpoint...")
    try:
        response = requests.get('http://localhost:8000/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Health endpoint working")
            print(f"      Status: {data.get('status', 'Unknown')}")
            print(f"      Service: {data.get('service', 'Unknown')}")
            return True
        else:
            print(f"   ❌ Health endpoint returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Health endpoint error: {e}")
        return False

def test_ask_endpoint():
    """Test the ask endpoint with a simple request"""
    print("\n💬 Testing ask endpoint...")
    test_data = {
        'message': 'Test message',
        'video': {
            'videoId': 'dQw4w9WgXcQ',
            'url': 'https://youtube.com/watch?v=dQw4w9WgXcQ',
            'title': 'Test Video',
            'description': 'Test Description',
            'channel': 'Test Channel',
            'timestamp': int(time.time())
        },
        'conversationHistory': []
    }
    
    try:
        response = requests.post('http://localhost:8000/ask', 
                               json=test_data, 
                               timeout=15)
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Ask endpoint working")
            response_text = data.get('response', '')
            if 'error' in response_text.lower():
                print(f"      ⚠️  Response contains error (expected in cloud environment): {response_text[:100]}...")
            else:
                print(f"      Response: {response_text[:100]}...")
            print(f"      Confidence: {data.get('metadata', {}).get('confidence', 'N/A')}")
            return True
        else:
            print(f"   ❌ Ask endpoint returned status {response.status_code}")
            print(f"      Error: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"   ❌ Ask endpoint error: {e}")
        return False

def check_api_key():
    """Check if API key is configured"""
    print("\n🔑 Checking API key configuration...")
    try:
        from dotenv import load_dotenv
        import os
        
        load_dotenv()
        api_key = os.getenv('GOOGLE_API_KEY')
        
        if not api_key:
            print("   ❌ No API key found")
            return False
        elif api_key == 'your_google_api_key_here':
            print("   ⚠️  API key is still set to placeholder")
            print("      The server will work for basic tests but AI responses will be disabled")
            return False
        elif api_key.startswith('AIza'):
            print("   ✅ API key is configured")
            return True
        else:
            print("   ⚠️  API key doesn't look like a valid Google API key")
            return False
    except Exception as e:
        print(f"   ❌ Error checking API key: {e}")
        return False

def provide_troubleshooting():
    """Provide troubleshooting steps"""
    print("\n🔧 Troubleshooting Steps:")
    print("   1. Start the server:")
    print("      python3 main.py")
    print()
    print("   2. If server won't start, check for errors:")
    print("      python3 main.py 2>&1 | head -20")
    print()
    print("   3. If port is blocked, try a different port:")
    print("      python3 -c \"import uvicorn; uvicorn.run('main:app', host='0.0.0.0', port=8001)\"")
    print()
    print("   4. Configure API key (optional for basic testing):")
    print("      Edit .env file and set GOOGLE_API_KEY=your_actual_key")
    print()
    print("   5. Test from browser extension:")
    print("      Make sure the extension is pointing to http://localhost:8000")

def main():
    """Main function"""
    print("🚀 RAG API Server Status Check")
    print("=" * 50)
    print(f"📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run all checks
    process_ok = check_process()
    port_ok = check_port()
    health_ok = test_health_endpoint() if port_ok else False
    ask_ok = test_ask_endpoint() if port_ok else False
    api_key_ok = check_api_key()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 SUMMARY:")
    print(f"   Server Process: {'✅' if process_ok else '❌'}")
    print(f"   Port Access: {'✅' if port_ok else '❌'}")
    print(f"   Health Endpoint: {'✅' if health_ok else '❌'}")
    print(f"   Ask Endpoint: {'✅' if ask_ok else '❌'}")
    print(f"   API Key: {'✅' if api_key_ok else '⚠️'}")
    
    if process_ok and port_ok and health_ok and ask_ok:
        print("\n🎉 SERVER IS RUNNING AND ACCESSIBLE!")
        print("   Your Chrome extension should be able to connect.")
        if not api_key_ok:
            print("   ⚠️  Note: Configure your Google API key for AI responses")
    else:
        print("\n❌ SERVER HAS ISSUES!")
        provide_troubleshooting()
        sys.exit(1)

if __name__ == "__main__":
    main()