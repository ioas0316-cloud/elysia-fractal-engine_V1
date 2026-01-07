"""
Avatar Lip-Sync Engine
======================

립싱크 엔진 - 음성과 입 모양을 자연스럽게 동기화

Phoneme-based lip-sync that maps speech sounds to mouth shapes (visemes).
Works with both real-time audio analysis and TTS output.

Architecture:
    Audio Input → Frequency Analysis → Phoneme Detection → Viseme Mapping → Mouth Animation
    
Key Features:
- Real-time audio frequency analysis
- Phoneme to viseme mapping (Korean + English)
- Smooth animation with interpolation
- Integration with avatar expression system
- Low computational overhead
"""

import logging
import math
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from collections import deque

logger = logging.getLogger("LipSyncEngine")

@dataclass
class Phoneme:
    """
    Phoneme representation with audio characteristics
    
    Phonemes are the basic units of speech sound.
    Each phoneme maps to a specific mouth shape (viseme).
    """
    name: str  # Phoneme name (e.g., 'a', 'i', 'u', 'p', 'm')
    frequency_range: Tuple[float, float]  # Hz range for this phoneme
    mouth_width: float  # 0.0-1.0 (narrow to wide)
    mouth_height: float  # 0.0-1.0 (closed to open)
    duration: float = 0.1  # Average duration in seconds


# Korean Vowel Phonemes (모음)
KOREAN_VOWELS = {
    'a': Phoneme('a', (700, 1200), 0.8, 0.9),  # 아 - wide open
    'e': Phoneme('e', (400, 700), 0.6, 0.7),   # 에 - medium open
    'i': Phoneme('i', (200, 400), 0.3, 0.4),   # 이 - narrow
    'o': Phoneme('o', (400, 600), 0.5, 0.6),   # 오 - rounded
    'u': Phoneme('u', (300, 500), 0.3, 0.5),   # 우 - rounded closed
}

# English Vowel Phonemes
ENGLISH_VOWELS = {
    'aa': Phoneme('aa', (700, 1200), 0.8, 0.9),  # father
    'eh': Phoneme('eh', (500, 800), 0.6, 0.7),   # bet
    'ih': Phoneme('ih', (300, 500), 0.4, 0.5),   # bit
    'oh': Phoneme('oh', (400, 600), 0.5, 0.6),   # boat
    'uh': Phoneme('uh', (300, 500), 0.3, 0.4),   # book
}

# Consonant Phonemes (자음)
CONSONANTS = {
    'p': Phoneme('p', (100, 300), 0.0, 0.0),   # 프 - lips closed
    'b': Phoneme('b', (100, 300), 0.0, 0.0),   # 브 - lips closed
    'm': Phoneme('m', (100, 300), 0.0, 0.0),   # 므 - lips closed
    'f': Phoneme('f', (200, 500), 0.2, 0.1),   # 프 - teeth on lip
    'v': Phoneme('v', (200, 500), 0.2, 0.1),   # 브 - teeth on lip
    's': Phoneme('s', (4000, 8000), 0.3, 0.2), # 스 - teeth close
    'ch': Phoneme('ch', (2000, 4000), 0.4, 0.3), # 츠 - teeth gap
    'k': Phoneme('k', (1000, 3000), 0.5, 0.4), # 크 - back of mouth
    'g': Phoneme('g', (1000, 3000), 0.5, 0.4), # 그 - back of mouth
    't': Phoneme('t', (2000, 5000), 0.3, 0.2), # 트 - tongue on teeth
    'd': Phoneme('d', (2000, 5000), 0.3, 0.2), # 드 - tongue on teeth
    'n': Phoneme('n', (200, 400), 0.3, 0.3),   # 느 - tongue on palate
    'l': Phoneme('l', (200, 400), 0.4, 0.3),   # 르 - tongue tip
    'r': Phoneme('r', (200, 400), 0.4, 0.4),   # 르 - tongue back
}

# Silent/Rest phoneme
SILENCE = Phoneme('silence', (0, 100), 0.0, 0.0, 0.2)


