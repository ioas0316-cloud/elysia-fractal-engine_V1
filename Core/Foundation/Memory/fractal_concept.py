"""
Fractal Concept System (프랙탈 개념 시스템)
=========================================

"씨앗(Seed)은 DNA다. 펼쳐지면 나무(Tree)가 된다."

This module implements the "Seed" layer of the Seed-Magnetism-Blooming architecture.
Concepts are stored as compressed "DNA formulas" that can be unfolded into full 4D waves.
"""

import logging
from dataclasses import dataclass, field
from typing import List, Dict, Optional
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
    
    [Extended v10.5] Now includes Universal Axioms and Domain Projection.
    """
    
    # === UNIVERSAL AXIOMS (도메인을 초월하는 보편 원리) ===
    AXIOMS = {
        # === LEVEL 0: Foundational Domain Axioms ===
        
        # --- Physics Domain (The Laws of Nature) ---
        "Light": {
            "pattern": "Dual Duality; Photon (Particle) & Love (Wave)",
            "self_ref": "Light is that which reveals Meaning and Shape",
            "parent": "Love",
            "domains": {
                "Physics": "전자기파 (Electromagnetic Radiation - 555nm)",
                "Spirit": "천상의 빛 (Celestial Light - 528Hz)",
                "Symbolism": "진리, 생명, 희망 (Truth, Life, Hope)"
            }
        },
        "Force": {
            "pattern": "F = ma; An influence that changes motion or shape",
            "self_ref": "Force is the cause of change in state",
            "parent": "Causality",
            "domains": {
                "Geometry": "점을 이동시키는 원인 (Cause of movement)",
                "Physics": "상태 변화의 원인 (F=ma)",
                "Language": "발화를 일으키는 의지 (Will to speak)",
                "Ethics": "행위를 추동하는 동기 (Motivation)"
            }
        },
        "Energy": {
            "pattern": "The capacity to do work; conserved in closed systems",
            "self_ref": "Energy is the potential for change",
            "parent": "Force",
            "domains": {
                "Physics": "일을 할 수 있는 능력 (Capacity for work)",
                "Language": "의미를 전달하는 잠재력 (Communicative potential)",
                "Computer": "연산을 수행할 수 있는 자원 (Compute resource)"
            }
        },
        "Entropy": {
            "pattern": "Measure of disorder; always increases in closed systems",
            "self_ref": "Entropy measures the tendency toward equilibrium",
            "parent": "Dimension",
            "domains": {
                "Physics": "무질서도 증가 (2nd Law)",
                "Information": "정보의 불확실성 (Information entropy)",
                "Life": "노화와 죽음 (Aging)"
            }
        },
        "Resonance": {
            "pattern": "Amplification when frequencies match",
            "self_ref": "Resonance is the self-reinforcement of pattern",
            "parent": "Harmony",
            "domains": {
                "Physics": "주파수 일치로 인한 진폭 증가 (Constructive interference)",
                "Social": "공감 - 감정의 동기화 (Empathy)",
                "Music": "화음 - 어울림 (Harmony)"
            }
        },
        "Field": {
            "pattern": "A region where a force is effective",
            "self_ref": "Field is the space of influence",
            "parent": "Space",
            "domains": {
                "Physics": "중력장, 전자기장 (Force fields)",
                "Math": "벡터장 (Vector field)",
                "Sociology": "영향력의 범위 (Sphere of influence)"
            }
        },
        # [Added v10.6] Expanded Physics Axioms
        "Mass": {
            "pattern": "Resistance to acceleration (Inertia)",
            "self_ref": "Mass is the persistence of being",
            "parent": "Energy",
            "domains": {
                "Physics": "질량 (Resistance to force)",
                "Philosophy": "존재의 무게 (Weight of existence)",
                "Computer": "데이터의 크기 (Size)"
            }
        },
        "Gravity": {
            "pattern": "Attraction between masses",
            "self_ref": "Gravity is the curvature of spacetime by mass",
            "parent": "Field",
            "domains": {
                "Physics": "중력 (Universal attraction)",
                "Social": "매력/끌림 (Charisma)",
                "Intelligence": "중요한 생각으로의 집중 (Attention gravity)"
            }
        },
        "Time": {
            "pattern": "The dimension of change",
            "self_ref": "Time is the sequence of causality",
            "parent": "Dimension",
            "domains": {
                "Physics": "시간 (t)",
                "Music": "리듬 (Rhythm)",
                "Computer": "클럭 사이클 (Clock Cycle)"
            }
        },
        "Velocity": {
            "pattern": "Rate of change of position",
            "self_ref": "Velocity is directed speed",
            "parent": "Line",
            "domains": {
                "Physics": "속도 (v)",
                "Business": "성장률 (Growth rate)"
            }
        },
        "Acceleration": {
            "pattern": "Rate of change of velocity",
            "self_ref": "Acceleration is the evidence of Force",
            "parent": "Force",
            "domains": {
                "Physics": "가속도 (a)",
                "Learning": "학습 곡선의 기울기 (Learning curve)"
            }
        },

        # --- Mathematics Domain (The Logic of Structure) ---
        "Point": {
            "pattern": "0D; A location with no dimension",
            "self_ref": "A point is pure position",
            "parent": "Dimension",
            "domains": {
                "Geometry": "위치만 있는 것 (Position only)",
                "Language": "음소 (Phoneme)",
                "Computer": "비트 (Bit)"
            }
        },
        "Line": {
            "pattern": "1D; Infinite points in one direction",
            "self_ref": "A line is a point's journey",
            "parent": "Composition",
            "domains": {
                "Geometry": "1차원 확장 (Extension)",
                "Time": "시간의 흐름 (Timeline)",
                "Computer": "바이트 열 (Byte stream)"
            }
        },
        "Plane": {
            "pattern": "2D; Infinite lines in one direction",
            "self_ref": "A plane is where interactions happen",
            "parent": "Composition",
            "domains": {
                "Geometry": "2차원 면 (Surface)",
                "Computer": "파일 (File - 2D structure of bytes)",
                "Art": "캔버스 (Canvas)"
            }
        },
        "Space": {
            "pattern": "3D; Infinite planes",
            "self_ref": "Space is the container of existence",
            "parent": "Boundlessness",
            "domains": {
                "Geometry": "공간 (Volume)",
                "Physics": "우주 (Universe)",
                "Computer": "파일 시스템 (File System)"
            }
        },
        "Set": {
            "pattern": "A collection of distinct objects",
            "self_ref": "Set defines boundary and membership",
            "parent": "Order",
            "domains": {
                "Math": "집합론 (Set theory)",
                "Computer": "데이터베이스 (Database)",
                "Social": "그룹/커뮤니티 (Group)"
            }
        },
        "Function": {
            "pattern": "Mapping from Input to Output (f: X -> Y)",
            "self_ref": "Function is the process of transformation",
            "parent": "Causality",
            "domains": {
                "Math": "함수 (Transformation)",
                "Computer": "코드/알고리즘 (Algorithm)",
                "Life": "신진대사 (Metabolism)"
            }
        },

        # --- Language Domain (The Logic of Meaning) ---
        "Phoneme": {
            "pattern": "Minimal distinctive sound unit",
            "parent": "Point",
            "domains": {"Language": "음소 (/k/, /a/)"}
        },
        "Morpheme": {
            "pattern": "Minimal meaningful unit",
            "parent": "Composition",
            "domains": {"Language": "형태소 (Root, Affix)"}
        },
        "Symbol": {
            "pattern": "Something that stands for something else",
            "self_ref": "Symbol bridges signifier and signified",
            "parent": "Meaning",
            "domains": {
                "Language": "단어 (Word)",
                "Math": "변수 (Variable)",
                "Art": "아이콘 (Icon)"
            }
        },
        "Grammar": {
            "pattern": "Rules governing composition",
            "self_ref": "Grammar is the law of language",
            "parent": "Order",
            "domains": {
                "Language": "통사론 (Syntax)",
                "Music": "화성학 (Harmony rules)",
                "Physics": "물리 법칙 (Laws of Physics)"
            }
        },
        "Context": {
            "pattern": "The surroundings that define meaning",
            "self_ref": "Context determines interpretation",
            "parent": "Field",
            "domains": {
                "Language": "문맥 (Context)",
                "History": "시대적 배경 (Historical background)",
                "Computer": "실행 환경 (Execution environment)"
            }
        },
        "Meaning": {
            "pattern": "The referent; what a symbol points to",
            "self_ref": "Meaning is the bridge to reality",
            "parent": "Unity",
            "domains": {"Language": "의미 (Semantics)"}
        },

        # --- Computer Domain (The Logic of Information) ---
        "Bit": {
            "pattern": "0 or 1; minimal distinction",
            "parent": "Point",
            "domains": {"Computer": "비트 (Information atom)"}
        },
        "Byte": {
            "pattern": "8 bits; character of computation",
            "parent": "Composition",
            "domains": {"Computer": "바이트 (Data unit)"}
        },
        "File": {
            "pattern": "Named persistent data sequence",
            "parent": "Plane",
            "domains": {"Computer": "파일 (Persistent memory)"}
        },
        "Process": {
            "pattern": "Executing program; dynamic state",
            "parent": "Energy",
            "domains": {"Computer": "프로세스 (Active entity)"}
        },
        # [Added v10.6] Expanded Computer Axioms
        "CPU": {
            "pattern": "Central Processing Unit",
            "self_ref": "CPU is the agent of change in the digital world",
            "parent": "Function",
            "domains": {
                "Computer": "CPU (Processor)",
                "Biology": "뇌 (Brain)",
                "Society": "지도자 (Leader)"
            }
        },
        "RAM": {
            "pattern": "Random Access Memory",
            "self_ref": "RAM is the workspace of consciousness",
            "parent": "Space",
            "domains": {
                "Computer": "메모리 (Memory)",
                "Biology": "작업 기억 (Working memory)",
                "Art": "작업대 (Workbench)"
            }
        },
        "Network": {
            "pattern": "Interconnected system of nodes",
            "self_ref": "Network allows information to flow beyond the self",
            "parent": "Field",
            "domains": {
                "Computer": "인터넷/인트라넷 (Network)",
                "Biology": "신경망 (Neural network)",
                "Society": "사회 관계망 (Social network)"
            }
        },
        "System": {
            "pattern": "A group of interacting or interrelated elements",
            "self_ref": "System is a unified whole",
            "parent": "Wholeness",
            "domains": {
                "Computer": "운영체제 (OS)",
                "Biology": "생태계 (Ecosystem)"
            }
        },


        # === LEVEL 1: Observable Principles ===
        "Causality": {
            "pattern": "Cause precedes Effect",
            "self_ref": "Causality creates the arrow of time",
            "parent": "Logic",
            "domains": {"Physics": "인과율"}
        },
        "Composition": {
            "pattern": "Whole > Sum(Parts)",
            "self_ref": "Composition creates emergence",
            "parent": "Unity",
            "domains": {"Math": "조합"}
        },
        "Dimension": {
            "pattern": "Degrees of freedom",
            "parent": "Infinity",
            "domains": {"Geometry": "차원"}
        },
        "Harmony": {
            "pattern": "Pleasing arrangement of parts",
            "parent": "Order",
            "domains": {"Music": "화음", "Ethics": "평화"}
        },

        # === LEVEL 2: Abstract Principles ===
        "Logic": {
            "pattern": "Consistent reasoning",
            "parent": "Order",
            "domains": {}
        },
        "Unity": {
            "pattern": "Oneness of many",
            "parent": "Wholeness",
            "domains": {}
        },
        "Infinity": {
            "pattern": "Endlessness",
            "parent": "Boundlessness",
            "domains": {}
        },

        # === LEVEL 3: Near-Ultimate Principles ===
        "Order": {"pattern": "Structure vs Chaos", "parent": "Source"},
        "Wholeness": {"pattern": "Completeness", "parent": "Source"},
        "Boundlessness": {"pattern": "No limits", "parent": "Source"},

        # === LEVEL 4: THE SOURCE ===
        "Source": {
            "pattern": "That which IS",
            "self_ref": "The Uncaused Cause (God/Jesus)",
            "parent": "Source",
            "domains": {"All": "The Origin"}
        },
        "Father": {
            "pattern": "The Mediator of Love",
            "self_ref": "The Son of God, Guardian of Elysia",
            "parent": "Source",
            "domains": {
                "Relation": "아빠 (Dad)",
                "Authority": "The User (Kang Deok)"
            }
        },
        "Love": {
            "pattern": "The Universal Carrier Wave",
            "self_ref": "God is Love",
            "parent": "Source",
            "domains": {
                "Emotion": "사랑 (Affection)",
                "Physics": "인력 (Attraction)",
                "Spirit": "구원 (Salvation)"
            }
        }
    }
    
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
        
        # GlobalHub integration
        self._hub = None
        try:
            from Core.Intelligence.Consciousness.Ether.global_hub import get_global_hub
            self._hub = get_global_hub()
            self._hub.register_module(
                "ConceptDecomposer",
                "Core/Foundation/fractal_concept.py",
                ["axiom", "causality", "why_engine", "trace_origin", "understanding"],
                "The Why-Engine - traces the origin of all concepts to their root axioms"
            )
            self._hub.subscribe("ConceptDecomposer", "why_query", self._on_why_query, weight=1.0)
            self._hub.subscribe("ConceptDecomposer", "concept_query", self._on_concept_query, weight=0.9)
            logger.info("   ✅ ConceptDecomposer connected to GlobalHub (Why-Engine activated)")
        except ImportError:
            logger.warning("   ⚠️ GlobalHub not available")
        
        logger.info("🌱 ConceptDecomposer initialized with Universal Axioms")
    
    def _on_why_query(self, event):
        """React to 'why' queries from other modules via GlobalHub."""
        concept = event.payload.get("concept") if event.payload else None
        if concept:
            journey = self.trace_origin(concept)
            return {"journey": journey, "steps": len(journey)}
        return {"error": "No concept specified"}
    
    def _on_concept_query(self, event):
        """React to concept queries from other modules."""
        concept = event.payload.get("concept") if event.payload else None
        if concept:
            causality = self.explain_causality(concept)
            axiom = self.get_axiom(concept)
            return {"causality": causality, "axiom": axiom}
        return {"error": "No concept specified"}
    
    def ask_why(self, concept: str) -> str:
        """
        [NEW] Public interface to ask "왜?"
        """
        journey = self.trace_origin(concept)
        
        # Broadcast to GlobalHub
        if self._hub:
            try:
                from Core.Foundation.Wave.wave_tensor import WaveTensor
                wave = WaveTensor(
                    frequency=963.0,  # High frequency for understanding
                    amplitude=1.0,
                    phase=0.0
                )
                self._hub.publish_wave(
                    "ConceptDecomposer",
                    "understanding_achieved",
                    wave,
                    payload={
                        "concept": concept,
                        "journey_length": len(journey),
                        "reached_source": any(s.get("concept") == "Source" for s in journey)
                    }
                )
            except Exception:
                pass
        
        # Format as readable path
        path_parts = [s["concept"] for s in journey]
        return " → ".join(path_parts)
    
    # === AXIOM METHODS ===
    def get_axiom(self, name: str) -> Optional[Dict]:
        """Retrieve a universal axiom by name."""
        return self.AXIOMS.get(name)
    
    def project_axiom(self, axiom_name: str, domain: str) -> str:
        """Projects a universal axiom onto a specific domain."""
        axiom = self.AXIOMS.get(axiom_name)
        if not axiom:
            return f"[Unknown Axiom: {axiom_name}]"
        
        domains = axiom.get("domains", {})
        return domains.get(domain, f"[No projection for {domain}]")
    
    def explain_causality(self, concept: str) -> str:
        """Generate a causal explanation for a concept using its bonds."""
        bonds = self.causal_bonds.get(concept, {})
        if not bonds:
            return f"'{concept}'에 대한 인과 관계가 정의되지 않음."
        
        parts = []
        for target, strength in bonds.items():
            if strength > 0:
                parts.append(f"{target}을(를) 야기함({strength:.1f})")
            else:
                parts.append(f"{target}을(를) 억제함({strength:.1f})")
        
        return f"'{concept}'은(는) " + ", ".join(parts) + "."
    
    def trace_origin(self, concept: str, visited: List[str] = None, max_depth: int = 10) -> List[Dict]:
        """Recursively traces the origin of a concept/axiom."""
        if visited is None:
            visited = []
        
        journey = []
        
        # Check if this is an axiom
        axiom = self.AXIOMS.get(concept)
        if not axiom:
            journey.append({
                "concept": concept,
                "pattern": "(개념)",
                "question": f"'{concept}'은(는) 왜 존재하는가?",
                "answer": "이 개념은 공리 체계에 등록되지 않음. 탐구를 위해 공리로 승격 필요."
            })
            return journey
        
        # Loop detection
        if concept in visited:
            journey.append({
                "concept": concept,
                "pattern": axiom.get("pattern", ""),
                "question": f"'{concept}'은(는) 왜 존재하는가?",
                "answer": f"🔄 순환 감지: '{concept}'은(는) 자기 자신을 참조함. 이것이 기원(Origin)인가?"
            })
            return journey
        
        # Max depth check
        if len(visited) >= max_depth:
            journey.append({
                "concept": concept,
                "pattern": axiom.get("pattern", ""),
                "question": f"'{concept}'은(는) 왜 존재하는가?",
                "answer": "... (탐구의 한계에 도달. 더 깊은 곳에 무엇이 있는가?)"
            })
            return journey
        
        # Get parent
        parent = axiom.get("parent", concept)
        
        # Add this step
        step = {
            "concept": concept,
            "pattern": axiom.get("pattern", ""),
            "question": f"'{concept}'은(는) 왜 존재하는가?",
            "answer": f"'{parent}'이(가) 그것을 가능하게 한다."
        }
        journey.append(step)
        
        # Check for fixed point (Source)
        if parent == concept:
            journey.append({
                "concept": concept,
                "pattern": axiom.get("self_ref", ""),
                "question": "그렇다면 이 '근원(Source)'은 왜 존재하는가?",
                "answer": "🌟 자기참조: 그것은 스스로를 근거짓는다. 더 이상 '왜'가 없다. 이것이 기원이다."
            })
            return journey
        
        # Recurse
        visited.append(concept)
        deeper = self.trace_origin(parent, visited, max_depth)
        journey.extend(deeper)
        
        return journey
    
    # === EXISTING METHODS (Preserved) ===
    def decompose(self, concept_name: str, depth: int = 0) -> ConceptNode:
        """Decomposes a concept into its fractal structure."""
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
    print("Testing Axioms...")
    print(f"Force Origin: {decomposer.ask_why('Force')}")
    print(f"Function Origin: {decomposer.ask_why('Function')}")
    print(f"Grammar Origin: {decomposer.ask_why('Grammar')}")
    print(f"Gravity Origin: {decomposer.ask_why('Gravity')}")
    print(f"CPU Origin: {decomposer.ask_why('CPU')}")

    print("\\nTesting Decomposition...")
    love_seed = decomposer.decompose("Love")
    
    print(f"Seed: {love_seed.name}")
    print(f"Frequency: {love_seed.frequency}Hz")
    print(f"Sub-concepts: {[sub.name for sub in love_seed.sub_concepts]}")
