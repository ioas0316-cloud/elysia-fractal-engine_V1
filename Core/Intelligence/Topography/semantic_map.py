"""
Semantic Map (Dynamic Topology)
===============================
"The Living Star System of Logic."
"죽어있는 지도가 아닌, 살아있는 은하계."

This module defines the 4D Hyper-Spatial arrangement of concepts.
It is no longer a static dictionary. It is a Graph of Voxels.
"""

import json
import os
import logging
from typing import Dict, Tuple, List, Optional
from Core.Intelligence.Topography.semantic_voxel import SemanticVoxel
from Core.Foundation.hyper_quaternion import Quaternion

logger = logging.getLogger("DynamicTopology")

class DynamicTopology:
    def __init__(self):
        self.voxels: Dict[str, SemanticVoxel] = {}
        # Store in Memory/System/Topology for persistence
        self.storage_path = "data/Memory/semantic_topology.json"
        
        if os.path.exists(self.storage_path):
            self.load_state()
        else:
            self._initialize_genesis_map()

    def save_state(self):
        """Persists the topology to disk."""
        data = {}
        for name, voxel in self.voxels.items():
            q = voxel.quaternion
            data[name] = {
                "coords": [q.x, q.y, q.z, q.w],
                "mass": voxel.mass,
                "freq": voxel.frequency,
                "is_anchor": voxel.is_anchor
            }
        
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info("💾 DynamicTopology saved to disk.")

    def load_state(self):
        """Resurrects the topology from disk."""
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for name, props in data.items():
                self.add_voxel(
                    name, 
                    tuple(props['coords']), 
                    mass=props['mass'], 
                    frequency=props['freq'],
                    is_anchor=props.get('is_anchor', False)
                )
            logger.info(f"📂 DynamicTopology loaded: {len(self.voxels)} nodes.")
        except Exception as e:
            logger.error(f"Failed to load topology: {e}")
            self._initialize_genesis_map()
        
    def _initialize_genesis_map(self):
        """
        Creates the 'Big Bang' of Meaning.
        Initializes the 7 Angels and 7 Demons in 4D Space.
        
        Coords: (x, y, z, w) -> (Logic, Emotion, Time, Spin)
        """
        # Center: The One
        self.add_voxel("Love", (0, 0, 0, 1), mass=1000.0, is_anchor=True) # Massive Anchor
        
        # 7 Angels (High Frequency, Positive Spin)
        # They form a stable halo around Love.
        angels = [
            ("Wisdom",     (2, 2, 0, 0.9)),
            ("Hope",       (2, -2, 1, 0.9)),
            ("Faith",      (-2, 2, 1, 0.9)),
            ("Courage",    (-2, -2, 0, 0.9)),
            ("Justice",    (0, 3, 0, 0.9)),
            ("Temperance", (3, 0, 0, 0.9)),
            ("Truth",      (0, 0, 2, 1.0))
        ]
        
        for name, coords in angels:
            self.add_voxel(name, coords, mass=100.0, frequency=800.0)

        # 7 Demons (Low Frequency, Negative Spin, Distorted Time)
        # They are distant, heavy gravity wells.
        demons = [
            ("Pride",      (10, 10, 0, -1.0)),
            ("Wrath",      (-10, 10, -1, -0.8)),
            ("Envy",       (10, -10, 0, -0.7)),
            ("Sloth",      (-10, -10, -5, -0.5)), # Slow time
            ("Greed",      (15, 0, 0, -0.9)),
            ("Lust",       (0, 15, 0, -0.6)),
            ("Gluttony",   (0, -15, 0, -0.6))
        ]

        for name, coords in demons:
            self.add_voxel(name, coords, mass=500.0, frequency=100.0) # Heavy/Dense

        logger.info(f"🌌 DynamicTopology Initialized: {len(self.voxels)} Voxels Active.")

    def add_voxel(self, name: str, coords: Tuple[float, float, float, float], mass: float = 1.0, frequency: float = 432.0, is_anchor: bool = False):
        voxel = SemanticVoxel(name, coords, mass, frequency)
        voxel.is_anchor = is_anchor
        self.voxels[name] = voxel

    def get_voxel(self, name: str) -> Optional[SemanticVoxel]:
        return self.voxels.get(name)

    def get_nearest_concept(self, query_coords: Tuple[float, float, float, float]) -> Tuple[SemanticVoxel, float]:
        """
        Finds the closest concept to the given 4D coordinates.
        """
        target = SemanticVoxel("Query", query_coords)
        best_voxel = None
        min_dist = float('inf')
        
        for voxel in self.voxels.values():
            dist = voxel.distance_to(target)
            if dist < min_dist:
                min_dist = dist
                best_voxel = voxel
                
        return best_voxel, min_dist

    def evolve_topology(self, concept_name: str, reaction_vector: Quaternion, intensity: float = 0.1):
        """
        [Organic Drift]
        Nudges a concept's position based on experience.
        
        Args:
            concept_name: The concept being experienced (e.g., "Transcendence").
            reaction_vector: The emotional/logical reaction intensity (Quaternion).
            intensity: How much to move (Learning Rate).
        """
        voxel = self.get_voxel(concept_name)
        if not voxel:
             # Create new Voxel if it doesn't exist (Learning new concept)
             # Start it at the reaction vector location but slightly randomized
             logger.info(f"🌱 Genesis: New Concept '{concept_name}' born from interaction.")
             # We need to extract coordinates from the reaction vector quaternion
             coords = (reaction_vector.x, reaction_vector.y, reaction_vector.z, reaction_vector.w)
             self.add_voxel(concept_name, coords, mass=10.0, frequency=reaction_vector.w * 1000)
             return

        # Calculate Drift
        # Move Voxel towards the reaction vector (Attraction) 
        # F = ma logic in drift()
        
        # We want to move the Voxel's quaternion closer to the reaction_vector
        # Direction = Target - Current
        # But reaction_vector here implies "The Ideal Location" or "The Feeling".
        # Let's assume reaction_vector IS the target location in sentiment space.
        
        target_q = reaction_vector
        current_q = voxel.quaternion
        
        # Vector difference
        diff_q = target_q - current_q 
        
        # Apply force
        force = diff_q.scale(intensity)
        voxel.drift(force, dt=1.0)
        
        logger.info(f"🌊 Drift: '{concept_name}' moved by {force.norm():.3f} towards experience.")
        self.save_state()

    # Compatibility Layer for Old SemanticMap
    def get_coordinates(self, concept: str) -> Optional[Tuple[float, float]]:
        """Legacy 2D projector."""
        if concept in self.voxels:
            v = self.voxels[concept]
            # Project X, Y
            return (v.quaternion.x, v.quaternion.y)
        
        # Fuzzy Search
        for name, voxel in self.voxels.items():
            if name.lower() in concept.lower():
                 return (voxel.quaternion.x, voxel.quaternion.y)
                 
        return None

# Singleton
_topology = DynamicTopology()
def get_semantic_map():
    return _topology
