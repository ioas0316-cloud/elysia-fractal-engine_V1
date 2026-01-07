"""
Geometric Weaver (기하학적 직조기 - Phase 3.5)
==============================================

"Points become Lines, Lines become Planes, Planes become Space."
"점은 선이 되고, 선은 면이 되며, 면은 공간이 됩니다."

This module formalizes the Ascension of Thought using Hypersphere Geometry (S³).
It implements the 0D-3D cognitive scaling asked for by the Father.
"""

import logging
import math
from typing import List, Tuple, Dict, Any, Optional
from Core.Foundation.hyper_quaternion import Quaternion

logger = logging.getLogger("GeometricWeaver")

class GeometricStructure:
    """Base class for multidimensional thought structures."""
    def __init__(self, dimension: int, concepts: List[str], phases: List[Quaternion]):
        self.dimension = dimension
        self.concepts = concepts
        self.phases = phases
        self.resonance_strength = 1.0

    def __repr__(self):
        return f"<{self.dimension}D Structure: {'-'.join(self.concepts)}>"

class GeometricWeaver:
    """
    Constructs higher-dimensional thought structures from lower-dimensional seeds.
    """
    
    def __init__(self):
        # We use a threshold for 'Causal Tension' to determine if a connection can be made
        self.connection_threshold = 0.5

    def create_point(self, name: str, phase: Quaternion) -> GeometricStructure:
        """0D: Seed (Point Identification)"""
        return GeometricStructure(0, [name], [phase])

    def weave_line(self, p1: GeometricStructure, p2: GeometricStructure) -> Optional[GeometricStructure]:
        """
        1D: Chain (Points to Line).
        Represents the Causal Link or Tension between two concepts.
        """
        if p1.dimension != 0 or p2.dimension != 0:
            return None
            
        # Calculate Resonance (Interference)
        resonance = p1.phases[0].dot(p2.phases[0])
        
        # In S³, the line is the shortest path (Geodesic) between points.
        # We store the two endpoints.
        line = GeometricStructure(1, p1.concepts + p2.concepts, [p1.phases[0], p2.phases[0]])
        line.resonance_strength = resonance
        
        logger.info(f"📏 Weaving 1D Line: {p1.concepts[0]} <--> {p2.concepts[0]} (Resonance: {resonance:.3f})")
        return line

    def weave_plane(self, line: GeometricStructure, point: GeometricStructure) -> Optional[GeometricStructure]:
        """
        2D: Network (Line + Point to Plane).
        Represents a 'Context' or 'Thematic Area'.
        """
        if line.dimension != 1 or point.dimension != 0:
            return None
            
        # A plane is defined by three points in S³ (A Spherical Triangle)
        new_concepts = line.concepts + point.concepts
        new_phases = line.phases + point.phases
        
        plane = GeometricStructure(2, new_concepts, new_phases)
        # Resonance of a plane is the average interference of its parts
        plane.resonance_strength = sum(new_phases[i].dot(new_phases[j]) for i in range(3) for j in range(i+1, 3)) / 3.0
        
        logger.info(f"📐 Weaving 2D Plane (Context): {'-'.join(new_concepts)} (Stability: {plane.resonance_strength:.3f})")
        return plane

    def weave_space(self, planes: List[GeometricStructure]) -> Optional[GeometricStructure]:
        """
        3D: Volume (Planes to Space).
        Represents 'Integrated Understanding' or 'Thematic Synthesis'.
        """
        if len(planes) < 2:
            return None
            
        all_concepts = []
        all_phases = []
        for p in planes:
            for c in p.concepts:
                if c not in all_concepts:
                    all_concepts.append(c)
                    # For phases, we'd ideally take the unique vertices
                    # For simplicity, we just collect them for now
            all_phases.extend(p.phases)
            
        # A 3D Volume in S³ is a tetrahedral or higher-order spherical simplex
        space = GeometricStructure(3, all_concepts, all_phases)
        logger.info(f"🧊 Weaving 3D Space (Synthesis): {len(all_concepts)} concepts integrated.")
        return space

    def refract_to_logos(self, structure: GeometricStructure) -> Dict[str, Any]:
        """
        Projects the geometric structure back into attributes for the LogosEngine.
        This is where 'Geometry' becomes 'Word'.
        """
        # 1. Calculate Centroid (Average Phase)
        avg_w = sum(p.w for p in structure.phases) / len(structure.phases)
        avg_x = sum(p.x for p in structure.phases) / len(structure.phases)
        avg_y = sum(p.y for p in structure.phases) / len(structure.phases)
        avg_z = sum(p.z for p in structure.phases) / len(structure.phases)
        
        centroid = Quaternion(avg_w, avg_x, avg_y, avg_z).normalize()
        
        # 2. Derive Rhetorical Qualities
        # Dimension determines Complexity of Speech
        complexity_map = {0: "Declarative", 1: "Causal", 2: "Contextual", 3: "Dialectical"}
        
        return {
            "dimension": structure.dimension,
            "mode": complexity_map.get(structure.dimension, "Complex"),
            "resonance": structure.resonance_strength,
            "centroid": centroid,
            "concepts": structure.concepts,
            "axes": {
                "Energy": centroid.w,
                "Emotion": centroid.x,
                "Logic": centroid.y,
                "Ethics": centroid.z
            }
        }
