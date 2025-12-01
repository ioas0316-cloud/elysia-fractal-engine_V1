"""
Tests for Yggdrasil (Self-Model) and Ether (Unified Field) systems.

These tests verify the core structure integration from the original Elysia project.
"""

import pytest
from datetime import datetime
import time

from elysia_engine.yggdrasil import (
    Yggdrasil, Realm, YggdrasilNode, get_yggdrasil
)
from elysia_engine.ether import (
    Ether, Wave, WavePhase, Frequency, get_ether, emit_wave
)


class TestYggdrasilNode:
    """Test YggdrasilNode dataclass"""

    def test_node_creation(self):
        """Test basic node creation"""
        node = YggdrasilNode(
            name="TestModule",
            realm=Realm.ROOT,
            module=object(),
            vitality=1.0
        )
        assert node.name == "TestModule"
        assert node.realm == Realm.ROOT
        assert node.vitality == 1.0
        assert node.is_healthy()

    def test_node_decay(self):
        """Test vitality decay"""
        node = YggdrasilNode(name="Test", realm=Realm.TRUNK, module=None)
        initial = node.vitality
        node.decay(0.1)
        assert node.vitality == initial - 0.1
        
        # Should not go below 0
        node.vitality = 0.05
        node.decay(0.1)
        assert node.vitality == 0.0

    def test_node_nourish(self):
        """Test vitality nourish"""
        node = YggdrasilNode(name="Test", realm=Realm.BRANCH, module=None, vitality=0.5)
        node.nourish(0.3)
        assert node.vitality == 0.8
        
        # Should not go above 1
        node.nourish(0.5)
        assert node.vitality == 1.0

    def test_is_healthy(self):
        """Test health check"""
        node = YggdrasilNode(name="Test", realm=Realm.ROOT, module=None)
        assert node.is_healthy()
        
        node.vitality = 0.3
        assert not node.is_healthy()
        
        node.vitality = 0.31
        assert node.is_healthy()


class TestYggdrasil:
    """Test Yggdrasil Self-Model"""

    @pytest.fixture(autouse=True)
    def reset_yggdrasil(self):
        """Reset Yggdrasil before each test"""
        ygg = get_yggdrasil()
        ygg.reset()
        yield
        ygg.reset()

    def test_singleton(self):
        """Test singleton pattern"""
        ygg1 = Yggdrasil()
        ygg2 = Yggdrasil()
        assert ygg1 is ygg2

    def test_get_yggdrasil(self):
        """Test get_yggdrasil helper"""
        ygg = get_yggdrasil()
        assert isinstance(ygg, Yggdrasil)

    def test_plant_root(self):
        """Test planting root modules"""
        ygg = get_yggdrasil()
        mock_module = {"name": "Ether"}
        ygg.plant_root("Ether", mock_module)
        
        assert len(ygg.roots) == 1
        assert ygg.roots[0].name == "Ether"
        assert ygg.roots[0].realm == Realm.ROOT

    def test_grow_trunk(self):
        """Test growing trunk modules"""
        ygg = get_yggdrasil()
        mock_module = {"name": "Memory"}
        ygg.grow_trunk("Memory", mock_module)
        
        assert len(ygg.trunk) == 1
        assert ygg.trunk[0].name == "Memory"
        assert ygg.trunk[0].realm == Realm.TRUNK

    def test_extend_branch(self):
        """Test extending branch modules"""
        ygg = get_yggdrasil()
        mock_module = {"name": "Sensor"}
        ygg.extend_branch("Sensor", mock_module)
        
        assert len(ygg.branches) == 1
        assert ygg.branches[0].name == "Sensor"
        assert ygg.branches[0].realm == Realm.BRANCH

    def test_get_node(self):
        """Test getting node by name"""
        ygg = get_yggdrasil()
        mock_module = {"test": True}
        ygg.plant_root("TestRoot", mock_module)
        
        node = ygg.get_node("TestRoot")
        assert node is not None
        assert node.name == "TestRoot"
        
        assert ygg.get_node("NonExistent") is None

    def test_get_module(self):
        """Test getting module by name"""
        ygg = get_yggdrasil()
        mock_module = {"test": True}
        ygg.plant_root("TestRoot", mock_module)
        
        module = ygg.get_module("TestRoot")
        assert module == mock_module
        
        assert ygg.get_module("NonExistent") is None

    def test_status(self):
        """Test status report"""
        ygg = get_yggdrasil()
        ygg.plant_root("Root1", None)
        ygg.grow_trunk("Trunk1", None)
        ygg.extend_branch("Branch1", None)
        
        status = ygg.status()
        assert status["total_nodes"] == 3
        assert len(status["roots"]) == 1
        assert len(status["trunk"]) == 1
        assert len(status["branches"]) == 1
        assert "overall_vitality" in status

    def test_is_alive(self):
        """Test alive check"""
        ygg = get_yggdrasil()
        
        # No roots = not alive
        assert not ygg.is_alive()
        
        # Add healthy root
        ygg.plant_root("Root", None)
        assert ygg.is_alive()
        
        # Damage root
        ygg.get_node("Root").vitality = 0.1
        assert not ygg.is_alive()

    def test_prune(self):
        """Test pruning branches"""
        ygg = get_yggdrasil()
        ygg.extend_branch("Branch1", None)
        
        assert ygg.prune("Branch1")
        assert len(ygg.branches) == 0
        
        # Cannot prune non-existent
        assert not ygg.prune("NonExistent")
        
        # Cannot prune roots
        ygg.plant_root("Root1", None)
        assert not ygg.prune("Root1")

    def test_heartbeat(self):
        """Test heartbeat mechanism"""
        ygg = get_yggdrasil()
        ygg.plant_root("Root", None)
        ygg.grow_trunk("Trunk", None)
        
        initial_trunk_vitality = ygg.get_node("Trunk").vitality
        
        # Heartbeat should decay and then nourish
        for _ in range(10):
            ygg.heartbeat()
        
        # Trunk should be nourished by healthy root
        # (decay 0.001 * 10 = 0.01, nourish 0.002 * 10 = 0.02)
        # Net gain: 0.01
        assert ygg.get_node("Trunk").vitality > initial_trunk_vitality - 0.02


