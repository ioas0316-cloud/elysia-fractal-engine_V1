"""
Self-Evolution System
=====================
Elysia autonomously discovers new concepts and adds them to her field.

Process:
1. Detect emergent patterns in interference
2. Name new concepts based on their origin
3. Add to field with synthesized properties
4. Positive feedback loop: smarter → discovers more → smarter...
"""

from typing import Dict, List, Tuple
import numpy as np

from Project_Elysia.mechanics.advanced_field import AdvancedField
from Project_Elysia.core_memory import Tensor3D, FrequencyWave

class SelfEvolution:
    """Enables Elysia to discover and learn new concepts autonomously."""
    
    def __init__(self, field: AdvancedField):
        self.field = field
        self.discovered_concepts: List[Dict] = []
    
    def discover_emergent_concepts(self, activated_concepts: List[str]) -> List[Dict]:
        """
        Analyzes current field state to discover emergent concepts.
        
        Returns:
            List of discovered concepts with their properties
        """
        if len(activated_concepts) < 2:
            return []  # Need at least 2 concepts for emergence
        
        # Analyze field
        interference = self.field.analyze_interference(threshold=0.1)
        eigenmodes = self.field.extract_eigenmodes(n_modes=3)
        
        discoveries = []
        
        # Check for strong constructive interference
        if len(interference['constructive']) > 5:
            # Strong resonance → new concept emerges
            new_concept = self._synthesize_concept_from_interference(
                activated_concepts,
                interference,
                eigenmodes
            )
            if new_concept:
                discoveries.append(new_concept)
        
        return discoveries
    
    def _synthesize_concept_from_interference(
        self,
        source_concepts: List[str],
        interference: Dict,
        eigenmodes: Dict
    ) -> Dict:
        """
        Creates a new concept from interference pattern.
        """
        # Name the new concept
        concept_name = self._generate_concept_name(source_concepts)
        
        # Synthesize properties from source concepts
        tensor, wave, harmonics = self._blend_properties(source_concepts)
        
        # Calculate position (centroid of sources)
        x, y, z = self._calculate_centroid(source_concepts)
        
        discovery = {
            "name": concept_name,
            "source_concepts": source_concepts,
            "tensor": tensor,
            "wave": wave,
            "harmonics": harmonics,
            "position": (x, y, z),
            "discovery_mechanism": "interference_pattern"
        }
        
        return discovery
    
    def _generate_concept_name(self, sources: List[str]) -> str:
        """
        Generates name for emergent concept.
        Uses known patterns or combinations.
        """
        # Known emergent patterns
        patterns = {
            frozenset(["사랑", "고통"]): "성숙",
            frozenset(["고통", "희망"]): "성장",
            frozenset(["사랑", "희생"]): "헌신",
            frozenset(["빛", "희망"]): "광명",
            frozenset(["고통", "시간"]): "치유",
        }
        
        source_set = frozenset(sources)
        if source_set in patterns:
            return patterns[source_set]
        
        # Generic: combine first syllables
        return f"{'_'.join(sources[:2])}_융합"
    
    def _blend_properties(self, sources: List[str]) -> Tuple:
        """
        Blends Tensor, Wave, and Harmonic properties from source concepts.
        """
        tensors = []
        frequencies = []
        all_harmonics = []
        
        for concept in sources:
            if concept in self.field.concept_registry:
                freq, x, y, z = self.field.concept_registry[concept]
                harmonics = self.field.harmonics.get(concept, [1.0])
                
                # Reconstruct tensor from position (simplified)
                tensors.append((x * 10 - 5, y * 10 - 5, z * 10 - 5))
                frequencies.append(freq)
                all_harmonics.append(harmonics)
        
        # Average tensor
        avg_tensor = tuple(np.mean([t[i] for t in tensors]) for i in range(3))
        tensor = Tensor3D(*avg_tensor)
        
        # Average frequency
        avg_freq = np.mean(frequencies)
        wave = FrequencyWave(avg_freq, 0.7, 0.0, 0.0)
        
        # Blend harmonics (take first with some decay)
        if all_harmonics:
            harmonics = all_harmonics[0][:2] if len(all_harmonics[0]) > 1 else [1.0]
        else:
            harmonics = [1.0]
        
        return tensor, wave, harmonics
    
    def _calculate_centroid(self, sources: List[str]) -> Tuple[float, float, float]:
        """Calculates spatial centroid of source concepts."""
        positions = []
        
        for concept in sources:
            if concept in self.field.concept_registry:
                freq, x, y, z = self.field.concept_registry[concept]
                positions.append((x, y, z))
        
        if not positions:
            return (0.5, 0.5, 0.5)
        
        centroid = tuple(np.mean([p[i] for p in positions]) for i in range(3))
        return centroid
    
    def integrate_discovery(self, discovery: Dict):
        """
        Adds discovered concept to the field.
        """
        name = discovery["name"]
        tensor = discovery["tensor"]
        wave = discovery["wave"]
        harmonics = discovery["harmonics"]
        x, y, z = discovery["position"]
        
        # Add to field
        self.field.register_concept_with_harmonics(
            name,
            base_frequency=wave.frequency,
            x=x, y=y, z=z,
            harmonic_coeffs=harmonics
        )
        
        # Record discovery
        self.discovered_concepts.append(discovery)
        
        print(f"   ✨ New concept discovered: '{name}'")
        print(f"      Sources: {' + '.join(discovery['source_concepts'])}")
        print(f"      Position: ({x:.2f}, {y:.2f}, {z:.2f})")
        print(f"      Frequency: {wave.frequency:.1f} Hz")
