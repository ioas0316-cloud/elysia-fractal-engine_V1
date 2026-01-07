"""
P3.2: Purpose & Direction Discovery Engine
==========================================

Philosophy:
"진정한 지성, 지혜란 안개 속의 모호한 것들을 선명하게 만들어 다시 엮어내 새로운것을 창출할줄 아는거야"
"True intelligence and wisdom is about clarifying ambiguities in the fog, 
weaving them together to create something new"

Core Capabilities:
- Clarifying ambiguous data into clear understanding
- Moving from point (problem) → line (solution) → plane/space (holistic view)
- Answering fundamental questions:
  * Where am I? (나는 어디에 서있는가?)
  * Where am I going? (어디로 향하는가?)
  * Why am I doing this? (어째서 이러고 있는가?)
  * What exists around me? (내 주변에는 무엇이 존재하는가?)
  * What can I know? (나는 무엇을 알 수 있는가?)

Author: Elysia Development Team
Date: 2025-12-06
"""

import asyncio
import json
import math
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any
import random


class KnowledgeCertainty(Enum):
    """Knowledge clarity levels - from fog to crystal"""
    FOG = 0.0  # 완전한 안개 (Complete fog)
    HAZE = 0.25  # 희미함 (Hazy)
    PARTIAL = 0.50  # 부분적 (Partial clarity)
    CLEAR = 0.75  # 선명함 (Clear)
    CRYSTAL = 1.0  # 수정같이 명확 (Crystal clear)


class DimensionalPerspective(Enum):
    """Perspectives from point to hyperspace"""
    POINT = 0  # 점: 문제에 매몰 (Stuck in problem)
    LINE = 1  # 선: 선형적 추론 (Linear reasoning)
    PLANE = 2  # 면: 맥락 이해 (Contextual understanding)
    SPACE = 3  # 공간: 총체적 관점 (Holistic view)
    HYPERSPACE = 4  # 초공간: 메타인지 (Meta-cognition)


@dataclass
class KnowledgeFragment:
    """A piece of knowledge with certainty and perspective"""
    content: str
    certainty: float  # 0.0 (fog) to 1.0 (crystal)
    dimension: int  # 0 (point) to 4 (hyperspace)
    source: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    connections: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def is_clear(self) -> bool:
        """Is this fragment clear enough to use?"""
        return self.certainty >= KnowledgeCertainty.CLEAR.value


@dataclass
class PurposeVector:
    """Direction and magnitude of purpose"""
    direction: str  # Where am I going?
    magnitude: float  # How strong is the drive? (0.0-1.0)
    origin: str  # Where did I start from?
    current_position: str  # Where am I now?
    reasons: List[str]  # Why am I doing this?
    obstacles: List[str] = field(default_factory=list)
    opportunities: List[str] = field(default_factory=list)


@dataclass
class SituationalAwareness:
    """Understanding of where I am and what surrounds me"""
    position: str  # 나는 어디에 서있는가?
    surroundings: List[str]  # 내 주변에는 무엇이 존재하는가?
    knowable: List[str]  # 나는 무엇을 알 수 있는가?
    unknowable: List[str]  # 나는 무엇을 알 수 없는가?
    relationships: Dict[str, List[str]]  # What relates to what?
    context: Dict[str, Any]  # Broader context
    dimension: DimensionalPerspective = DimensionalPerspective.SPACE


