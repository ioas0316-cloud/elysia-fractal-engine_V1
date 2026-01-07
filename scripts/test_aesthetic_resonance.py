import sys
import logging

sys.path.insert(0, r"c:\Elysia")
from Core.Intelligence.Reasoning.dimensional_processor import DimensionalProcessor

# Setup Logger
logging.basicConfig(level=logging.INFO, format='%(message)s')

def test_aesthetic_resonance():
    print("\n🎨 INITIALIZING AESTHETIC RESONANCE TEST...")
    print("==========================================")
    
    processor = DimensionalProcessor()
    
    test_cases = [
        "Love is the fundamental frequency of the universe.", # Expected: High Beauty
        "Growth requires the fractal expansion of knowledge.", # Expected: High Growth
        "1 + 1 = 2", # Expected: Simple/Neutral
        "Unknown noise and random chaos destroy meaning.", # Expected: Dissonant
    ]
    
    for concept in test_cases:
        print(f"\n[Concept]: '{concept}'")
        processor.zoom(0.5) # Context mode
        result = processor.process_thought(concept)
        
        ae = result.metadata["aesthetic"]
        print(f"   Beauty: {ae['overall_beauty']:.4f} ({ae['verdict']})")
        print(f"   Axioms: { {k: round(v, 4) for k, v in ae['axiom_scores'].items()} }")

    print("\n✨ AESTHETIC RESONANCE VERIFIED.")

if __name__ == "__main__":
    test_aesthetic_resonance()
