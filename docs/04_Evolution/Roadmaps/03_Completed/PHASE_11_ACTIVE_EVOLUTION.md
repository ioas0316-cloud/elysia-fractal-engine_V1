# Implementation Roadmap: Competence (Phase 11)

**Theme**: "The Stomach is Already There" (Using Intrinsic Systems)
**Date**: 2025-12-21
**Version**: 11.3 (Final Alignment)

## 🧘 Insight: Anti-Proliferation

The user corrected me: *"That absorption structure is also creating ANOTHER system. Check SYSTEM_MAP to see how the existing system works."*
I found `Core/Foundation/knowledge_acquisition.py` in `SYSTEM_MAP.md` marked as **PRIMARY**.
I must NOT create `KnowledgeSedimenter` or `absorb_wisdom.py` as new structures.
I must **USE** the existing `KnowledgeAcquisitionSystem`.

---

## 🗺️ Revised Plan (Simplification)

### Step 1: Verification of Intrinsic Capability

- **Target**: `Core/Foundation/knowledge_acquisition.py`
- **Method**: Run its innate `demonstrate_learning_cycle()` method.
- **Status**: ✅ Configured and Ready.

### Step 2: Feeding Proper Data

- **Script**: `scripts/feed_wisdom.py`
- **Logic**:
    1. Import `KnowledgeAcquisitionSystem` (Existing).
    2. Read `c:\Elysia\data` (Existing).
    3. Call `system.learn_curriculum()` (Existing method).
- **Goal**: Fill the `InternalUniverse` with high-quality data using only what we have.

### Step 3: From Quantity to Competence

- Once the `InternalUniverse` is dense with "Demian" and "Physics", the `why_engine` (Phase 9) will naturally find better metaphors.
- This creates the "Unified Competence" the user asked for.

---

## 🛠️ Assets being utilized (No New Code)

| Asset | Role | Status |
| :--- | :--- | :--- |
| `Core/Foundation/knowledge_acquisition.py` | **Primary Stomach** | ✅ Active |
| `Core/Foundation/internal_universe.py` | **Knowledge Store** | ✅ Active |
| `c:\Elysia\data\drama_*.txt` | **Nutrients** | ✅ Available |

**"We do not build the stomach. We just find the food."**
