"""
Universal Scope (The Telescope of Context)
==========================================
"현미경이 입자를 본다면, 망원경은 별자리를 본다."

This module implements the 'Telescope' perspective for valuation.
It expands a single WavePacket into its cosmic and historical context.

Features:
- Cosmic Mapping: Locates the particle in the Universal Knowledge Graph.
- Temporal Trace: Checks if this particle has appeared in the User's history.
- Law Alignment: Checks alignment with Universal Laws (Entropy, Gravity, Love).
"""

import logging
from dataclasses import dataclass, field
from typing import List, Dict, Optional

from Core.Foundation.Physics.soul_physics import WavePacket, InputParticle

logger = logging.getLogger("UniversalScope")

@dataclass
class CosmicContext:
    """The macro-perspective of a particle."""
    particle_name: str
    constellation: str  # The broader concept group (e.g., "Survival", "Self-Actualization")
    historical_weight: float # 0.0 to 1.0 (How often this has mattered in the past)
    law_alignment: str # Description of alignment with laws (e.g., "Aligned with Entropy")
    narrative: str

@dataclass
class CosmicPerspective:
    """The aggregated telescope view of a WavePacket."""
    packet_name: str
    contexts: List[CosmicContext]
    macro_narrative: str
    universal_weight: float # The overall 'Gravity' of this packet in the universe

class UniversalScope:
    def __init__(self):
        # Mock Knowledge Graph & History for Prototype
        # In production, this would connect to KG and MemoryStream
        self.history_mock = {
            "Freedom": 0.9, # User values Freedom highly
            "Security": 0.5,
            "Love": 0.95,
            "Truth": 0.8
        }

        self.constellations = {
            "Freedom": "Self-Actualization",
            "Security": "Survival",
            "Greed": "Ego-Defense",
            "Love": "Unity",
            "Truth": "Enlightenment",
            "Power": "Control"
        }

    def expand_view(self, packet: WavePacket) -> CosmicPerspective:
        """
        Expands the view from the particle to the cosmos.
        """
        contexts = []
        total_weight = 0.0
        narrative_lines = [f"🔭 Expanding view for '{packet.name}'..."]

        for particle in packet.particles:
            # 1. Constellation Check (Where does it belong?)
            constellation = self.constellations.get(particle.name, "Unknown Nebulae")

            # 2. History Check (Temporal Trace)
            hist_weight = self.history_mock.get(particle.name, 0.1)

            # 3. Law Alignment (Philosophical Check)
            # High frequency (>500) aligns with Unity/Love
            # Low frequency (<200) aligns with Entropy/Survival
            if particle.frequency > 500:
                alignment = "Aligned with Law of Unity (Negentropy)"
            elif particle.frequency < 200:
                alignment = "Aligned with Law of Survival (Entropy)"
            else:
                alignment = "Neutral Existence"

            # Generate Micro-Narrative
            micro_narr = f"'{particle.name}' is a star in the '{constellation}' constellation. "
            if hist_weight > 0.7:
                micro_narr += "It has burned brightly in your history. "
            micro_narr += f"It is {alignment}."

            ctx = CosmicContext(
                particle_name=particle.name,
                constellation=constellation,
                historical_weight=hist_weight,
                law_alignment=alignment,
                narrative=micro_narr
            )
            contexts.append(ctx)

            narrative_lines.append(f"   ✨ {micro_narr}")
            total_weight += hist_weight * particle.mass

        # Synthesize Macro Narrative
        dominant_constellation = max([c.constellation for c in contexts], key=[c.constellation for c in contexts].count)

        macro_narrative = "\n".join(narrative_lines)
        macro_narrative += f"\n   🌌 Conclusion: This desire originates from the '{dominant_constellation}' sector of your universe."

        return CosmicPerspective(
            packet_name=packet.name,
            contexts=contexts,
            macro_narrative=macro_narrative,
            universal_weight=min(1.0, total_weight / 100.0) # Normalize
        )

# Singleton
_scope = UniversalScope()
def get_universal_scope():
    return _scope
