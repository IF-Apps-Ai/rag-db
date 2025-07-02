import os
import hashlib
from pathlib import Path
from pymongo import MongoClient
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from openai import OpenAI
import PyPDF2
import fitz  # PyMuPDF
from typing import List, Dict, Any
import json
from datetime import datetime

# Load environment variables
load_dotenv()

# === Konfigurasi ===
client_openai = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE")
)

MONGO_URI = os.getenv("MONGO_URI")
MONGO_URI_LOCAL = "mongodb://localhost:27017"
DB_NAME = "RAG_PDF_Demo"
COLLECTION_NAME = "pdf_docs"
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
MODEL_TEMPERATURE = float(os.getenv("MODEL_TEMPERATURE", "0"))
MODEL_MAX_TOKENS = int(os.getenv("MODEL_MAX_TOKENS", "2048"))

# PDF Configuration
PDF_FOLDER = "pdf_documents"  # Folder yang berisi file PDF
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Conversation Configuration
MAX_CONVERSATION_HISTORY = 10  # Maximum number of previous Q&A pairs to remember
CONVERSATION_CONTEXT_WINDOW = 3  # Number of recent exchanges to include in context

# === Koneksi MongoDB ===
def connect_mongodb():
    """Mencoba koneksi ke MongoDB dengan fallback ke lokal"""
    
    if MONGO_URI:
        try:
            print("🔍 Mencoba koneksi ke MongoDB remote...")
            mongo_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
            mongo_client.admin.command('ping')
            print("✅ Koneksi MongoDB remote berhasil.")
            return mongo_client
        except Exception as e:
            print(f"⚠️ MongoDB remote tidak dapat dijangkau: {e}")
    
    try:
        print("🔍 Mencoba koneksi ke MongoDB lokal...")
        mongo_client = MongoClient(MONGO_URI_LOCAL, serverSelectionTimeoutMS=3000)
        mongo_client.admin.command('ping')
        print("✅ Koneksi MongoDB lokal berhasil.")
        return mongo_client
    except Exception as e:
        print(f"❌ MongoDB lokal juga tidak dapat dijangkau: {e}")
        print("\n💡 Solusi yang bisa dicoba:")
        print("1. Install dan jalankan MongoDB lokal:")
        print("   sudo apt-get install mongodb")
        print("   sudo systemctl start mongodb")
        print("\n2. Atau gunakan Docker:")
        print("   docker run -d -p 27017:27017 --name mongodb mongo:latest")
        print("\n3. Atau gunakan MongoDB Atlas (cloud):")
        print("   https://cloud.mongodb.com")
        return None

# === Setup MongoDB ===
try:
    mongo_client = connect_mongodb()
    if mongo_client is None:
        print("❌ Tidak dapat terhubung ke MongoDB. Program berhenti.")
        exit(1)
    
    db = mongo_client[DB_NAME]
    collection = db[COLLECTION_NAME]
    
except Exception as e:
    print(f"❌ Error setup MongoDB: {e}")
    exit(1)

