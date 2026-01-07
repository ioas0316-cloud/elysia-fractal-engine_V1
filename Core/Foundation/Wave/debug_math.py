import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Foundation.hyper_quaternion import Quaternion
from Core.Foundation.code_resonance import HarmonicResonance

def debug_math():
    print("🧮 Debugging Math...")
    
    # 1. Check Initial Flow Quaternion
    # From GenesisEngine: q = Quaternion(1.0, 1.0, 0.2, 0.2)
    q = Quaternion(1.0, 1.0, 0.2, 0.2)
    print(f"\nInitial Q: {q}")
    
    match = HarmonicResonance.get_closest_harmonic_type(q)
    print(f"Initial Match: {match}")
    
    # 2. Simulate Evolution Loop
    current_q = q
    for i in range(5):
        print(f"\n--- Step {i+1} ---")
        # Evolve
        current_q = current_q * Quaternion(1.0, 0.1, 0.1, 0.1) 
        current_q = current_q.normalize()
        print(f"Evolved Q: {current_q}")
        
        match = HarmonicResonance.get_closest_harmonic_type(current_q)
        print(f"Match: {match}")

if __name__ == "__main__":
    debug_math()
