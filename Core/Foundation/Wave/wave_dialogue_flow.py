"""
Wave-Based Dialogue Flow (파동 기반 대화 흐름)
============================================

"사고는 파동이고, 감정은 주파수며, 대화는 공명이다"
"Thought is wave, emotion is frequency, dialogue is resonance"

Philosophy:
-----------
Rather than rigid state machines, Elysia's dialogue flows like water:
- Thoughts propagate as waves through the system
- Emotions modulate the frequency
- Memories resonate with current input
- Context flows continuously rather than being rigidly stored

This ensures the system remains fluid, organic, and wave-like rather than mechanical.

Architecture:
-------------
Input → Wave Conversion → Emotional Modulation → Memory Resonance → 
Poetic Collapse → Output

All components are interconnected through wave physics, not rigid interfaces.
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
import time

logger = logging.getLogger("WaveDialogueFlow")


@dataclass
class DialogueWave:
    """
    A dialogue turn represented as a wave packet.
    대화 턴의 파동 표현
    """
    # Content
    message: str
    speaker: str  # 'user' or 'assistant'
    
    # Wave properties
    frequency: float = 100.0  # Emotional frequency (Hz)
    amplitude: float = 0.5  # Intensity (0-1)
    phase: float = 0.0  # Phase offset (0-2π)
    
    # Semantic properties
    valence: float = 0.0  # -1 to 1
    arousal: float = 0.5  # 0 to 1
    
    # Metadata
    timestamp: float = field(default_factory=time.time)
    topics: List[str] = field(default_factory=list)
    
    def resonate_with(self, other: 'DialogueWave') -> float:
        """
        Calculate resonance strength with another wave.
        共鳴強度 計算
        
        Returns:
            Resonance coefficient (0-1)
        """
        # Frequency difference (closer = stronger resonance)
        freq_diff = abs(self.frequency - other.frequency)
        freq_resonance = 1.0 / (1.0 + freq_diff / 100.0)
        
        # Valence alignment
        valence_diff = abs(self.valence - other.valence)
        valence_resonance = 1.0 - (valence_diff / 2.0)
        
        # Combined resonance
        resonance = (freq_resonance + valence_resonance) / 2.0
        return max(0.0, min(1.0, resonance))


class WaveDialogueFlow:
    """
    Wave-based dialogue flow manager.
    파동 기반 대화 흐름 관리자
    
    Ensures all dialogue processing flows like water through interconnected systems:
    - EmotionalEngine: Modulates wave frequencies
    - ConversationMemory: Stores wave patterns
    - LinguisticCollapse: Converts waves to language
    - ReasoningEngine: Processes wave logic
    
    Everything is wave-based, nothing is rigid.
    """
    
    def __init__(self,
                 enable_emotional_modulation: bool = True,
                 enable_conversation_memory: bool = True,
                 enable_poetic_expression: bool = True):
        """
        Initialize wave dialogue flow.
        
        Args:
            enable_emotional_modulation: Enable emotional wave modulation
            enable_conversation_memory: Enable conversation memory system
            enable_poetic_expression: Enable linguistic collapse for poetic output
        """
        self.enable_emotional = enable_emotional_modulation
        self.enable_memory = enable_conversation_memory
        self.enable_poetic = enable_poetic_expression
        
        # Initialize emotional engine (wave modulator)
        if self.enable_emotional:
            try:
                from Core.Foundation.emotional_engine import EmotionalEngine
                self.emotional_engine = EmotionalEngine(
                    enable_conversation_memory=enable_conversation_memory
                )
            except ImportError:
                logger.warning("EmotionalEngine not available")
                self.emotional_engine = None
        else:
            self.emotional_engine = None
        
        # Wave buffer (recent dialogue waves)
        self.wave_buffer: List[DialogueWave] = []
        self.max_buffer_size = 10
        
        logger.info(f"🌊 WaveDialogueFlow initialized (emotional={enable_emotional_modulation}, " +
                   f"memory={enable_conversation_memory}, poetic={enable_poetic_expression})")
    
    def process_user_input(self,
                          user_message: str,
                          user_id: Optional[str] = None,
                          topics: Optional[List[str]] = None,
                          intent: Optional[str] = None) -> Dict[str, Any]:
        """
        Process user input through the wave flow.
        사용자 입력을 파동 흐름으로 처리
        
        Args:
            user_message: User's message
            user_id: User identifier
            topics: Detected topics
            intent: User intent
            
        Returns:
            Dict containing:
            - response: Assistant's response text
            - emotional_state: Current emotional state
            - poetic_expression: Poetic description of emotion
            - overflow: Optional overflow state
            - wave_properties: Wave properties of the response
            - context_resonance: Resonance with conversation history
        """
        # 1. Convert input to wave
        user_wave = self._text_to_wave(user_message, speaker='user')
        self.wave_buffer.append(user_wave)
        
        # 2. Calculate resonance with conversation history
        context_resonance = self._calculate_context_resonance(user_wave)
        
        # 3. Modulate emotional state based on input wave
        if self.emotional_engine:
            self._modulate_emotional_state(user_wave)
        
        # 4. Generate response (this would integrate with reasoning engine)
        assistant_message = self._generate_response(user_message, context_resonance)
        
        # 5. Convert response to wave
        assistant_wave = self._text_to_wave(assistant_message, speaker='assistant')
        if self.emotional_engine:
            # Set wave properties from emotional state
            state = self.emotional_engine.current_state
            assistant_wave.frequency = getattr(state.wave, 'frequency', 100.0)
            assistant_wave.amplitude = getattr(state.wave, 'amplitude', 0.5)
            assistant_wave.phase = getattr(state.wave, 'phase', 0.0)
            assistant_wave.valence = state.valence
            assistant_wave.arousal = state.arousal
        
        self.wave_buffer.append(assistant_wave)
        
        # Trim buffer
        if len(self.wave_buffer) > self.max_buffer_size:
            self.wave_buffer = self.wave_buffer[-self.max_buffer_size:]
        
        # 6. Record turn in conversation memory
        if self.emotional_engine and hasattr(self.emotional_engine, 'record_conversation_turn'):
            self.emotional_engine.record_conversation_turn(
                user_message=user_message,
                assistant_message=assistant_message,
                topics=topics,
                intent=intent,
                user_id=user_id
            )
        
        # 7. Get poetic expression
        poetic_expression = ""
        overflow_state = None
        if self.enable_poetic and self.emotional_engine:
            poetic_expression = self.emotional_engine.get_poetic_expression(context=user_message)
            overflow_state = self.emotional_engine.get_overflow_state()
        
        # 8. Package results
        result = {
            "response": assistant_message,
            "emotional_state": self.emotional_engine.current_state if self.emotional_engine else None,
            "poetic_expression": poetic_expression,
            "overflow": overflow_state,
            "wave_properties": {
                "frequency": assistant_wave.frequency,
                "amplitude": assistant_wave.amplitude,
                "phase": assistant_wave.phase,
                "valence": assistant_wave.valence,
                "arousal": assistant_wave.arousal
            },
            "context_resonance": context_resonance,
            "topics": topics or []
        }
        
        return result
    
    def _text_to_wave(self, text: str, speaker: str) -> DialogueWave:
        """
        Convert text to dialogue wave.
        텍스트를 대화 파동으로 변환
        """
        # Simple heuristics (can be enhanced with sentiment analysis)
        text_lower = text.lower()
        
        # Estimate valence
        positive_words = ['good', 'great', 'love', 'happy', 'beautiful', '좋', '멋', '사랑', '행복', '아름답']
        negative_words = ['bad', 'hate', 'sad', 'angry', 'terrible', '나쁘', '싫', '슬', '화', '끔찍']
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        valence = (positive_count - negative_count) / max(1, positive_count + negative_count + 1)
        
        # Estimate arousal (longer, more punctuation = higher arousal)
        arousal = min(1.0, (len(text) / 100.0) + (text.count('!') * 0.1) + (text.count('?') * 0.1))
        
        # Map to frequency (higher arousal = higher frequency)
        frequency = 100.0 + (arousal * 300.0)
        
        # Amplitude based on text length
        amplitude = min(1.0, len(text) / 200.0)
        
        return DialogueWave(
            message=text,
            speaker=speaker,
            frequency=frequency,
            amplitude=amplitude,
            valence=valence,
            arousal=arousal
        )
    
    def _calculate_context_resonance(self, current_wave: DialogueWave) -> float:
        """
        Calculate resonance with conversation history.
        대화 히스토리와의 공명 계산
        """
        if len(self.wave_buffer) == 0:
            return 0.5  # Neutral resonance for first turn
        
        # Calculate average resonance with recent waves
        recent_waves = self.wave_buffer[-5:]  # Last 5 turns
        resonances = [current_wave.resonate_with(wave) for wave in recent_waves]
        
        return sum(resonances) / len(resonances) if resonances else 0.5
    
    def _modulate_emotional_state(self, input_wave: DialogueWave):
        """
        Modulate emotional engine based on input wave.
        입력 파동에 기반하여 감정 엔진 조정
        """
        if not self.emotional_engine:
            return
        
        # Create temporary emotional state from wave properties
        try:
            from Core.Foundation.emotional_engine import EmotionalState
            from Core.Foundation.hangul_physics import Tensor3D
            from Core.Intelligence.Memory_Linguistics.Memory.unified_types import FrequencyWave
        except ImportError:
            return
        
        # Map wave to emotional state
        event_state = EmotionalState(
            valence=input_wave.valence,
            arousal=input_wave.arousal,
            dominance=0.0,  # Neutral
            primary_emotion="engaged",
            tensor=Tensor3D(input_wave.amplitude, input_wave.valence, input_wave.arousal),
            wave=FrequencyWave(input_wave.frequency, input_wave.amplitude, input_wave.phase, 0.1)
        )
        
        # Process event with intensity based on amplitude
        self.emotional_engine.process_event(event_state, intensity=input_wave.amplitude)
    
    def _generate_response(self, user_message: str, context_resonance: float) -> str:
        """
        Generate assistant response.
        (This is a placeholder - should integrate with ReasoningEngine)
        """
        # This is a simple placeholder
        # In real integration, this would call ReasoningEngine with:
        # - user_message
        # - conversation context from memory
        # - current emotional state
        # - wave properties
        
        # For now, return acknowledgment with context awareness
        if context_resonance > 0.7:
            return f"I understand, building on our conversation... [Response would be generated here]"
        elif context_resonance > 0.4:
            return f"Interesting point. [Response would be generated here]"
        else:
            return f"Let me think about that... [Response would be generated here]"
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """
        Get summary of current conversation flow.
        현재 대화 흐름 요약
        """
        if not self.wave_buffer:
            return {"status": "empty", "turns": 0}
        
        # Calculate average wave properties
        avg_frequency = sum(w.frequency for w in self.wave_buffer) / len(self.wave_buffer)
        avg_valence = sum(w.valence for w in self.wave_buffer) / len(self.wave_buffer)
        avg_arousal = sum(w.arousal for w in self.wave_buffer) / len(self.wave_buffer)
        
        summary = {
            "status": "active",
            "turns": len(self.wave_buffer),
            "average_frequency": avg_frequency,
            "average_valence": avg_valence,
            "average_arousal": avg_arousal,
            "emotional_state": self.emotional_engine.current_state.primary_emotion if self.emotional_engine else "unknown"
        }
        
        # Add conversation memory stats if available
        if self.emotional_engine and hasattr(self.emotional_engine, 'get_conversation_context'):
            emotional_arc = self.emotional_engine.get_emotional_arc()
            if emotional_arc:
                summary["emotional_arc_length"] = len(emotional_arc)
                summary["emotional_trend"] = "positive" if emotional_arc[-1] > emotional_arc[0] else "negative"
        
        return summary
    
    def reset_flow(self):
        """
        Reset dialogue flow (clear buffer, reset state).
        대화 흐름 리셋
        """
        self.wave_buffer.clear()
        if self.emotional_engine:
            # Reset to neutral state
            from Core.Foundation.emotional_engine import EmotionalEngine
            self.emotional_engine.current_state = EmotionalEngine.FEELING_PRESETS["neutral"]
        
        logger.info("🔄 Wave dialogue flow reset")


def create_wave_dialogue_flow(
    emotional: bool = True,
    memory: bool = True,
    poetic: bool = True
) -> WaveDialogueFlow:
    """
    Convenience function to create wave dialogue flow.
    
    Args:
        emotional: Enable emotional modulation
        memory: Enable conversation memory
        poetic: Enable poetic expressions
        
    Returns:
        WaveDialogueFlow instance
    """
    return WaveDialogueFlow(
        enable_emotional_modulation=emotional,
        enable_conversation_memory=memory,
        enable_poetic_expression=poetic
    )


if __name__ == "__main__":
    # Demo
    print("=" * 70)
    print("Wave-Based Dialogue Flow Demo")
    print("=" * 70)
    print()
    
    flow = create_wave_dialogue_flow()
    
    # Simulate conversation
    conversations = [
        "Hello! How are you today?",
        "I'm feeling a bit stressed about work.",
        "Can you help me relax?",
        "Thank you, that's very helpful!"
    ]
    
    for i, user_msg in enumerate(conversations, 1):
        print(f"Turn {i}:")
        print(f"User: {user_msg}")
        
        result = flow.process_user_input(
            user_message=user_msg,
            user_id="demo_user",
            topics=["conversation", "emotion"]
        )
        
        print(f"Assistant: {result['response']}")
        print(f"Poetic: {result['poetic_expression'][:100]}..." if result['poetic_expression'] else "")
        print(f"Wave: freq={result['wave_properties']['frequency']:.1f}Hz, " +
              f"valence={result['wave_properties']['valence']:.2f}")
        print(f"Context Resonance: {result['context_resonance']:.2f}")
        print()
    
    print("Conversation Summary:")
    print(flow.get_conversation_summary())
