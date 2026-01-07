# WORLD_KIT_INDEX (World Scenarios Map, v0, English)

> Map of `WORLD_KIT_*` scenario protocols and their main code/log locations.

---

## 0. Base World

- **WORLD-01: CELLWORLD (Base World)**  
  - Code: `Project_Sophia/core/world.py: class World`  
  - Description: grid-based life world with energy, hunger/thirst, fields, laws, and sensory channels.  
  - Related: `scripts/cellworld_growth_loop.py`, `ELYSIA/WORLD/CELLWORLD_DROUGHT_FLOOD_PRESET.md`.

All world kits share this single body; they configure laws, initial state, or observers.

---

## 1. Fantasy / Trade Line (ARCHIVED)

- **WORLD-02: FAIRY_VILLAGE** *(ARCHIVED)*  
  - Protocol: `WORLD_KIT_FAIRY_VILLAGE.md`  
  - Theme: short-lived fairy village; death/memory/culture patterns.  
  - WORLD_KIT: `WORLD_KIT_FAIRY_VILLAGE`  
  - STATUS: `ARCHIVED` (protocol only; not used in the main loop).

- **WORLD-03: TWIN_VILLAGES_TRADE** *(ARCHIVED)*  
  - Protocol: `WORLD_KIT_TWIN_VILLAGES_TRADE.md`  
  - Theme: trade and trust between human and fae twin villages.  
  - WORLD_KIT: `WORLD_KIT_TWIN_VILLAGES_TRADE`  
  - STATUS: `ARCHIVED` (protocol only; not used in the main loop).

---

## 2. Death / Memory Line

- **WORLD-04: DEATH_FLOW_CORPSE_TO_MEMORY**  
  - Protocol: `WORLD_KIT_DEATH_FLOW_CORPSE_TO_MEMORY.md` (archived stub).  
  - Theme: death → corpse → grave/field change → memory effects.  
  - Note: implemented as overlays on CELLWORLD, not a separate world body.

---

## 3. Martial / Wuxia Line (ARCHIVED)

- **WORLD-10: WULINWORLD (Wuxia Scenario, ARCHIVED)**  
  - Original script: `scripts/wulin_trials_loop.py` (removed).  
  - Logs: `logs/wulin_trials_loop.jsonl` (martial duels and tension metrics).  
  - STATUS: `ARCHIVED` (martial flavor should now be expressed as themes on CELLWORLD).

---

## 4. Code / Mirror Lines

- **WORLD-20: CODEWORLD**  
  - Script: `scripts/elysia_engineer_loop.py`  
  - Theme: code/engineer persona world snapshots.  
  - WORLD_KIT: `CODEWORLD`  
  - LAYER: `WORLD` (logical, not physical).

- **WORLD-30: MIRRORWORLD**  
  - Script: `scripts/mirror_layer_loop.py`  
  - Logs: `logs/mirror_layer_loop.jsonl` (`world_kit: "MIRRORWORLD"`).  
  - Theme: mirror/UI state, sync ratio, latency, clarity.  
  - Tags: `measurement_world`, `mirror_layer`, `LENS`.

---

## 5. Themes instead of new worlds

- **THEME: east_continent (East Continent / Wulin flavor)**  
  - Code: `Project_Sophia/world_themes/east_continent/`  
  - Description: martial arts, sects, rivers-and-lakes culture; lives on CELLWORLD body.

- **THEME: west_continent (West Continent / Western fantasy)**  
  - Code: `Project_Sophia/world_themes/west_continent/`  
  - Description: knights, magic guilds, kingdoms and citadels; lives on CELLWORLD body.

New worlds should be expressed as **themes, presets, or overlays** on `WORLD-01: CELLWORLD`,
not as separate world bodies.

