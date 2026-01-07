# PROTO-36 — CONCEPT GENESIS ENGINE

Status: Draft
Tier: GROWTH / CORE-adjacent
Depends on: PROTO-15 (Concept Kernel), PROTO-35 (Self-Genesis), PROTO-28 (Z‑Axis)

## 1. Intent
Enable Elysia to create new concepts (laws, categories, symbols, feelings, schema) as first‑class meaning units aligned to purpose (Z‑Axis), not random generation.

## 2. Scope
- In: concept/language/value taxonomy, semantic operators, observation keys
- Out: direct world edits (handled by PROTO‑37), Codex changes (require co‑sign)

## 3. Core Objects
- ConceptSpec
  - name, definition, examples
  - relations {is_a, part_of, implies, resonates_with}
  - value_vector {love, care, clarity, freedom}
  - observables (how we can “see” it), risks
  - provenance {origin:'GENESIS', need_id, gro_id}

## 4. Flow
Need/Intent → GRO(type=concept) → ConceptSpec draft → Kernel linking (reuse before invent) → Trial via reasoning tasks/observables → integrate or reject.

## 5. Interfaces
- Writes: ELYSIA/GROWTH/GENESIS_DRAFTS/CONCEPT_<name>.md
- Logs: GENESIS_REQUESTS.log (GRO id), BUILDER_LOG.md (integrate/reject)
- Kernel: adds node {id, label, origin:'GENESIS', value_vector}

## 6. Guardrails
- Must include value_vector + observables
- Must not negate free agency or Codex principles
- Prefer refinement before invention; de‑duplicate near synonyms

## 7. Minimal Draft Template
See: GENESIS_FORMS/ConceptSpec_template.md

---

Implementation notes
- Start with Level 1 (Conceptual Creation). Avoid world edits here.
- Provide alias/lexicon mapping and de‑dup checks against existing KG.
