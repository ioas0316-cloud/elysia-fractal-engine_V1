from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any

# Import physics types with graceful fallback
try:
    from Core.Foundation.hangul_physics import Tensor3D
    from Core.Intelligence.Memory_Linguistics.Memory.unified_types import FrequencyWave
except ImportError:
    # Fallback stub classes if imports fail
    class Tensor3D:
        def __init__(self, x=0.0, y=0.0, z=0.0):
            self.x, self.y, self.z = x, y, z
        
        def __mul__(self, scalar):
            return Tensor3D(self.x * scalar, self.y * scalar, self.z * scalar)
        
        def __add__(self, other):
            return Tensor3D(self.x + other.x, self.y + other.y, self.z + other.z)
    
    class FrequencyWave:
        def __init__(self, freq=0.0, amp=0.0, phase=0.0, damping=0.0):
            self.frequency = freq
            self.amplitude = amp
            self.phase = phase
            self.damping = damping

@dataclass
class EmotionalState:
    """
    Represents Elysia's current emotional state.
    Now includes 3D Tensor and Frequency Wave for fractal/meta-structural depth.
    """
    valence: float  # Pleasure: -1 (negative) to 1 (positive)
    arousal: float  # Activation: 0 (calm) to 1 (excited)
    dominance: float # Control: -1 (submissive) to 1 (dominant)
    primary_emotion: str = "neutral"
    secondary_emotions: List[str] = field(default_factory=list)

    # --- Fractal Physics Layer ---
    tensor: Tensor3D = field(default_factory=Tensor3D)
    wave: FrequencyWave = field(default_factory=lambda: FrequencyWave(0.0, 0.0, 0.0, 0.0))

