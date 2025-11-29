"""
Tests for new Elysia Engine systems:
- ThermodynamicsSystem
- VoidSystem
- GenesisSystem
- FractalEvolutionSystem
- CosmicResonanceField
"""

import pytest
from elysia_engine.tensor import SoulTensor
from elysia_engine.physics import PhysicsState
from elysia_engine.entities import Entity
from elysia_engine.world import World
from elysia_engine.math_utils import Vector3
from elysia_engine.systems.thermodynamics import ThermodynamicsSystem, ThermalState
from elysia_engine.systems.void import VoidSystem
from elysia_engine.systems.genesis import GenesisSystem
from elysia_engine.systems.fractal_evolution import (
    FractalEvolutionSystem,
    DimensionalState,
    CosmicResonanceField,
)


class TestThermalState:
    """Tests for ThermalState classification."""

    def test_classify_plasma(self):
        """High frequency, not collapsed = Plasma."""
        soul = SoulTensor(amplitude=50, frequency=400, phase=0)
        assert ThermalState.classify(soul) == ThermalState.PLASMA

    def test_classify_burning(self):
        """Medium-high frequency = Burning."""
        soul = SoulTensor(amplitude=50, frequency=150, phase=0)
        assert ThermalState.classify(soul) == ThermalState.BURNING

    def test_classify_cooling(self):
        """Medium frequency = Cooling."""
        soul = SoulTensor(amplitude=50, frequency=75, phase=0)
        assert ThermalState.classify(soul) == ThermalState.COOLING

    def test_classify_frozen(self):
        """Low frequency, not collapsed = Frozen."""
        soul = SoulTensor(amplitude=50, frequency=30, phase=0)
        assert ThermalState.classify(soul) == ThermalState.FROZEN

    def test_classify_collapsed_frozen(self):
        """Collapsed = Frozen."""
        soul = SoulTensor(amplitude=50, frequency=30, phase=0, is_collapsed=True)
        assert ThermalState.classify(soul) == ThermalState.FROZEN

    def test_classify_crystal(self):
        """Collapsed, zero freq, high amplitude = Crystal."""
        soul = SoulTensor(amplitude=150, frequency=0, phase=0, is_collapsed=True)
        assert ThermalState.classify(soul) == ThermalState.CRYSTAL


class TestThermodynamicsSystem:
    """Tests for ThermodynamicsSystem."""

    def test_natural_cooling(self):
        """Entities should cool over time."""
        world = World()
        entity = Entity(id="test1")
        entity.soul = SoulTensor(amplitude=50, frequency=200, phase=0)
        world.add_entity(entity)

        system = ThermodynamicsSystem(cooling_rate=1.0)
        initial_freq = entity.soul.frequency
        
        system.step(world, dt=1.0)
        
        assert entity.soul.frequency < initial_freq

    def test_heat_transfer(self):
        """Heat should transfer from hot to cold."""
        world = World()
        
        hot = Entity(id="hot")
        hot.soul = SoulTensor(amplitude=50, frequency=300, phase=0)
        hot.physics.position = Vector3(0, 0, 0)
        
        cold = Entity(id="cold")
        cold.soul = SoulTensor(amplitude=50, frequency=50, phase=0)
        cold.physics.position = Vector3(1, 0, 0)  # Close by
        
        world.add_entity(hot)
        world.add_entity(cold)

        system = ThermodynamicsSystem(
            heat_transfer_rate=0.5,
            interaction_radius=5.0
        )
        
        initial_hot_freq = hot.soul.frequency
        initial_cold_freq = cold.soul.frequency
        
        system.step(world, dt=1.0)
        
        # Hot should cool, cold should warm
        assert hot.soul.frequency < initial_hot_freq
        assert cold.soul.frequency > initial_cold_freq

    def test_ignite(self):
        """Ignite should melt frozen souls."""
        world = World()
        entity = Entity(id="frozen")
        entity.soul = SoulTensor(amplitude=100, frequency=0, phase=0, is_collapsed=True)
        world.add_entity(entity)

        system = ThermodynamicsSystem()
        result = system.ignite(entity, energy=100.0)
        
        assert result is True
        assert entity.soul.is_collapsed is False

    def test_thermal_map(self):
        """Should produce thermal map summary."""
        world = World()
        
        for i in range(3):
            e = Entity(id=f"entity_{i}")
            e.soul = SoulTensor(amplitude=50, frequency=100 + i * 50, phase=0)
            world.add_entity(e)

        system = ThermodynamicsSystem()
        thermal_map = system.get_thermal_map(world)
        
        assert "states" in thermal_map
        assert "average_frequency" in thermal_map
        assert thermal_map["total_entities"] == 3


