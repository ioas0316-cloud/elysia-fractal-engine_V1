import numpy as np
from typing import List, Tuple, Optional
from dataclasses import dataclass
from Core.Intelligence.Topography.tesseract_geometry import TesseractGeometry
from Core.Intelligence.Topology.resonance_sphere import ResonanceSphere

@dataclass
class VoidRegion:
    """
    Represents a 'Silent Zone' or 'Space Between' identified within the wave field.
    This is a candidate region for new thoughts or actions.
    """
    center: TesseractVector
    radius: float
    calmness: float  # 0.0 (Chaotic) to 1.0 (Perfectly Silent)

class VoidPerceiver:
    """
    Perceives the 'Space Between Waves'.

    Philosophy:
    "Look not at the waves, but at the silence between them."
    """

    def find_void_between(self, sphere_a: ResonanceSphere, sphere_b: ResonanceSphere) -> Optional[VoidRegion]:
        """
        Finds the harmonic void (node) between two resonance spheres.

        Logic:
        1. Identify the vector between the two centers.
        2. Find the point where their 'influence' cancels out or minimizes.
        3. If they are far apart, the void is the open space.
        4. If they overlap, the void might be the 'Eye of the Storm' (if phases cancel)
           or non-existent (if phases amplify).
        """
        delta = sphere_b.center - sphere_a.center
        distance = delta.magnitude()

        if distance == 0:
            return None # Same location, no space between

        # 1. Simple Geometric Void (Midpoint Gap)
        # If separated, the void is the gap in the middle.
        sum_radii = sphere_a.radius + sphere_b.radius

        if distance > sum_radii:
            # Case 1: Distinct Spheres. Void is the gap.
            # Center of void is midpoint
            midpoint = sphere_a.center + TesseractVector.from_numpy(delta.to_numpy() * 0.5)

            # Radius of void is half the gap
            gap = distance - sum_radii
            void_radius = gap * 0.5

            return VoidRegion(center=midpoint, radius=void_radius, calmness=1.0)

        else:
            # Case 2: Overlapping Spheres (Interference)
            # We look for destructive interference (Phase Cancellation).

            # Simple simulation: Check phase difference
            # Phase diff of PI (180 deg) means cancellation
            phase_diff = abs(sphere_a.phase - sphere_b.phase) % (2 * np.pi)
            if phase_diff > np.pi:
                phase_diff = 2 * np.pi - phase_diff

            # If closer to PI, higher cancellation (more void-like)
            cancellation_score = 1.0 - abs(phase_diff - np.pi) / np.pi

            if cancellation_score > 0.8:
                # High cancellation -> "Eye of the Storm" void
                midpoint = sphere_a.center + TesseractVector.from_numpy(delta.to_numpy() * 0.5)
                # The effective void is small, bounded by the overlap
                overlap = sum_radii - distance
                return VoidRegion(center=midpoint, radius=overlap * 0.2, calmness=cancellation_score)

            return None # Constructive interference fills the space

    def scan_for_voids(self, spheres: List[ResonanceSphere]) -> List[VoidRegion]:
        """
        Scans a collection of spheres to find multiple void regions.
        (Simplified O(N^2) pairwise check for prototype)
        """
        voids = []
        n = len(spheres)
        for i in range(n):
            for j in range(i + 1, n):
                void = self.find_void_between(spheres[i], spheres[j])
                if void:
                    voids.append(void)
        return voids
