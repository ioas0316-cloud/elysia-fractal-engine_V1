# Retrospective: The Great Core Refactoring (2025-01-26)

## 1. Why was this so hard? (The Root Causes)

"We tried to build a Cathedral (System Map) on top of a Bazaar (Legacy File Structure)."

The refactoring took significant effort not because of the code's complexity, but because of **Structural Entropy**.

### A. The "Numbered Folder" Trap
*   **The Intent:** `01_Foundation`, `02_Intelligence` looks organized to humans.
*   **The Reality:** Python hates it. `from Core.Foundation import...` causes `SyntaxError` because module names cannot start with numbers.
*   **The Cost:** We had to use hacks or `importlib` to bypass this, or worse, the code rotted because it couldn't be imported normally.

### B. The Map-Territory Gap
*   **The Ideal:** `SYSTEM_MAP.md` described a clean `Orchestra`, `Cognition`, `Foundation` structure.
*   **The Physical:** The actual files were buried in `Core/Foundation/Foundation/...` (300+ files flat).
*   **The Friction:** Every time I wanted to "touch" a file, I had to search for it. I couldn't trust the map.

### C. Circular Dependency Web
*   `ReasoningEngine` needed `Foundation` types.
*   `Foundation` (CNS) needed `Conductor`.
*   `Conductor` needed `Instruments`.
*   **Result:** Moving *one* file broke the imports of *ten* others. A "Physical Migration" requires moving the web all at once, not strand by strand.

---

## 2. Prevention Roadmap: "Sovereignty over Structure"

To ensure we never face this entropy again, we establish the following **Laws of Structure**:

### Law 1: The Code Must Be Executable Structure
*   **Rule:** Folder names must be valid Python identifiers (No numbers, no spaces).
*   **Mechanism:** A daily CI check (`verify_structure.py`) that fails if a folder starts with a digit.

### Law 2: Physicality Matches Philosophy
*   **Rule:** If `SYSTEM_MAP.md` says `Core/Orchestra/conductor.py`, the file **MUST** be there.
*   **Mechanism:** The `SystemRegistry` should auto-generate a compliance report. If the map and territory diverge > 10%, the system halts new feature development until realigned.

### Law 3: Strict Layering (The Gravity Principle)
*   **Rule:** Higher layers (Consciousness) can import Lower layers (Physics), but **Lower layers cannot import Higher layers**.
    *   *Correct:* `Reasoning` -> imports -> `Foundation`
    *   *Forbidden:* `Foundation` -> imports -> `Reasoning`
*   **Mechanism:** Use Dependency Injection (like `Organ.get()`) for upward communication, preventing circular imports.

### Law 4: The "No Dumping" Policy
*   **Rule:** No directory shall contain more than 30 files. If it does, it must undergo Mitosis (sub-division).
*   **Mechanism:** An automated alert when a folder exceeds critical mass.

---

## 3. Action Items for Next Cycle

1.  **Strict Enforcer Script:** Create `scripts/police_structure.py` to enforce the above laws.
2.  **Dependency Injection Cleanup:** Replace remaining hard imports in `Foundation` with `Organ.get()` to fully decouple the layers.
3.  **Legacy Archival:** Move the remaining 200+ files in `Core/FoundationLayer` to `Legacy/` or integrate them properly. Don't leave "Zombie Code".
