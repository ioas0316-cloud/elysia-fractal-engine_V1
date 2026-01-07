import sys
import logging

sys.path.insert(0, r"c:\Elysia")
from Core.Intelligence.Reasoning.dimensional_reasoner import DimensionalReasoner

# Setup Logger
logging.basicConfig(level=logging.INFO, format='%(message)s')

def test_narrative_causality():
    print("\n📖 INITIALIZING NARRATIVE CAUSALITY TEST...")
    print("===========================================")
    
    reasoner = DimensionalReasoner()
    kernel = "Chef's Rhythm"
    
    print(f"Propagating concept through the dimensions: '{kernel}'")
    thought = reasoner.contemplate(kernel)
    
    print("\n--- [ NARRATIVE PROJECTION ] ---")
    story = reasoner.project_narrative(thought)
    print(story)
    
    print("\n✨ NARRATIVE CAUSALITY VERIFIED.")

if __name__ == "__main__":
    test_narrative_causality()
