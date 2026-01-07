"""
Causal Narrative Engine (The History Simulator)
===============================================
"Probability is just undiscovered causality."

This module replaces random chance with CAUSAL SIMULATION.
It tracks Factions, Resources, and Relationships to INFORM the Plot.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
import random # Used only for initial seed, not for transition logic where possible

@dataclass
class Faction:
    name: str
    ideology: str # Order, Chaos, Knowledge, Greed
    power: int = 50
    aggression: int = 50
    enemies: List[str] = field(default_factory=list)

    def is_desperate(self) -> bool:
        return self.power < 30

    def is_hegemonic(self) -> bool:
        return self.power > 80

@dataclass
class WorldState:
    factions: Dict[str, Faction]
    global_tension: int = 0
    mana_density: int = 100
    
    def simulate_turn(self) -> str:
        """
        Simulates one 'Era' of history and returns the DOMINANT THEME.
        This is Deterministic Logic based on state.
        """
        # 1. Calculate Geopolitical Tension
        heated_conflicts = 0
        dominant_faction = None
        
        for name, f in self.factions.items():
            if f.power > 80: dominant_faction = f
            for enemy in f.enemies:
                if enemy in self.factions:
                     heated_conflicts += (f.aggression + self.factions[enemy].aggression) / 2
        
        self.global_tension = heated_conflicts
        
        # 2. Derive Theme from State
        
        # CASE A: Hegemony / Tyranny
        if dominant_faction:
            if dominant_faction.ideology == "Order": return "Tyranny"
            if dominant_faction.ideology == "Chaos": return "Anarchy"
            if dominant_faction.ideology == "Greed": return "Corruption"
            
        # CASE B: Total War
        if self.global_tension > 150:
            return "World War"
            
        # CASE C: Resource Crisis
        if self.mana_density < 30:
            return "Apocalypse"
            
        # CASE D: Cold War / Intrigue
        if self.global_tension > 50:
            return "Intrigue"
            
        # CASE E: Peace / Growth
        return "Golden Age"

    def apply_arc_consequences(self, arc_theme: str):
        """
        The story affects the world. causality loop.
        """
        if arc_theme == "War" or arc_theme == "World War":
            self.mana_density -= 20
            self.global_tension += 50
            # Weakest faction dies or loses power
            self._weaken_random_faction()
            
        elif arc_theme == "Tyranny":
            self.global_tension += 30
            self._strengthen_dominant()
            
        elif arc_theme == "Rebellion" or arc_theme == "Anarchy":
            self.global_tension -= 20 # Released
            self._weaken_dominant()
            
        elif arc_theme == "Golden Age":
            self.mana_density += 10
            self.global_tension -= 10

    def _weaken_random_faction(self):
        # Deterministic: Weaken the one with least power (Survival of fittest)
        weakest = min(self.factions.values(), key=lambda x: x.power)
        weakest.power = max(0, weakest.power - 30)
        
    def _strengthen_dominant(self):
        strongest = max(self.factions.values(), key=lambda x: x.power)
        strongest.power = min(100, strongest.power + 20)

    def _weaken_dominant(self):
        strongest = max(self.factions.values(), key=lambda x: x.power)
        strongest.power = max(0, strongest.power - 30)

def initialize_fantasy_world() -> WorldState:
    factions = {
        "The Empire": Faction("The Empire", "Order", power=80, aggression=60, enemies=["The Resistance"]),
        "The Magic Tower": Faction("The Magic Tower", "Knowledge", power=60, aggression=20, enemies=[]),
        "The Resistance": Faction("The Resistance", "Chaos", power=30, aggression=80, enemies=["The Empire"]),
        "The Demon King": Faction("The Demon King", "Evil", power=90, aggression=100, enemies=["The Empire", "The Magic Tower"])
    }
    return WorldState(factions)