class AudioAnalyzer:
    """
    Analyzes audio to detect phonemes in real-time.
    
    Uses frequency analysis and energy detection to identify
    the current phoneme being spoken.
    """
    
    def __init__(self, sample_rate: int = 16000):
        """
        Initialize audio analyzer
        
        Args:
            sample_rate: Audio sample rate in Hz
        """
        self.sample_rate = sample_rate
        self.phoneme_history = deque(maxlen=5)  # Last 5 detected phonemes
        
        # Combine all phoneme sets
        self.all_phonemes = {
            **KOREAN_VOWELS,
            **ENGLISH_VOWELS,
            **CONSONANTS
        }
        
        logger.info(f"🎵 AudioAnalyzer initialized with {len(self.all_phonemes)} phonemes")
    
    def analyze_frequencies(self, audio_data: List[float]) -> Dict[str, float]:
        """
        Analyze audio frequencies using simple FFT-like approach
        
        Args:
            audio_data: List of audio samples
            
        Returns:
            Dictionary with frequency bands and their energies
        """
        if not audio_data:
            return {}
        
        # Calculate energy in different frequency bands
        # This is a simplified approach - in production, use proper FFT
        energy = sum(abs(sample) for sample in audio_data) / len(audio_data)
        
        # Estimate dominant frequency from zero-crossings
        zero_crossings = 0
        for i in range(1, len(audio_data)):
            if (audio_data[i-1] >= 0 and audio_data[i] < 0) or \
               (audio_data[i-1] < 0 and audio_data[i] >= 0):
                zero_crossings += 1
        
        # Estimate frequency (simplified)
        duration = len(audio_data) / self.sample_rate
        estimated_freq = zero_crossings / (2 * duration) if duration > 0 else 0
        
        return {
            'energy': energy,
            'frequency': estimated_freq,
            'low': energy if estimated_freq < 500 else 0,
            'mid': energy if 500 <= estimated_freq < 2000 else 0,
            'high': energy if estimated_freq >= 2000 else 0
        }
    
    def detect_phoneme(self, frequency_analysis: Dict[str, float]) -> Phoneme:
        """
        Detect most likely phoneme from frequency analysis
        
        Args:
            frequency_analysis: Frequency band energies
            
        Returns:
            Most likely phoneme
        """
        energy = frequency_analysis.get('energy', 0)
        freq = frequency_analysis.get('frequency', 0)
        
        # If very low energy, it's silence
        if energy < 0.02:
            return SILENCE
        
        # Find best matching phoneme based on frequency
        best_match = SILENCE
        best_score = 0
        
        for phoneme in self.all_phonemes.values():
            freq_min, freq_max = phoneme.frequency_range
            
            # Check if frequency is in range
            if freq_min <= freq <= freq_max:
                # Calculate score based on how centered the frequency is
                center = (freq_min + freq_max) / 2
                distance = abs(freq - center)
                max_distance = (freq_max - freq_min) / 2
                score = 1.0 - (distance / max_distance) if max_distance > 0 else 1.0
                
                if score > best_score:
                    best_score = score
                    best_match = phoneme
        
        # Add to history
        self.phoneme_history.append(best_match)
        
        return best_match


class VisemeAnimator:
    """
    Animates mouth shapes (visemes) based on detected phonemes.
    
    Provides smooth interpolation between phonemes for natural animation.
    """
    
    def __init__(self, interpolation_speed: float = 10.0):
        """
        Initialize viseme animator
        
        Args:
            interpolation_speed: How quickly to transition between visemes (higher = faster)
        """
        self.interpolation_speed = interpolation_speed
        self.current_mouth_width = 0.0
        self.current_mouth_height = 0.0
        self.target_mouth_width = 0.0
        self.target_mouth_height = 0.0
        self.last_update_time = time.time()
        
        logger.info(f"👄 VisemeAnimator initialized (speed: {interpolation_speed})")
    
    def set_target_phoneme(self, phoneme: Phoneme):
        """
        Set target phoneme for animation
        
        Args:
            phoneme: Target phoneme to animate towards
        """
        self.target_mouth_width = phoneme.mouth_width
        self.target_mouth_height = phoneme.mouth_height
    
    def update(self, delta_time: float) -> Tuple[float, float]:
        """
        Update animation state
        
        Args:
            delta_time: Time since last update in seconds
            
        Returns:
            Tuple of (mouth_width, mouth_height) in range [0, 1]
        """
        # Smooth interpolation using exponential decay
        alpha = 1.0 - math.exp(-self.interpolation_speed * delta_time)
        
        self.current_mouth_width += (self.target_mouth_width - self.current_mouth_width) * alpha
        self.current_mouth_height += (self.target_mouth_height - self.current_mouth_height) * alpha
        
        return self.current_mouth_width, self.current_mouth_height
    
    def get_mouth_width_for_expression(self) -> float:
        """
        Get current mouth width suitable for avatar expression
        
        Returns:
            Mouth width in range [0, 1]
        """
        return self.current_mouth_width


