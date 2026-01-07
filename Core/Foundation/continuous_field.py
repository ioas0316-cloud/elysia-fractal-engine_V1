"""
Continuous Field Inference (Grok's Approach)
==============================================
A continuous, wave-based field where concepts exist as density distributions
in a 4D space (x, y, z, time), enabling truly spatial-temporal reasoning.

This complements the discrete ConceptField with a continuous mathematical model.
"""

import numpy as np
from typing import Dict, Tuple
import math

class ContinuousField:
    """
    A 4D continuous field where concepts manifest as wave functions.
    ψ(x,y,z,t) = superposition of concept waves
    """
    
    def __init__(self, resolution: int = 50):
        """
        Initialize a 3D spatial field + time.
        Lower resolution for 1060 GPU safety (50x50x50 = 125K cells).
        """
        self.resolution = resolution
        self.field = np.zeros((resolution, resolution, resolution), dtype=np.float32)
        self.time = 0.0
        self.concept_registry: Dict[str, Tuple[float, float, float]] = {}
    
    def register_concept(self, name: str, base_frequency: float, x: float, y: float, z: float):
        """
        Register a concept with its base frequency and spatial coordinates.
        
        Args:
            name: Concept name
            base_frequency: Base oscillation frequency
            x, y, z: Normalized coordinates (0-1)
        """
        self.concept_registry[name] = (base_frequency, x, y, z)
    
    def activate(self, concept: str, intensity: float = 1.0, depth: float = 1.0):
        """
        Activates a concept by adding its wave pattern to the field.
        
        Args:
            concept: Concept to activate
            intensity: Amplitude of the wave
            depth: Z-axis penetration (0-1)
        """
        if concept not in self.concept_registry:
            return
        
        freq, cx, cy, cz = self.concept_registry[concept]
        
        # Convert normalized coords to grid indices
        ix = int(cx * self.resolution)
        iy = int(cy * self.resolution)
        iz = int(cz * depth * self.resolution)
        
        # Create wave pattern centered at (ix, iy, iz)
        for x in range(self.resolution):
            for y in range(self.resolution):
                for z in range(min(self.resolution, iz + 20)):  # Limited Z spread
                    # Distance from center
                    dist = math.sqrt((x - ix)**2 + (y - iy)**2 + (z - iz)**2)
                    
                    # Wave function: amplitude * cos(freq * time + phase)
                    phase = 2 * math.pi * dist / 10.0
                    wave_value = intensity * math.cos(freq * self.time + phase)
                    
                    # Gaussian decay with distance
                    decay = math.exp(-dist**2 / (2 * 10**2))
                    
                    self.field[x, y, z] += wave_value * decay
        
        # Advance time
        self.time += 0.1
    
    def get_field_insight(self) -> Dict[str, float]:
        """
        Extracts insights from the field state.
        Returns multidimensional understanding of current field.
        """
        return {
            "total_energy": float(np.sum(np.abs(self.field))),
            "peak_intensity": float(np.max(self.field)),
            "field_coherence": float(np.std(self.field)),
            "spatial_mean": float(np.mean(self.field)),
            "z_depth_profile": float(np.mean(self.field[:, :, -10:])),  # Deep layers
        }
    
    def find_resonance_zones(self, threshold: float = 0.1) -> list:
        """
        Finds regions of high field intensity (resonance zones).
        These indicate emergent patterns.
        """
        zones = []
        high_intensity = self.field > threshold
        
        # Find connected regions (simplified)
        if np.any(high_intensity):
            indices = np.where(high_intensity)
            for i in range(min(5, len(indices[0]))):  # Top 5 zones
                x, y, z = indices[0][i], indices[1][i], indices[2][i]
                intensity = self.field[x, y, z]
                zones.append({
                    "position": (x, y, z),
                    "intensity": float(intensity),
                    "depth_ratio": z / self.resolution
                })
        
        return zones
    
    def reset(self):
        """Resets the field to zero (except time continues)."""
        self.field.fill(0.0)
    
    def get_slice(self, axis: str = 'z', position: int = None) -> np.ndarray:
        """
        Gets a 2D slice of the 3D field for visualization.
        
        Args:
            axis: 'x', 'y', or 'z'
            position: Position along that axis (default: middle)
        """
        if position is None:
            position = self.resolution // 2
        
        if axis == 'z':
            return self.field[:, :, position]
        elif axis == 'y':
            return self.field[:, position, :]
        else:  # x
            return self.field[position, :, :]
