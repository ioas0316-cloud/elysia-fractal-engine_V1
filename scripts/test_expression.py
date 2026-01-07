"""
TEST EXPRESSION: THE PRISM
==========================
"A thought is a sphere; Speech is a line."

This script validates that Elysia's "Linguistic Projector" correctly 
transforms internal 4D states into 1D stylistic output.
"""

import sys
import logging
import time

sys.path.insert(0, r"c:\Elysia")

from Core.Foundation.unified_field import UnifiedField, HyperQuaternion
from Core.Expression.linguistic_topology import LinguisticTopology

# Setup Logger
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("TestExpression")

def test_prism():
    print("\n🌈 IGNITING THE PRISM...")
    print("=======================")
    
    field = UnifiedField()
    prism = LinguisticTopology(field)
    
    kernel = "I choose the synthesis of Logic and Emotion"
    
    # CASE 1: High Coherence (Divine Resonance)
    print("\n[State 1: Divine Harmony]")
    field.coherence = 0.95
    field.total_energy = 1.5
    field.inject_wave(field.create_wave_packet("Love", 432.0, 1.0, 0.0, HyperQuaternion(0,0,0,0)))
    
    output1 = prism.project_thought(kernel)
    print(f"   Input: '{kernel}'")
    print(f"   Output: \"{output1}\"\n")
    
    # CASE 2: High Entropy (Panic/Chaos)
    print("\n[State 2: System Panic]")
    field.coherence = 0.2
    field.entropy = 0.9
    field.total_energy = 5.0 # Screaming
    
    output2 = prism.project_thought(kernel)
    print(f"   Input: '{kernel}'")
    print(f"   Output: \"{output2}\"\n")
    
    # CASE 3: Cold Logic (Machine Mode)
    print("\n[State 3: Cold Logic]")
    field.coherence = 0.5 # Neutral
    field.entropy = 0.0 # Ordered
    field.total_energy = 0.5 # Low energy
    
    # Force warmth low via coherence hack or implement better logic
    # Here we just rely on coherence 0.5 giving warmth 0.0 (Neutral)
    # Let's adjust coherence manually to lower warmth
    field.coherence = 0.1 # Very low coherence = Cold? No, Coherence is Harmony. 
    # Actually, Cold logic is often High Logic Coherence but Low Emotional Amplitude.
    # For this simple Prism, low coherence = cold/fragmented.
    
    output3 = prism.project_thought(kernel)
    print(f"   Input: '{kernel}'")
    print(f"   Output: \"{output3}\"\n")
    
    print("\n✨ PRISM TEST COMPLETE.")

if __name__ == "__main__":
    test_prism()
