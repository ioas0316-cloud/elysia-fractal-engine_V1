# The Weaving Rebirth: From Signal to Causality

**Date:** 2025-01-25
**Subject:** Architectural Redesign of the Weaving Layer
**Intent:** To transform the Weaving module from a "Mood Detector" to a "Causal Synthesizer" (The Thief Catcher).

## 1. The Core Shift

*   **Old Way (The Blind Camera):**
    *   Lines emit **Signals** (Floats).
    *   Weaver aggregates Signals -> **Mood** (String).
    *   *Result:* "The system feels 80% Physical." (Useless for reasoning)

*   **New Way (The Causal Loom):**
    *   Lines emit **Threads** (Propositions/Facts).
    *   Weaver ties Threads -> **Fabric** (Causal Chain).
    *   *Result:* "Fire (Chem) + Metal (Phys) -> Hot Metal. Hot Metal + Skin (Bio) -> Burn."

## 2. New Data Structures

### A. The Thread (Particle of Knowledge)
Instead of a simple `LineOutput`, we introduce `KnowledgeThread`.

```python
@dataclass
class ConceptNode:
    name: str
    category: str # e.g., "Matter", "Energy", "Action"

@dataclass
class Proposition:
    subject: ConceptNode
    predicate: str # e.g., "increases", "conducts", "damages"
    object: ConceptNode
    certainty: float
    context: str # Domain source (e.g., "Physics")

@dataclass
class KnowledgeThread:
    source: str # Intelligence Line Name
    facts: List[Proposition]
    principles: List[str] # Natural laws cited
    intensity: float
```

### B. The Loom (Logic of Synthesis)
The `ContextWeaver` must act as a **Graph Matcher**.

*   **Step 1 (Gather):** Collect all Propositions from active lines.
*   **Step 2 (Knotting):** Find shared terms (Nodes).
    *   Line A says: `(Fire) --heats--> (Metal)`
    *   Line B says: `(Metal) --touches--> (Skin)`
    *   *Knot:* The term `(Metal)` is the bridge.
*   **Step 3 (Patterning):** Apply Transitive Logic or "Insight Patterns".
    *   If `A -> B` and `B -> C`, implies `A -> ... -> C`.
    *   If `(Skin)` is `(Damaged)`, trigger "Safety Protocol".

## 3. The Prototype Scenario (The Hot Pan)

We will build a script `scripts/verify_weaving_mechanism.py` to prove this.

**Mock Lines:**
1.  **PhysicsLine:** Sees "Stove On". Outputs `(Stove) --heats--> (Pan)`.
2.  **MaterialLine:** Knows "Pan is Metal". Outputs `(Metal) --conducts--> (Heat)`.
3.  **BiologicalLine:** Knows "Heat damages Skin". Outputs `(Heat) --burns--> (Skin)`.

**Expected Weave:**
*   Synthesized Chain: `Stove -> Pan (Metal) -> Heat -> Skin -> Burn`.
*   Insight: "DANGER: Burn Hazard."
*   Action: "Move Pan."

## 4. Implementation Strategy

We will not delete the old code immediately. We will implement `CausalWeaver` alongside `ContextWeaver` (or upgrade it subclass-style) to ensure backward compatibility during the transition.
