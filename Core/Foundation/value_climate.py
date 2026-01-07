from dataclasses import dataclass
from typing import Dict


@dataclass
class ValueClimate:
    """
    Soft mapping from Elysia's current feelings into
    field-level modulation parameters.

    This does not directly modify any field; it is a
    summary that other modules can read.
    """

    value_mass_gain: float
    will_tension_gain: float
    threat_sensitivity: float
    exploration_bias: float

    def as_dict(self) -> Dict[str, float]:
        return {
            "value_mass_gain": float(self.value_mass_gain),
            "will_tension_gain": float(self.will_tension_gain),
            "threat_sensitivity": float(self.threat_sensitivity),
            "exploration_bias": float(self.exploration_bias),
        }


def compute_value_climate(feelings: Dict[str, float]) -> ValueClimate:
    """
    Derive a soft "climate" from the current feeling state.

    Intuition:
    - Joy/Creation 높음: value_mass 강화, exploration 증가.
    - Care 높음: threat_sensitivity는 조금 줄이고, will_tension도 부드럽게.
    - Mortality 높음: threat_sensitivity와 will_tension이 올라가고,
      exploration은 약간 줄어든다.
    """

    joy = max(0.0, float(feelings.get("joy", 0.0)))
    creation = max(0.0, float(feelings.get("creation", 0.0)))
    care = max(0.0, float(feelings.get("care", 0.0)))
    mortality = max(0.0, float(feelings.get("mortality", 0.0)))

    # Normalize with a gentle squash to avoid runaway values.
    def squash(x: float) -> float:
        return 1.0 - (2.718281828 ** (-x)) if x > 0.0 else 0.0

    j = squash(joy)
    c = squash(creation)
    ca = squash(care)
    m = squash(mortality)

    # Value mass gain: more joy/creation -> stronger reinforcement.
    value_mass_gain = 1.0 + 0.5 * j + 0.5 * c

    # Will tension: more mortality -> stronger; care slightly softens it.
    will_tension_gain = 1.0 + 0.7 * m - 0.3 * ca
    if will_tension_gain < 0.5:
        will_tension_gain = 0.5

    # Threat sensitivity: mortality raises it, care lowers it a bit.
    threat_sensitivity = 1.0 + 0.8 * m - 0.2 * ca
    if threat_sensitivity < 0.5:
        threat_sensitivity = 0.5

    # Exploration bias: joy/creation encourage exploration; mortality dampens it.
    exploration_bias = 1.0 + 0.6 * j + 0.6 * c - 0.4 * m
    if exploration_bias < 0.2:
        exploration_bias = 0.2

    return ValueClimate(
        value_mass_gain=value_mass_gain,
        will_tension_gain=will_tension_gain,
        threat_sensitivity=threat_sensitivity,
        exploration_bias=exploration_bias,
    )

