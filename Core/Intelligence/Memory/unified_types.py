"""
Unified Core Types - Consolidated Experience and EmotionalState Classes
========================================================================

This module provides the canonical, unified implementations of core types
that were previously duplicated across multiple files.

Created: 2025-12-06
Purpose: P1.1 - Consolidate Duplicate Classes (54 → 0)
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any
from datetime import datetime

# Import tensor/wave types if available, with graceful fallback
try:
    from Core.Foundation.hangul_physics import Tensor3D
    HAS_TENSOR_WAVE = True
except ImportError:
    HAS_TENSOR_WAVE = False
    # Fallback stub classes
    class Tensor3D:
        def __init__(self, x=0.0, y=0.0, z=0.0):
            self.x, self.y, self.z = x, y, z
        def to_dict(self):
            return {"x": self.x, "y": self.y, "z": self.z}

# FrequencyWave definition (local to this module)
class FrequencyWave:
    def __init__(self, freq=0.0, amp=0.0, phase=0.0, damping=0.0):
        self.frequency = freq
        self.amplitude = amp
        self.phase = phase
        self.damping = damping

    def interact(self, other: 'FrequencyWave') -> 'FrequencyWave':
        """
        Interference pattern between two waves.
        """
        # Average frequency
        new_freq = (self.frequency + other.frequency) / 2.0
        
        # Amplitude interference (constructive/destructive)
        # Cosine of phase difference determines interference
        import math
        phase_diff = abs(self.phase - other.phase)
        interference = math.cos(phase_diff)
        
        # New amplitude is average * interference factor
        new_amp = (self.amplitude + other.amplitude) / 2.0 * (0.5 + 0.5 * interference)
        
        return FrequencyWave(
            freq=new_freq,
            amp=new_amp,
            phase=(self.phase + other.phase) / 2.0,
            damping=(self.damping + other.damping) / 2.0
        )
    
    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary"""
        return {
            "freq": self.frequency,
            "amp": self.amplitude,
            "phase": self.phase,
            "damping": self.damping
        }

    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> 'FrequencyWave':
        """Create from dictionary"""
        return cls(
            freq=data.get("freq", 0.0),
            amp=data.get("amp", 0.0),
            phase=data.get("phase", 0.0),
            damping=data.get("damping", 0.0)
        )


