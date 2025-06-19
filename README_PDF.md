# RAG PDF System

Sistem RAG (Retrieval Augmented Generation) yang dapat memproses dan mencari informasi dari banyak file PDF dalam satu folder.

## 🚀 Fitur Utama

- 📄 **Multi-PDF Processing**: Memproses banyak file PDF dalam satu folder
- 🔍 **Intelligent Chunking**: Membagi dokumen PDF menjadi chunk-chunk yang optimal
- 🧠 **Semantic Search**: Pencarian berdasarkan makna menggunakan embeddings OpenAI
- 💾 **Database Storage**: Menyimpan dokumen dan metadata di MongoDB
- ⚡ **Vector Database**: Menggunakan ChromaDB untuk pencarian cepat
- 🎯 **Smart Q&A**: Menjawab pertanyaan berdasarkan konten PDF
- 🏷️ **File Filtering**: Filter pencarian berdasarkan nama file
- 🔄 **Incremental Processing**: Hanya memproses file PDF yang berubah

## 📋 Prerequisites

### Environment Variables (.env)
```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_API_BASE=https://api.openai.com/v1
MODEL_NAME=gpt-4o-mini
MODEL_TEMPERATURE=0
MODEL_MAX_TOKENS=2048
MONGO_URI=your_mongodb_connection_string_here
```

### Dependencies
```bash
pip install -r requirements.txt
```

**Additional PDF Dependencies:**
- PyPDF2>=3.0.0
- PyMuPDF>=1.23.0
- langchain-text-splitters>=0.0.1
- reportlab>=4.0.0 (untuk konversi TXT ke PDF)

## 📁 Setup Folder PDF

1. Buat folder `pdf_documents` (otomatis dibuat jika belum ada)
2. Masukkan file PDF ke dalam folder tersebut
3. Jalankan script untuk memproses PDF

### Contoh Struktur Folder:
```
rag-db/
├── pdf_documents/
│   ├── python_guide.pdf
│   ├── machine_learning_basics.pdf
│   ├── database_fundamentals.pdf
│   └── web_development_guide.pdf
├── rag-db-pdf.py
├── .env
└── requirements.txt
```

## 🎮 Cara Penggunaan

### Menjalankan Sistem RAG PDF
```bash
python rag-db-pdf.py
```

### Menu Interaktif:
```
🤖 RAG PDF System - Menu Utama
==================================================
1. 📚 Ingest PDF Documents
2. 🔍 Build ChromaDB Vector Store  
3. ❓ Tanya Jawab dengan PDF
4. 📋 Lihat File yang Sudah Diproses
5. 🗑️  Hapus File dari Database
6. 🔍 Cari Dokumen Mirip
0. 🚪 Keluar
==================================================
```

### Workflow Penggunaan:

1. **Ingest PDF Documents** (Menu 1)
   - Memproses semua file PDF dalam folder `pdf_documents`
   - Ekstrak teks dari PDF
   - Bagi menjadi chunks yang optimal
   - Buat embeddings untuk setiap chunk
   - Simpan ke MongoDB

2. **Build ChromaDB** (Menu 2)
   - Membangun vector database dari dokumen di MongoDB
   - Diperlukan untuk pencarian semantic

3. **Tanya Jawab** (Menu 3)
   - Input pertanyaan dalam bahasa natural
   - Sistem mencari dokumen yang relevan
   - Generate jawaban berdasarkan konten PDF
   - Optional: filter berdasarkan nama file

## 💡 Fitur-Fitur Canggih

### 🔍 Dual PDF Extraction
- **PyMuPDF (fitz)**: Lebih baik untuk PDF kompleks dan OCR
- **PyPDF2**: Lebih cepat untuk PDF sederhana
- Automatic fallback jika satu method gagal

### 📊 Smart Chunking
```python
CHUNK_SIZE = 1000        # Ukuran chunk optimal
CHUNK_OVERLAP = 200      # Overlap antar chunk
```

### 🏷️ Rich Metadata
- Filename dan chunk ID
- File hash untuk deteksi perubahan
- Source tracking
- Chunk size information

