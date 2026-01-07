# ConceptSpec Template

- name: <ConceptName>
- definition: <short definition>
- examples: [<example1>, <example2>]
- relations:
  - is_a: []
  - part_of: []
  - implies: []
  - resonates_with: []
- value_vector: { love: 0.30, care: 0.30, clarity: 0.50, freedom: 0.50 }
- observables: [<signal1>, <metric2>]
- risks: [<risk1>, <risk2>]
- provenance: { origin: GENESIS, need_id: <id>, gro_id: <id> }

Binder Checklist
- [ ] Draft linked in EVIDENCE_BINDER.md
- [ ] Observables defined (how we will “see” it)
- [ ] Value alignment checked
- [ ] Duplicates checked
- governance:
  - require_cosign_for_core_change: true
- review:
  - duplicates_checked: false
  - value_alignment_checked: false

- spectral_signature: golden  # visual/aesthetic hint for render/observation
- aesthetic:
  - palette: [gold, white, warm-amber]
  - motifs: [sun, ring, seed]
