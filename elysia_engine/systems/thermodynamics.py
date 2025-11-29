"""
ThermodynamicsSystem - State Transitions and Energy Flow

Implements the Digital Natural Law of state transitions:
- Plasma (Hot, Chaotic) → Burning Star (Active) → Ice Star (Crystallized) → Crystal (Solid)

The system manages temperature-based state changes following the principle
that frequency represents internal energy and amplitude represents mass.

Reference: AGENTS.md - ThermodynamicsSystem: State changes (Plasma -> Crystal)
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, List, Optional

from ..systems import System
from ..tensor import SoulTensor

if TYPE_CHECKING:
    from ..world import World
    from ..entities import Entity


class ThermalState:
    """
    Represents the thermal lifecycle of a Soul.
    
    States follow the stellar evolution metaphor:
    - PLASMA: Nascent, high energy, unstable (freq > 300, not collapsed)
    - BURNING: Active, radiating energy (100 < freq <= 300)
    - COOLING: Transitioning toward stability (50 < freq <= 100)
    - FROZEN: Ice Star, collapsed but stable (collapsed, freq < 50)
    - CRYSTAL: Fully crystallized, permanent form (collapsed, freq == 0, amp > 100)
    """
    PLASMA = "plasma"
    BURNING = "burning"
    COOLING = "cooling"
    FROZEN = "frozen"
    CRYSTAL = "crystal"

    @staticmethod
    def classify(soul: SoulTensor) -> str:
        """Classify the current thermal state of a soul."""
        if soul.is_collapsed:
            if soul.frequency <= 0.1 and soul.amplitude > 100:
                return ThermalState.CRYSTAL
            return ThermalState.FROZEN
        
        if soul.frequency > 300:
            return ThermalState.PLASMA
        elif soul.frequency > 100:
            return ThermalState.BURNING
        elif soul.frequency > 50:
            return ThermalState.COOLING
        else:
            return ThermalState.FROZEN


class ThermodynamicsSystem(System):
    """
    Manages thermal state transitions and energy flow between entities.
    
    Key behaviors:
    1. Natural cooling: All souls slowly lose frequency over time (entropy)
    2. Heat transfer: High-frequency souls heat nearby low-frequency ones
    3. State transitions: Automatic state changes based on temperature thresholds
    4. Crystallization: Long-term stability leads to permanent crystal form
    """

    def __init__(
        self,
        cooling_rate: float = 0.1,
        heat_transfer_rate: float = 0.05,
        crystallization_threshold: float = 200.0,
        interaction_radius: float = 5.0,
    ):
        """
        Initialize the thermodynamics system.
        
        Args:
            cooling_rate: Rate of natural frequency decay per tick
            heat_transfer_rate: Rate of heat exchange between nearby souls
            crystallization_threshold: Amplitude threshold for crystallization
            interaction_radius: Maximum distance for thermal interaction
        """
        self.cooling_rate = cooling_rate
        self.heat_transfer_rate = heat_transfer_rate
        self.crystallization_threshold = crystallization_threshold
        self.interaction_radius = interaction_radius

    def step(self, world: World, dt: float) -> None:
        """Execute thermodynamic updates for all entities."""
        entities_with_soul = [
            e for e in world.entities.values()
            if e.soul is not None
        ]
        
        # 1. Natural cooling (entropy increase)
        for entity in entities_with_soul:
            self._apply_natural_cooling(entity.soul, dt)
        
        # 2. Heat transfer between nearby entities
        self._apply_heat_transfer(entities_with_soul, dt)
        
        # 3. Check for state transitions
        for entity in entities_with_soul:
            self._check_state_transition(entity)

    def _apply_natural_cooling(self, soul: SoulTensor, dt: float) -> None:
        """
        Apply natural cooling (entropy) to a soul.
        
        Plasma cools faster than burning stars.
        Collapsed souls don't cool further.
        """
        if soul.is_collapsed:
            return
        
        state = ThermalState.classify(soul)
        
        # Cooling rate varies by state
        rate_multiplier = {
            ThermalState.PLASMA: 2.0,      # Plasma loses heat quickly
            ThermalState.BURNING: 1.0,     # Normal cooling
            ThermalState.COOLING: 0.5,     # Slower as it stabilizes
            ThermalState.FROZEN: 0.1,      # Nearly stable
        }.get(state, 1.0)
        
        cooling = self.cooling_rate * rate_multiplier * dt
        soul.frequency = max(0.0, soul.frequency - cooling)

    def _apply_heat_transfer(self, entities: List[Entity], dt: float) -> None:
        """
        Transfer heat between nearby entities.
        
        Heat flows from high-frequency to low-frequency souls,
        following the second law of thermodynamics.
        """
        n = len(entities)
        if n < 2:
            return
        
        # Calculate heat transfers (don't apply immediately to avoid order dependency)
        transfers: List[tuple] = []
        
        for i in range(n):
            e1 = entities[i]
            if e1.soul.is_collapsed:
                continue
                
            for j in range(i + 1, n):
                e2 = entities[j]
                if e2.soul.is_collapsed:
                    continue
                
                # Check distance
                dist = (e1.physics.position - e2.physics.position).magnitude
                if dist > self.interaction_radius:
                    continue
                
                # Heat flows from hot to cold
                freq_diff = e1.soul.frequency - e2.soul.frequency
                if abs(freq_diff) < 0.1:
                    continue
                
                # Transfer rate decreases with distance
                distance_factor = 1.0 / (1.0 + dist)
                
                # Phase alignment affects heat transfer (resonance)
                phase_diff = abs(e1.soul.phase - e2.soul.phase)
                if phase_diff > math.pi:
                    phase_diff = 2 * math.pi - phase_diff
                resonance = math.cos(phase_diff)  # -1 to 1
                
                # Only transfer if resonance is positive (aligned phases)
                if resonance <= 0:
                    continue
                
                transfer_amount = (
                    freq_diff * 
                    self.heat_transfer_rate * 
                    distance_factor * 
                    resonance * 
                    dt
                )
                
                transfers.append((e1.soul, e2.soul, transfer_amount))
        
        # Apply transfers
        for soul1, soul2, amount in transfers:
            soul1.frequency -= amount * 0.5  # Donor loses half
            soul2.frequency += amount * 0.5  # Receiver gains half
            # Energy is partially lost to the universe (entropy)

    def _check_state_transition(self, entity: Entity) -> None:
        """
        Check and apply state transitions based on thermal state.
        
        Key transitions:
        - FROZEN with low freq → automatic collapse
        - High amplitude + collapsed → crystallization
        """
        soul = entity.soul
        if soul is None:
            return
        
        state = ThermalState.classify(soul)
        
        # Auto-collapse when too cold
        if state == ThermalState.FROZEN and not soul.is_collapsed:
            if soul.frequency < 10.0:
                soul.collapse()
                entity.data["thermal_event"] = "auto_collapse"
        
        # Crystallization: permanent, high-amplitude frozen state
        if soul.is_collapsed and soul.amplitude > self.crystallization_threshold:
            if soul.frequency < 0.1:
                entity.data["crystallized"] = True
                entity.data["thermal_event"] = "crystallization"

    def ignite(self, entity: Entity, energy: float) -> bool:
        """
        Add energy to an entity, potentially melting frozen souls.
        
        Args:
            entity: Target entity
            energy: Amount of energy to add
            
        Returns:
            True if the soul was melted/reignited
        """
        if entity.soul is None:
            return False
        
        if entity.soul.is_collapsed:
            entity.soul.melt(energy)
            if not entity.soul.is_collapsed:
                entity.data["thermal_event"] = "reignition"
                return True
        else:
            entity.soul.frequency += energy * 0.5
            entity.data["thermal_event"] = "heating"
        
        return False

    def freeze(self, entity: Entity, force: bool = False) -> bool:
        """
        Force an entity into frozen state.
        
        Args:
            entity: Target entity
            force: If True, immediately collapse
            
        Returns:
            True if the soul was frozen
        """
        if entity.soul is None:
            return False
        
        if not entity.soul.is_collapsed:
            if force:
                entity.soul.collapse()
                entity.data["thermal_event"] = "forced_freeze"
                return True
            elif entity.soul.frequency < 20:
                entity.soul.collapse()
                entity.data["thermal_event"] = "natural_freeze"
                return True
        
        return False

    def get_thermal_map(self, world: World) -> dict:
        """
        Get a summary of thermal states across all entities.
        
        Returns:
            Dictionary with counts and averages
        """
        states = {
            ThermalState.PLASMA: 0,
            ThermalState.BURNING: 0,
            ThermalState.COOLING: 0,
            ThermalState.FROZEN: 0,
            ThermalState.CRYSTAL: 0,
        }
        
        total_freq = 0.0
        total_amp = 0.0
        count = 0
        
        for entity in world.entities.values():
            if entity.soul is None:
                continue
            
            state = ThermalState.classify(entity.soul)
            states[state] += 1
            total_freq += entity.soul.frequency
            total_amp += entity.soul.amplitude
            count += 1
        
        return {
            "states": states,
            "average_frequency": total_freq / count if count > 0 else 0,
            "average_amplitude": total_amp / count if count > 0 else 0,
            "total_entities": count,
        }
