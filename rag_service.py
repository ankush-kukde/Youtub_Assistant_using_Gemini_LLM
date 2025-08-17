import os
import time
from typing import List, Tuple, Optional
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
import google.generativeai as genai

class RAGService:
    def __init__(self):
        """Initialize the RAG service with models and configurations"""
        # Initialize embedding model
        self.embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, 
            chunk_overlap=200
        )
        
        # Initialize Google Gemini
        self._setup_gemini()
        
        # Store for vector stores (video_id -> FAISS store)
        self.vector_stores = {}
        
        # Initialize prompt template
        self.prompt_template = PromptTemplate(
            template="""
            You are a helpful assistant.
            Answer ONLY from the provided transcript context.
            If the context is insufficient, just say you don't know.

            Context: {context}
            
            Conversation History: {conversation_history}
            
            Question: {question}
            
            Answer:
            """,
            input_variables=['context', 'conversation_history', 'question']
        )
    
    def _setup_gemini(self):
        """Setup Google Gemini API"""
        # Try to get API key from environment
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            # For demo purposes, we'll use a placeholder
            # In production, this should be properly configured
            print("Warning: GOOGLE_API_KEY not found in environment variables")
            print("Please set your Google API key for Gemini to work properly")
            self.model = None
            return
            
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
    
    def _generate_response(self, prompt: str, temperature: float = 0.2, max_tokens: int = 256) -> str:
        """Generate response using Google Gemini"""
        if not self.model:
            return "Sorry, the AI model is not properly configured. Please check the API key."
            
        try:
            response = self.model.generate_content(
                prompt,  # Pass prompt directly, not as a list
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                )
            )
            
            # Handle the response properly
            if response.text:
                return response.text
            else:
                return "Sorry, I couldn't generate a response. The model may have been blocked or returned empty content."
                
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error in _generate_response: {str(e)}", exc_info=True)
            return f"Sorry, I encountered an error generating the response: {str(e)}"
    
    def _get_video_transcript(self, video_id: str) -> str:
        """Fetch and process YouTube transcript"""
        try:
            # Fetch transcript
            ytt_api = YouTubeTranscriptApi()
            fetched_transcript = ytt_api.fetch(video_id)
            
            # Join all transcript text
            transcript_text = " ".join(snippet.text for snippet in fetched_transcript)
            return transcript_text
            
        except TranscriptsDisabled:
            raise Exception(f"Transcripts are disabled for video {video_id}")
        except Exception as e:
            raise Exception(f"Error fetching transcript: {str(e)}")
    
    def _create_vector_store(self, transcript_text: str) -> FAISS:
        """Create FAISS vector store from transcript"""
        # Split text into chunks
        chunks = self.text_splitter.create_documents([transcript_text])
        
        # Create vector store
        vector_store = FAISS.from_documents(chunks, self.embedding_model)
        return vector_store
    
    def _get_or_create_vector_store(self, video_id: str) -> FAISS:
        """Get existing vector store or create new one"""
        if video_id not in self.vector_stores:
            # Fetch transcript and create vector store
            transcript_text = self._get_video_transcript(video_id)
            vector_store = self._create_vector_store(transcript_text)
            self.vector_stores[video_id] = vector_store
        
        return self.vector_stores[video_id]
    
    def _format_conversation_history(self, conversation_history: List) -> str:
        """Format conversation history for context"""
        if not conversation_history:
            return "No previous conversation."
            
        formatted_history = []
        for msg in conversation_history[-5:]:  # Only use last 5 messages
            # Handle both Pydantic models and dictionaries
            if hasattr(msg, 'sender') and hasattr(msg, 'text'):
                # Pydantic model
                sender = msg.sender
                text = msg.text
            elif isinstance(msg, dict):
                # Dictionary
                try:
                    sender = msg.get('sender', 'unknown')
                    text = msg.get('text', '')
                except Exception:   # ✅ use except instead of else
                    sender = 'unknown'
                    text = str(msg)
            else:
                # Fallback for unexpected types
                sender = 'unknown'
                text = str(msg)
            
            formatted_history.append(f"{sender}: {text}")
        
        return "\n".join(formatted_history)
    
    async def answer_question(self, video_id: str, question: str, conversation_history: List = None) -> Tuple[str, float]:
        """
        Answer a question about a YouTube video
        
        Returns:
            Tuple of (answer, confidence_score)
        """
        try:
            # Get or create vector store for the video
            vector_store = self._get_or_create_vector_store(video_id)
            
            # Create retriever
            retriever = vector_store.as_retriever(
                search_type="similarity", 
                search_kwargs={"k": 4}
            )
            
            # Retrieve relevant documents
            retrieved_docs = retriever.invoke(question)
            
            # Format context
            context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
            
            # Format conversation history
            conversation_text = self._format_conversation_history(conversation_history or [])
            
            # Create final prompt
            final_prompt_value = self.prompt_template.invoke({
                "context": context_text,
                "conversation_history": conversation_text,
                "question": question
            })
            final_prompt = final_prompt_value.text
            
            # Generate answer
            answer = self._generate_response(final_prompt)
            
            # Calculate confidence based on retrieval similarity (simplified)
            # In a real implementation, you might use more sophisticated confidence scoring
            confidence = min(0.95, max(0.6, len(retrieved_docs) / 4.0))
            
            return answer, confidence
            
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error in answer_question: {str(e)}", exc_info=True)
            return f"Sorry, I encountered an error: {str(e)}", 0.0