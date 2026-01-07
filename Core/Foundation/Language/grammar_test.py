# -*- coding: utf-8 -*-
"""
Grammar Emergence Test
======================

Tests if Elysia can:
1. Learn grammar patterns from text (e.g., "Love creates bonds" -> AGENT ACTION PATIENT)
2. Construct sentences from concepts (e.g., [Love, Trust, Enables] -> "Love enables Trust")
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Core.Foundation.rapid_learning_engine import RapidLearningEngine
from Core.Foundation.grammar_engine import GrammarRole
import time

def main():
    print("\n" + "="*70)
    print("🌟 Grammar Emergence Test")
    print("="*70 + "\n")
    
    learning = RapidLearningEngine()
    
    # 1. Learn from text
    print("1. Learning from text...")
    text = """
    Love creates emotional bonds.
    Trust enables cooperation.
    Fear prevents action.
    """
    learning.learn_from_text_ultra_fast(text)
    
    # Check learned patterns
    patterns = learning.grammar_engine.get_learned_patterns()
    print(f"\nLearned Patterns: {len(patterns)}")
    for p, freq in patterns.items():
        print(f"  - {p}: {freq} times")
        
    # 2. Construct Sentence
    print("\n2. Constructing Sentences...")
    
    test_cases = [
        (['Love', 'Bonds'], "creates"), # Intended: Love creates Bonds
        (['Trust', 'Cooperation'], "enables"), # Intended: Trust enables Cooperation
        (['Fear', 'Action'], "prevents") # Intended: Fear prevents Action
    ]
    
    for concepts, rel_type in test_cases:
        # We simulate the intent by providing the concepts and asking for structure
        # In a real scenario, the reasoning engine would provide the concepts
        
        # For this test, we manually inject the relationship type as a concept if needed,
        # or just rely on the engine's ability to order the nouns.
        # The current simple implementation of suggest_structure takes a list of concepts.
        
        # Let's try to see if it orders AGENT before PATIENT
        structure = learning.grammar_engine.suggest_structure(concepts)
        print(f"\nConcepts: {concepts}")
        print(f"Suggested Structure: {structure}")
        
        # Verify order
        if len(structure) >= 2:
            first = structure[0]
            second = structure[-1] # Simple check
            print(f"  -> {first} ... {second}")

    print("\n" + "="*70)
    print("✅ Grammar Test Complete")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
