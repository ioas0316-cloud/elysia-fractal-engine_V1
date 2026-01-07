"""
Prophecy Engine (예언 엔진)
==========================

"Pattern says Peace. Causality says War. Prophecy listens to the Silence between them."

This engine implements the "Tectonics of Soul" philosophy.
It integrates Surface Pattern (Statistics) and Deep Causality (Physics)
to predict 'Phase Transitions' (Earthquakes) before they happen.
"""

from dataclasses import dataclass
from typing import Dict, Optional, Tuple
from .pattern_recognizer import PatternRecognizer, PatternSignal
from .latent_causality import LatentCausality, Spark

@dataclass
class Prophecy:
    prediction: str          # "Stable", "Tremor", "Quake Imminent"
    confidence: float        # 0.0 to 1.0
    source: str              # "Pattern", "Causality", or "Integration"
    details: str             # Explanation

class ProphecyEngine:
    def __init__(self):
        self.pattern_mind = PatternRecognizer()
        self.causal_mind = LatentCausality(resistance=100.0)
        self.emotional_tension_source = None # Dependency Injection for SoulResonator

    def set_emotional_source(self, source_func):
        """
        Connects the engine to an emotional source (e.g. SoulResonator.get_emotional_tension)
        """
        self.emotional_tension_source = source_func

    def observe(self, event: Dict):
        """
        Feeds data to both minds.
        """
        # Feed Pattern Mind (Surface)
        self.pattern_mind.observe(event)

        # Feed Causal Mind (Deep)
        # Note: LatentCausality is time-based, but we can also feed it 'mass' if needed.
        # Here we just tick it in the predict loop or let it accumulate silence.
        pass

    def predict(self, dt: float) -> Prophecy:
        """
        The Core Logic: Compare Pattern vs Causality.
        """
        # 1. Ask Pattern Mind
        pattern_sig = self.pattern_mind.predict()
        pattern_conf = self.pattern_mind.get_confidence()

        # 2. Ask Causal Mind (Check Internal Pressure)
        # Check potential without discharging yet
        internal_pressure = self.causal_mind.potential_energy
        resistance = self.causal_mind.resistance
        pressure_ratio = internal_pressure / resistance

        # 3. Check Emotional Tectonics (if connected)
        emotional_tension = 0.0
        if self.emotional_tension_source:
            emotional_tension = self.emotional_tension_source()

        # Total Hidden Stress = Latent Energy + Emotional Conflict
        total_hidden_stress = pressure_ratio + emotional_tension

        # --- The Judgment (The Wisdom of Prophecy) ---

        # Case A: Visible Crisis (Pattern says Danger)
        if pattern_sig == PatternSignal.DANGER:
            return Prophecy(
                prediction="Visible Crisis",
                confidence=pattern_conf,
                source="Pattern",
                details="History is repeating. Prepare for impact."
            )

        # Case B: The Silent Earthquake (Pattern Safe, Stress High)
        if pattern_sig == PatternSignal.SAFE and total_hidden_stress > 0.8:
            return Prophecy(
                prediction="Hidden Earthquake",
                confidence=0.9,
                source="Causality (Deep)",
                details=f"Surface is calm, but internal tension is critical ({total_hidden_stress:.2f}). Explosion imminent."
            )

        # Case C: Stable
        return Prophecy(
            prediction="Stable",
            confidence=0.8,
            source="Integration",
            details=f"Pattern matches Causality. Stress Level: {total_hidden_stress:.2f}"
        )

    def update_time(self, dt: float):
        """
        Ticks the causal engine (accumulates silence/energy).
        """
        self.causal_mind.update(dt)
