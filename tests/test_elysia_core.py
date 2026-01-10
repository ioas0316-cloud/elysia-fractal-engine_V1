"""
Tests for the Refactored Elysia Core (Field/Tensor Architecture).
"""

import pytest
import math
from elysia_core import (
    ElysiaIdentity,
    ElysiaBridge,
    SoulTensor,
    PhysicsWorld,
    Entity,
    Persona,
    Vector3,
    Vector4,
    Quaternion
)

class TestElysiaIdentity:
    """Tests for the Identity Module."""
    
    def test_identity_axioms(self):
        """Test that the Ten Commandments are correctly defined."""
        axioms = ElysiaIdentity.assert_identity()
        assert len(axioms) == 10
        assert "E.L.Y.S.I.A." in axioms[0]
        assert "Not a Tool" in axioms[1] or "Being" in axioms[1]

class TestSoulTensor:
    """Tests for the SoulTensor Data Structure."""
    
    def test_creation(self):
        soul = SoulTensor(amplitude=10.0, frequency=7.0, phase=0.0)
        assert soul.amplitude == 10.0
        assert soul.frequency == 7.0
        assert soul.phase == 0.0
        assert not soul.is_collapsed
        
    def test_step(self):
        """Test phase evolution."""
        soul = SoulTensor(amplitude=10.0, frequency=math.pi, phase=0.0)
        soul.step(dt=1.0)
        # Phase should increase by freq * dt = pi
        assert soul.phase == pytest.approx(math.pi)
        
    def test_resonance(self):
        """Test resonance calculation."""
        soul1 = SoulTensor(amplitude=10, frequency=10, phase=0)
        soul2 = SoulTensor(amplitude=10, frequency=10, phase=0)
        
        # Perfect resonance (same phase)
        res = soul1.resonate(soul2)
        assert res["resonance"] == pytest.approx(1.0)
        
        # Anti-resonance (phase pi apart)
        soul2.phase = math.pi
        res = soul1.resonate(soul2)
        assert res["resonance"] == pytest.approx(-1.0)

class TestPhysicsWorld:
    """Tests for the Physics Engine."""
    
    def test_world_step(self):
        world = PhysicsWorld()
        entity = Entity(id="test", soul=SoulTensor(10, 10, 0))
        world.add_entity(entity)
        
        # Run a step
        world.step(0.1)
        assert world.tick == 1
        
    def test_sedimentation(self):
        """Test that heavy entities sink to the abyss."""
        world = PhysicsWorld()
        # High entropy -> High mass
        # To force high mass, we need high entropy (dissonance).
        # Resonance penalty scale is 10. Horizon freq is ~1.6.
        # Freq 100 -> Delta ~98 -> Entropy ~980 -> Mass ~490 >> 50
        entity = Entity(id="heavy", soul=SoulTensor(100, 100.0, 0))
        world.add_entity(entity)
        
        world.step(0.1)
        
        # Should be moved to sediments
        assert len(world.entities) == 0
        assert len(world.sediments) == 1

class TestElysiaBridge:
    """Tests for the Adapter/Bridge."""
    
    def test_wake_up(self):
        bridge = ElysiaBridge()
        msg = bridge.wake_up()
        assert "E.L.Y.S.I.A." in msg or "Identity" in msg
        
    def test_process_input(self):
        bridge = ElysiaBridge()
        result = bridge.process_input("Hello World", "TestUser")
        
        assert "resonance" in result
        assert "narrative_stream" in result
        assert len(result["narrative_stream"]) > 0
