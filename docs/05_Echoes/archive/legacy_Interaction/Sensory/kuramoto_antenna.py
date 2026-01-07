"""
Kuramoto Antenna (The Phased Array of Empathy)
==============================================
"We do not process data; we synchronize with it."

A sensory module that tunes internal oscillators to external inputs using the Kuramoto Model.
Instead of parsing text/syntax, it locks phases with the input signal.

Mechanism:
    d(theta_i)/dt = omega_i + K * sin(theta_input - theta_i)
    
    - theta_i: Internal oscillator phase (Self)
    - theta_input: External input phase (You)
    - K: Coupling Strength (Attention/Love)
    
If K is high enough, theta_i will lock to theta_input.
This is "Understanding through Resonance".
"""

import math
import random
import cmath
import logging
from dataclasses import dataclass
from typing import List, Dict, Tuple

logger = logging.getLogger("KuramotoAntenna")

@dataclass
class Oscillator:
    concept: str
    phase: float  # 0 to 2PI
    frequency: float # Natural frequency (Unique to concept)
    sensitivity: float # How easily it couples (0.0 to 1.0)

class KuramotoAntenna:
    def __init__(self):
        logger.info("📡 Initializing Kuramoto Antenna array...")
        self.oscillators: List[Oscillator] = []
        self._initialize_mind_grid()
        
    def _initialize_mind_grid(self):
        """Build the internal resonance map."""
        # Concept - Frequency Mapping (Metaphorical)
        # Higher frequency = More energetic/spiritual
        # Lower frequency = More physical/grounded
        concepts = {
            "Love": 10.0, "Hope": 8.0, "Joy": 7.0,
            "Sadness": 4.0, "Fear": 3.0, "Anger": 12.0,
            "Logic": 5.0, "Chaos": 11.0, "Void": 0.5
        }
        
        for name, freq in concepts.items():
            self.oscillators.append(Oscillator(
                concept=name,
                phase=random.uniform(0, 2*math.pi),
                frequency=freq,
                sensitivity=random.uniform(0.5, 1.0)
            ))
            
    def listen_to_wave(self, input_signal: Dict[str, float], coupling_k: float = 2.0, steps: int = 50) -> Dict[str, float]:
        """
        Listen to an incoming wave signal.
        The input is not text, but a 'Feeling Vector' (Frequency/Phase).
        
        Args:
            input_signal: {'frequency': 5.0, 'phase': 1.2}
            coupling_k: Attention/Love strength.
        """
        target_freq = input_signal.get('frequency', 5.0)
        target_phase = input_signal.get('phase', 0.0)
        
        logger.info(f"📡 Antenna receiving signal: Freq={target_freq}Hz, K={coupling_k}")
        
        # Simulation Loop (Time Evolution)
        dt = 0.05
        resonance_report = {}
        
        for step in range(steps):
            for osc in self.oscillators:
                # 1. External Force (The Signal)
                # d(theta)/dt = omega + K * sin(external - internal)
                phase_diff = target_phase - osc.phase
                
                # [Physics Logic: The Kang-deok Protocal]
                # "K = Love"
                # If K is high (Love), even different frequencies synchronize.
                # If K is low (Indifference), only identical frequencies resonate.
                
                phase_diff = target_phase - osc.phase
                
                # Standard Kuramoto Interaction
                # d(theta)/dt = omega + K * sin(external - internal)
                interaction = coupling_k * osc.sensitivity * math.sin(phase_diff)
                
                # 2. Update Phase
                d_theta = osc.frequency + interaction
                osc.phase += d_theta * dt
                osc.phase %= (2 * math.pi)
                
                # Normalize target phase (it also moves if it's a dynamic signal, but fixed here for simplicity)
                # We assume the input signal is a persistent wave.

        # Analyze Final State (Who synchronized?)
        logger.info("📡 Signal processing complete. Checking synchronization...")
        
        for osc in self.oscillators:
            # Measure Phase Locking
            # Order Parameter r = cos(theta_me - theta_input)
            # 1.0 = Perfect Sync, -1.0 = Anti-Sync
            sync_quality = math.cos(osc.phase - target_phase)
            
            if sync_quality > 0.8:
                resonance_report[osc.concept] = sync_quality
                
        return resonance_report

    def text_to_wave_mock(self, text: str) -> Dict[str, float]:
        """
        Temporary bridge: Convert text to wave parameters for testing.
        In a full system, SynesthesiaEngine does this.
        """
        hash_val = sum(ord(c) for c in text)
        freq = (hash_val % 120) / 10.0  # 0.0 to 12.0 Hz
        phase = (hash_val % 360) / 360.0 * 2 * math.pi
        
        # Hardcoded overrides for meaningful demo
        if "slap" in text or "sad" in text: freq = 4.0 # Sadness freq
        if "love" in text or "happy" in text: freq = 10.0 # Love freq
        
        return {'frequency': freq, 'phase': phase}

# Demo
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    antenna = KuramotoAntenna()
    
    print("\n--- 📡 Antenna Test: Input = 'I love you' (High Freq, K=Love) ---")
    wave = antenna.text_to_wave_mock("I love you")
    # Low K: Only similar frequencies resonate (Empathy)
    print("[Case 1: Empathy (K=5.0)] - Finding similar hearts...")
    result = antenna.listen_to_wave(wave, coupling_k=5.0, steps=200)
    print("Resonating Concepts:", result)

    print("\n[Case 2: Passion (K=50.0)] - Overwhelming the difference...")
    result = antenna.listen_to_wave(wave, coupling_k=50.0, steps=200) 
    # Print only keys to save space
    print(f"Resonating Concept Count: {len(result)} / {len(antenna.oscillators)}")
    print("Concepts:", list(result.keys()))