### 🔄 Incremental Processing
- Deteksi file yang sudah diproses
- Hash-based change detection
- Skip file yang tidak berubah

## 📈 Performance Tips

### 1. Optimasi Chunk Size
```python
# Untuk dokumen teknis
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Untuk dokumen naratif
CHUNK_SIZE = 1500  
CHUNK_OVERLAP = 150
```

### 2. MongoDB Indexing
```javascript
// Buat index untuk pencarian lebih cepat
db.pdf_docs.createIndex({"filename": 1})
db.pdf_docs.createIndex({"doc_id": 1})
```

### 3. File Organization
- Kelompokkan PDF berdasarkan topik
- Gunakan nama file yang deskriptif
- Hindari file PDF yang terlalu besar (>50MB)

## 🛠️ Troubleshooting

### PDF Extraction Issues
```python
# Jika PyMuPDF gagal, coba PyPDF2
text = extract_text_from_pdf(pdf_path, method="pypdf2")

# Untuk PDF dengan OCR
text = extract_text_from_pdf(pdf_path, method="pymupdf")
```

### Memory Issues
- Proses file PDF satu per satu
- Gunakan chunk size yang lebih kecil
- Monitor penggunaan memory

### MongoDB Connection
- Script otomatis fallback ke MongoDB lokal
- Cek koneksi dengan menu utilitas

## 📊 Database Schema

### MongoDB Collection: `pdf_docs`
```json
{
  "_id": "ObjectId",
  "doc_id": "filename.pdf_chunk_0",
  "filename": "python_guide.pdf", 
  "file_hash": "md5_hash",
  "text": "chunk content",
  "chunk_id": 0,
  "source": "pdf",
  "chunk_size": 950,
  "embedding": [0.1, 0.2, ...],
  "kategori": "pdf_document"
}
```

### ChromaDB Metadata
```json
{
  "doc_id": "filename.pdf_chunk_0",
  "filename": "python_guide.pdf",
  "kategori": "pdf_document"
}
```

## 🔧 Utility Scripts

### 1. Buat Sample PDF
```bash
python create_sample_docs.py  # Buat file TXT
python txt_to_pdf.py          # Konversi TXT ke PDF
```

### 2. Test Ekstraksi PDF
```python
from rag_db_pdf import extract_text_from_pdf
text = extract_text_from_pdf("file.pdf")
print(f"Extracted {len(text)} characters")
```

### 3. Monitor Database
```python
# Lihat statistik database
pipeline = [
    {"$group": {
        "_id": "$filename",
        "chunks": {"$sum": 1},
        "total_size": {"$sum": "$chunk_size"}
    }}
]
```

## 🎯 Use Cases

### 1. Technical Documentation
- API documentation
- Software manuals
- Research papers

### 2. Educational Content
- Textbooks
- Course materials
- Study guides

### 3. Business Documents
- Reports
- Policies
- Procedures

### 4. Legal Documents
- Contracts
- Regulations
- Case studies

## 🚦 Status Monitoring

### System Health Check
```bash
# Test semua komponen
python -c "
from rag_db_pdf import *
print('✅ MongoDB:', 'OK' if mongo_client else 'FAIL')
print('✅ OpenAI:', 'OK' if client_openai else 'FAIL')
print('✅ ChromaDB:', 'OK' if os.path.exists('chroma_pdf_db') else 'NEED_BUILD')
"
```

### Performance Metrics
- Processing time per PDF
- Chunk count per file
- Search response time
- Memory usage

## 🎉 Ready to Use!

Sistem RAG PDF siap memproses dokumen PDF Anda dan memberikan jawaban cerdas berdasarkan konten yang ada.

**Next Steps:**
1. Setup environment variables
2. Masukkan file PDF ke folder `pdf_documents`
3. Jalankan `python rag-db-pdf.py`
4. Pilih menu 1 untuk ingest dokumen
5. Pilih menu 2 untuk build vector store
6. Pilih menu 3 untuk mulai bertanya!

Happy RAG-ing! 🚀📄🤖
