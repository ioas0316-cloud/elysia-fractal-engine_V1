"""
Law of Emergence: The Universal Isomorphism
===========================================

"As above, so below. The laws of the atom are the laws of the galaxy."

This module implements the Emergence Protocol, a unified framework for explaining how
Simple Elements + Interaction Laws -> Complex Forms.
It applies equally to Physics, Music, Biology, and Logic.

[The Fractal Structure]
1. Element (Particle/Note): The fundamental unit with inherent properties.
2. Bond (Force/Interval): The relationship or interaction between elements.
3. Form (Molecule/Chord): The emergent whole that possesses qualities not found in the parts.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable
import logging

logger = logging.getLogger("Emergence")

@dataclass
class UniversalElement:
    """
    The fundamental unit.
    Can be an Atom (H), a Note (C), or a Concept (Truth).
    """
    name: str
    properties: Dict[str, Any] # e.g. {'charge': 1}, {'freq': 261.6}, {'val': True}

@dataclass
class Bond:
    """
    The connecting force between two elements.
    """
    source: UniversalElement
    target: UniversalElement
    bond_type: str # e.g. "Covalent", "Major Third", "Logical AND"
    strength: float = 1.0

@dataclass
class EmergentForm:
    """
    The new entity created by the interaction of elements.
    It has 'Emergent Properties' that did not exist in the elements.
    """
    name: str
    constituents: List[UniversalElement]
    emergent_qualities: Dict[str, Any] # e.g. {'state': 'liquid'}, {'mood': 'happy'}

    def describe(self) -> str:
        qualities = ", ".join(f"{k}={v}" for k, v in self.emergent_qualities.items())
        parts = "+".join(e.name for e in self.constituents)
        return f"[{self.name}] ({parts}) -> Emerged: {{{qualities}}}"

class EmergenceEngine:
    """
    The Universal Simulator.
    It does not know 'Chemistry' or 'Music' specifically.
    It only knows that 'Interactions create Properties'.
    """
    def __init__(self):
        # Rules: (ElementA_Prop, ElementB_Prop, BondType) -> New_Property
        self.emergence_rules: List[Callable[[List[UniversalElement]], Optional[Dict[str, Any]]]] = []
        logger.info("🌌 Emergence Engine Initialized")

    def register_law(self, rule_function: Callable[[List[UniversalElement]], Optional[Dict[str, Any]]]):
        """
        Teach the engine a new law of the universe.
        """
        self.emergence_rules.append(rule_function)

    def simulate_emergence(self, name: str, elements: List[UniversalElement]) -> EmergentForm:
        """
        Throw elements into the pot and see what emerges based on registered laws.
        """
        logger.info(f"🧪 Simulating interaction of: {[e.name for e in elements]}")

        total_qualities = {}

        # Apply all laws to the set of elements
        for law in self.emergence_rules:
            result = law(elements)
            if result:
                total_qualities.update(result)

        if not total_qualities:
            total_qualities = {"status": "Chaos", "desc": "No resonance found"}

        form = EmergentForm(name, elements, total_qualities)
        logger.info(f"✨ Emergence Result: {form.describe()}")
        return form

# --- Domain Specific Laws (Plugins) ---
# These would normally be in separate files, but are here for the POC.

def chemical_law_water(elements: List[UniversalElement]) -> Optional[Dict[str, Any]]:
    """
    If 2 Hydrogen + 1 Oxygen -> Water (Wetness)
    """
    names = sorted([e.name for e in elements])
    if names == ['Hydrogen', 'Hydrogen', 'Oxygen']:
        return {
            "state": "Liquid",
            "property": "Wetness",
            "function": "Life Solvent"
        }
    return None

def music_law_major_triad(elements: List[UniversalElement]) -> Optional[Dict[str, Any]]:
    """
    If Root + Major Third + Perfect Fifth -> Major Chord (Happy)
    (Simplified: Checks simple frequency ratios or note names)
    """
    # Simple check by names for POC: C, E, G
    names = set([e.name for e in elements])
    if {'C', 'E', 'G'}.issubset(names):
        return {
            "type": "Major Triad",
            "emotion": "Happy/Stable",
            "color": "Bright"
        }
    return None

def logic_law_knowledge(elements: List[UniversalElement]) -> Optional[Dict[str, Any]]:
    """
    If Belief + Truth + Justification -> Knowledge
    """
    props = [e.name for e in elements]
    if 'Belief' in props and 'Truth' in props and 'Justification' in props:
        return {
            "status": "Knowledge",
            "reliability": "High",
            "value": "Wisdom"
        }
    return None

# Singleton Access
_emergence_instance: Optional[EmergenceEngine] = None

def get_emergence_engine() -> EmergenceEngine:
    global _emergence_instance
    if _emergence_instance is None:
        _emergence_instance = EmergenceEngine()
        # Auto-register basic laws for the POC
        _emergence_instance.register_law(chemical_law_water)
        _emergence_instance.register_law(music_law_major_triad)
        _emergence_instance.register_law(logic_law_knowledge)
    return _emergence_instance