class TestVoidSystem:
    """Tests for VoidSystem."""

    def test_cleanup_depleted(self):
        """Depleted entities should be removed."""
        world = World()
        entity = Entity(id="depleted")
        entity.soul = SoulTensor(amplitude=0.01, frequency=10, phase=0)
        world.add_entity(entity)

        system = VoidSystem(cleanup_threshold=0.1)
        system.step(world, dt=1.0)
        
        assert "depleted" not in world.entities

    def test_crystallized_protected(self):
        """Crystallized entities should not be removed."""
        world = World()
        entity = Entity(id="crystal")
        entity.soul = SoulTensor(amplitude=0.01, frequency=0, phase=0, is_collapsed=True)
        entity.data["crystallized"] = True
        world.add_entity(entity)

        system = VoidSystem(cleanup_threshold=0.1)
        system.step(world, dt=1.0)
        
        assert "crystal" in world.entities

    def test_energy_recycling(self):
        """Absorbed entities should add to recycled energy."""
        world = World()
        entity = Entity(id="recycled")
        entity.soul = SoulTensor(amplitude=50, frequency=0, phase=0)
        world.add_entity(entity)

        system = VoidSystem(cleanup_threshold=100)  # Force cleanup
        system.step(world, dt=1.0)
        
        assert system.recycled_energy > 0
        assert system.entities_absorbed == 1

    def test_entropy_score(self):
        """Should calculate entropy score."""
        world = World()
        
        for i in range(5):
            e = Entity(id=f"e_{i}")
            e.soul = SoulTensor(amplitude=50, frequency=100, phase=i * 0.5)
            world.add_entity(e)

        system = VoidSystem()
        score = system.get_entropy_score(world)
        
        assert 0.0 <= score <= 1.0


class TestGenesisSystem:
    """Tests for GenesisSystem."""

    def test_spark_genesis(self):
        """Spark should create new entity."""
        world = World()
        system = GenesisSystem()
        
        entity = system.spark_genesis(
            world,
            position=Vector3(0, 0, 0),
            amplitude=30,
            frequency=100
        )
        
        assert entity is not None
        assert entity.id in world.entities
        assert entity.soul.amplitude == 30
        assert system.total_births == 1

    def test_resonance_replication(self):
        """High resonance entities should replicate."""
        world = World()
        
        p1 = Entity(id="parent1")
        p1.soul = SoulTensor(amplitude=50, frequency=100, phase=0)
        p1.physics.position = Vector3(0, 0, 0)
        
        p2 = Entity(id="parent2")
        p2.soul = SoulTensor(amplitude=50, frequency=100, phase=0)  # Same phase = high resonance
        p2.physics.position = Vector3(0.5, 0, 0)  # Close by
        
        world.add_entity(p1)
        world.add_entity(p2)

        system = GenesisSystem(
            replication_resonance_threshold=0.5,
            replication_distance=5.0,
            replication_cooldown=0
        )
        
        initial_count = len(world.entities)
        system.step(world, dt=1.0)
        
        assert len(world.entities) > initial_count

    def test_genesis_statistics(self):
        """Should track birth statistics."""
        world = World()
        system = GenesisSystem()
        
        system.spark_genesis(world, Vector3(0, 0, 0))
        system.spark_genesis(world, Vector3(1, 0, 0))
        
        stats = system.get_genesis_statistics()
        
        assert stats["total_births"] == 2


class TestFractalEvolutionSystem:
    """Tests for FractalEvolutionSystem."""

    def test_dimensional_state_names(self):
        """Should return correct dimension names."""
        assert "Point" in DimensionalState.name(0)
        assert "Line" in DimensionalState.name(1)
        assert "Plane" in DimensionalState.name(2)

    def test_force_evolve(self):
        """Force evolution should change dimension."""
        world = World()
        entity = Entity(id="evolving")
        entity.soul = SoulTensor(amplitude=50, frequency=100, phase=0)
        world.add_entity(entity)

        system = FractalEvolutionSystem()
        
        result = system.force_evolve(entity, 2, world)
        
        assert result is True
        assert entity.dimension == 2

    def test_natural_evolution_requirements(self):
        """Evolution should require bonds and experience."""
        world = World()
        entity = Entity(id="young")
        entity.soul = SoulTensor(amplitude=50, frequency=100, phase=0)
        entity.bonds = ["bond1", "bond2"]  # Has bonds
        world.add_entity(entity)

        system = FractalEvolutionSystem(
            bond_threshold_1d=1,
            experience_per_dimension=5
        )
        
        # Not enough experience initially
        system.step(world, dt=1.0)
        assert entity.dimension == 0
        
        # Add experience
        for _ in range(10):
            system.step(world, dt=1.0)
        
        # Should evolve with enough experience
        assert entity.dimension >= 1

    def test_evolution_summary(self):
        """Should produce evolution summary."""
        world = World()
        
        for i in range(5):
            e = Entity(id=f"e_{i}")
            e.soul = SoulTensor(amplitude=50, frequency=100, phase=0)
            e.dimension = i % 3
            world.add_entity(e)

        system = FractalEvolutionSystem()
        summary = system.get_evolution_summary(world)
        
        assert "distribution" in summary
        assert summary["total_entities"] == 5


