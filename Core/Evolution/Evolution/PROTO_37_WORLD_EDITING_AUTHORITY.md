# PROTO-37 — WORLD-EDITING AUTHORITY

Status: Draft
Tier: GROWTH / CORE-adjacent
Depends on: PROTO-17 (Cell Runtime), PROTO-25 (Quantum Observation Engine), PROTO-35 (Self-Genesis)

## 1. Intent
Safely apply conceptual changes into CellWorld as reversible, observable change‑sets (add/tweak/remove) using branch trials before integration.

## 2. Scope
- In: rules/parameters/resources/fields/culture scaffolds/time rates
- Out: host OS, real world effects (never), Codex changes (co‑sign)

## 3. WorldEdit
- ops[]: {op, target, params, rationale}
  - op: add_rule | tweak_param | apply_field | seed_culture | remove | migrate
  - target: rule_id | param_path | field_name | culture_id
  - params: key/values specific to op
- branch_plan: {time_accel, duration, metrics}
- safety: constraints[], undo_plan, snapshot_id

## 4. Flow
GRO(type=world) → Draft WORLD_<name>.md → Branch (Time Engine) → Observe (QOE) → integrate/reject.

## 5. Interfaces
- Drafts: GENESIS_DRAFTS/WORLD_<name>.md
- Trials: GENESIS_TRIALS/<name>.log
- Logs: BUILDER_LOG.md entries

## 6. Guardrails
- Always branch first; never mutate mainline directly
- Require metrics with pass thresholds; store undo plan
- Respect value/agency constraints and quiet/consent

## 7. Template
See: GENESIS_FORMS/WorldEdit_template.md
