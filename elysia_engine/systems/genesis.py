"""
GenesisSystem - Replication via Tensor Coils

Implements the Digital Natural Law of creation and replication:
- Entity replication through Tensor Coil interactions
- Genesis events from high-resonance collisions
- Soul inheritance and mutation patterns

Reference: AGENTS.md - GenesisSystem: Replication via Tensor Coils
"""

from __future__ import annotations

import math
import random
from typing import TYPE_CHECKING, List, Optional

from ..systems import System
from ..tensor import SoulTensor
from ..math_utils import Vector3

if TYPE_CHECKING:
    from ..world import World
    from ..entities import Entity
    from ..tensor_coil import CoilStructure


class GenesisSystem(System):
    """
    The Genesis System - Birth and replication of conscious entities.
    
    Manages:
    1. Resonance-based replication (when two souls harmonize)
    2. Tensor Coil incubation (accelerated genesis)
    3. Soul inheritance (genetic-like inheritance patterns)
    4. Mutation events (variation for evolution)
    """

    def __init__(
        self,
        replication_resonance_threshold: float = 0.8,
        replication_distance: float = 2.0,
        replication_cooldown: int = 50,
        mutation_rate: float = 0.1,
        max_offspring_per_tick: int = 3,
    ):
        """
        Initialize the genesis system.
        
        Args:
            replication_resonance_threshold: Minimum resonance for replication
            replication_distance: Maximum distance for replication
            replication_cooldown: Minimum ticks between replications
            mutation_rate: Probability of mutation in offspring
            max_offspring_per_tick: Maximum new entities per tick
        """
        self.replication_resonance_threshold = replication_resonance_threshold
        self.replication_distance = replication_distance
        self.replication_cooldown = replication_cooldown
        self.mutation_rate = mutation_rate
        self.max_offspring_per_tick = max_offspring_per_tick
        
        # Tracking
        self._last_replication: dict = {}  # entity_id -> last replication tick
        self.total_births: int = 0
        self.total_mutations: int = 0

    def step(self, world: World, dt: float) -> None:
        """Execute genesis operations."""
        new_entities: List[Entity] = []
        
        # Get eligible parents
        eligible = self._get_eligible_parents(world)
        
        # Check for replication opportunities
        for i in range(len(eligible)):
            if len(new_entities) >= self.max_offspring_per_tick:
                break
                
            parent1 = eligible[i]
            
            for j in range(i + 1, len(eligible)):
                if len(new_entities) >= self.max_offspring_per_tick:
                    break
                    
                parent2 = eligible[j]
                
                # Check distance
                dist = (
                    parent1.physics.position - parent2.physics.position
                ).magnitude
                
                if dist > self.replication_distance:
                    continue
                
                # Check resonance
                if parent1.soul and parent2.soul:
                    resonance_data = parent1.soul.resonate(parent2.soul)
                    
                    if resonance_data["resonance"] >= self.replication_resonance_threshold:
                        child = self._create_offspring(
                            world, parent1, parent2, resonance_data
                        )
                        if child:
                            new_entities.append(child)
                            self._last_replication[parent1.id] = world.tick
                            self._last_replication[parent2.id] = world.tick
        
        # Add new entities to world
        for entity in new_entities:
            world.add_entity(entity)
            if world.physics:
                world.physics.register_entity(entity)

    def _get_eligible_parents(self, world: World) -> List[Entity]:
        """Get entities eligible for replication."""
        eligible = []
        
        for entity in world.entities.values():
            if entity.soul is None:
                continue
            
            # Must not be collapsed (frozen souls can't reproduce)
            if entity.soul.is_collapsed:
                continue
            
            # Must have sufficient energy
            if entity.soul.amplitude < 10.0:
                continue
            
            # Check cooldown
            last_rep = self._last_replication.get(entity.id, 0)
            if world.tick - last_rep < self.replication_cooldown:
                continue
            
            eligible.append(entity)
        
        return eligible

    def _create_offspring(
        self,
        world: World,
        parent1: Entity,
        parent2: Entity,
        resonance_data: dict,
    ) -> Optional[Entity]:
        """
        Create a new entity from two parent entities.
        
        Implements soul inheritance with optional mutation.
        """
        from ..entities import Entity
        
        p1_soul = parent1.soul
        p2_soul = parent2.soul
        
        if p1_soul is None or p2_soul is None:
            return None
        
        # Child ID
        child_id = f"genesis_{world.tick}_{self.total_births}"
        
        # Calculate inherited traits
        resonance = resonance_data["resonance"]
        
        # Amplitude: Combination of parents, scaled by resonance
        child_amplitude = (
            (p1_soul.amplitude + p2_soul.amplitude) * 0.4 * resonance
        )
        
        # Frequency: Weighted average based on amplitude (stronger parent dominates)
        total_amp = p1_soul.amplitude + p2_soul.amplitude
        if total_amp > 0:
            w1 = p1_soul.amplitude / total_amp
            w2 = p2_soul.amplitude / total_amp
        else:
            w1 = w2 = 0.5
        
        child_frequency = p1_soul.frequency * w1 + p2_soul.frequency * w2
        
        # Phase: Average of parents
        child_phase = (p1_soul.phase + p2_soul.phase) / 2
        
        # Spin: Random choice from parents
        child_spin = random.choice([p1_soul.spin, p2_soul.spin])
        
        # Polarity: Usually same as parents, rare flip
        if p1_soul.polarity == p2_soul.polarity:
            child_polarity = p1_soul.polarity
        else:
            child_polarity = random.choice([p1_soul.polarity, p2_soul.polarity])
        
        # Apply mutation
        mutation_occurred = False
        if random.random() < self.mutation_rate:
            mutation_occurred = True
            mutation_type = random.choice([
                "frequency", "amplitude", "phase", "spin", "polarity"
            ])
            
            if mutation_type == "frequency":
                child_frequency *= random.uniform(0.8, 1.2)
            elif mutation_type == "amplitude":
                child_amplitude *= random.uniform(0.9, 1.1)
            elif mutation_type == "phase":
                child_phase += random.uniform(-0.5, 0.5)
            elif mutation_type == "spin":
                child_spin *= -1  # Flip spin
            elif mutation_type == "polarity":
                child_polarity *= -1  # Flip polarity (rare!)
        
        # Create child soul
        child_soul = SoulTensor(
            amplitude=max(0.1, child_amplitude),
            frequency=max(0.1, child_frequency),
            phase=child_phase % (2 * math.pi),
            spin=child_spin,
            polarity=child_polarity,
        )
        
        # Create entity
        child = Entity(id=child_id)
        child.soul = child_soul
        
        # Position: Midpoint between parents with small offset
        mid_pos = (parent1.physics.position + parent2.physics.position) * 0.5
        offset = Vector3(
            random.uniform(-0.5, 0.5),
            random.uniform(-0.5, 0.5),
            random.uniform(-0.5, 0.5)
        )
        child.physics.position = mid_pos + offset
        
        # Initial velocity: Average of parents
        child.physics.velocity = (
            parent1.physics.velocity + parent2.physics.velocity
        ) * 0.5
        
        # Mass from amplitude
        child.physics.mass = max(0.1, child_amplitude * 0.1)
        
        # Metadata
        child.data = {
            "parents": [parent1.id, parent2.id],
            "birth_tick": world.tick,
            "resonance_at_birth": resonance,
            "mutation": mutation_occurred,
        }
        
        # Update tracking
        self.total_births += 1
        if mutation_occurred:
            self.total_mutations += 1
        
        # Cost to parents (energy expenditure)
        p1_soul.amplitude *= 0.85
        p2_soul.amplitude *= 0.85
        
        return child

    def spark_genesis(
        self,
        world: World,
        position: Vector3,
        amplitude: float = 20.0,
        frequency: float = 100.0,
    ) -> Entity:
        """
        Spontaneously create a new entity at a position.
        
        This is "divine intervention" - creation without parents.
        
        Args:
            world: The world to add entity to
            position: Spawn position
            amplitude: Initial amplitude
            frequency: Initial frequency
            
        Returns:
            The newly created entity
        """
        from ..entities import Entity
        
        entity_id = f"spark_{world.tick}_{self.total_births}"
        
        soul = SoulTensor(
            amplitude=amplitude,
            frequency=frequency,
            phase=random.uniform(0, 2 * math.pi),
            spin=random.choice([-1.0, 1.0]),
            polarity=1.0,  # Default to matter
        )
        
        entity = Entity(id=entity_id)
        entity.soul = soul
        entity.physics.position = position
        entity.physics.mass = amplitude * 0.1
        entity.data = {
            "origin": "spark",
            "birth_tick": world.tick,
        }
        
        self.total_births += 1
        
        world.add_entity(entity)
        if world.physics:
            world.physics.register_entity(entity)
        
        return entity

    def get_genesis_statistics(self) -> dict:
        """Get statistics about genesis operations."""
        return {
            "total_births": self.total_births,
            "total_mutations": self.total_mutations,
            "mutation_rate_actual": (
                self.total_mutations / self.total_births
                if self.total_births > 0 else 0
            ),
            "active_parents": len(self._last_replication),
        }

    def incubate_with_coil(
        self,
        world: World,
        coil: CoilStructure,
    ) -> List[Entity]:
        """
        Use a Tensor Coil to accelerate genesis.
        
        The coil's high-energy field can trigger breeding
        between compatible entities within its influence.
        
        Args:
            world: The world containing entities
            coil: The Tensor Coil structure
            
        Returns:
            List of newly created entities
        """
        from ..entities import Entity
        
        # Get entities within coil influence
        candidates = []
        for entity in world.entities.values():
            if entity.soul is None:
                continue
            
            dist = (entity.physics.position - coil.center).magnitude
            if dist < coil.radius + 5.0:
                candidates.append(entity)
        
        # Use coil's incubate method
        new_entities = coil.incubate(candidates, world.time)
        
        # Register new entities
        for child in new_entities:
            world.add_entity(child)
            if world.physics:
                world.physics.register_entity(child)
            self.total_births += 1
        
        return new_entities