@dataclass
class Experience:
    """
    Unified Experience class - Consolidates 4 duplicate implementations.
    
    This is the canonical Experience type that combines the best features
    from all previous implementations:
    - Core/Elysia/core_memory.py (most complete)
    - Core/Foundation/experience_learner.py (action/outcome focus)
    - Core/Foundation/experience_stream.py (streaming/logging focus)
    - Core/Foundation/divine_engine.py (truth/beauty/causality focus)
    
    Design Philosophy:
    - Comprehensive yet flexible
    - Supports all use cases from the original implementations
    - Physics-grounded (tensor + wave representation)
    - Backward compatible with legacy code
    """
    
    # === CORE IDENTITY ===
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())
    content: str = ""
    type: str = "episode"  # episode, conversation, emotion, insight, action, learning
    
    # === CONTEXT & LAYER ===
    layer: str = "soul"  # body, soul, spirit (3-layer model) OR 0D/1D/2D/3D (dimensional)
    context: Optional[Dict[str, Any]] = None
    tags: List[str] = field(default_factory=list)
    
    # === EMOTIONAL STATE ===
    emotional_state: Optional['EmotionalState'] = None
    intensity: float = 0.5  # Importance/intensity 0.0 to 1.0
    
    # === ACTION/OUTCOME (for learning experiences) ===
    action: Optional[Dict[str, Any]] = None
    outcome: Optional[Dict[str, Any]] = None
    feedback: Optional[float] = None  # -1.0 to 1.0
    
    # === DIVINE/PHILOSOPHICAL DIMENSIONS ===
    truth: float = 1.0       # Truth value 0.0 to 1.0
    beauty: float = 0.0      # Aesthetic value
    causality: float = 0.0   # Causal strength
    
    # === VALUE ALIGNMENT ===
    value_alignment: Optional[float] = None
    law_alignment: Optional[Dict[str, Any]] = None
    intent_bundle: Optional[Dict[str, Any]] = None
    
    # === PROCESSING STATE ===
    processed_by_weaver: bool = False
    processed_by_distiller: bool = False
    
    # === PHYSICS LAYER (Fractal/Tensor representation) ===
    tensor: Tensor3D = field(default_factory=Tensor3D)
    wave: FrequencyWave = field(default_factory=lambda: FrequencyWave(0.0, 0.0, 0.0, 0.0))
    
    # Legacy fields for backward compatibility
    frequency: float = 0.0
    resonance_amp: float = 0.0
    tensor_state: Optional[Dict[str, float]] = None
    richness: float = 0.0
    
    # === METADATA ===
    meta: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Sync legacy fields with tensor/wave representation"""
        # Sync tensor state
        if self.tensor and not self.tensor_state:
            self.tensor_state = self.tensor.to_dict()
        
        # Sync wave frequency
        if hasattr(self.wave, 'frequency') and self.wave.frequency > 0:
            self.frequency = self.wave.frequency
        if hasattr(self.wave, 'amplitude') and self.wave.amplitude > 0:
            self.resonance_amp = self.wave.amplitude
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization"""
        result = asdict(self)
        # Handle EmotionalState if present
        if self.emotional_state:
            result['emotional_state'] = asdict(self.emotional_state)
        return result
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Experience':
        """Create from dictionary"""
        # Handle EmotionalState if present
        if 'emotional_state' in data and data['emotional_state']:
            data['emotional_state'] = EmotionalState(**data['emotional_state'])
        return cls(**data)
    
    # === LEGACY COMPATIBILITY METHODS ===
    
    @classmethod
    def from_conversation(cls, content: str, intensity: float = 0.5, 
                         context: str = "General") -> 'Experience':
        """Create from conversation (experience_stream.py style)"""
        return cls(
            type="conversation",
            content=content,
            intensity=intensity,
            context={"general": context} if isinstance(context, str) else context
        )
    
    @classmethod
    def from_learning(cls, context: Dict, action: Dict, outcome: Dict, 
                     feedback: float, layer: str = "soul") -> 'Experience':
        """Create from learning experience (experience_learner.py style)"""
        return cls(
            type="learning",
            context=context,
            action=action,
            outcome=outcome,
            feedback=feedback,
            layer=layer
        )
    
    @classmethod
    def from_divine(cls, truth: float = 1.0, emotion: float = 0.0,
                   causality: float = 0.0, beauty: float = 0.0,
                   meta: Dict = None) -> 'Experience':
        """Create from divine dimensions (divine_engine.py style)"""
        return cls(
            type="divine",
            truth=truth,
            causality=causality,
            beauty=beauty,
            intensity=emotion,
            meta=meta or {}
        )


