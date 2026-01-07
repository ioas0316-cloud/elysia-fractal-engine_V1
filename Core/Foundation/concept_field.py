"""
Concept Field
=============
A spatial reasoning system where concepts exist in a field and interact
through resonance (wave similarity) and structural affinity (tensor similarity).

This enables non-linear, multi-dimensional cognition beyond simple path-finding.
"""

from typing import Dict, List, Tuple, Set
from dataclasses import dataclass
import math

from Project_Elysia.core_memory import Tensor3D, FrequencyWave

@dataclass
class ConceptNode:
    """A concept with its physical properties in the field."""
    name: str
    tensor: Tensor3D
    wave: FrequencyWave
    activation: float = 0.0  # Current activation level (0.0 to 1.0)

class ConceptField:
    """
    A field where concepts resonate based on structural and vibrational similarity.
    """
    
    def __init__(self):
        self.nodes: Dict[str, ConceptNode] = {}
        self.decay_rate = 0.9  # How fast activation decays
    
    def add_concept(self, name: str, tensor: Tensor3D, wave: FrequencyWave):
        """Adds a concept to the field."""
        self.nodes[name] = ConceptNode(name, tensor, wave)
    
    def activate(self, concept_name: str, intensity: float = 1.0):
        """Activates a concept, sending a wave through the field."""
        if concept_name not in self.nodes:
            return
        
        # Activate the source concept
        self.nodes[concept_name].activation = intensity
        
        # Propagate to similar concepts via resonance
        self._propagate_activation(concept_name)
    
    def _propagate_activation(self, source: str):
        """Propagates activation to resonant concepts."""
        source_node = self.nodes[source]
        
        for name, node in self.nodes.items():
            if name == source:
                continue
            
            # Calculate resonance (wave similarity)
            resonance = self._calculate_resonance(source_node.wave, node.wave)
            
            # Calculate shape affinity (tensor similarity)
            affinity = self._calculate_shape_affinity(source_node.tensor, node.tensor)
            
            # Combined influence
            influence = (resonance + affinity) / 2.0
            
            # Activate proportionally
            node.activation = min(1.0, node.activation + source_node.activation * influence * 0.5)
    
    def _calculate_resonance(self, wave1: FrequencyWave, wave2: FrequencyWave) -> float:
        """
        Calculates how much two waves resonate (0.0 to 1.0).
        Higher = more similar frequency.
        """
        freq_diff = abs(wave1.frequency - wave2.frequency)
        max_freq = max(wave1.frequency, wave2.frequency, 1.0)
        
        # Normalize to 0-1, where 0 = identical frequency
        similarity = 1.0 - min(1.0, freq_diff / max_freq)
        return similarity
    
    def _calculate_shape_affinity(self, tensor1: Tensor3D, tensor2: Tensor3D) -> float:
        """
        Calculates structural similarity between two tensors (0.0 to 1.0).
        Uses cosine similarity of the tensor vectors.
        """
        # Calculate dot product
        dot = tensor1.x * tensor2.x + tensor1.y * tensor2.y + tensor1.z * tensor2.z
        
        # Calculate magnitudes
        mag1 = math.sqrt(tensor1.x**2 + tensor1.y**2 + tensor1.z**2)
        mag2 = math.sqrt(tensor2.x**2 + tensor2.y**2 + tensor2.z**2)
        
        if mag1 == 0 or mag2 == 0:
            return 0.0
        
        # Cosine similarity (-1 to 1), normalize to (0 to 1)
        cosine_sim = dot / (mag1 * mag2)
        return (cosine_sim + 1.0) / 2.0
    
    def get_activated_concepts(self, threshold: float = 0.1) -> List[Tuple[str, float]]:
        """Returns concepts with activation above threshold, sorted by activation."""
        activated = [
            (name, node.activation)
            for name, node in self.nodes.items()
            if node.activation >= threshold
        ]
        return sorted(activated, key=lambda x: x[1], reverse=True)
    
    def find_resonant_concepts(self, concept_name: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """
        Finds concepts that resonate with the given concept.
        Returns list of (concept_name, resonance_score).
        """
        if concept_name not in self.nodes:
            return []
        
        source_node = self.nodes[concept_name]
        scores = []
        
        for name, node in self.nodes.items():
            if name == concept_name:
                continue
            
            # Combined resonance and shape affinity
            resonance = self._calculate_resonance(source_node.wave, node.wave)
            affinity = self._calculate_shape_affinity(source_node.tensor, node.tensor)
            combined = (resonance + affinity) / 2.0
            
            scores.append((name, combined))
        
        # Sort by score and return top k
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]
    
    def find_shape_analogs(self, concept_name: str, top_k: int = 3) -> List[Tuple[str, float]]:
        """
        Finds concepts with similar Tensor shape (for metaphor generation).
        """
        if concept_name not in self.nodes:
            return []
        
        source_node = self.nodes[concept_name]
        scores = []
        
        for name, node in self.nodes.items():
            if name == concept_name:
                continue
            
            affinity = self._calculate_shape_affinity(source_node.tensor, node.tensor)
            scores.append((name, affinity))
        
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]
    
    def decay_activation(self):
        """Decays all activation levels (simulates time passing)."""
        for node in self.nodes.values():
            node.activation *= self.decay_rate
    
    def reset(self):
        """Resets all activations to zero."""
        for node in self.nodes.values():
            node.activation = 0.0
