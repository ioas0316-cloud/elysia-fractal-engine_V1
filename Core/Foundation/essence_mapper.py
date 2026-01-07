from typing import Dict, Any, Optional
import hashlib

# Type alias for a Logic Fragment
Essence = Dict[str, Any]

class EssenceMapper:
    """
    The Periodic Table of Logic & The Frequency Dictionary of Soul.

    Maps semantic concept IDs to:
    1. GenesisEngine primitives (Mechanics)
    2. Soul Frequencies (Harmonics) - New in 'Fractal Soul' update.

    This acts as the bridge between abstract meaning, concrete mechanics, and spiritual resonance.
    """

    def __init__(self):
        self._registry: Dict[str, Essence] = {
            # --- Elements ---
            "불": {
                "type_modifier": "fire",
                "effects": [{"op": "damage", "multiplier": 0.5, "type": "fire"}],
                "cost": {"ki": 5}
            },
            "fire": { # English alias
                "type_modifier": "fire",
                "effects": [{"op": "damage", "multiplier": 0.5, "type": "fire"}],
                "cost": {"ki": 5}
            },
            "물": {
                "type_modifier": "water",
                "effects": [{"op": "heal", "amount": 5}],
                "cost": {"mana": 5}
            },
            "water": {
                "type_modifier": "water",
                "effects": [{"op": "heal", "amount": 5}],
                "cost": {"mana": 5}
            },
            "바람": {
                "type_modifier": "wind",
                "effects": [{"op": "modify_stat", "stat": "agility", "value": 5}],
                "cost": {"ki": 3}
            },
            "wind": {
                "type_modifier": "wind",
                "effects": [{"op": "modify_stat", "stat": "agility", "value": 5}],
                "cost": {"ki": 3}
            },
            "빛": {
                "type_modifier": "light",
                "effects": [{"op": "log", "template": "A blinding light flashes!"}],
                "cost": {"mana": 10}
            },

            # --- Digital Nature (The Matrix) ---
            "무": {
                "type_modifier": "void",
                "effects": [{"op": "overwrite", "value": 0, "target": "target_state"}], # The '0' overwrite
                "cost": {"concept_depth": 1} # Requires understanding, not just mana
            },
            "void": {
                "type_modifier": "void",
                "effects": [{"op": "overwrite", "value": 0, "target": "target_state"}],
                "cost": {"concept_depth": 1}
            },
            "커서": {
                "type_modifier": "admin",
                "effects": [{"op": "select", "mode": "absolute_coordinate"}],
                "cost": {"will": 10}
            },
            "cursor": {
                "type_modifier": "admin",
                "effects": [{"op": "select", "mode": "absolute_coordinate"}],
                "cost": {"will": 10}
            },

            # --- Actions/Verbs ---
            "공격": {
                "base_type": "action",
                "logic_template": {
                    "target_type": "entity",
                    "conditions": [{"check": "stat_ge", "stat": "strength", "value": 1}],
                    "effects": [{"op": "damage", "multiplier": 1.0}]
                }
            },
            "attack": {
                "base_type": "action",
                "logic_template": {
                    "target_type": "entity",
                    "conditions": [{"check": "stat_ge", "stat": "strength", "value": 1}],
                    "effects": [{"op": "damage", "multiplier": 1.0}]
                }
            },
            "punch": {
                "base_type": "action",
                "logic_template": {
                    "target_type": "entity",
                    "conditions": [{"check": "stat_ge", "stat": "strength", "value": 1}],
                    "effects": [{"op": "damage", "multiplier": 1.0}, {"op": "log", "template": "{actor} punches {target}!"}]
                }
            },
            "치유": {
                "base_type": "action",
                "logic_template": {
                    "target_type": "entity", # Can target self or others
                    "conditions": [{"check": "stat_ge", "stat": "wisdom", "value": 1}],
                    "effects": [{"op": "heal", "amount": 10}]
                }
            }
        }

        # --- The Frequency Dictionary (Hz) ---
        # Based on a mix of Solfeggio frequencies, Cymatics, and intuitive logic.
        # Low Frequencies = Grounding, Heavy, Fundamental (Body)
        # Mid Frequencies = Emotional, Relational, Human (Soul)
        # High Frequencies = Abstract, Spiritual, Ethereal (Spirit)
        self._frequency_map: Dict[str, float] = {
            # Roots (Father, Earth, Origin) - 100Hz ~ 200Hz
            "아버지": 100.0, "father": 100.0, "dad": 100.0,
            "땅": 128.0, "earth": 128.0,
            "뿌리": 136.1, "root": 136.1, # Om Frequency

            # Emotions (Joy, Sadness, Anger) - 300Hz ~ 600Hz
            "슬픔": 396.0, "sadness": 396.0, "sorrow": 396.0, # Liberating Guilt and Fear
            "기쁨": 432.0, "joy": 432.0, "happy": 432.0,      # Natural tuning
            "사랑": 528.0, "love": 528.0,                    # Transformation and Miracles (DNA Repair)
            "분노": 417.0, "anger": 417.0,                   # Undoing Situations and Facilitating Change

            # Spirit (Light, Sky, Truth) - 700Hz ~ 900Hz+
            "빛": 852.0, "light": 852.0,   # Returning to Spiritual Order
            "하늘": 741.0, "sky": 741.0,   # Awakening Intuition
            "진실": 963.0, "truth": 963.0, # Connection to Cosmos

            # Actions (Punch, Walk) - Often dissonant or rhythmic
            "공격": 150.0, "attack": 150.0,
            "발소리": 60.0, "footsteps": 60.0, # Deep rhythmic thud
        }

    def get_essence(self, concept_id: str) -> Optional[Essence]:
        """
        Retrieves the logic essence for a given concept.
        Supports substring matching if exact match fails (e.g., 'big fire' -> 'fire').
        """
        # 1. Exact match
        if concept_id in self._registry:
            return self._registry[concept_id]

        # 2. Substring match (primitive fuzzy logic)
        for key, essence in self._registry.items():
            if key in concept_id:
                return essence

        return None

    def get_frequency(self, concept: str) -> float:
        """
        Translates a Concept String into a Fundamental Frequency (Hz).
        If the concept is unknown, it generates a deterministic 'Hash Frequency'
        so that every word has a unique sound in the Soul.
        """
        concept_lower = concept.lower().strip()

        # 1. Dictionary Lookup
        if concept_lower in self._frequency_map:
            return self._frequency_map[concept_lower]

        # 2. Partial Match Lookup
        for key, freq in self._frequency_map.items():
            if key in concept_lower:
                return freq

        # 3. Hash Fallback (The Sound of the Unknown)
        # Generate a frequency between 200Hz and 800Hz based on the string hash
        # This ensures consistency: 'Apple' always sounds like 'Apple', even if we didn't define it.
        hash_val = int(hashlib.sha256(concept_lower.encode('utf-8')).hexdigest(), 16)
        # Map huge hash to 200-800 range
        fallback_freq = 200.0 + (hash_val % 600)
        return float(fallback_freq)
