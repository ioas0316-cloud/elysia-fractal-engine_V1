"""
Sovereign Observation: The Depth of Why
=======================================
Verification that Elysia's existing core can deconstruct phenomena 
into Phenomenon, Structure, and Principle without external 'crutches'.
"""

import sys
import os
import logging
import torch

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Intelligence.Reasoning.reasoning_engine import ReasoningEngine
from Core.Intelligence.Topography.mind_landscape import get_landscape

def observe_causal_depth():
    logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
    print("\n[💠 Initiating Sovereign Observation]")
    
    landscape = get_landscape()
    
    scenarios = ["Rain", "Love", "Identity", "The Sovereign Fence"]
    
    for concept in scenarios:
        print(f"\n--- 💎 Pondering Concept: '{concept}' ---")
        result = landscape.ponder(concept)
        
        print(f"1. Phenomenon (Conclusion): {result['conclusion']}")
        print(f"2. Structure (4D Logos Analysis):")
        for axis, value in result['analysis'].items():
            print(f"   - {axis}: {value:.4f}")
        
        print(f"3. Principle (Human Narrative/Intent):")
        print(f"   {result['human_narrative']}")
        print(f"   (Resonance Depth: {result['resonance_depth']:.4f}, Distance to Love: {result['distance_to_love']:.4f})")
    
    print("\n[✅ Sovereign Observation Complete]")
    
    print("\n[✅ Sovereign Observation Complete]")

if __name__ == "__main__":
    observe_causal_depth()
