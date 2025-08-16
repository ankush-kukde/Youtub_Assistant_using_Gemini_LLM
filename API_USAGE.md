# Quick Start Guide - YouTube RAG API

## 🚀 Quick Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Google Gemini API Key:**
   ```bash
   export GOOGLE_API_KEY="your_api_key_here"
   ```
   Get your key from: https://makersuite.google.com/app/apikey

3. **Start the server:**
   ```bash
   ./start_server.sh
   # OR
   python3 main.py
   ```

4. **Test the API:**
   ```bash
   curl http://localhost:8000/health
   ```

## 📡 API Endpoints

### POST `/ask` - Ask Questions About Videos

**Input Format:**
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

**Output Format:**
```json
{
  "response": "This video is about...",
  "metadata": {
    "confidence": 0.95,
    "processing_time": 1.2,
    "video_id": "dQw4w9WgXcQ",
    "chunks_retrieved": 4
  }
}
```

## 🧪 Testing

Use the provided test script:
```bash
python3 test_api.py
```

Or test with curl:
```bash
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d @example_request.json
```

## 📚 Documentation

- **Interactive API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health
- **OpenAPI Schema:** http://localhost:8000/openapi.json

## 🔧 Configuration

- **Embedding Model:** sentence-transformers/all-MiniLM-L6-v2
- **LLM:** Google Gemini 1.5 Flash
- **Vector Store:** FAISS (in-memory)
- **Text Chunking:** 1000 chars with 200 overlap

## ⚠️ Important Notes

1. **API Key Required:** Set `GOOGLE_API_KEY` environment variable
2. **Transcript Availability:** Videos must have available transcripts
3. **IP Restrictions:** May not work from cloud IPs due to YouTube restrictions
4. **Memory Storage:** Vector stores are not persistent across restarts

## 🔍 How It Works

1. Fetches YouTube transcript using video ID
2. Splits transcript into chunks
3. Creates vector embeddings with sentence transformers
4. Stores in FAISS vector database
5. Retrieves relevant chunks for user questions
6. Generates contextual answers using Gemini AI

## 📈 Performance Tips

- Vector stores are cached per video
- First request per video is slower (transcript processing)
- Subsequent requests are faster (cached vectors)
- Conversation history limited to last 5 messages