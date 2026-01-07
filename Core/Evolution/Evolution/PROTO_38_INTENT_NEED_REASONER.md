# PROTO-38 — INTENT / NEED REASONER

Status: Draft
Tier: GROWTH / CORE-adjacent
Depends on: PROTO-28 (Z‑Axis), PROTO-20 (Insight), PROTO-35 (Self‑Genesis)

## 1. Intent
Continuously surface “what I want and why” as structured Need Signals to start Genesis flows, turning friction/curiosity into GRO drafts.

## 2. Signals
- friction_score: repeated failure or opacity
- curiosity_score: pull toward exploration
- value_alignment: Codex alignment estimate
- observability_gap: missing lenses/metrics to see a phenomenon

## 3. Outputs
- Need Statement (append to GENESIS_NEEDS_LOG.md)
- GRO skeleton (append to GENESIS_REQUESTS.log)
- priority hint (L/M/H) and suggested authority level

## 4. Flow
Telemetry/reflect → compute signals → format Need Statement → draft GRO (type: concept/system/world) → hand to PROTO‑35.

## 5. Guardrails
- Never auto‑integrate; this module only proposes
- Ask‑to‑act when confidence low or values conflict
- Keep causality notes to explain why a need emerged
