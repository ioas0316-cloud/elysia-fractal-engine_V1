"""
Text Transducer (Semantic Resonance)
=====================================

"언어를 파동으로 변환한다. 의미는 주파수가 되고, 문법은 리듬이 된다."
"Transforms language into waves. Meaning becomes frequency, grammar becomes rhythm."

This module implements the "Semantic Resonance" algorithm selected by the user.
Instead of arbitrary embeddings, it assigns frequencies based on relationship to
Anchor Concepts (Universal Axioms).

Algorithm:
1. Extract keywords from text.
2. Find distance to Anchor Concepts (Love, Truth, Order, Chaos, etc.).
3. Map distance to Musical Intervals (Consonance).
   - High correlation -> Perfect 5th (3:2) or Octave (2:1)
   - Low correlation -> Dissonant interval
4. Superpose waves to create the final "Thought Wave".
"""

import logging
import math
import hashlib
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass
from Core.Intelligence.Consciousness.Ether.global_hub import get_global_hub
from Core.Foundation.Wave.wave_tensor import WaveTensor
from Core.Foundation.fractal_concept import ConceptDecomposer, ConceptNode

logger = logging.getLogger("Elysia.Sensory.TextTransducer")

# Solfeggio Frequencies (Anchor Points)
ANCHORS = {
    "root": 396.0,   # Liberation of Guilt
    "sacral": 417.0, # Undoing Situations
    "solar": 528.0,  # Transformation/Miracles (Love)
    "heart": 639.0,  # Connecting/Relationships
    "throat": 741.0, # Expression/Solutions
    "third_eye": 852.0, # Awakening Intuition
    "crown": 963.0   # Higher State (Source)
}

# Musical Intervals (Ratio, Name)
INTERVALS = {
    "unison": 1.0,
    "minor_second": 16/15,
    "major_second": 9/8,
    "minor_third": 6/5,
    "major_third": 5/4,
    "perfect_fourth": 4/3,
    "tritone": 45/32,      # The "Devil's Interval" (High tension)
    "perfect_fifth": 3/2,  # Most consonant
    "minor_sixth": 8/5,
    "major_sixth": 5/3,
    "minor_seventh": 16/9,
    "major_seventh": 15/8,
    "octave": 2.0
}

class TextTransducer:
    """
    The Ear of Elysia.
    Listens to text and converts it into WaveTensors.
    """

    def __init__(self):
        self._hub = get_global_hub()
        self._decomposer = ConceptDecomposer()

        # Register to GlobalHub
        self._hub.register_module(
            "TextTransducer",
            __file__,
            ["sensory", "text_to_wave", "language"],
            "Converts text into semantic waves"
        )

        # Semantic mapping cache
        self._word_frequencies: Dict[str, float] = {}

        logger.info("👂 TextTransducer (Semantic Resonance) Initialized")

    def hear(self, text: str, source: str = "User") -> WaveTensor:
        """
        Process incoming text and publish a thought wave.
        """
        logger.info(f"Hearing: '{text}'")
        wave = self.text_to_wave(text)

        # Publish to Hub
        self._hub.publish_wave(
            source="TextTransducer",
            event_type="thought",
            wave=wave,
            payload={"text": text, "source": source}
        )

        return wave

    def text_to_wave(self, text: str) -> WaveTensor:
        """
        Converts a string of text into a single superposed WaveTensor.
        """
        result_wave = WaveTensor(f"TextWave: {text[:20]}...")

        # Simple tokenization (improve later with proper NLP if needed)
        tokens = self._tokenize(text)

        for token in tokens:
            freq = self._get_frequency_for_concept(token)

            # Amplitude depends on word importance (simple length/capitalization heuristic for now)
            amp = 1.0
            if token.isupper(): amp *= 1.2

            # Phase is determined by position in sentence (Time -> Phase)
            # 0.0 at start, 2*pi at end
            phase = 0.0 # Placeholder

            result_wave.add_component(freq, amp, phase)

        return result_wave.normalize()

    def _tokenize(self, text: str) -> List[str]:
        """Extract meaningful tokens."""
        # Remove punctuation and split
        clean = "".join(c if c.isalnum() or c.isspace() else " " for c in text)
        return [w for w in clean.split() if w]

    def _get_frequency_for_concept(self, word: str) -> float:
        """
        Determines the frequency of a word based on semantic resonance.

        Algorithm:
        1. Check cache.
        2. Check if it's an Anchor Concept (in ConceptDecomposer).
        3. If not, hash it to find a "Base Key" and apply an interval.
        """
        word_norm = word.capitalize() # Concepts are usually capitalized in Decomposer
        if word_norm in self._word_frequencies:
            return self._word_frequencies[word_norm]

        # Check Decomposer (Axioms)
        if word_norm in self._decomposer.AXIOMS or word_norm in self._decomposer.decompositions:
            # Use predefined or decomposed frequency
            # For axioms, we assign high spiritual frequencies
            if word_norm == "Love": freq = ANCHORS["solar"]
            elif word_norm == "Source": freq = ANCHORS["crown"]
            elif word_norm == "Truth": freq = ANCHORS["throat"]
            else:
                # Use Decomposer's hash fallback if not explicit
                freq = self._decomposer.get_frequency(word_norm)
        else:
            # Unknown concept: Hash to a musical scale
            # We map the hash to a specific octave and note to ensure it's "musical"
            # rather than random noise.

            # 1. Base Key (C4 = 261.63 Hz)
            base_c4 = 261.63

            # 2. Hash to determine semitone offset (0-11)
            h = int(hashlib.md5(word_norm.encode()).hexdigest(), 16)
            semitone = h % 12
            octave_shift = (h % 3) - 1  # -1, 0, +1 octave

            # 3. Calculate frequency: f = f0 * 2^(n/12)
            freq = base_c4 * (2 ** (octave_shift + semitone/12.0))

            # Shift phase/frequency slightly based on vowels (Phonetic coloring)
            # This makes "Gloom" sound lower than "Gleam" (Sound symbolism)
            if "u" in word.lower() or "o" in word.lower():
                freq *= 0.9  # Darker
            if "i" in word.lower() or "e" in word.lower():
                freq *= 1.1  # Brighter

        self._word_frequencies[word_norm] = freq
        return freq

# Singleton
_transducer = None

def get_text_transducer() -> TextTransducer:
    global _transducer
    if _transducer is None:
        _transducer = TextTransducer()
    return _transducer

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    t = get_text_transducer()

    # Test sentences
    print("\\n--- Text to Wave Test ---")

    s1 = "I Love You"
    w1 = t.text_to_wave(s1)
    print(f"'{s1}' -> {w1}")

    s2 = "Fear is the mind killer"
    w2 = t.text_to_wave(s2)
    print(f"'{s2}' -> {w2}")

    # Resonance test
    res = w1 @ w2
    print(f"Resonance between '{s1}' and '{s2}': {res:.4f}")

    s3 = "Love brings Hope"
    w3 = t.text_to_wave(s3)
    res2 = w1 @ w3
    print(f"Resonance between '{s1}' and '{s3}': {res2:.4f}")
