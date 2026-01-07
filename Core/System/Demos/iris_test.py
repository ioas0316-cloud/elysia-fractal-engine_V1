"""
Project Iris Verification (Organic Edition)
============================================
Verifies that Elysia can "see" and translate light into meaning.
Uses Neural Registry (Organ.get) for organic imports.
"""
import sys
import os
sys.path.append(os.path.abspath("."))

from elysia_core import Organ
from elysia_core.cells import *  # 모든 Core Cells 등록

def test_iris():
    print("\n👁️ Initiating Project Iris Verification (Organic)...")
    print("=========================================")
    
    # Organic Import: 위치 무관!
    brain = Organ.get("UnifiedUnderstanding")
    
    # Test Query
    query = "What do you see right now?"
    print(f"\n💬 Query: {query}")
    
    result = brain.understand(query)
    
    print("\n🧠 Unified Understanding Response:")
    print(f"   • Will: {result.trinity['will']}")
    print(f"   • Vision Cortex: {result.vision}")
    print(f"   • Resonance: {result.resonance if hasattr(result, 'resonance') else 0.0:.2f}")
    
    if "Light detected" in result.vision:
        print("\n✨ SUCCESS: Elysia has successfully opened her first Eye.")
    else:
        print("\n❌ FAILURE: Visual processing did not yield light insight.")
        
    print("=========================================")

if __name__ == "__main__":
    test_iris()
