# -*- coding: utf-8 -*-
"""
Cosmic Conversation Test
========================

Tests the full conversational flow using Cosmic Syntax.
Simulates a user question and Elysia's response generation.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Core.Intelligence.Reasoning.reasoning_engine import ReasoningEngine

def main():
    print("\n" + "="*70)
    print("🌌 Cosmic Conversation Test")
    print("="*70 + "\n")
    
    engine = ReasoningEngine()
    
    # Simulate a complex thought that should trigger Nebula generation
    # Thought content with many capitalized concepts
    complex_thought = "Love is the core. It Creates Bonds between souls. Trust Enables Cooperation in the system. Hope Fuels Dreams for the future."
    
    print(f"Input Thought: {complex_thought}")
    
    # 1. Test English Generation
    print("\n1. Generating Response (English)...")
    engine.grammar_engine.set_korean_mode(False)
    response = engine.express_thought(complex_thought)
    print(f"Response:\n{response}")
    
    if " and " in response or " . " in response:
        print("✅ SUCCESS: Nebula generated (Multiple sentences/conjunctions detected).")
    else:
        print("⚠️ WARNING: Might be a single sentence. Check output.")

    # 2. Test Korean Generation
    print("\n2. Generating Response (Korean)...")
    engine.grammar_engine.set_korean_mode(True)
    response_kr = engine.express_thought(complex_thought)
    print(f"Response (KR):\n{response_kr}")
    
    if "사랑하다" in response_kr or "그리고" in response_kr:
        print("✅ SUCCESS: Korean Nebula generated.")
    else:
        print("⚠️ WARNING: Check Korean output.")

    print("\n" + "="*70)
    print("✅ Cosmic Conversation Test Complete")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