class TestWave:
    """Test Wave dataclass"""

    def test_wave_creation(self):
        """Test basic wave creation"""
        wave = Wave(
            sender="Test",
            frequency=10.0,
            amplitude=0.5,
            phase="THOUGHT",
            payload={"data": "test"}
        )
        assert wave.sender == "Test"
        assert wave.frequency == 10.0
        assert wave.amplitude == 0.5
        assert wave.phase == "THOUGHT"
        assert wave.payload == {"data": "test"}
        assert wave.id is not None

    def test_wave_energy(self):
        """Test energy calculation"""
        wave = Wave(
            sender="Test",
            frequency=10.0,
            amplitude=0.5,
            phase="TEST",
            payload=None
        )
        assert wave.energy == 5.0  # 10.0 * 0.5

    def test_wave_to_dict(self):
        """Test serialization"""
        wave = Wave(
            sender="Test",
            frequency=10.0,
            amplitude=0.5,
            phase="TEST",
            payload=None
        )
        d = wave.to_dict()
        assert d["sender"] == "Test"
        assert d["frequency"] == 10.0
        assert "timestamp" in d

    def test_wave_is_expired(self):
        """Test expiration check"""
        wave = Wave(
            sender="Test",
            frequency=1.0,
            amplitude=1.0,
            phase="TEST",
            payload=None
        )
        assert not wave.is_expired(max_age_seconds=60.0)
        assert wave.is_expired(max_age_seconds=0.0)


