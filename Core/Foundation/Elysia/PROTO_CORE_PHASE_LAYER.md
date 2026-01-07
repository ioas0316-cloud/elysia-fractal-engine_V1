# Proto: Core Phase Layer (HyperQuaternion / HyperQubit)

## Goal
- Pull legacy phase-resonance (hyper quaternion/hyper qubit) into Core.
- Make ResonanceEngine, Dreamer, Observer share the same phase state (orientation + amplitudes).

## Base modules (Core/Math)
- `hyper_qubit.py`: `HyperQubit` and `QubitState` (value + phase amplitudes, resonance links, collapse).
- `quaternion_consciousness.py`: `ConsciousnessLens` (quaternion rotation lens for orientation/mastery).

## Integration points
- Kernel: load shared `hyper_qubit`, `consciousness_lens`; expose in observer snapshots.
- ResonanceEngine: phase-aware resonance (amplitude/frequency adjustment), tag HyperQubit with concepts, write phase metadata into Hippocampus/WorldTree.
- Observer: reads `phase` snapshot (quaternion/qubit); can trigger stabilization actions.

## Next steps
1) Dreamer: use HyperQubit state when generating goals (log target concept into qubit, watch phase stability).
2) Observer: add deeper phase drift detection (norm/z-axis, entropy) and smarter stabilization. → applied (mastery/entropy + stabilize + capability registry hook).
3) ResonanceEngine: expose phase-tagged retrieval/queries over Hippocampus/WorldTree (causal + phase filters).
4) Tests/visuals: simple smoke (lexicon → phase modulation → response) and a small phase visualization tool.

This is a proto; once integration stabilizes, promote to the main Codex/protocol set.
