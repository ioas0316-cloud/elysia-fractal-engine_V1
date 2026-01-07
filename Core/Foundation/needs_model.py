from dataclasses import dataclass
from typing import Dict

import numpy as np

from Core.Foundation.System.core.world import World


@dataclass
class HumanNeeds:
    """
    Minimal need vector for a human-like cell.

    Values are normalized into [0,1] where higher means
    "more satisfied" along that axis.
    """

    safety: float
    nourishment: float
    hydration: float
    comfort: float
    social_bond: float

    def as_dict(self) -> Dict[str, float]:
        return {
            "safety": float(self.safety),
            "nourishment": float(self.nourishment),
            "hydration": float(self.hydration),
            "comfort": float(self.comfort),
            "social_bond": float(self.social_bond),
        }


def _norm01(x: float, lo: float, hi: float) -> float:
    if hi <= lo:
        return 0.0
    v = (x - lo) / float(hi - lo)
    return float(np.clip(v, 0.0, 1.0))


def compute_human_needs(world: World, idx: int) -> HumanNeeds:
    """
    Derive a simple, analogue need vector for a human-like cell
    from the existing World state.

    This does not change behaviour; it is a bridge for MIND/META
    layers to read how the body/fields currently feel.
    """
    # Safety ~ inverse of local threat + current HP ratio.
    hp = float(world.hp[idx]) if world.hp.size > idx else 0.0
    max_hp = float(world.max_hp[idx]) if world.max_hp.size > idx and world.max_hp[idx] > 0 else 1.0
    hp_ratio = np.clip(hp / max_hp, 0.0, 1.0)

    try:
        x = int(world.positions[idx][0]) % world.width
        y = int(world.positions[idx][1]) % world.width
        threat_local = float(getattr(world, "threat_field", None)[y, x]) if hasattr(world, "threat_field") else 0.0
    except Exception:
        threat_local = 0.0

    safety = float(np.clip(1.0 - threat_local, 0.0, 1.0)) * 0.7 + hp_ratio * 0.3

    # Nourishment ~ hunger (0..100) normalized (higher = more fed).
    hunger = float(world.hunger[idx]) if world.hunger.size > idx else 100.0
    nourishment = _norm01(hunger, lo=0.0, hi=100.0)

    # Hydration ~ hydration (0..100) normalized.
    hydration_raw = float(world.hydration[idx]) if world.hydration.size > idx else 100.0
    hydration = _norm01(hydration_raw, lo=0.0, hi=100.0)

    # Comfort ~ inverse of injury + temperature closeness to ambient.
    is_injured = bool(world.is_injured[idx]) if world.is_injured.size > idx else False
    temp = float(world.temperature[idx]) if world.temperature.size > idx else float(world.ambient_temperature_c)
    ambient = float(getattr(world, "ambient_temperature_c", 15.0))
    temp_delta = abs(temp - ambient)
    temp_score = float(np.clip(1.0 - (temp_delta / 40.0), 0.0, 1.0))
    comfort = temp_score * (0.3 if is_injured else 1.0)

    # Social bond ~ number/strength of connections.
    social_bond = 0.0
    try:
        if hasattr(world, "adjacency_matrix") and world.adjacency_matrix.shape[0] > idx:
            # Outgoing connections strength sum, normalized softly.
            strengths = np.asarray(world.adjacency_matrix[idx].data, dtype=float)
            bond_raw = float(strengths.sum()) if strengths.size else 0.0
            social_bond = float(np.tanh(bond_raw))
    except Exception:
        social_bond = 0.0

    return HumanNeeds(
        safety=safety,
        nourishment=nourishment,
        hydration=hydration,
        comfort=comfort,
        social_bond=social_bond,
    )
