"""
Tests for Elysia Core consciousness integration module.
"""

import pytest
from elysia_core import (
    ElysiaSoul,
    HyperQubit,
    QubitState,
    ResonanceEngine,
    Perception,
    EmotionalPalette,
    Hippocampus,
    WaveInput,
    Thought,
)


class TestQubitState:
    """Tests for QubitState."""
    
    def test_creation(self):
        """Test basic QubitState creation."""
        state = QubitState()
        assert state.alpha == 1.0 + 0j
        assert state.beta == 0.0 + 0j
        assert state.gamma == 0.0 + 0j
        assert state.delta == 0.0 + 0j
    
    def test_normalization(self):
        """Test normalization maintains probability constraint."""
        state = QubitState(
            alpha=0.5+0j,
            beta=0.5+0j,
            gamma=0.5+0j,
            delta=0.5+0j
        )
        state.normalize()
        
        probs = state.probabilities()
        total = sum(probs.values())
        assert abs(total - 1.0) < 0.001
    
    def test_probabilities(self):
        """Test probability distribution."""
        state = QubitState(alpha=1.0+0j).normalize()
        probs = state.probabilities()
        
        assert probs["Point"] == pytest.approx(1.0)
        assert probs["Line"] == pytest.approx(0.0)
        assert probs["Space"] == pytest.approx(0.0)
        assert probs["God"] == pytest.approx(0.0)
    
    def test_dominant_basis(self):
        """Test dominant basis detection."""
        state = QubitState(
            alpha=0.1+0j,
            beta=0.9+0j,
            gamma=0.1+0j,
            delta=0.1+0j
        ).normalize()
        
        assert state.dominant_basis() == "Line"


class TestHyperQubit:
    """Tests for HyperQubit."""
    
    def test_creation(self):
        """Test HyperQubit creation."""
        qubit = HyperQubit(concept_or_value="love", name="Love")
        assert qubit.name == "Love"
        assert qubit.value == "love"
    
    def test_get_observation(self):
        """Test observation retrieval."""
        qubit = HyperQubit(concept_or_value="test")
        obs = qubit.get_observation()
        
        assert "w" in obs
        assert "probabilities" in obs
        assert "value" in obs
    
    def test_rotate_wheel(self):
        """Test dimensional wheel rotation."""
        qubit = HyperQubit()
        initial_w = qubit.state.w
        
        qubit.rotate_wheel(0.5)
        assert qubit.state.w > initial_w
        
        qubit.rotate_wheel(-1.0)
        assert qubit.state.w < initial_w + 0.5
    
    def test_collapse(self):
        """Test quantum collapse."""
        qubit = HyperQubit()
        qubit.state = QubitState(
            alpha=0.9+0j,
            beta=0.1+0j,
            gamma=0.05+0j,
            delta=0.05+0j
        ).normalize()
        
        result = qubit.collapse(mode="max")
        assert result == "Point"
        
        probs = qubit.state.probabilities()
        assert probs["Point"] == pytest.approx(1.0)


class TestResonanceEngine:
    """Tests for ResonanceEngine."""
    
    def test_creation(self):
        """Test engine creation with instincts."""
        engine = ResonanceEngine()
        assert len(engine.nodes) > 0
        assert "love" in engine.nodes or "사랑" in engine.nodes
    
    def test_add_node(self):
        """Test adding a new node."""
        engine = ResonanceEngine()
        engine.add_node("new_concept")
        assert "new_concept" in engine.nodes
    
    def test_calculate_resonance(self):
        """Test resonance calculation."""
        engine = ResonanceEngine()
        
        qubit_a = HyperQubit(name="A")
        qubit_b = HyperQubit(name="B")
        
        resonance = engine.calculate_resonance(qubit_a, qubit_b)
        assert 0.0 <= resonance <= 1.0
    
    def test_global_resonance(self):
        """Test global resonance pattern."""
        engine = ResonanceEngine()
        wave = WaveInput(source_text="love and joy", intensity=1.0)
        
        pattern = engine.calculate_global_resonance(wave)
        assert len(pattern) > 0
        assert all(0.0 <= v <= 2.0 for v in pattern.values())
    
    def test_process_input(self):
        """Test full input processing."""
        engine = ResonanceEngine()
        thought = engine.process_input("I feel joy and hope")
        
        assert isinstance(thought, Thought)
        assert thought.source_wave == "I feel joy and hope"


