# PROTO-40 — MIRROR LAYER PROTOCOL (EN)

Fractal Mirror Mapping between Code & World

## 0. Purpose
Make it intuitive for humans/agents to understand which code structures produce which world phenomena, and vice‑versa.

We build a fractal Mirror Map between:
- Code (modules/classes/functions)
- CellWorld (layers/rules/phenomena/entities)

## 1. Scope: the “narrow mirrorworld”
Not cosmology. Only the bridge between:
- Coding layer: `*.py`, configs, data schemas, rule defs
- Phenomenon layer: time/weather, flora/fauna, human behavior, civilization, affect, language

World‑Tree/Root/Spirit remain higher philosophy; this protocol defines the concrete links below.

## 2. Fractal hierarchy (3 levels)
### 2.1 Level 0 — Domain Axes
TIME | SPACE | LIFE | MIND | CIVIL — used to tie code module groups to phenomenon groups.

### 2.2 Level 1 — Layer↔Layer mapping
```yaml
layers:
  - id: TIME_CORE
    domain: TIME
    code:
      modules:
        - core/time_engine.py
        - config/time_cycles.yaml
    world:
      phenomena:
        - "Day/Night cycle"
        - "Season changes"
        - "Age scaling (1 year = X ticks)"
  - id: LIFE_BEHAVIOR
    domain: LIFE
    code:
      modules:
        - world/life/cell_behavior.py
    world:
      phenomena:
        - "Walk/Run/Rest behaviors"
        - "Hunger / HP recovery"
```

### 2.3 Level 2 — Rule↔Phenomenon mapping
```yaml
rules:
  - id: TIME_DAYNIGHT_CYCLE
    layer: TIME_CORE
    code:
      symbol: "TimeEngine.update_day_night"
      file: "core/time_engine.py"
    world:
      effect:
        - "Sky color changes"
        - "Sleep/Active pattern changes"
        - "Diurnal/Nocturnal switching"

  - id: LIFE_HUNGER_DECAY
    layer: LIFE_BEHAVIOR
    code:
      symbol: "Cell.update_hunger"
      file: "world/life/cell_behavior.py"
    world:
      effect:
        - "Hunger increases over time"
        - "Above threshold, seek food"
        - "At very high levels, HP decreases"
```

## 3. Practical form (single file)
Keep one file at repo root: `MIRROR_MAP.yaml` with:
- domains (with optional children), layers, rules, and natural‑language `world.effect` entries for matching.

## 4. Agent detection loop
Phenomenon → Rule → Code and Code → Rule → Phenomenon. Match user phrasing to `world.effect`, open `code.symbol/file`, patch, re‑run, verify.

## 5. Fractal extension
Refine domains later, e.g., CIVIL splits into ECON / RITUAL / TECH via `children`.

## 6. Summary
A compact, extensible mirror map so humans/agents can navigate changes bidirectionally between code and world.

