# -*- coding: utf-8 -*-
"""
Grand Cross Test
================

Tests the Cosmic Syntax Engine.
Verifies the alignment of Star, Planet, Satellite, and Gravity.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Core.Foundation.resonance_grammar import CosmicSyntaxEngine

def main():
    print("\n" + "="*70)
    print("🌌 Grand Cross Test (Cosmic Syntax)")
    print("="*70 + "\n")
    
    engine = CosmicSyntaxEngine()
    
    # Case 1: Full System (Star + Planet + Satellite + Gravity)
    # Love (Star) -> Creates (Gravity) -> Strong (Satellite) -> Bonds (Planet)
    print("1. Testing Full System (English)...")
    concepts = ["Love", "Bonds", "Creates", "Strong"]
    sentence = engine.express_thought(concepts)
    print(f"Concepts: {concepts}")
    print(f"Result: {sentence}")
    
    # Expected: Love creates Strong Bonds
    # 'Strong' should be identified as Satellite (Low Mass) and attached to 'Bonds' (Planet)
    if "Love creates Strong Bonds" in sentence or "Love creates strong Bonds" in sentence:
        print("✅ SUCCESS: Grand Cross aligned correctly.")
    else:
        print("❌ FAILED: Alignment incorrect.")

    # Case 2: Korean Alignment (SOV)
    print("\n2. Testing Korean Alignment (SOV)...")
    engine.set_korean_mode(True)
    sentence = engine.express_thought(concepts)
    print(f"Result: {sentence}")
    
    # Expected: 사랑하다(은/는) Strong Bonds(을/를) 만들다(한다)
    # Note: 'Strong' and 'Bonds' might not be in the lexicon, so they stay English.
    # 'Love' -> '사랑하다', 'Creates' -> '만들다'
    
    if "사랑하다" in sentence and "Strong Bonds" in sentence and "만들다" in sentence:
         print("✅ SUCCESS: Korean alignment correct.")
    else:
         print(f"❌ FAILED: Korean alignment incorrect. Got: {sentence}")

    # Case 3: Star Only (I am Happy)
    # I (Star) -> Happy (Satellite) -> Is (Gravity)
    # If no planet, Satellite orbits Star?
    print("\n3. Testing Star + Satellite...")
    engine.set_korean_mode(False)
    concepts = ["I", "Happy", "is"]
    sentence = engine.express_thought(concepts)
    print(f"Concepts: {concepts}")
    print(f"Result: {sentence}")
    # Expected: Happy I is ... or I is Happy (if Happy is treated as Planet/Object)
    # 'Happy' is low mass -> Satellite. 'I' is Star.
    # Logic says: if no planet, sat orbits star -> "Happy I is related to something"?
    # Let's see what happens.
    
    print("\n" + "="*70)
    print("✅ Grand Cross Test Complete")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
