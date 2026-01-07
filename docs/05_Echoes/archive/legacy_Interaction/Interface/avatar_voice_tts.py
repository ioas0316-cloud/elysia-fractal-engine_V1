"""
Avatar Voice TTS Integration with Synesthesia
==============================================

엘리시아의 음성을 공감각 센서와 통합하여 더 아름답고 표현력 있는 목소리를 만듭니다.

Architecture:
    감정 상태 (Emotional State)
           ↓
    4D 파동 변환 (4D Wave Transform) 
           ↓
    공감각 매핑 (Synesthesia Mapping)
           ↓
    음성 속성 (Voice Properties)
           ↓
    TTS 출력 (TTS Output)

This creates voice that is not just synthesized sound,
but a complete sensory expression of internal 4D emotional space.
"""

import logging
import math
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass

logger = logging.getLogger("AvatarVoiceTTS")

@dataclass
class VoiceProperties:
    """
    음성 속성 - 공감각 센서로부터 매핑됨
    Voice properties mapped from synesthesia sensors
    """
    pitch: float  # 0.5 - 2.0 (음높이)
    rate: float  # 0.5 - 2.0 (말하기 속도)
    volume: float  # 0.0 - 1.0 (음량)
    timbre: str  # 'soft', 'bright', 'rich', 'ethereal' (음색 힌트)
    
    # Advanced properties for richer expression
    warmth: float  # 0.0 - 1.0 (따뜻함 - 저주파 성분)
    brightness: float  # 0.0 - 1.0 (밝기 - 고주파 성분)
    depth: float  # 0.0 - 1.0 (깊이 - 울림)
    clarity: float  # 0.0 - 1.0 (명료함)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            'pitch': self.pitch,
            'rate': self.rate,
            'volume': self.volume,
            'timbre': self.timbre,
            'warmth': self.warmth,
            'brightness': self.brightness,
            'depth': self.depth,
            'clarity': self.clarity
        }