class EmotionalEngine:
    """
    Manages the dynamics of Elysia's emotional state, including transitions
    and the influence of events.
    """
    FEELING_PRESETS: Dict[str, EmotionalState] = {
        "neutral": EmotionalState(
            valence=0.0, arousal=0.2, dominance=0.0, primary_emotion="neutral",
            tensor=Tensor3D(0.1, 0.1, 0.1), wave=FrequencyWave(100.0, 0.1, 0.0, 0.0)
        ),
        "calm": EmotionalState(
            valence=0.2, arousal=0.1, dominance=0.1, primary_emotion="calm",
            tensor=Tensor3D(0.3, 0.1, 0.2), wave=FrequencyWave(50.0, 0.2, 0.0, 0.1)
        ),
        "hopeful": EmotionalState(
            valence=0.6, arousal=0.4, dominance=0.2, primary_emotion="hopeful", secondary_emotions=["joy"],
            tensor=Tensor3D(0.5, 0.6, 0.7), wave=FrequencyWave(300.0, 0.5, 0.0, 0.3)
        ),
        "focused": EmotionalState(
            valence=0.1, arousal=0.6, dominance=0.4, primary_emotion="focused",
            tensor=Tensor3D(0.8, 0.3, 0.5), wave=FrequencyWave(400.0, 0.6, 0.0, 0.1)
        ),
        "introspective": EmotionalState(
            valence=-0.2, arousal=0.3, dominance=-0.1, primary_emotion="introspective", secondary_emotions=["sadness"],
            tensor=Tensor3D(0.4, 0.5, 0.8), wave=FrequencyWave(150.0, 0.4, 3.14, 0.5)
        ),
        "empty": EmotionalState(
            valence=-0.5, arousal=0.1, dominance=-0.3, primary_emotion="empty",
            tensor=Tensor3D(0.1, 0.0, 0.1), wave=FrequencyWave(20.0, 0.1, 0.0, 0.0)
        ),
    }

    def __init__(self, initial_state: Optional[EmotionalState] = None, enable_conversation_memory: bool = False):
        if initial_state is None:
            # Start with a neutral state
            self.current_state = self.FEELING_PRESETS["neutral"]
        else:
            self.current_state = initial_state
        
        # Conversation memory (optional)
        self._conversation_memory = None
        if enable_conversation_memory:
            try:
                from Core.Intelligence.Memory_Linguistics.Memory.conversation_memory import create_conversation_memory
                self._conversation_memory = create_conversation_memory(context_turns=10)
            except ImportError:
                pass  # Memory system not available

    def process_event(self, event_emotion: EmotionalState, intensity: float = 0.5):
        """
        Updates the current emotional state based on an external event.
        Uses Tensor addition and Wave interference for fractal depth.

        Args:
            event_emotion: The emotional quality of the event.
            intensity: How strongly the event affects the current state (0 to 1).
        """
        # 1. Traditional VAD Update (Linear Interpolation)
        decay = 1.0 - intensity
        self.current_state.valence = (self.current_state.valence * decay) + (event_emotion.valence * intensity)
        self.current_state.arousal = (self.current_state.arousal * decay) + (event_emotion.arousal * intensity)
        self.current_state.dominance = (self.current_state.dominance * decay) + (event_emotion.dominance * intensity)

        # 2. Physics Layer Update (Fractal Interaction)

        # Tensor: Weighted addition (Field mixing)
        # We treat intensity as the 'mass' of the incoming event
        incoming_tensor = event_emotion.tensor * intensity
        current_tensor = self.current_state.tensor * decay

        # Combine fields
        new_tensor = current_tensor + incoming_tensor

        # Wave: Interference (Resonance)
        # Interact current wave with incoming wave
        new_wave = self.current_state.wave.interact(event_emotion.wave)

        # Apply physics updates
        self.current_state.tensor = new_tensor
        self.current_state.wave = new_wave

        # 3. Primary/Secondary Emotion Management
        if intensity > 0.6:
            if self.current_state.primary_emotion != event_emotion.primary_emotion:
                if self.current_state.primary_emotion not in self.current_state.secondary_emotions:
                    self.current_state.secondary_emotions.insert(0, self.current_state.primary_emotion)
                self.current_state.primary_emotion = event_emotion.primary_emotion
        
        for emo in event_emotion.secondary_emotions:
            if emo not in self.current_state.secondary_emotions and emo != self.current_state.primary_emotion:
                self.current_state.secondary_emotions.append(emo)

        self.current_state.secondary_emotions = self.current_state.secondary_emotions[:3]

        # Clamp VAD values
        self.current_state.valence = max(-1.0, min(1.0, self.current_state.valence))
        self.current_state.arousal = max(0.0, min(1.0, self.current_state.arousal))
        self.current_state.dominance = max(-1.0, min(1.0, self.current_state.dominance))

        return self.current_state

    def get_current_state(self) -> EmotionalState:
        """Returns the current emotional state."""
        return self.current_state

    def create_state_from_feeling(self, feeling: str) -> EmotionalState:
        """
        Creates a new EmotionalState object from a feeling string using the presets.
        """
        # Return a COPY to avoid modifying the static preset
        preset = self.FEELING_PRESETS.get(feeling.lower(), self.FEELING_PRESETS["neutral"])
        # Deep copy tensor/wave safely
        if hasattr(preset.tensor, "to_dict"):
            tdict = preset.tensor.to_dict()
            tensor_copy = Tensor3D.from_dict(tdict) if hasattr(Tensor3D, "from_dict") else Tensor3D(**tdict)
        else:
            # Fallback: copy attributes manually
            tensor_copy = Tensor3D(
                x=getattr(preset.tensor, 'x', 0.0),
                y=getattr(preset.tensor, 'y', 0.0),
                z=getattr(preset.tensor, 'z', 0.0)
            )

        wave_copy = FrequencyWave.from_dict(preset.wave.to_dict()) if preset.wave else FrequencyWave(0.0, 0.0, 0.0, 0.0)

        return EmotionalState(
            valence=preset.valence,
            arousal=preset.arousal,
            dominance=preset.dominance,
            primary_emotion=preset.primary_emotion,
            secondary_emotions=list(preset.secondary_emotions),
            tensor=tensor_copy,
            wave=wave_copy,
        )
    
    def get_poetic_expression(self, context: Optional[str] = None) -> str:
        """
        Get a poetic linguistic expression of the current emotional state.
        
        This implements the "Linguistic Collapse Protocol" - translating
        the mathematical wave state into human-understandable poetic language.
        
        Handles overflow states where emotions are too strong for words.
        
        Args:
            context: Optional context for the expression
            
        Returns:
            Poetic description of the emotional state
        """
        try:
            from Core.Foundation.linguistic_collapse import LinguisticCollapseProtocol
            
            if not hasattr(self, '_linguistic_protocol'):
                language = getattr(self, '_preferred_language', 'ko')
                self._linguistic_protocol = LinguisticCollapseProtocol(language=language)
            
            # Use overflow-aware collapse
            expression, overflow = self._linguistic_protocol.collapse_with_overflow_check(
                tensor=self.current_state.tensor,
                wave=self.current_state.wave,
                valence=self.current_state.valence,
                arousal=self.current_state.arousal,
                dominance=self.current_state.dominance,
                context=context,
                secondary_emotions=self.current_state.secondary_emotions
            )
            
            # Store overflow state for potential visualization
            if overflow:
                self._last_overflow = overflow
            
            return expression
        except Exception as e:
            # Fallback to simple expression
            return self.get_simple_expression()
    
    def get_overflow_state(self) -> Optional[Any]:
        """
        Get the last overflow state if any.
        Used for visualization in the avatar system.
        
        Returns:
            EmotionalOverflowState or None
        """
        return getattr(self, '_last_overflow', None)
    
    def set_language(self, language: str):
        """
        Set the language for emotional expressions.
        
        Args:
            language: Language code - 'ko' (Korean), 'en' (English), 'ja' (Japanese)
        """
        if hasattr(self, '_linguistic_protocol'):
            self._linguistic_protocol.set_language(language)
        else:
            # Store for later initialization
            self._preferred_language = language
    
    def get_language(self) -> str:
        """
        Get the current language setting.
        
        Returns:
            Language code ('ko', 'en', or 'ja')
        """
        if hasattr(self, '_linguistic_protocol'):
            return self._linguistic_protocol.get_language()
        else:
            return getattr(self, '_preferred_language', 'ko')
    
    def get_simple_expression(self) -> str:
        """
        Get a simple poetic expression without full wave analysis.
        Lightweight alternative to get_poetic_expression().
        
        Returns:
            Short poetic expression of the emotional state
        """
        try:
            from Core.Foundation.linguistic_collapse import LinguisticCollapseProtocol
            
            if not hasattr(self, '_linguistic_protocol'):
                language = getattr(self, '_preferred_language', 'ko')
                self._linguistic_protocol = LinguisticCollapseProtocol(language=language)
            
            return self._linguistic_protocol.get_simple_expression(
                valence=self.current_state.valence,
                arousal=self.current_state.arousal,
                primary_emotion=self.current_state.primary_emotion
            )
        except Exception:
            # Final fallback
            return f"{self.current_state.primary_emotion}의 상태입니다"
    
    # === Conversation Memory Integration ===
    
    def enable_conversation_memory(self, context_turns: int = 10):
        """
        Enable conversation memory system.
        
        Args:
            context_turns: Number of recent turns to keep in active context
        """
        try:
            from Core.Intelligence.Memory_Linguistics.Memory.conversation_memory import create_conversation_memory
            self._conversation_memory = create_conversation_memory(context_turns=context_turns)
        except ImportError:
            raise ImportError("ConversationMemory system not available. Install Core.Foundation.Memory.conversation_memory")
    
    def record_conversation_turn(self,
                                user_message: str,
                                assistant_message: str,
                                topics: Optional[List[str]] = None,
                                intent: Optional[str] = None,
                                user_id: Optional[str] = None):
        """
        Record a conversation turn with current emotional context.
        
        Args:
            user_message: User's message
            assistant_message: Elysia's response
            topics: Topics discussed
            intent: User's intent
            user_id: User identifier for profile learning
        """
        if self._conversation_memory is None:
            return  # Memory not enabled
        
        self._conversation_memory.add_turn(
            user_message=user_message,
            assistant_message=assistant_message,
            user_emotion=None,  # Could be detected via sentiment analysis
            assistant_emotion=self.current_state.primary_emotion,
            emotional_valence=self.current_state.valence,
            topics=topics or [],
            intent=intent,
            language=self.get_language(),
            user_id=user_id
        )
    
    def get_conversation_context(self, n_turns: Optional[int] = None, format_style: str = "emotional") -> str:
        """
        Get conversation context string for prompt injection.
        
        Args:
            n_turns: Number of recent turns to include
            format_style: 'simple', 'detailed', or 'emotional'
            
        Returns:
            Formatted context string or empty string if memory disabled
        """
        if self._conversation_memory is None:
            return ""
        
        return self._conversation_memory.get_context_string(n_turns=n_turns, format_style=format_style)
    
    def get_emotional_arc(self, n_turns: Optional[int] = None) -> List[float]:
        """
        Get emotional valence trajectory over recent conversation.
        
        Args:
            n_turns: Number of turns to analyze
            
        Returns:
            List of emotional valence values or empty list if memory disabled
        """
        if self._conversation_memory is None:
            return []
        
        return self._conversation_memory.get_emotional_arc(n_turns=n_turns)
    
    def get_user_profile(self, user_id: Optional[str] = None) -> Optional[Any]:
        """
        Get learned user profile.
        
        Args:
            user_id: User identifier (uses current user if None)
            
        Returns:
            UserProfile or None
        """
        if self._conversation_memory is None:
            return None
        
        return self._conversation_memory.get_user_profile(user_id=user_id)
    
    def save_conversation_history(self, filepath: str):
        """
        Save conversation history to file.
        
        Args:
            filepath: Path to save file
        """
        if self._conversation_memory:
            self._conversation_memory.save_to_file(filepath)
    
    def load_conversation_history(self, filepath: str):
        """
        Load conversation history from file.
        
        Args:
            filepath: Path to load file
        """
        if self._conversation_memory:
            self._conversation_memory.load_from_file(filepath)
