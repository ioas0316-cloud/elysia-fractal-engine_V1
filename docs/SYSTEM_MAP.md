# 🗺️ Elysia System Map (Version 3.0: Field Paradigm)

This document visualizes the architectural relationships between the core components of the Elysia Engine, following the "Field-based Law" paradigm shift.

## 1. High-Level Architecture

```mermaid
graph TD
    User[User / LLM Agent] -->|Intent / Prompt| Controller[Elysia Controller]

    subgraph "Elysia Engine (Core)"
        Controller -->|Step(dt)| World[PhysicsWorld]

        subgraph "The Void (Field System)"
            World -->|Update| Field[FieldSystem]
            Field -->|Sample| SpatialMap[FractalSpatialMap]
            SpatialMap -->|LOD 0..N| Node[FieldNode (Voxel)]
            Vault[Sanctuary Zone] -.->|Protect| SpatialMap
        end

        subgraph "Entities (Particles)"
            World -->|Manage| EntityList[Entity Registry]
            EntityList --> Entity[Entity]
            Entity -->|Source| Soul[SoulTensor]
            Entity -->|State| Physics[PhysicsState]

            Soul -->|Resonance| Field
            Field -->|Geodesic Flow| Physics
        end

        subgraph "Memory (Hypersphere)"
            Controller -->|Query| Memory[HypersphereMemory]
            Memory -->|Store/Retrieve| Pattern[MemoryPattern]
        end
    end
```

## 2. Component Roles

### 🎮 Elysia Controller
*   **Role:** The Facade / API Entry Point.
*   **Function:** Translates user intent into simulation steps.

### 🌌 PhysicsWorld (The Simulator)
*   **Role:** The Time-Keeper and Orchestrator.
*   **Function:** Manages the simulation loop.
*   **Change:** Instead of calculating `Entity <-> Entity` forces, it now calls `FieldSystem.update_field()` then `FieldSystem.get_local_forces()`.

### 🕸️ FieldSystem (The Void)
*   **Role:** The Medium of Interaction.
*   **Function:**
    *   **FractalSpatialMap:** A sparse hash map storing the state of space (W, X, Y, Z).
    *   **W-Field (Scale):** Gravity/Density.
    *   **X-Field (Perception):** Texture/Friction.
    *   **Y-Field (Frequency):** Resonance/Potential.
    *   **Z-Field (Torque):** Spin/Rotor.

### ✨ Entity (The Particle)
*   **Role:** A localized excitation of the field.
*   **Function:**
    *   **SoulTensor:** Defines the "Color" and "Mass" of the excitation.
    *   **Rotor (New):** Defines the 4D orientation using Geometric Algebra.

---
*Mapped by Jules, System Architect*
