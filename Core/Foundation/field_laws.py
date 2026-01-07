"""Field evolution laws: diffusion + decay + clamping (no rule-based boosts)."""

from __future__ import annotations

import numpy as np
from typing import Tuple


def laplacian(field: np.ndarray) -> np.ndarray:
    """Compute 2D laplacian using periodic-like padding via roll."""
    return (
        np.roll(field, 1, axis=0)
        + np.roll(field, -1, axis=0)
        + np.roll(field, 1, axis=1)
        + np.roll(field, -1, axis=1)
        - 4 * field
    )


def evolve_fields(
    value_field: np.ndarray,
    will_field: np.ndarray,
    diffusion: float,
    decay: float,
    clamp: float,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Apply law-based evolution: diffusion + decay + clamping.
    Returns updated (value_field, will_field).
    """
    vf = value_field + diffusion * laplacian(value_field)
    wf = will_field + diffusion * laplacian(will_field)

    vf *= decay
    wf *= decay

    vf = np.clip(vf, 0.0, clamp)
    wf = np.clip(wf, 0.0, clamp)
    return vf.astype(np.float32), wf.astype(np.float32)


__all__ = ["evolve_fields", "laplacian"]