# === Conversation Manager Class ===
class ConversationManager:
    """
    Mengelola conversation history untuk multi-turn chat
    """
    
    def __init__(self, max_history: int = MAX_CONVERSATION_HISTORY):
        self.conversation_history = []
        self.max_history = max_history
        self.context_window = CONVERSATION_CONTEXT_WINDOW  # Dynamic context window
        self.current_session_id = self._generate_session_id()
        
    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        from datetime import datetime
        return f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def add_exchange(self, question: str, answer: str, sources: List[str] = None):
        """
        Menambahkan Q&A exchange ke history
        """
        exchange = {
            "question": question,
            "answer": answer,
            "sources": sources or [],
            "timestamp": datetime.now().isoformat()
        }
        
        self.conversation_history.append(exchange)
        
        # Keep only recent history
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]
    
    def get_conversation_context(self, num_recent: int = None) -> str:
        """
        Mendapatkan context dari percakapan sebelumnya
        """
        if not self.conversation_history:
            return ""
        
        # Use instance context window if num_recent not specified
        if num_recent is None:
            num_recent = self.context_window
        
        recent_exchanges = self.conversation_history[-num_recent:]
        context_parts = []
        
        for i, exchange in enumerate(recent_exchanges, 1):
            context_parts.append(f"Q{i}: {exchange['question']}")
            context_parts.append(f"A{i}: {exchange['answer']}")
        
        return "\n".join(context_parts)
    
    def get_last_question(self) -> str:
        """Mendapatkan pertanyaan terakhir"""
        if self.conversation_history:
            return self.conversation_history[-1]["question"]
        return ""
    
    def get_last_answer(self) -> str:
        """Mendapatkan jawaban terakhir"""
        if self.conversation_history:
            return self.conversation_history[-1]["answer"]
        return ""
    
    def clear_history(self):
        """Membersihkan history percakapan"""
        self.conversation_history = []
        self.current_session_id = self._generate_session_id()
    
    def save_conversation(self, filename: str = None):
        """
        Menyimpan conversation ke file JSON
        """
        if filename is None:
            filename = f"conversation_{self.current_session_id}.json"
        
        try:
            conversation_data = {
                "session_id": self.current_session_id,
                "history": self.conversation_history,
                "saved_at": datetime.now().isoformat()
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                import json
                json.dump(conversation_data, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Conversation saved to: {filename}")
            
        except Exception as e:
            print(f"❌ Error saving conversation: {e}")
    
    def load_conversation(self, filename: str):
        """
        Memuat conversation dari file JSON
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                import json
                conversation_data = json.load(f)
            
            self.conversation_history = conversation_data.get("history", [])
            self.current_session_id = conversation_data.get("session_id", self._generate_session_id())
            
            print(f"📂 Conversation loaded from: {filename}")
            print(f"   Session ID: {self.current_session_id}")
            print(f"   History entries: {len(self.conversation_history)}")
            
        except Exception as e:
            print(f"❌ Error loading conversation: {e}")
    
    def show_history(self):
        """
        Menampilkan history percakapan
        """
        if not self.conversation_history:
            print("📭 Belum ada history percakapan.")
            return
        
        print(f"💬 Conversation History (Session: {self.current_session_id})")
        print("=" * 60)
        
        for i, exchange in enumerate(self.conversation_history, 1):
            print(f"\n{i}. Q: {exchange['question']}")
            print(f"   A: {exchange['answer'][:200]}{'...' if len(exchange['answer']) > 200 else ''}")
            if exchange.get('sources'):
                print(f"   📚 Sources: {', '.join(exchange['sources'])}")

# Create global conversation manager
conversation_manager = ConversationManager()

# === Fungsi Ekstraksi PDF ===
def extract_text_from_pdf(pdf_path: str, method: str = "pymupdf") -> str:
    """
    Ekstrak teks dari file PDF menggunakan PyMuPDF atau PyPDF2
    """
    try:
        if method == "pymupdf":
            # Menggunakan PyMuPDF (fitz) - lebih baik untuk OCR dan layout kompleks
            doc = fitz.open(pdf_path)
            text = ""
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text += page.get_text() + "\n"
            doc.close()
            return text
        
        elif method == "pypdf2":
            # Menggunakan PyPDF2 - lebih cepat untuk PDF sederhana
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text
            
    except Exception as e:
        print(f"❌ Error extracting text from {pdf_path}: {e}")
        return ""

def get_pdf_files(folder_path: str) -> List[str]:
    """
    Mendapatkan daftar semua file PDF dalam folder
    """
    if not os.path.exists(folder_path):
        print(f"❌ Folder {folder_path} tidak ditemukan.")
        return []
    
    pdf_files = []
    for file in os.listdir(folder_path):
        if file.lower().endswith('.pdf'):
            pdf_files.append(os.path.join(folder_path, file))
    
    return pdf_files

def get_file_hash(file_path: str) -> str:
    """
    Generate hash untuk file untuk mendeteksi perubahan
    """
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# === Fungsi Text Splitting ===
def split_text_into_chunks(text: str, filename: str) -> List[Dict[str, Any]]:
    """
    Membagi teks menjadi chunk-chunk kecil
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
    )
    
    chunks = text_splitter.split_text(text)
    
    # Create documents with metadata
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

# === Fungsi Membuat Embedding ===
def get_embedding(text: str) -> List[float]:
    """
    Membuat embedding untuk teks menggunakan OpenAI
    """
    try:
        result = client_openai.embeddings.create(
            input=[text],
            model="text-embedding-3-small"
        )
        return result.data[0].embedding
    except Exception as e:
        print(f"❌ Error creating embedding: {e}")
        return []

# === Fungsi Ingest PDF Documents ===
def ingest_pdf_documents(folder_path: str = PDF_FOLDER):
    """
    Memproses semua file PDF dalam folder dan menyimpannya ke MongoDB
    """
    if not os.path.exists(folder_path):
        print(f"📁 Membuat folder {folder_path}...")
        os.makedirs(folder_path)
        print(f"✅ Folder {folder_path} telah dibuat.")
        print(f"📋 Silakan masukkan file PDF ke dalam folder {folder_path} dan jalankan lagi.")
        return
    
    pdf_files = get_pdf_files(folder_path)
    
    if not pdf_files:
        print(f"❌ Tidak ada file PDF ditemukan dalam folder {folder_path}")
        return
    
    print(f"📚 Ditemukan {len(pdf_files)} file PDF:")
    for pdf_file in pdf_files:
        print(f"   - {os.path.basename(pdf_file)}")
    
    total_chunks = 0
    processed_files = 0
    
    for pdf_path in pdf_files:
        filename = os.path.basename(pdf_path)
        file_hash = get_file_hash(pdf_path)
        
        # Cek apakah file sudah diproses sebelumnya
        existing_doc = collection.find_one({"filename": filename, "file_hash": file_hash})
        if existing_doc:
            print(f"⏭️ File {filename} sudah diproses sebelumnya, skip...")
            continue
        
        print(f"📖 Memproses file: {filename}")
        
        # Extract text from PDF
        text = extract_text_from_pdf(pdf_path)
        if not text.strip():
            print(f"⚠️ Tidak ada teks yang dapat diekstrak dari {filename}")
            continue
        
        # Split text into chunks
        documents = split_text_into_chunks(text, filename)
        
        # Process each chunk
        chunk_count = 0
        for doc in documents:
            # Create embedding
            embedding = get_embedding(doc["text"])
            if not embedding:
                continue
            
            # Prepare document for MongoDB
            mongo_doc = {
                "doc_id": f"{filename}_chunk_{doc['chunk_id']}",
                "filename": filename,\
                "file_hash": file_hash,
                "text": doc["text"],
                "chunk_id": doc["chunk_id"],
                "source": doc["source"],
                "chunk_size": doc["chunk_size"],
                "embedding": embedding,
                "kategori": "pdf_document"
            }
            
            # Insert to MongoDB
            try:
                collection.insert_one(mongo_doc)
                chunk_count += 1
            except Exception as e:
                print(f"❌ Error inserting chunk {doc['chunk_id']} from {filename}: {e}")
        
        if chunk_count > 0:
            processed_files += 1
            total_chunks += chunk_count
            print(f"✅ {filename}: {chunk_count} chunks berhasil disimpan")
        else:
            print(f"❌ {filename}: Gagal memproses file")
    
    print(f"\n🎉 Selesai! {processed_files} file PDF diproses, total {total_chunks} chunks disimpan.")

# === Fungsi Build ChromaDB ===
def build_chroma_vectorstore():
    """
    Membangun ChromaDB dari dokumen yang ada di MongoDB
    """
    try:
        docs = list(collection.find({}, {"doc_id": 1, "text": 1, "filename": 1, "kategori": 1}))
        if not docs:
            print("❌ Tidak ada dokumen ditemukan di MongoDB.")
            return
        
        print(f"📊 Membangun ChromaDB dari {len(docs)} dokumen...")
        
        texts = [doc["text"] for doc in docs]
        metadatas = [
            {
                "doc_id": doc["doc_id"], 
                "filename": doc["filename"],
                "kategori": doc["kategori"]
            } for doc in docs
        ]
        
        # Set OpenAI API key untuk embeddings
        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        
        # Create ChromaDB
        Chroma.from_texts(
            texts, 
            embeddings, 
            metadatas=metadatas, 
            persist_directory="chroma_pdf_db"
        )
        
        print("✅ ChromaDB telah dibuat dan disimpan di 'chroma_pdf_db'.")
        
    except Exception as e:
        print(f"❌ Error building ChromaDB: {e}")

# === Fungsi Search dan Answer ===
def search_similar_documents(query: str, top_k: int = 3, filename_filter: str = None):
    """
    Mencari dokumen yang mirip berdasarkan query
    """
    try:
        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        
        if not os.path.exists("chroma_pdf_db"):
            print("❌ ChromaDB belum dibuat. Jalankan build_chroma_vectorstore() terlebih dahulu.")
            return []
        
        chroma = Chroma(persist_directory="chroma_pdf_db", embedding_function=embeddings)
        
        # Apply filename filter if specified
        filter_dict = {"filename": filename_filter} if filename_filter else None
        
        results = chroma.similarity_search(query, k=top_k, filter=filter_dict)
        
        return results
        
    except Exception as e:
        print(f"❌ Error searching documents: {e}")
        return []

def answer_question_with_context(query: str, top_k: int = 3, filename_filter: str = None):
    """
    Menjawab pertanyaan berdasarkan dokumen PDF dengan conversation context
    """
    try:
        print(f"🔍 Mencari dokumen relevan untuk: '{query}'")
        
        # Check for conversation context
        conversation_context = conversation_manager.get_conversation_context()
        
        # Enhanced query with conversation context
        enhanced_query = query
        if conversation_context:
            # Check if this is a follow-up question
            follow_up_indicators = [
                "lanjut", "selanjutnya", "lebih detail", "contoh", "bagaimana", 
                "jelaskan lebih", "detail", "itu", "tersebut", "tadi", "sebelumnya"
            ]
            
            is_follow_up = any(indicator in query.lower() for indicator in follow_up_indicators)
            
            if is_follow_up:
                last_question = conversation_manager.get_last_question()
                enhanced_query = f"Berdasarkan pertanyaan sebelumnya '{last_question}', {query}"
                print("🔗 Detected follow-up question, enhancing context...")
        
        # Search similar documents
        results = search_similar_documents(enhanced_query, top_k, filename_filter)
        
        if not results:
            answer = "❌ Tidak ada dokumen relevan ditemukan untuk pertanyaan Anda."
            conversation_manager.add_exchange(query, answer, [])
            print(answer)
            return
        
        # Get document IDs and fetch full documents from MongoDB
        doc_ids = [res.metadata["doc_id"] for res in results]
        full_docs = list(collection.find({"doc_id": {"$in": doc_ids}}))
        
        # Prepare context
        context_parts = []
        source_files = set()
        
        for doc in full_docs:
            filename = doc.get("filename", "Unknown")
            text = doc.get("text", "")
            context_parts.append(f"[File: {filename}]\n{text}")
            source_files.add(filename)
        
        document_context = "\n\n---\n\n".join(context_parts)
        
        # Build comprehensive prompt with conversation context
        prompt_parts = []
        
        if conversation_context:
            prompt_parts.append("CONVERSATION HISTORY:")
            prompt_parts.append(conversation_context)
            prompt_parts.append("\n" + "="*50 + "\n")
        
        prompt_parts.append("DOKUMEN REFERENSI:")
        prompt_parts.append(document_context)
        prompt_parts.append("\n" + "="*50 + "\n")
        
        if conversation_context:
            prompt_parts.append(f"PERTANYAAN SAAT INI: {query}")
            prompt_parts.append("\nInstruksi: Jawab pertanyaan saat ini dengan mempertimbangkan konteks percakapan sebelumnya. Jika pertanyaan ini adalah lanjutan dari pertanyaan sebelumnya, berikan jawaban yang konsisten dan terhubung. Gunakan informasi dari dokumen referensi untuk memberikan jawaban yang akurat dan lengkap.")
        else:
            prompt_parts.append(f"PERTANYAAN: {query}")
            prompt_parts.append("\nInstruksi: Berdasarkan dokumen referensi di atas, jawab pertanyaan dengan akurat dan lengkap.")
        
        prompt_parts.append("\nJAWABAN:")
        
        full_prompt = "\n".join(prompt_parts)
        
        # Generate answer using OpenAI
        response = client_openai.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": full_prompt}],
            temperature=MODEL_TEMPERATURE,
            max_tokens=MODEL_MAX_TOKENS
        )
        
        answer = response.choices[0].message.content
        
        # Store in conversation history
        sources = list(source_files)
        conversation_manager.add_exchange(query, answer, sources)
        
        print("\n🤖 Jawaban:")
        print(f"{answer}")
        
        print("\n📚 Sumber dokumen:")
        for doc in full_docs:
            filename = doc.get("filename", "Unknown")
            chunk_id = doc.get("chunk_id", 0)
            print(f"   - {filename} (chunk {chunk_id})")
        
        # Show conversation context info
        if conversation_context:
            print(f"\n💬 Context: Menggunakan {len(conversation_manager.conversation_history)} percakapan sebelumnya")
            
    except Exception as e:
        error_msg = f"❌ Error answering question: {e}"
        print(error_msg)
        conversation_manager.add_exchange(query, error_msg, [])