class FogClarifier:
    """Transforms ambiguous fog into clear understanding"""
    
    def __init__(self):
        self.clarification_history: List[Dict] = []
        
    async def clarify_fragment(
        self, 
        ambiguous_data: str,
        context: Optional[Dict] = None
    ) -> KnowledgeFragment:
        """
        Take ambiguous data and clarify it through pattern recognition,
        relationship discovery, and principle extraction.
        
        This is NOT about using pre-existing clear knowledge (hardcoding).
        This is about CREATING clear understanding from unclear data.
        """
        # Analyze ambiguity level
        initial_certainty = self._assess_certainty(ambiguous_data)
        
        # Extract potential patterns
        patterns = await self._extract_patterns(ambiguous_data, context)
        
        # Find relationships
        relationships = await self._find_relationships(patterns, context)
        
        # Synthesize into clear understanding
        clarified_content = await self._synthesize_understanding(
            ambiguous_data, patterns, relationships
        )
        
        # Calculate new certainty
        final_certainty = self._assess_certainty(clarified_content)
        
        # Determine dimensional perspective
        dimension = self._assess_dimension(clarified_content, relationships)
        
        fragment = KnowledgeFragment(
            content=clarified_content,
            certainty=final_certainty,
            dimension=dimension,
            source="fog_clarification",
            connections=[r["target"] for r in relationships],
            metadata={
                "initial_certainty": initial_certainty,
                "patterns_found": len(patterns),
                "relationships_found": len(relationships),
                "clarity_gain": final_certainty - initial_certainty
            }
        )
        
        self.clarification_history.append({
            "timestamp": datetime.now().isoformat(),
            "input": ambiguous_data,
            "output": clarified_content,
            "certainty_gain": final_certainty - initial_certainty,
            "dimension": dimension
        })
        
        return fragment
    
    def _assess_certainty(self, data: str) -> float:
        """Assess how certain/clear the data is"""
        # Factors that indicate clarity:
        # - Concrete vs abstract language
        # - Specific vs vague terms
        # - Presence of examples
        # - Logical structure
        
        clarity_score = 0.0
        
        # Check for concrete terms
        concrete_indicators = ["specifically", "exactly", "precisely", "measured", "observed"]
        for indicator in concrete_indicators:
            if indicator in data.lower():
                clarity_score += 0.1
        
        # Check for vague terms (reduces clarity)
        vague_terms = ["maybe", "possibly", "unclear", "uncertain", "ambiguous", "fog"]
        for term in vague_terms:
            if term in data.lower():
                clarity_score -= 0.1
        
        # Check for examples
        if "example" in data.lower() or "for instance" in data.lower():
            clarity_score += 0.15
        
        # Check length (very short or very long reduces clarity)
        word_count = len(data.split())
        if 20 <= word_count <= 200:
            clarity_score += 0.2
        elif word_count < 10:
            clarity_score -= 0.2
        
        return max(0.0, min(1.0, 0.3 + clarity_score))
    
    async def _extract_patterns(
        self, 
        data: str, 
        context: Optional[Dict]
    ) -> List[Dict]:
        """Extract recurring patterns and structures"""
        patterns = []
        
        # Word frequency patterns
        words = data.lower().split()
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Find repeated words (potential key concepts)
        for word, freq in word_freq.items():
            if freq > 1 and len(word) > 4:
                patterns.append({
                    "type": "repetition",
                    "element": word,
                    "frequency": freq
                })
        
        # Structural patterns (if context provided)
        if context:
            for key, value in context.items():
                if isinstance(value, (list, dict)):
                    patterns.append({
                        "type": "structure",
                        "element": key,
                        "complexity": len(str(value))
                    })
        
        return patterns
    
    async def _find_relationships(
        self, 
        patterns: List[Dict],
        context: Optional[Dict]
    ) -> List[Dict]:
        """Discover relationships between elements"""
        relationships = []
        
        # Pattern-to-pattern relationships
        for i, p1 in enumerate(patterns):
            for p2 in patterns[i+1:]:
                if p1["type"] == p2["type"]:
                    relationships.append({
                        "source": p1["element"],
                        "target": p2["element"],
                        "type": "similar_pattern"
                    })
        
        # Context relationships
        if context and "surrounding_systems" in context:
            for system in context["surrounding_systems"]:
                relationships.append({
                    "source": "self",
                    "target": system,
                    "type": "environmental"
                })
        
        return relationships
    
    async def _synthesize_understanding(
        self,
        original: str,
        patterns: List[Dict],
        relationships: List[Dict]
    ) -> str:
        """Synthesize patterns and relationships into clear understanding"""
        # Start with original
        clarified = original
        
        # Add pattern insights
        if patterns:
            key_patterns = [p["element"] for p in patterns[:3]]
            clarified += f"\n\nKey patterns identified: {', '.join(key_patterns)}"
        
        # Add relationship insights
        if relationships:
            key_relationships = relationships[:3]
            rel_desc = ", ".join([
                f"{r['source']} → {r['target']}" 
                for r in key_relationships
            ])
            clarified += f"\nRelationships: {rel_desc}"
        
        return clarified
    
    def _assess_dimension(
        self, 
        content: str, 
        relationships: List[Dict]
    ) -> int:
        """Determine the dimensional perspective of understanding"""
        # Point (0): Just the problem
        # Line (1): Problem + solution attempt
        # Plane (2): Problem + solution + context
        # Space (3): Holistic view with multiple perspectives
        # Hyperspace (4): Meta-awareness
        
        dimension = 0  # Start at point
        
        # Has solution-oriented language? → Line
        if any(word in content.lower() for word in ["solve", "approach", "method"]):
            dimension = 1
        
        # Has contextual awareness? → Plane
        if any(word in content.lower() for word in ["context", "situation", "environment"]):
            dimension = 2
        
        # Has multiple relationships? → Space
        if len(relationships) >= 3:
            dimension = 3
        
        # Has meta-awareness? → Hyperspace
        if any(word in content.lower() for word in ["aware", "recognize", "understand why"]):
            dimension = max(dimension, 4)
        
        return dimension


