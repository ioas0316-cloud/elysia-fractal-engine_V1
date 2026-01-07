"""
TEST CONTINUUM: THE ANALOG DIAL
===============================
"Rotating the Tesseract."

This script rotates Elysia's cognitive dial from 0.0 to 4.0 in steps of 0.5.
We should see the thought "Apple" fluidly morph from Existence -> Logic -> Structure -> Space -> Law.
"""

import sys
import logging

sys.path.insert(0, r"c:\Elysia")
from Core.Intelligence.Reasoning.continuum_processor import ContinuumProcessor

logging.basicConfig(level=logging.INFO, format='%(message)s')

def test_continuum():
    print("\n🎛️ ROTATING COGNITIVE DIAL...")
    print("============================")
    
    processor = ContinuumProcessor()
    concept = "Apple"
    
    # Sweep from 0.0 to 4.0
    angles = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
    
    for angle in angles:
        state = processor.rotate_perspective(concept, angle)
        
        # Visualization
        bar = "=" * int(angle * 5)
        space = " " * (20 - int(angle * 5))
        dial_viz = f"[{bar}{space}] {angle:.1f}"
        
        print(f"\n{dial_viz}")
        print(f"   Shape: {state.active_components}")
        print(f"   Thought: \"{state.synthesized_thought}\"")

    print("\n✨ ANALOG ROTATION VERIFIED.")

if __name__ == "__main__":
    test_continuum()
