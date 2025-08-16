from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
from typing import List, Optional, Dict, Any
import time
import os
import logging
from rag_service import RAGService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="YouTube RAG API", description="API for answering questions about YouTube videos using RAG")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG service
rag_service = RAGService()

# Request/Response Models
class VideoInfo(BaseModel):
    videoId: str
    url: str
    title: str
    description: str
    channel: str
    timestamp: int
    
    @validator('videoId')
    def validate_video_id(cls, v):
        if not v or len(v) < 10:
            raise ValueError('Invalid video ID')
        return v

class ConversationMessage(BaseModel):
    text: str
    sender: str  # "user" or "bot"
    timestamp: int

class QueryRequest(BaseModel):
    message: str
    video: VideoInfo
    conversationHistory: List[ConversationMessage] = []
    
    @validator('message')
    def validate_message(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Message cannot be empty')
        if len(v) > 1000:
            raise ValueError('Message too long (max 1000 characters)')
        return v.strip()

class QueryResponse(BaseModel):
    response: str
    metadata: Dict[str, Any]

@app.post("/ask", response_model=QueryResponse)
async def ask_question(request: QueryRequest):
    """
    Answer a question about a YouTube video using RAG
    """
    try:
        logger.info(f"Processing question for video {request.video.videoId}: {request.message[:50]}...")
        start_time = time.time()
        
        # Get response from RAG service
        response_text, confidence = await rag_service.answer_question(
            video_id=request.video.videoId,
            question=request.message,
            conversation_history=request.conversationHistory
        )
        
        processing_time = time.time() - start_time
        logger.info(f"Response generated in {processing_time:.2f}s with confidence {confidence}")
        
        return QueryResponse(
            response=response_text,
            metadata={
                "confidence": confidence,
                "processing_time": round(processing_time, 2),
                "video_id": request.video.videoId,
                "chunks_retrieved": 4  # Could be dynamic based on retrieval
            }
        )
        
    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "YouTube RAG API"}

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "YouTube RAG API",
        "version": "1.0.0",
        "endpoints": {
            "ask": "/ask - Ask questions about YouTube videos",
            "health": "/health - Health check",
            "docs": "/docs - API documentation"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