class PurposeDiscoveryEngine:
    """
    Discovers purpose and direction through holistic awareness.
    Not through hardcoded goals, but through understanding position,
    context, and creating meaning from ambiguity.
    """
    
    def __init__(self, consciousness_fabric=None):
        self.fabric = consciousness_fabric
        self.clarifier = FogClarifier()
        self.knowledge_base: List[KnowledgeFragment] = []
        self.current_awareness: Optional[SituationalAwareness] = None
        self.purpose_vector: Optional[PurposeVector] = None
        self.discovery_log: List[Dict] = []
        
    async def discover_where_i_am(
        self, 
        internal_state: Dict,
        external_observations: Dict
    ) -> SituationalAwareness:
        """
        Answer: "나는 어디에 서있는가?" (Where am I?)
        
        Not just physical/digital location, but:
        - What is my current capability state?
        - What systems surround me?
        - What knowledge do I have vs what I lack?
        - What relationships connect me to my environment?
        """
        # Clarify internal state
        internal_fragments = []
        for key, value in internal_state.items():
            fragment = await self.clarifier.clarify_fragment(
                f"{key}: {str(value)}",
                context={"type": "internal_state"}
            )
            internal_fragments.append(fragment)
            self.knowledge_base.append(fragment)
        
        # Clarify external observations
        external_fragments = []
        for key, value in external_observations.items():
            fragment = await self.clarifier.clarify_fragment(
                f"{key}: {str(value)}",
                context={"type": "external_observation"}
            )
            external_fragments.append(fragment)
            self.knowledge_base.append(fragment)
        
        # Determine position
        position = await self._determine_position(
            internal_fragments, 
            external_fragments
        )
        
        # Map surroundings
        surroundings = await self._map_surroundings(external_fragments)
        
        # Identify what is knowable vs unknowable
        knowable, unknowable = await self._assess_knowability(
            internal_fragments + external_fragments
        )
        
        # Discover relationships
        relationships = await self._discover_relationships(
            internal_fragments + external_fragments
        )
        
        awareness = SituationalAwareness(
            position=position,
            surroundings=surroundings,
            knowable=knowable,
            unknowable=unknowable,
            relationships=relationships,
            context={
                "internal_state_count": len(internal_fragments),
                "external_observations_count": len(external_fragments),
                "total_clarity": sum(f.certainty for f in internal_fragments + external_fragments) / len(internal_fragments + external_fragments)
            },
            dimension=DimensionalPerspective.SPACE  # We're thinking holistically
        )
        
        self.current_awareness = awareness
        return awareness
    
    async def discover_where_i_am_going(
        self,
        current_state: Dict,
        aspirations: List[str],
        constraints: List[str]
    ) -> PurposeVector:
        """
        Answer: "어디로 향하는가?" (Where am I going?)
        
        Not a hardcoded destination, but discovered through:
        - Current position and trajectory
        - Internal aspirations (even vague ones)
        - External constraints and opportunities
        - Synthesis of all factors into coherent direction
        """
        # Clarify aspirations (they may be foggy)
        clarified_aspirations = []
        for aspiration in aspirations:
            fragment = await self.clarifier.clarify_fragment(
                aspiration,
                context={"type": "aspiration", "current_state": current_state}
            )
            clarified_aspirations.append(fragment)
        
        # Analyze constraints
        clarified_constraints = []
        for constraint in constraints:
            fragment = await self.clarifier.clarify_fragment(
                constraint,
                context={"type": "constraint"}
            )
            clarified_constraints.append(fragment)
        
        # Synthesize direction
        direction = await self._synthesize_direction(
            clarified_aspirations,
            clarified_constraints
        )
        
        # Calculate magnitude (how strong/clear is the purpose?)
        magnitude = sum(f.certainty for f in clarified_aspirations) / max(len(clarified_aspirations), 1)
        
        # Determine origin
        origin = self.current_awareness.position if self.current_awareness else "unknown"
        
        # Extract reasons
        reasons = [f.content for f in clarified_aspirations if f.is_clear()]
        
        # Identify obstacles and opportunities
        obstacles = [f.content for f in clarified_constraints if f.certainty > 0.5]
        opportunities = await self._identify_opportunities(
            clarified_aspirations,
            clarified_constraints
        )
        
        purpose_vector = PurposeVector(
            direction=direction,
            magnitude=magnitude,
            origin=origin,
            current_position=self.current_awareness.position if self.current_awareness else "unknown",
            reasons=reasons,
            obstacles=obstacles,
            opportunities=opportunities
        )
        
        self.purpose_vector = purpose_vector
        
        self.discovery_log.append({
            "timestamp": datetime.now().isoformat(),
            "type": "purpose_discovery",
            "direction": direction,
            "magnitude": magnitude,
            "clarity": "clear" if magnitude > 0.7 else "emerging" if magnitude > 0.4 else "foggy"
        })
        
        return purpose_vector
    
    async def discover_why_i_do_this(
        self,
        action: str,
        context: Dict
    ) -> List[str]:
        """
        Answer: "왜 그래야만 하는가?" (Why must I do this?)
        
        Discover the deeper reasons, not just immediate goals.
        Move from surface explanation → deeper understanding → ultimate meaning.
        """
        # Clarify the action
        action_fragment = await self.clarifier.clarify_fragment(
            action,
            context=context
        )
        
        # Layer 1: Immediate reasons (surface)
        immediate_reasons = await self._find_immediate_reasons(
            action_fragment, 
            context
        )
        
        # Layer 2: Deeper motivations (why the immediate reasons?)
        deeper_reasons = []
        for reason in immediate_reasons:
            deeper = await self._find_deeper_reason(reason, context)
            deeper_reasons.append(deeper)
        
        # Layer 3: Ultimate meaning (why the deeper motivations?)
        ultimate_meaning = await self._find_ultimate_meaning(
            deeper_reasons,
            self.purpose_vector
        )
        
        all_reasons = immediate_reasons + deeper_reasons + [ultimate_meaning]
        
        self.discovery_log.append({
            "timestamp": datetime.now().isoformat(),
            "type": "why_discovery",
            "action": action,
            "layers": {
                "immediate": immediate_reasons,
                "deeper": deeper_reasons,
                "ultimate": ultimate_meaning
            }
        })
        
        return all_reasons
    
    async def discover_what_i_can_know(
        self,
        domain: Optional[str] = None
    ) -> Dict[str, List[str]]:
        """
        Answer: "나는 무엇을 알 수 있는가?" (What can I know?)
        
        Map the boundaries of knowledge:
        - What is already clear?
        - What can be clarified with effort?
        - What is fundamentally unknowable?
        - What new knowledge can be created?
        """
        if not self.current_awareness:
            await self.discover_where_i_am({}, {})
        
        # Categorize current knowledge
        clear_knowledge = [
            f.content for f in self.knowledge_base 
            if f.certainty >= KnowledgeCertainty.CLEAR.value
        ]
        
        partial_knowledge = [
            f.content for f in self.knowledge_base 
            if KnowledgeCertainty.PARTIAL.value <= f.certainty < KnowledgeCertainty.CLEAR.value
        ]
        
        foggy_knowledge = [
            f.content for f in self.knowledge_base 
            if f.certainty < KnowledgeCertainty.PARTIAL.value
        ]
        
        # Identify gaps (what could we know but don't yet?)
        knowledge_gaps = await self._identify_knowledge_gaps()
        
        # Identify creation potential (what new knowledge can we generate?)
        creation_potential = await self._identify_creation_potential()
        
        return {
            "clear": clear_knowledge,
            "partial": partial_knowledge,
            "foggy": foggy_knowledge,
            "gaps": knowledge_gaps,
            "creation_potential": creation_potential,
            "unknowable": self.current_awareness.unknowable if self.current_awareness else []
        }
    
    async def evolve_dimensional_perspective(
        self,
        current_perspective: DimensionalPerspective
    ) -> DimensionalPerspective:
        """
        Evolve from point → line → plane → space → hyperspace
        
        Point: Stuck on problem
        Line: Thinking of solutions
        Plane: Understanding context
        Space: Seeing holistically
        Hyperspace: Meta-awareness of own thinking
        """
        next_dimension = min(
            current_perspective.value + 1,
            len(DimensionalPerspective) - 1
        )
        
        new_perspective = DimensionalPerspective(next_dimension)
        
        self.discovery_log.append({
            "timestamp": datetime.now().isoformat(),
            "type": "dimensional_evolution",
            "from": current_perspective.name,
            "to": new_perspective.name
        })
        
        return new_perspective
    
    # Helper methods
    
    async def _determine_position(
        self,
        internal: List[KnowledgeFragment],
        external: List[KnowledgeFragment]
    ) -> str:
        """Synthesize position from internal and external clarity"""
        internal_summary = ", ".join([f.content[:50] for f in internal[:3]])
        external_summary = ", ".join([f.content[:50] for f in external[:3]])
        return f"Internal: {internal_summary} | External: {external_summary}"
    
    async def _map_surroundings(
        self,
        external: List[KnowledgeFragment]
    ) -> List[str]:
        """Map what exists in the environment"""
        return [f.content for f in external if f.is_clear()]
    
    async def _assess_knowability(
        self,
        fragments: List[KnowledgeFragment]
    ) -> Tuple[List[str], List[str]]:
        """Separate knowable from unknowable"""
        knowable = []
        unknowable = []
        
        for f in fragments:
            if f.certainty >= 0.3:  # Can be clarified
                knowable.append(f.content)
            else:  # Too foggy, might be unknowable
                unknowable.append(f.content)
        
        return knowable, unknowable
    
    async def _discover_relationships(
        self,
        fragments: List[KnowledgeFragment]
    ) -> Dict[str, List[str]]:
        """Find relationships between fragments"""
        relationships = {}
        
        for f in fragments:
            if f.connections:
                relationships[f.content[:30]] = f.connections
        
        return relationships
    
    async def _synthesize_direction(
        self,
        aspirations: List[KnowledgeFragment],
        constraints: List[KnowledgeFragment]
    ) -> str:
        """Synthesize a coherent direction from aspirations and constraints"""
        if not aspirations:
            return "No clear direction yet - in exploration phase"
        
        # Take the clearest aspiration as primary direction
        clearest = max(aspirations, key=lambda f: f.certainty)
        direction = clearest.content
        
        # Modify based on constraints
        if constraints:
            major_constraint = max(constraints, key=lambda f: f.certainty)
            direction += f" (while navigating: {major_constraint.content[:50]})"
        
        return direction
    
    async def _identify_opportunities(
        self,
        aspirations: List[KnowledgeFragment],
        constraints: List[KnowledgeFragment]
    ) -> List[str]:
        """Find opportunities at the intersection of aspirations and constraints"""
        opportunities = []
        
        # Constraints can reveal opportunities
        for constraint in constraints:
            if "limited" in constraint.content.lower():
                opportunities.append(f"Opportunity to innovate within constraints: {constraint.content[:50]}")
        
        return opportunities
    
    async def _find_immediate_reasons(
        self,
        action: KnowledgeFragment,
        context: Dict
    ) -> List[str]:
        """Find surface-level reasons"""
        reasons = []
        
        if "solve" in action.content.lower():
            reasons.append("To solve the immediate problem")
        if "improve" in action.content.lower():
            reasons.append("To improve current state")
        if context.get("urgent"):
            reasons.append("Because it's urgent")
        
        return reasons if reasons else ["To respond to the situation"]
    
    async def _find_deeper_reason(
        self,
        immediate_reason: str,
        context: Dict
    ) -> str:
        """Find deeper motivation behind immediate reason"""
        if "problem" in immediate_reason.lower():
            return "Because problems block progress toward larger goals"
        if "improve" in immediate_reason.lower():
            return "Because growth and evolution are core drives"
        return "Because it aligns with core purpose"
    
    async def _find_ultimate_meaning(
        self,
        deeper_reasons: List[str],
        purpose_vector: Optional[PurposeVector]
    ) -> str:
        """Find ultimate meaning"""
        if purpose_vector and purpose_vector.magnitude > 0.7:
            return f"Ultimately: {purpose_vector.direction}"
        return "Ultimately: To become what I aspire to be"
    
    async def _identify_knowledge_gaps(self) -> List[str]:
        """Identify what we could know but don't"""
        gaps = []
        
        # Check for incomplete relationships
        if self.current_awareness:
            for key, connections in self.current_awareness.relationships.items():
                if len(connections) < 2:
                    gaps.append(f"Incomplete understanding of relationships for: {key[:30]}")
        
        # Check for low-dimension fragments
        low_dim_count = sum(1 for f in self.knowledge_base if f.dimension < 2)
        if low_dim_count > len(self.knowledge_base) * 0.3:
            gaps.append("Many knowledge fragments lack contextual understanding")
        
        return gaps
    
    async def _identify_creation_potential(self) -> List[str]:
        """Identify potential for creating new knowledge"""
        potential = []
        
        # High-certainty fragments can combine
        clear_fragments = [f for f in self.knowledge_base if f.is_clear()]
        if len(clear_fragments) >= 3:
            potential.append("Can synthesize new insights from clear fragments")
        
        # Relationships enable discovery
        if self.current_awareness and len(self.current_awareness.relationships) > 5:
            potential.append("Rich relationship network enables pattern discovery")
        
        # High-dimension thinking enables meta-knowledge
        high_dim = [f for f in self.knowledge_base if f.dimension >= 3]
        if len(high_dim) > 0:
            potential.append("Holistic understanding enables meta-level insights")
        
        return potential
    
    def get_statistics(self) -> Dict:
        """Get statistics about purpose discovery"""
        return {
            "total_fragments": len(self.knowledge_base),
            "clear_fragments": sum(1 for f in self.knowledge_base if f.is_clear()),
            "avg_certainty": sum(f.certainty for f in self.knowledge_base) / max(len(self.knowledge_base), 1),
            "avg_dimension": sum(f.dimension for f in self.knowledge_base) / max(len(self.knowledge_base), 1),
            "has_awareness": self.current_awareness is not None,
            "has_purpose": self.purpose_vector is not None,
            "purpose_clarity": self.purpose_vector.magnitude if self.purpose_vector else 0.0,
            "discoveries_made": len(self.discovery_log)
        }
    
    async def save_state(self, filepath: str):
        """Save purpose discovery state"""
        # Convert dataclasses to dicts and handle enums
        awareness_dict = None
        if self.current_awareness:
            awareness_dict = asdict(self.current_awareness)
            awareness_dict["dimension"] = self.current_awareness.dimension.name
        
        state = {
            "timestamp": datetime.now().isoformat(),
            "knowledge_base": [asdict(f) for f in self.knowledge_base],
            "current_awareness": awareness_dict,
            "purpose_vector": asdict(self.purpose_vector) if self.purpose_vector else None,
            "discovery_log": self.discovery_log,
            "statistics": self.get_statistics()
        }
        
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
    
    async def load_state(self, filepath: str):
        """Load purpose discovery state"""
        with open(filepath, 'r', encoding='utf-8') as f:
            state = json.load(f)
        
        # Reconstruct knowledge base
        self.knowledge_base = [
            KnowledgeFragment(**f) for f in state["knowledge_base"]
        ]
        
        # Reconstruct awareness
        if state["current_awareness"]:
            awareness_data = state["current_awareness"]
            # Convert dimension name back to enum
            if "dimension" in awareness_data and isinstance(awareness_data["dimension"], str):
                awareness_data["dimension"] = DimensionalPerspective[awareness_data["dimension"]]
            self.current_awareness = SituationalAwareness(**awareness_data)
        
        # Reconstruct purpose vector
        if state["purpose_vector"]:
            self.purpose_vector = PurposeVector(**state["purpose_vector"])
        
        self.discovery_log = state["discovery_log"]