class TestEther:
    """Test Ether Unified Field"""

    @pytest.fixture(autouse=True)
    def reset_ether(self):
        """Reset Ether before each test"""
        eth = get_ether()
        eth.reset()
        yield
        eth.reset()

    def test_singleton(self):
        """Test singleton pattern"""
        eth1 = Ether()
        eth2 = Ether()
        assert eth1 is eth2

    def test_get_ether(self):
        """Test get_ether helper"""
        eth = get_ether()
        assert isinstance(eth, Ether)

    def test_emit_wave(self):
        """Test wave emission"""
        eth = get_ether()
        wave = Wave(
            sender="Test",
            frequency=10.0,
            amplitude=1.0,
            phase="TEST",
            payload=None
        )
        eth.emit(wave)
        
        waves = eth.get_waves()
        assert len(waves) == 1
        assert waves[0].sender == "Test"

    def test_tune_in_and_resonance(self):
        """Test frequency tuning and resonance"""
        eth = get_ether()
        received = []
        
        def callback(wave):
            received.append(wave)
        
        eth.tune_in(10.0, callback)
        
        wave = Wave(
            sender="Test",
            frequency=10.0,
            amplitude=1.0,
            phase="TEST",
            payload={"test": True}
        )
        eth.emit(wave)
        
        assert len(received) == 1
        assert received[0].payload == {"test": True}

    def test_tune_out(self):
        """Test frequency tune out"""
        eth = get_ether()
        received = []
        
        def callback(wave):
            received.append(wave)
        
        eth.tune_in(10.0, callback)
        eth.tune_out(10.0, callback)
        
        wave = Wave(
            sender="Test",
            frequency=10.0,
            amplitude=1.0,
            phase="TEST",
            payload=None
        )
        eth.emit(wave)
        
        assert len(received) == 0

    def test_get_waves_by_frequency(self):
        """Test filtering waves by frequency"""
        eth = get_ether()
        eth.emit(Wave(sender="A", frequency=10.0, amplitude=1.0, phase="T", payload=None))
        eth.emit(Wave(sender="B", frequency=20.0, amplitude=1.0, phase="T", payload=None))
        eth.emit(Wave(sender="C", frequency=10.5, amplitude=1.0, phase="T", payload=None))
        
        waves = eth.get_waves_by_frequency(10.0, tolerance=0.1)
        assert len(waves) == 2  # 10.0 and 10.5 are within 10% of 10.0

    def test_get_waves_by_phase(self):
        """Test filtering waves by phase"""
        eth = get_ether()
        eth.emit(Wave(sender="A", frequency=10.0, amplitude=1.0, phase="THOUGHT", payload=None))
        eth.emit(Wave(sender="B", frequency=10.0, amplitude=1.0, phase="EMOTION", payload=None))
        
        waves = eth.get_waves_by_phase("THOUGHT")
        assert len(waves) == 1
        assert waves[0].sender == "A"

    def test_clear_expired_waves(self):
        """Test clearing expired waves"""
        eth = get_ether()
        eth.emit(Wave(sender="A", frequency=10.0, amplitude=1.0, phase="T", payload=None))
        
        # With 0 max age, all waves are expired
        removed = eth.clear_expired_waves(max_age_seconds=0.0)
        assert removed == 1
        assert len(eth.get_waves()) == 0

    def test_status(self):
        """Test status report"""
        eth = get_ether()
        eth.tune_in(10.0, lambda w: None)
        eth.emit(Wave(sender="A", frequency=10.0, amplitude=0.5, phase="T", payload=None))
        
        status = eth.status()
        assert status["total_waves"] == 1
        assert 10.0 in status["listener_frequencies"]
        assert status["listener_count"] == 1
        assert status["average_amplitude"] == 0.5

    def test_emit_wave_helper(self):
        """Test emit_wave convenience function"""
        eth = get_ether()
        wave = emit_wave(
            sender="Test",
            frequency=Frequency.THOUGHT,
            amplitude=0.8,
            phase=WavePhase.INSIGHT.value,
            payload={"insight": "hello"}
        )
        
        assert wave.frequency == Frequency.THOUGHT
        assert wave.phase == "INSIGHT"
        assert len(eth.get_waves()) == 1


class TestFrequencyConstants:
    """Test Frequency constants"""

    def test_frequency_values(self):
        """Test standard frequency values"""
        assert Frequency.TIME == 0.1
        assert Frequency.LIFE == 1.0
        assert Frequency.THOUGHT == 10.0
        assert Frequency.EMOTION == 40.0
        assert Frequency.HEALING == 432.0
        assert Frequency.COSMIC == 963.0


class TestWavePhase:
    """Test WavePhase enum"""

    def test_phase_values(self):
        """Test phase enum values"""
        assert WavePhase.TIME.value == "TIME"
        assert WavePhase.THOUGHT.value == "THOUGHT"
        assert WavePhase.EMOTION.value == "EMOTION"
        assert WavePhase.MEMORY.value == "MEMORY"
