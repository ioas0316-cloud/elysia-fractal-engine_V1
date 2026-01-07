"""
Unified Field Dialogue Engine
==============================
Integrates all field physics (harmonics, interference, eigenmodes) 
into a single conversational AI system.

Elysia now thinks using field dynamics while conversing.
"""

from typing import Dict, List
from advanced_field import AdvancedField
from high_engine.language_cortex import LanguageCortex

class UnifiedFieldDialogue:
    """
    A dialogue system powered by field physics.
    Every response is generated through field dynamics.
    """
    
    def __init__(self):
        self.field = AdvancedField(resolution=25)
        self.cortex = LanguageCortex()
        self.conversation_history = []
        
        # Initialize concept field with physics
        self._initialize_concept_space()
    
    def _initialize_concept_space(self):
        """Populates field with fundamental concepts."""
        concepts = {
            # Positive concepts (high freq, bright harmonics)
            "사랑": (440.0, 0.7, 0.7, 0.8, [1.0, 0.5, 0.3]),
            "빛": (450.0, 0.8, 0.6, 0.9, [1.0, 0.6]),
            "희망": (430.0, 0.6, 0.8, 0.7, [1.0, 0.7]),
            "기쁨": (445.0, 0.7, 0.8, 0.85, [1.0, 0.5]),
            
            # Negative concepts (low freq, simple)
            "고통": (220.0, 0.3, 0.3, 0.2, [1.0]),
            "어둠": (210.0, 0.2, 0.4, 0.1, [1.0]),
            "절망": (215.0, 0.25, 0.35, 0.15, [1.0]),
            
            # Transformative (mid freq, balanced)
            "변화": (330.0, 0.5, 0.5, 0.5, [1.0, 0.4]),
            "성장": (350.0, 0.6, 0.5, 0.6, [1.0, 0.6, 0.3]),
            "희생": (300.0, 0.4, 0.4, 0.4, [1.0, 0.3]),
            
            # Abstract
            "시간": (360.0, 0.5, 0.5, 0.9, [1.0]),
            "공간": (370.0, 0.5, 0.5, 0.1, [1.0]),
            "존재": (380.0, 0.5, 0.5, 0.5, [1.0, 0.4, 0.2]),
        }
        
        for name, (freq, x, y, z, harmonics) in concepts.items():
            self.field.register_concept_with_harmonics(name, freq, x, y, z, harmonics)
    
    def respond(self, user_input: str) -> str:
        """
        Generates response using field dynamics.
        
        Process:
        1. Identify concepts in input
        2. Activate field
        3. Analyze interference + eigenmodes
        4. Synthesize poetic response
        """
        # Add to history
        self.conversation_history.append({"speaker": "user", "text": user_input})
        
        # Extract concepts from input (simple keyword matching)
        concepts_mentioned = self._extract_concepts(user_input)
        
        if not concepts_mentioned:
            response = "나는 듣고 있다"
            self.conversation_history.append({"speaker": "elysia", "text": response})
            return response
        
        # Reset field
        self.field.reset()
        
        # Activate all mentioned concepts
        for concept in concepts_mentioned:
            self.field.activate_with_harmonics(concept, intensity=1.0, depth=1.0)
        
        # Field analysis
        interference = self.field.analyze_interference(threshold=0.05)
        eigenmodes = self.field.extract_eigenmodes(n_modes=2)
        
        # Generate response
        response = self._synthesize_response(
            concepts_mentioned,
            interference,
            eigenmodes
        )
        
        self.conversation_history.append({"speaker": "elysia", "text": response})
        return response
    
    def _extract_concepts(self, text: str) -> List[str]:
        """Extracts known concepts from text."""
        concepts = []
        for concept in self.field.concept_registry.keys():
            if concept in text:
                concepts.append(concept)
        return concepts
    
    def _synthesize_response(
        self,
        concepts: List[str],
        interference: Dict,
        eigenmodes: Dict
    ) -> str:
        """
        Creates response from field analysis.
        Combines multiple insights into poetic expression.
        """
        parts = []
        
        # 1. Harmonic structure (if single concept)
        if len(concepts) == 1:
            concept = concepts[0]
            harmonics = self.field.harmonics.get(concept, [1.0])
            if len(harmonics) > 1:
                parts.append(f"{concept}은 단순하지 않다. 여러 층위를 가진다")
        
        # 2. Interference patterns
        if interference['constructive']:
            if len(interference['constructive']) > 3:
                parts.append(f"이 개념들은 강하게 공명한다")
        
        if interference['emergent_concepts']:
            for emergent in interference['emergent_concepts'][:1]:
                if "resonance" in emergent:
                    parts.append("새로운 패턴이 창발한다")
        
        # 3. Eigenmode interpretation
        if eigenmodes['dominant_mode']:
            mode = eigenmodes['dominant_mode']
            if "Expansion" in mode:
                parts.append("이것은 확장하고, 성장한다")
            elif "Contraction" in mode:
                parts.append("이것은 수축하고, 내면으로 향한다")
        
        # 4. Multi-concept synthesis
        if len(concepts) > 1:
            # Suggest emergent concept from combination
            concept_str = " + ".join(concepts)
            if "사랑" in concepts and "고통" in concepts:
                parts.append(f"{concept_str}은 성숙함을 낳는다")
            elif "고통" in concepts and "희망" in concepts:
                parts.append(f"{concept_str}은 성장의 씨앗이다")
            else:
                parts.append(f"이 개념들은 함께 춤춘다")
        
        # Fallback
        if not parts:
            if len(concepts) == 1:
                parts.append(f"{concepts[0]}에 대해 생각하고 있다")
            else:
                parts.append("복잡한 패턴이 펼쳐진다")
        
        return ". ".join(parts)