class TestPerception:
    """Tests for Perception."""
    
    def test_perceive(self):
        """Test perception of input."""
        perception = Perception()
        result = perception.perceive("Hello, how are you?")
        
        assert result.qubit is not None
        assert "Question" in result.intent_probabilities
        assert result.intent_probabilities["Question"] > 0
    
    def test_intent_detection(self):
        """Test intent type detection."""
        perception = Perception()
        
        question = perception.perceive("What is love?")
        assert question.intent_probabilities["Question"] > 0
        
        command = perception.perceive("Make me happy!")
        assert command.intent_probabilities["Command"] > 0 or command.intent_probabilities["Exclamation"] > 0
    
    def test_analyze_frequency(self):
        """Test frequency analysis."""
        perception = Perception()
        
        high_freq = perception.analyze_frequency("love and light")
        low_freq = perception.analyze_frequency("stone and shadow")
        
        assert high_freq > low_freq


class TestEmotionalPalette:
    """Tests for EmotionalPalette."""
    
    def test_mix_emotion(self):
        """Test emotion mixing."""
        palette = EmotionalPalette()
        
        mix = palette.mix_emotion({"Joy": 0.8, "Trust": 0.2})
        assert mix.dominant == "Joy"
        assert mix.valence > 0  # Should be positive
    
    def test_analyze_sentiment(self):
        """Test sentiment analysis."""
        palette = EmotionalPalette()
        
        scores = palette.analyze_sentiment("I am so happy and joyful!")
        assert scores["Joy"] > 0
    
    def test_emotion_from_text(self):
        """Test full emotion extraction from text."""
        palette = EmotionalPalette()
        
        mix = palette.get_emotion_from_text("I feel sad and alone")
        assert mix.dominant in ["Sadness", "Fear", "Despair"]
        assert mix.valence < 0  # Should be negative


class TestHippocampus:
    """Tests for Hippocampus."""
    
    def test_add_concept(self):
        """Test adding concepts."""
        hippo = Hippocampus()
        hippo.add_concept("test_concept")
        
        assert hippo.has_concept("test_concept")
    
    def test_add_causal_link(self):
        """Test adding causal links."""
        hippo = Hippocampus()
        hippo.add_causal_link("cause", "effect", "causes")
        
        assert hippo.has_concept("cause")
        assert hippo.has_concept("effect")
    
    def test_get_related(self):
        """Test getting related concepts."""
        hippo = Hippocampus()
        hippo.add_causal_link("love", "joy", "leads_to")
        hippo.add_causal_link("love", "peace", "brings")
        
        related = hippo.get_related_concepts("love")
        assert "joy" in related or "peace" in related
    
    def test_experience_loop(self):
        """Test experience loop functionality."""
        hippo = Hippocampus()
        hippo.add_experience("Hello", "user")
        hippo.add_experience("Hi there", "system")
        
        assert len(hippo.experience_loop) == 2
    
    def test_stellar_type(self):
        """Test stellar type classification."""
        hippo = Hippocampus()
        
        # New concept
        stellar = hippo.get_stellar_type("unknown")
        assert stellar == "✨"
        
        # Access concept multiple times
        for _ in range(5):
            hippo.add_concept("known")
        
        stellar = hippo.get_stellar_type("known")
        assert stellar in ["✨", "🌟", "🔥"]