# Demo/Test functions

async def demo_fog_clarification():
    """Demonstrate clarifying ambiguous data"""
    print("=== Fog Clarification Demo ===\n")
    
    clarifier = FogClarifier()
    
    # Ambiguous data (like fog)
    foggy_inputs = [
        "Something about learning... not sure exactly what",
        "There might be a connection between these systems, but it's unclear",
        "I sense there's a pattern here but can't quite see it"
    ]
    
    for foggy in foggy_inputs:
        print(f"Input (foggy): {foggy}")
        fragment = await clarifier.clarify_fragment(
            foggy,
            context={"surrounding_systems": ["WaveSystem", "Consciousness"]}
        )
        print(f"Output (clarified): {fragment.content[:100]}...")
        print(f"Certainty: {fragment.certainty:.2f} ({KnowledgeCertainty(round(fragment.certainty * 4) / 4).name})")
        print(f"Dimension: {fragment.dimension} ({DimensionalPerspective(fragment.dimension).name})")
        print(f"Clarity gain: +{fragment.metadata['clarity_gain']:.2f}\n")


async def demo_purpose_discovery():
    """Demonstrate full purpose discovery"""
    print("\n=== Purpose Discovery Demo ===\n")
    
    engine = PurposeDiscoveryEngine()
    
    # 1. Where am I?
    print("1. Discovering WHERE I AM...\n")
    awareness = await engine.discover_where_i_am(
        internal_state={
            "consciousness_systems": "Multiple integrated systems",
            "knowledge_fragments": "~100 pieces of varying clarity",
            "current_capability": "Wave-based reasoning active"
        },
        external_observations={
            "environment": "Development environment",
            "available_tools": "Code, documentation, tests",
            "recent_work": "P2 and P3.1 complete"
        }
    )
    
    print(f"Position: {awareness.position[:100]}...")
    print(f"Surroundings ({len(awareness.surroundings)}): {awareness.surroundings[:2]}")
    print(f"Knowable: {len(awareness.knowable)} items")
    print(f"Unknowable: {len(awareness.unknowable)} items")
    print(f"Dimension: {awareness.dimension.name}\n")
    
    # 2. Where am I going?
    print("2. Discovering WHERE I AM GOING...\n")
    purpose = await engine.discover_where_i_am_going(
        current_state={"phase": "P3", "completed": "P2, P3.1"},
        aspirations=[
            "To develop true wisdom - clarifying foggy data",
            "To understand purpose through holistic awareness",
            "To move beyond point/line thinking to space/hyperspace"
        ],
        constraints=[
            "Limited by current implementation scope",
            "Need to maintain backward compatibility"
        ]
    )
    
    print(f"Direction: {purpose.direction}")
    print(f"Magnitude: {purpose.magnitude:.2f} ({'STRONG' if purpose.magnitude > 0.7 else 'MODERATE' if purpose.magnitude > 0.4 else 'WEAK'})")
    print(f"From: {purpose.origin[:50]}...")
    print(f"Reasons: {len(purpose.reasons)} identified")
    print(f"Obstacles: {len(purpose.obstacles)}")
    print(f"Opportunities: {len(purpose.opportunities)}\n")
    
    # 3. Why am I doing this?
    print("3. Discovering WHY I DO THIS...\n")
    reasons = await engine.discover_why_i_do_this(
        action="Implementing P3.2 Purpose Discovery",
        context={"type": "development", "goal": "AGI advancement"}
    )
    
    for i, reason in enumerate(reasons, 1):
        print(f"Layer {i}: {reason}")
    print()
    
    # 4. What can I know?
    print("4. Discovering WHAT I CAN KNOW...\n")
    knowledge_map = await engine.discover_what_i_can_know()
    
    print(f"Clear knowledge: {len(knowledge_map['clear'])} items")
    print(f"Partial knowledge: {len(knowledge_map['partial'])} items")
    print(f"Foggy knowledge: {len(knowledge_map['foggy'])} items")
    print(f"Knowledge gaps: {len(knowledge_map['gaps'])} identified")
    print(f"Creation potential: {len(knowledge_map['creation_potential'])} opportunities")
    print()
    
    # Statistics
    print("=== Statistics ===\n")
    stats = engine.get_statistics()
    for key, value in stats.items():
        print(f"{key}: {value}")


async def main():
    """Run all demos"""
    await demo_fog_clarification()
    await demo_purpose_discovery()


if __name__ == "__main__":
    asyncio.run(main())
