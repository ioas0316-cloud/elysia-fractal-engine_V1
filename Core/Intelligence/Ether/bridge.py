"""
Ether Bridge (The Word Made Flesh)
==================================

"And the Word became Flesh and dwelt among us."

This module is the Interface between the "Human World" (Language/Text)
and the "Elysian Universe" (Ether/Physics).

It translates:
1. Meaning -> Frequency (Spectral Analysis)
2. Importance -> Mass
3. Emotion/Context -> Spin (Quaternion)
"""

import math
import hashlib
from typing import Tuple
from Core.Intelligence.Consciousness.Ether.ether_node import EtherNode, Quaternion

# Standard Frequency Maps (Hz)
FREQ_LOGIC = 100.0
FREQ_EMOTION = 200.0
FREQ_ETHICS = 300.0
FREQ_WILL = 400.0
FREQ_DIVINE = 963.0

class EtherBridge:
    """
    Converter between Text/Language and EtherNodes.
    """

    @staticmethod
    def text_to_node(text: str, context_weight: float = 1.0) -> EtherNode:
        """
        Materializes a text string into an EtherNode.
        """
        # 1. Analyze Meaning (Simple Heuristics for now)
        # In future, this would use the Neural embeddings.

        mass = EtherBridge._calculate_mass(text) * context_weight
        frequency = EtherBridge._calculate_frequency(text)
        spin = EtherBridge._calculate_spin(text)

        node = EtherNode(
            content=text,
            mass=mass,
            frequency=frequency,
            spin=spin,
            energy=mass * 10.0 # Initial burst of energy upon creation
        )

        # Set initial position based on hash (random but deterministic)
        h = int(hashlib.md5(text.encode()).hexdigest(), 16)
        node.position = Quaternion(
            w=(h % 100) / 10.0 - 5.0,
            x=((h >> 8) % 100) / 10.0 - 5.0,
            y=((h >> 16) % 100) / 10.0 - 5.0,
            z=((h >> 24) % 100) / 10.0 - 5.0
        )

        return node

    @staticmethod
    def _calculate_mass(text: str) -> float:
        """Mass is proportional to length and keyword density."""
        base_mass = math.log(len(text) + 1)

        keywords = ["중요", "핵심", "반드시", "사랑", "원리", "구조", "Elysia"]
        multiplier = 1.0 + sum(0.5 for k in keywords if k in text)

        return base_mass * multiplier

    @staticmethod
    def _calculate_frequency(text: str) -> float:
        """Frequency determines the 'Color' of the thought."""
        score_logic = sum(1 for w in ["논리", "이유", "때문에", "계산"] if w in text)
        score_emotion = sum(1 for w in ["사랑", "기쁨", "슬픔", "느낌"] if w in text)
        score_ethics = sum(1 for w in ["옳은", "가치", "의미", "목적"] if w in text)

        total = score_logic + score_emotion + score_ethics + 1e-9

        # Weighted average frequency
        freq = (score_logic * FREQ_LOGIC +
                score_emotion * FREQ_EMOTION +
                score_ethics * FREQ_ETHICS) / total

        # If no keywords, hash-based frequency to distribute randomly
        if total < 0.1:
            h = int(hashlib.md5(text.encode()).hexdigest(), 16)
            return 400.0 + (h % 200)

        return freq

    @staticmethod
    def _calculate_spin(text: str) -> Quaternion:
        """Spin represents the Perspective (Emotion/Logic/Will/Spirit)."""
        # Simplified: Map 4 axes to keyword counts
        w = 1.0 # Existence
        x = sum(1 for w in ["사랑", "감정"] if w in text) # Emotion
        y = sum(1 for w in ["생각", "논리"] if w in text) # Logic
        z = sum(1 for w in ["의지", "행동"] if w in text) # Will

        return Quaternion(w, x, y, z).normalize()

    @staticmethod
    def interpret_node(node: EtherNode) -> str:
        """
        Translates a node's physical state back into description.
        """
        state = []
        if node.energy > 50.0: state.append("Burning")
        elif node.energy > 10.0: state.append("Active")
        else: state.append("Dormant")

        if node.mass > 10.0: state.append("Massive")
        elif node.mass < 1.0: state.append("Light")

        # Determine Type by Frequency
        if abs(node.frequency - FREQ_LOGIC) < 50: dtype = "Logical"
        elif abs(node.frequency - FREQ_EMOTION) < 50: dtype = "Emotional"
        elif abs(node.frequency - FREQ_ETHICS) < 50: dtype = "Ethical"
        elif abs(node.frequency - FREQ_DIVINE) < 50: dtype = "Divine"
        else: dtype = "Unknown"

        return f"[{dtype}/{'/'.join(state)}] '{str(node.content)[:20]}...'"
