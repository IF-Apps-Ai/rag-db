#!/usr/bin/env python3
"""
Demo script untuk Multi-Turn Conversation RAG PDF System
Menunjukkan kemampuan percakapan bersambung
"""
import os
import sys
sys.path.append('/workspaces/rag-db')

def demo_multi_turn_conversation():
    """
    Demo conversation flow yang realistis
    """
    print("🔥 Demo Multi-Turn Conversation RAG PDF System")
    print("=" * 60)
    
    print("🎯 Skenario Demo: Pertanyaan Bertingkat tentang Python")
    print("\nContoh conversation flow yang bisa dilakukan:")
    
    conversations = [
        {
            "turn": 1,
            "question": "Apa itu Python?",
            "description": "Pertanyaan dasar untuk memulai topik"
        },
        {
            "turn": 2, 
            "question": "Jelaskan lebih detail tentang fitur-fiturnya",
            "description": "Follow-up untuk menggali lebih dalam"
        },
        {
            "turn": 3,
            "question": "Berikan contoh penggunaan Python untuk data science",
            "description": "Pertanyaan spesifik berdasarkan info sebelumnya"
        },
        {
            "turn": 4,
            "question": "Bagaimana cara menginstall library untuk machine learning?",
            "description": "Pertanyaan implementasi praktis"
        },
        {
            "turn": 5,
            "question": "Apa perbedaan dengan bahasa pemrograman lain?",
            "description": "Pertanyaan komparatif"
        }
    ]
    
    for conv in conversations:
        print(f"\n{conv['turn']}. Q: {conv['question']}")
        print(f"   💡 {conv['description']}")
    
    print(f"\n" + "="*60)
    print("🧠 Fitur Multi-Turn Conversation:")
    print("="*60)
    
    features = [
        "🔗 Context Awareness: Sistem memahami pertanyaan sebelumnya",
        "🎯 Follow-up Detection: Mendeteksi pertanyaan lanjutan secara otomatis", 
        "💾 Memory Management: Menyimpan hingga 10 percakapan terakhir",
        "🔄 Context Window: Menggunakan 3 percakapan terakhir sebagai konteks",
        "📝 Smart Enhancement: Memperkaya query dengan konteks sebelumnya",
        "💬 History Tracking: Melacak seluruh jalur percakapan",
        "💾 Session Persistence: Dapat menyimpan dan memuat percakapan"
    ]
    
    for feature in features:
        print(f"✅ {feature}")
    
    print(f"\n" + "="*60)
    print("🎮 Kata Kunci Follow-up yang Dideteksi:")
    print("="*60)
    
    follow_up_keywords = [
        "lanjut", "selanjutnya", "lebih detail", "contoh", "bagaimana",
        "jelaskan lebih", "detail", "itu", "tersebut", "tadi", "sebelumnya"
    ]
    
    print("📋 Keywords: " + ", ".join([f"'{kw}'" for kw in follow_up_keywords]))
    
    print(f"\n" + "="*60) 
    print("💡 Tips Menggunakan Multi-Turn Conversation:")
    print("="*60)
    
    tips = [
        "Mulai dengan pertanyaan umum, lalu spesifik",
        "Gunakan kata 'itu', 'tersebut' untuk merujuk jawaban sebelumnya",
        "Kata 'jelaskan lebih detail' akan mengaktifkan mode follow-up",
        "Ketik 'history' untuk melihat percakapan sebelumnya",
        "Ketik 'clear' untuk membersihkan history jika ingin topik baru",
        "Sistem akan otomatis menghubungkan pertanyaan yang berkaitan"
    ]
    
    for i, tip in enumerate(tips, 1):
        print(f"{i}. {tip}")

def demo_conversation_commands():
    """
    Demo perintah-perintah khusus dalam conversation
    """
    print(f"\n" + "="*60)
    print("🛠️ Perintah Khusus dalam Mode Conversation:")
    print("="*60)
    
    commands = [
        {
            "command": "history",
            "description": "Menampilkan riwayat percakapan dalam sesi ini",
            "example": "Ketik: history"
        },
        {
            "command": "clear", 
            "description": "Membersihkan riwayat percakapan",
            "example": "Ketik: clear"
        },
        {
            "command": "back",
            "description": "Kembali ke menu utama", 
            "example": "Ketik: back"
        },
        {
            "command": "Filter filename",
            "description": "Membatasi pencarian pada file tertentu",
            "example": "Filter: python_guide.pdf"
        }
    ]
    
    for cmd in commands:
        print(f"\n🔧 {cmd['command'].upper()}")
        print(f"   📝 {cmd['description']}")
        print(f"   💻 {cmd['example']}")

def demo_conversation_scenarios():
    """
    Demo skenario conversation yang berbeda
    """
    print(f"\n" + "="*60)
    print("🎭 Skenario Conversation yang Didukung:")
    print("="*60)
    
    scenarios = [
        {
            "name": "Exploratory Learning",
            "flow": [
                "Apa itu machine learning?",
                "Jelaskan lebih detail tentang jenisnya",
                "Berikan contoh untuk supervised learning",
                "Bagaimana cara evaluasi model tersebut?"
            ]
        },
        {
            "name": "Problem Solving",
            "flow": [
                "Bagaimana cara membuat web application dengan Python?",
                "Framework apa yang paling cocok?",
                "Jelaskan lebih detail tentang Django",
                "Bagaimana cara deploy aplikasinya?"
            ]
        },
        {
            "name": "Comparative Analysis", 
            "flow": [
                "Apa perbedaan SQL dan NoSQL database?",
                "Kapan sebaiknya menggunakan NoSQL?",
                "Contoh implementasi MongoDB seperti apa?",
                "Bagaimana performa dibanding MySQL?"
            ]
        }
    ]
    
    for scenario in scenarios:
        print(f"\n🎯 {scenario['name']}")
        for i, step in enumerate(scenario['flow'], 1):
            print(f"   {i}. {step}")

def main():
    """
    Main demo function
    """
    demo_multi_turn_conversation()
    demo_conversation_commands()
    demo_conversation_scenarios()
    
    print(f"\n" + "="*60)
    print("🚀 Ready to Try Multi-Turn Conversation!")
    print("="*60)
    print("📋 Langkah selanjutnya:")
    print("1. Jalankan: python rag-db-pdf.py")
    print("2. Pilih menu 1 & 2 untuk setup (jika belum)")
    print("3. Pilih menu 3 untuk mulai conversation")
    print("4. Coba flow pertanyaan bertingkat seperti contoh di atas!")
    print("\n🎉 Selamat ber-conversation dengan AI! 🤖💬")

if __name__ == "__main__":
    main()