def answer_question(query: str, top_k: int = 3, filename_filter: str = None):
    """
    Wrapper untuk backward compatibility - now uses conversation context
    """
    answer_question_with_context(query, top_k, filename_filter)

# === Utility Functions ===
def list_processed_files():
    """
    Menampilkan daftar file PDF yang sudah diproses
    """
    try:
        pipeline = [
            {"$group": {
                "_id": "$filename",
                "chunks": {"$sum": 1},
                "file_hash": {"$first": "$file_hash"}
            }},
            {"$sort": {"_id": 1}}
        ]
        
        files = list(collection.aggregate(pipeline))
        
        if not files:
            print("📭 Belum ada file PDF yang diproses.")
            return
        
        print(f"📚 File PDF yang sudah diproses ({len(files)} file):")
        total_chunks = 0
        for file_info in files:
            filename = file_info["_id"]
            chunks = file_info["chunks"]
            total_chunks += chunks
            print(f"   - {filename}: {chunks} chunks")
        
        print(f"📊 Total chunks: {total_chunks}")
        
    except Exception as e:
        print(f"❌ Error listing files: {e}")

def delete_file_from_db(filename: str):
    """
    Menghapus semua chunks dari file tertentu
    """
    try:
        result = collection.delete_many({"filename": filename})
        if result.deleted_count > 0:
            print(f"✅ {result.deleted_count} chunks dari file '{filename}' telah dihapus.")
        else:
            print(f"❌ File '{filename}' tidak ditemukan dalam database.")
    except Exception as e:
        print(f"❌ Error deleting file: {e}")

