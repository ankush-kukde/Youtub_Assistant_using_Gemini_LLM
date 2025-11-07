import os
import logging
from typing import List, Tuple, Optional
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
import google.generativeai as genai
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()


class RAGService:
    def __init__(self):
        """Initialize the RAG service with models and configurations"""

        # ✅ Initialize embedding model (modern syntax)
        self.embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},  # change to "cuda" if GPU is available
            encode_kwargs={"normalize_embeddings": True}
        )

        # ✅ Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        # ✅ Initialize Gemini
        self._setup_gemini()

        # ✅ In-memory cache of FAISS stores per video
        self.vector_stores: dict[str, FAISS] = {}

        # ✅ Prompt template (for Gemini context generation)
        self.prompt_template = PromptTemplate(
            template=(
                "You are a helpful assistant.\n"
                "Answer ONLY using the provided YouTube transcript context.\n"
                "If the context does not contain the answer, say you don't know.\n\n"
                "Context:\n{context}\n\n"
                "Conversation History:\n{conversation_history}\n\n"
                "Question:\n{question}\n\n"
                "Answer:"
            ),
            input_variables=["context", "conversation_history", "question"]
        )

    # -------------------------------------------------------------------------
    # GEMINI SETUP
    # -------------------------------------------------------------------------
    def _setup_gemini(self):
        """Configure Google Gemini API"""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("⚠️ GOOGLE_API_KEY not found in environment variables.")
            print("Please set it in your .env file for Gemini to work.")
            self.model = None
            return

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def _generate_response(
        self,
        prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 256
    ) -> str:
        """Generate a response using Google Gemini"""
        if not self.model:
            return "Sorry, the Gemini model is not configured properly. Please check your API key."

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                )
            )

            # ✅ Gemini responses return a .text attribute if successful
            if hasattr(response, "text") and response.text:
                return response.text.strip()
            else:
                return "Sorry, I couldn't generate a meaningful response."
        except Exception as e:
            logging.error(f"Error in Gemini response: {e}", exc_info=True)
            return f"Error generating response: {e}"

    # -------------------------------------------------------------------------
    # TRANSCRIPT & VECTOR STORE
    # -------------------------------------------------------------------------
    # def _get_video_transcript(self, video_id: str) -> str:
    #     """Fetch YouTube transcript text"""
    #     try:
    #         transcript = YouTubeTranscriptApi.get_transcript(video_id)
    #         text = " ".join(segment["text"] for segment in transcript)
    #         return text
    #     except TranscriptsDisabled:
    #         raise Exception(f"Transcripts are disabled for video ID: {video_id}")
    #     except Exception as e:
    #         raise Exception(f"Error fetching transcript for {video_id}: {str(e)}")

    def _get_video_transcript(self, video_id: str) -> str:
        """Fetch and return YouTube transcript text for a given video ID."""
        try:
            # ✅ Use the instance-based API, not the static one
            ytt_api = YouTubeTranscriptApi()
            fetched_transcript = ytt_api.fetch(video_id)

            # ✅ Extract text safely from iterable transcript snippets
            transcript_text = " ".join(snippet.text for snippet in fetched_transcript)
            return transcript_text.strip()

        except TranscriptsDisabled:
            raise Exception(f"❌ Transcripts are disabled for video ID: {video_id}")

        except Exception as e:
            raise Exception(f"❌ Error fetching transcript for {video_id}: {str(e)}")

    def _create_vector_store(self, transcript_text: str) -> FAISS:
        """Create a FAISS vector store from transcript text"""
        chunks = self.text_splitter.create_documents([transcript_text])
        vector_store = FAISS.from_documents(chunks, self.embedding_model)
        return vector_store

    def _get_or_create_vector_store(self, video_id: str) -> FAISS:
        """Get an existing vector store or create one for this video"""
        if video_id not in self.vector_stores:
            transcript = self._get_video_transcript(video_id)
            self.vector_stores[video_id] = self._create_vector_store(transcript)
        return self.vector_stores[video_id]

    # -------------------------------------------------------------------------
    # CONTEXT HANDLING
    # -------------------------------------------------------------------------
    def _format_conversation_history(self, conversation_history: Optional[List] = None) -> str:
        """Convert conversation history list into readable string"""
        if not conversation_history:
            return "No previous conversation."

        formatted = []
        for msg in conversation_history[-5:]:
            if isinstance(msg, dict):
                sender = msg.get("sender", "User")
                text = msg.get("text", "")
            else:
                sender = getattr(msg, "sender", "User")
                text = getattr(msg, "text", str(msg))
            formatted.append(f"{sender}: {text}")
        return "\n".join(formatted)

    # -------------------------------------------------------------------------
    # MAIN RAG QUERY PIPELINE
    # -------------------------------------------------------------------------
    async def answer_question(
        self,
        video_id: str,
        question: str,
        conversation_history: Optional[List] = None
    ) -> Tuple[str, float]:
        """Answer a user question using YouTube transcript + Gemini"""
        try:
            # ✅ Retrieve or build vector store
            vector_store = self._get_or_create_vector_store(video_id)

            # ✅ Create retriever
            retriever = vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 4}
            )

            # ✅ Retrieve relevant chunks
            retrieved_docs = retriever.invoke(question)
            context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)

            # ✅ Build conversation context
            conversation_text = self._format_conversation_history(conversation_history)

            # ✅ Build final prompt
            final_prompt = self.prompt_template.format(
                context=context_text,
                conversation_history=conversation_text,
                question=question
            )

            # ✅ Generate final answer
            answer = self._generate_response(final_prompt)

            # ✅ Confidence estimation (simplified heuristic)
            confidence = 0.6 + 0.1 * min(4, len(retrieved_docs))
            confidence = round(min(confidence, 0.95), 2)

            return answer, confidence

        except Exception as e:
            logging.error(f"Error answering question: {e}", exc_info=True)
            return f"Sorry, I encountered an error: {str(e)}", 0.0
