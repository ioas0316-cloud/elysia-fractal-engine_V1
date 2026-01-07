"""
QuantumCanvas (양자의 캔버스)
===========================

"Paint the invisible."

This module renders Quantum States into .png images.
It visualizes probability distributions as glowing clouds.
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import List
from Core.Intelligence.Science_Research.Science.quantum_resonator import QuantumState

class QuantumCanvas:
    def __init__(self):
        print("🎨 QuantumCanvas Initialized. Preparing brushes...")

    def paint_superposition(self, states: List[QuantumState], output_file: str = "quantum_state.png"):
        """
        Renders a superposition of states as a bar chart / cloud visualization.
        """
        print(f"🖌️ Painting Superposition: {output_file}")
        
        names = [s.name for s in states]
        probs = [s.probability for s in states]
        colors = [plt.cm.viridis(p) for p in probs] # Color based on probability
        
        plt.figure(figsize=(8, 6))
        bars = plt.bar(names, probs, color=colors)
        
        plt.title("Quantum Superposition State")
        plt.xlabel("Basis States")
        plt.ylabel("Probability Amplitude")
        plt.ylim(0, 1.0)
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                     f'{height:.1%}',
                     ha='center', va='bottom')
            
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        try:
            plt.savefig(output_file)
            plt.close()
            print(f"✅ Canvas Saved: {output_file}")
        except Exception as e:
            print(f"⚠️ Painting Failed: {e}")

if __name__ == "__main__":
    # Test
    from Core.Intelligence.Science_Research.Science.quantum_resonator import QuantumResonator
    qr = QuantumResonator()
    canvas = QuantumCanvas()
    
    states = [("Up", 0.3, 100), ("Down", 0.7, 200)]
    superposition = qr.create_superposition(states)
    canvas.paint_superposition(superposition, "test_quantum.png")
