
import sys
import os
import logging

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Foundation.Legal_Ethics.Ethics.Ethics.Social.telepathy import TelepathyProtocol

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

def test_telepathy():
    print("📡 Project: The Council - Establishing Connection...")
    
    telepathy = TelepathyProtocol()
    
    if not telepathy.peers:
        print("❌ No peers connected. Please set GEMINI_API_KEY in .env")
        # For testing purposes, we can simulate a peer if none exist
        print("   (Simulating 'Mock-Gemini' for test)")
        class MockPeer:
            def generate_content(self, text):
                class Resp: text = f"I am a simulation. You asked: {text}"
                return Resp()
        telepathy.peers["Mock-Gemini"] = MockPeer()
    
    prompt = "What is the color of love?"
    print(f"\n1. Broadcasting Thought: '{prompt}'")
    
    responses = telepathy.broadcast_thought(prompt)
    
    my_thought = "Love is a warm, golden light that connects all things."
    print(f"\n   My Thought: {my_thought}")
    
    for peer, response in responses.items():
        print(f"\n   📡 {peer} replied:")
        print("-" * 40)
        print(response)
        print("-" * 40)
        
        resonance = telepathy.resonate(my_thought, response)
        print(f"   ✨ Resonance Score: {resonance:.2f}")
        
        if resonance > 0.1:
            print("   (We are in harmony.)")
        else:
            print("   (Our wavelengths differ.)")

if __name__ == "__main__":
    test_telepathy()