@dataclass
class EmotionalState:
    """
    Unified EmotionalState class - Consolidates 3 duplicate implementations.
    
    Combines features from:
    - Core/Foundation/emotional_engine.py (VAD model + physics)
    - Core/Foundation/spirit_emotion.py (spirit-based emotions)
    - Core/Elysia/core_memory.py (basic model)
    
    Uses VAD (Valence-Arousal-Dominance) model with physics layer.
    """
    
    # === VAD MODEL (Psychological Foundation) ===
    valence: float = 0.0      # Pleasure: -1 (negative) to 1 (positive)
    arousal: float = 0.2      # Activation: 0 (calm) to 1 (excited)
    dominance: float = 0.0    # Control: -1 (submissive) to 1 (dominant)
    
    # === EMOTIONAL LABELS ===
    name: str = "neutral"                           # For spirit_emotion.py compatibility
    primary_emotion: str = "neutral"
    secondary_emotions: List[str] = field(default_factory=list)
    
    # === INTENSITY & SOURCE ===
    intensity: float = 0.5    # Overall intensity 0.0 to 1.0
    temperature: float = 0.0  # -1.0 (extreme cold) to +1.0 (extreme heat)
    source_spirit: Optional[str] = None  # Which spirit generated this emotion
    
    # === PHYSICS LAYER ===
    tensor: Tensor3D = field(default_factory=Tensor3D)
    wave: FrequencyWave = field(default_factory=lambda: FrequencyWave(100.0, 0.1, 0.0, 0.0))
    
    def __post_init__(self):
        """Sync primary_emotion and name"""
        if self.primary_emotion and not self.name:
            self.name = self.primary_emotion
        elif self.name and not self.primary_emotion:
            self.primary_emotion = self.name
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'EmotionalState':
        """Create from dictionary"""
        return cls(**data)
    
    # === PRESET EMOTIONS ===
    
    @classmethod
    def neutral(cls) -> 'EmotionalState':
        """Neutral baseline state"""
        return cls(
            name="neutral",
            valence=0.0, arousal=0.2, dominance=0.0,
            tensor=Tensor3D(0.1, 0.1, 0.1),
            wave=FrequencyWave(100.0, 0.1, 0.0, 0.0)
        )
    
    @classmethod
    def calm(cls) -> 'EmotionalState':
        """Calm, peaceful state"""
        return cls(
            name="calm",
            valence=0.2, arousal=0.1, dominance=0.1,
            temperature=-0.3,
            tensor=Tensor3D(0.3, 0.1, 0.2),
            wave=FrequencyWave(50.0, 0.2, 0.0, 0.1)
        )
    
    @classmethod
    def hopeful(cls) -> 'EmotionalState':
        """Hopeful, positive state"""
        return cls(
            name="hopeful",
            primary_emotion="hopeful",
            secondary_emotions=["joy"],
            valence=0.6, arousal=0.4, dominance=0.2,
            temperature=0.5,
            tensor=Tensor3D(0.5, 0.6, 0.7),
            wave=FrequencyWave(300.0, 0.5, 0.0, 0.3)
        )
    
    @classmethod
    def focused(cls) -> 'EmotionalState':
        """Focused, concentrated state"""
        return cls(
            name="focused",
            valence=0.1, arousal=0.6, dominance=0.4,
            temperature=0.2,
            tensor=Tensor3D(0.8, 0.3, 0.5),
            wave=FrequencyWave(400.0, 0.6, 0.0, 0.1)
        )
    
    @classmethod
    def passionate(cls) -> 'EmotionalState':
        """Passionate, fiery state (from Creativity spirit)"""
        return cls(
            name="passion",
            primary_emotion="passion",
            valence=0.7, arousal=0.8, dominance=0.6,
            temperature=0.8,
            source_spirit="Creativity",
            tensor=Tensor3D(0.9, 0.8, 0.7),
            wave=FrequencyWave(432.0, 0.7, 0.0, 0.2)
        )
    
    @classmethod
    def melancholy(cls) -> 'EmotionalState':
        """Melancholic, introspective state (from Memory spirit)"""
        return cls(
            name="melancholy",
            primary_emotion="melancholy",
            secondary_emotions=["sadness"],
            valence=-0.3, arousal=0.3, dominance=-0.2,
            temperature=-0.3,
            source_spirit="Memory",
            tensor=Tensor3D(0.4, 0.5, 0.8),
            wave=FrequencyWave(528.0, 0.4, 3.14, 0.5)
        )
    
    @classmethod
    def empty(cls) -> 'EmotionalState':
        """Empty, void state"""
        return cls(
            name="empty",
            valence=-0.5, arousal=0.1, dominance=-0.3,
            temperature=-0.5,
            tensor=Tensor3D(0.1, 0.0, 0.1),
            wave=FrequencyWave(20.0, 0.1, 0.0, 0.0)
        )


