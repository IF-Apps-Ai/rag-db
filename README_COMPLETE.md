# 🤖 RAG PDF System - Complete Documentation

## 📋 **Project Overview**

Sistem RAG (Retrieval-Augmented Generation) PDF dengan kemampuan multi-turn conversation menggunakan MongoDB, ChromaDB, dan OpenAI. Tersedia dalam versi CLI dan RESTful API.

## 🚀 **Quick Start**

### Prerequisites
```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env dengan API keys dan database URLs
```

### Running CLI Version
```bash
python rag-db-pdf.py
```

### Running API Version  
```bash
python rag_pdf_api.py
# API tersedia di: http://127.0.0.1:8000
# Dokumentasi: http://127.0.0.1:8000/docs
```

## 📁 **Project Structure**

### **Core Files**
- `rag-db-pdf.py` - Main CLI application dengan multi-turn conversation
- `rag_pdf_api.py` - RESTful API version (FastAPI)
- `requirements.txt` - Python dependencies
- `.env` - Environment configuration

### **Utility Scripts**
- `create_sample_docs.py` - Generate sample documents
- `create_sample_pdfs.py` - Create sample PDF files
- `txt_to_pdf.py` - Convert text files to PDF
- `demo_conversation.py` - Demo script untuk conversation features
- `test_conversation_simple.py` - Simple conversation test
- `quick_test.py` - API test script
- `start_api.sh` - API startup script

### **Documentation**
- `README_API_SUCCESS.md` - API implementation success guide
- `README_PDF.md` - PDF processing documentation
- `README_CONVERSATION.md` - Multi-turn conversation guide
- `CONVERSATION_COMPLETE.md` - Complete conversation features

### **Data Directories**
- `pdf_documents/` - Source PDF files
- `uploads/` - API uploaded files
- `chroma_pdf_db/` - ChromaDB vector database
- `.venv/` - Python virtual environment

## 🔧 **Features**

### **Document Processing**
- ✅ Multiple PDF file support
- ✅ Text extraction (PyMuPDF + PyPDF2)
- ✅ Smart text chunking
- ✅ OpenAI embeddings
- ✅ MongoDB storage

### **Vector Search**
- ✅ ChromaDB integration
- ✅ Semantic similarity search
- ✅ Configurable result count
- ✅ Source attribution

### **AI-Powered Q&A**
- ✅ OpenAI GPT integration
- ✅ Context-aware responses
- ✅ Multi-turn conversation support
- ✅ Follow-up question detection

### **RESTful API**
- ✅ FastAPI framework
- ✅ Auto-generated documentation (Swagger)
- ✅ File upload endpoints
- ✅ Conversation management
- ✅ Health monitoring
- ✅ CORS support

### **Conversation Management**
- ✅ Session persistence
- ✅ History tracking (up to 10 turns)
- ✅ Context window (3 recent exchanges)
- ✅ Save/load conversations
- ✅ Export functionality

## 🎯 **Usage Examples**

### **CLI Multi-Turn Conversation**
```
1. Upload PDFs → Menu 1: Ingest PDF Documents
2. Build Vector Store → Menu 2: Build ChromaDB Vector Store  
3. Start Conversation → Menu 3: Tanya Jawab dengan PDF

Example flow:
Q1: "Apa itu Python?"
A1: [Detailed answer about Python...]

Q2: "Jelaskan lebih detail tentang fitur-fiturnya"
A2: [Contextual follow-up answer...]

Q3: "Berikan contoh untuk machine learning"
A3: [Specific ML examples with Python...]
```

### **API Usage**
```bash
# Upload PDF
curl -X POST "http://127.0.0.1:8000/upload" \
  -F "files=@document.pdf"

# Ingest documents
curl -X POST "http://127.0.0.1:8000/ingest" \
  -H "Content-Type: application/json" \
  -d '{"folder_path": "uploads"}'

# Build vector store
curl -X POST "http://127.0.0.1:8000/build-vectorstore"

# Ask question
curl -X POST "http://127.0.0.1:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "Apa isi dokumen?", "max_results": 3}'

# Follow-up question
curl -X POST "http://127.0.0.1:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "Jelaskan lebih detail", "conversation_id": "uuid"}'
```

## 🛠️ **Configuration**

### **Environment Variables (.env)**
```bash
# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key
OPENAI_API_BASE=https://api.openai.com/v1
MODEL_NAME=gpt-4o-mini
MODEL_TEMPERATURE=0
MODEL_MAX_TOKENS=2048

# MongoDB Configuration  
MONGO_URI=mongodb://user:pass@host:port/database?authSource=admin

# API Configuration (optional)
API_HOST=0.0.0.0
API_PORT=8000
```

### **Customization**
```python
# rag-db-pdf.py configuration
PDF_FOLDER = "pdf_documents"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
MAX_CONVERSATION_HISTORY = 10
CONVERSATION_CONTEXT_WINDOW = 3
```

## 🔍 **API Endpoints**

### **System Health**
- `GET /` - API information
- `GET /health` - System health check
- `GET /stats` - System statistics
- `GET /debug` - Debug information

### **Document Management**
- `POST /upload` - Upload PDF files
- `POST /ingest` - Process PDF documents
- `POST /build-vectorstore` - Build ChromaDB

### **Question Answering**
- `POST /ask` - Ask questions (supports multi-turn)
- `GET /conversations` - List conversations
- `GET /conversations/{id}` - Get conversation history
- `DELETE /conversations/{id}` - Delete conversation

## 🧪 **Testing**

### **Test API**
```bash
python quick_test.py
```

### **Test Conversation**
```bash
python test_conversation_simple.py
```

### **Demo Conversation Features**
```bash
python demo_conversation.py
```

## 🚦 **Troubleshooting**

### **Common Issues**

**MongoDB Connection Failed**
- Check MONGO_URI in .env
- System will fallback to local MongoDB if remote fails

**OpenAI API Error**
- Verify OPENAI_API_KEY in .env
- Check API quota and billing

**ChromaDB Not Found**
- Run "Build ChromaDB Vector Store" first
- Ensure documents are ingested

**PDF Processing Failed**
- Check PDF file integrity
- Ensure PDF contains extractable text

### **Debug Commands**
```bash
# Check API health
curl http://127.0.0.1:8000/health

# Get debug information  
curl http://127.0.0.1:8000/debug

# View system stats
curl http://127.0.0.1:8000/stats
```

## 📈 **Performance Tips**

1. **Document Processing**: Process PDFs in batches
2. **Vector Search**: Adjust `max_results` based on needs
3. **Conversation**: Use `clear` command for new topics
4. **API**: Enable caching for production
5. **Memory**: Monitor conversation history size

## 🔒 **Security Notes**

- Never commit `.env` file to version control
- Use environment variables for sensitive data
- Configure CORS appropriately for production
- Implement authentication for production API
- Validate file uploads and sizes

## 🎉 **Success Metrics**

✅ **Multi-PDF Processing**: Support untuk multiple file upload  
✅ **Multi-Turn Conversation**: Context-aware follow-up questions  
✅ **RESTful API**: Complete FastAPI implementation  
✅ **Vector Search**: Semantic similarity dengan ChromaDB  
✅ **AI Integration**: OpenAI GPT untuk natural language responses  
✅ **Production Ready**: Error handling, logging, documentation  

---

## 📞 **Support**

Untuk issues atau pertanyaan:
1. Check logs dan error messages
2. Gunakan `/debug` endpoint untuk system info
3. Test dengan script yang disediakan
4. Review dokumentasi ini

**Status: ✅ PRODUCTION READY**
