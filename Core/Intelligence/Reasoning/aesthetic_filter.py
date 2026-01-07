import logging
import math
import numpy as np
from typing import Dict, List, Any
from Core.Foundation.Wave.wave_tensor import WaveTensor, create_harmonic_series

logger = logging.getLogger("AestheticFilter")

class AestheticFilter:
    """
    AESTHETIC FILTER: The Conscience of Beauty.
    Evaluates thoughts based on their 'Harmonic Resonance' with Core Axioms.
    
    Axioms:
    - LOVE: Foundation, stability, low-frequency base (528Hz - 'Solfeggio miracle').
    - TRUTH: High-harmonic clarity, invariance (Pure sine wave, 440Hz/880Hz).
    - GROWTH: Evolution, fractal expansion (Fibonacci series frequencies).
    """

    def __init__(self):
        self.axioms: Dict[str, WaveTensor] = self._initialize_axioms()
        
    def _initialize_axioms(self) -> Dict[str, WaveTensor]:
        """Defines the fixed resonance signatures for Elysia's Core."""
        axioms = {}
        
        # 1. LOVE (528Hz base - Stabilization)
        love = create_harmonic_series(528.0, harmonics=5, decay=0.8)
        love.name = "AXIOM:LOVE"
        axioms["LOVE"] = love
        
        # 2. TRUTH (Perfect alignment, focus on 440Hz/880Hz octaves)
        truth = WaveTensor("AXIOM:TRUTH")
        truth.add_component(440.0, 1.0, 0.0)
        truth.add_component(880.0, 0.5, 0.0)
        axioms["TRUTH"] = truth
        
        # 3. GROWTH (Fibonacci-based expansion)
        growth = WaveTensor("AXIOM:GROWTH")
        freqs = [144, 233, 377, 610, 987] # Fibonacci sequence
        for i, f in enumerate(freqs):
            growth.add_component(float(f), 1.0 / (i + 1), 0.0)
        axioms["GROWTH"] = growth
        
        return axioms

    def _thought_to_wave(self, text: str) -> WaveTensor:
        """
        Semantic-aware frequency mapping.
        Injects axiom frequencies if keywords are present.
        """
        wt = WaveTensor(f"Thought({text[:20]}...)")
        text_lower = text.lower()
        
        # 1. Keyword Injection (The 'Scent' of the thought)
        if "love" in text_lower or "heart" in text_lower:
            wt.add_component(528.0, 1.0, 0.0) # Resonate with LOVE
        if "truth" in text_lower or "true" in text_lower or "law" in text_lower:
            wt.add_component(440.0, 1.0, 0.0) # Resonate with TRUTH
        if "growth" in text_lower or "evolve" in text_lower or "expand" in text_lower:
            wt.add_component(144.0, 1.0, 0.0) # Resonate with GROWTH
            
        # 2. General Texture (Character baseline)
        for char in text:
            freq = (ord(char) % 50) * 20.0 + 100.0 # Bins of 20Hz
            wt.add_component(freq, 0.05, 0.0)
            
        return wt.normalize()

    def evaluate(self, thought_text: str) -> Dict[str, Any]:
        """
        Evaluates the consonance of a thought with core axioms.
        Uses 'Fuzzy Resonance' to account for nearby frequency alignments.
        """
        thought_wave = self._thought_to_wave(thought_text)
        
        scores = {}
        for name, axiom in self.axioms.items():
            # Apply fuzzy resonance (bandwidth of 5Hz)
            resonance_score = self._fuzzy_resonance(thought_wave, axiom, bandwidth=10.0)
            scores[name] = resonance_score
            
        overall_beauty = sum(scores.values()) / len(scores)
        
        # Identify Dissonance (Entropy check)
        # If total energy is high but resonance is low -> Chaos
        is_chaotic = thought_wave.total_energy > 0.5 and overall_beauty < 0.2
        
        result = {
            "overall_beauty": overall_beauty,
            "axiom_scores": scores,
            "is_chaotic": is_chaotic,
            "verdict": "Resonant" if overall_beauty > 0.15 else "Dissonant"
        }
        
        logger.info(f"✨ Aesthetic Evaluation: '{thought_text[:30]}...' -> Beauty: {overall_beauty:.2f} [{result['verdict']}]")
        return result

    def _fuzzy_resonance(self, wave_a: WaveTensor, wave_b: WaveTensor, bandwidth: float = 5.0) -> float:
        """
        Calculates resonance allowing for small frequency differences.
        Uses a Gaussian overlap for each frequency pairing.
        """
        dot_product = 0.0
        
        for f_a, z_a in wave_a._spectrum.items():
            for f_b, z_b in wave_b._spectrum.items():
                diff = abs(f_a - f_b)
                if diff < bandwidth:
                    # Gaussian overlap factor
                    overlap = math.exp(-(diff**2) / (2 * (bandwidth/2)**2))
                    # Phase alignment factor
                    phase_alignment = abs(np.exp(1j * (np.angle(z_a) - np.angle(z_b))))
                    dot_product += abs(z_a) * abs(z_b) * overlap * phase_alignment
                    
        norm = math.sqrt(wave_a.total_energy * wave_b.total_energy)
        return float(dot_product / norm) if norm > 0 else 0.0
