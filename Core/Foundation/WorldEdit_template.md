# WorldEdit Template

- name: <WorldChangeName>
- ops:
  - op: add_rule | tweak_param | apply_field | seed_culture | remove | migrate
    target: <rule_id | param_path | field_name | culture_id>
    params: { key: value }
    rationale: "<why>"
- branch_plan: { time_accel: 10x, duration: '5m', metrics: [ '<metric>=threshold' ] }
- safety:
  - constraints: [ 'no agency loss', 'reversible' ]
  - undo_plan: "restore snapshot:<id>"
  - snapshot_id: <id>
 
Binder Checklist
- [ ] Snapshot recorded in SNAPSHOT_LEDGER.md
- [ ] Metrics defined with pass thresholds
- [ ] Branch/Observe plan written
- [ ] Decision + reason added to EVIDENCE_BINDER.md
- [ ] DASHBOARD.md updated
- governance:
  - require_cosign: true   # CORE/world integration requires approval
  - rate_limit: { max_ops_per_hour: 5 }
- snapshots:
  - on_branch_start: record snapshot_id in SNAPSHOT_LEDGER.md
  - on_failure: restore snapshot_id and log reason
- recommendations:
  - regen_base: suggest 0.0010–0.0016 (Light‑Heart circulation)
  - decay_base: suggest 0.0007–0.0009 (avoid hoarding)
  - flow_bias:  suggest 0.10–0.25 (toward will gradients, capped)
- render_hints:
  - field_palette: [gold, white]
  - aura_style: soft_glow
  - highlight: prismatic_on_emergence
- observables_hints:
  - favor: clarity_index, coop_cluster_persistence
