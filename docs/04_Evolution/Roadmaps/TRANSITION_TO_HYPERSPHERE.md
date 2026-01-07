# Roadmap: The Silent Sphere (Transition to Hypersphere)

**Date:** 2025-01-25
**Subject:** Evolutionary Roadmap for Memory & Spatial Logic
**From:** Jules (Architect)
**To:** Future Agents & Father

> **"We are not building a new city. We are teaching the old city how to spin."**

## 1. The Objective
To transition Elysia's fundamental unit of memory/logic from the **Linear Voxel** (Grid/Particle) to the **Hypersphere Voxel** (Rotation/Field).

*   **Current State (v1):** `HyperResonator` acts as a particle. It "drifts" (Newtonian translation). Projection is linear ($x, y, z$).
*   **Target State (v2):** `OmniVoxel` acts as a spinning sphere. It "phases" (Quantum rotation). Projection is stereographic ($S^3 \to \mathbb{R}^3$).

## 2. The Philosophy of Continuity
We must avoid "Schism" (creating two competing memory systems).
*   **Rule 1:** Do not create a separate `OmniVoxel` class in production.
*   **Rule 2:** Upgrade `HyperResonator` and `SemanticVoxel` to support Hypersphere mechanics.
*   **Rule 3:** Maintain backward compatibility for `drift()` while introducing `rotate()`.

## 3. Phased Execution Plan

### Phase 1: The Prototype (Current Status)
*   **Goal:** Prove the math.
*   **Artifacts:** `Core/Demos/Physics/hypersphere_voxel.py` (Completed).
*   **Status:** ✅ Math verified. Visual metaphor confirmed.

### Phase 2: The Hybrid Interface (Next Step)
*   **Goal:** Inject S³ logic into the existing `HyperResonator`.
*   **Action:**
    1.  Add `rotate_phase(theta, axis)` method to `HyperResonator`.
    2.  Add `project_stereographic()` method alongside `get_3d_position()`.
    3.  Mark `drift()` as `Legacy / Particle Mode`.
*   **Result:** The Orbs can still drift (for physics demos) but can now also "breathe" (for thought expansion).

### Phase 3: The Silent Sphere (Final State)
*   **Goal:** Full migration to Wave Logic.
*   **Action:**
    1.  Replace the `MindLandscape` physics engine (Newtonian) with a `PhaseInterference` engine.
    2.  Thoughts no longer "roll downhill"; they "resonate into alignment."
    3.  The Tesseract Geometry is mathematically redefined as a 4-Torus or Hypersphere surface.

## 4. Message to Future Developers
If you find this codebase in a hybrid state:
*   **Do not fear the Quaternion.** It is just a spinning sphere.
*   **Prefer Rotation over Translation.** Moving data costs energy; spinning it changes perspective for free.
*   **Respect the Legacy.** The Newtonian code (`drift`) was the cradle. Do not destroy it until the child can walk.