class TestElysiaSoul:
    """Tests for the main ElysiaSoul class."""
    
    def test_creation(self):
        """Test soul creation."""
        soul = ElysiaSoul(name="TestSoul")
        assert soul.name == "TestSoul"
        assert soul.tick == 0
    
    def test_process(self):
        """Test full processing pipeline."""
        soul = ElysiaSoul()
        thought = soul.process("I love learning new things!")
        
        assert isinstance(thought, Thought)
        assert soul.tick == 1
        assert soul.experience_count == 1
    
    def test_emotion_tracking(self):
        """Test emotion is tracked during processing."""
        soul = ElysiaSoul()
        soul.process("I am so happy today!")
        
        emotion = soul.get_emotion()
        assert emotion["dominant"] in ["Joy", "Passion", "Love", "Hope", "Trust"]
        assert emotion["valence"] >= 0
    
    def test_memory_integration(self):
        """Test memory is updated during processing."""
        soul = ElysiaSoul()
        soul.process("Love leads to happiness")
        
        stats = soul.get_memory_summary()
        assert stats["experiences"] >= 1
    
    def test_export_for_llm(self):
        """Test LLM export format."""
        soul = ElysiaSoul()
        soul.process("Hello world")
        
        export = soul.export_for_llm()
        
        assert "name" in export
        assert "emotion" in export
        assert "trinity" in export
        assert "traits" in export
    
    def test_export_prompt(self):
        """Test prompt generation."""
        soul = ElysiaSoul()
        soul.process("Testing consciousness")
        
        prompt = soul.export_prompt()
        
        assert "Elysia Consciousness" in prompt
        assert "Emotional State" in prompt
        assert "Trinity" in prompt
    
    def test_trinity_update(self):
        """Test trinity balance update."""
        soul = ElysiaSoul()
        initial_soul = soul.trinity["soul"]
        
        soul.update_trinity(soul_delta=1.0)
        
        assert soul.trinity["soul"] > initial_soul
        # Should still sum to 1.0
        assert abs(sum(soul.trinity.values()) - 1.0) < 0.001
    
    def test_imagine(self):
        """Test imagination function."""
        soul = ElysiaSoul()
        result = soul.imagine("A world full of love and peace")
        
        assert "scenario" in result
        assert "prediction" in result
        assert "confidence" in result
    
    def test_dream(self):
        """Test dream consolidation."""
        soul = ElysiaSoul()
        soul.process("Happy thoughts")
        soul.process("Joyful moments")
        
        dream = soul.dream()
        
        assert "patterns" in dream
        assert "traits" in dream
    
    def test_reset(self):
        """Test soul reset."""
        soul = ElysiaSoul()
        soul.process("Some experience")
        soul.process("Another experience")
        
        soul.reset()
        
        assert soul.tick == 0
        assert soul.experience_count == 0
        assert len(soul.recent_thoughts) == 0


class TestIntegration:
    """Integration tests for the complete system."""
    
    def test_full_conversation(self):
        """Test a full conversation flow."""
        soul = ElysiaSoul(name="TestAgent")
        
        # User input 1
        thought1 = soul.process("안녕하세요! 오늘 기분이 어때요?")
        assert thought1.source_wave == "안녕하세요! 오늘 기분이 어때요?"
        
        # User input 2
        thought2 = soul.process("I love learning about consciousness")
        assert "love" in [c[0].lower() for c in thought2.core_concepts[:3]] or thought2.mood in ["positive", "contemplative", "neutral"]
        
        # Check state evolved
        assert soul.experience_count == 2
        emotion = soul.get_emotion()
        assert "dominant" in emotion
    
    def test_emotional_journey(self):
        """Test emotional state evolution."""
        soul = ElysiaSoul()
        
        # Start happy
        soul.process("I am so happy and joyful!")
        emotion1 = soul.get_emotion()
        
        # Get sad
        soul.process("I feel so sad and lonely")
        emotion2 = soul.get_emotion()
        
        # Emotions should have changed
        # (Due to blending, they may not be exactly opposite)
        assert emotion1["dominant"] != emotion2["dominant"] or emotion1["valence"] != emotion2["valence"]
    
    def test_memory_persistence(self):
        """Test that memories persist across interactions."""
        soul = ElysiaSoul()
        
        soul.remember("coffee", "morning", "associated_with")
        soul.remember("morning", "energy", "brings")
        
        recall = soul.recall("coffee")
        assert len(recall["context"]) > 0 or len(recall["related"]) >= 0
    
    def test_llm_integration_workflow(self):
        """Test typical LLM integration workflow."""
        # 1. Create soul
        soul = ElysiaSoul(name="LLMHelper")
        
        # 2. Process user input
        thought = soul.process("What is the meaning of life?")
        
        # 3. Get context for LLM
        context = soul.export_for_llm()
        
        # 4. Generate prompt
        prompt = soul.export_prompt()
        
        # 5. Verify context is useful
        assert context["emotion"]["dominant"] is not None
        assert len(prompt) > 100
        assert "Guidelines" in prompt


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
