# RAG (Retrieval Augmented Generation) System

Sistem RAG yang mengintegrasikan MongoDB dan ChromaDB untuk menyimpan dan mencari dokumen menggunakan embeddings OpenAI.

## Fitur

- 📄 Import dokumen dari file teks
- 🧠 Membuat embeddings menggunakan OpenAI
- 🗃️ Menyimpan dokumen dan embeddings di MongoDB
- 🔍 Vector search menggunakan ChromaDB
- 🏷️ Filter berdasarkan kategori dokumen
- 🤖 Q&A menggunakan GPT model

## Konfigurasi

1. Buat file `.env` dengan konfigurasi berikut:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_API_BASE=https://api.openai.com/v1
MODEL_NAME=gpt-4o-mini
MODEL_TEMPERATURE=0
MODEL_MAX_TOKENS=2048
LOGGER_MONGO_URI=your_mongodb_connection_string_here
```

1. Install dependencies:

```bash
pip install -r requirements.txt
```

1. Buat file `documents.txt` dengan konten dokumen (satu dokumen per baris).

## Cara Menjalankan

```bash
python rag-db.py
```

### Untuk Demo Non-Interaktif

```bash
python demo_rag.py
```

### Untuk Test Sistem

```bash
python test_rag.py
python test_mongodb.py  # Test koneksi MongoDB
```

## Troubleshooting MongoDB

Jika terjadi error "Connection refused" pada MongoDB:

### 1. MongoDB Remote Tidak Dapat Dijangkau
```bash
# Script akan otomatis fallback ke MongoDB lokal
```

### 2. Setup MongoDB Lokal dengan Docker
```bash
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

### 3. Setup MongoDB Lokal (Ubuntu/Debian)
```bash
sudo apt-get install mongodb
sudo systemctl start mongodb
```

### 4. Menggunakan MongoDB Atlas (Cloud)
1. Daftar di https://cloud.mongodb.com
2. Buat cluster gratis
3. Update `LOGGER_MONGO_URI` di file `.env`

## Struktur Data

### MongoDB Document

```json
{
  "doc_id": "dok_0",
  "text": "Konten dokumen...",
  "kategori": "akademik",
  "embedding": [0.1, 0.2, ...]
}
```

### ChromaDB Metadata

- `doc_id`: ID dokumen
- `kategori`: Kategori dokumen (akademik/umum)

## Error Handling

- ✅ Validasi environment variables
- ✅ Test koneksi MongoDB
- ✅ Error handling untuk OpenAI API
- ✅ Validasi file input
- ✅ Graceful shutdown dengan Ctrl+C

## Dependencies

- `openai`: OpenAI API client
- `pymongo`: MongoDB client
- `langchain-openai`: LangChain OpenAI integration
- `langchain-chroma`: LangChain ChromaDB integration
- `python-dotenv`: Environment variables loader
- `chromadb`: Vector database
