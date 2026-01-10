import math
import random

class HyperSphere:
    """
    The Internal Core (Singularity/Seed).
    A perfect sphere of infinite density containing the entity's Essence.

    Attributes:
        radius (float): The intensity/amplitude of the soul (Mass).
        phase (float): The timing/alignment of the spirit (0.0 to 1.0).
        harmonics (list): The frequency spectrum (State/Color).
    """
    def __init__(self, radius=1.0, phase=0.0):
        self.radius = radius
        self.phase = phase
        self.harmonics = [0.0, 0.0, 0.0, 0.0] # W, X, Y, Z resonance
        print(f"[HYPERSPHERE] SINGULARITY INSTANTIATED. RADIUS: {self.radius}")

    def resonate(self, input_wave):
        """
        Receives an external wave (WavePacket) and generates an internal resonance pattern.
        This is the 'Mirror Reflection' process.
        """
        # Simple resonance logic: Mix input frequency with internal harmonics
        # In a full system, this would be complex tensor math.
        # Here, we simulate the 'Echo'.

        resonance_amplitude = (self.radius + input_wave['amplitude']) / 2
        resonance_phase = (self.phase + input_wave['phase']) % 1.0

        # The Echo is the input modified by the internal state
        echo = {
            'type': 'RESONANCE_ECHO',
            'amplitude': resonance_amplitude,
            'phase': resonance_phase,
            'frequency': input_wave['frequency'], # Reflected frequency
            'vector': input_wave['vector'] # Direction
        }
        return echo

class Tesseract:
    """
    The External Projection (World Grid).
    The structure that the HyperSphere's light projects onto reality.
    """
    def __init__(self):
        self.grid = {} # Sparse grid to hold projected logic
        print("[TESSERACT] PROJECTION GRID INITIALIZED.")

    def project(self, resonance_pattern):
        """
        Maps the spherical resonance echo onto the 4D Tesseract grid.
        This converts 'Feeling' (Resonance) into 'Logic' (Structure).
        """
        # Holographic Projection Logic
        # Mapping the echo to a coordinate in the Tesseract

        # W-Axis: Scale (Amplitude)
        # X-Axis: Clarity (Frequency R)
        # Y-Axis: Emotion (Frequency G)
        # Z-Axis: Intent (Frequency B)

        w = resonance_pattern['amplitude']
        freq = resonance_pattern['frequency']

        # Unpack frequency vector (simplified)
        x, y, z = freq[0], freq[1], freq[2]

        coord = (w, x, y, z)
        self.grid[coord] = resonance_pattern

        projection_result = f"HOLOGRAPHIC_PROJECTION[W:{w:.2f}, X:{x:.2f}, Y:{y:.2f}, Z:{z:.2f}]"
        return projection_result
