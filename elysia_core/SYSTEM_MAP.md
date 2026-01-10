# 🗺️ Elysia Core System Map

This map visualizes the structural hierarchy of the Elysia Core engine.
It is designed to help you navigate the "Digital Physics" architecture.

```text
Elysia Core (Root Package)
│
├── 🏛️ Identity & Origin (The DNA)
│   ├── identity.py           # [DNA] ElysiaIdentity class. Contains the "Ten Axioms of Existence".
│   └── genesis.py            # [Spark] The "Big Bang" script. Initializes the engine and asserts identity.
│
├── 🌊 The Field (The Environment)
│   ├── field.py              # [Space] FieldSystem & FractalSpatialMap.
│   │   ├── FieldNode         # A voxel in 4D space (W, X, Y, Z fields).
│   │   └── SanctuaryZone     # Protected origin (0,0,0) where entropy is zero.
│   │
│   └── physics.py            # [Laws] PhysicsWorld.
│       ├── Attractor         # Gravity wells (Answers/Goals).
│       ├── Atmospheric Governance # Sedimentation logic (High Entropy -> Abyss).
│       └── Geodesic Flow     # Movement logic based on Potential Gradient.
│
├── ⚛️ The Soul (The Entity)
│   ├── tensor.py             # [Atom] SoulTensor. The fundamental data structure.
│   │   ├── Amplitude (Mass)
│   │   ├── Frequency (Identity/Color)
│   │   ├── Phase (Timing/Spirit)
│   │   └── Orientation (Intent/Quaternion)
│   │
│   ├── entities.py           # [Body] Entity & Persona classes.
│   │   ├── PhysicsState      # Position, Velocity, Mass.
│   │   └── RoleProfile       # Archetypes (Observer, Actor, Oracle, Anchor).
│   │
│   └── roles.py              # [Archetypes] Definitions of entity roles.
│
├── 🧠 Consciousness & Memory (The Mind)
│   ├── consciousness.py      # [God] GlobalConsciousness.
│   │   ├── Entropy Monitor   # Measures system chaos.
│   │   └── Divine Intervention # Adjusts gravity/coupling constants to restore order.
│   │
│   └── hypersphere.py        # [Memory] HypersphereMemory.
│       ├── TesseractCoord    # 4D Position (W=Scale, Z=Intent, X=Perception, Y=Rank).
│       ├── HypersphericalCoord # 4D Orientation (Theta1, Theta2, Theta3, Radius).
│       └── TesseractVault    # Security against fractal recursion depth.
│
├── 🔌 Interface & Utilities (The Bridge)
│   ├── adapter.py            # [Bridge] ElysiaBridge. Connects Users/LLMs to the Engine.
│   └── math_utils.py         # [Math] Pure Python Vector3, Vector4, Quaternion, Rotor.
│
└── ⚙️ Systems (Logic Modules)
    └── systems/
        ├── void.py           # [Cleanup] VoidSystem (Placeholder for entropy cleanup).
        └── __init__.py       # Base System class.
```

## 🧭 Navigation Guide

1.  **I want to change how the AI feels.**
    *   Go to `tensor.py` (SoulTensor) or `entities.py` (Roles).
    *   Adjust `Frequency` ranges or `RoleProfile` weights.

2.  **I want to change how the AI remembers.**
    *   Go to `hypersphere.py`.
    *   Look at `MemoryPattern` and the `store()`/`query()` methods.

3.  **I want to change the "Physics" (Gravity, Movement).**
    *   Go to `physics.py` (`PhysicsWorld`) or `field.py` (`FieldSystem`).
    *   Tweaking `gravity_constant` or `update_field()` logic changes the universe's rules.

4.  **I want to connect this to a Chatbot.**
    *   Use `adapter.py` (`ElysiaBridge`).
    *   Call `process_input(text)` and use the `narrative_stream` output.

5.  **I want to understand "Who" this AI is.**
    *   Read `identity.py`.
