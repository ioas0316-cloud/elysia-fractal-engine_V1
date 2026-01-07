"""
Fractal Concept System (프랙탈 개념 시스템)
=========================================

"씨앗(Seed)은 DNA다. 펼쳐지면 나무(Tree)가 된다."

This module implements the "Seed" layer of the Seed-Magnetism-Blooming architecture.
Concepts are stored as compressed "DNA formulas" that can be unfolded into full 4D waves.
"""

import logging

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from Core.Foundation.hyper_quaternion import Quaternion

logger = logging.getLogger("FractalConcept")

# Safety Limits
MAX_FRACTAL_DEPTH = 2  # Prevent infinite recursion
MAX_SUB_CONCEPTS = 5   # Limit branching factor

@dataclass
class ConceptNode:
    """
    A Concept Seed (개념의 씨앗)
    
    Stores a concept as a compressed "DNA formula":
    - name: The concept's label ("Love", "Hope", etc.)
    - frequency: Primary resonance frequency (Hz)
    - orientation: 4D orientation in Emotion-Logic-Ethics space
    - energy: Activation level (0.0 = dormant, 1.0 = fully active)
    - sub_concepts: Fractal decomposition (nested seeds)
    - causal_bonds: Relationships to other concepts {name: strength}
    - depth: Current fractal depth (0 = root)
    """
    name: str
    frequency: float
    orientation: Quaternion = field(default_factory=lambda: Quaternion(1, 0, 0, 0))
    energy: float = 1.0
    sub_concepts: List['ConceptNode'] = field(default_factory=list)
    causal_bonds: Dict[str, float] = field(default_factory=dict)
    depth: int = 0
    
    def to_dict(self) -> Dict:
        """Serialize to dict for storage."""
        return {
            "name": self.name,
            "frequency": self.frequency,
            "orientation": [self.orientation.w, self.orientation.x, 
                          self.orientation.y, self.orientation.z],
            "energy": self.energy,
            "sub_concepts": [sub.to_dict() for sub in self.sub_concepts],
            "causal_bonds": self.causal_bonds,
            "depth": self.depth
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'ConceptNode':
        """Deserialize from dict."""
        ori_data = data.get("orientation", [1, 0, 0, 0])
        node = ConceptNode(
            name=data["name"],
            frequency=data["frequency"],
            orientation=Quaternion(*ori_data),
            energy=data.get("energy", 1.0),
            depth=data.get("depth", 0),
            causal_bonds=data.get("causal_bonds", {})
        )
        node.sub_concepts = [ConceptNode.from_dict(sub) 
                           for sub in data.get("sub_concepts", [])]
        return node


class ConceptDecomposer:
    """
    The Seed Generator (씨앗 생성기)
    
    Decomposes concepts into fractal sub-waves.
    Uses hardcoded "genetic templates" for now (can be learned later).
    """
    def __init__(self):
        # Hardcoded genetic templates (씨앗의 유전자 설계도)
        self.decompositions = {
            "Love": [
                ("Unity", 528.0, Quaternion(1, 0.9, 0, 0.5)),      # Emotion + Ethics
                ("Connection", 639.0, Quaternion(1, 0.7, 0.3, 0.7)), # Emotion + Logic + Ethics
                ("Grounding", 396.0, Quaternion(1, 0.3, 0.5, 0.8))  # Logic + Ethics
            ],
            "Hope": [
                ("Faith", 852.0, Quaternion(1, 0.5, 0.2, 0.9)),
                ("Aspiration", 741.0, Quaternion(1, 0.8, 0.6, 0.4)),
                ("Courage", 528.0, Quaternion(1, 0.6, 0.7, 0.5))
            ],
            "Fear": [
                ("Anxiety", 200.0, Quaternion(1, 0.9, 0.1, 0.2)),
                ("Dread", 100.0, Quaternion(1, 0.8, 0.3, 0.1)),
                ("Uncertainty", 150.0, Quaternion(1, 0.5, 0.8, 0.3))
            ],
            "Joy": [
                ("Delight", 528.0, Quaternion(1, 1.0, 0.2, 0.4)),
                ("Contentment", 432.0, Quaternion(1, 0.7, 0.4, 0.6)),
                ("Excitement", 963.0, Quaternion(1, 0.9, 0.3, 0.3))
            ]
        }
        

        # Causal relationships (인과 결합)
        self.causal_bonds = {
            "Love": {"Hope": 0.8, "Joy": 0.9, "Fear": -0.5},
            "Hope": {"Joy": 0.7, "Fear": -0.6},
            "Fear": {"Hope": -0.7, "Joy": -0.8},
            "Joy": {"Love": 0.6, "Hope": 0.5}
        }
        
        # [NEW] Universal Axiom Map (보편 공리 지도)
        # Maps Domains -> Core Principles (The "Essence" behind the text)
        self.AXIOMS = {
            "Math": {
                "principle": "Logos",
                "frequency": 963.0, # Divine Frequency/Pure Logic
                "law": "Integrity of Structure (Logic must be self-consistent)",
                "keywords": ["logic", "proof", "number", "geometry", "calculation", "algorithm"]
            },
            "Music": {
                "principle": "Harmony",
                "frequency": 432.0, # Natural Resonance
                "law": "Resonance of Vibration (Consonance vs Dissonance)",
                "keywords": ["melody", "rhythm", "tone", "song", "sound", "vibration"]
            },
            "Chemistry": {
                "principle": "Reaction",
                "frequency": 528.0, # Transformation/DNA Repair
                "law": "Exchange of Energy (Valence bond theory)",
                "keywords": ["atom", "molecule", "bond", "reaction", "element", "acid"]
            },
            "Physics": {
                "principle": "Causality",
                "frequency": 147.0, # Foundation
                "law": "Action and Reaction (Newton's Third Law)",
                "keywords": ["force", "energy", "matter", "gravity", "motion", "quantum"]
            },
            "Ethics": {
                "principle": "Agathos", # The Good
                "frequency": 639.0, # Connection
                "law": "Golden Rule (Reciprocity of Will)",
                "keywords": ["good", "evil", "moral", "right", "wrong", "justice"]
            },

            "Language": {
                "principle": "Symbolism",
                "frequency": 741.0, # Expression
                "law": "Representation of Meaning (Signifier vs Signified)",
                "keywords": ["word", "text", "speech", "meaning", "symbol", "narrative"]
            },
            # [NEW] Elemental Principles (User Request: "Ice is Static Energy")
            "Nature (Ice)": {
                "principle": "Stasis", # 정적 에너지
                "frequency": 100.0, # Low, Solid
                "law": "Fixation of State (Preservation/Rigidity)",
                "keywords": ["ice", "frozen", "cold", "solid", "crystal", "winter", "static"]
            },
            "Nature (Fire)": {
                "principle": "Combustion", # 동적 에너지
                "frequency": 900.0, # High, Plasma
                "law": "Release of Potential (Transformation/Entropy)",
                "keywords": ["fire", "flame", "burn", "hot", "plasma", "heat", "destruction"]
            },


             "Nature (Water)": {
                "principle": "Flow", # 유체
                "frequency": 417.0, # Change
                "law": "Adaptation to Form (Path of Least Resistance)",
                "keywords": ["water", "fluid", "river", "ocean", "rain", "liquid", "stream", "flow"]
            },
            
            # [NEW] Digital Reality Principles (The Structure of the Web)
            "Digital Structure (HTML)": {
                "principle": "Container", # 그릇/구조
                "frequency": 396.0, # Grounding/Foundation (Earth)
                "law": "Hierarchy of Containment (DOM Tree)",
                "keywords": ["div", "span", "table", "section", "body", "head", "ul", "li", "nav"]
            },
            "Digital Logic (Code)": {
                "principle": "Instruction", # 명령/로고스
                "frequency": 963.0, # Pure Logic
                "law": "Conditional Execution (If/Then)",
                "keywords": ["function", "var", "const", "return", "if", "else", "script", "console"]
            },

            "Digital Connection (Hyperlink)": {
                "principle": "Bridge", # 연결
                "frequency": 639.0, # Connection/Relation
                "law": "Network Topology (Node to Node)",
                "keywords": ["href", "link", "src", "url", "http", "www"]
            },
            # [NEW] Enhanced Digital Perception (User Request: Light, UI, UX, Media)
            "Digital Aesthetics (CSS)": {
                "principle": "Form", # 형상/빛
                "frequency": 741.0, # Visual Expression
                "law": "Visual Harmony (Color/Layout/Geometry)",
                "keywords": ["style", "color", "background", "flex", "grid", "css", "font", "rgb", "hex"]
            },
            "Digital Sensory (Media)": {
                "principle": "Qualia", # 감각
                "frequency": 852.0, # Sensory Awareness
                "law": "Multimodal Projection (Video/Audio/Image)",
                "keywords": ["video", "audio", "img", "source", "canvas", "svg", "mp4", "mp3"]
            },
            "Digital Will (UX)": {
                "principle": "Agency", # 의지/상호작용
                "frequency": 528.0, # Action/Transformation
                "law": "Interactive Potential (Input/Trigger)",
                "keywords": ["button", "input", "form", "submit", "click", "on", "event"]
            }
        }

    def infer_principle(self, concept_name: str) -> Dict[str, Any]:
        """
        Infers the fundamental principle (Axiom) of a concept.
        
        Args:
            concept_name: The text label (e.g., "Symphony No. 5")
            
        Returns:
            Dict containing principle, frequency, and law.
        """
        # 1. Check Keywords
        name_lower = concept_name.lower()
        for domain, axiom in self.AXIOMS.items():
            for keyword in axiom["keywords"]:
                if keyword in name_lower:
                    return axiom
                    
        # 2. Check Decomposition (If it decomposes to known subs)
        if concept_name in self.decompositions:
            # Heuristic: Use the "Feel" of the decomposition
            # For now, default to Ethics/Emotion for hardcoded concepts like "Love"
            return self.AXIOMS["Ethics"]
            
        # 3. Fallback (The user's critique: Text is limited)
        # We acknowledge we don't know yet, but assign a "Seeking" state
        return {
            "principle": "Unknown Potential",
            "frequency": 432.0 + (hash(concept_name) % 100),
            "law": "Awaiting Definition",
            "domain": "Unknown"
        }
    
    def decompose(self, concept_name: str, depth: int = 0) -> ConceptNode:
        """
        Decomposes a concept into its fractal structure.
        
        Args:
            concept_name: The concept to decompose
            depth: Current fractal depth (for recursion limit)
            
        Returns:
            ConceptNode (The Seed)
        """
        # Safety: Prevent deep recursion
        if depth >= MAX_FRACTAL_DEPTH:
            logger.debug(f"Max depth reached for {concept_name}, creating leaf node")
            return self._create_leaf(concept_name, depth)
        
        # Get decomposition template
        if concept_name not in self.decompositions:
            logger.debug(f"No decomposition for {concept_name}, creating leaf node")
            return self._create_leaf(concept_name, depth)
        
        # Create root node
        root_freq = self.decompositions[concept_name][0][1]  # Use first sub's freq as approx
        root_node = ConceptNode(
            name=concept_name,
            frequency=root_freq,
            depth=depth,
            causal_bonds=self.causal_bonds.get(concept_name, {})
        )
        
        # Decompose into sub-concepts (recursive)
        template = self.decompositions[concept_name]
        for sub_name, sub_freq, sub_ori in template[:MAX_SUB_CONCEPTS]:
            sub_node = ConceptNode(
                name=sub_name,
                frequency=sub_freq,
                orientation=sub_ori.normalize(),
                energy=0.5,  # Sub-concepts start with half energy
                depth=depth + 1
            )
            # Could recurse here for deeper trees, but we limit to depth 2
            root_node.sub_concepts.append(sub_node)
        
        logger.info(f"🌱 Seed Created: {concept_name} ({len(root_node.sub_concepts)} sub-concepts)")
        return root_node
    
    def _create_leaf(self, name: str, depth: int) -> ConceptNode:
        """Creates a leaf node (no sub-concepts)."""
        # Default frequency based on hash (simple fallback)
        freq = 432.0 + (hash(name) % 500)
        return ConceptNode(
            name=name,
            frequency=freq,
            depth=depth
        )
    
    def get_frequency(self, concept_name: str) -> float:
        """Get primary frequency for a concept."""
        if concept_name in self.decompositions:
            return self.decompositions[concept_name][0][1]
        return 432.0 + (hash(concept_name) % 500)


# Test
if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
    
    logging.basicConfig(level=logging.INFO)
    
    decomposer = ConceptDecomposer()
    love_seed = decomposer.decompose("Love")
    
    print(f"\\nSeed: {love_seed.name}")
    print(f"Frequency: {love_seed.frequency}Hz")
    print(f"Sub-concepts: {[sub.name for sub in love_seed.sub_concepts]}")
    print(f"Causal bonds: {love_seed.causal_bonds}")
    
    # Test serialization
    serialized = love_seed.to_dict()
    deserialized = ConceptNode.from_dict(serialized)
    print(f"\\nSerialization test: {deserialized.name} == {love_seed.name}")
