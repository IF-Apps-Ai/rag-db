# Multi-Turn Conversation RAG PDF System

## 🔥 **NEW FEATURE: Multi-Turn Conversation**

Sistem RAG PDF sekarang mendukung **percakapan bersambung** yang memungkinkan Anda mengajukan pertanyaan follow-up yang saling terkait, seperti berbicara dengan asisten AI yang memahami konteks percakapan sebelumnya.

## 🧠 **Intelligent Conversation Features**

### 🔗 **Context Awareness**
- Sistem mengingat hingga **10 percakapan terakhir**
- Menggunakan **3 percakapan terakhir** sebagai konteks aktif
- Otomatis menghubungkan pertanyaan yang berkaitan

### 🎯 **Smart Follow-up Detection**
Sistem secara otomatis mendeteksi pertanyaan lanjutan berdasarkan kata kunci:
```
"lanjut", "selanjutnya", "lebih detail", "contoh", "bagaimana"
"jelaskan lebih", "detail", "itu", "tersebut", "tadi", "sebelumnya"
```

### 💾 **Memory Management**
- **Session Persistence**: Simpan dan muat percakapan
- **Dynamic Context Window**: Atur jumlah percakapan dalam konteks
- **Automatic Cleanup**: Manajemen memori otomatis

## 🎮 **Cara Menggunakan Multi-Turn Conversation**

### 1. **Mulai Conversation Mode**
```bash
python rag-db-pdf.py
# Pilih menu 3: ❓ Tanya Jawab dengan PDF
```

### 2. **Flow Conversation yang Natural**

#### **Skenario 1: Exploratory Learning**
```
User: Apa itu Python?
AI: [Jawaban lengkap tentang Python...]

User: Jelaskan lebih detail tentang fitur-fiturnya
AI: [Enhanced dengan konteks sebelumnya tentang Python...]

User: Berikan contoh penggunaan untuk data science
AI: [Spesifik ke data science berdasarkan context Python...]
```

#### **Skenario 2: Problem Solving**
```
User: Bagaimana cara membuat web application?
AI: [Jawaban umum tentang web development...]

User: Framework apa yang paling cocok untuk Python?
AI: [Fokus ke Python frameworks berdasarkan context...]

User: Jelaskan lebih detail tentang Django
AI: [Deep dive ke Django...]
```

### 3. **Special Commands dalam Conversation**
```bash
# Lihat history percakapan
history

# Clear conversation history  
clear

# Kembali ke menu utama
back

# Filter berdasarkan file tertentu
Filter: python_guide.pdf
```

## 🛠️ **Advanced Conversation Management**

### **Menu Conversation Management (Menu 7)**

#### 📜 **View History**
- Lihat seluruh riwayat percakapan dalam sesi
- Informasi sources dan timestamp
- Preview jawaban dengan truncation

#### 💾 **Save/Load Conversations**
```bash
# Simpan conversation
Menu 7 → 3 → filename.json

# Load conversation  
Menu 7 → 4 → filename.json
```

#### ⚙️ **Configure Context Window**
```bash
# Atur berapa percakapan yang digunakan sebagai konteks
Menu 7 → 5 → 1-10
```

## 🎯 **Enhanced Prompt Engineering**

### **Context-Aware Prompts**
Sistem secara otomatis membangun prompt yang mencakup:

1. **Conversation History**
```
CONVERSATION HISTORY:
Q1: Apa itu Python?
A1: Python adalah bahasa pemrograman...
Q2: Jelaskan fitur-fiturnya
A2: Fitur utama Python meliputi...
```

2. **Document Context**
```
DOKUMEN REFERENSI:
[File: python_guide.pdf]
Python adalah bahasa pemrograman tingkat tinggi...
```

3. **Smart Instructions**
```
Instruksi: Jawab pertanyaan saat ini dengan mempertimbangkan 
konteks percakapan sebelumnya. Berikan jawaban yang konsisten 
dan terhubung dengan pembahasan sebelumnya.
```

## 📊 **Technical Architecture**

### **ConversationManager Class**
```python
class ConversationManager:
    - conversation_history: List[Dict]
    - max_history: int = 10
    - context_window: int = 3
    - current_session_id: str
    
    Methods:
    - add_exchange(question, answer, sources)
    - get_conversation_context(num_recent)
    - save_conversation(filename)
    - load_conversation(filename)
    - clear_history()
```

### **Enhanced Query Processing**
```python
# 1. Detect follow-up questions
is_follow_up = detect_follow_up_indicators(query)

# 2. Enhance query with context
if is_follow_up:
    enhanced_query = f"Berdasarkan '{last_question}', {query}"

# 3. Build context-aware prompt
prompt = build_contextual_prompt(
    conversation_history,
    document_context,
    current_query
)
```

## 🎭 **Use Case Examples**

### **1. Learning Programming**
```
Q1: Apa itu Python?
Q2: Bagaimana syntax dasarnya?
Q3: Berikan contoh kode sederhana
Q4: Jelaskan tentang data types
Q5: Bagaimana cara error handling?
```

### **2. Technical Troubleshooting** 
```
Q1: Bagaimana cara setup database MongoDB?
Q2: Ada error connection refused, kenapa?
Q3: Bagaimana cara fallback ke database lokal?
Q4: Berikan contoh konfigurasi yang benar
```

### **3. Comparative Analysis**
```
Q1: Apa perbedaan SQL dan NoSQL?
Q2: Kapan sebaiknya pakai NoSQL?
Q3: Jelaskan kelebihan MongoDB dibanding MySQL
Q4: Bagaimana performa query pada masing-masing?
```

## 💡 **Best Practices**

### **1. Conversation Flow**
- ✅ Mulai dengan pertanyaan umum
- ✅ Gunakan pertanyaan follow-up yang spesifik  
- ✅ Manfaatkan kata kunci "itu", "tersebut" untuk referensi
- ✅ Gunakan "jelaskan lebih detail" untuk deep dive

### **2. Context Management**
- ✅ Monitor jumlah percakapan dalam history
- ✅ Clear history saat ganti topik besar
- ✅ Save conversation untuk sesi panjang
- ✅ Atur context window sesuai kebutuhan

### **3. Performance Optimization**
- ✅ Context window optimal: 3-5 percakapan
- ✅ Max history tidak lebih dari 10
- ✅ Regular cleanup untuk memory efficiency

## 🚀 **Ready for Multi-Turn Conversation!**

**Multi-Turn Conversation RAG PDF System** memberikan pengalaman tanya jawab yang natural dan kontekstual, memungkinkan eksplorasi topik yang mendalam melalui pertanyaan bertingkat yang saling terkait.

### **Key Benefits:**
- 🧠 **Contextual Understanding**: AI memahami alur percakapan
- 🔗 **Seamless Follow-ups**: Pertanyaan lanjutan otomatis terhubung
- 💾 **Persistent Memory**: Conversation history tersimpan
- 🎯 **Enhanced Relevance**: Jawaban lebih akurat dengan konteks

**Start your intelligent conversation with PDFs now!** 🤖💬📄
