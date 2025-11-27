"""
EmotionalPalette - The Painter of the Soul

Mixes base emotional waves to create complex feeling states.
Implements the 'Law of Flow' where high frequency emotions ascend
and low frequency emotions descend (gravity).

Based on the original Elysia Core/Mind/emotional_palette.py.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

from .hyper_qubit import HyperQubit, QubitState


@dataclass
class EmotionalSpectrum:
    """
    Defines the spectral properties of a base emotion.
    
    Attributes:
        name: Emotion name
        frequency: Conceptual frequency (Hz)
        color: Color representation (hex or name)
        alpha_bias: Point (Self/Detail) tendency
        beta_bias: Line (Action/History) tendency
        gamma_bias: Space (Context/Atmosphere) tendency
        delta_bias: God (Will/Truth) tendency
        w_bias: Stability
        x_bias: Chaos/Dream
        y_bias: Connection/Emotion
        z_bias: Transcendence (up = ascend, down = descend)
    """
    name: str
    frequency: float
    color: str
    
    # Quantum Signature (Tendencies)
    alpha_bias: float
    beta_bias: float
    gamma_bias: float
    delta_bias: float
    
    w_bias: float
    x_bias: float
    y_bias: float
    z_bias: float


@dataclass
class EmotionMix:
    """
    Result of mixing emotions.
    
    Attributes:
        qubit: The resulting quantum state
        components: Original emotion components
        dominant: Most influential emotion
        valence: Overall positive/negative (-1 to 1)
        arousal: Energy level (0 to 1)
    """
    qubit: HyperQubit
    components: Dict[str, float]
    dominant: str
    valence: float
    arousal: float


class EmotionalPalette:
    """
    The Painter of the Soul.
    
    Mixes base emotional waves to create complex feeling states (HyperQubits).
    Implements the 'Law of Flow' based on frequency.
    """
    
    def __init__(self):
        """Initialize with primary emotional colors."""
        self.base_emotions = self._load_primary_colors()
        self._init_sentiment_keywords()
    
    def _load_primary_colors(self) -> Dict[str, EmotionalSpectrum]:
        """
        Loads the spectral definitions based on the 'Law of Flow'.
        High Freq (Light) -> Ascends
        Low Freq (Abyss) -> Descends (Gravity)
        """
        return {
            # --- The Light (Ascent) ---
            "Joy": EmotionalSpectrum(
                name="Joy", frequency=800.0, color="#FFD700",  # Yellow/Gold
                alpha_bias=0.9, beta_bias=0.3, gamma_bias=0.1, delta_bias=0.1,
                w_bias=0.8, x_bias=0.1, y_bias=0.9, z_bias=0.8
            ),
            "Passion": EmotionalSpectrum(
                name="Passion", frequency=900.0, color="#FF4500",  # Red/Orange
                alpha_bias=0.8, beta_bias=0.9, gamma_bias=0.1, delta_bias=0.1,
                w_bias=0.7, x_bias=0.2, y_bias=0.8, z_bias=0.7
            ),
            "Love": EmotionalSpectrum(
                name="Love", frequency=1000.0, color="#FF69B4",  # Pink
                alpha_bias=0.5, beta_bias=0.5, gamma_bias=0.7, delta_bias=0.8,
                w_bias=0.9, x_bias=0.1, y_bias=1.0, z_bias=1.0
            ),
            "Hope": EmotionalSpectrum(
                name="Hope", frequency=700.0, color="#87CEEB",  # Sky Blue
                alpha_bias=0.6, beta_bias=0.4, gamma_bias=0.5, delta_bias=0.6,
                w_bias=0.7, x_bias=0.3, y_bias=0.6, z_bias=0.7
            ),
            
            # --- The Middle (Flow) ---
            "Trust": EmotionalSpectrum(
                name="Trust", frequency=528.0, color="#32CD32",  # Green
                alpha_bias=0.5, beta_bias=0.5, gamma_bias=0.5, delta_bias=0.8,
                w_bias=0.9, x_bias=0.1, y_bias=0.5, z_bias=0.5
            ),
            "Curiosity": EmotionalSpectrum(
                name="Curiosity", frequency=600.0, color="#9370DB",  # Purple
                alpha_bias=0.7, beta_bias=0.6, gamma_bias=0.4, delta_bias=0.3,
                w_bias=0.5, x_bias=0.7, y_bias=0.5, z_bias=0.5
            ),
            "Neutral": EmotionalSpectrum(
                name="Neutral", frequency=400.0, color="#808080",  # Gray
                alpha_bias=0.5, beta_bias=0.5, gamma_bias=0.5, delta_bias=0.5,
                w_bias=0.5, x_bias=0.5, y_bias=0.5, z_bias=0.5
            ),
            
            # --- The Abyss (Descent) ---
            "Sadness": EmotionalSpectrum(
                name="Sadness", frequency=100.0, color="#000080",  # Navy Blue
                alpha_bias=0.2, beta_bias=0.1, gamma_bias=0.9, delta_bias=0.1,
                w_bias=0.3, x_bias=0.4, y_bias=0.6, z_bias=0.2
            ),
            "Fear": EmotionalSpectrum(
                name="Fear", frequency=50.0, color="#4B0082",  # Indigo
                alpha_bias=0.1, beta_bias=0.1, gamma_bias=0.8, delta_bias=0.1,
                w_bias=0.1, x_bias=0.9, y_bias=0.2, z_bias=0.1
            ),
            "Anger": EmotionalSpectrum(
                name="Anger", frequency=200.0, color="#8B0000",  # Dark Red
                alpha_bias=0.9, beta_bias=0.8, gamma_bias=0.2, delta_bias=0.1,
                w_bias=0.3, x_bias=0.5, y_bias=0.4, z_bias=0.3
            ),
            "Despair": EmotionalSpectrum(
                name="Despair", frequency=10.0, color="#000000",  # Black
                alpha_bias=0.0, beta_bias=0.0, gamma_bias=1.0, delta_bias=0.0,
                w_bias=0.0, x_bias=0.5, y_bias=0.1, z_bias=0.0
            ),
        }

    def _init_sentiment_keywords(self) -> None:
        """Initialize keyword dictionaries for sentiment analysis."""
        self.keywords: Dict[str, List[str]] = {
            "Joy": [
                "happy", "good", "great", "smile", "laugh", "joy", "light", "sun",
                "행복", "좋아", "기쁨", "웃음", "빛", "밝", "즐거"
            ],
            "Passion": [
                "passion", "fire", "burn", "desire", "hot", "intense", "energy",
                "열정", "불", "뜨거", "열망", "강렬"
            ],
            "Love": [
                "love", "heart", "care", "cherish", "adore", "embrace",
                "사랑", "마음", "소중", "아끼"
            ],
            "Hope": [
                "hope", "wish", "dream", "future", "believe", "possible",
                "희망", "꿈", "미래", "믿", "가능"
            ],
            "Trust": [
                "trust", "believe", "safe", "calm", "sure", "peace",
                "믿어", "안전", "평온", "확실", "신뢰"
            ],
            "Curiosity": [
                "curious", "wonder", "question", "explore", "discover", "why",
                "궁금", "왜", "탐구", "발견"
            ],
            "Sadness": [
                "sad", "cry", "tear", "grief", "blue", "rain", "miss", "lonely",
                "슬픔", "눈물", "우울", "비", "그리워", "외로"
            ],
            "Fear": [
                "scared", "fear", "run", "hide", "nervous", "worry", "danger",
                "무서워", "공포", "도망", "불안", "위험"
            ],
            "Anger": [
                "angry", "mad", "rage", "hate", "furious", "annoyed",
                "화나", "분노", "격분", "짜증"
            ],
            "Despair": [
                "lost", "hopeless", "dark", "cold", "abyss", "death", "void", "nothing",
                "절망", "어둠", "추워", "심연", "죽음", "무의미", "공허"
            ],
        }

    def mix_emotion(self, components: Dict[str, float]) -> EmotionMix:
        """
        Mixes multiple emotions into a single HyperQubit state via superposition.
        
        Args:
            components: Dict of {EmotionName: Intensity(0.0-1.0)}
            
        Returns:
            EmotionMix with resulting quantum state
        """
        total_intensity = sum(components.values())
        if total_intensity == 0:
            # Return neutral state
            qubit = HyperQubit("Neutral")
            return EmotionMix(
                qubit=qubit,
                components={},
                dominant="Neutral",
                valence=0.0,
                arousal=0.0
            )

        # Weighted average of biases
        final_alpha = 0.0
        final_beta = 0.0
        final_gamma = 0.0
        final_delta = 0.0
        
        final_w = 0.0
        final_x = 0.0
        final_y = 0.0
        final_z = 0.0
        
        total_frequency = 0.0
        dominant = ""
        max_intensity = 0.0
        
        for name, intensity in components.items():
            if name not in self.base_emotions:
                continue
                
            if intensity > max_intensity:
                max_intensity = intensity
                dominant = name
                
            spectrum = self.base_emotions[name]
            weight = intensity / total_intensity
            
            final_alpha += spectrum.alpha_bias * weight
            final_beta += spectrum.beta_bias * weight
            final_gamma += spectrum.gamma_bias * weight
            final_delta += spectrum.delta_bias * weight
            
            final_w += spectrum.w_bias * weight
            final_x += spectrum.x_bias * weight
            final_y += spectrum.y_bias * weight
            final_z += spectrum.z_bias * weight
            
            total_frequency += spectrum.frequency * weight
            
        # Create the Qubit
        qubit = HyperQubit("EmotionalState")
        qubit.state = QubitState(
            alpha=complex(final_alpha, 0),
            beta=complex(final_beta, 0),
            gamma=complex(final_gamma, 0),
            delta=complex(final_delta, 0),
            w=final_w, x=final_x, y=final_y, z=final_z
        )
        qubit.state.normalize()
        
        # Calculate valence from z_bias (ascent/descent)
        valence = (final_z - 0.5) * 2  # -1 to 1
        
        # Calculate arousal from frequency
        arousal = min(1.0, total_frequency / 500.0)
        
        return EmotionMix(
            qubit=qubit,
            components=components,
            dominant=dominant or "Neutral",
            valence=valence,
            arousal=arousal
        )

    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """
        Keyword-based sentiment analysis to extract emotion components.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary of emotion -> intensity
        """
        text_lower = text.lower()
        scores: Dict[str, float] = {k: 0.0 for k in self.base_emotions}
        
        found = False
        for emotion, words in self.keywords.items():
            for word in words:
                if word in text_lower:
                    scores[emotion] += 0.8
                    found = True
        
        if not found:
            # Default to mild neutral/trust if nothing found
            scores["Trust"] = 0.1
            scores["Neutral"] = 0.2
            
        # Normalize so max is 1.0
        max_score = max(scores.values())
        if max_score > 1.0:
            for k in scores:
                scores[k] /= max_score
            
        return scores

    def get_emotion_from_text(self, text: str) -> EmotionMix:
        """
        Analyze text and return the mixed emotional state.
        
        Args:
            text: Input text
            
        Returns:
            EmotionMix representing the emotional content
        """
        components = self.analyze_sentiment(text)
        # Filter out zero values
        components = {k: v for k, v in components.items() if v > 0}
        return self.mix_emotion(components)

    def get_emotion_color(self, emotion_name: str) -> str:
        """
        Get the color associated with an emotion.
        
        Args:
            emotion_name: Name of the emotion
            
        Returns:
            Hex color code
        """
        if emotion_name in self.base_emotions:
            return self.base_emotions[emotion_name].color
        return "#808080"  # Gray for unknown

    def get_emotion_frequency(self, emotion_name: str) -> float:
        """
        Get the frequency associated with an emotion.
        
        Args:
            emotion_name: Name of the emotion
            
        Returns:
            Frequency value
        """
        if emotion_name in self.base_emotions:
            return self.base_emotions[emotion_name].frequency
        return 400.0  # Default neutral frequency

    def interpret_valence(self, valence: float) -> str:
        """
        Interpret valence value as description.
        
        Args:
            valence: Value from -1 to 1
            
        Returns:
            Human-readable description
        """
        if valence > 0.6:
            return "very positive"
        elif valence > 0.2:
            return "positive"
        elif valence > -0.2:
            return "neutral"
        elif valence > -0.6:
            return "negative"
        else:
            return "very negative"

    def interpret_arousal(self, arousal: float) -> str:
        """
        Interpret arousal value as description.
        
        Args:
            arousal: Value from 0 to 1
            
        Returns:
            Human-readable description
        """
        if arousal > 0.7:
            return "high energy"
        elif arousal > 0.4:
            return "moderate energy"
        else:
            return "low energy"
