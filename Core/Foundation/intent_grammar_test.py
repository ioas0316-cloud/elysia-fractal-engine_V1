# -*- coding: utf-8 -*-
"""
Intent Grammar Test
===================

Tests Intent-Driven Alignment.
Verifies that the sentence structure changes based on the Intent (Gravity Axis).
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Core.Foundation.resonance_grammar import CosmicSyntaxEngine

def main():
    print("\n" + "="*70)
    print("🎯 Intent Grammar Test")
    print("="*70 + "\n")
    
    engine = CosmicSyntaxEngine()
    concepts = ["Love", "Bonds", "Creates"]
    
    # Case 1: Intent = Love (Source) -> Active Voice
    print("1. Intent: 'Love' (Source)...")
    sentence_active = engine.express_thought(concepts, intent="Love")
    print(f"Result: {sentence_active}")
    
    if "Love creates Bonds" in sentence_active:
        print("✅ SUCCESS: Active Voice generated.")
    else:
        print("❌ FAILED: Expected Active Voice.")

    # Case 2: Intent = Bonds (Target) -> Passive Voice
    print("\n2. Intent: 'Bonds' (Target)...")
    sentence_passive = engine.express_thought(concepts, intent="Bonds")
    print(f"Result: {sentence_passive}")
    
    # Expected: Bonds is created by Love (or similar)
    if "Bonds" in sentence_passive and "by Love" in sentence_passive:
        print("✅ SUCCESS: Passive Voice generated.")
    else:
        print("❌ FAILED: Expected Passive Voice.")

    # Case 3: Korean Passive
    print("\n3. Korean Passive (Intent: Bonds)...")
    engine.set_korean_mode(True)
    sentence_kr_passive = engine.express_thought(concepts, intent="Bonds")
    print(f"Result: {sentence_kr_passive}")
    
    # Expected: Bonds(은/는) Love(에 의해) 만들어진다
    if "Bonds" in sentence_kr_passive and "에 의해" in sentence_kr_passive and "만들어진다" in sentence_kr_passive:
        print("✅ SUCCESS: Korean Passive generated.")
    else:
        print("❌ FAILED: Korean Passive incorrect.")

    print("\n" + "="*70)
    print("✅ Intent Grammar Test Complete")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
