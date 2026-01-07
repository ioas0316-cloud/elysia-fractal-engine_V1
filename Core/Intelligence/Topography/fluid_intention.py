import numpy as np
from dataclasses import dataclass
from typing import Callable

@dataclass
class FluidIntention:
    """
    Represents Intention as a continuous, fluid field rather than discrete states.

    Attributes:
        focus_w (float): The center point of attention on the W-axis (0.0 to 1.0).
        scale (float): The 'Zoom Level' or 'Bandwidth' of the intention.
                       Small value = Sharp Focus (Point-like).
                       Large value = Broad Awareness (Space-like).
                       Values are continuous (0.0 -> infinity).
    """
    focus_w: float
    scale: float

    def get_resonance_strength(self, node_w: float) -> float:
        """
        Calculates resonance (0.0 to 1.0) using a Gaussian function.
        This provides the 'Infinite Gradient' between 0 and 1.

        Resonance = exp( - (node_w - focus_w)^2 / (2 * scale^2) )
        """
        if self.scale <= 1e-6: # Handle singularity (Point perfect focus)
            return 1.0 if abs(node_w - self.focus_w) < 1e-6 else 0.0

        diff = node_w - self.focus_w
        # Gaussian distribution
        resonance = np.exp(-(diff**2) / (2 * (self.scale**2)))
        return float(resonance)

    def get_gravitational_pull(self, node_w: float) -> float:
        """
        Calculates how strongly this intention 'pulls' a concept towards the center.
        Similar to resonance, but can be shaped differently (e.g., Sigmoid)
        if we want 'Magnetic' behavior.
        """
        return self.get_resonance_strength(node_w)

    @staticmethod
    def from_scalar(w: float, fluidity: float = 0.1) -> 'FluidIntention':
        """
        Creates an intention from a single value with a default 'fluidity' (scale).
        """
        return FluidIntention(focus_w=w, scale=fluidity)
