# 🔧 API Key Troubleshooting Guide

Your API key `AIzaSyAItVeBwZ6HZ0-efB1kSUOH8txmmzSa8TYA` is showing as invalid. Here's how to fix this:

## 🚨 Common Issues & Solutions

### 1. **API Key Not Activated**
**Problem**: The API key exists but isn't properly activated.

**Solution**:
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Check if your API key is listed and active
3. If not listed, create a new one
4. Make sure you accept all terms and conditions

### 2. **Billing Not Set Up**
**Problem**: Google requires billing to be set up for Gemini API.

**Solution**:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to "Billing" → "Account Management"
3. Set up a billing account (even for free tier usage)
4. Link your project to the billing account

### 3. **API Not Enabled**
**Problem**: The Generative AI API isn't enabled for your project.

**Solution**:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to "APIs & Services" → "Library"
3. Search for "Generative Language API"
4. Click "Enable"

### 4. **Quota/Limits Exceeded**
**Problem**: You've exceeded the API quota or rate limits.

**Solution**:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to "APIs & Services" → "Quotas"
3. Check your usage and limits
4. Request quota increase if needed

### 5. **API Key Restrictions**
**Problem**: The API key has restrictions that prevent it from working.

**Solution**:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to "APIs & Services" → "Credentials"
3. Find your API key and click "Edit"
4. Remove any application restrictions
5. Ensure "Generative Language API" is allowed

## 🔄 Steps to Create a New API Key

1. **Visit Google AI Studio**: https://makersuite.google.com/app/apikey
2. **Sign in** with your Google account
3. **Click "Create API Key"**
4. **Choose "Create API key in new project"** (recommended)
5. **Copy the new API key**
6. **Update your .env file** with the new key

## ✅ Testing Your New API Key

After getting a new API key:

1. **Update .env file**:
   ```bash
   nano .env
   ```
   Replace the GOOGLE_API_KEY value with your new key.

2. **Test the key**:
   ```bash
   python3 test_api_key.py
   ```

3. **Restart the server**:
   ```bash
   pkill -f "python.*main.py"
   python3 main.py
   ```

## 🆘 Alternative: Use Different Model

If gemini-2.0-flash-lite doesn't work, try these models:
- `gemini-1.5-flash` (most common)
- `gemini-1.5-pro`
- `gemini-pro`

Edit `rag_service.py` and change the model name in the `_setup_gemini` method.

## 📞 Contact Information

If none of these solutions work:
1. Check [Google AI Studio Status](https://status.cloud.google.com/)
2. Visit [Google AI Support](https://cloud.google.com/support)
3. Check [Gemini API Documentation](https://ai.google.dev/docs)

---

**Current API Key**: `AIzaSyAItVeBwZ6HZ0-efB1kSUOH8txmmzSa8TYA`
**Status**: Invalid - needs troubleshooting