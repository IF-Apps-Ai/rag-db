#!/usr/bin/env python3
"""
Test script untuk RAG system
"""
import os
import sys
sys.path.append('/workspaces/rag-db')

from dotenv import load_dotenv
load_dotenv()

# Import fungsi dari script utama
from pymongo import MongoClient
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI

def test_rag_functionality():
    """Test basic RAG functionality"""
    
    print("🧪 Testing RAG System")
    print("=" * 30)
    
    # Test MongoDB connection
    MONGO_URI = os.getenv("MONGO_URI")
    if MONGO_URI:
        try:
            mongo_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
            mongo_client.admin.command('ping')
            print("✅ MongoDB connection: OK")
            
            # Check documents count
            db = mongo_client["RAG_Demo"]
            collection = db["docs"]
            doc_count = collection.count_documents({})
            print(f"✅ Documents in MongoDB: {doc_count}")
            
            mongo_client.close()
        except Exception as e:
            print(f"❌ MongoDB test failed: {e}")
            return False
    
    # Test ChromaDB
    try:
        if os.path.exists("chroma_db"):
            os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
            embeddings = OpenAIEmbeddings()
            chroma = Chroma(persist_directory="chroma_db", embedding_function=embeddings)
            
            # Test search
            results = chroma.similarity_search("Python", k=1)
            if results:
                print("✅ ChromaDB search: OK")
                print(f"   Sample result: {results[0].page_content[:100]}...")
            else:
                print("⚠️ ChromaDB search: No results")
        else:
            print("⚠️ ChromaDB directory not found")
    except Exception as e:
        print(f"❌ ChromaDB test failed: {e}")
    
    # Test OpenAI API
    try:
        client_openai = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE")
        )
        
        # Test simple embedding
        result = client_openai.embeddings.create(
            input=["Test embedding"],
            model="text-embedding-3-small"
        )
        
        if result.data[0].embedding:
            print("✅ OpenAI embeddings: OK")
        
        # Test chat completion
        response = client_openai.chat.completions.create(
            model=os.getenv("MODEL_NAME", "gpt-4o-mini"),
            messages=[{"role": "user", "content": "Say 'test successful'"}],
            max_tokens=10
        )
        
        if response.choices[0].message.content:
            print("✅ OpenAI chat: OK")
            
    except Exception as e:
        print(f"❌ OpenAI API test failed: {e}")
    
    print("\n🎉 RAG System test completed!")

if __name__ == "__main__":
    test_rag_functionality()