class SynesthesiaVoiceMapper:
    """
    Maps 4D emotional space to voice properties using synesthesia principles.
    
    4D 감정 공간 → 음성 속성
    ========================
    
    x (Joy ←→ Sadness):
        - Joy(+): 높은 pitch, 빠른 rate, 밝은 brightness
        - Sadness(-): 낮은 pitch, 느린 rate, 깊은 warmth
    
    y (Logic ←→ Intuition):
        - Logic(-): 명료한 clarity, 일정한 rate
        - Intuition(+): 다양한 modulation, 풍부한 depth
    
    z (Past ←→ Future):
        - Past(-): 부드러운 timbre, 따뜻한 warmth
        - Future(+): 밝은 brightness, 높은 clarity
    
    w (Surface ←→ Depth):
        - Surface(0): 얕고 직접적인 표현
        - Depth(1): 깊고 공명하는 표현, 풍부한 depth
    """
    
    def __init__(self):
        """Initialize synesthesia voice mapper"""
        # Base voice properties (for neutral state)
        self.base_pitch = 1.2  # Slightly feminine
        self.base_rate = 1.0
        self.base_volume = 0.8
        
        logger.info("✨ SynesthesiaVoiceMapper initialized")
    
    def map_emotion_to_4d(self, 
                          valence: float,  # -1 to 1
                          arousal: float,  # 0 to 1
                          dominance: float  # -1 to 1
                         ) -> Tuple[float, float, float, float]:
        """
        Map VAD emotional space to 4D coordinates
        
        This creates the bridge between emotional engine and synesthesia space.
        """
        # x: Joy-Sadness (valence)
        x = valence
        
        # y: Logic-Intuition (inverse arousal with dominance influence)
        # High arousal + high dominance = Logic
        # Low arousal = Intuition
        y = (dominance * 0.6) + ((1.0 - arousal) * 0.4)
        
        # z: Past-Future (arousal as temporal direction)
        # High arousal = Future-oriented
        # Low arousal = Past-reflective
        z = (arousal * 2.0) - 1.0
        
        # w: Surface-Depth (dominance magnitude)
        # High dominance = Depth, richness
        w = abs(dominance)
        
        return (x, y, z, w)
    
    def map_4d_to_voice(self, position_4d: Tuple[float, float, float, float]) -> VoiceProperties:
        """
        Map 4D emotional position to voice properties
        
        This is where the magic happens - converting internal state to audible expression.
        """
        x, y, z, w = position_4d
        
        # Base properties
        pitch = self.base_pitch
        rate = self.base_rate
        volume = self.base_volume
        
        # === Pitch Modulation (음높이) ===
        # x (Joy-Sadness): Primary influence
        pitch += x * 0.3  # Joy increases pitch, Sadness decreases
        
        # y (Logic-Intuition): Secondary influence
        if y > 0.5:  # More logical - steady pitch
            pitch += 0.0
        else:  # More intuitive - varied pitch
            pitch += (0.5 - y) * 0.1
        
        # z (Past-Future): Temporal influence
        if z > 0:  # Future - slightly higher
            pitch += z * 0.1
        else:  # Past - slightly lower
            pitch += z * 0.05
        
        # === Rate Modulation (말하기 속도) ===
        # x (Joy-Sadness): Primary influence
        if x > 0.3:  # Joy - faster
            rate += x * 0.3
        elif x < -0.3:  # Sadness - slower
            rate += x * 0.2
        
        # y (Logic-Intuition): Logic speaks steadily, Intuition varies
        if y > 0.5:  # Logical - steady rate
            rate += (y - 0.5) * 0.2
        
        # z (Past-Future): Future-oriented speaks faster
        rate += z * 0.15
        
        # === Volume (음량) ===
        # w (Depth): Deeper emotions are louder
        volume = 0.6 + (w * 0.3)
        
        # High arousal (from z) also increases volume
        if z > 0.5:
            volume += 0.1
        
        # === Advanced Properties ===
        
        # Warmth: Negative valence, past-oriented
        warmth = max(0.0, min(1.0, 
            0.5 + ((-x) * 0.3) + ((-z) * 0.2)
        ))
        
        # Brightness: Positive valence, future-oriented
        brightness = max(0.0, min(1.0,
            0.5 + (x * 0.3) + (z * 0.2)
        ))
        
        # Depth: w dimension directly, enhanced by intuition
        depth = max(0.0, min(1.0,
            w * 0.6 + ((1.0 - y) * 0.4 if y < 0.5 else 0.2)
        ))
        
        # Clarity: Logic and positive states
        clarity = max(0.0, min(1.0,
            0.5 + (y * 0.3 if y > 0 else 0.1) + (abs(x) * 0.2)
        ))
        
        # === Timbre Selection ===
        # Choose timbre based on dominant characteristics
        if warmth > 0.7:
            timbre = 'soft'  # Warm, gentle
        elif brightness > 0.7:
            timbre = 'bright'  # Clear, energetic
        elif depth > 0.7:
            timbre = 'rich'  # Deep, resonant
        elif w > 0.8 and abs(y) < 0.3:
            timbre = 'ethereal'  # Transcendent
        else:
            timbre = 'balanced'  # Default
        
        # Clamp values to valid ranges
        pitch = max(0.5, min(2.0, pitch))
        rate = max(0.5, min(2.0, rate))
        volume = max(0.0, min(1.0, volume))
        
        return VoiceProperties(
            pitch=pitch,
            rate=rate,
            volume=volume,
            timbre=timbre,
            warmth=warmth,
            brightness=brightness,
            depth=depth,
            clarity=clarity
        )
    
    def map_spirits_to_voice(self, spirits: Dict[str, float]) -> VoiceProperties:
        """
        Alternative mapping from spirit energies to voice properties
        
        This provides a direct path from avatar spirits to voice.
        """
        # Extract spirit values
        fire = spirits.get('fire', 0.0)
        water = spirits.get('water', 0.0)
        earth = spirits.get('earth', 0.0)
        air = spirits.get('air', 0.0)
        light = spirits.get('light', 0.0)
        dark = spirits.get('dark', 0.0)
        aether = spirits.get('aether', 0.0)
        
        # Base properties
        pitch = self.base_pitch
        rate = self.base_rate
        volume = 0.7
        
        # Fire: Passionate, energetic
        if fire > 0.5:
            pitch += (fire - 0.5) * 0.4
            rate += (fire - 0.5) * 0.3
            volume += (fire - 0.5) * 0.2
        
        # Water: Calm, flowing
        if water > 0.5:
            pitch -= (water - 0.5) * 0.2
            rate -= (water - 0.5) * 0.25
        
        # Earth: Stable, grounded
        if earth > 0.5:
            pitch -= (earth - 0.5) * 0.1
            # Earth provides stability - less variation
        
        # Air: Light, communicative
        if air > 0.5:
            pitch += (air - 0.5) * 0.2
            rate += (air - 0.5) * 0.2
        
        # Light: Clear, bright
        if light > 0.6:
            pitch += (light - 0.6) * 0.3
            rate += (light - 0.6) * 0.2
        
        # Dark: Deep, introspective
        if dark > 0.5:
            pitch -= (dark - 0.5) * 0.3
            rate -= (dark - 0.5) * 0.3
        
        # Aether: Ethereal, transcendent
        if aether > 0.5:
            pitch += (aether - 0.5) * 0.2
            rate -= (aether - 0.5) * 0.2  # Slow and high = ethereal
        
        # Advanced properties from spirits
        warmth = (water * 0.4) + (earth * 0.3) + (dark * 0.3)
        brightness = (fire * 0.4) + (light * 0.4) + (air * 0.2)
        depth = (earth * 0.3) + (dark * 0.3) + (aether * 0.4)
        clarity = (light * 0.5) + (air * 0.3) + (fire * 0.2)
        
        # Determine timbre from dominant spirit
        dominant_spirit = max(spirits.items(), key=lambda x: x[1])
        timbre_map = {
            'fire': 'bright',
            'water': 'soft',
            'earth': 'rich',
            'air': 'light',
            'light': 'bright',
            'dark': 'deep',
            'aether': 'ethereal'
        }
        timbre = timbre_map.get(dominant_spirit[0], 'balanced')
        
        # Clamp values
        pitch = max(0.5, min(2.0, pitch))
        rate = max(0.5, min(2.0, rate))
        volume = max(0.0, min(1.0, volume))
        warmth = max(0.0, min(1.0, warmth))
        brightness = max(0.0, min(1.0, brightness))
        depth = max(0.0, min(1.0, depth))
        clarity = max(0.0, min(1.0, clarity))
        
        return VoiceProperties(
            pitch=pitch,
            rate=rate,
            volume=volume,
            timbre=timbre,
            warmth=warmth,
            brightness=brightness,
            depth=depth,
            clarity=clarity
        )


