# 🗺️ Elysia Core System Map

This map visualizes the structural hierarchy of the Elysia Core engine.
It is designed to help you navigate the "Digital Physics" architecture.

```text
Elysia Core (Root Package)
│
├── 🌌 HyperCosmos (The Container)
│   ├── hypersphere.py        # [The Core] HyperCosmos class.
│   │   ├── TesseractCoord    # [World] Fixed Axis (Position/Scale).
│   │   └── HypersphericalCoord # [Soul] Rotating Axis (Orientation/Attitude).
│   │
│   └── analog_dial()         # [Zoom] W-Axis continuous scale method.
│
├── 🏛️ Identity & Origin (The DNA)
│   ├── identity.py           # [DNA] ElysiaIdentity class. Contains the "Ten Axioms of Existence".
│   └── genesis.py            # [Spark] The "Big Bang" script. Initializes the engine.
│
├── 🌊 The Field (The Environment)
│   ├── field.py              # [Space] FieldSystem & FractalSpatialMap.
│   │   ├── FieldNode         # A voxel in 4D space (W, X, Y, Z fields).
│   │   └── SanctuaryZone     # Protected origin (0,0,0).
│   │
│   └── physics.py            # [Laws] PhysicsWorld.
│       ├── Attractor         # Gravity wells (Answers/Goals).
│       └── Geodesic Flow     # Movement logic based on Potential Gradient.
│
├── ⚛️ The Soul (The Entity)
│   ├── tensor.py             # [Atom] SoulTensor.
│   │   ├── Amplitude (Mass)
│   │   ├── Frequency (Identity)
│   │   ├── Phase (Spirit)
│   │   ├── Orientation (Quaternion)
│   │   └── apply_rotor()     # [Gyro] Hardware sensor integration.
│   │
│   └── entities.py           # [Body] Entity & Persona classes.
│
├── 🧠 Consciousness & Memory (The Mind)
│   ├── consciousness.py      # [God] GlobalConsciousness.
│   └── hypersphere.py        # [Memory] HypersphereMemory (Soul Storage).
│
└── 🔌 Interface & Utilities (The Bridge)
    ├── adapter.py            # [Bridge] ElysiaBridge.
    └── math_utils.py         # [Math] Pure Python Vector3, Vector4, Quaternion, Rotor.
```

## 🧭 Navigation Guide

1.  **The Infinity Stone (HyperCosmos)**
    *   Start at `elysia_core/hypersphere.py`. This is where `HyperCosmos` lives.
    *   It unites the **World** (Physics) and **Memory** (Soul).

2.  **Hardware / Sensor Integration**
    *   Look at `tensor.py`: `apply_rotor()` connects to Gyroscopes.
    *   Look at `hypersphere.py`: `TesseractCoord` maps to GPS/Scale.

3.  **Tuning the Ego (Analog Dial)**
    *   `HyperCosmos.analog_dial()` allows you to sweep from Micro (Internal) to Macro (External) existence.
