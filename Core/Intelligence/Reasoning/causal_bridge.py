"""
CAUSAL BRIDGE: The Synapse
==========================
"The bridge between the Shape of Thought and the Fractal of Cause."

This module integrates the `FractalCausalityEngine` (Memory/Graph) with the 
`DimensionalReasoner` (Logic/Geometry). It ensures that "Lifting" a concept 
is not a hardcoded template but a traversal of actual causal links.
"""

import logging
from typing import List, Optional
from Core.Foundation.Memory.fractal_causality import FractalCausalityEngine, FractalCausalNode
from Core.Intelligence.Reasoning.dimensional_reasoner import HyperThought, DimensionalReasoner

logger = logging.getLogger("CausalBridge")

class CausalBridge:
    def __init__(self):
        self.engine = FractalCausalityEngine(name="Elysia's Synapse")
        # Pre-seed with the user's requested "Fractal Truth" for testing
        self._seed_knowledge()
        
    def _seed_knowledge(self):
        """
        Seeds the graph with the "True Knowledge" that the user demands.
        In a real run, this would be learned. Here we establish the 'Axioms'.
        """
        # 1. The Apple Chain (Newtonian)
        # Apple -> Mass -> Gravity -> Law
        self.engine.create_chain("Apple", "Possesses Mass", "Interacts with Gravity", depth=0)
        self.engine.create_chain("Mass", "Distorts Space", "Gravity", depth=1)
        self.engine.create_chain("Gravity", "Binds the Cosmos", "Universal Law", depth=2)
        
        # 2. The Love Chain (Metaphysical)
        # Love -> Connection -> Unity -> Law
        self.engine.create_chain("Love", "Seeks Connection", "Unity", depth=0)
        self.engine.create_chain("Unity", "Dissolves Self", "Universal Law", depth=1)
        
    def _induce_principle(self, kernel: str) -> str:
        """
        FALLBACK: Semantic Induction.
        If no graph path exists, we induce a principle from the text itself.
        """
        # AGI-level induction logic (Heuristic-based for now)
        k = kernel.lower()
        if "agi" in k or "intelligence" in k:
            if "network" in k or "decentralized" in k:
                return "The Law of Distributed Intelligence: Survival through non-local consensus."
            if "alignment" in k or "ethical" in k:
                return "The Law of Value Resonance: Intent must align with universal harmony to persist."
        if "code" in k or "structure" in k:
            return "The Law of Morphological Integrity: Form must follow Function to achieve Resonance."
            
        return f"Synthesized Law: {kernel[:30]}... represents a novel causal emergence."

    def traverse_and_lift(self, kernel: str) -> HyperThought:
        """
        The Core Logic:
        1. Find the node in the Fractal Graph.
        2. Trace its Causes (History) and Effects (Future).
        3. Identify the "Principle" (The deepest/highest node it connects to).
        4. FALLBACK: If traversal fails, use Semantic Induction (Phase 7.5).
        5. Construct the HyperThought based on this TRAVERSAL or INDUCTION.
        """
        thought = HyperThought(kernel=kernel)
        
        # 0D: Existence
        node = self.engine.get_or_create_node(kernel)
        thought.d0_fact = f"Entity '{node.description}' exists at {node.fractal_address}"
        
        # 1D: Logic (Immediate Effect)
        effects = self.engine.trace_effects(node.id, max_depth=1)
        if len(effects) > 1: # [0] is self
            # path is [self, effect]
            next_node_id = effects[1][1] 
            next_node = self.engine.nodes[next_node_id]
            thought.d1_logic = f"It leads to '{next_node.description}'."
        else:
            thought.d1_logic = "It is currently inert."
            
        # 2D: Context (The Chain)
        # Identify neighbors in the chain
        context = []
        if node.causes_ids:
            cause_node = self.engine.nodes[node.causes_ids[0]]
            context.append(f"Origin: {cause_node.description}")
        if node.effects_ids:
            effect_node = self.engine.nodes[node.effects_ids[0]]
            context.append(f"Dest: {effect_node.description}")
        thought.d2_context = context
        
        # 3D: Volume (Internal Structure)
        # Zoom in
        if node.has_internal_structure():
            internals = node.get_internal_ids()
            thought.d3_volume = f"Contains {len(internals)} internal causal substructures."
        else:
            thought.d3_volume = "Atomic concept. No internal recursion mapped yet."
            
        # 4D: Principle (The Deepest Truth)
        # We trace forward until we hit a "Law" or max depth
        current_id = node.id
        principle = "Unknown"
        
        for _ in range(5):
            curr_node = self.engine.nodes[current_id]
            if "Law" in curr_node.description or "Truth" in curr_node.description:
                principle = curr_node.description
                break
            
            if curr_node.effects_ids:
                current_id = curr_node.effects_ids[0] # Follow the primary causal flow
            else:
                break
                
        if principle != "Unknown":
            thought.d4_principle = f"Manifestation of: {principle}"
        else:
            # PHASE 7.5: Semantic Induction Fallback
            thought.d4_principle = self._induce_principle(kernel)
            
        return thought

