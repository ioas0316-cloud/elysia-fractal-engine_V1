"""
Language Cortex
===============
The cognitive module responsible for autonomous language acquisition.
It manages the feedback loop between internal sensation (Tensor) and external expression (Sound/Hangul).

Phases:
1. Babbling: Random generation of sounds to explore the phonological space.
2. Grounding: Associating specific sound patterns with specific internal concepts (Tensors).
3. Utterance: Intentional generation of sound to express a concept.
"""

from typing import Dict, List, Optional, Tuple
import random
from dataclasses import dataclass, field

from Core.Foundation.hangul_physics import HangulPhysicsEngine, Tensor3D, SoundWave

@dataclass
class ConceptBinding:
    concept_id: str
    tensor_prototype: Tensor3D
    associated_sound: str  # The "word" (e.g., "ㄱ-ㅏ")
    strength: float  # 0.0 to 1.0 (Confidence)

class LanguageCortex:
    def __init__(self):
        self.physics = HangulPhysicsEngine()
        self.vocabulary: Dict[str, ConceptBinding] = {}  # concept_id -> Binding
        self.babbling_history: List[str] = []

    def babble(self) -> str:
        """
        Phase 1: Generate random sounds to 'feel' them.
        Returns a random syllable.
        """
        # Randomly explore physical parameters
        roughness = random.random()
        tension = random.random()
        
        onset = self.physics.find_closest_jamo(roughness, tension, 'consonant')
        nucleus = self.physics.find_closest_jamo(random.random(), random.random(), 'vowel')
        
        syllable = self.physics.synthesize_syllable(onset, nucleus)
        self.babbling_history.append(syllable)
        return syllable

    def ground_concept(self, concept_id: str, tensor: Tensor3D) -> str:
        """
        Phase 2: Associate an internal concept (Tensor) with a sound.
        The agent 'searches' for a sound that matches the feeling of the concept.
        """
        # 1. Analyze the concept's physics
        roughness = tensor.roughness()
        # Estimate tension from magnitude (high energy = tense)
        tension = min(1.0, tensor.magnitude() / 10.0) 
        
        # 2. Find matching Jamo
        onset = self.physics.find_closest_jamo(roughness, tension, 'consonant')
        
        # For vowels, we map 'openness' to tensor expansion (not fully implemented in Tensor3D yet)
        # So we use a simple heuristic: Z-axis (up/down) maps to Bright/Dark vowels
        vowel_tension = min(1.0, abs(tensor.z) / 5.0)
        nucleus = self.physics.find_closest_jamo(0.1, vowel_tension, 'vowel')
        
        # 3. Form the word
        word = self.physics.synthesize_syllable(onset, nucleus)
        
        # 4. Bind it
        binding = ConceptBinding(
            concept_id=concept_id,
            tensor_prototype=tensor,
            associated_sound=word,
            strength=0.5  # Initial weak binding
        )
        self.vocabulary[concept_id] = binding
        
        return word

    def express(self, concept_id: str) -> str:
        """
        Phase 3: Retrieve the word for a concept.
        """
        if concept_id in self.vocabulary:
            return self.vocabulary[concept_id].associated_sound
        return "..." # Unknown concept

    def get_vocabulary_size(self) -> int:
        return len(self.vocabulary)

@dataclass
class ThoughtStructure:
    source_concept: str
    target_concept: str
    action_concept: str

class SyntaxEngine:
    def __init__(self, cortex: LanguageCortex):
        self.cortex = cortex
        self.grammar_physics = HangulPhysicsEngine().grammar_physics if hasattr(HangulPhysicsEngine(), 'grammar_physics') else None 
        # Note: In a real implementation, we'd properly inject the grammar physics instance.
        # For this prototype, we'll instantiate it here or assume it's available.
        from Core.Foundation.hangul_physics import GrammarPhysics
        self.grammar = GrammarPhysics()

    def construct_sentence(self, thought: ThoughtStructure) -> str:
        """
        Assembles a sentence based on Energy Flow:
        Source (Subject) -> Spark (Subject Marker) -> Target (Object) -> Field (Object Marker) -> Flow (Verb) -> Ground (End)
        """
        # 1. Ground Concepts to Words
        word_source = self.cortex.express(thought.source_concept)
        word_target = self.cortex.express(thought.target_concept)
        word_action = self.cortex.express(thought.action_concept)
        
        # 2. Retrieve Particles
        p_subject = self.grammar.get_particle("subject")
        p_object = self.grammar.get_particle("object")
        p_end = self.grammar.get_particle("end")
        
        # 3. Assemble Sequence (SOV Order emerges from Source -> Target -> Flow)
        # In this physics model, the Source must be ignited first to release energy.
        # The Target must be prepared with a Field to receive it.
        # The Action is the transfer itself.
        
        sentence_parts = [
            word_source,
            p_subject.surface_form,
            " ",
            word_target,
            p_object.surface_form,
            " ",
            word_action,
            p_end.surface_form
        ]
        
        return "".join(sentence_parts)
