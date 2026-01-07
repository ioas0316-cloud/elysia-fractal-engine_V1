"""
Memetic Legacy & Akashic Field 🧬🌌

"The soul is not a record, but a resonance passed through time."

This module implements the inheritance of Technique, Reason, and Meaning (Spiritual DNA)
and the 'Akashic Field' where deceased masters linger as resonant echoes.
"""

import time
import uuid
import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any

@dataclass
class SpiritualDNA:
    technique: float = 0.5
    reason: float = 0.5
    meaning: float = 0.5
    moral_valence: float = 0.5 # 1.0 = Saintly/Warm, 0.0 = Vicious/Cold
    archetype_path: str = "Commoner"
    
    # Phase 12: Potency & Realization
    # Potency: Growth capacity (The Seed's potential)
    potency: Dict[str, float] = field(default_factory=lambda: {"tech": 0.5, "res": 0.5, "mean": 0.5})
    # Realization: 0.0 (Flat/Taught) to 1.0 (Deep/Experienced)
    realization: Dict[str, float] = field(default_factory=lambda: {"tech": 0.2, "res": 0.2, "mean": 0.2})

    def blend(self, other: 'SpiritualDNA', ratio: float = 0.5, counter: bool = False) -> 'SpiritualDNA':
        """Blends DNA. Mastery teaching results in 'Flat' realization."""
        m = -1.0 if counter else 1.0
        
        # Realization increases slowly during teaching, capped at 0.6 (The Ceiling)
        new_real = {k: min(0.6, self.realization[k] + 0.05) for k in self.realization}
        
        return SpiritualDNA(
            technique=max(0.0, min(1.0, self.technique + (other.technique - self.technique) * ratio * m)),
            reason=max(0.0, min(1.0, self.reason + (other.reason - self.reason) * ratio * m)),
            meaning=max(0.0, min(1.0, self.meaning + (other.meaning - self.meaning) * ratio * m)),
            moral_valence=max(0.0, min(1.0, self.moral_valence + (other.moral_valence - self.moral_valence) * ratio * m)),
            archetype_path=self.archetype_path,
            potency=self.potency,
            realization=new_real
        )

@dataclass
class AkashicEcho:
    id: str
    original_name: str
    dna: SpiritualDNA
    resonance_coord: Tuple[float, float, float, float] # 4D semantic location
    timestamp: float = field(default_factory=time.time)

class AkashicField:
    """A persistent graveyard of spirits that guides the living."""
    
    def __init__(self):
        self.echoes: Dict[str, AkashicEcho] = {}
        self.logger = logging.getLogger("AkashicField")

    def record_legacy(self, ego_name: str, dna: SpiritualDNA, coord: Tuple[float, float, float, float]):
        echo_id = str(uuid.uuid4())
        self.echoes[echo_id] = AkashicEcho(echo_id, ego_name, dna, coord)
        self.logger.info(f"✨ Akashic Echo Born: {ego_name}'s spirit now resonates in the field.")

    def find_nearest_echo(self, coord: Tuple[float, float, float, float], radius: float = 5.0) -> Optional[AkashicEcho]:
        """Finds a master's echo for a seeker to resonate with."""
        for echo in self.echoes.values():
            dist = sum((a-b)**2 for a, b in zip(coord, echo.resonance_coord))**0.5
            if dist < radius:
                return echo
        return None

class PositionInductor:
    """Induces different 'Normalcy Gravities' based on family position or role."""
    
    def __init__(self):
        self.roles = {
            "FirstBorn": {"env_gravity": 0.8, "desire_mod": 1.2, "intent": "Uphold Authority"},
            "MiddleBorn": {"env_gravity": 0.5, "desire_mod": 1.0, "intent": "Calculated Survival"},
            "LastBorn": {"env_gravity": 0.2, "desire_mod": 1.5, "intent": "Independence/Play"},
            "Outcast": {"env_gravity": 0.1, "desire_mod": 2.0, "intent": "Rebellion"}
        }

    def get_role_params(self, role: str) -> Dict[str, Any]:
        return self.roles.get(role, {"env_gravity": 0.3, "desire_mod": 1.0, "intent": "Exist"})

class RegionalField:
    """Defines the 'Atmospheric Ethos' of a region."""
    
    def __init__(self, name: str, dominant_archetype: str, ethos_dna: SpiritualDNA):
        self.name = name
        self.dominant_archetype = dominant_archetype
        self.ethos_dna = ethos_dna
        self.stigma_threshold = 0.4 # Difference in DNA that triggers social stigma

    def calculate_friction(self, ego_archetype: str, ego_dna: SpiritualDNA) -> float:
        """Calculates 'Inductive Friction' based on regional ethos."""
        friction = 0.0
        # 1. Archetype Friction (e.g., Mage in a Warrior region)
        if ego_archetype != self.dominant_archetype:
            friction += 0.5
            
        # 2. Moral/DNA Friction (Acting against local 'Common Sense')
        dna_diff = abs(ego_dna.moral_valence - self.ethos_dna.moral_valence)
        if dna_diff > self.stigma_threshold:
            friction += dna_diff * 0.5
            
        return friction

class LifeFieldInductor:
    """Calculates Narrative Pressure and induces life path changes."""
    
    def __init__(self):
        self.base_env_gravity = 0.3 # Average stability of a village
        self.seed_threshold = 2 # Depth below which a soul is a 'fragile seed'
        
    def calculate_pressure(self, ego_depth: int, satisfaction: float, desire: float, 
                           env_gravity: Optional[float] = None, regional_friction: float = 0.0,
                           kismet: float = 0.5) -> float:
        """
        Pressure = (Depth * Desire * (1 + Friction)) / (Satisfaction * Env_Gravity * Kismet)
        """
        gravity = env_gravity if env_gravity is not None else self.base_env_gravity
        
        # Kismet (Luck/Timing) is now a powerful dampener
        # 0.1 kismet -> 0.2 factor (Severe pressure)
        # 0.9 kismet -> 5.0 factor (Protected)
        k_factor = 0.1 + (kismet ** 2 * 10.0) 
        
        # Friction increases narrative pressure (Unrest/Abnormality)
        pressure = (ego_depth * desire * (1.0 + regional_friction)) / (max(0.1, satisfaction) * gravity * 20.0 * k_factor)
        
        # Seed Vulnerability: High pressure on a young soul (Seed Phase) causes 'Breakage'
        if ego_depth <= self.seed_threshold and pressure > 2.5:
            return pressure * 2.0 
            
        return min(5.0, pressure)

    def calculate_catalytic_growth(self, pressure: float, potency: float, current_stability: float) -> Tuple[float, float]:
        """
        Converts pressure into intensity/growth if potency allows.
        Returns: (Intensity_Gain, Stability_Loss)
        """
        if pressure < 0.5:
            return 0.0, -0.01 # Small stability recovery when peaceful
            
        # Growth is proportional to (Pressure * Potency)
        growth = (pressure) * potency * 0.15
        
        # Strain is heavily mitigated by potency
        strain = (pressure / max(0.1, potency ** 2)) * 0.02
        
        return growth, strain

    def induce_path(self, current_pressure: float, depth: int) -> str:
        # Seeds don't become adventurers easily; they just 'break'
        threshold = 2.0 if depth > self.seed_threshold else 4.0
        
        if current_pressure > threshold:
            return "Adventurer"
        elif current_pressure < 0.4:
            return "Citizen"
        else:
            return "Seeker"
