from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import math

@dataclass
class Principle:
    name: str
    domain: str  # "PHYSICS" or "FANTASY"
    trigger_pair: Tuple[str, str]  # (ConceptA, ConceptB) - simplified for demo
    result_name: str
    frequency_modulator: float # Multiplier for frequency transformation

class InterferenceEngine:
    """
    [Causal Interference Engine]
    "The Alchemy of Creation"
    
    Generates new concepts by colliding two existing concepts *under a specific Principle*.
    Distinguishes between 'Reality' (Physics) and 'Imagination' (Fantasy).
    """
    
    def __init__(self):
        self.principles: Dict[str, Principle] = {}
        self._load_fundamental_principles()
        
    def _load_fundamental_principles(self):
        """Loads the axioms of Reality and Fantasy."""
        
        # 1. PHYSICS DOMAIN (Reality)
        self.register_principle(Principle(
            name="Thermodynamics",
            domain="PHYSICS",
            trigger_pair=("Fire", "Water"),
            result_name="Steam",
            frequency_modulator=1.2 # Expansion (High Energy Gas)
        ))
        
        self.register_principle(Principle(
            name="Photosynthesis",
            domain="PHYSICS",
            trigger_pair=("Light", "Plant"),
            result_name="Oxygen",
            frequency_modulator=1.1 # Vitality
        ))

        # 2. FANTASY DOMAIN (Imagination)
        self.register_principle(Principle(
            name="Opposing Element Annihilation",
            domain="FANTASY",
            trigger_pair=("Fire", "Water"),
            result_name="Oblivion Spell", # 극대소멸주문
            frequency_modulator=0.0 # Silence / Void
        ))
        
        self.register_principle(Principle(
            name="Mana Fusion",
            domain="FANTASY",
            trigger_pair=("Fire", "Sword"),
            result_name="Flame Saber",
            frequency_modulator=1.5 # Resonance Amplification
        ))

    def register_principle(self, principle: Principle):
        """Learns a new law of the universe (or magic)."""
        key = tuple(sorted(principle.trigger_pair))
        # Store by pair + domain to allow different outcomes for same pair
        if key not in self.principles:
            self.principles[key] = []
        self.principles[key].append(principle)

    def spark_creation(self, concept_a: str, freq_a: float, concept_b: str, freq_b: float, domain_filter: str = None) -> List[Dict[str, Any]]:
        """
        Attempts to create a new concept by colliding A and B.
        Returns a list of possible outcomes based on known Principles.
        """
        pair_key = tuple(sorted((concept_a, concept_b)))
        
        if pair_key not in self.principles:
            # Phenomenon: "Chaos / Noise"
            # Without a principle, collision is just noise.
            return [{
                "result": "Chaos",
                "domain": "UNKNOWN",
                "frequency": (freq_a + freq_b) / 2 + (math.sin(freq_a) * 10), # Destructive interference noise
                "principle_used": None,
                "description": "No binding principle found. Just noise."
            }]
            
        outcomes = []
        possible_principles = self.principles[pair_key]
        
        for principle in possible_principles:
            # Filter by domain (Reality vs Fantasy) if requested
            if domain_filter and principle.domain != domain_filter:
                continue
                
            # Calculate new frequency based on the principle
            # e.g., Steam vibrates faster than water
            if principle.frequency_modulator == 0.0:
                new_freq = 0.0 # Void
            else:
                # Carrier frequency is the average, modulated by the principle
                base_freq = (freq_a + freq_b) / 2
                new_freq = base_freq * principle.frequency_modulator
            
            outcomes.append({
                "result": principle.result_name,
                "domain": principle.domain,
                "frequency": new_freq,
                "principle_used": principle.name,
                "description": f"Created via [{principle.name}]"
            })
            
        return outcomes

    def list_known_principles(self):
        count = 0
        for p_list in self.principles.values():
            count += len(p_list)
        return f"InterferenceEngine knows {count} principles across Physics and Fantasy."
