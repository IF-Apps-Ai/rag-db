#!/usr/bin/env python3
"""
Demo script untuk RAG PDF System
Demonstrasi penggunaan sistem tanpa interaksi manual
"""
import os
import sys
sys.path.append('/workspaces/rag-db')

from dotenv import load_dotenv
load_dotenv()

def demo_rag_pdf_system():
    """
    Demo RAG PDF system
    """
    print("🚀 RAG PDF System Demo")
    print("=" * 50)
    
    # Import functions from main script
    try:
        from pymongo import MongoClient
        from langchain_chroma import Chroma
        from langchain_openai import OpenAIEmbeddings
        from openai import OpenAI
        import fitz  # PyMuPDF
        
        print("✅ All dependencies imported successfully")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return
    
    # Check environment variables
    required_vars = ["OPENAI_API_KEY", "MONGO_URI"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing environment variables: {missing_vars}")
        return
    
    print("✅ Environment variables configured")
    
    # Check PDF folder
    pdf_folder = "pdf_documents"
    if not os.path.exists(pdf_folder):
        print(f"❌ PDF folder '{pdf_folder}' not found")
        return
    
    # List PDF files
    pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith('.pdf')]
    if not pdf_files:
        print(f"❌ No PDF files found in '{pdf_folder}'")
        return
    
    print(f"✅ Found {len(pdf_files)} PDF files:")
    for pdf_file in pdf_files:
        print(f"   - {pdf_file}")
    
    # Test PDF extraction
    print(f"\n🔍 Testing PDF extraction...")
    sample_pdf = os.path.join(pdf_folder, pdf_files[0])
    
    try:
        # Test PyMuPDF extraction
        doc = fitz.open(sample_pdf)
        text = ""
        for page_num in range(min(2, len(doc))):  # First 2 pages only
            page = doc.load_page(page_num)
            text += page.get_text()
        doc.close()
        
        if text.strip():
            print(f"✅ Successfully extracted text from {pdf_files[0]}")
            print(f"   Characters extracted: {len(text)}")
            print(f"   Preview: {text[:200]}...")
        else:
            print(f"⚠️ No text extracted from {pdf_files[0]}")
            
    except Exception as e:
        print(f"❌ Error extracting PDF: {e}")
    
    # Test MongoDB connection
    print(f"\n🗄️ Testing MongoDB connection...")
    try:
        mongo_uri = os.getenv("MONGO_URI")
        mongo_client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        mongo_client.admin.command('ping')
        print("✅ MongoDB connection successful")
        
        # Check existing documents
        db = mongo_client["RAG_PDF_Demo"]
        collection = db["pdf_docs"]
        doc_count = collection.count_documents({})
        print(f"📊 Documents in database: {doc_count}")
        
        mongo_client.close()
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
    
    # Test OpenAI API
    print(f"\n🤖 Testing OpenAI API...")
    try:
        client_openai = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE")
        )
        
        # Test embedding
        result = client_openai.embeddings.create(
            input=["Test embedding for RAG PDF"],
            model="text-embedding-3-small"
        )
        
        if result.data[0].embedding:
            print("✅ OpenAI embeddings working")
            print(f"   Embedding dimension: {len(result.data[0].embedding)}")
        
    except Exception as e:
        print(f"❌ OpenAI API error: {e}")
    
    # Test ChromaDB
    print(f"\n🔍 Testing ChromaDB...")
    chroma_dir = "chroma_pdf_db"
    if os.path.exists(chroma_dir):
        try:
            os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
            embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
            chroma = Chroma(persist_directory=chroma_dir, embedding_function=embeddings)
            
            # Test search
            results = chroma.similarity_search("Python programming", k=1)
            if results:
                print("✅ ChromaDB search working")
                print(f"   Found {len(results)} results")
                print(f"   Sample result: {results[0].page_content[:100]}...")
            else:
                print("⚠️ ChromaDB search returned no results")
                
        except Exception as e:
            print(f"❌ ChromaDB error: {e}")
    else:
        print("⚠️ ChromaDB not found - need to build vector store first")
    
    print(f"\n🎯 Demo Summary:")
    print("=" * 30)
    print("✅ RAG PDF System components tested")
    print("📋 Next steps:")
    print("   1. Run: python rag-db-pdf.py")
    print("   2. Choose menu 1 to ingest PDFs")
    print("   3. Choose menu 2 to build ChromaDB")
    print("   4. Choose menu 3 to start asking questions!")
    print("\n🚀 RAG PDF System is ready to use!")

def demo_sample_queries():
    """
    Demo beberapa sample queries
    """
    print("\n🔍 Sample Queries for RAG PDF System:")
    print("=" * 40)
    
    sample_queries = [
        "Apa itu Python dan fitur-fitur utamanya?",
        "Jelaskan tentang machine learning dan jenisnya",
        "Bagaimana cara kerja database relational?",
        "Apa saja framework populer untuk web development?",
        "Sebutkan algoritma machine learning untuk classification",
        "Bagaimana cara optimasi performa database?",
        "Apa perbedaan frontend dan backend development?",
        "Jelaskan tentang NoSQL database"
    ]
    
    for i, query in enumerate(sample_queries, 1):
        print(f"{i}. {query}")
    
    print("\n💡 Tips:")
    print("- Gunakan pertanyaan spesifik untuk hasil yang lebih akurat")
    print("- Filter berdasarkan filename untuk fokus pada dokumen tertentu")
    print("- Sistem akan mencari dan menggabungkan informasi dari multiple PDF")

if __name__ == "__main__":
    demo_rag_pdf_system()
    demo_sample_queries()
