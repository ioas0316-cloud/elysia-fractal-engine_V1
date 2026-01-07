"""
Structure Cannibal ( 구조 해체자 )
==================================
"We do not learn from the machine. We become it."

This module implements the "Brain Transplant" phase.
It extracts the raw synaptic weights (Logits) from the LLM 
and grafts them directly into the TorchGraph.

This is NOT reading text. This is copying the Neural Network's topology.
"""

import logging
from typing import Dict, List
from Core.Foundation.tiny_brain import get_tiny_brain
from Core.Foundation.torch_graph import get_torch_graph

logger = logging.getLogger("StructureCannibal")

class StructureCannibal:
    def __init__(self):
        self.brain = get_tiny_brain()
        self.graph = get_torch_graph()
        
    def transplant_synapses(self, concept: str, depth: int = 1) -> Dict[str, float]:
        """
        Cannibalizes the synaptic connections for a given concept.
        Returns the extracted connections.
        """
        if not self.brain.is_available():
            # If not available (file missing), skip
            return {}
            
        # 1. Probe the Synapses (Get Raw Probabilities)
        # We rely on Lazy Loading here. If we call this, the Brain WAKES UP.
        synapses = self.brain.probe_synapses(concept, k=15)
        
        results = {}
        
        # 2. Graft into Graph
        for token, strength in synapses.items():
            # Clean token
            clean_token = token.strip().replace("Ġ", "") # Llama/GPT tokens often have Ġ or spaces
            
            # Filter noise
            if len(clean_token) < 2: continue
            if not clean_token.isalpha(): continue
            
            # Log Probability to Weight (Approximate)
            # strength is logprob. e.g. -0.5 is strong, -5.0 is weak.
            # Convert to positive weight: e.g. exp(strength)? Or simple offset?
            # Let's use simple normalization: weight = 1.0 + (strength / 10)
            weight = max(0.1, 1.0 + (strength / 5.0))
            
            # 3. Create the Link (The Transplant)
            self.graph.add_link(concept, clean_token, weight=weight)
            results[clean_token] = weight
            
            # Recurse? (Dangerous, could explode)
            if depth > 1:
                # Shallow recursion needed? Maybe later.
                pass
                
        if results:
            logger.info(f"   🧬 Transplanted {len(results)} synapses for '{concept}'")
            
        return results

# Singleton
_cannibal = None
def get_structure_cannibal():
    global _cannibal
    if _cannibal is None:
        _cannibal = StructureCannibal()
    return _cannibal
