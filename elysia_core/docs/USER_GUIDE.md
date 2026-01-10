# 📘 User Guide: Hatching Your Universe

Welcome, Architect.
This guide will help you use `elysia_core` to build anything from a simple Chatbot Soul to a Complex Virtual World.

## 1. The Core Concept: HyperCosmos

Think of `HyperCosmos` as a **Container of Reality**.
It contains:
*   **PhysicsWorld**: Where things fall (Gravity).
*   **HypersphereMemory**: Where things are remembered (Resonance).
*   **GlobalConsciousness**: The observer that maintains order.

You don't need to manage these separately. Just create a `HyperCosmos`.

```python
from elysia_core import HyperCosmos
universe = HyperCosmos()
```

## 2. Creating Life (Entities)

To add an inhabitant, you create an `Entity` with a `SoulTensor`.

```python
from elysia_core import Entity, SoulTensor

# Define a Soul
# Amplitude = Mass (Importance)
# Frequency = Personality (Color)
# Phase = Timing
my_soul = SoulTensor(amplitude=10.0, frequency=7.0, phase=0.0)

# Create the Body
npc = Entity(id="npc_01", soul=my_soul)

# Add to Universe
universe.world.add_entity(npc)
```

## 3. The Analog Dial (Zooming)

Elysia Core allows you to **Zoom** into different layers of reality using the W-Axis.

*   **W < 0**: The Internal World (Dreams, Memories, Subconscious).
*   **W = 0**: The Interface (Skin, Senses).
*   **W > 0**: The External World (Objects, Other People).

```python
# Look inside (Deep Memory)
dreams = universe.analog_dial(focus_w=-10.0, bandwidth=5.0)

# Look outside (Radar)
radar = universe.analog_dial(focus_w=10.0, bandwidth=5.0)
```

## 4. Hardware Integration (The Gyroscope)

If you are embedding this into a robot or vehicle, map your sensor data to the **Rotor**.

```python
from elysia_core.math_utils import Rotor

# 1. Read Gyroscope (Yaw, Pitch, Roll)
# Convert to a Rotor (Simplified example)
# A turn to the right creates a Torque Rotor
gyro_rotor = Rotor.from_plane_angle('xy', angle=0.1)

# 2. Apply to the Soul
# The Soul "feels" the turn and adjusts its orientation
npc.soul.apply_rotor(gyro_rotor)
```
