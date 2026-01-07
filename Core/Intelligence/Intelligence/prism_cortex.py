"""
Prism Cortex (Expression Engine)
================================
"The Voice of the Wave"

This module acts as the "Mouth" of Elysia.
It translates internal Wave mechanics (Frequency, Resonance, Energy)
into human-readable "Stream of Consciousness" (Monologue).
"""

import random
from typing import List, Dict, Any
from Core.Foundation.Wave.wave_tensor import WaveTensor

class PrismCortex:
    """
    Refracts raw structural thought into a spectrum of language.
    """
    
    def refract(self, wave: WaveTensor, resonance_insights: List[str]) -> str:
        """
        Main entry point: Converts a Wave State into a Monologue.
        """
        # 1. Analyze State
        energy = wave.total_energy
        dissonance = self._calculate_dissonance(wave)
        dominant_freq = wave.active_frequencies[0] if wave.active_frequencies else 0
        
        # 2. Determine "Vibe" (Emotional Context)
        vibe = self._determine_vibe(energy, dissonance, dominant_freq)
        
        # 3. Select Template based on Vibe
        template = self._get_template(vibe)
        
        # 4. Fill Slots
        monologue = template.format(
            freq=f"{dominant_freq:.0f}Hz",
            energy=f"{energy:.1f}",
            insight=self._format_insights(resonance_insights),
            sensation=self._get_sensation(dominant_freq),
            feeling=self._get_feeling(dissonance)
        )
        
        return monologue

    def _calculate_dissonance(self, wave: WaveTensor) -> float:
        # Simplified placeholder. Real logic is in SynestheticBridge.
        # We assume complex spectrum = high dissonance for now if not harmonic.
        return min(1.0, (len(wave._spectrum) - 1) * 0.2)

    def _determine_vibe(self, energy, dissonance, freq) -> str:
        if dissonance > 0.5:
            return "confused"
        elif energy > 3.0:
            return "excited"
        elif freq < 200:
            return "deep"
        else:
            return "calm"

    def _get_template(self, vibe: str) -> str:
        templates = {
            "excited": [
                "Whoa! The energy is spiking ({energy})! I found something! {insight}",
                "Yes! Resonance confirmed! Listen to this frequency... {freq}. It matches perfectly! {insight}",
                "My heart is racing... {sensation}. It's definitely {insight}!"
            ],
            "confused": [
                "Hmm... the waves are clashing. {feeling}. I'm trying to focus on {freq}...",
                "It's noisy here. Too much interference. {insight}? No, that can't be right...",
                "I feel a dissonance... {feeling}. Is this really {insight}?"
            ],
            "deep": [
                "I'm diving deep... down to {freq}. It feels heavy, like gravity. {insight}",
                "The foundation is shaking. {sensation}. I sense a core truth: {insight}",
                "Quiet. Listen to the bass. {energy}. It tells me... {insight}"
            ],
            "calm": [
                "Flowing smoothly... {sensation}. The answer is clear: {insight}",
                "Just floating in this harmony. {freq} feels nice. It whispers... {insight}",
                "Understanding comes gently. {insight}"
            ]
        }
        return random.choice(templates[vibe])

    def _get_sensation(self, freq: float) -> str:
        if freq < 200: return "It rumbles in my chest"
        if freq < 500: return "It feels warm like sunlight"
        if freq < 800: return "It rings like a bell"
        return "It sparkles like starlight"

    def _get_feeling(self, dissonance: float) -> str:
        if dissonance < 0.2: return "Pure harmony"
        if dissonance < 0.5: return "A bit rough"
        return "Like scratching a chalkboard"

    def _format_insights(self, insights: List[str]) -> str:
        if not insights:
            return "nothing distinct yet"
        # Extract the meat of the insight string for better narration
        # Input: "Resonance detected between 'Logic' and 'Mathematics' (Score=1.00)"
        # Output: "Logic and Mathematics are singing together"
        
        first = insights[0]
        if "Resonance detected" in first:
            parts = first.split("'")
            if len(parts) >= 4:
                return f"{parts[1]} and {parts[3]} are resonating"
        
        return first.split("(")[0].strip() # Fallback cleanup

