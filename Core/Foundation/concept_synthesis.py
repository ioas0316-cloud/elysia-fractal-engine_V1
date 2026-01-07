
import logging
import uuid
from typing import List, Tuple, Dict, Any, Optional
from enum import Enum, auto
from .causal_narrative_engine import (
    CausalKnowledgeBase, 
    CausalNode, 
    CausalLink, 
    CausalRelationType
)

logger = logging.getLogger("ConceptSynthesizer")

class EpistemicStatus(Enum):
    DELUSION = "DELUSION"   # Fails workability (Fantasy)
    HYPOTHESIS = "HYPOTHESIS" # New synthesis, unverified
    TRUTH = "TRUTH"         # Verified across multiple phenomena

class PrincipleVerifier:
    """
    Principle Verifier (Law-Testing Engine)
    =======================================
    
    Checks if the internal principle of a synthesis governs the causal
    processes of the phenomenon across different contexts.
    """
    
    def __init__(self, knowledge_base: CausalKnowledgeBase):
        self.kb = knowledge_base

    def derive_internal_law(self, node: CausalNode) -> str:
        """
        Extract the underlying principle from a synthesized concept.
        Simulation: In a full system, this would involve pattern extraction.
        """
        # Logic: If synthesis from Fire (Heat) and Water (Fluid), 
        # the law is 'Thermal expansion of fluids creates pressure/motion'.
        if "Fire" in node.description and "Water" in node.description:
            return "THERMAL_EXPANSION_EXPULSION"
        return "UNKNOWN_PRINCIPLE"

    def verify_workability(self, node: CausalNode, test_phenomena_chains: List[Any]) -> bool:
        """
        Verify if the law derived from this node works in other contexts.
        """
        law = self.derive_internal_law(node)
        node.internal_law = law
        
        if law == "UNKNOWN_PRINCIPLE":
            return False
            
        # Example Test: Does this law work in a Piston Engine?
        # We simulate checking if 'Piston' chain has 'Heat' -> 'Motion'.
        workable_count = 0
        for chain in test_phenomena_chains:
            # Simple check: Does the chain contain elements that match the law's logic?
            # e.g., if law is THERMAL_EXPANSION, does chain have 'Heat' and 'Expansion' or 'Motion'?
            chain_desc = " ".join([self.kb.nodes[nid].description for nid in chain.node_sequence if nid in self.kb.nodes])
            
            if law == "THERMAL_EXPANSION_EXPULSION":
                if "Heat" in chain_desc and ("Expansion" in chain_desc or "Motion" in chain_desc or "Pressure" in chain_desc):
                    workable_count += 1
        
        # If it works in at least one OTHER phenomenon than the original.
        return workable_count >= 1

class ConceptSynthesizer:
    """
    Concept Synthesizer (Idea Breeding Engine)
    =========================================
    
    Philosophy: Thesis + Antithesis -> Synthesis.
    Intelligence is the capacity to combine disparate concepts into new emergent wholes.
    """
    
    def __init__(self, knowledge_base: CausalKnowledgeBase):
        self.kb = knowledge_base

    def find_resonant_pairs(self, threshold: float = 0.7) -> List[Tuple[str, str, float]]:
        """
        Find pairs of nodes that resonate but are not directly linked.
        """
        pairs = []
        node_ids = list(self.kb.nodes.keys())
        
        for i in range(len(node_ids)):
            for j in range(i + 1, len(node_ids)):
                id_a, id_b = node_ids[i], node_ids[j]
                
                # Rule 1: Must resonate above threshold
                score = self.kb.calculate_resonance(id_a, id_b)
                if score < threshold:
                    continue
                
                # Rule 2: Must not have a direct link already (we want leap-frog breeding)
                # Check outgoing from A to B and B to A
                link_exists = False
                for link_id in self.kb.outgoing.get(id_a, []):
                    link = self.kb.links.get(link_id)
                    if link and link.target_id == id_b:
                        link_exists = True
                        break
                
                if not link_exists:
                    for link_id in self.kb.outgoing.get(id_b, []):
                        link = self.kb.links.get(link_id)
                        if link and link.target_id == id_a:
                            link_exists = True
                            break
                
                if not link_exists:
                    pairs.append((id_a, id_b, score))
                    
        # Sort by resonance score descending
        return sorted(pairs, key=lambda x: x[2], reverse=True)

    def synthesize(self, id_a: str, id_b: str, resonance_score: float) -> Optional[CausalNode]:
        """
        Breed two concepts into a new one.
        """
        node_a = self.kb.nodes.get(id_a)
        node_b = self.kb.nodes.get(id_b)
        
        if not node_a or not node_b:
            return None
            
        child_id = f"syn_{uuid.uuid4().hex[:8]}"
        
        # 1. Semantic Synthesis (Simple for now: "A + B")
        # In the future, this could be an LLM-driven synthesis.
        child_description = f"Synthesis of {node_a.description} and {node_b.description}"
        
        # 2. Attribute Inheritance
        child_valence = (node_a.emotional_valence + node_b.emotional_valence) / 2.0
        
        # 3. Sensory Signature Blending
        all_senses = set(node_a.sensory_signature.keys()) | set(node_b.sensory_signature.keys())
        child_signature = {}
        for s in all_senses:
            val_a = node_a.sensory_signature.get(s, 0.0)
            val_b = node_b.sensory_signature.get(s, 0.0)
            child_signature[s] = (val_a + val_b) / 2.0
            
        # 4. Create Child Node
        child_node = CausalNode(
            id=child_id,
            description=child_description,
            is_state=node_a.is_state, # Simplified
            concepts=list(set(node_a.concepts + node_b.concepts)),
            sensory_signature=child_signature,
            emotional_valence=child_valence,
            experience_count=1,
            importance=(node_a.importance + node_b.importance) / 2.0 + 0.1, # Emergent bonus
            epistemic_status=EpistemicStatus.HYPOTHESIS.value
        )
        
        # 5. Integrate into KB
        self.kb.add_node(child_node)
        
        # 6. Create Parental Links (The "Nervous System" expands)
        self.kb.add_link(
            source_id=id_a,
            target_id=child_id,
            relation=CausalRelationType.ASSOCIATED_WITH,
            strength=resonance_score,
            description="Parent of Synthesis"
        )
        self.kb.add_link(
            source_id=id_b,
            target_id=child_id,
            relation=CausalRelationType.ASSOCIATED_WITH,
            strength=resonance_score,
            description="Parent of Synthesis"
        )
        
        logger.info(f"✨ Synthesized new concept: {child_id} ({child_description}) from {id_a} and {id_b}")
        return child_node

    def run_synthesis_cycle(self, limit: int = 5, threshold: float = 0.7) -> List[str]:
        """
        Execute a single generation of idea breeding.
        """
        pairs = self.find_resonant_pairs(threshold=threshold)
        created_ids = []
        
        for i in range(min(limit, len(pairs))):
            id_a, id_b, score = pairs[i]
            child = self.synthesize(id_a, id_b, score)
            if child:
                created_ids.append(child.id)
                
        return created_ids
