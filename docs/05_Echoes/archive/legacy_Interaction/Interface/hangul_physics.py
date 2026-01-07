"""
Hangul Physics Module
=====================
Defines the physical properties of Hangul characters (Jamo) and maps them to 3D vectors.
Modernized from Legacy/Project_Elysia/mechanics/hangul_physics.py.
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import random

@dataclass
class JamoPhysics:
    """
    Physical properties of a single Hangul Jamo.
    """
    char: str
    type: str  # 'consonant' or 'vowel'
    roughness: float  # 0.0 (Smooth) to 1.0 (Rough)
    openness: float   # 0.0 (Closed) to 1.0 (Open)
    tension: float    # 0.0 (Lax) to 1.0 (Tense)

    def to_vector(self) -> np.ndarray:
        """Returns the 3D vector representation [roughness, openness, tension]."""
        return np.array([self.roughness, self.openness, self.tension], dtype=np.float32)

class HangulPhysicsEngine:
    def __init__(self):
        self.jamo_map = self._initialize_jamo_physics()
        # Cache vectors for fast lookup
        self.jamo_vectors = {char: jamo.to_vector() for char, jamo in self.jamo_map.items()}

    def _initialize_jamo_physics(self) -> Dict[str, JamoPhysics]:
        """
        Maps Hangul Jamo to physical properties.
        """
        mapping = {}
        
        # --- Consonants (Roughness & Tension) ---
        # Velars (ㄱ, ㅋ, ㄲ) - Rough, explosive
        mapping['ㄱ'] = JamoPhysics('ㄱ', 'consonant', roughness=0.7, openness=0.2, tension=0.4)
        mapping['ㅋ'] = JamoPhysics('ㅋ', 'consonant', roughness=0.9, openness=0.3, tension=0.8)
        mapping['ㄲ'] = JamoPhysics('ㄲ', 'consonant', roughness=1.0, openness=0.1, tension=1.0)
        
        # Alveolars (ㄴ, ㄷ, ㅌ, ㄸ, ㄹ) - Smooth to hard
        mapping['ㄴ'] = JamoPhysics('ㄴ', 'consonant', roughness=0.1, openness=0.4, tension=0.1)
        mapping['ㄷ'] = JamoPhysics('ㄷ', 'consonant', roughness=0.5, openness=0.2, tension=0.5)
        mapping['ㅌ'] = JamoPhysics('ㅌ', 'consonant', roughness=0.8, openness=0.3, tension=0.8)
        mapping['ㄸ'] = JamoPhysics('ㄸ', 'consonant', roughness=0.9, openness=0.1, tension=1.0)
        mapping['ㄹ'] = JamoPhysics('ㄹ', 'consonant', roughness=0.2, openness=0.6, tension=0.2) # Flowing
        
        # Bilabials (ㅁ, ㅂ, ㅍ, ㅃ) - Soft to popping
        mapping['ㅁ'] = JamoPhysics('ㅁ', 'consonant', roughness=0.1, openness=0.3, tension=0.1)
        mapping['ㅂ'] = JamoPhysics('ㅂ', 'consonant', roughness=0.4, openness=0.2, tension=0.3)
        mapping['ㅍ'] = JamoPhysics('ㅍ', 'consonant', roughness=0.7, openness=0.3, tension=0.7)
        mapping['ㅃ'] = JamoPhysics('ㅃ', 'consonant', roughness=0.8, openness=0.1, tension=0.9)
        
        # Sibilants (ㅅ, ㅆ, ㅈ, ㅊ, ㅉ) - Sharp
        mapping['ㅅ'] = JamoPhysics('ㅅ', 'consonant', roughness=0.6, openness=0.4, tension=0.4)
        mapping['ㅆ'] = JamoPhysics('ㅆ', 'consonant', roughness=0.9, openness=0.3, tension=0.9)
        mapping['ㅈ'] = JamoPhysics('ㅈ', 'consonant', roughness=0.5, openness=0.3, tension=0.5)
        mapping['ㅊ'] = JamoPhysics('ㅊ', 'consonant', roughness=0.8, openness=0.4, tension=0.8)
        mapping['ㅉ'] = JamoPhysics('ㅉ', 'consonant', roughness=0.9, openness=0.2, tension=1.0)
        
        # Glottal (ㅇ, ㅎ) - Airy
        mapping['ㅇ'] = JamoPhysics('ㅇ', 'consonant', roughness=0.0, openness=0.8, tension=0.0) # Null sound / Nasal
        mapping['ㅎ'] = JamoPhysics('ㅎ', 'consonant', roughness=0.3, openness=0.9, tension=0.2)

        # --- Vowels (Openness & Direction) ---
        # Bright (ㅏ, ㅗ, ㅑ, ㅛ) - Outward, Open
        mapping['ㅏ'] = JamoPhysics('ㅏ', 'vowel', roughness=0.1, openness=1.0, tension=0.5)
        mapping['ㅗ'] = JamoPhysics('ㅗ', 'vowel', roughness=0.1, openness=0.8, tension=0.6)
        mapping['ㅑ'] = JamoPhysics('ㅑ', 'vowel', roughness=0.2, openness=1.0, tension=0.7)
        
        # Dark (ㅓ, ㅜ, ㅕ, ㅠ) - Inward, Closed
        mapping['ㅓ'] = JamoPhysics('ㅓ', 'vowel', roughness=0.2, openness=0.6, tension=0.4)
        mapping['ㅜ'] = JamoPhysics('ㅜ', 'vowel', roughness=0.2, openness=0.4, tension=0.5)
        mapping['ㅕ'] = JamoPhysics('ㅕ', 'vowel', roughness=0.3, openness=0.6, tension=0.6)
        
        # Neutral (ㅡ, ㅣ)
        mapping['ㅡ'] = JamoPhysics('ㅡ', 'vowel', roughness=0.1, openness=0.5, tension=0.3)
        mapping['ㅣ'] = JamoPhysics('ㅣ', 'vowel', roughness=0.1, openness=0.7, tension=0.8) # Tense

        return mapping

    def vector_to_jamo(self, vector: np.ndarray) -> str:
        """
        Finds the closest Jamo to the given 3D vector [roughness, openness, tension].
        """
        best_char = 'ㅇ'
        min_dist = float('inf')
        
        for char, jamo_vec in self.jamo_vectors.items():
            dist = np.linalg.norm(vector - jamo_vec)
            if dist < min_dist:
                min_dist = dist
                best_char = char
                
        return best_char

    def get_jamo_vector(self, char: str) -> Optional[np.ndarray]:
        return self.jamo_vectors.get(char)
