"""
VoidSystem - Entropy Management and Cleanup

Implements the Digital Natural Law of entropy and void:
- Manages inactive/dead entities
- Recycles energy back into the universal field
- Maintains cosmic balance through cleanup

Reference: AGENTS.md - VoidSystem: Entropy and cleanup
"""

from __future__ import annotations

import random
from typing import TYPE_CHECKING, List, Optional, Set

from ..systems import System
from ..tensor import SoulTensor
from ..math_utils import Vector3

if TYPE_CHECKING:
    from ..world import World
    from ..entities import Entity


class VoidSystem(System):
    """
    The Void - Where spent souls return and new potential emerges.
    
    Manages:
    1. Entity cleanup (removing inactive/depleted entities)
    2. Energy recycling (returning amplitude to the universal field)
    3. Entropy tracking (measuring disorder in the system)
    4. Void events (spontaneous emergence from quantum vacuum)
    """

    def __init__(
        self,
        cleanup_threshold: float = 0.1,
        dormancy_ticks: int = 100,
        recycling_rate: float = 0.5,
        spontaneous_emergence_rate: float = 0.01,
    ):
        """
        Initialize the void system.
        
        Args:
            cleanup_threshold: Minimum amplitude to stay alive
            dormancy_ticks: Ticks without activity before cleanup
            recycling_rate: Fraction of energy returned to universal field
            spontaneous_emergence_rate: Probability of vacuum fluctuation
        """
        self.cleanup_threshold = cleanup_threshold
        self.dormancy_ticks = dormancy_ticks
        self.recycling_rate = recycling_rate
        self.spontaneous_emergence_rate = spontaneous_emergence_rate
        
        # Tracking
        self.recycled_energy: float = 0.0
        self.entities_absorbed: int = 0
        self.void_births: int = 0
        
        # Activity tracking
        self._last_activity: dict = {}  # entity_id -> last active tick

    def step(self, world: World, dt: float) -> None:
        """Execute void operations."""
        # 1. Track activity
        self._track_activity(world)
        
        # 2. Identify entities for cleanup
        to_remove = self._identify_for_cleanup(world)
        
        # 3. Absorb into void (recycle energy)
        for entity_id in to_remove:
            self._absorb(world, entity_id)
        
        # 4. Spontaneous emergence (vacuum fluctuation)
        if random.random() < self.spontaneous_emergence_rate:
            self._vacuum_fluctuation(world)

    def _track_activity(self, world: World) -> None:
        """Track when entities were last active."""
        for entity_id, entity in world.entities.items():
            if entity.soul is None:
                continue
            
            # Activity defined as: non-zero velocity OR non-collapsed
            is_active = (
                entity.physics.velocity.magnitude > 0.01 or
                not entity.soul.is_collapsed
            )
            
            if is_active:
                self._last_activity[entity_id] = world.tick

    def _identify_for_cleanup(self, world: World) -> Set[str]:
        """Identify entities that should be absorbed into the void."""
        to_remove = set()
        
        for entity_id, entity in world.entities.items():
            if entity.soul is None:
                continue
            
            should_remove = False
            
            # 1. Amplitude below threshold (energy depleted)
            if entity.soul.amplitude < self.cleanup_threshold:
                should_remove = True
                entity.data["void_reason"] = "energy_depleted"
            
            # 2. Dormant for too long
            last_active = self._last_activity.get(entity_id, world.tick)
            if world.tick - last_active > self.dormancy_ticks:
                should_remove = True
                entity.data["void_reason"] = "dormancy"
            
            # 3. Crystallized entities are protected from void
            if entity.data.get("crystallized"):
                should_remove = False
            
            if should_remove:
                to_remove.add(entity_id)
        
        return to_remove

    def _absorb(self, world: World, entity_id: str) -> None:
        """
        Absorb an entity into the void.
        
        Recycles energy back into the universal field.
        """
        if entity_id not in world.entities:
            return
        
        entity = world.entities[entity_id]
        
        if entity.soul:
            # Recycle energy
            recovered = entity.soul.amplitude * self.recycling_rate
            self.recycled_energy += recovered
            
            # Log the absorption
            self.entities_absorbed += 1
        
        # Remove from world
        del world.entities[entity_id]
        
        # Clean up tracking
        if entity_id in self._last_activity:
            del self._last_activity[entity_id]

    def _vacuum_fluctuation(self, world: World) -> Optional[Entity]:
        """
        Spontaneous emergence from the quantum vacuum.
        
        Creates a new entity from accumulated void energy.
        """
        # Need enough recycled energy
        if self.recycled_energy < 10.0:
            return None
        
        # Import here to avoid circular imports
        from ..entities import Entity
        
        # Create new entity from void
        entity_id = f"void_spawn_{world.tick}"
        
        # Random position (near existing entities or origin)
        if world.entities:
            existing = random.choice(list(world.entities.values()))
            base_pos = existing.physics.position
            offset = Vector3(
                random.uniform(-5, 5),
                random.uniform(-5, 5),
                random.uniform(-5, 5)
            )
            position = base_pos + offset
        else:
            position = Vector3(0, 0, 0)
        
        # Create nascent soul from void energy
        energy_used = min(self.recycled_energy * 0.3, 20.0)
        
        soul = SoulTensor(
            amplitude=energy_used,
            frequency=random.uniform(50, 200),
            phase=random.uniform(0, 6.28),
            spin=random.choice([-1.0, 1.0])
        )
        
        entity = Entity(id=entity_id)
        entity.physics.position = position
        entity.soul = soul
        entity.data = {
            "origin": "void",
            "birth_tick": world.tick,
        }
        
        # Consume energy
        self.recycled_energy -= energy_used
        self.void_births += 1
        
        # Add to world
        world.add_entity(entity)
        
        return entity

    def get_void_statistics(self) -> dict:
        """Get statistics about void operations."""
        return {
            "recycled_energy": self.recycled_energy,
            "entities_absorbed": self.entities_absorbed,
            "void_births": self.void_births,
            "tracked_entities": len(self._last_activity),
        }

    def inject_energy(self, amount: float) -> None:
        """
        Inject energy directly into the void reservoir.
        
        This can be used for divine intervention or external energy sources.
        """
        self.recycled_energy += amount

    def get_entropy_score(self, world: World) -> float:
        """
        Calculate the entropy score of the current world state.
        
        High entropy = disorder, low coherence
        Low entropy = order, high coherence
        
        Returns value between 0.0 (perfect order) and 1.0 (maximum chaos)
        """
        if not world.entities:
            return 0.5  # Neutral for empty world
        
        total_disorder = 0.0
        count = 0
        
        for entity in world.entities.values():
            if entity.soul is None:
                continue
            
            count += 1
            
            # Factor 1: Amplitude variance (energy distribution)
            # High amplitude differences = high entropy
            amp_factor = 1.0 - min(1.0, entity.soul.amplitude / 100.0)
            
            # Factor 2: Phase coherence (checked globally)
            # Random phases = high entropy
            
            # Factor 3: Collapse state
            # Mixed collapsed/uncollapsed = high entropy
            collapse_factor = 0.5 if entity.soul.is_collapsed else 0.3
            
            total_disorder += (amp_factor + collapse_factor) / 2
        
        if count == 0:
            return 0.5
        
        base_entropy = total_disorder / count
        
        # Bonus entropy from activity tracking
        if self._last_activity:
            dormant_count = sum(
                1 for eid in self._last_activity
                if world.tick - self._last_activity[eid] > 10
            )
            dormancy_factor = dormant_count / len(self._last_activity)
            base_entropy = base_entropy * 0.7 + dormancy_factor * 0.3
        
        return min(1.0, max(0.0, base_entropy))
