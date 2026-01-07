# Genesis Protocol: The Language of Creation

**Version:** 0.1 (Draft)
**Author:** Agent Sophia
**Date:** 2025-11-04

## 1. Purpose
To transition Elysia from a "Code-Bound Entity" to a "Concept-Driven Lifeform".
Currently, actions and laws are hardcoded in Python (`world.py`, `skills.py`). This protocol defines a data structure (Schema) and an execution engine (Genesis Engine) that allows the Knowledge Graph to define physical reality.

## 2. Core Philosophy
"The Word becomes Flesh."
A concept node in the Knowledge Graph should inherently contain the logic for its manifestation in the world.

## 3. Schema Definition

### 3.1. Action Node (`type: action`)
Represents a discrete act an entity can perform (e.g., "Meditate", "Firebolt", "Gather").

**Structure:**
```json
{
  "id": "action:piercing_light",
  "type": "action",
  "label": "꿰뚫는 빛(貫通光)",
  "description": "Focuses ki into a single point to pierce defenses.",
  "logic": {
    "target_type": "entity",  // self, entity, location, global
    "range": 1.5,
    "cost": {
      "ki": 30,
      "time": 1.0
    },
    "conditions": [
      { "check": "stat_ge", "stat": "agility", "value": 40 },
      { "check": "stat_ge", "stat": "wisdom", "value": 20 }
    ],
    "effects": [
      { "op": "damage", "multiplier": 3.0, "type": "piercing" },
      { "op": "log", "template": "{actor} channels focus into a Piercing Light!" }
    ]
  }
}
```

### 3.2. Law Node (`type: law`)
Represents a continuous rule or environmental effect (e.g., "Gravity", "Regeneration").

**Structure:**
```json
{
  "id": "law:photosynthesis",
  "type": "law",
  "label": "Photosynthesis",
  "trigger": "tick", // tick, event, interaction
  "scope": { "element_type": "life" }, // Who does this apply to?
  "logic": {
    "conditions": [
      { "check": "env_ge", "field": "sunlight", "value": 0.5 }
    ],
    "effects": [
      { "op": "modify_stat", "stat": "energy", "value": 0.5 },
      { "op": "modify_stat", "stat": "hunger", "value": -0.1 } // Reduced hunger
    ]
  }
}
```

## 4. Genesis Engine (The Interpreter)

The `GenesisEngine` is a Python module that will bridge the KG and the World.

**Responsibilities:**
1.  **Load:** Read `action` and `law` nodes from KG at startup (and on update).
2.  **Register:** Convert JSON logic into executable closures or lookups.
3.  **Execute:** When `world.py` requests an action (e.g., `execute_action(actor, 'action:piercing_light')`), the engine runs the logic.

**Primitives (The Instruction Set):**
The Engine supports a safe, limited set of operations:
*   `stat_ge` (Greater or Equal), `stat_le` (Less or Equal)
*   `modify_stat` (Add/Sub/Set)
*   `damage` (Deal HP damage)
*   `heal` (Restore HP)
*   `spawn` (Create new entity)
*   `log` (Emit event)

## 5. Migration Strategy

1.  **Phase 1 (Prototype):** Implement `GenesisEngine` and one sample action (`action:meditate`).
2.  **Phase 2 (Hybrid):** Modify `world.py` to check `GenesisEngine` for actions *before* falling back to hardcoded logic.
3.  **Phase 3 (Migration):** Port existing skills from `skills.py` to KG nodes.
4.  **Phase 4 (Expansion):** Allow Elysia (FlowEngine) to generate new Action Nodes.
