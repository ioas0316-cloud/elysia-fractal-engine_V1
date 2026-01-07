"""
This module provides the Observer class, which is responsible for
inspecting the state of a World instance and exporting it in a
structured format for external tools like visualizers.
"""
from __future__ import annotations
import typing
import numpy as np

if typing.TYPE_CHECKING:
    from elysia_world.world import World


class Observer:
    """
    Observes a World instance and creates snapshots of its state.
    """
    def __init__(self, world: "World"):
        """
        Initializes the Observer with a reference to the world.

        Args:
            world: The World instance to observe.
        """
        self.world = world

    def get_world_snapshot(self, level: int = 0) -> dict:
        """
        Generates a JSON-serializable snapshot of the current world state,
        tailored to the requested detail level.

        Args:
            level: The level of detail for the snapshot.
                   - 0: Core spiritual fields and world info.
                   - 1: Level 0 + Basic physical state of all cells.
                   - 2: Level 1 + Detailed internal state (emotions, PFE/Trinity).
                   - 3: Level 2 + Relational data (not yet implemented).
        """
        world = self.world
        if not world:
            return {}

        # --- Base Information (Always Included) ---
        year, month, day = world.get_date_ymd()
        snapshot = {
            "world_info": {
                "time_step": world.time_step,
                "time_of_day": world.time_of_day,
                "season": world.get_season_name(),
                "year": year,
                "month": month,
                "day": day,
            },
        }

        # --- Level 0: Spiritual Laws Layer ---
        if level >= 0:
            def get_field_summary(field_array: np.ndarray) -> dict:
                if field_array is not None and field_array.size > 0:
                    return {
                        "mean": float(np.mean(field_array)),
                        "max": float(np.max(field_array)),
                        "min": float(np.min(field_array)),
                    }
                return {"mean": 0, "max": 0, "min": 0}

            snapshot["fields"] = {
                "value_mass": get_field_summary(world.value_mass_field),
                "will": get_field_summary(world.will_field),
                "threat": get_field_summary(world.threat_field),
                "coherence": get_field_summary(world.coherence_field),
            }

        # --- Level 1: Physical Survival Layer ---
        if level >= 1:
            snapshot["cells_l1"] = []
            alive_indices = np.where(world.is_alive_mask)[0]
            for i in alive_indices:
                try:
                    pos = world.positions[i]
                    snapshot["cells_l1"].append({
                        "id": world.cell_ids[i],
                        "position": {"x": float(pos[0]), "y": float(pos[1]), "z": float(pos[2])},
                        "hp": float(world.hp[i]),
                    })
                except IndexError:
                    continue

        # --- Level 2: Internal State & Emotion Layer ---
        if level >= 2:
            snapshot["cells_l2"] = []
            alive_indices = np.where(world.is_alive_mask)[0]
            for i in alive_indices:
                try:
                    p_val, f_val, e_val = world.get_pfe_for_actor(i)
                    body_val, soul_val, spirit_val = world.get_trinity_for_actor(i)
                    snapshot["cells_l2"].append({
                        "id": world.cell_ids[i],
                        "label": world.labels[i],
                        "max_hp": float(world.max_hp[i]),
                        "emotion": world.emotions[i],
                        "pfe_values": {
                            "persistence": float(p_val),
                            "force": float(f_val),
                            "energy": float(e_val)
                        },
                        "trinity_values": {
                            "body": float(body_val),
                            "soul": float(soul_val),
                            "spirit": float(spirit_val)
                        }
                    })
                except IndexError:
                    continue
                except Exception as e:
                    if world.logger:
                        world.logger.error(f"Error in L2 snapshot for cell index {i}: {e}")
                    continue

        # --- Level 3: Interaction Layer (Placeholder) ---
        if level >= 3:
            snapshot["interactions"] = [] # Placeholder for future implementation

        return snapshot
