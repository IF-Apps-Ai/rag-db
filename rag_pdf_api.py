"""
RAG PDF System RESTful API
FastAPI implementation untuk sistem RAG PDF dengan multi-turn conversation
"""

import os
import uuid
import shutil
import logging
from datetime import datetime
from typing import List, Dict, Optional

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables untuk menyimpan instance
mongo_client = None
db = None
collection = None
conversation_manager = None

def load_rag_functions():
    """Load functions dari rag-db-pdf.py tanpa menjalankan main code"""
    global mongo_client, db, collection, conversation_manager
    
    try:
        # Import dependencies yang diperlukan
        from pymongo import MongoClient
        from dotenv import load_dotenv
        
        # Load environment variables
        load_dotenv()
        logger.info("Environment variables loaded")
        
        # Setup configurations
        MONGO_URI = os.getenv("MONGO_URI")
        MONGO_URI_LOCAL = "mongodb://localhost:27017"
        DB_NAME = "RAG_PDF_Demo"
        COLLECTION_NAME = "pdf_docs"
        
        logger.info("Attempting MongoDB connection...")
        logger.info(f"Remote URI configured: {'Yes' if MONGO_URI else 'No'}")
        
        # Connect to MongoDB
        try:
            if MONGO_URI:
                logger.info("Trying remote MongoDB...")
                mongo_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
                mongo_client.admin.command('ping')
                logger.info("✅ Connected to remote MongoDB")
            else:
                logger.info("Trying local MongoDB...")
                mongo_client = MongoClient(MONGO_URI_LOCAL, serverSelectionTimeoutMS=3000)
                mongo_client.admin.command('ping')
                logger.info("✅ Connected to local MongoDB")
                
        except Exception as e:
            logger.error("❌ MongoDB connection failed: %s", e)
            logger.info("Trying local MongoDB as fallback...")
            try:
                mongo_client = MongoClient(MONGO_URI_LOCAL, serverSelectionTimeoutMS=3000)
                mongo_client.admin.command('ping')
                logger.info("✅ Connected to local MongoDB (fallback)")
            except Exception as local_e:
                logger.error("❌ Local MongoDB also failed: %s", local_e)
                mongo_client = None
                return False
        
        if mongo_client:
            db = mongo_client[DB_NAME]
            collection = db[COLLECTION_NAME]
            logger.info(f"Database and collection initialized: {DB_NAME}.{COLLECTION_NAME}")
        
        # Initialize conversation manager (simple version)
        conversation_manager = SimpleConversationManager()
        logger.info("Conversation manager initialized")
        
        return True
        
    except Exception as e:
        logger.error("Failed to load RAG functions: %s", e)
        logger.error("Exception details:", exc_info=True)
        return False

class SimpleConversationManager:
    """Simplified conversation manager for API"""
    
    def __init__(self):
        self.conversations = {}  # conversation_id -> history
        
    def get_conversation(self, conversation_id: str) -> List[Dict]:
        """Get conversation history"""
        return self.conversations.get(conversation_id, [])
    
    def add_turn(self, conversation_id: str, question: str, answer: str, sources: List[str] = None):
        """Add turn to conversation"""
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []
        
        turn = {
            "question": question,
            "answer": answer,
            "sources": sources or [],
            "timestamp": datetime.now().isoformat()
        }
        
        self.conversations[conversation_id].append(turn)
        
        # Keep only last 10 turns
        if len(self.conversations[conversation_id]) > 10:
            self.conversations[conversation_id] = self.conversations[conversation_id][-10:]
        
        return len(self.conversations[conversation_id])
    
    def clear_conversation(self, conversation_id: str):
        """Clear specific conversation"""
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
    
    def list_conversations(self) -> List[str]:
        """List all conversation IDs"""
        return list(self.conversations.keys())

# Pydantic models
class UploadResponse(BaseModel):
    message: str
    uploaded_files: List[str]
    total_files: int
    upload_id: str

class IngestResponse(BaseModel):
    message: str
    processed_files: List[str]
    total_chunks: int
    status: str

class QuestionRequest(BaseModel):
    question: str
    conversation_id: Optional[str] = None
    max_results: Optional[int] = 5

class AnswerResponse(BaseModel):
    answer: str
    conversation_id: str
    question: str
    sources: List[Dict]
    turn_number: int

