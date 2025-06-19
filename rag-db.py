import os
from pymongo import MongoClient
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# === Konfigurasi ===
client_openai = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE")
)

MONGO_URI = os.getenv("MONGO_URI")
MONGO_URI_LOCAL = "mongodb://localhost:27017"  # Fallback ke MongoDB lokal
DB_NAME = "RAG_Demo"
COLLECTION_NAME = "docs"
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
MODEL_TEMPERATURE = float(os.getenv("MODEL_TEMPERATURE", "0"))
MODEL_MAX_TOKENS = int(os.getenv("MODEL_MAX_TOKENS", "2048"))

# === Koneksi MongoDB ===
def connect_mongodb():
    """Mencoba koneksi ke MongoDB dengan fallback ke lokal"""
    
    # Coba koneksi ke server remote terlebih dahulu
    if MONGO_URI:
        try:
            print(f"🔍 Mencoba koneksi ke MongoDB remote...")
            mongo_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
            mongo_client.admin.command('ping')
            print("✅ Koneksi MongoDB remote berhasil.")
            return mongo_client
        except Exception as e:
            print(f"⚠️ MongoDB remote tidak dapat dijangkau: {e}")
    
    # Fallback ke MongoDB lokal
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

# === Fungsi Membuat Embedding ===
def get_embedding(text):
    try:
        result = client_openai.embeddings.create(
            input=[text],
            model="text-embedding-3-small"
        )
        return result.data[0].embedding
    except Exception as e:
        print(f"❌ Error creating embedding: {e}")
        return None

# === Fungsi Menyimpan Dokumen + Embedding ke MongoDB ===
def ingest_documents(filepath):
    if not os.path.exists(filepath):
        print(f"❌ File {filepath} tidak ditemukan.")
        return
        
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            texts = [line.strip() for line in f if line.strip()]
            for i, text in enumerate(texts):
                embedding = get_embedding(text)
                if embedding is None:
                    print(f"⚠️ Gagal membuat embedding untuk dokumen {i}")
                    continue
                    
                doc_kategori = "akademik" if i % 2 == 0 else "umum"  # contoh kategori dummy
                doc_id = f"dok_{i}"
                collection.insert_one({
                    "doc_id": doc_id,
                    "text": text,
                    "kategori": doc_kategori,
                    "embedding": embedding
                })
            print(f"✅ {len(texts)} dokumen berhasil disimpan ke MongoDB.")
    except Exception as e:
        print(f"❌ Error ingesting documents: {e}")

# === Simpan Embedding ke ChromaDB ===
def build_chroma_vectorstore():
    try:
        docs = list(collection.find({}, {"doc_id": 1, "text": 1, "kategori": 1}))
        if not docs:
            print("⚠️ Tidak ada dokumen di MongoDB untuk dibuat ChromaDB.")
            return
            
        texts = [doc["text"] for doc in docs]
        metadatas = [{"doc_id": doc["doc_id"], "kategori": doc["kategori"]} for doc in docs]
        
        # Set OpenAI API key untuk embeddings
        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
        embeddings = OpenAIEmbeddings()
        
        Chroma.from_texts(texts, embeddings, metadatas=metadatas, persist_directory="chroma_db")
        print("✅ ChromaDB telah dibuat dan disimpan.")
    except Exception as e:
        print(f"❌ Error building ChromaDB: {e}")

# === Fungsi Menjawab Pertanyaan Menggunakan Chroma + MongoDB ===
def answer_question(query, top_k=2, kategori_filter=None):
    try:
        # Set OpenAI API key untuk embeddings
        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
        embeddings = OpenAIEmbeddings()
        
        if not os.path.exists("chroma_db"):
            print("⚠️ ChromaDB tidak ditemukan. Pastikan sudah menjalankan build_chroma_vectorstore().")
            return
            
        chroma = Chroma(persist_directory="chroma_db", embedding_function=embeddings)

        filter_ = {"kategori": kategori_filter} if kategori_filter else None
        results = chroma.similarity_search(query, k=top_k, filter=filter_)

        if not results:
            print("⚠️ Tidak ada dokumen yang cocok.")
            return

        doc_ids = [res.metadata["doc_id"] for res in results]
        full_docs = list(collection.find({"doc_id": {"$in": doc_ids}}))
        context = "\n".join([doc["text"] for doc in full_docs])

        prompt = f"Jawablah berdasarkan teks berikut:\n\n{context}\n\nPertanyaan: {query}"

        response = client_openai.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=MODEL_TEMPERATURE,
            max_tokens=MODEL_MAX_TOKENS
        )
        print("\n🤖 Jawaban:\n", response.choices[0].message.content)
    except Exception as e:
        print(f"❌ Error answering question: {e}")

# === Jalankan Script ===
if __name__ == "__main__":
    # Cek apakah semua environment variables tersedia
    required_env = ["OPENAI_API_KEY", "MONGO_URI"]
    missing_env = [env for env in required_env if not os.getenv(env)]
    
    if missing_env:
        print(f"❌ Environment variables tidak ditemukan: {', '.join(missing_env)}")
        print("Pastikan file .env sudah dikonfigurasi dengan benar.")
        exit(1)
    
    try:
        if collection.count_documents({}) == 0:
            print("📄 Tidak ada dokumen di database. Mencari file documents.txt...")
            if not os.path.exists("documents.txt"):
                print("❌ File documents.txt tidak ditemukan.")
                print("Buat file documents.txt dengan konten dokumen (satu dokumen per baris).")
                exit(1)
            
            print("📥 Mengimpor dokumen...")
            ingest_documents("documents.txt")
            print("🔧 Membangun ChromaDB...")
            build_chroma_vectorstore()
        else:
            print(f"✅ Database sudah memiliki {collection.count_documents({})} dokumen.")
            if not os.path.exists("chroma_db"):
                print("🔧 ChromaDB tidak ditemukan, membangun ulang...")
                build_chroma_vectorstore()

        print("\n" + "="*50)
        print("🚀 RAG System siap digunakan!")
        print("="*50)
        
        while True:
            question = input("\n❓ Pertanyaan (atau 'exit' untuk keluar): ")
            if question.lower() in ["exit", "quit", "keluar"]:
                print("👋 Terima kasih telah menggunakan RAG System!")
                break

            kategori = input("📂 Filter kategori (akademik/umum, kosongkan jika tidak ada): ")
            filter_kategori = kategori.strip() if kategori else None

            answer_question(question, top_k=2, kategori_filter=filter_kategori)
            
    except KeyboardInterrupt:
        print("\n\n👋 Program dihentikan oleh user.")
    except Exception as e:
        print(f"❌ Error menjalankan program: {e}")
    finally:
        if 'mongo_client' in locals():
            mongo_client.close()
            print("🔌 Koneksi MongoDB ditutup.")
