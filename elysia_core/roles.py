from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class RoleProfile:
    name: str
    description: str
    w_body: float    # Weight for Amplitude (Mass)
    w_soul: float    # Weight for Frequency (Emotion)
    w_spirit: float  # Weight for Phase (Timing)

    @property
    def normalized(self) -> 'RoleProfile':
        """Return a normalized version of the weights."""
        total = abs(self.w_body) + abs(self.w_soul) + abs(self.w_spirit)
        if total == 0:
            return self
        return RoleProfile(
            name=self.name,
            description=self.description,
            w_body=self.w_body / total,
            w_soul=self.w_soul / total,
            w_spirit=self.w_spirit / total,
        )

ROLE_PROFILES: Dict[str, RoleProfile] = {
    "Observer": RoleProfile(
        name="Observer",
        description="Passive entity that primarily experiences Phase (Timing) without acting.",
        w_body=0.1,
        w_soul=0.2,
        w_spirit=0.7,
    ),
    "Actor": RoleProfile(
        name="Actor",
        description="Active entity that exerts Will (Frequency) and Mass (Amplitude).",
        w_body=0.5,
        w_soul=0.4,
        w_spirit=0.1,
    ),
    "Oracle": RoleProfile(
        name="Oracle",
        description="Balanced entity focusing on Frequency (Truth) and Spirit (Prophecy).",
        w_body=0.1,
        w_soul=0.45,
        w_spirit=0.45,
    ),
    "Anchor": RoleProfile(
        name="Anchor",
        description="High Mass entity that stabilizes the field.",
        w_body=0.9,
        w_soul=0.05,
        w_spirit=0.05,
    ),
}