# === Menu Interface ===
def show_menu():
    """
    Menampilkan menu pilihan
    """
    print("\n" + "="*50)
    print("🤖 RAG PDF System - Menu Utama")
    print("="*50)
    print("1. 📚 Ingest PDF Documents")
    print("2. 🔍 Build ChromaDB Vector Store")
    print("3. ❓ Tanya Jawab dengan PDF")
    print("4. 📋 Lihat File yang Sudah Diproses")
    print("5. 🗑️  Hapus File dari Database")
    print("6. 🔍 Cari Dokumen Mirip")
    print("7. 💬 Kelola Conversation")
    print("0. 🚪 Keluar")
    print("="*50)

def show_conversation_menu():
    """
    Menampilkan menu conversation management
    """
    print("\n" + "="*40)
    print("💬 Conversation Management")
    print("="*40)
    print("1. 📜 Lihat History Percakapan")
    print("2. 🗑️  Clear History")
    print("3. 💾 Simpan Conversation")
    print("4. 📂 Load Conversation")
    print("5. ⚙️  Set Context Window")
    print("0. 🔙 Kembali ke Menu Utama")
    print("="*40)

# === Main Function ===
if __name__ == "__main__":
    # Validasi environment variables
    required_env = ["OPENAI_API_KEY", "MONGO_URI"]
    missing_env = [env for env in required_env if not os.getenv(env)]
    
    if missing_env:
        print(f"❌ Environment variables tidak ditemukan: {', '.join(missing_env)}")
        print("Pastikan file .env sudah dikonfigurasi dengan benar.")
        exit(1)
    
    print("🚀 RAG PDF System dimulai...")
    print(f"📁 Folder PDF: {PDF_FOLDER}")
    print(f"🗄️ Database: {DB_NAME}")
    print(f"📊 Collection: {COLLECTION_NAME}")
    
    try:
        while True:
            show_menu()
            choice = input("Pilih menu (0-6): ").strip()
            
            if choice == "1":
                print("\n📚 Memproses file PDF...")
                ingest_pdf_documents()
                
            elif choice == "2":
                print("\n🔍 Membangun ChromaDB...")
                build_chroma_vectorstore()
                
            elif choice == "3":
                print("\n❓ Mode Tanya Jawab Multi-Turn")
                print("💡 Tips: Anda dapat mengajukan pertanyaan lanjutan yang terkait!")
                print("   Contoh: 'Jelaskan lebih detail', 'Berikan contoh', 'Bagaimana cara implementasinya?'")
                
                while True:
                    query = input("\nMasukkan pertanyaan (atau 'back' untuk kembali): ").strip()
                    if query.lower() == 'back':
                        break
                    if query.lower() == 'history':
                        conversation_manager.show_history()
                        continue
                    if query.lower() == 'clear':
                        conversation_manager.clear_history()
                        print("🗑️ History percakapan telah dibersihkan.")
                        continue
                    if query:
                        # Optional: filter by filename
                        filename_filter = input("Filter by filename (optional, tekan Enter untuk skip): ").strip()
                        filename_filter = filename_filter if filename_filter else None
                        
                        answer_question_with_context(query, top_k=3, filename_filter=filename_filter)
                        
            elif choice == "4":
                print("\n📋 File yang sudah diproses:")
                list_processed_files()
                
            elif choice == "5":
                print("\n🗑️ Hapus file dari database")
                list_processed_files()
                filename = input("Masukkan nama file yang ingin dihapus: ").strip()
                if filename:
                    confirm = input(f"Yakin ingin menghapus '{filename}'? (y/N): ").strip().lower()
                    if confirm == 'y':
                        delete_file_from_db(filename)
                        
            elif choice == "6":
                print("\n🔍 Cari dokumen mirip")
                query = input("Masukkan query pencarian: ").strip()
                if query:
                    results = search_similar_documents(query, top_k=5)
                    if results:
                        print(f"\n📄 Ditemukan {len(results)} dokumen mirip:")
                        for i, result in enumerate(results, 1):
                            filename = result.metadata.get("filename", "Unknown")
                            doc_id = result.metadata.get("doc_id", "Unknown")
                            preview = result.page_content[:200] + "..." if len(result.page_content) > 200 else result.page_content
                            print(f"\n{i}. File: {filename}")
                            print(f"   ID: {doc_id}")
                            print(f"   Preview: {preview}")
                    else:
                        print("❌ Tidak ada dokumen mirip ditemukan.")
            
            elif choice == "7":
                print("\n💬 Conversation Management")
                while True:
                    show_conversation_menu()
                    conv_choice = input("Pilih menu conversation (0-5): ").strip()
                    
                    if conv_choice == "1":
                        conversation_manager.show_history()
                        
                    elif conv_choice == "2":
                        confirm = input("Yakin ingin clear history? (y/N): ").strip().lower()
                        if confirm == 'y':
                            conversation_manager.clear_history()
                            print("🗑️ History percakapan telah dibersihkan.")
                            
                    elif conv_choice == "3":
                        filename = input("Nama file untuk menyimpan (tekan Enter untuk default): ").strip()
                        if filename:
                            conversation_manager.save_conversation(filename)
                        else:
                            conversation_manager.save_conversation()
                            
                    elif conv_choice == "4":
                        filename = input("Nama file untuk dimuat: ").strip()
                        if filename and os.path.exists(filename):
                            conversation_manager.load_conversation(filename)
                        else:
                            print("❌ File tidak ditemukan.")
                            
                    elif conv_choice == "5":
                        try:
                            current_window = conversation_manager.max_history if hasattr(conversation_manager, 'context_window') else CONVERSATION_CONTEXT_WINDOW
                            new_window = int(input(f"Context window saat ini: {current_window}. Masukkan nilai baru (1-10): "))
                            if 1 <= new_window <= 10:
                                # Update conversation manager's context window
                                conversation_manager.context_window = new_window
                                print(f"✅ Context window diubah menjadi: {new_window}")
                            else:
                                print("❌ Nilai harus antara 1-10.")
                        except ValueError:
                            print("❌ Masukkan nilai numerik yang valid.")
                            
                    elif conv_choice == "0":
                        break
                        
                    else:
                        print("❌ Pilihan tidak valid. Silakan pilih 0-5.")
                        
            elif choice == "0":
                print("👋 Terima kasih! Program selesai.")
                break
                
            else:
                print("❌ Pilihan tidak valid. Silakan pilih 0-6.")
                
    except KeyboardInterrupt:
        print("\n\n🛑 Program dihentikan oleh user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        if 'mongo_client' in locals():
            mongo_client.close()
            print("🔌 Koneksi MongoDB ditutup.")
