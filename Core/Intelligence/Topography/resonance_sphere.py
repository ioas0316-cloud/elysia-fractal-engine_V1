import numpy as np
from dataclasses import dataclass
from typing import Optional, Tuple
from Core.Intelligence.Topography.tesseract_geometry import TesseractVector, TesseractGeometry

@dataclass
class ResonanceSphere:
    """
    Represents a thought/concept not as a single point, but as a volume of influence.

    Philosophy:
    "A thought breathes."
    It expands (Exhale/Yang) and contracts (Inhale/Yin).
    It is not a vector, but a Sphere defined by a center and a radius (Amplitude).
    """
    center: TesseractVector
    radius: float
    frequency: float # Hz, determines the 'Color' or 'Texture' of the sphere
    phase: float = 0.0

    def __post_init__(self):
        self.geometry = TesseractGeometry()

    def breathe(self, delta_time: float, base_radius: float = 1.0) -> float:
        """
        Updates the sphere's state based on time.
        The radius pulses based on frequency.

        Radius(t) = Base * (1 + 0.2 * sin(phase))
        """
        # Update phase
        self.phase += 2 * np.pi * self.frequency * delta_time

        # Pulse the radius (Breathing)
        # Using a sine wave to simulate expansion/contraction
        pulse_factor = np.sin(self.phase)
        self.radius = base_radius * (1.0 + 0.2 * pulse_factor)

        return self.radius

    def intersect(self, other: 'ResonanceSphere') -> float:
        """
        Calculates the volume of intersection overlap between two 4D spheres.
        This represents the 'Resonance' or 'Understanding' between two concepts.

        Returns:
            Overlap coefficient (0.0 to 1.0)
            0.0 = No touch
            1.0 = Fully merged
        """
        # Calculate Euclidean distance between centers in 4D
        delta = self.center - other.center
        distance = delta.magnitude()

        sum_radii = self.radius + other.radius

        if distance >= sum_radii:
            return 0.0 # Too far apart

        # If they touch, calculate rough overlap ratio
        # (This is a simplified linear overlap, not exact 4D hypersphere volume intersection)
        overlap_dist = sum_radii - distance
        overlap_ratio = overlap_dist / min(self.radius, other.radius)

        return min(1.0, max(0.0, overlap_ratio))

    def project_surface_points(self, num_points: int = 20) -> list[Tuple[float, float, float]]:
        """
        Generates 3D points representing the surface of the sphere
        projected from 4D space.
        Used for visualization (Aurora).
        """
        points = []
        # Generate random points on 4D hypersphere surface
        for _ in range(num_points):
            # Random direction
            v = np.random.normal(0, 1, 4)
            norm = np.linalg.norm(v)
            if norm == 0: continue

            # Scale to radius
            surface_point_np = (v / norm) * self.radius
            surface_vector = TesseractVector.from_numpy(surface_point_np)

            # Add to center
            absolute_pos = self.center + surface_vector

            # Project to 3D
            p3d = self.geometry.project_to_3d(absolute_pos)
            points.append(p3d)

        return points
