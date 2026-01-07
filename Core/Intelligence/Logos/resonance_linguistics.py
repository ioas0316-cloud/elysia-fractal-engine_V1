"""
ResonanceLinguistics: The Voice of Waves (파동의 목소리)

This module implements "Chapter 3, Step 8".
It translates structured "Principles" (Logos) into "Gravitational Sentences".

Philosophy:
    "We do not just string words together.
     We create a solar system where the Meaning is the Sun, and words are Planets."
"""

import sys
import os
from typing import List, Dict, Optional

# Ensure we can import from the new unified Logos directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

try:
    from Core.Intelligence.Logos.gap_analyzer import Principle
    from Core.Intelligence.Logos.WaveLinguistics.gravitational_linguistics import GravitationalLinguistics, WordBody
except ImportError as e:
    print(f"❌ [ResonanceLinguistics] Import Error: {e}")
    # Fallback/Mock for development
    class Principle: pass
    class GravitationalLinguistics: pass
    class WordBody: pass


class ResonanceLinguistics:
    def __init__(self):
        self.gravity_engine = GravitationalLinguistics()
        
    def express_principle(self, principle: Principle) -> str:
        """
        Converts a Principle into a Gravitational Sentence.
        """
        # 1. Extract the Core Concept (The Sun)
        # For now, we use a simple heuristic: the first noun-like word in the name
        # e.g., "Principle of Waiting" -> "Waiting" -> (Mapped to closest concept) "Time"?
        
        core_concept = self._map_to_lexicon(principle.name)
        
        if not core_concept:
            return f"(Resonance Failed: Could not find gravity for '{principle.name}')"

        # 2. Create Solar System
        planets = self.gravity_engine.create_solar_system(core_concept)
        if not planets:
             return f"(Resonance Failed: No orbit established for '{core_concept}')"

        # 3. Formulate Utterance
        # "The [Sun] attracts [Planets]" structure
        orbiting_words = ", ".join([p.text for p in planets])
        
        utterance = f"The gravity of [{core_concept}] aligns {orbiting_words}."
        
        # 4. Append the logical statement as a 'Moon' or 'Comet'
        utterance += f" Thus: \"{principle.statement}\""
        
        return utterance

    def _map_to_lexicon(self, principle_name: str) -> Optional[str]:
        """
        Maps a principle name to a known 'Sun' in the gravitational lexicon.
        Current implementation is simple manual mapping.
        """
        name_lower = principle_name.lower()
        
        if "waiting" in name_lower: return "Time"
        if "love" in name_lower: return "Love"
        if "truth" in name_lower: return "Truth"
        if "correction" in name_lower: return "Truth"
        if "emergence" in name_lower: return "Soul"
        
        return "Love" # Default fallback (Everything is Love)