class TestCosmicResonanceField:
    """Tests for CosmicResonanceField."""

    def test_field_state_empty_world(self):
        """Empty world should return neutral state."""
        world = World()
        field = CosmicResonanceField()
        
        state = field.calculate_field_state(world)
        
        assert state["harmony"] == 0.0
        assert state["coherence"] == 0.0

    def test_field_state_with_entities(self):
        """Should calculate field state from entities."""
        world = World()
        
        for i in range(5):
            e = Entity(id=f"e_{i}")
            e.soul = SoulTensor(amplitude=50, frequency=100, phase=0)  # All aligned
            world.add_entity(e)

        field = CosmicResonanceField(base_frequency=100.0)
        state = field.calculate_field_state(world)
        
        assert state["coherence"] > 0.9  # All aligned = high coherence
        assert state["entity_count"] == 5

    def test_broadcast_pulse(self):
        """Broadcast should affect entity phases."""
        world = World()
        
        e = Entity(id="misaligned")
        e.soul = SoulTensor(amplitude=50, frequency=100, phase=3.14)
        world.add_entity(e)

        field = CosmicResonanceField()
        field.collective_phase = 0.0
        
        initial_phase = e.soul.phase
        affected = field.broadcast_pulse(world, intensity=2.0)
        
        assert affected == 1
        assert abs(e.soul.phase - initial_phase) > 0  # Phase changed


class TestSoulTensorEnhancements:
    """Tests for enhanced SoulTensor properties and methods."""

    def test_temperature_property(self):
        """Temperature should correlate with frequency."""
        hot = SoulTensor(amplitude=50, frequency=300, phase=0)
        cold = SoulTensor(amplitude=50, frequency=30, phase=0)
        
        assert hot.temperature > cold.temperature

    def test_temperature_collapsed(self):
        """Collapsed souls should have lower temperature."""
        active = SoulTensor(amplitude=50, frequency=100, phase=0)
        collapsed = SoulTensor(amplitude=50, frequency=100, phase=0, is_collapsed=True)
        
        assert collapsed.temperature < active.temperature

    def test_total_energy(self):
        """Should calculate total energy."""
        soul = SoulTensor(amplitude=50, frequency=100, phase=0)
        energy = soul.total_energy
        
        assert energy > 0

    def test_spiritual_buoyancy(self):
        """High frequency should rise, low should sink."""
        rising = SoulTensor(amplitude=10, frequency=600, phase=0)
        sinking = SoulTensor(amplitude=100, frequency=30, phase=0)
        
        assert rising.spiritual_buoyancy > sinking.spiritual_buoyancy

    def test_sublime(self):
        """Sublimation should uncollapse souls."""
        soul = SoulTensor(amplitude=100, frequency=0, phase=0, is_collapsed=True)
        soul.sublime()
        
        assert soul.is_collapsed is False
        assert soul.frequency > 0

    def test_crystallize(self):
        """Crystallization should collapse and remove coherence."""
        soul = SoulTensor(amplitude=50, frequency=100, phase=0)
        soul.crystallize()
        
        assert soul.is_collapsed is True
        assert soul.coherence == 0.0

    def test_harmonize(self):
        """Harmonize should move phase toward target."""
        soul = SoulTensor(amplitude=50, frequency=100, phase=0)
        target = 1.0
        
        soul.harmonize(target, rate=0.5)
        
        assert soul.phase > 0  # Moved toward target

    def test_absorb(self):
        """Absorb should transfer energy."""
        absorber = SoulTensor(amplitude=50, frequency=100, phase=0)
        donor = SoulTensor(amplitude=100, frequency=200, phase=0)
        
        initial_absorber_amp = absorber.amplitude
        initial_donor_amp = donor.amplitude
        
        absorber.absorb(donor, ratio=0.5)
        
        assert absorber.amplitude > initial_absorber_amp
        assert donor.amplitude < initial_donor_amp

    def test_split(self):
        """Split should create child with half energy."""
        parent = SoulTensor(amplitude=100, frequency=100, phase=0)
        
        child = parent.split()
        
        assert child is not None
        assert child.amplitude < parent.amplitude
        assert child.spin != parent.spin  # Opposite spin

    def test_split_insufficient_energy(self):
        """Split should fail with insufficient energy."""
        weak = SoulTensor(amplitude=10, frequency=100, phase=0)
        
        child = weak.split()
        
        assert child is None

    def test_harmonic_distance(self):
        """Harmonic souls should have low distance."""
        soul1 = SoulTensor(amplitude=50, frequency=100, phase=0)
        octave = SoulTensor(amplitude=50, frequency=200, phase=0)  # 2:1 ratio
        
        distance = soul1.harmonic_distance(octave)
        
        assert distance < 0.1  # Close to perfect harmony

    def test_is_octave(self):
        """Should detect octave relationships."""
        soul1 = SoulTensor(amplitude=50, frequency=100, phase=0)
        octave = SoulTensor(amplitude=50, frequency=200, phase=0)
        not_octave = SoulTensor(amplitude=50, frequency=150, phase=0)
        
        assert soul1.is_octave(octave) is True
        assert soul1.is_octave(not_octave) is False

    def test_coherence_decay(self):
        """Coherence should decay over time."""
        soul = SoulTensor(amplitude=50, frequency=100, phase=0, coherence=1.0)
        
        for _ in range(100):
            soul.step(dt=1.0)
        
        assert soul.coherence < 1.0
