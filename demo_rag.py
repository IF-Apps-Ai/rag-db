#!/usr/bin/env python3
"""
Demo script untuk RAG System
Menunjukkan cara menggunakan sistem tanpa interaksi manual
"""
import os
from pymongo import MongoClient
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Konfigurasi
client_openai = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE")
)

MONGO_URI = os.getenv("MONGO_URI")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")

def demo_rag_query(query, kategori_filter=None):
    """Demonstrasi query ke RAG system"""
    
    print(f"\n❓ Pertanyaan: {query}")
    if kategori_filter:
        print(f"📂 Filter kategori: {kategori_filter}")
    
    try:
        # Setup koneksi
        mongo_client = MongoClient(MONGO_URI)
        db = mongo_client["RAG_Demo"]
        collection = db["docs"]
        
        # Setup ChromaDB
        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
        embeddings = OpenAIEmbeddings()
        chroma = Chroma(persist_directory="chroma_db", embedding_function=embeddings)
        
        # Search dokumen yang relevan
        filter_ = {"kategori": kategori_filter} if kategori_filter else None
        results = chroma.similarity_search(query, k=2, filter=filter_)
        
        if not results:
            print("⚠️ Tidak ada dokumen yang cocok.")
            return
        
        # Ambil detail dokumen dari MongoDB
        doc_ids = [res.metadata["doc_id"] for res in results]
        full_docs = list(collection.find({"doc_id": {"$in": doc_ids}}))
        context = "\n".join([doc["text"] for doc in full_docs])
        
        print(f"🔍 Ditemukan {len(results)} dokumen relevan:")
        for i, doc in enumerate(full_docs, 1):
            print(f"   {i}. {doc['text'][:100]}...")
        
        # Generate jawaban
        prompt = f"Jawablah berdasarkan teks berikut:\n\n{context}\n\nPertanyaan: {query}"
        
        response = client_openai.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=2048
        )
        
        print(f"\n🤖 Jawaban:\n{response.choices[0].message.content}")
        
        mongo_client.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Demo berbagai jenis pertanyaan"""
    
    print("🚀 RAG System Demo")
    print("=" * 50)
    
    # Demo pertanyaan umum
    demo_rag_query("Apa itu Python?")
    
    # Demo pertanyaan tentang teknologi
    demo_rag_query("Bagaimana cara kerja machine learning?")
    
    # Demo pertanyaan dengan filter kategori
    demo_rag_query("Jelaskan tentang database", "umum")
    
    # Demo pertanyaan tentang API
    demo_rag_query("Apa kegunaan API?")
    
    print("\n✨ Demo selesai!")
    print("\nUntuk menggunakan secara interaktif, jalankan:")
    print("python rag-db.py")

if __name__ == "__main__":
    main()