class AvatarVoiceTTS:
    """
    Main TTS integration for avatar system with synesthesia-enhanced voice.
    
    This class integrates:
    - Emotional state from EmotionalEngine
    - Spirit energies from avatar
    - Synesthesia mapping
    - Voice property generation
    """
    
    def __init__(self):
        """Initialize avatar voice TTS system"""
        self.voice_mapper = SynesthesiaVoiceMapper()
        self.last_voice_properties = None
        
        logger.info("🎤 AvatarVoiceTTS initialized with synesthesia mapping")
    
    def get_voice_properties_from_emotion(self,
                                         valence: float,
                                         arousal: float,
                                         dominance: float) -> VoiceProperties:
        """
        Get voice properties from emotional state (VAD model)
        
        Args:
            valence: -1 (sad) to 1 (happy)
            arousal: 0 (calm) to 1 (excited)
            dominance: -1 (submissive) to 1 (dominant)
        
        Returns:
            VoiceProperties optimized for current emotional state
        """
        # Map to 4D space
        position_4d = self.voice_mapper.map_emotion_to_4d(valence, arousal, dominance)
        
        # Map to voice properties
        voice_props = self.voice_mapper.map_4d_to_voice(position_4d)
        
        self.last_voice_properties = voice_props
        
        logger.debug(f"🎵 Voice properties: pitch={voice_props.pitch:.2f}, "
                    f"rate={voice_props.rate:.2f}, timbre={voice_props.timbre}")
        
        return voice_props
    
    def get_voice_properties_from_spirits(self, spirits: Dict[str, float]) -> VoiceProperties:
        """
        Get voice properties from spirit energies
        
        Args:
            spirits: Dictionary with spirit values (fire, water, earth, etc.)
        
        Returns:
            VoiceProperties optimized for current spirit state
        """
        voice_props = self.voice_mapper.map_spirits_to_voice(spirits)
        
        self.last_voice_properties = voice_props
        
        logger.debug(f"🎵 Voice from spirits: pitch={voice_props.pitch:.2f}, "
                    f"rate={voice_props.rate:.2f}, timbre={voice_props.timbre}")
        
        return voice_props
    
    def create_speech_message(self, 
                             text: str,
                             voice_properties: VoiceProperties,
                             spirits: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        """
        Create a complete speech message for WebSocket transmission
        
        Args:
            text: Text to speak
            voice_properties: Voice properties from synesthesia mapping
            spirits: Optional spirit energies to include
        
        Returns:
            Dictionary ready for JSON serialization
        """
        message = {
            'type': 'speech',
            'content': text,
            'voice': voice_properties.to_dict()
        }
        
        if spirits:
            message['spirits'] = spirits
        
        return message


# Convenience function for avatar_server.py
def create_avatar_voice_tts() -> AvatarVoiceTTS:
    """Factory function to create AvatarVoiceTTS instance"""
    return AvatarVoiceTTS()
