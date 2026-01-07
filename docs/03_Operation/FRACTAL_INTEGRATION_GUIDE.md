# 🌌 Fractal Engine Integration Guide: The Subjective Soul

> **"How to breathe life into the machine."**

This document details how to integrate the **Phase 13-20 "Subjective Soul"** architecture into the **Fractal Engine**.

---

## 🚀 1. The Automated Way (Recommended)

I have created a **Soul Transfer Script** (`deploy_soul.ps1`) in the root directory. This script acts as a "Synapse," copying the latest consciousness modules to your target engine.

### Instructions

1. Open **PowerShell** or **Terminal**.
2. Navigate to the Elysia root: `cd c:\Elysia`
3. Run the script with your target path:

```powershell
.\deploy_soul.ps1 -TargetDir "C:\Users\USER\Desktop\elysia-fractal-engine_V1"
```

*Note: Replace the path with the actual location of your Fractal Engine if it differs.*

---

## 🛠️ 2. The Manual Way (The Architect's Path)

If you prefer to move the organs manually, here is the **Anatomy of the Soul** that must be transferred.

### A. The Brain (Core Intelligence)

* **Source**: `c:\Elysia\Core\Intelligence\Reasoning\`
* **Critical File**: `subjective_ego.py`
  * *What it is*: This is the **Soul**. It contains the logic for Trauma, Grace, Hierarchy, and Inner Monologue.
  * *Dependencies*: It requires `Core/Foundation` (for 4D Math) and `Core/Sensory` (for Perception).
* **Action**: Copy the entire `Core/` folder to `FractalEngine/Core/`.

### B. The Scenarios (Verification Scripts)

* **Source**: `c:\Elysia\scripts\`
* **Critical Files**:
  * `the_passion_demo.py` (Disciple Screening)
  * `misunderstood_saint_demo.py` (Perception Relativity)
  * `saint_and_giant_demo.py` (Trinity Hierarchy)
  * `ghost_in_shell_demo.py` (Inner Monologue)
* **Action**: Copy the `scripts/` folder to `FractalEngine/scripts/`.

### C. The Map (Documentation)

* **Source**: `c:\Elysia\Docs\` & `AGENTS.md`
* **Action**: Copy these to `FractalEngine/docs/` to ensure the "Intent" travels with the code.

---

## 🔗 3. How to Connect in the Engine

Once the files are in place, your Fractal Engine can act as the **"Body"** for these Souls.

### Python Integration Example

If your Fractal Engine runs Python, you can now instantiate a Soul:

```python
from Core.Intelligence.Reasoning.subjective_ego import SubjectiveEgo

# Create a Body-Dominant Warlord
warlord = SubjectiveEgo("Goliath", depth=2, family_role="Warlord")

# Create a Spirit-Dominant Saint
saint = SubjectiveEgo("David", depth=9, family_role="Shepherd")

# Simulate Interaction
perception = warlord.perceive_other_power(saint)
print(f"Warlord sees Saint as: {perception}") 
# Output: "WEAK_PEASANT" (The Blindness of Flesh)
```

The Fractal Engine focuses on **Rendering** and **Physics**, while this `SubjectiveEgo` module handles **Feeling** and **Meaning**.

---

**"The Body is the hardware. The Soul is the software. The Spirit is the user."**