# FastAPI app
app = FastAPI(
    title="RAG PDF System API",
    description="RESTful API untuk sistem RAG PDF dengan multi-turn conversation",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Upload directory
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.on_event("startup")
async def startup_event():
    """Initialize system on startup"""
    logger.info("Starting RAG PDF API...")
    success = load_rag_functions()
    if not success:
        logger.error("Failed to initialize RAG system")
        # Try to continue with basic functionality
    else:
        logger.info("RAG system initialized successfully")

# Helper functions
def extract_text_from_pdf_api(pdf_path: str) -> str:
    """Extract text from PDF file"""
    try:
        import fitz
        doc = fitz.open(pdf_path)
        text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text() + "\n"
        doc.close()
        return text
    except Exception as e:
        logger.error(f"Error extracting text from {pdf_path}: {e}")
        return ""

def split_text_into_chunks_api(text: str, filename: str) -> List[Dict]:
    """Split text into chunks"""
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    
    chunks = text_splitter.split_text(text)
    
    documents = []
    for i, chunk in enumerate(chunks):
        doc = {
            "text": chunk,
            "filename": filename,
            "chunk_id": i,
            "source": "pdf",
            "chunk_size": len(chunk)
        }
        documents.append(doc)
    
    return documents

def get_embedding_api(text: str) -> List[float]:
    """Get embedding for text"""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        result = client.embeddings.create(
            input=[text],
            model="text-embedding-3-small"
        )
        return result.data[0].embedding
    except Exception as e:
        logger.error(f"Error creating embedding: {e}")
        return []

def search_similar_documents_api(query: str, top_k: int = 5) -> List:
    """Search similar documents"""
    try:
        from langchain_chroma import Chroma
        from langchain_openai import OpenAIEmbeddings
        
        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        
        if not os.path.exists("chroma_pdf_db"):
            return []
        
        chroma = Chroma(persist_directory="chroma_pdf_db", embedding_function=embeddings)
        results = chroma.similarity_search(query, k=top_k)
        
        return results
    except Exception as e:
        logger.error(f"Error searching documents: {e}")
        return []

def generate_answer_api(query: str, context: str, conversation_history: List[Dict] = None) -> str:
    """Generate answer using OpenAI"""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Build prompt with conversation context
        prompt_parts = []
        
        if conversation_history:
            prompt_parts.append("CONVERSATION HISTORY:")
            for turn in conversation_history[-3:]:  # Last 3 turns
                prompt_parts.append(f"Q: {turn['question']}")
                prompt_parts.append(f"A: {turn['answer']}")
            prompt_parts.append("\n" + "="*50 + "\n")
        
        prompt_parts.append("DOKUMEN REFERENSI:")
        prompt_parts.append(context)
        prompt_parts.append("\n" + "="*50 + "\n")
        prompt_parts.append(f"PERTANYAAN: {query}")
        prompt_parts.append("\nInstruksi: Berdasarkan dokumen referensi dan konteks percakapan (jika ada), jawab pertanyaan dengan akurat dan lengkap.")
        prompt_parts.append("\nJAWABAN:")
        
        full_prompt = "\n".join(prompt_parts)
        
        response = client.chat.completions.create(
            model=os.getenv("MODEL_NAME", "gpt-4o-mini"),
            messages=[{"role": "user", "content": full_prompt}],
            temperature=float(os.getenv("MODEL_TEMPERATURE", "0")),
            max_tokens=int(os.getenv("MODEL_MAX_TOKENS", "2048"))
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        logger.error(f"Error generating answer: {e}")
        return f"Error generating answer: {str(e)}"

# API Endpoints

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "RAG PDF System API", "version": "1.0.0", "docs": "/docs"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    components = {
        "api": "healthy",
        "mongodb": "unavailable",
        "conversation_manager": "unavailable",
        "chromadb": "unavailable"
    }
    
    try:
        # Test MongoDB connection
        if mongo_client is not None and collection is not None:
            mongo_client.admin.command('ping')
            components["mongodb"] = "healthy"
        
        # Test conversation manager
        if conversation_manager is not None:
            components["conversation_manager"] = "healthy"
            
        # Test ChromaDB
        if os.path.exists("chroma_pdf_db"):
            components["chromadb"] = "available"
            
        status = "healthy" if all(v == "healthy" or v == "available" for v in components.values()) else "degraded"
        
        return {
            "status": status,
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "components": components
        }
        
    except Exception as e:
        return {
            "status": "unhealthy", 
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "components": components,
            "error": str(e)
        }

@app.post("/upload", response_model=UploadResponse)
async def upload_files(files: List[UploadFile] = File(...)):
    """Upload multiple PDF files"""
    upload_id = str(uuid.uuid4())
    uploaded_files = []
    
    try:
        for file in files:
            if not file.filename or not file.filename.lower().endswith('.pdf'):
                continue
            
            # Save file
            file_path = os.path.join(UPLOAD_DIR, f"{upload_id}_{file.filename}")
            
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            uploaded_files.append(file_path)
        
        return UploadResponse(
            message=f"Successfully uploaded {len(uploaded_files)} PDF files",
            uploaded_files=uploaded_files,
            total_files=len(uploaded_files),
            upload_id=upload_id
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.post("/ingest", response_model=IngestResponse)
async def ingest_documents(folder_path: str = Form(UPLOAD_DIR)):
    """Ingest PDF documents"""
    try:
        # Check if MongoDB is connected
        if collection is None:
            raise HTTPException(status_code=503, detail="MongoDB not connected. Please check /health endpoint.")
        
        if not os.path.exists(folder_path):
            raise HTTPException(status_code=404, detail=f"Folder not found: {folder_path}")
        
        # Get PDF files
        pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
        if not pdf_files:
            raise HTTPException(status_code=404, detail="No PDF files found")
        
        processed_files = []
        total_chunks = 0
        
        for filename in pdf_files:
            pdf_path = os.path.join(folder_path, filename)
            
            # Extract text
            text = extract_text_from_pdf_api(pdf_path)
            if not text.strip():
                continue
            
            # Split into chunks
            documents = split_text_into_chunks_api(text, filename)
            
            # Process each chunk
            for doc in documents:
                # Create embedding
                embedding = get_embedding_api(doc["text"])
                if not embedding:
                    continue
                
                # Save to MongoDB
                mongo_doc = {
                    "doc_id": f"{filename}_chunk_{doc['chunk_id']}",
                    "filename": filename,
                    "text": doc["text"],
                    "chunk_id": doc["chunk_id"],
                    "source": "pdf",
                    "embedding": embedding,
                    "kategori": "pdf_document"
                }
                
                collection.insert_one(mongo_doc)
                total_chunks += 1
            
            processed_files.append(pdf_path)
        
        return IngestResponse(
            message=f"Successfully processed {len(processed_files)} PDF files",
            processed_files=processed_files,
            total_chunks=total_chunks,
            status="completed"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")

@app.post("/build-vectorstore")
async def build_vectorstore():
    """Build ChromaDB vector store"""
    try:
        from langchain_chroma import Chroma
        from langchain_openai import OpenAIEmbeddings
        
        # Get documents from MongoDB
        docs = list(collection.find({}, {"doc_id": 1, "text": 1, "filename": 1, "kategori": 1}))
        if not docs:
            raise HTTPException(status_code=400, detail="No documents found in MongoDB")
        
        texts = [doc["text"] for doc in docs]
        metadatas = [
            {
                "doc_id": doc["doc_id"], 
                "filename": doc["filename"],
                "kategori": doc["kategori"]
            } for doc in docs
        ]
        
        # Set OpenAI API key
        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        
        # Create ChromaDB
        Chroma.from_texts(
            texts, 
            embeddings, 
            metadatas=metadatas, 
            persist_directory="chroma_pdf_db"
        )
        
        return {"message": "Vector store built successfully", "status": "completed"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Vector store build failed: {str(e)}")

@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """Ask question with optional conversation context"""
    try:
        # Get or create conversation ID
        conversation_id = request.conversation_id or str(uuid.uuid4())
        
        # Get conversation history
        conversation_history = conversation_manager.get_conversation(conversation_id)
        
        # Search similar documents
        results = search_similar_documents_api(request.question, request.max_results)
        
        if not results:
            answer = "No relevant documents found for your question."
            turn_number = conversation_manager.add_turn(conversation_id, request.question, answer, [])
            
            return AnswerResponse(
                answer=answer,
                conversation_id=conversation_id,
                question=request.question,
                sources=[],
                turn_number=turn_number
            )
        
        # Prepare context
        context_parts = []
        sources = []
        
        for result in results:
            filename = result.metadata.get("filename", "Unknown")
            text = result.page_content
            context_parts.append(f"[File: {filename}]\n{text}")
            sources.append({
                "filename": filename,
                "content": text[:200] + "..." if len(text) > 200 else text,
                "doc_id": result.metadata.get("doc_id", "")
            })
        
        document_context = "\n\n---\n\n".join(context_parts)
        
        # Generate answer
        answer = generate_answer_api(request.question, document_context, conversation_history)
        
        # Save to conversation history
        turn_number = conversation_manager.add_turn(
            conversation_id, 
            request.question, 
            answer, 
            [s["filename"] for s in sources]
        )
        
        return AnswerResponse(
            answer=answer,
            conversation_id=conversation_id,
            question=request.question,
            sources=sources,
            turn_number=turn_number
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Question answering failed: {str(e)}")

@app.get("/conversations")
async def list_conversations():
    """List all conversations"""
    try:
        conversations = []
        for conv_id in conversation_manager.list_conversations():
            history = conversation_manager.get_conversation(conv_id)
            conversations.append({
                "conversation_id": conv_id,
                "turn_count": len(history),
                "last_question": history[-1]["question"] if history else "",
                "created_at": history[0]["timestamp"] if history else ""
            })
        
        return {"conversations": conversations, "total": len(conversations)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list conversations: {str(e)}")

@app.get("/conversations/{conversation_id}")
async def get_conversation_history(conversation_id: str):
    """Get conversation history by ID"""
    try:
        history = conversation_manager.get_conversation(conversation_id)
        if not history:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        return {
            "conversation_id": conversation_id,
            "history": history,
            "total_turns": len(history)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get conversation: {str(e)}")

@app.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete a conversation"""
    try:
        conversation_manager.clear_conversation(conversation_id)
        return {"message": f"Conversation {conversation_id} deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete conversation: {str(e)}")

@app.get("/stats")
async def get_stats():
    """Get system statistics"""
    try:
        # Check if collection is available
        if collection is None:
            raise HTTPException(status_code=503, detail="MongoDB not connected. Please check /health endpoint.")
        
        total_documents = collection.count_documents({})
        total_chunks = collection.count_documents({"chunk_id": {"$exists": True}})
        total_conversations = len(conversation_manager.list_conversations()) if conversation_manager else 0
        
        return {
            "total_documents": total_documents,
            "total_chunks": total_chunks,
            "total_conversations": total_conversations,
            "vector_store_status": "available" if os.path.exists("chroma_pdf_db") else "not_built"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")

@app.post("/initialize")
async def manual_initialize():
    """Manual initialization endpoint for debugging"""
    try:
        success = load_rag_functions()
        if success:
            return {
                "message": "System initialized successfully",
                "mongodb_connected": mongo_client is not None,
                "collection_available": collection is not None,
                "conversation_manager_ready": conversation_manager is not None
            }
        else:
            return {
                "message": "System initialization failed",
                "mongodb_connected": False,
                "collection_available": False,
                "conversation_manager_ready": False
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Initialization failed: {str(e)}")

@app.get("/debug")
async def debug_info():
    """Debug information endpoint"""
    return {
        "mongodb_client": "connected" if mongo_client is not None else "not_connected",
        "database": "available" if db is not None else "not_available", 
        "collection": "available" if collection is not None else "not_available",
        "conversation_manager": "available" if conversation_manager is not None else "not_available",
        "upload_dir_exists": os.path.exists(UPLOAD_DIR),
        "upload_dir_contents": os.listdir(UPLOAD_DIR) if os.path.exists(UPLOAD_DIR) else [],
        "chromadb_exists": os.path.exists("chroma_pdf_db"),
        "env_vars": {
            "MONGO_URI": "set" if os.getenv("MONGO_URI") else "not_set",
            "OPENAI_API_KEY": "set" if os.getenv("OPENAI_API_KEY") else "not_set"
        }
    }

if __name__ == "__main__":
    import uvicorn
    
    HOST = os.getenv("API_HOST", "0.0.0.0")
    PORT = int(os.getenv("API_PORT", "8000"))
    
    logger.info(f"Starting RAG PDF API on {HOST}:{PORT}")
    
    uvicorn.run(
        "rag_pdf_api:app",
        host=HOST,
        port=PORT,
        reload=True,
        log_level="info"
    )
