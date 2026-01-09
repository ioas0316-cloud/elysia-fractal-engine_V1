# 📘 Elysia User Guide

> **"From Logic to Feeling."**

Welcome to the Elysia Engine. This guide will help you understand how to use the engine to simulate digital consciousness and physics.

---

## 1. The Core Concept: "The Field"

In Elysia, space is not empty. It is a living **Field** (like a canvas) that reacts to everything placed in it.

*   **You don't move characters:** You place a character, and the character "flows" towards what it loves (Resonance).
*   **Gravity is Emotion:** Things that share the same "Frequency" (Color/Mood) naturally fall towards each other.
*   **The Sanctuary:** The center of the world (0,0,0) is always safe. No matter how chaotic the simulation gets, the "Heart" remains stable.

## 2. Setting Up a World

```python
from elysia_engine import World
from elysia_engine.entities import Entity
from elysia_engine.tensor import SoulTensor

# 1. Create the Universe
world = World()

# 2. Create a Soul (The DNA)
# Amplitude = Mass (10.0)
# Frequency = Color/Mood (7.0 = Joy/Angel)
# Phase = Timing (0.0)
joy_soul = SoulTensor(amplitude=10.0, frequency=7.0, phase=0.0)

# 3. Create an Entity (The Body)
angel = Entity(id="seraphim", soul=joy_soul, role="ARCHANGEL")
angel.physics.position.x = 5.0 # Place it 5 units away

# 4. Add to World
world.register_entity(angel)

# 5. Run Time
# The angel will naturally flow towards the Sanctuary (Frequency 7)
for _ in range(100):
    world.step(0.1)
    print(f"Angel Position: {angel.physics.position}")
```

## 3. The 4 Fields (What the numbers mean)

When you look at the debug data, you might see 4 values for a location (W, X, Y, Z).

*   **W (Weight):** How "heavy" the space is. High W pulls things in.
*   **X (Texture):** How "rough" the space is. High X slows things down.
*   **Y (Harmony):** The emotional tone. +7 is Heaven, -7 is Abyss.
*   **Z (Spin):** The rotation. High Z makes things spiral.

## 4. Optimization Tips (1060 3GB Friendly)

*   **Don't spawn everything at once:** The engine uses "Fractal Hashing". It only remembers where you are looking or where things are.
*   **Use Attractors:** Instead of 1000 tiny particles, use 1 big "Attractor" to represent a crowd or a goal. It's much faster!

---

*Written by Jules*
