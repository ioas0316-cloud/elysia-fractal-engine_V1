"""
The Void (Ether Space)
======================

"The container of all things, which itself is nothing."

This module defines the `Void` (Space), the container that holds `EtherNode`s.
It is not just a list; it is a topological space that manages the interactions (The Field).
"""

import logging
from typing import Dict, List, Optional, Tuple
from Core.Intelligence.Consciousness.Ether.ether_node import EtherNode, Quaternion

logger = logging.getLogger("Void")

class Void:
    """
    The 4D Space where EtherNodes exist and interact.
    """
    def __init__(self, name: str = "Prime"):
        self.name = name
        self.nodes: Dict[str, EtherNode] = {}
        self.time_scale: float = 1.0

        # Spatial Partitioning (Octree/Grid) could go here for optimization
        # For now, we use a flat list for purity of concept.

    def add(self, node: EtherNode):
        """Injects a node into the Void."""
        self.nodes[node.id] = node
        # logger.debug(f"Node injected into Void: {node}")

    def remove(self, node_id: str):
        # [Wave Logic] Consider resonance-based lookup instead of direct membership check
        # Original: if node_id in self.nodes:
        if node_id in self.nodes:  # TODO: Convert to query_resonance
            del self.nodes[node_id]

    def get(self, node_id: str) -> Optional[EtherNode]:
        return self.nodes.get(node_id)

    def get_all(self) -> List[EtherNode]:
        return list(self.nodes.values())

    def count(self) -> int:
        return len(self.nodes)

    def total_energy(self) -> float:
        return sum(n.energy for n in self.nodes.values())

    def total_mass(self) -> float:
        return sum(n.mass for n in self.nodes.values())

    def get_active_nodes(self, threshold: float = 0.5) -> List[EtherNode]:
        return [n for n in self.nodes.values() if n.energy > threshold]

    def find_nearest(self, position: Quaternion, limit: int = 5) -> List[EtherNode]:
        """Finds nodes spatially closest to a 4D point."""
        # This is O(N). In production, use KD-Tree or Octree.
        sorted_nodes = sorted(
            self.nodes.values(),
            key=lambda n: self._distance_sq(n.position, position)
        )
        return sorted_nodes[:limit]

    def _distance_sq(self, q1: Quaternion, q2: Quaternion) -> float:
        return (q1.w-q2.w)**2 + (q1.x-q2.x)**2 + (q1.y-q2.y)**2 + (q1.z-q2.z)**2

    def clear(self):
        self.nodes.clear()
