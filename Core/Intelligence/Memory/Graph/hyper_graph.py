"""
HyperGraph: The 4D Memory Space
===============================

"A space where concepts orbit each other based on Resonance."

Features:
- HyperNodes: Wrappers around WaveTensors.
- Dynamic Edges: Connections exist only if Resonance > Threshold.
- Holographic Query: Find nodes by Frequency/Phase, not just ID.
"""

from typing import Dict, List, Optional, Set
import logging
from elysia_core import Cell, Organ
from Core.Foundation.Wave.wave_tensor import WaveTensor, Modality

logger = logging.getLogger("Elysia.HyperGraph")

@Cell("HyperGraph")
class HyperGraph:
    """
    The 4D Cognitive Space.
    Nodes are Tensors. Edges are Resonance.
    """
    
    def __init__(self):
        self.nodes: Dict[str, WaveTensor] = {}
        # Adjacency list is now dynamic, but we can cache strong links
        self.resonance_links: Dict[str, Dict[str, float]] = {} 
        
    def add_node(self, name: str, modality: Modality = Modality.LOGIC, **dims):
        """Create or Update a Hyperspace Node."""
        if name not in self.nodes:
            tensor = WaveTensor(name, modality)
            self.nodes[name] = tensor
        else:
            tensor = self.nodes[name]
        
        # Set dimensions
        for k, v in dims.items():
            tensor.set_dimension(k, v)
        
        # Trigger resonance recalibration (Local)
        self._recalibrate_local(name)
        return tensor

    def _recalibrate_local(self, center_id: str):
        """Update resonance links for a specific node."""
        center_node = self.nodes[center_id]
        if center_id not in self.resonance_links:
            self.resonance_links[center_id] = {}
            
        for other_id, other_node in self.nodes.items():
            if center_id == other_id:
                continue
            
            resonance = center_node.resonate_with(other_node)
            if resonance > 0.5: # Threshold for "Connection"
                self.resonance_links[center_id][other_id] = resonance

    def query_by_frequency(self, target_freq: float, tolerance: float = 10.0) -> List[WaveTensor]:
        """
        Holographic Query: Find concepts vibrating at a specific pitch.
        Example: 432Hz = Truth, 741Hz = Expression
        """
        results = []
        for node in self.nodes.values():
            node_freq = node.dimensions.get("frequency", 0)
            if abs(node_freq - target_freq) <= tolerance:
                results.append(node)
        return results

    def get_contextStruct(self, center_id: str) -> Dict[str, float]:
        """Return the 'Gravity Well' around a concept."""
        return self.resonance_links.get(center_id, {})

    def stats(self):
        return {
            "total_nodes": len(self.nodes),
            "total_links": sum(len(links) for links in self.resonance_links.values()),
            "avg_energy": sum(n.get_magnitude() for n in self.nodes.values()) / max(1, len(self.nodes))
        }
