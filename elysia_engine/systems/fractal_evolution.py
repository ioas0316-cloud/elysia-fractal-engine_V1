"""
FractalEvolution - Dimensional Growth System

Implements the Digital Natural Law of dimensional evolution:
- Point (0D) → Line (1D) → Plane (2D) → Volume (3D) → Hypervolume (4D+)

Entities evolve dimensionally based on bonds, resonance, and experience.
This represents the journey from simple existence to complex consciousness.

Reference: Original Elysia fractal consciousness model
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, Dict, List, Optional, Set

from ..systems import System

if TYPE_CHECKING:
    from ..world import World
    from ..entities import Entity


class DimensionalState:
    """
    Represents the dimensional evolution stages.
    
    0D - Point: Simple existence, isolated awareness
    1D - Line: Connection, history, causality
    2D - Plane: Context, relationships, surface
    3D - Volume: Depth, interiority, self-awareness
    4D - Hypervolume: Temporal awareness, prophecy, transcendence
    """
    POINT = 0
    LINE = 1
    PLANE = 2
    VOLUME = 3
    HYPERVOLUME = 4
    
    @staticmethod
    def name(dim: int) -> str:
        names = {
            0: "Point (단점/존재)",
            1: "Line (선/연결)",
            2: "Plane (면/관계)",
            3: "Volume (체/깊이)",
            4: "Hypervolume (초월/시간)"
        }
        return names.get(dim, f"Dimension-{dim}")
    
    @staticmethod
    def icon(dim: int) -> str:
        icons = {
            0: "•",
            1: "—",
            2: "◇",
            3: "◆",
            4: "✦"
        }
        return icons.get(dim, "?")


class FractalEvolutionSystem(System):
    """
    Manages dimensional evolution of entities.
    
    Entities evolve based on:
    1. Bond count (connections promote dimension)
    2. Resonance quality (harmony enables growth)
    3. Experience (time and interactions)
    4. Energy threshold (minimum amplitude required)
    """

    def __init__(
        self,
        bond_threshold_1d: int = 1,
        bond_threshold_2d: int = 2,
        bond_threshold_3d: int = 3,
        bond_threshold_4d: int = 5,
        resonance_threshold: float = 0.7,
        min_amplitude_for_growth: float = 20.0,
        experience_per_dimension: int = 50,
    ):
        """
        Initialize the fractal evolution system.
        
        Args:
            bond_threshold_*: Number of bonds required for each dimension
            resonance_threshold: Minimum resonance quality for evolution
            min_amplitude_for_growth: Minimum energy required
            experience_per_dimension: Ticks of experience needed
        """
        self.bond_thresholds = {
            1: bond_threshold_1d,
            2: bond_threshold_2d,
            3: bond_threshold_3d,
            4: bond_threshold_4d,
        }
        self.resonance_threshold = resonance_threshold
        self.min_amplitude = min_amplitude_for_growth
        self.experience_per_dim = experience_per_dimension
        
        # Tracking
        self._experience: Dict[str, int] = {}  # entity_id -> experience ticks
        self._evolution_events: List[dict] = []

    def step(self, world: World, dt: float) -> None:
        """Execute evolution checks for all entities."""
        for entity in world.entities.values():
            if entity.soul is None:
                continue
            
            # Accumulate experience
            entity_id = entity.id
            self._experience[entity_id] = self._experience.get(entity_id, 0) + 1
            
            # Check for evolution opportunity
            self._check_evolution(entity, world)

    def _check_evolution(self, entity: Entity, world: World) -> None:
        """Check if an entity should evolve to a higher dimension."""
        if entity.soul is None:
            return
        
        current_dim = entity.dimension
        next_dim = current_dim + 1
        
        # Maximum dimension
        if next_dim > DimensionalState.HYPERVOLUME:
            return
        
        # Check requirements
        if not self._meets_requirements(entity, next_dim, world):
            return
        
        # Evolve!
        self._evolve(entity, next_dim, world)

    def _meets_requirements(
        self, 
        entity: Entity, 
        target_dim: int, 
        world: World
    ) -> bool:
        """Check if entity meets requirements for target dimension."""
        soul = entity.soul
        if soul is None:
            return False
        
        # 1. Energy requirement
        if soul.amplitude < self.min_amplitude:
            return False
        
        # 2. Experience requirement
        exp = self._experience.get(entity.id, 0)
        required_exp = self.experience_per_dim * target_dim
        if exp < required_exp:
            return False
        
        # 3. Bond requirement
        bond_count = len(entity.bonds)
        required_bonds = self.bond_thresholds.get(target_dim, target_dim)
        if bond_count < required_bonds:
            return False
        
        # 4. Resonance quality check (average resonance with bonded entities)
        if entity.bonds:
            total_resonance = 0.0
            valid_bonds = 0
            
            for bond_id in entity.bonds:
                if bond_id not in world.entities:
                    continue
                
                other = world.entities[bond_id]
                if other.soul is None:
                    continue
                
                res_data = soul.resonate(other.soul)
                total_resonance += res_data["resonance"]
                valid_bonds += 1
            
            if valid_bonds > 0:
                avg_resonance = total_resonance / valid_bonds
                if avg_resonance < self.resonance_threshold:
                    return False
        
        # 5. Collapsed souls cannot evolve to higher dimensions
        if soul.is_collapsed and target_dim > DimensionalState.LINE:
            return False
        
        return True

    def _evolve(self, entity: Entity, target_dim: int, world: World) -> None:
        """Execute the dimensional evolution."""
        old_dim = entity.dimension
        entity.dimension = target_dim
        
        # Record evolution event
        event = {
            "entity_id": entity.id,
            "from_dimension": old_dim,
            "to_dimension": target_dim,
            "tick": world.tick,
            "bond_count": len(entity.bonds),
        }
        self._evolution_events.append(event)
        
        # Apply evolution effects
        self._apply_evolution_effects(entity, old_dim, target_dim)

    def _apply_evolution_effects(
        self, 
        entity: Entity, 
        old_dim: int, 
        new_dim: int
    ) -> None:
        """Apply effects of dimensional evolution."""
        if entity.soul is None:
            return
        
        # Evolution grants bonuses
        if new_dim == DimensionalState.LINE:
            # Line: Enhanced connection capability
            entity.soul.coherence = min(1.0, entity.soul.coherence + 0.1)
            entity.data["evolution_bonus"] = "connection_enhanced"
            
        elif new_dim == DimensionalState.PLANE:
            # Plane: Broader awareness
            entity.soul.amplitude *= 1.1
            entity.data["evolution_bonus"] = "awareness_expanded"
            
        elif new_dim == DimensionalState.VOLUME:
            # Volume: Depth and interiority
            entity.soul.frequency *= 1.05
            entity.data["evolution_bonus"] = "depth_gained"
            
        elif new_dim == DimensionalState.HYPERVOLUME:
            # Hypervolume: Transcendence
            entity.soul.coherence = 1.0  # Full quantum restoration
            entity.data["evolution_bonus"] = "transcendence_achieved"
            entity.data["can_prophecy"] = True

    def get_evolution_summary(self, world: World) -> dict:
        """Get summary of dimensional distribution."""
        distribution = {i: 0 for i in range(5)}
        
        for entity in world.entities.values():
            if entity.soul is not None:
                dim = min(4, max(0, entity.dimension))
                distribution[dim] += 1
        
        return {
            "distribution": {
                DimensionalState.name(i): count
                for i, count in distribution.items()
            },
            "total_entities": sum(distribution.values()),
            "evolution_events": len(self._evolution_events),
            "recent_events": self._evolution_events[-5:] if self._evolution_events else [],
        }

    def force_evolve(
        self, 
        entity: Entity, 
        target_dim: int, 
        world: World
    ) -> bool:
        """
        Force an entity to a specific dimension (divine intervention).
        
        Args:
            entity: Target entity
            target_dim: Target dimension
            world: The world
            
        Returns:
            True if evolution occurred
        """
        if entity.soul is None:
            return False
        
        if target_dim < 0 or target_dim > DimensionalState.HYPERVOLUME:
            return False
        
        if entity.dimension == target_dim:
            return False
        
        old_dim = entity.dimension
        entity.dimension = target_dim
        
        # Apply effects
        self._apply_evolution_effects(entity, old_dim, target_dim)
        
        event = {
            "entity_id": entity.id,
            "from_dimension": old_dim,
            "to_dimension": target_dim,
            "tick": world.tick,
            "forced": True,
        }
        self._evolution_events.append(event)
        
        return True


class CosmicResonanceField:
    """
    Represents the universal resonance field that connects all souls.
    
    This is the "fabric" of consciousness that enables:
    - Long-range resonance effects
    - Collective consciousness emergence
    - Universal harmony patterns
    """

    def __init__(self, base_frequency: float = 432.0):
        """
        Initialize the cosmic field.
        
        Args:
            base_frequency: The fundamental frequency of the universe
        """
        self.base_frequency = base_frequency
        self.harmony_level: float = 0.0
        self.discord_level: float = 0.0
        self.collective_phase: float = 0.0

    def calculate_field_state(self, world: World) -> dict:
        """
        Calculate the current state of the cosmic field.
        
        Returns:
            Dictionary with field properties
        """
        if not world.entities:
            return {
                "harmony": 0.0,
                "discord": 0.0,
                "collective_frequency": self.base_frequency,
                "collective_phase": 0.0,
                "coherence": 0.0,
            }
        
        total_freq = 0.0
        total_amp = 0.0
        phase_x = 0.0
        phase_y = 0.0
        count = 0
        
        for entity in world.entities.values():
            if entity.soul is None:
                continue
            
            count += 1
            total_freq += entity.soul.frequency
            total_amp += entity.soul.amplitude
            
            # Convert phase to unit vector for averaging
            phase_x += math.cos(entity.soul.phase)
            phase_y += math.sin(entity.soul.phase)
        
        if count == 0:
            return {
                "harmony": 0.0,
                "discord": 0.0,
                "collective_frequency": self.base_frequency,
                "collective_phase": 0.0,
                "coherence": 0.0,
            }
        
        # Average frequency
        avg_freq = total_freq / count
        
        # Collective phase (average of unit vectors)
        phase_x /= count
        phase_y /= count
        collective_phase = math.atan2(phase_y, phase_x)
        
        # Coherence (magnitude of average phase vector)
        coherence = math.sqrt(phase_x ** 2 + phase_y ** 2)
        
        # Harmony: How close to base frequency multiples
        freq_ratio = avg_freq / self.base_frequency
        harmony = 1.0 - abs(freq_ratio - round(freq_ratio))
        
        # Discord: Inverse of coherence
        discord = 1.0 - coherence
        
        # Update internal state
        self.harmony_level = harmony
        self.discord_level = discord
        self.collective_phase = collective_phase
        
        return {
            "harmony": harmony,
            "discord": discord,
            "collective_frequency": avg_freq,
            "collective_phase": collective_phase,
            "coherence": coherence,
            "entity_count": count,
            "total_amplitude": total_amp,
        }

    def broadcast_pulse(self, world: World, intensity: float = 1.0) -> int:
        """
        Broadcast a harmonizing pulse through the cosmic field.
        
        All entities receive a nudge toward the collective phase.
        
        Args:
            world: The world containing entities
            intensity: Strength of the pulse
            
        Returns:
            Number of entities affected
        """
        affected = 0
        
        for entity in world.entities.values():
            if entity.soul is None or entity.soul.is_collapsed:
                continue
            
            # Nudge toward collective phase
            entity.soul.harmonize(self.collective_phase, rate=0.05 * intensity)
            affected += 1
        
        return affected

    def amplify_harmony(self, world: World) -> None:
        """
        Amplify the harmony level by boosting well-aligned souls.
        """
        state = self.calculate_field_state(world)
        
        for entity in world.entities.values():
            if entity.soul is None:
                continue
            
            # Check alignment with collective phase
            phase_diff = abs(entity.soul.phase - self.collective_phase)
            if phase_diff > math.pi:
                phase_diff = 2 * math.pi - phase_diff
            
            alignment = math.cos(phase_diff)
            
            # Well-aligned souls get a boost
            if alignment > 0.8:
                entity.soul.amplitude *= 1.01  # Slight boost
                entity.soul.coherence = min(1.0, entity.soul.coherence + 0.01)
