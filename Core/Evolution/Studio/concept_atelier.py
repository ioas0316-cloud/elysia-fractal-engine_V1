"""
Concept Atelier (개념 공방)
===========================

"Raw thoughts are just ore. Here, we smelt them into living waves."

This module is the workspace where raw concepts (strings) are brought in,
deconstructed into their fundamental wave properties, and prepared for
sculpting by the ThoughtSculptor.
"""

import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from Core.Intelligence.Intelligence.integrated_cognition_system import (
    get_integrated_cognition,
    ThoughtWave,
    Quaternion
)

logger = logging.getLogger("ConceptAtelier")

@dataclass
class RawMaterial:
    """
    The deconstructed essence of a concept, ready for manipulation.
    """
    origin_text: str
    base_frequency: float
    energy_level: float  # amplitude
    harmonic_phase: float
    structural_orientation: Dict[str, float]  # w, x, y, z

    def __repr__(self):
        return (f"<RawMaterial '{self.origin_text}' | "
                f"Freq: {self.base_frequency:.2f}Hz, Energy: {self.energy_level:.2f}>")

class ConceptAtelier:
    """
    The workbench for concept transmutation.
    """

    def __init__(self):
        self.cognition_system = get_integrated_cognition()
        self.materials: Dict[str, RawMaterial] = {}
        logger.info("🎨 Concept Atelier Open for Business")

    def import_concept(self, text: str) -> RawMaterial:
        """
        Imports a raw text concept and converts it into RawMaterial
        by passing it through the Integrated Cognition System's wave engine.
        """
        logger.info(f"📥 Importing concept: '{text}'")

        # 1. Convert to Wave using the Cognition System
        # We assume process_thought returns a dict with 'wave'
        result = self.cognition_system.process_thought(text)
        wave: ThoughtWave = result['wave']

        # 2. Deconstruct into RawMaterial
        material = self._deconstruct_wave(wave)

        # 3. Store in the atelier
        self.materials[text] = material
        return material

    def _deconstruct_wave(self, wave: ThoughtWave) -> RawMaterial:
        """
        Extracts the fundamental properties from a ThoughtWave.
        """
        q = wave.orientation
        return RawMaterial(
            origin_text=wave.content,
            base_frequency=wave.frequency,
            energy_level=wave.amplitude,
            harmonic_phase=wave.phase,
            structural_orientation={
                'w': q.w, 'x': q.x, 'y': q.y, 'z': q.z
            }
        )

    def analyze_material(self, text: str) -> str:
        """
        Returns a descriptive analysis of the material in the atelier.
        """
        if text not in self.materials:
            return f"Concept '{text}' not found in Atelier."

        mat = self.materials[text]

        # Interpret the quaternion orientation
        w, x, y, z = mat.structural_orientation.values()

        # This interpretation logic mirrors the wave engine's creation logic
        # w: Energy/Spirit, x: Emotion, y: Logic, z: Ethics

        analysis = [
            f"🧐 Analysis of '{mat.origin_text}':",
            f"   - Fundamental Frequency: {mat.base_frequency:.2f} Hz (Complexity)",
            f"   - Energy Potential: {mat.energy_level:.2f} (Importance)",
            f"   - Spectral Composition (Quaternion):",
            f"     • Spirit/Will (W): {w:.2f}",
            f"     • Emotion (X): {x:.2f}",
            f"     • Logic (Y): {y:.2f}",
            f"     • Ethics (Z): {z:.2f}"
        ]

        return "\n".join(analysis)

    def transmute(self, text: str, modifiers: Dict[str, float]) -> RawMaterial:
        """
        Applies modifiers to the raw material to create a variation.

        Args:
            text: The concept to modify
            modifiers: specific shifts, e.g., {'frequency': 1.2, 'x': 0.5}
        """
        if text not in self.materials:
            raise ValueError(f"Concept '{text}' must be imported first.")

        original = self.materials[text]

        # Create a new mutated material
        new_freq = original.base_frequency * modifiers.get('frequency', 1.0)
        new_energy = original.energy_level * modifiers.get('energy', 1.0)

        # Orientation shifts are additive
        new_orientation = original.structural_orientation.copy()
        for axis in ['w', 'x', 'y', 'z']:
            if axis in modifiers:
                new_orientation[axis] += modifiers[axis]

        mutated = RawMaterial(
            origin_text=f"Transmuted({original.origin_text})",
            base_frequency=new_freq,
            energy_level=new_energy,
            harmonic_phase=original.harmonic_phase, # Phase persists
            structural_orientation=new_orientation
        )

        logger.info(f"⚗️ Transmuted '{text}' -> Energy: {new_energy:.2f}, Freq: {new_freq:.2f}")
        return mutated