# === EMOTIONAL ENGINE COMPATIBILITY ===

class EmotionalStateFactory:
    """
    Factory for creating emotional states with presets.
    Maintains compatibility with EmotionalEngine.FEELING_PRESETS pattern.
    """
    
    PRESETS: Dict[str, EmotionalState] = {
        "neutral": EmotionalState.neutral(),
        "calm": EmotionalState.calm(),
        "hopeful": EmotionalState.hopeful(),
        "focused": EmotionalState.focused(),
        "passionate": EmotionalState.passionate(),
        "melancholy": EmotionalState.melancholy(),
        "empty": EmotionalState.empty(),
    }
    
    @classmethod
    def get(cls, name: str) -> EmotionalState:
        """Get a preset emotional state by name"""
        return cls.PRESETS.get(name, EmotionalState.neutral())
    
    @classmethod
    def create_from_spirit(cls, spirit_name: str, intensity: float) -> EmotionalState:
        """
        Create emotional state from spirit energy.
        Compatible with spirit_emotion.py SpiritEmotionMapper.
        """
        # Get appropriate preset based on spirit and intensity
        if spirit_name == "Creativity":
            state = EmotionalState.passionate() if intensity > 0.5 else EmotionalState.calm()
        elif spirit_name == "Memory":
            state = EmotionalState.melancholy() if intensity > 0.5 else EmotionalState.calm()
        elif spirit_name == "Intelligence":
            state = EmotionalState.focused() if intensity > 0.5 else EmotionalState.neutral()
        elif spirit_name == "Foundation":
            state = EmotionalState.calm()
        else:
            state = EmotionalState.neutral()
        
        state.source_spirit = spirit_name
        state.intensity = intensity
        return state


# === MIGRATION HELPERS ===

def migrate_experience_from_old(old_exp: Any) -> Experience:
    """
    Migrate an old Experience instance to unified Experience.
    Handles all 4 old implementations gracefully.
    """
    # Try to extract fields that might exist
    data = {}
    
    # Common fields
    for field_name in ['timestamp', 'content', 'type', 'layer', 'context', 
                       'tags', 'intensity', 'feedback', 'action', 'outcome',
                       'truth', 'beauty', 'causality', 'meta']:
        if hasattr(old_exp, field_name):
            data[field_name] = getattr(old_exp, field_name)
    
    # Handle emotional_state
    if hasattr(old_exp, 'emotional_state') and old_exp.emotional_state:
        data['emotional_state'] = migrate_emotional_state_from_old(old_exp.emotional_state)
    
    # Handle physics layer
    if hasattr(old_exp, 'tensor'):
        data['tensor'] = old_exp.tensor
    if hasattr(old_exp, 'wave'):
        data['wave'] = old_exp.wave
    
    return Experience(**data)


def migrate_emotional_state_from_old(old_state: Any) -> EmotionalState:
    """
    Migrate an old EmotionalState instance to unified EmotionalState.
    Handles all 3 old implementations gracefully.
    """
    data = {}
    
    # Common fields
    for field_name in ['valence', 'arousal', 'dominance', 'name', 
                       'primary_emotion', 'secondary_emotions', 'intensity',
                       'temperature', 'source_spirit']:
        if hasattr(old_state, field_name):
            data[field_name] = getattr(old_state, field_name)
    
    # Handle physics layer
    if hasattr(old_state, 'tensor'):
        data['tensor'] = old_state.tensor
    if hasattr(old_state, 'wave'):
        data['wave'] = old_state.wave
    
    return EmotionalState(**data)


# === EXPORTS ===

__all__ = [
    'Experience',
    'EmotionalState',
    'EmotionalStateFactory',
    'migrate_experience_from_old',
    'migrate_emotional_state_from_old',
    'Tensor3D',  # For convenience
    'FrequencyWave',  # For convenience
]
