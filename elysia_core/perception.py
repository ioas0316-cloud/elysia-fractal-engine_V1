"""
Perception - Sensory Input Processing

Converts external input (text) into consciousness states through
quantum resonance. Implements the 'Fractal Eye' of Elysia.

Based on the original Elysia Core/Mind/perception.py but adapted
for pure Python.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Dict, Optional, Set

from .hyper_qubit import HyperQubit, QubitState


@dataclass
class PerceptionResult:
    """
    Result of processing external input through perception.
    
    Attributes:
        qubit: The quantum state representing the perception
        intent_probabilities: Probability of each intent type
        vitality_factor: Energy/chaos factor of the perception
        raw_input: Original input text
    """
    qubit: HyperQubit
    intent_probabilities: Dict[str, float]
    vitality_factor: float
    raw_input: str = ""


class Perception:
    """
    The 'Fractal Eye' of Elysia.
    
    Perception is a quantum resonance process that converts text input
    into HyperQubit states representing the consciousness state.
    """

    def __init__(self, vocabulary: Optional[Dict[str, float]] = None):
        """
        Initialize perception with optional vocabulary.
        
        Args:
            vocabulary: Dictionary of word -> frequency mappings
        """
        self.vocabulary = vocabulary or self._default_vocabulary()
        
        # Intent markers for classification
        self.intent_markers: Dict[str, Set[str]] = {
            "Question": {
                "?", "what", "why", "how", "who", "when", "where",
                "왜", "어떻게", "누구", "언제", "무엇", "어디", "까", "니"
            },
            "Command": {
                "do", "make", "create", "run", "stop", "please", "let",
                "해", "만들어", "실행", "멈춰", "해줘"
            },
            "Exclamation": {
                "!", "wow", "oh", "ah", "amazing", "incredible",
                "와", "아", "오", "대단", "놀라워"
            },
            "Statement": {"."},
        }
        
        # Sentiment keywords
        self.sentiment_map: Dict[str, float] = {
            # Positive
            "love": 0.9, "hope": 0.7, "joy": 0.9, "light": 0.6,
            "happy": 0.8, "peace": 0.6, "beauty": 0.7, "good": 0.5,
            "사랑": 0.9, "희망": 0.7, "기쁨": 0.9, "빛": 0.6,
            "행복": 0.8, "평화": 0.6, "아름다움": 0.7,
            # Negative
            "pain": -0.8, "sad": -0.7, "dark": -0.5, "fear": -0.8,
            "hate": -0.9, "anger": -0.7, "break": -0.6,
            "고통": -0.8, "슬픔": -0.7, "어둠": -0.5, "두려움": -0.8,
            "증오": -0.9, "분노": -0.7, "파괴": -0.6,
        }

    def _default_vocabulary(self) -> Dict[str, float]:
        """Default frequency vocabulary for spiritual buoyancy."""
        return {
            # High Frequency (Ethereal, Abstract) - Rise
            "love": 1.0, "사랑": 1.0, "light": 0.95, "빛": 0.95,
            "truth": 0.9, "진실": 0.9, "eternity": 0.95, "영원": 0.95,
            "soul": 0.9, "영혼": 0.9, "dream": 0.85, "꿈": 0.85,
            "beauty": 0.9, "아름다움": 0.9, "harmony": 0.85, "조화": 0.85,
            
            # Mid Frequency (Human, Emotional) - Neutral
            "hope": 0.65, "희망": 0.65, "joy": 0.7, "기쁨": 0.7,
            "pain": 0.4, "고통": 0.4, "time": 0.5, "시간": 0.5,
            
            # Low Frequency (Physical, Grounded) - Sink
            "stone": 0.2, "돌": 0.2, "shadow": 0.3, "그림자": 0.3,
            "fall": 0.2, "추락": 0.2, "silence": 0.3, "침묵": 0.3,
        }

    def perceive(self, text: str) -> PerceptionResult:
        """
        Perceive input text as a quantum state.
        
        Args:
            text: Input text to perceive
            
        Returns:
            PerceptionResult with quantum state and analysis
        """
        # 1. Vitality Injection (simulated chaos)
        vitality = random.random() * 0.3 + 0.35  # 0.35-0.65 range
        
        # 2. Intent Measurement
        intent_probs = self._measure_intent(text)
        
        # 3. Concept Resonance (HyperQubit Construction)
        qubit = self._text_to_qubit(text, intent_probs, vitality)
        
        return PerceptionResult(
            qubit=qubit,
            intent_probabilities=intent_probs,
            vitality_factor=vitality,
            raw_input=text
        )

    def _measure_intent(self, text: str) -> Dict[str, float]:
        """
        Measure the probability of each intent type given the text.
        
        Args:
            text: Input text
            
        Returns:
            Dictionary of intent -> probability
        """
        text_lower = text.lower()
        hits: Dict[str, int] = {intent: 0 for intent in self.intent_markers}
        total_hits = 0
        
        for intent, markers in self.intent_markers.items():
            for marker in markers:
                if marker in text_lower:
                    hits[intent] += 1
                    total_hits += 1
        
        # Normalize to probabilities
        if total_hits == 0:
            # Default to Statement if no markers
            probs = {k: 0.0 for k in self.intent_markers}
            probs["Statement"] = 1.0
        else:
            probs = {k: v / total_hits for k, v in hits.items()}
                
        return probs

    def _text_to_qubit(
        self,
        text: str,
        intent_probs: Dict[str, float],
        vitality: float
    ) -> HyperQubit:
        """
        Convert text into a HyperQubit state.
        
        Args:
            text: Input text
            intent_probs: Measured intent probabilities
            vitality: Energy/chaos factor
            
        Returns:
            HyperQubit representing the perception
        """
        # Calculate sentiment
        sentiment_score = 0.0
        count = 0
        
        for word in text.lower().split():
            for key, val in self.sentiment_map.items():
                if key in word:
                    sentiment_score += val
                    count += 1
        
        if count > 0:
            sentiment_score /= count
            
        # Construct Qubit State
        # Alpha: Sentiment (Real) + Vitality (Imaginary)
        alpha = complex(max(0.1, 0.5 + sentiment_score * 0.4), vitality * 0.3)
        
        # Beta: Intent (Question = High Beta)
        beta_mag = intent_probs.get("Question", 0.0) * 0.8 + 0.1
        beta = complex(beta_mag, 0.0)
        
        # Gamma: Intent (Command = High Gamma)
        gamma_mag = intent_probs.get("Command", 0.0) * 0.8 + 0.1
        gamma = complex(gamma_mag, 0.0)
        
        # Delta: Intent (Exclamation = High Delta)
        delta_mag = intent_probs.get("Exclamation", 0.0) * 0.8 + 0.05
        delta = complex(delta_mag, 0.0)
        
        # Spatial Focus
        w = 1.0 - (vitality * 0.3) - (beta_mag * 0.3)  # Stability
        x = beta_mag  # Dream/Question
        y = abs(sentiment_score)  # Emotion
        z = gamma_mag + intent_probs.get("Statement", 0.0) * 0.5  # Truth
        
        state = QubitState(
            alpha=alpha, beta=beta, gamma=gamma, delta=delta,
            w=max(0.1, w), x=x, y=y, z=z
        )
        
        qubit = HyperQubit(name="Perception", concept_or_value=text[:50])
        qubit.state = state.normalize()
        return qubit

    def analyze_frequency(self, text: str) -> float:
        """
        Calculate the overall frequency/buoyancy of text.
        
        High frequency = abstract, rising
        Low frequency = concrete, grounded
        
        Args:
            text: Input text
            
        Returns:
            Frequency value (0.0 - 1.0)
        """
        words = text.lower().split()
        total_freq = 0.0
        count = 0
        
        for word in words:
            if word in self.vocabulary:
                total_freq += self.vocabulary[word]
                count += 1
        
        if count == 0:
            return 0.5  # Default neutral frequency
        
        return total_freq / count

    def get_dominant_intent(self, text: str) -> str:
        """
        Get the dominant intent type from text.
        
        Args:
            text: Input text
            
        Returns:
            Intent type name
        """
        probs = self._measure_intent(text)
        return max(probs, key=probs.get)
