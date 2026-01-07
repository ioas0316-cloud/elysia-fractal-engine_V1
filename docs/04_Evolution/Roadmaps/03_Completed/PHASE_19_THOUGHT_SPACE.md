# Phase 19: The Thought Space (Active vs Passive)

## The Philosophy
>
> "Activation of all concepts is meaningless. The Thought Universe (Active) and Knowledge Graph (Passive) must be distinct."
> "Elysia's Intent/Context should drive what is pulled from the Graph."

## The Architecture

### 1. The Passive Library (`TorchGraph`)

- **Role**: Deep Storage, Association, Gravity.
- **State**: Passive. Contains 35,000 nodes.
- **Function**: `get_subgraph(context_vector)` -> Returns relevant nodes.

### 2. The Active Workspace (`ThoughtSpace`)

- **Role**: Working Memory, Reasoning, Imagination.
- **State**: Dynamic. Contains 5-10 active "Thought Forms".
- **Structure**:

    ```python
    class ThoughtSpace:
        def __init__(self):
            self.active_thoughts = [] # [Thought("Git"), Thought("Quantum")]
            self.focus_vector = None # Current intent
    ```

### 3. The Retrieval Mechanism (The Lens)

- **Pulse**: Instead of "Global Resonance", we use "Focused Pulse".
- **Logic**:
    1. **Intent**: Elysia asks "Why is this code conflicting?"
    2. **Focus**: Vector = `Vector("Code") + Vector("Conflict")`
    3. **Retrieval**: `TorchGraph.query(vector, k=3)` -> Returns `Quantum_Superposition`.
    4. **Internalization**: `Quantum_Superposition` is copied into `ThoughtSpace` as a Metaphor.

## Implementation Steps

### Step 1: Define `ThoughtSpace`

- Create `Core/Cognition/thought_space.py`.
- Implement `ActiveThought` class (content, vector, resonance).

### Step 2: Implement Contextual Retrieval

- Modify `TorchGraph` to support `context_query(vector)`.
- Ensure it returns *Rich Content* (Payload), not just IDs.

### Step 3: The "Think" Loop

- Create `script/simulate_thought_process.py`:
  - Context: "I want to explain Merge Conflicts."
  - Action: Pull "Physics/Superposition" from Graph.
  - Result: `ThoughtSpace` contains both. Bridging happens *here*, not in the global graph.

## Success Metric

- Elysia does NOT activate the whole brain.
- She activates ONLY what is relevant to the "Context".
- "Efficiency of Thought" > "Volume of Activation".
