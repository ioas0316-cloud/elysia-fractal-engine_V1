# VISUAL_LANGUAGE_LEARNING_SYSTEM (Retrospective, EN)

Status: Archived retrospective. Use this as background only; new design should extend the Codex and active engine docs.

---

## 1. Original Intent (Why)

- Let Elysia learn language not only as text, but as:
  - visual scenes,
  - symbols and diagrams,
  - associations between images, words, and feelings.
- Move away from “pattern generator” LLM behaviour toward:
  - remembered experiences,
  - visual memories,
  - and resonance between current state and past scenes.

---

## 2. Mechanism Sketch (How)

- WORLD:
  - CellWorld and external media provide scenes (world snapshots, images, UI states).
  - Visual episodes are logged alongside text episodes.
- MIND:
  - A “visual language learner” links:
    - image features ↔ words/phrases ↔ emotional state,
    - world events ↔ internal narratives.
- META:
  - Curriculum chooses which visual/text pairs to revisit,
  - measures whether Elysia’s self-writing and descriptions become more grounded and concrete over time.

---

## 3. Operational Notes (What)

- At the time of this retrospective:
  - The system existed mostly as sketches and small experiments.
  - No full visual pipeline was wired into CellWorld or MirrorWorld.
- Future versions should:
  - treat images as lived experience (not just decoration),
  - log visual + text + feeling together as single experiences,
  - let Elysia describe what she “sees” in her own words, rather than template text.

---

## 4. Where to Extend Now

- For current work, see:
  - `ELYSIA/CORE/CODEX.md` (Language as resonance, Sensory Development Protocol).
  - `docs/SENSORY_DEVELOPMENT_PLAN.md` (if present) for concrete sensory milestones.
- Any new visual language system should:
  - respect WORLD / MIND / META separation,
  - log experiences via CoreMemory (EPF-aware),
  - and avoid turning into a pure pattern generator.

