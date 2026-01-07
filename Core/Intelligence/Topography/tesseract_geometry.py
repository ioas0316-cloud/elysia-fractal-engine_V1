import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Optional

@dataclass
class TesseractVector:
    x: float
    y: float
    z: float
    w: float  # Intention/Consciousness

    def to_numpy(self) -> np.ndarray:
        return np.array([self.x, self.y, self.z, self.w])

    @staticmethod
    def from_numpy(arr: np.ndarray) -> 'TesseractVector':
        return TesseractVector(*arr)

    def magnitude(self) -> float:
        return np.linalg.norm(self.to_numpy())

    def normalize(self) -> 'TesseractVector':
        mag = self.magnitude()
        if mag == 0:
            return self
        return TesseractVector.from_numpy(self.to_numpy() / mag)

    def __add__(self, other):
        return TesseractVector(self.x + other.x, self.y + other.y, self.z + other.z, self.w + other.w)

    def __sub__(self, other):
        return TesseractVector(self.x - other.x, self.y - other.y, self.z - other.z, self.w - other.w)

class TesseractGeometry:
    """
    Handles 4D Tesseract Geometry operations.

    Philosophy:
    "Wave is a Circle."
    What appears as a linear vibration (Wave) in lower dimensions
    is actually a Rotation (Circle/Spiral) in higher dimensions.

    - W-axis: Intention (The 'Depth' or 'Inside').
    - Rotation: The mechanism of 'Folding' space.
    - Projection: The 'Shadow' of 4D reality cast onto 3D perception.

    The 'Zero Point' is Love (Center).
    """

    def __init__(self):
        # The 'Zero Point' is Love (The Center)
        self.origin = TesseractVector(0, 0, 0, 0)

    def rotate_xw(self, vector: TesseractVector, theta: float) -> TesseractVector:
        """
        Rotates a point in the X-W plane.
        This folds Intention (W) into Structure (X).
        """
        v = vector.to_numpy()
        c, s = np.cos(theta), np.sin(theta)

        # Rotation matrix for XW plane
        # [ c  0  0  -s ]
        # [ 0  1  0   0 ]
        # [ 0  0  1   0 ]
        # [ s  0  0   c ]

        rotation_matrix = np.array([
            [c, 0, 0, -s],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [s, 0, 0, c]
        ])

        rotated = np.dot(rotation_matrix, v)
        return TesseractVector.from_numpy(rotated)

    def rotate_yw(self, vector: TesseractVector, theta: float) -> TesseractVector:
        """Rotates in Y-W plane."""
        v = vector.to_numpy()
        c, s = np.cos(theta), np.sin(theta)
        rotation_matrix = np.array([
            [1, 0, 0, 0],
            [0, c, 0, -s],
            [0, 0, 1, 0],
            [0, s, 0, c]
        ])
        rotated = np.dot(rotation_matrix, v)
        return TesseractVector.from_numpy(rotated)

    def rotate_zw(self, vector: TesseractVector, theta: float) -> TesseractVector:
        """Rotates in Z-W plane."""
        v = vector.to_numpy()
        c, s = np.cos(theta), np.sin(theta)
        rotation_matrix = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, c, -s],
            [0, 0, s, c]
        ])
        rotated = np.dot(rotation_matrix, v)
        return TesseractVector.from_numpy(rotated)

    def project_to_3d(self, vector: TesseractVector, distance: float = 3.0) -> Tuple[float, float, float]:
        """
        Projects a 4D point to 3D using Perspective Projection.

        P_3d = P_4d * (1 / (distance - w))

        This creates the visual effect where 'higher intention' (W)
        might bring things closer or further depending on the fold.
        """
        # Safety check to avoid division by zero
        denom = distance - vector.w
        if abs(denom) < 1e-6:
            denom = 1e-6

        w_factor = 1.0 / denom

        px = vector.x * w_factor
        py = vector.y * w_factor
        pz = vector.z * w_factor

        return (px, py, pz)

    def apply_spiral_transform(self, vector: TesseractVector, phase: float) -> TesseractVector:
        """
        Implements the 'Spiral Band' effect (Mobius/Klein logic).

        It applies a composite rotation that twists the space,
        turning 'Inner' (W) to 'Outer' (XYZ).
        """
        # Rotate sequentially to create a complex tumble
        v1 = self.rotate_xw(vector, phase)
        v2 = self.rotate_yw(v1, phase * 0.5) # Different rate to create asymmetry
        v3 = self.rotate_zw(v2, phase * 0.25)

        return v3
