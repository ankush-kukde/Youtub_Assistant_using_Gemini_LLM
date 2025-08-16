# 🔑 API Key Setup Guide

This guide will help you configure your Google Gemini API key for the YouTube AI Chatbot.

## 🚀 Quick Setup

### Step 1: Get Your Google API Key

1. **Visit Google AI Studio**: Go to [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
2. **Sign in** with your Google account
3. **Create API Key**: Click "Create API Key" button
4. **Copy the key**: Copy the generated API key (it starts with `AIza...`)

### Step 2: Configure the Backend (RAG Service)

1. **Open the `.env` file** in the project root directory
2. **Replace the placeholder** with your actual API key:
   ```
   GOOGLE_API_KEY=AIzaSyYourActualAPIKeyHere
   ```
3. **Save the file**

### Step 3: Restart the Server

```bash
# Stop the current server (Ctrl+C if running)
# Then restart it
python3 main.py
```

You should see: `✅ Google Gemini API configured successfully!`

## 🔍 Troubleshooting

### Problem: "Sorry, the AI model is not properly configured"

**Solution**: Check these steps:

1. **Verify .env file exists**:
   ```bash
   ls -la .env
   ```

2. **Check .env file content**:
   ```bash
   cat .env
   ```
   Make sure `GOOGLE_API_KEY=` is followed by your actual API key (not the placeholder).

3. **Test environment variable loading**:
   ```bash
   python3 -c "from dotenv import load_dotenv; import os; load_dotenv(); print('API Key loaded:', 'Yes' if os.getenv('GOOGLE_API_KEY') else 'No')"
   ```

4. **Restart the server** after making changes.

### Problem: API Key Invalid

**Symptoms**: Error messages about invalid API key or authentication failed.

**Solutions**:
- Make sure you copied the entire API key (starts with `AIza`)
- Check that the API key is enabled in Google Cloud Console
- Verify your Google account has access to Gemini API
- Try generating a new API key

### Problem: Rate Limiting

**Symptoms**: "Quota exceeded" or "Rate limit" errors.

**Solutions**:
- Wait a few minutes and try again
- Check your API usage in Google Cloud Console
- Consider upgrading your API quota if needed

## 🛡️ Security Best Practices

1. **Never commit .env file** to version control
2. **Keep your API key private** - don't share it publicly
3. **Regenerate the key** if you suspect it's been compromised
4. **Set up API quotas** to prevent unexpected charges

## 📝 Alternative Setup Methods

### Method 1: Environment Variable (Linux/Mac)
```bash
export GOOGLE_API_KEY=AIzaSyYourActualAPIKeyHere
python3 main.py
```

### Method 2: Direct in Terminal (Linux/Mac)
```bash
GOOGLE_API_KEY=AIzaSyYourActualAPIKeyHere python3 main.py
```

### Method 3: Windows Command Prompt
```cmd
set GOOGLE_API_KEY=AIzaSyYourActualAPIKeyHere
python main.py
```

### Method 4: Windows PowerShell
```powershell
$env:GOOGLE_API_KEY="AIzaSyYourActualAPIKeyHere"
python main.py
```

## ✅ Verification

To verify your setup is working:

1. **Start the server**: `python3 main.py`
2. **Look for success message**: `✅ Google Gemini API configured successfully!`
3. **Test the API**: 
   ```bash
   curl -X GET http://localhost:8000/health
   ```
4. **Try a chat request** through the extension

## 🆘 Still Having Issues?

If you're still having problems:

1. Check the server logs for detailed error messages
2. Verify your internet connection
3. Make sure you're using Python 3.7 or higher
4. Try regenerating your API key
5. Check if your region supports Gemini API

---

**Need help?** Check the main README.md or create an issue with your error logs.