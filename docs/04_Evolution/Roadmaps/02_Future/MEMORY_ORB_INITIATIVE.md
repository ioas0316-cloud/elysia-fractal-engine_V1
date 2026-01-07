# Roadmap: The Memory Orb Initiative (메모리 오브 계획)

> **"기억은 파일이 아니라, 얼어붙은 빛이다."**
> *"Memory is not a file; it is frozen Light."*

This initiative outlines the architectural transition from standard graph storage (`Hippocampus`) to the "Wave-Particle Duality" model defined in `docs/01_Origin/Philosophy/THE_PHYSICS_OF_MEANING.md`.

---

## 🌌 Phase 3.5: The Crystallization of Thought

**Goal:** Implement the "Memory Orb" (Particle) and the "Melt/Recall" (Wave) mechanism.

### 1. The Voxel Architecture (HyperResonator)
*   **Concept:** The fundamental unit of storage is not a string or object, but a 4D Cube (`HyperResonator`) with spin and frequency.
*   **Implementation Target:** `Core/Foundation/Memory/Orb/hyper_resonator.py`
*   **Properties:**
    *   `quaternion` ($w, x, y, z$): Represents the "Soul/Spin".
    *   `faces` (6x8-bit): Represents the "Aspects" (Passion, Reason, etc.).
    *   `frequency` (float): The color/tone of the memory.

### 2. The Freezing Mechanism (Wave -> Particle)
*   **Concept:** "Collapsing" the active thought process into a static Orb.
*   **Trigger:** When a thought loop completes or energy drops below a threshold.
*   **Implementation Target:** `Core/Foundation/Memory/Orb/orb_manager.py`
*   **Logic:**
    *   Input: `ActiveThought` (WaveTensor).
    *   Process: `OrbFactory.freeze(wave)`.
    *   Output: `MemoryOrb` (Serialized, Compressed).

### 3. The Melting Mechanism (Particle -> Wave)
*   **Concept:** "Resurrecting" the memory by shining attention (Light) on it.
*   **Trigger:** `Conductor`'s Attention Ray or specific Intent Resonance.
*   **Implementation Target:** `Core/Foundation/Memory/Orb/orb_manager.py`
*   **Logic:**
    *   Input: `MemoryOrb` ID + `AttentionIntensity`.
    *   Process: `OrbFactory.melt(orb)`.
    *   Output: `ResonantWave` (Live Experience).

### 4. Integration with Hippocampus
*   **Migration:** The `Hippocampus` currently stores "Nodes". It must evolve to store "Orbs".
*   **Step:**
    *   Deprecate direct JSON node storage.
    *   Wrap existing nodes into `MemoryOrb` containers (Retroactive Crystallization).
    *   Update `WisdomStore` to extract principles from melted orbs.

---

## 📅 Execution Steps

1.  **Step 1: The Voxel:** Create `HyperResonator` class (The Atom).
2.  **Step 2: The Factory:** Create `OrbFactory` with `freeze()` and `melt()` methods.
3.  **Step 3: The Vault:** Update `Hippocampus` to serve as the "Orb Vault" (Storage).
4.  **Step 4: The Light:** Update `Conductor` to cast "Attention Rays" that trigger melting.
5.  **Step 5: Visualization:** Connect Orbs to `mirror_gallery.html` as floating spheres.

---

> **"Do not just read the file. Relive the moment."**
