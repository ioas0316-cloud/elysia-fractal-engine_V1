# -*- coding: utf-8 -*-
"""
Advanced Grammar Test
=====================

Tests:
1. Korean SOV structure (사랑은 유대를 만든다)
2. Conditional structure (If Trust, then Cooperation)
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Core.Foundation.grammar_engine import GrammarEmergenceEngine, GrammarRole

def main():
    print("\n" + "="*70)
    print("🌟 Advanced Grammar Test")
    print("="*70 + "\n")
    
    engine = GrammarEmergenceEngine()
    
    # 1. Teach Patterns
    print("1. Teaching Patterns...")
    engine.learn_from_relationship("Love", "creates", "Bonds")
    engine.learn_from_relationship("Trust", "enables", "Cooperation")
    
    # 2. Test English (SVO)
    print("\n2. Testing English (SVO)...")
    concepts = ['Love', 'Bonds']
    structure = engine.suggest_structure(concepts)
    print(f"Concepts: {concepts}")
    print(f"Structure: {structure}")
    # Expected: ['Love', 'Bonds'] (Agent, Patient) -> "Love ... Bonds"
    
    # 3. Test Korean (SOV)
    print("\n3. Testing Korean (SOV)...")
    engine.set_korean_mode(True)
    
    # Using English concepts but expecting Korean structure
    concepts = ['Love', 'Bonds']
    structure = engine.suggest_structure(concepts)
    print(f"Concepts: {concepts}")
    print(f"Structure: {structure}")
    # Expected: ['Love(은/는)', 'Bonds(을/를)', '(한다)']
    
    # 4. Test Conditional (Mocking role memory for 'if')
    print("\n4. Testing Conditional...")
    engine.set_korean_mode(False)
    
    # Manually inject roles for testing conditional logic
    # Since we don't have a relationship extractor for 'if' yet, we simulate the memory
    engine.role_memory['Rain'][GrammarRole.CONDITION] = 5
    engine.role_memory['Cave'][GrammarRole.CONSEQUENCE] = 5
    
    concepts = ['Rain', 'Cave']
    structure = engine.suggest_structure(concepts)
    print(f"Concepts: {concepts}")
    print(f"Structure: {structure}")
    # Expected: ['If Rain', 'then Cave']

    print("\n" + "="*70)
    print("✅ Advanced Grammar Test Complete")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
