# YouTube AI Chatbot Extension + RAG API Setup Guide

This guide will help you set up the complete YouTube AI Chatbot system with the integrated RAG API.

## 🎯 What You'll Get

- **Chrome Extension**: Beautiful chatbot interface on YouTube pages
- **RAG API**: Local AI service that analyzes YouTube transcripts
- **Google Gemini Integration**: Advanced AI responses about video content
- **Conversation Memory**: Maintains context across questions

## 📋 Prerequisites

1. **Python 3.8+** installed on your system
2. **Google Gemini API Key** (get from https://makersuite.google.com/app/apikey)
3. **Chrome Browser** for the extension

## 🚀 Quick Setup (5 minutes)

### Step 1: Install Python Dependencies

```bash
# Navigate to the project directory
cd /path/to/youtube-ai-chatbot

# Install required packages
pip install -r requirements.txt
```

### Step 2: Configure Google Gemini API

```bash
# Set your Google API key (replace with your actual key)
export GOOGLE_API_KEY="your_actual_api_key_here"

# Or create a .env file
echo "GOOGLE_API_KEY=your_actual_api_key_here" > .env
```

### Step 3: Start the RAG API Server

```bash
# Start the API server
python3 main.py

# Or use the startup script
./start_server.sh
```

You should see:
```
INFO:     Started server process
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Step 4: Install Chrome Extension

1. **Open Chrome** and go to `chrome://extensions/`
2. **Enable Developer Mode** (toggle in top-right)
3. **Click "Load unpacked"** and select this project folder
4. **Pin the extension** (puzzle piece icon → pin YouTube AI Chatbot)

### Step 5: Test the Integration

1. **Go to any YouTube video** (e.g., https://www.youtube.com/watch?v=dQw4w9WgXcQ)
2. **Click the extension icon** to open the chatbot
3. **Ask a question** about the video content
4. **Enjoy AI-powered responses!**

## ⚙️ Configuration Options

### API Endpoints

The extension is pre-configured to use:
- **RAG API**: `http://localhost:8000/ask`
- **Health Check**: `http://localhost:8000/health`

### Customizing the API Port

If you need to use a different port:

1. **Update main.py**:
   ```python
   if __name__ == "__main__":
       import uvicorn
       uvicorn.run(app, host="0.0.0.0", port=YOUR_PORT)
   ```

2. **Update config.js**:
   ```javascript
   ENDPOINT: 'http://localhost:YOUR_PORT/ask',
   HEALTH_ENDPOINT: 'http://localhost:YOUR_PORT/health',
   ```

3. **Update manifest.json**:
   ```json
   "host_permissions": [
     "http://localhost:YOUR_PORT/*"
   ]
   ```

## 🔧 Troubleshooting

### Extension Shows "RAG API is not available"

**Cause**: The API server is not running or not accessible.

**Solutions**:
1. Make sure the API server is running: `python3 main.py`
2. Check the server is accessible: `curl http://localhost:8000/health`
3. Reload the extension in `chrome://extensions/`

### "No response received from API"

**Cause**: Missing Google API key or API quota exceeded.

**Solutions**:
1. Verify your API key: `echo $GOOGLE_API_KEY`
2. Check API key validity at https://makersuite.google.com/app/apikey
3. Check the server logs for error messages

### "Please navigate to a YouTube video"

**Cause**: Extension is not detecting the current video.

**Solutions**:
1. Make sure you're on a YouTube video page (`/watch?v=...`)
2. Refresh the page and try again
3. Check browser console for errors (F12)

### Video Transcript Not Available

**Cause**: The video doesn't have transcripts or they're restricted.

**Solutions**:
1. Try a different video with available transcripts
2. Check if the video has closed captions enabled
3. Some videos may have transcripts disabled by the creator

## 🎮 Usage Tips

### Best Questions to Ask

- **Content Summary**: "What is this video about?"
- **Key Points**: "What are the main points discussed?"
- **Specific Topics**: "What did they say about [topic]?"
- **Explanations**: "Can you explain [concept] mentioned in the video?"
- **Timestamps**: "At what time do they discuss [topic]?"

### Conversation Features

- **Context Memory**: The bot remembers your previous questions
- **Confidence Scores**: Low confidence responses include a note
- **Processing Time**: Metadata shows how long responses took
- **Error Handling**: Graceful fallbacks when issues occur

## 🔒 Privacy & Security

- **Local Processing**: Your conversations stay on your machine
- **No Data Collection**: The extension doesn't send data to third parties
- **API Key Security**: Your Google API key stays in your environment
- **Transcript Access**: Only accesses publicly available YouTube transcripts

## 📊 API Endpoints Reference

### Chat Endpoint: POST `/ask`

```json
{
  "message": "What is this video about?",
  "video": {
    "videoId": "dQw4w9WgXcQ",
    "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "title": "Video Title",
    "description": "Video description",
    "channel": "Channel Name",
    "timestamp": 1645123456789
  },
  "conversationHistory": [
    {"text": "Previous message", "sender": "user", "timestamp": 1645123456789}
  ]
}
```

### Health Check: GET `/health`

```json
{
  "status": "healthy",
  "service": "YouTube RAG API"
}
```

## 📈 Performance Notes

- **First Request**: Slower (fetches and processes transcript)
- **Subsequent Requests**: Faster (uses cached embeddings)
- **Memory Usage**: Vectors stored in memory per video
- **Processing Time**: Typically 1-3 seconds per response

## 🔧 Advanced Configuration

### Changing AI Models

Edit `rag_service.py`:

```python
# Change embedding model
self.embedding_model = HuggingFaceEmbeddings(
    model_name="your-preferred-model"
)

# Change Gemini model
self.model = genai.GenerativeModel("gemini-1.5-pro")  # or other variants
```

### Adjusting Chunk Size

```python
self.text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,  # Increase for longer chunks
    chunk_overlap=300  # Increase for more context overlap
)
```

## 📱 Extension Development

To modify the extension:

1. **Edit files** in the project directory
2. **Reload extension** in `chrome://extensions/`
3. **Test changes** on YouTube pages
4. **Check console** for debugging (F12)

### Key Files

- `manifest.json`: Extension configuration
- `popup.html/css/js`: Chat interface
- `content.js`: YouTube page integration
- `background.js`: API communication
- `config.js`: Extension settings

## 🆘 Getting Help

If you encounter issues:

1. **Check server logs** in the terminal running `python3 main.py`
2. **Check browser console** (F12) for JavaScript errors
3. **Verify API health** by visiting `http://localhost:8000/docs`
4. **Test API directly** using the test script: `python3 test_api.py`

## 🎉 Success!

Once everything is working, you'll have:
- ✅ A running RAG API server
- ✅ Chrome extension installed and active
- ✅ AI chatbot responding to questions about YouTube videos
- ✅ Conversation history and context memory

Enjoy chatting with your YouTube videos! 🤖📺

