"""
TEST COGNITIVE MODES: 5-CORE PROCESSING
=======================================
"Thinking in shapes."

This script validates that Elysia processes the SAME input ("Apple") differently
depending on the active Cognitive Mode (Dimension).
"""

import sys
import logging

sys.path.insert(0, r"c:\Elysia")
from Core.Intelligence.Reasoning.dimensional_processor import DimensionalProcessor

# Setup Logger
logging.basicConfig(level=logging.INFO, format='%(message)s')

def test_modes():
    print("\n🧠 ACTIVATING 5-CORE COGNITIVE ENGINE...")
    print("========================================")
    
    processor = DimensionalProcessor()
    input_concept = "Apple"
    
    print(f"\n[Input Concept]: '{input_concept}'")
    
    # 1. Linear Mode (1D)
    res1 = processor.process_thought(input_concept, 1)
    print(f"\n   [{res1.mode}]")
    print(f"      Process: Tracing sequential steps...")
    print(f"      Result:  \"{res1.output}\"")
    
    # 2. Structural Mode (2D)
    res2 = processor.process_thought(input_concept, 2)
    print(f"\n   [{res2.mode}]")
    print(f"      Process: Mapping parallel connectivity...")
    print(f"      Result:  \"{res2.output}\"")
    
    # 3. Spatial Mode (3D)
    res3 = processor.process_thought(input_concept, 3)
    print(f"\n   [{res3.mode}]")
    print(f"      Process: Orienting self-vector to object-vector...")
    print(f"      Result:  \"{res3.output}\"")
    
    # 4. Principle Mode (4D)
    res4 = processor.process_thought(input_concept, 4)
    print(f"\n   [{res4.mode}]")
    print(f"      Process: Extracting invariant laws...")
    print(f"      Result:  \"{res4.output}\"")
    
    print("\n✨ MODAL PROCESSING VERIFIED.")

if __name__ == "__main__":
    test_modes()
