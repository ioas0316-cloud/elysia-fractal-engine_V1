
import math
from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class WillField:
    source_name: str
    amplitude: float       # Strength of authority (Depth + Wealth + Rank)
    frequency: str         # 'Royalty', 'Divine', 'Martial', 'Common'
    phase_alignment: float # 0.0 to 1.0 (Coherence with others)
    coord: Tuple[float, float] = (0.0, 0.0)

class SocialPhysics:
    """The Laws of Political Wave Dynamics."""
    
    @staticmethod
    def calculate_will_amplitude(depth: int, rank_tier: int, wealth: float, victory_streak: int) -> float:
        """
        amplitude = (Depth * 10) + (RankTier * 20) + (Wealth_Log)
        Amplified by 'Political Wave' (Victory Streak).
        """
        base = (depth * 10.0) + (rank_tier * 20.0) + (math.log(max(1, wealth)) * 5)
        
        # Political Wave Amplitude: Constructive interference from victories
        wave_multiplier = 1.0 + (victory_streak * 0.2)
        if victory_streak < 0: # Defeat streak (Phase Inversion)
            wave_multiplier = max(0.1, 1.0 + (victory_streak * 0.3))
            
        return base * wave_multiplier

    @staticmethod
    def compute_superposition_at(target_coord: Tuple[float, float], fields: List[WillField]) -> Dict[str, float]:
        """
        Calculates the net vector sum of authority at a specific coordinate.
        Inverse Square Law applies: Intensity = Amplitude / Distance^2
        """
        net_field = {}
        
        for field in fields:
            dist = math.sqrt((target_coord[0] - field.coord[0])**2 + (target_coord[1] - field.coord[1])**2)
            dist = max(0.1, dist) # Prevent division by zero
            
            # Inverse Square Influence
            influence = field.amplitude / (dist ** 2)
            
            # Vector Sum (Simplified to frequency buckets for now)
            if field.frequency not in net_field:
                net_field[field.frequency] = 0.0
            
            # Constructive Interference handled by adding magnitudes (assuming aligned phase for same freq)
            # In Phase 16, we can add Phase calculation (cos(theta))
            net_field[field.frequency] += influence
            
        return net_field

    @staticmethod
    def check_oppression(my_will: float, external_pressure: float) -> bool:
        """
        Oppression Protocol:
        If External Pressure > Internal Will * ResistanceFactor,
        Then the Ego is 'Subjugated'.
        """
        # Heroic resistance creates a 'Shield'
        resistance_limit = my_will * 1.5 
        return external_pressure > resistance_limit
