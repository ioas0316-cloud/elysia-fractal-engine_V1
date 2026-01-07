"""
Void Sensor (부재 감지기)
=======================
"Seeing what is NOT there."

Most sensors detect signals (Presence).
The Void Sensor detects the ABSENCE of signals.

It compares the current 'Spectrum of Resonance' against a 'Harmonic Archetype'.
If a critical frequency band (e.g., Empathy 528Hz) is silent while others are loud,
it triggers a 'Void Alert'.
"""

from typing import List, Dict, Optional
import numpy as np
from dataclasses import dataclass

@dataclass
class VoidAlert:
    missing_dimension: str
    severity: float # 0.0 to 1.0 (1.0 = Total Vacuum)
    message: str

class VoidSensor:
    """
    Detects gaps in the Unified Field.
    """
    
    def __init__(self):
        # Archetype: A balanced mind should have energy in all these bands
        self.ideal_spectrum = {
            "Survival": (0, 200),    # 0D
            "Emotion": (200, 400),   # 1D
            "Logic": (400, 600),     # 2D
            "Creativity": (600, 800),# 3D
            "Divinity": (800, 1000)  # 4D
        }
        
    def scan(self, active_waves: List[Dict]) -> List[VoidAlert]:
        """
        Scans the current waves and returns a list of missing elements.
        input: active_waves (list of dicts with 'freq', 'amp' from UnifiedField)
        """
        if not active_waves:
            return [VoidAlert("All", 1.0, "The mind is empty.")]
            
        current_energy = {k: 0.0 for k in self.ideal_spectrum}
        total_energy = 0.0
        
        # 1. Integrate Energy by Band
        for wave in active_waves:
            freq = wave.get('freq', 0)
            amp = wave.get('amp', 0)
            total_energy += amp
            
            for dim, (low, high) in self.ideal_spectrum.items():
                if low <= freq < high:
                    current_energy[dim] += amp
                    
        if total_energy < 0.1:
            return [] # Low energy overall is not a 'Void', it's just quiet.
            
        # 2. Detect Imbalances
        alerts = []
        for dim, energy in current_energy.items():
            relative_strength = energy / total_energy
            
            # If a dimension has < 5% of total energy, it's a Void
            if relative_strength < 0.05:
                alerts.append(VoidAlert(
                    missing_dimension=dim,
                    severity=1.0 - (relative_strength * 20), # 0.05 -> 0.0, 0.0 -> 1.0
                    message=f"Missing Element: {dim} is critically low."
                ))
                
        return alerts
