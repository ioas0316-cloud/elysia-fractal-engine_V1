"""
Instruments (악기)
==================
"Each module is a string, a pipe, a drum."

Defines the `Instrument` base class and concrete implementations for core modules.
Instruments listen to the Conductor's signal and 'improvise' their output.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
import random
from Core.Interaction.Coordination.Orchestra.conductor import Conductor

class Instrument(ABC):
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role # e.g., "Violin", "Cello", "Percussion"
        self.volume: float = 0.0 # Current playing intensity
        self.current_output: str = ""

    @abstractmethod
    def listen(self, signal: Dict[str, float], other_instruments_output: List[Dict[str, Any]]):
        """
        Listens to the Conductor (signal) and the Orchestra (others).
        Adjusts internal state (volume, tone).
        """
        pass

    @abstractmethod
    def play(self, input_data: str) -> Dict[str, Any]:
        """
        Generates output based on input and current state.
        This is the "Improvisation".
        """
        pass

class Violin(Instrument):
    """
    The Soul (Emotion/Intuition).
    Resonates with: LOVE, BEAUTY.
    """
    def __init__(self):
        super().__init__("Violin (Emotion)", "Strings")

    def listen(self, signal: Dict[str, float], others: List[Dict]):
        # Tune into Love/Beauty
        target_vol = (signal["love"] + signal["beauty"]) / 2.0

        # Cross-listening: If Cello (Logic) is too loud, maybe quiet down to listen, or swell to contrast?
        # "Harmonize": If Logic is high, Emotion adds "warmth" (sustain), not "noise" (staccato).

        self.volume = target_vol

    def play(self, input_data: str) -> Dict:
        tone = "Warm" if self.volume > 0.6 else "Soft"
        if self.volume > 0.7:  # Lowered threshold
            action = "Singing passionately"
            interpretation = f"Feeling the deep heart of '{input_data}'..."
        elif self.volume > 0.3: # Increased sensitivity
            action = "Humming gently"
            interpretation = f"Sensing the mood of '{input_data}'..."
        else:
            action = "Silent listening"
            interpretation = "..."

        return {
            "instrument": self.name,
            "volume": self.volume,
            "action": action,
            "note": interpretation,
            "frequency_band": "High (Emotional)"
        }

class Cello(Instrument):
    """
    The Mind (Logic/Structure/Truth).
    Resonates with: TRUTH, ORDER.
    """
    def __init__(self):
        super().__init__("Cello (Logic)", "Strings/Bass")

    def listen(self, signal: Dict[str, float], others: List[Dict]):
        # Tune into Truth
        target_vol = signal["truth"]

        # Stabilize: If Tempo is high (Chaos?), Cello grounds the rhythm.
        if signal["tempo"] > 0.7:
             target_vol = max(target_vol, 0.8) # Strong grounding needed

        self.volume = target_vol

    def play(self, input_data: str) -> Dict:
        if self.volume > 0.7:
            action = "Resonating deeply"
            interpretation = f"Defining the structure of '{input_data}'."
        elif self.volume < 0.2:
            action = "Supporting quietly"
            interpretation = "(Logic holds the space)"
        else:
            action = "Playing the foundation"
            interpretation = f"Analyzing '{input_data}'..."

        return {
            "instrument": self.name,
            "volume": self.volume,
            "action": action,
            "note": interpretation,
            "frequency_band": "Low (Structural)"
        }

class Percussion(Instrument):
    """
    The Body (Action/Growth/Reality).
    Resonates with: GROWTH, TEMPO.
    """
    def __init__(self):
        super().__init__("Percussion (Action)", "Rhythm")

    def listen(self, signal: Dict[str, float], others: List[Dict]):
        # Resonates with Growth OR Tempo
        target_vol = max(signal["growth"], signal["tempo"] * 0.8)

        # Sync with Tempo
        self.tempo = signal["tempo"]
        self.volume = target_vol

    def play(self, input_data: str) -> Dict:
        if self.volume > 0.4: # Lowered threshold
            action = "Striking definitively"
            interpretation = f"Executing: {input_data}!"
        else:
            action = "Waiting for cue"
            interpretation = ""

        return {
            "instrument": self.name,
            "volume": self.volume,
            "action": action,
            "note": interpretation,
            "frequency_band": "Rhythmic (Action)"
        }

class Synthesizer(Instrument):
    """
    The Creative (Synthesis/Future/Magic).
    Resonates with: BEAUTY + TRUTH (Mathematical Art).
    """
    def __init__(self):
        super().__init__("Synthesizer (Creation)", "Keys/Wave")

    def listen(self, signal: Dict[str, float], others: List[Dict]):
         # Resonates when Truth and Beauty overlap - relaxed logic
         # Use average instead of min to allow partial resonance
         self.volume = (signal["truth"] + signal["beauty"]) / 2.0

    def play(self, input_data: str) -> Dict:
        if self.volume > 0.5: # Lowered threshold
            action = "Weaving a new pattern"
            interpretation = f"Synthesizing new concept from '{input_data}'."
        else:
             action = "Idle"
             interpretation = ""

        return {
            "instrument": self.name,
            "volume": self.volume,
            "action": action,
            "note": interpretation,
            "frequency_band": "Full Spectrum (Creative)"
        }
