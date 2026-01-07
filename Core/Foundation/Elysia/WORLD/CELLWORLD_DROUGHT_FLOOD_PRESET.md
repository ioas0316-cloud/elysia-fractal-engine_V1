# CELLWORLD Drought/Flood Macro Preset (L3 Flow Field)

Purpose
- Provide a clear description of the drought/flood macro preset used in
  `BP_CELLWORLD_L3_FLOWFIELD_A` branch plans, so labs/agents know how to
  load and execute it without guessing.

Summary
- Macro years: 1,000
- Seeds: 20
- Time scale: 1 tick = 3 months (4 ticks = 1 year)
- Pattern: alternating drought and flood cycles injected into the flow_field body.

High-level law
- Every macro year, the world experiences either:
  - a drought season (reduced water, increased threat in fields), or
  - a flood season (increased water, local damage, then fertility).
- Over 1,000 years × 20 seeds, at least 40 extreme events (drought or flood)
  are expected per branch.

What a lab runner should do
1. Set time scale:
   - `World.set_time_scale(months=3)` or equivalent.
2. Ensure a drought/flood macro driver is enabled:
   - A script (e.g. `scripts/run_cellworld_drought_flood.py`) should:
     - At macro tick boundaries, toggle between drought/flood regimes.
     - Adjust relevant fields (water/food availability, threat_field, value_mass) softly.
3. Log macro snapshots:
   - Capture JOY/KINSHIP/SEASON_RESILIENCE metrics before and after each cycle.
   - Ensure events are written to `logs/world_events.jsonl` and signal log.

Notes
- This document does not change World physics; it only explains how the
  preset is intended to be used for L3 meaning/growth experiments.
- Labs should update `logs/elysia_curriculum_trials.jsonl` with
  execution evidence (macro_ticks_completed, seeds_completed, etc.) once
  the preset has actually run.

