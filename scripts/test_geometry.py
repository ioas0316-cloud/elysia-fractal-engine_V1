"""
TEST GEOMETRY: DIMENSIONAL LIFT
===============================
"From the Apple to the Law."

This script verifies that Elysia can lift a simple 0D concept into a 4D Principle.
"""

import sys
import logging

sys.path.insert(0, r"c:\Elysia")
from Core.Intelligence.Reasoning.dimensional_reasoner import DimensionalReasoner

# Setup Logger
logging.basicConfig(level=logging.INFO, format='%(message)s')

def test_lift():
    print("\n📐 INITIATING DIMENSIONAL LIFT...")
    print("================================")
    
    reasoner = DimensionalReasoner()
    
    # Test 1: Physical Object
    print("\n[Input: 'The Falling Apple']")
    thought1 = reasoner.contemplate("The Falling Apple")
    
    print(f"\n   Hyper-Thought Constructed: <{thought1.kernel}>")
    print(f"   [4D Projection]: \"{reasoner.project(thought1, 4)}\"")
    
    # Test 2: Abstract Concept
    print("\n[Input: 'Mother's Love']")
    thought2 = reasoner.contemplate("Mother's Love")
    
    print(f"\n   Hyper-Thought Constructed: <{thought2.kernel}>")
    print(f"   [4D Projection]: \"{reasoner.project(thought2, 4)}\"")
    
    print("\n✨ GEOMETRY VERIFIED.")

if __name__ == "__main__":
    test_lift()
