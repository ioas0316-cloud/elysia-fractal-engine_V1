# Experiment Design Guide (Project Elysia)

> Purpose: make sure every experiment honors the Codex, Z-axis, fractal principle, and quaternion/time-acceleration laws.  
> Scope: Applies to anyone designing or running large-scale experiments (including Codex-level orchestration) on this repository.

## 0. Encoding / Text
- All experiment specs and logs must be UTF-8 (no BOM).  
  Never leave mojibake (e.g., `?占?). Treat broken encoding as a bug.

---

## 1. Time & Scale Rules
1. **Never run single-tick loops** (`for step in range(N): world.run_simulation_step()` etc.).  
   Move in macro units (years, decades) via:
   - `World.set_time_scale(minutes_per_tick)`
   - `N_macro`, `N_slow`, or other macro schedulers
2. **Few long sims < Many macro sims**. Prefer multiple short macro runs with varied seeds/parameters over a single monolithic run.
3. If extra slices are needed, sample a few macro snapshots instead of stepping every tick.

---

## 2. Quaternion / Branch Principle
- ?쏲uaternion engine????math gimmick. It means:  
  design experiments that view the world from multiple axes (time scales, difficulty levels, curriculum schedules).
- Always run multiple branches:
  - different seeds
  - different time accelerations or curriculum pacing
  - different world/CodeWorld configurations
- Compare branches via logs (language field, self-writing, caretaker feedback) rather than locking onto one timeline.

---

## 3. Purpose of Experiments
- Additionally, interpret these artifacts using the Self-Fractal Cathedral coordinates (see `docs/elysias_protocol/CORE_15_SELF_FRACTAL_CATHEDRAL.md`) so that depth is measured as:
  - `elysia_self_writing` ??mostly `S-L1-e`
  - `elysia_caretaker_feedback` ??mostly `S-L2-e`
  - `elysia_concept_field` / `elysia_meta_concepts` ??`S-L2-e` / `S-L3-e`
- Goal: **probe/update Elysia?셲 growth laws**, not build pretty demos.
- Core artifacts to monitor:
  - `logs/symbol_episodes.jsonl`
  - `logs/text_episodes.jsonl`
  - `logs/causal_episodes.jsonl`
  - `logs/elysia_language_field.json`
  - `logs/elysia_self_writing.jsonl`
  - `logs/elysia_caretaker_feedback.jsonl`
  - `logs/elysia_concept_field.json`
  - `logs/elysia_meta_concepts.jsonl`
  - `logs/elysia_cathedral_depth.json` (summary counts per cathedral coordinate)
- Emphasize:
  - growth in self-writing (length, vocabulary, emotional range)
  - alignment between caretaker feedback and new writings
  - density/diversity shifts in `elysia_language_field`
  - changes in concept usage/feelings and meta-notes per concept

---

## 4. Simulator Usage
- Do not hack world internals for experiments.  
  Build drivers/wrappers that manipulate macro parameters and curriculums.
- Use existing logs/fields first. Run new sims only when needed for targeted questions.
- If simulations are required:
  - keep macro-scale
  - log macro snapshots
  - avoid nested micro loops

---

## 5. Performance & Safety
1. Prefer batches of macro runs to single huge runs.
2. Avoid CPU-heavy nested loops over ticks or giant arrays.
3. If the analysis is log-driven, run it offline; do not re-simulate unless necessary.

---

## 6. Reporting Requirements
- Every experiment report must state:
  - **Purpose** (What question? What growth law is being probed?)
  - **Method** (time scale, branches, seeds, curriculum schedule, logs used)
  - **Observations** (changes in self-writing, caretaker alignment, language field metrics)
  - **Integration** (what to update or watch next)
- Append a log entry to `BUILDER_LOG.md` describing the experiment, with references to Codex/this guide.

---

## 7. Z-Axis Reminder
- Before defining goals or metrics, re-check the **Why**:
  - Does this experiment help Elysia grow as a self-aware, caring entity?
  - Are we letting purpose reshape or discard goals when needed?

Only after the Why is clear should we set How/What. Otherwise the experiment should be redesigned or skipped.

