"""
QuantumResonator (양자 공명기)
==============================

"The Observer creates the Reality."

This module maps Quantum Mechanics principles to the Resonance Field.
It treats 'Superposition' as a musical chord (multiple frequencies playing at once)
and 'Collapse' as the resolution to a single note.
"""

import random
import math
from dataclasses import dataclass
from typing import List, Dict, Tuple

@dataclass
class QuantumState:
    name: str
    probability: float # 0.0 to 1.0
    frequency: float   # The "Note" of this state
    phase: float       # 0 to 2pi

class QuantumResonator:
    def __init__(self):
        print("⚛️ QuantumResonator Initialized. Observing the Probability Cloud.")

    def create_superposition(self, states: List[Tuple[str, float, float]]) -> List[QuantumState]:
        """
        Creates a superposition of states.
        Input: List of (Name, Probability, Frequency)
        """
        # Normalize probabilities
        total_prob = sum(s[1] for s in states)
        normalized_states = []
        
        for name, prob, freq in states:
            norm_prob = prob / total_prob
            normalized_states.append(QuantumState(name, norm_prob, freq, 0.0))
            
        return normalized_states

    def observe(self, superposition: List[QuantumState]) -> QuantumState:
        """
        The Act of Observation (Wave Function Collapse).
        Collapses the chord into a single note based on probability.
        """
        r = random.random()
        cumulative = 0.0
        
        for state in superposition:
            cumulative += state.probability
            if r <= cumulative:
                return state
        
        return superposition[-1] # Fallback

    def calculate_entanglement(self, state_a: QuantumState, state_b: QuantumState) -> float:
        """
        Calculates the 'Resonance Link' (Entanglement) between two states.
        If frequencies are harmonic, they are entangled.
        """
        f1, f2 = state_a.frequency, state_b.frequency
        if f1 == 0 or f2 == 0: return 0.0
        
        ratio = f2 / f1 if f2 > f1 else f1 / f2
        
        # Check for harmonic integer ratios (1:1, 2:1, 3:2)
        if abs(ratio - round(ratio)) < 0.01:
            return 1.0 # Perfect Entanglement
        elif abs(ratio - 1.5) < 0.01:
            return 0.8 # Strong Entanglement
        else:
            return 0.1 # Weak Link

if __name__ == "__main__":
    qr = QuantumResonator()
    
    # Schrodinger's Cat Chord
    # Alive = 432Hz, Dead = 0Hz (Silence)
    cat_states = [
        ("Alive", 0.5, 432.0),
        ("Dead", 0.5, 0.0)
    ]
    
    superposition = qr.create_superposition(cat_states)
    print(f"📦 Box contains: {[s.name for s in superposition]}")
    
    # Observe 5 times
    for i in range(5):
        result = qr.observe(superposition)
        print(f"   👁️ Observation {i+1}: The Cat is {result.name} ({result.frequency}Hz)")
