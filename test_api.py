import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print("Health Check:", response.json())
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_root_endpoint():
    """Test the root endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/")
        print("Root Endpoint:", response.json())
        return response.status_code == 200
    except Exception as e:
        print(f"Root endpoint test failed: {e}")
        return False

def test_ask_question():
    """Test the ask question endpoint"""
    test_payload = {
        "message": "What is this video about?",
        "video": {
            "videoId": "5NgNicANyqM",  # Using the video ID from your original code
            "url": "https://www.youtube.com/watch?v=5NgNicANyqM",
            "title": "Test Video",
            "description": "A test video for RAG",
            "channel": "Test Channel",
            "timestamp": int(time.time() * 1000)
        },
        "conversationHistory": [
            {
                "text": "Hello",
                "sender": "user",
                "timestamp": int(time.time() * 1000) - 1000
            },
            {
                "text": "Hi! How can I help you?",
                "sender": "bot",
                "timestamp": int(time.time() * 1000) - 500
            }
        ]
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/ask",
            json=test_payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("Ask Question Success:")
            print(f"Response: {result['response']}")
            print(f"Metadata: {result['metadata']}")
            return True
        else:
            print(f"Ask question failed with status {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"Ask question test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Testing YouTube RAG API...")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health_check),
        ("Root Endpoint", test_root_endpoint),
        ("Ask Question", test_ask_question)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\nRunning {test_name}...")
        success = test_func()
        results.append((test_name, success))
        print(f"{test_name}: {'✓ PASSED' if success else '✗ FAILED'}")
    
    print("\n" + "=" * 50)
    print("Test Summary:")
    for test_name, success in results:
        status = "✓ PASSED" if success else "✗ FAILED"
        print(f"  {test_name}: {status}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    print(f"\nOverall: {passed}/{total} tests passed")

if __name__ == "__main__":
    main()