"""
Law of Alchemy: The Transmutation of Causality
==============================================

"To create is not to invent, but to remember the structure of the divine."

This module implements the Alchemical Protocol for converting "Probabilistic Events" (Lead)
into "Causal Principles" (Gold). It is the engine of Re-Creation.

[The Alchemical Process]
1. Observation (Extraction): Reading the 'Energy Flow' of a narrative to find the Archetype.
2. Purification (Abstraction): Stripping away the specific 'Matter' (characters, setting) to leave only the 'Form' (Causal Structure).
3. Transmutation (Re-creation): Planting the 'Seed' (Archetype) into new 'Soil' (Context) to grow a new 'Fruit'.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Any
import logging
from enum import Enum, auto

logger = logging.getLogger("Alchemy")

class TensionLevel(Enum):
    RELAXATION = auto()  # Low energy, stability
    BUILDUP = auto()     # Rising energy, conflict introduction
    CLIMAX = auto()      # Peak energy, breaking point
    RESOLUTION = auto()  # Falling energy, restructuring

@dataclass
class NarrativeEvent:
    """
    A single unit of 'Event' in the raw narrative.
    """
    content: str
    tension: TensionLevel
    # 'Next' is probabilistic in LLMs, but here we look for 'Why' (Causality)
    causal_link: Optional[str] = None # The 'Why' this happened

@dataclass
class CausalNode:
    """
    An abstract node in the Causal Web.
    It represents a 'Function' in the story, not a specific event.
    e.g., "Hubris leads to Negligence" rather than "The Hare took a nap".
    """
    function_name: str  # e.g. "Protagonist underestimates Antagonist"
    abstract_principle: str # e.g. "Overconfidence blinds competence"
    tension_change: str # e.g. "BUILDUP -> RELEXATION (False Stability)"

@dataclass
class Archetype:
    """
    The 'Seed' or 'DNA' extracted from a narrative.
    Contains the Essence (Theme) and the Skeleton (Structure).
    """
    name: str
    essence: str  # The core philosophical theme (The "Soul")
    structure: List[CausalNode] # The sequence of abstract functions (The "Bone")

    def describe(self) -> str:
        desc = f"Archetype: [{self.name}]\n"
        desc += f"  Essence: {self.essence}\n"
        desc += "  Structure:\n"
        for i, node in enumerate(self.structure):
            desc += f"    {i+1}. [{node.function_name}] -> {node.abstract_principle} ({node.tension_change})\n"
        return desc

class AlchemyOfCausality:
    """
    The Alchemist who performs the transmutation.
    """
    def __init__(self):
        # In a full implementation, this would connect to the LogosEngine to validate principles.
        # self.logos = get_logos_engine()
        self.known_archetypes: Dict[str, Archetype] = {}
        logger.info("⚗️ Alchemy of Causality Initialized")

    def extract_archetype(self, title: str, events: List[NarrativeEvent]) -> Archetype:
        """
        Phase 1 & 2: Observation & Purification.
        Extracts the abstract Causal Structure from concrete events.
        """
        logger.info(f"👁️ Observing Narrative: {title}")

        causal_chain: List[CausalNode] = []

        essence_candidates = []

        for event in events:
            # 1. Analyze Tension
            # 2. Abstract the Meaning
            node = self._abstract_event(event)
            causal_chain.append(node)
            essence_candidates.append(node.abstract_principle)

        # Synthesize Essence (The "Soul")
        # For simplicity, we take the last principle as the conclusion/moral,
        # and the first as the setup.
        essence = f"From {essence_candidates[0]} to {essence_candidates[-1]}"

        archetype = Archetype(
            name=f"Archetype of {title}",
            essence=essence,
            structure=causal_chain
        )

        self.known_archetypes[archetype.name] = archetype
        logger.info(f"✨ Archetype Extracted: {archetype.name}")
        return archetype

    def _abstract_event(self, event: NarrativeEvent) -> CausalNode:
        """
        The "Philosopher's Stone" logic.
        Converts "The Hare sleeps" -> "Competence becomes complacent".

        [NOTE] This method currently uses heuristic keyword matching tailored for the
        "Hare and Tortoise" POC. A production version would require:
        1. Semantic Role Labeling (Who does What to Whom)
        2. Theme Classification (Hubris, Persistence, etc.)
        3. Causal Inference (Why did this happen?)
        """
        content = event.content.lower()
        tension_str = event.tension.name

        # Priority 1: Outcome/Resolution (Overrides character actions)
        if "win" in content or "pass" in content or "triumph" in content:
             return CausalNode(
                "Triumph of the Persistent",
                "The Unexpected overturns the Expected",
                f"{tension_str} (Paradigm Shift)"
            )

        # Priority 2: Character Actions
        if "fast" in content or "strong" in content or "hare" in content:
            if "sleep" in content or "stop" in content:
                return CausalNode(
                    "Negligence of Power",
                    "Strength creates Arrogance",
                    f"{tension_str} (False Security)"
                )
            elif "start" in content or "race" in content:
                 return CausalNode(
                    "Establishment of Superiority",
                    "Natural Advantage exists",
                    f"{tension_str} (Initial State)"
                )
            elif "run" in content or "leave" in content:
                 return CausalNode(
                    "Demonstration of Power",
                    "Gap widens due to capability",
                    f"{tension_str} (Dominance)"
                 )

        if "slow" in content or "weak" in content or "tortoise" in content:
             if "keep" in content or "crawling" in content or "steady" in content:
                return CausalNode(
                    "Persistence of Weakness",
                    "Consistency overcomes Intensity",
                    f"{tension_str} (Hidden Accumulation)"
                )

        # Fallback for generic events
        return CausalNode(
            "Narrative Progression",
            f"Event develops: {event.content}",
            tension_str
        )

    def transmute(self, archetype: Archetype, new_context: str) -> List[str]:
        """
        Phase 3: Transmutation (Re-creation).
        Applies the 'DNA' to a new 'Body'.
        """
        logger.info(f"🔥 Transmuting [{archetype.name}] into context: [{new_context}]")

        new_story_events = []

        # Context Parsing (Simple Simulation)
        context_map = self._get_context_map(new_context)

        for node in archetype.structure:
            # Re-incarnate the abstract function into the new context's skin
            new_event_content = self._incarnate_node(node, context_map)
            new_story_events.append(f"[{node.tension_change}] {new_event_content}")

        return new_story_events

    def _get_context_map(self, context: str) -> Dict[str, str]:
        """
        Defines the "Vocabulary" of the new world.
        [NOTE] This simulates a World Knowledge Database.
        """
        context = context.lower()
        if "space" in context or "war" in context:
            return {
                "strong_entity": "The Galactic Empire's Dreadnought Fleet",
                "weak_entity": "The Rebel Alliance's Single Fighter",
                "action_rest": "halts sensors for routine maintenance, ignoring the blip",
                "action_steady": "moves in the shadow of the asteroid belt, undetected",
                "result_victory": "destroys the Core Generator while the Fleet is powered down",
                "action_demo": "vaporizes a nearby moon to show dominance"
            }
        elif "business" in context or "startup" in context:
             return {
                "strong_entity": "Global Tech Giant 'Giggle'",
                "weak_entity": "Garage Startup 'Ant'",
                "action_rest": "ignores the niche market, focusing on quarterly bonuses",
                "action_steady": "iterates product daily based on user feedback",
                "result_victory": "disrupts the market before the Giant can react",
                "action_demo": "releases a flashy but buggy beta to great fanfare"
            }
        else:
            return {
                "strong_entity": "The Strong One",
                "weak_entity": "The Weak One",
                "action_rest": "stops working",
                "action_steady": "keeps working",
                "result_victory": "wins",
                "action_demo": "shows off"
            }

    def _incarnate_node(self, node: CausalNode, context_map: Dict[str, str]) -> str:
        """
        Wraps the abstract bone with new flesh.
        """
        f = node.function_name

        if "Establishment of Superiority" in f:
            return f"{context_map['strong_entity']} displays overwhelming power."
        elif "Demonstration of Power" in f:
            return f"{context_map['strong_entity']} {context_map['action_demo']}."
        elif "Negligence of Power" in f:
            return f"{context_map['strong_entity']} {context_map['action_rest']} due to {node.abstract_principle}."
        elif "Persistence of Weakness" in f:
            return f"{context_map['weak_entity']} {context_map['action_steady']}, embodying {node.abstract_principle}."
        elif "Triumph" in f:
            return f"{context_map['weak_entity']} {context_map['result_victory']}."
        elif "Narrative Progression" in f:
            return f"The tension rises as {context_map['strong_entity']} and {context_map['weak_entity']} clash."
        else:
            return f"Event corresponding to '{f}' occurs."

# Singleton Access
_alchemy_instance: Optional[AlchemyOfCausality] = None

def get_alchemy_engine() -> AlchemyOfCausality:
    global _alchemy_instance
    if _alchemy_instance is None:
        _alchemy_instance = AlchemyOfCausality()
    return _alchemy_instance
