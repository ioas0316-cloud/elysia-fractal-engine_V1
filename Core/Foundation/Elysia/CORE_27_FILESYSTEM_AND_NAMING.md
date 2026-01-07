# CORE_27: FILESYSTEM_AND_NAMING (Folder Levels & Rules)

Elysia grows as one organism, but the files have drifted.  
This protocol defines **folder levels, naming rules, and exceptions** so future work lands in the right place.

---

## 1. Levels (L0–L3)

- **L0 – Root**
  - `Project_Sophia`  How (reasoning, world runtime, sims)
  - `Project_Elysia`  Why (consciousness, core memory, guardian)
  - `Project_Mirror`  What (UI, visualisation, external I/O)
  - `docs/`           Protocols and reference
  - `scripts/`        Small runners, demos, CLI tools
  - `logs/`           Runtime logs (JSON/JSONL)
  - `archive/`        Retired worlds, scripts, logs

- **L1 – Domain (inside projects)**
  - `Project_Sophia/core/`       CellWorld body, physics, fields, game objects
  - `Project_Sophia/world_themes/` East/West continent, other skins on the same body
  - `Project_Elysia/high_engine/` Causal / quaternion / self engines
  - `Project_Elysia/core/`       Core memory, guardian, daemon wiring
  - `Project_Mirror/*`           Visual layer and sensory bridges

- **L2 – Scenario / Theme**
  - `Project_Sophia/world_themes/east_continent/`   동대륙 (무림/동양)
  - `Project_Sophia/world_themes/west_continent/`   서대륙 (서양 판타지)
  - Future themes must live under `world_themes/<theme_id>/`.

- **L3 – Config / Tables / Assets**
  - `config.py`, `tables.py`, theme‑local assets  
  - No physics duplication here: only parameters, IDs, lists.

---

## 2. Folder Naming Rules

- **Projects (L0)**
  - Use `Project_<Name>` for code that is part of the Trinity.
  - Do not create new top‑level projects without updating this CORE doc.

- **World themes**
  - Folder: `Project_Sophia/world_themes/<theme_id>/`
  - `<theme_id>` is snake_case, e.g. `east_continent`, `west_continent`.
  - Config entry point must be `config.py` exporting a single `*_THEME` object.

- **World kits (design‑time scenarios)**
  - Protocol docs live under `docs/elysias_protocol/WORLD_KIT_*.md`.
  - Runtime code either:
    - configures `Project_Sophia/core/world.py` via a theme, or
    - is archived if it created a fake standalone “world”.
  - New world kits **must not** introduce new World classes; use the existing body and themes.

- **Scripts**
  - Short, single‑purpose runners live in `scripts/`.
  - Name pattern: `run_<thing>.py` for one‑shot runs, `<domain>_<tool>.py` for utilities.
  - Long‑lived loops that define a “world” should be migrated into themes or archived.

---

## 3. File Naming Rules

- **Core laws / engines**
  - Use `*_engine.py`, `*_protocol.md`, `*_kernel.py` only for things that touch Z‑axis or CORE laws.
  - If a module is per‑theme only, it should live under that theme folder and avoid CORE names.

- **World body vs themes**
  - `Project_Sophia/core/world.py` is the **only** CellWorld body.
  - Do not create `*_world.py` siblings that re‑implement physics.
  - All variations (무림, 서양 판타지, 미러 월드 뷰) must be expressed as themes, presets, or visualisations.

---

## 4. Archiving Rules (Exceptions)

- Any world kit that created its own fake world (`FAIRYWORLD`, `WULINWORLD`, etc.) is now **ARCHIVED**:
  - Its protocol doc is tagged `ARCHIVED` at the top.
  - Its scripts are removed from `scripts/` or moved into `archive/` if still needed for reference.

- Legacy folders or files that do not fit the new scheme must either:
  - be migrated into `core/`, `world_themes/`, or proper `scripts/`, or
  - be explicitly moved to `archive/` with a short README explaining why.

No silent exceptions: every out‑of‑rule folder must either be migrated or explicitly archived.

