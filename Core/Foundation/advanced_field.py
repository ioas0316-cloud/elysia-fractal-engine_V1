"""
Advanced Field Physics
======================
Extends ContinuousField with:
1. Orthogonal Harmonics (complex wave structures)
2. Interference Pattern Analysis (emergent concept detection)
3. Eigenvalue Mode Extraction (dominant pattern identification)
"""

import numpy as np
from typing import Dict, List, Tuple
from Project_Elysia.mechanics.continuous_field import ContinuousField

class AdvancedField(ContinuousField):
    """
    Enhanced field with harmonic decomposition and pattern analysis.
    """
    
    def __init__(self, resolution: int = 30):
        super().__init__(resolution)
        # Harmonic coefficients for each concept
        self.harmonics: Dict[str, List[float]] = {}
    
    def register_concept_with_harmonics(
        self, 
        name: str, 
        base_frequency: float,
        x: float, y: float, z: float,
        harmonic_coeffs: List[float] = None
    ):
        """
        Register concept with harmonic structure.
        
        Args:
            harmonic_coeffs: [a1, a2, a3, ...] for harmonics
                           Default: [1.0] (single fundamental)
        """
        self.register_concept(name, base_frequency, x, y, z)
        
        if harmonic_coeffs is None:
            harmonic_coeffs = [1.0]  # Just fundamental
        
        self.harmonics[name] = harmonic_coeffs
    
    def activate_with_harmonics(self, concept: str, intensity: float = 1.0, depth: float = 1.0):
        """
        Activates concept with its full harmonic structure.
        wave = Σ aₙ · cos(n·ω·t + φₙ)
        """
        if concept not in self.concept_registry:
            return
        
        freq, cx, cy, cz = self.concept_registry[concept]
        harmonics = self.harmonics.get(concept, [1.0])
        
        # Convert normalized coords to grid indices
        ix = int(cx * self.resolution)
        iy = int(cy * self.resolution)
        iz = int(cz * depth * self.resolution)
        
        # Create multi-harmonic wave pattern
        for x in range(self.resolution):
            for y in range(self.resolution):
                for z in range(min(self.resolution, iz + 20)):
                    dist = np.sqrt((x - ix)**2 + (y - iy)**2 + (z - iz)**2)
                    
                    # Sum of harmonics
                    wave_value = 0.0
                    for n, coeff in enumerate(harmonics, start=1):
                        phase = 2 * np.pi * dist / 10.0
                        harmonic_freq = n * freq
                        wave_value += coeff * np.cos(harmonic_freq * self.time + phase)
                    
                    # Normalize and apply decay
                    wave_value *= intensity / len(harmonics)
                    decay = np.exp(-dist**2 / (2 * 10**2))
                    
                    self.field[x, y, z] += wave_value * decay
        
        self.time += 0.1
    
    def analyze_interference(self, threshold: float = 0.2) -> Dict[str, List]:
        """
        Analyzes interference patterns to detect emergent concepts.
        
        Returns:
            {
                "constructive": [(x,y,z, intensity), ...],
                "destructive": [(x,y,z, intensity), ...],
                "emergent_concepts": [description, ...]
            }
        """
        constructive = []
        destructive = []
        
        # Find local maxima (constructive) and minima (destructive)
        for x in range(1, self.resolution - 1):
            for y in range(1, self.resolution - 1):
                for z in range(1, self.resolution - 1):
                    val = self.field[x, y, z]
                    
                    # Check if local extremum
                    neighbors = [
                        self.field[x-1, y, z], self.field[x+1, y, z],
                        self.field[x, y-1, z], self.field[x, y+1, z],
                        self.field[x, y, z-1], self.field[x, y, z+1]
                    ]
                    
                    if val > threshold and all(val >= n for n in neighbors):
                        # Constructive interference (local max)
                        constructive.append((x, y, z, float(val)))
                    elif val < -threshold and all(val <= n for n in neighbors):
                        # Destructive interference (local min)
                        destructive.append((x, y, z, float(val)))
        
        # Interpret emergent concepts
        emergent = []
        if len(constructive) > 0:
            avg_intensity = np.mean([i for _, _, _, i in constructive])
            emergent.append(f"Strong resonance pattern (intensity={avg_intensity:.2f})")
        
        if len(destructive) > 0:
            emergent.append(f"Concept annihilation zones ({len(destructive)} locations)")
        
        return {
            "constructive": constructive[:10],  # Top 10
            "destructive": destructive[:10],
            "emergent_concepts": emergent
        }
    
    def extract_eigenmodes(self, n_modes: int = 3) -> Dict[str, any]:
        """
        Extracts dominant patterns using eigenvalue decomposition.
        
        Returns:
            {
                "eigenvalues": [λ1, λ2, ...],
                "dominant_mode": description,
                "mode_energies": [E1, E2, ...]
            }
        """
        # Flatten 3D field to 2D for eigendecomposition
        # Use XY plane average across Z
        field_2d = np.mean(self.field, axis=2)
        
        # Eigendecomposition
        eigenvalues, eigenvectors = np.linalg.eig(field_2d)
        
        # Sort by absolute eigenvalue
        idx = np.abs(eigenvalues).argsort()[::-1]
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]
        
        # Extract top modes
        top_eigenvalues = eigenvalues[:n_modes]
        mode_energies = np.abs(top_eigenvalues)
        
        # Interpret dominant mode
        dominant_real = np.real(eigenvalues[0])
        if dominant_real > 0:
            interpretation = "Expansion pattern (positive energy)"
        elif dominant_real < 0:
            interpretation = "Contraction pattern (negative energy)"
        else:
            interpretation = "Neutral balance"
        
        return {
            "eigenvalues": [complex(e) for e in top_eigenvalues],
            "dominant_mode": interpretation,
            "mode_energies": mode_energies.tolist(),
            "energy_ratio": float(mode_energies[0] / np.sum(mode_energies)) if len(mode_energies) > 0 else 0.0
        }
