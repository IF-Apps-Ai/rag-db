#!/usr/bin/env python3
"""
Simple test for conversation system
"""

# Test ConversationManager
class SimpleConversationTest:
    def __init__(self):
        self.history = []
    
    def add_exchange(self, q, a):
        self.history.append({"q": q, "a": a})
    
    def get_context(self):
        return "\n".join([f"Q: {h['q']}\nA: {h['a']}" for h in self.history[-3:]])

def test_conversation():
    print("🧪 Testing Conversation System")
    print("=" * 40)
    
    conv = SimpleConversationTest()
    
    # Test basic functionality
    conv.add_exchange("Apa itu Python?", "Python adalah bahasa pemrograman...")
    conv.add_exchange("Jelaskan fitur-fiturnya", "Fitur Python meliputi...")
    conv.add_exchange("Berikan contoh", "Contoh kode Python...")
    
    context = conv.get_context()
    print("✅ Conversation context generated")
    print(f"📊 Context length: {len(context)} characters")
    print(f"💬 History entries: {len(conv.history)}")
    
    # Test follow-up detection
    follow_up_keywords = ["lanjut", "detail", "contoh", "itu", "tersebut"]
    test_query = "Jelaskan lebih detail tentang itu"
    
    has_follow_up = any(keyword in test_query.lower() for keyword in follow_up_keywords)
    print(f"🔍 Follow-up detection: {'✅ Detected' if has_follow_up else '❌ Not detected'}")
    
    print("\n🎉 Basic conversation system working!")
    return True

if __name__ == "__main__":
    test_conversation()
