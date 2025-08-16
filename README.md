# YouTube RAG API

A FastAPI-based service that uses Retrieval-Augmented Generation (RAG) to answer questions about YouTube videos using their transcripts.

## Features

- 🎥 **YouTube Transcript Processing**: Automatically fetches and processes YouTube video transcripts
- 🔍 **Semantic Search**: Uses FAISS vector store with sentence transformers for semantic similarity search
- 🤖 **AI-Powered Responses**: Leverages Google Gemini for generating contextual answers
- 💬 **Conversation History**: Maintains conversation context for better responses
- ⚡ **Fast API**: Built with FastAPI for high performance and automatic API documentation
- 📊 **Confidence Scoring**: Returns confidence scores with each response

## Installation

1. **Clone the repository and navigate to the project directory**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your Google Gemini API key:
   ```
   GOOGLE_API_KEY=your_actual_api_key_here
   ```
   
   Get your API key from: https://makersuite.google.com/app/apikey

## Usage

### Starting the Server

```bash
python main.py
```

The API will be available at `http://localhost:8000`

### API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI)

### API Endpoints

#### POST `/ask`

Ask a question about a YouTube video.

**Request Body:**
```json
{
  "message": "What is this video about?",
  "video": {
    "videoId": "dQw4w9WgXcQ",
    "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "title": "Video Title",
    "description": "Video description...",
    "channel": "Channel Name",
    "timestamp": 1645123456789
  },
  "conversationHistory": [
    {"text": "Previous message", "sender": "user", "timestamp": 1645123456789},
    {"text": "Previous response", "sender": "bot", "timestamp": 1645123456790}
  ]
}
```

**Response:**
```json
{
  "response": "This video is about...",
  "metadata": {
    "confidence": 0.95,
    "processing_time": 1.2
  }
}
```

#### GET `/health`

Health check endpoint.

#### GET `/`

Root endpoint with API information.

## Testing

Run the test script to verify the API functionality:

```bash
python test_api.py
```

## Example Usage

### Using curl

```bash
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{
       "message": "What is this video about?",
       "video": {
         "videoId": "5NgNicANyqM",
         "url": "https://www.youtube.com/watch?v=5NgNicANyqM",
         "title": "Sample Video",
         "description": "A sample video",
         "channel": "Sample Channel",
         "timestamp": 1645123456789
       }
     }'
```

### Using Python requests

```python
import requests

response = requests.post("http://localhost:8000/ask", json={
    "message": "What is this video about?",
    "video": {
        "videoId": "5NgNicANyqM",
        "url": "https://www.youtube.com/watch?v=5NgNicANyqM",
        "title": "Sample Video",
        "description": "A sample video",
        "channel": "Sample Channel",
        "timestamp": 1645123456789
    }
})

print(response.json())
```

## How It Works

1. **Transcript Fetching**: The service uses `youtube-transcript-api` to fetch video transcripts
2. **Text Chunking**: Transcripts are split into chunks using LangChain's `RecursiveCharacterTextSplitter`
3. **Vector Embeddings**: Text chunks are converted to embeddings using sentence transformers
4. **Vector Storage**: Embeddings are stored in FAISS for fast similarity search
5. **Retrieval**: Relevant chunks are retrieved based on question similarity
6. **Generation**: Google Gemini generates contextual answers using retrieved chunks
7. **Response**: Final answer with confidence score and metadata is returned

## Configuration

### Environment Variables

- `GOOGLE_API_KEY`: Your Google Gemini API key (required)

### Model Configuration

The service uses:
- **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **LLM**: Google Gemini 1.5 Flash
- **Text Splitter**: Recursive character splitter (1000 chars, 200 overlap)
- **Vector Store**: FAISS

## Error Handling

The API includes comprehensive error handling for:
- Invalid video IDs
- Missing transcripts
- API failures
- Network issues
- Invalid request formats

## Performance Considerations

- Vector stores are cached per video ID to avoid reprocessing
- Conversation history is limited to last 5 messages
- Responses include processing time metrics
- FAISS provides fast vector similarity search

## Limitations

- Requires videos to have available transcripts
- Currently supports English transcripts
- API key required for Google Gemini
- Memory-based vector store (not persistent)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License