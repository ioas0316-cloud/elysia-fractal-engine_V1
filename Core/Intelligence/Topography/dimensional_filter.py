import numpy as np
from dataclasses import dataclass
from typing import Tuple, List, Optional
from Core.Intelligence.Topography.resonance_sphere import ResonanceSphere
from Core.Intelligence.Topography.tesseract_geometry import TesseractGeometry

@dataclass
class FilterResult:
    """
    The result of a judgment/splitting operation.
    """
    accepted: Optional[ResonanceSphere] # Matches the standard
    rejected: Optional[ResonanceSphere] # Does not match (The 'Other')
    resonance: float # How well it fit the filter (0.0 - 1.0)

class DimensionalFilter:
    """
    Represents a 'Standard' or 'Boundary' that splits reality.

    Philosophy:
    "Judgment is Splitting."
    This filter takes a wave (Sphere) and splits it into two:
    what fits the criteria, and what doesn't.
    """

    def __init__(self, target_frequency: float, bandwidth: float = 0.5):
        """
        Args:
            target_frequency: The 'Standard' (e.g., 440Hz for 'A')
            bandwidth: The tolerance of the filter (The width of the boundary)
        """
        self.target_frequency = target_frequency
        self.bandwidth = bandwidth

    def apply(self, thought: ResonanceSphere) -> FilterResult:
        """
        Applies the filter to a thought.

        Logic:
        1. Calculate resonance based on frequency difference.
        2. If resonance is high, the thought is 'Accepted' (Passes the filter).
        3. If resonance is low, it is 'Rejected' (Blocked by boundary).
        4. In a true wave physics, it's not binary. It splits energy.
        """
        diff = abs(thought.frequency - self.target_frequency)

        # Gaussian resonance curve
        # 1.0 at perfect match, decays as diff increases
        resonance = np.exp(-(diff**2) / (2 * (self.bandwidth**2)))

        if resonance > 0.1: # Threshold for interaction
            # Energy Split
            # Accepted part retains the frequency but amplitude scales with resonance
            accepted_radius = thought.radius * resonance
            accepted = ResonanceSphere(
                center=thought.center,
                radius=accepted_radius,
                frequency=thought.frequency, # Retains identity
                phase=thought.phase
            )

            # Rejected part is the 'Noise' or 'Remainder'
            rejected_radius = thought.radius * (1.0 - resonance)
            rejected = ResonanceSphere(
                center=thought.center,
                radius=rejected_radius,
                frequency=thought.frequency,
                phase=thought.phase + np.pi # Phase shift (Inversion/Rejection)
            )

            return FilterResult(accepted, rejected, resonance)

        else:
            # Totally rejected (No resonance)
            return FilterResult(None, thought, 0.0)

    def __repr__(self):
        return f"<DimensionalFilter Freq={self.target_frequency}Hz Width={self.bandwidth}>"
