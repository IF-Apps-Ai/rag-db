#!/usr/bin/env python3
import os
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_mongodb_connection():
    mongo_uri = os.getenv("MONGO_URI")
    
    if not mongo_uri:
        print("❌ MONGO_URI tidak ditemukan di file .env")
        return False
    
    print(f"🔍 Testing koneksi ke: {mongo_uri.split('@')[1] if '@' in mongo_uri else mongo_uri}")
    
    try:
        # Test dengan timeout yang lebih pendek
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        
        # Test connection
        client.admin.command('ping')
        print("✅ Koneksi MongoDB berhasil!")
        
        # List databases untuk verifikasi
        databases = client.list_database_names()
        print(f"📦 Databases tersedia: {databases}")
        
        client.close()
        return True
        
    except ServerSelectionTimeoutError as e:
        print(f"❌ Timeout: Server MongoDB tidak dapat dijangkau")
        print(f"   Pesan error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error koneksi MongoDB: {e}")
        return False

def suggest_alternatives():
    print("\n💡 Saran solusi:")
    print("1. ✅ Gunakan MongoDB lokal dengan Docker:")
    print("   docker run -d -p 27017:27017 --name mongodb mongo:latest")
    print("   Ubah LOGGER_MONGO_URI ke: mongodb://localhost:27017/RAG_Demo")
    print()
    print("2. ✅ Gunakan MongoDB Atlas (cloud) gratis:")
    print("   - Daftar di https://cloud.mongodb.com")
    print("   - Buat cluster gratis")
    print("   - Dapatkan connection string")
    print()
    print("3. ✅ Periksa firewall/network:")
    print("   - Pastikan port 27005 terbuka")
    print("   - Periksa apakah server MongoDB berjalan")
    print("   - Verify kredensial username/password")

if __name__ == "__main__":
    print("🧪 MongoDB Connection Test")
    print("=" * 30)
    
    success = test_mongodb_connection()
    
    if not success:
        suggest_alternatives()
