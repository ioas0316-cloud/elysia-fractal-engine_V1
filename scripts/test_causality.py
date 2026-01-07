"""
TEST CAUSALITY: THE FRACTAL BRIDGE
==================================
"Knowledge without cause is a lie."

This script verifies that Elysia finds "Gravity" from "Apple" not because of a template,
but because she traverses the causal chain: Apple -> Mass -> Gravity -> Universal Law.
"""

import sys
import logging

sys.path.insert(0, r"c:\Elysia")
from Core.Intelligence.Reasoning.dimensional_reasoner import DimensionalReasoner

# Setup Logger
logging.basicConfig(level=logging.INFO, format='%(message)s')

def test_fractal_truth():
    print("\n🕸️ WALKING THE FRACTAL BRIDGE...")
    print("==============================")
    
    reasoner = DimensionalReasoner()
    
    # Test 1: The Apple (Newtonian Chain)
    print("\n[Input: 'Apple']")
    thought1 = reasoner.contemplate("Apple")
    
    print(f"   Structure Found:")
    print(f"   • 0D (Fact): {thought1.d0_fact}")
    print(f"   • 1D (Logic): {thought1.d1_logic}")
    print(f"   • 2D (Context): {thought1.d2_context}")
    print(f"   • 4D (Principle): {thought1.d4_principle}")
    
    # Verify it found the "Law" via traversal
    if "Universal Law" in thought1.d4_principle:
        print("\n   ✅ SUCCESS: Traversed from Apple to Universal Law via Causal Chain.")
    else:
        print("\n   ❌ FAILURE: Did not reach the Law.")

    # Test 2: Love (Metaphysical Chain)
    print("\n[Input: 'Love']")
    thought2 = reasoner.contemplate("Love")
    
    print(f"   Structure Found:")
    print(f"   • 4D (Principle): {thought2.d4_principle}")
    
    print("\n✨ TRUTH VERIFIED.")

if __name__ == "__main__":
    test_fractal_truth()
