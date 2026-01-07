"""
Resonance Hall (공명 홀)
======================
"Where the individual notes become a Symphony."

This module acts as the stage. It:
1. Gathers all instruments.
2. Broadcasts the Conductor's signal.
3. Collects outputs.
4. Harmonizes the result into a single 'Symphonic Output'.
"""

from typing import List, Dict, Any
from Core.Interaction.Coordination.Orchestra.conductor import Conductor, get_conductor
from Core.Interaction.Coordination.Orchestra.instruments import Instrument, Violin, Cello, Percussion, Synthesizer

class ResonanceHall:
    def __init__(self):
        self.conductor = get_conductor()
        self.instruments: List[Instrument] = [
            Violin(),
            Cello(),
            Percussion(),
            Synthesizer()
        ]
        self.history: List[str] = []

    def perform(self, input_context: str) -> Dict[str, Any]:
        """
        Conducts a performance based on the input context.
        """
        # 1. Conductor analyzes context and sets the Wave Signal
        signal = self.conductor.conduct(input_context)
        inspiration = self.conductor.inspire()

        # 2. Instruments Listen (First Pass)
        # In a real continuous system, this would be a loop.
        # Here we simulate one 'tick' of listening.
        current_outputs = [] # Previous tick's outputs could go here for cross-listening

        for inst in self.instruments:
            inst.listen(signal, current_outputs) # They listen to the signal

        # 3. Instruments Play (Improvisation)
        section_outputs = []
        for inst in self.instruments:
            output = inst.play(input_context)
            if output["note"]: # Only capture if playing
                section_outputs.append(output)

        # 4. Harmonization (Mixing)
        # Combine notes into a coherent narrative
        harmony_text = f"[Theme: {self.conductor.current_theme.name} | {inspiration}]\n"
        for out in section_outputs:
            harmony_text += f"   🎵 {out['instrument']}: {out['note']} ({out['action']})\n"

        return {
            "theme": self.conductor.current_theme.name,
            "signal": signal,
            "performance": section_outputs,
            "full_harmony": harmony_text
        }

# Singleton
_hall_instance = None
def get_resonance_hall() -> ResonanceHall:
    global _hall_instance
    if _hall_instance is None:
        _hall_instance = ResonanceHall()
    return _hall_instance
