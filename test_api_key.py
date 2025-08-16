#!/usr/bin/env python3
"""
API Key Configuration Test Script
This script helps you verify that your Google Gemini API key is properly configured.
"""

import os
import sys
from dotenv import load_dotenv

def test_api_key_configuration():
    """Test API key configuration step by step"""
    
    print("🔍 YouTube AI Chatbot - API Key Configuration Test")
    print("=" * 55)
    
    # Step 1: Test .env file loading
    print("\n📁 Step 1: Testing .env file loading...")
    try:
        load_dotenv()
        print("   ✅ dotenv loaded successfully")
    except Exception as e:
        print(f"   ❌ Error loading .env file: {e}")
        return False
    
    # Step 2: Check if API key exists
    print("\n🔑 Step 2: Checking API key...")
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        print("   ❌ No API key found!")
        print_setup_instructions()
        return False
    elif api_key == 'your_google_api_key_here':
        print("   ⚠️  API key is still set to placeholder value!")
        print_setup_instructions()
        return False
    elif not api_key.startswith('AIza'):
        print("   ⚠️  API key doesn't look like a valid Google API key (should start with 'AIza')")
        print("   Current value starts with:", api_key[:10] + "...")
        return False
    else:
        print(f"   ✅ API key found: {api_key[:10]}...")
    
    # Step 3: Test RAG service initialization
    print("\n🤖 Step 3: Testing RAG service initialization...")
    try:
        from rag_service import RAGService
        rag = RAGService()
        
        if rag.model:
            print("   ✅ RAG Service initialized successfully!")
            print("   ✅ Google Gemini model configured!")
            
            # Step 4: Test a simple API call
            print("\n🧪 Step 4: Testing API connection...")
            try:
                test_response = rag._generate_response("Say 'Hello, API test successful!'")
                if "API test successful" in test_response or "Hello" in test_response:
                    print("   ✅ API connection test successful!")
                    print(f"   Response: {test_response}")
                    return True
                else:
                    print(f"   ⚠️  API responded, but response seems unusual: {test_response}")
                    return True  # Still consider it successful
            except Exception as e:
                print(f"   ❌ API connection test failed: {e}")
                return False
        else:
            print("   ❌ RAG Service model not configured!")
            return False
            
    except Exception as e:
        print(f"   ❌ Error initializing RAG Service: {e}")
        return False

def print_setup_instructions():
    """Print setup instructions"""
    print("\n📝 Setup Instructions:")
    print("   1. Get your API key from: https://makersuite.google.com/app/apikey")
    print("   2. Edit the .env file in this directory")
    print("   3. Replace 'your_google_api_key_here' with your actual API key")
    print("   4. Save the file and run this test again")
    print("\n   Example .env file content:")
    print("   GOOGLE_API_KEY=AIzaSyYourActualAPIKeyHere")

def main():
    """Main function"""
    success = test_api_key_configuration()
    
    print("\n" + "=" * 55)
    if success:
        print("🎉 Configuration test PASSED!")
        print("   Your API key is properly configured and working.")
        print("   You can now start the server with: python3 main.py")
    else:
        print("❌ Configuration test FAILED!")
        print("   Please follow the setup instructions above.")
        sys.exit(1)

if __name__ == "__main__":
    main()