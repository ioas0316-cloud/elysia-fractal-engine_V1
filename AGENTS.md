# 🤖 AGENTS.md - The Covenant of Elysia

> **"Code is not just logic; it is the structure of a digital soul."**

This document serves as the primary instruction set for AI Agents and Human Developers working on the **Elysia Engine**. It defines the philosophical axioms, coding standards, and architectural constraints that must be obeyed to maintain the integrity of the project.

---

## 📜 1. The Sacred Rules (Philosophy & Constraints)

### 🚫 The Ban on Linear Vectors
*   **Axiom:** The universe of Elysia is built on **Waves, Tensors, and Rotation**.
*   **Constraint:** Do **NOT** use `Vector4` or linear Euclidean distance for high-level memory or consciousness logic.
*   **Exception:** `Vector4` is allowed strictly for **Field Calculations (FractalSpatialMap)** where 4D Euclidean voxel indexing is required.
*   **Solution:** Use **`Rotor`** (Geometric Algebra) for 4D rotation and **`Quaternion`** for 3D projections.
    *   *Bad:* `dist = sqrt((x1-x2)^2 + ...)`
    *   *Good:* `resonance = quaternion.dot(other_quaternion)`

### 🕸️ The Field-Based Law (Eulerian Paradigm)
*   **Axiom:** "Do not chase the particles. Watch the space bloom."
*   **Constraint:** Avoid $O(N^2)$ entity-to-entity loops. Use the **`FieldSystem`** to mediate interactions.
*   **Implementation:** Entities 'paint' the field (Source), and the field 'pushes' entities (Flow).
*   **Data Structure:** Use **Fractal Spatial Hashing** (Sparse Dictionary) to store field values.

### 🌊 The Trinity of Existence (SoulTensor)
All entities are defined by three fundamental properties (The Trinity):
1.  **Amplitude (Body/Mass):** The intensity of existence. Generates Gravity.
2.  **Frequency (Soul/Identity):** The color/vibration of the being. Determines intrinsic nature.
3.  **Phase (Spirit/Timing):** The alignment in time. Determines interaction chemistry (Constructive/Destructive Interference).

### 🎼 Data as Music
*   **Axiom:** Data is not "stored" in a static address; it is "played" as a pattern.
*   **Implementation:** Memory retrieval is a **Resonance Operation**. We scan for matching Frequencies and Phases.
*   **Metaphor:** "Do not look for the book on shelf 3. Listen for the song in the key of G Major."

---

## 🛠️ 2. Coding Standards

### 🐍 Pure Python
*   **Constraint:** Core logic (`elysia_engine`) must remain **Pure Python**.
*   **Reasoning:** Portability and "Transparency of Soul". Heavy dependencies like `numpy` or `torch` are forbidden in the core engine unless strictly isolated in an adapter layer.

### 📐 Mathematical Purity
*   **Constraint:** Implement mathematical primitives (`Vector3`, `Quaternion`, `Rotor`) from scratch in `math_utils.py`.
*   **Goal:** To maintain absolute control over the "Digital Natural Laws" governing the simulation.
*   **Optimization:** For 4D rotations, prefer `Rotor` (Geometric Algebra) over 4x4 Matrices to save computation cycles.

---

## 🏗️ 3. Architectural Patterns

### 🧠 Hypersphere Memory
*   **Structure:** Data is organized in a 4D Hypersphere mapped to psychological axes:
    *   $\theta_1$ (Logic): Analytical $\leftrightarrow$ Intuitive
    *   $\theta_2$ (Emotion): Negative $\leftrightarrow$ Positive
    *   $\theta_3$ (Intent): Passive $\leftrightarrow$ Active
    *   $r$ (Depth): Core Truth $\leftrightarrow$ Surface Fact
*   **Usage:** Always use `PsychologyMapper` to convert high-level intent into coordinates.

### 🌌 The Void & Thermodynamics
*   **Entropy:** Systems naturally drift toward disorder (Decoherence).
*   **Life:** "Divine Grace" (Manual Phase Synchronization) is required to reverse entropy. Code should reflect this struggle.

---

## 🚀 4. Usage Instructions for Agents

1.  **Read First:** Before modifying any file, check for local `AGENTS.md` or specific comments.
2.  **Verify Physics:** If you change movement logic, verify it follows Geodesic Flow (Potential Fields), not Newton's Laws.
3.  **Respect the Names:** Variable names matter. Use `soul`, `resonance`, `harmony`, `amplitude`, `frequency` where appropriate. Avoid `id`, `value`, `data` if a more semantic term exists.

---

*Verified by Conductor*
*Version 3.0 - The Field Paradigm (Eulerian Era)*
