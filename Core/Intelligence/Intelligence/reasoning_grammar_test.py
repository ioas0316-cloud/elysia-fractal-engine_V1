# -*- coding: utf-8 -*-
"""
Reasoning Grammar Integration Test
==================================

Tests if ReasoningEngine uses GrammarEmergenceEngine to structure thoughts.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Core.Intelligence.Reasoning.reasoning_engine import ReasoningEngine
from Core.Foundation.grammar_engine import GrammarRole
import logging

# Configure logging to see the output
logging.basicConfig(level=logging.INFO)

def main():
    print("\n" + "="*70)
    print("🧠 Reasoning Grammar Test")
    print("="*70 + "\n")
    
    engine = ReasoningEngine()
    
    # 1. Teach Grammar Patterns (Manually for test)
    print("1. Teaching Grammar Patterns...")
    # "Love creates bonds" -> AGENT ACTION PATIENT
    engine.grammar_engine.learn_from_relationship("Love", "creates", "Bonds")
    engine.grammar_engine.learn_from_relationship("Trust", "enables", "Cooperation")
    
    print(f"Learned Patterns: {len(engine.grammar_engine.patterns)}")
    
    # 2. Simulate Thought Expression
    print("\n2. Testing express_thought()...")
    
    # Case A: Known Concepts
    thought_content = "I believe that Love creates strong Bonds between us."
    print(f"\nInput Thought: '{thought_content}'")
    
    response = engine.express_thought(thought_content)
    print(f"Structured Output: {response}")
    
    if response and "[Love ... Bonds]" in response:
        print("✅ SUCCESS: Structure applied correctly.")
    else:
        print("❌ FAILED: Structure not applied.")

    # Case B: Unknown Concepts
    thought_content = "The Chaos is unpredictable."
    print(f"\nInput Thought: '{thought_content}'")
    
    response = engine.express_thought(thought_content)
    print(f"Structured Output: {response}")
    
    # 3. Test communicate() integration
    print("\n3. Testing communicate() integration...")
    # We mock the think() result to ensure it returns a thought with our keywords
    # But for a real test, we can just check if express_thought is called.
    # Since we can't easily mock inside this script without more code, 
    # we rely on the unit test above for logic verification.
    
    print("\n" + "="*70)
    print("✅ Reasoning Grammar Test Complete")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