class LipSyncEngine:
    """
    Complete lip-sync engine integrating audio analysis and viseme animation.
    
    Usage:
        engine = LipSyncEngine()
        
        # In audio callback:
        mouth_width = engine.process_audio(audio_samples)
        avatar.expression.mouth_width = mouth_width
    """
    
    def __init__(self, sample_rate: int = 16000, interpolation_speed: float = 10.0):
        """
        Initialize lip-sync engine
        
        Args:
            sample_rate: Audio sample rate in Hz
            interpolation_speed: Animation smoothness (higher = faster transitions)
        """
        self.analyzer = AudioAnalyzer(sample_rate)
        self.animator = VisemeAnimator(interpolation_speed)
        self.enabled = True
        self.last_update = time.time()
        
        logger.info("🎤 LipSyncEngine initialized and ready")
    
    def process_audio(self, audio_samples: List[float]) -> float:
        """
        Process audio samples and return mouth width for animation
        
        Args:
            audio_samples: List of audio sample values
            
        Returns:
            Mouth width value [0, 1] for avatar expression
        """
        if not self.enabled or not audio_samples:
            return 0.0
        
        # Calculate delta time
        current_time = time.time()
        delta_time = current_time - self.last_update
        self.last_update = current_time
        
        # Analyze audio
        freq_analysis = self.analyzer.analyze_frequencies(audio_samples)
        
        # Detect phoneme
        phoneme = self.analyzer.detect_phoneme(freq_analysis)
        
        # Set animation target
        self.animator.set_target_phoneme(phoneme)
        
        # Update animation
        mouth_width, mouth_height = self.animator.update(delta_time)
        
        # Log occasionally for debugging
        if int(current_time * 2) != int((current_time - delta_time) * 2):
            logger.debug(f"👄 Phoneme: {phoneme.name}, mouth_width: {mouth_width:.2f}")
        
        return mouth_width
    
    def process_tts_event(self, text: str, phoneme_sequence: Optional[List[str]] = None) -> List[Tuple[float, float]]:
        """
        Process TTS text and generate phoneme sequence with timings
        
        Args:
            text: Text being spoken
            phoneme_sequence: Optional pre-computed phoneme sequence
            
        Returns:
            List of (timestamp, mouth_width) tuples for animation
        """
        # Simple heuristic-based phoneme generation
        # In production, use a proper text-to-phoneme system
        
        if phoneme_sequence is None:
            # Generate simple phoneme sequence from text
            phoneme_sequence = self._text_to_phonemes(text)
        
        # Generate animation keyframes
        keyframes = []
        current_time = 0.0
        
        for phoneme_name in phoneme_sequence:
            phoneme = self.all_phonemes.get(phoneme_name, SILENCE)
            keyframes.append((current_time, phoneme.mouth_width))
            current_time += phoneme.duration
        
        return keyframes
    
    def _text_to_phonemes(self, text: str) -> List[str]:
        """
        Simple text to phoneme conversion (heuristic-based)
        
        Args:
            text: Input text
            
        Returns:
            List of phoneme names
        """
        # This is a very simple approach - just for demonstration
        # Production system should use proper G2P (Grapheme-to-Phoneme)
        
        phonemes = []
        text = text.lower()
        
        # Simple vowel detection
        for char in text:
            if char in 'aeiou':
                if char in ENGLISH_VOWELS:
                    phonemes.append(char * 2)  # Map to long vowel
                elif char in KOREAN_VOWELS:
                    phonemes.append(char)
            elif char.isalpha():
                # Try to map consonant
                if char in CONSONANTS:
                    phonemes.append(char)
            else:
                # Space or punctuation - add silence
                phonemes.append('silence')
        
        return phonemes
    
    def enable(self):
        """Enable lip-sync processing"""
        self.enabled = True
        logger.info("✅ Lip-sync enabled")
    
    def disable(self):
        """Disable lip-sync processing"""
        self.enabled = False
        logger.info("⏸️ Lip-sync disabled")
    
    @property
    def all_phonemes(self):
        """Get all available phonemes"""
        return {
            **KOREAN_VOWELS,
            **ENGLISH_VOWELS,
            **CONSONANTS,
            'silence': SILENCE
        }


# Factory function for easy instantiation
def create_lipsync_engine(sample_rate: int = 16000) -> LipSyncEngine:
    """
    Create and return a LipSyncEngine instance
    
    Args:
        sample_rate: Audio sample rate in Hz
        
    Returns:
        Configured LipSyncEngine
    """
    return LipSyncEngine(sample_rate=sample_rate)
