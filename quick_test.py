"""
Quick test script untuk RAG PDF API
"""

import requests

def test_question():
    """Test question answering"""
    url = "http://127.0.0.1:8000/ask"
    data = {
        "question": "Apa isi dari dokumen yang tersedia?",
        "max_results": 3
    }
    
    print("🔍 Testing question answering...")
    print(f"Question: {data['question']}")
    
    try:
        response = requests.post(url, json=data, timeout=60)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Answer: {result['answer'][:200]}...")
            print(f"🆔 Conversation ID: {result['conversation_id']}")
            print(f"📚 Sources: {len(result['sources'])} documents")
            return result['conversation_id']
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    return None

def test_follow_up(conversation_id):
    """Test follow-up question"""
    url = "http://127.0.0.1:8000/ask"
    data = {
        "question": "Jelaskan lebih detail",
        "conversation_id": conversation_id,
        "max_results": 3
    }
    
    print("\n🔄 Testing follow-up question...")
    print(f"Question: {data['question']}")
    
    try:
        response = requests.post(url, json=data, timeout=60)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Follow-up Answer: {result['answer'][:200]}...")
            print(f"🔢 Turn number: {result['turn_number']}")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    print("🚀 RAG PDF API - Quick Test")
    print("=" * 40)
    
    # Test basic question
    conv_id = test_question()
    
    # Test follow-up if first question worked
    if conv_id:
        test_follow_up(conv_id)
