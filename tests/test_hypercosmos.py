"""
Tests for HyperCosmos Architecture and Analog Zoom.
"""

import pytest
import math
from elysia_core import (
    HyperCosmos,
    HypersphereMemory,
    TesseractCoord,
    SoulTensor,
    Rotor,
    Quaternion
)

class TestHyperCosmos:
    """Tests for the unifying HyperCosmos container."""

    def test_initialization(self):
        cosmos = HyperCosmos(name="TestUniverse")
        assert cosmos.world is not None
        assert cosmos.memory is not None
        assert cosmos.scale == 1.0

    def test_analog_dial_memory(self):
        """Test the Analog Zoom (W-Axis) for Memory Retrieval."""
        cosmos = HyperCosmos()

        # Store memories at different W-depths
        # Deep Subconscious (W = -10)
        cosmos.memory.store(
            content="Deep Trauma",
            coord=TesseractCoord(w=-10.0, x=0, y=0, z=0),
            soul_tensor=SoulTensor(10, 10, 0)
        )
        # Surface Thought (W = -1)
        cosmos.memory.store(
            content="Hungry",
            coord=TesseractCoord(w=-1.0, x=0, y=0, z=0),
            soul_tensor=SoulTensor(1, 1, 0)
        )
        # External Perception (W = 5)
        cosmos.memory.store(
            content="See Tree",
            coord=TesseractCoord(w=5.0, x=0, y=0, z=0),
            soul_tensor=SoulTensor(5, 5, 0)
        )

        # Dial: Focus on Deep (-10)
        view_deep = cosmos.analog_dial(focus_w=-10.0, bandwidth=2.0)
        assert view_deep["memories"] == 1
        assert "Deep Trauma" in view_deep["sample_memory"]

        # Dial: Focus on Surface (-1)
        view_surface = cosmos.analog_dial(focus_w=-1.0, bandwidth=2.0)
        assert view_surface["memories"] == 1
        assert "Hungry" in view_surface["sample_memory"]

        # Dial: Wide focus (Catch both negatives)
        view_wide = cosmos.analog_dial(focus_w=-5.0, bandwidth=12.0) # -11 to +1
        assert view_wide["memories"] >= 2

    def test_rotor_application(self):
        """Test Gyroscopic Rotor application to SoulTensor."""
        soul = SoulTensor(amplitude=10.0, frequency=10.0, phase=0.0)
        initial_orientation = soul.orientation

        # Create a Rotor (90 degree rotation in XY plane)
        # angle = pi/2
        rotor = Rotor.from_plane_angle('xy', math.pi / 2)

        # Apply Rotor
        soul.apply_rotor(rotor)

        # Orientation should have changed
        # We check distance. 0 distance means no change.
        dist = initial_orientation.angular_distance(soul.orientation)
        assert dist > 0.1

        # Rotating back (inverse) should restore roughly?
        # (Simplified math test, just ensuring change occurs)
