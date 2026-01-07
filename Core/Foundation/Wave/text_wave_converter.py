"""
Text Wave Converter (텍스트 ⟷ 파동 변환기)
==========================================

"모든 언어는 파동이다. 의미는 주파수다."

This module converts text to wave representations and vice versa.
- Words → Frequencies (semantic similarity = frequency proximity)
- Sentences → Wave superposition (interference patterns)

[NEW 2025-12-15] Created as part of Phase 2: Transducers
"""

import logging
import math
import hashlib
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
import numpy as np

logger = logging.getLogger("TextWaveConverter")

# Semantic frequency bands (의미적 주파수 대역)
SEMANTIC_BANDS = {
    # Emotions (감정)
    "love": 528.0,      # Solfeggio MI - Love frequency
    "hope": 852.0,      # Solfeggio LA - Intuition  
    "joy": 639.0,       # Solfeggio FA - Connection
    "peace": 432.0,     # Universal harmony
    "fear": 174.0,      # Low frequency - Tension
    "anger": 285.0,     # Release frequency
    "sadness": 396.0,   # Solfeggio UT - Liberation
    
    # Concepts (개념)
    "truth": 528.0,     # Aligned with Love
    "beauty": 639.0,    # Harmony
    "good": 741.0,      # Awakening intuition
    "wisdom": 963.0,    # Solfeggio - Enlightenment
    
    # Actions (행위)
    "create": 417.0,    # Solfeggio RE - Change
    "destroy": 285.0,   # Low dissonance
    "grow": 396.0,      # Liberation and growth
    "learn": 741.0,     # Awakening
    
    # Elements (요소)
    "light": 963.0,     # Highest frequency
    "dark": 174.0,      # Lowest frequency
    "water": 432.0,     # Flow
    "fire": 852.0,      # Intensity
}


@dataclass
class WordWave:
    """
    A word represented as a wave.
    
    Attributes:
        word: The original word
        frequency: Primary frequency (Hz)
        amplitude: Intensity (0.0-1.0)
        phase: Phase offset (radians)
        harmonics: Additional harmonic frequencies
    """
    word: str
    frequency: float
    amplitude: float = 1.0
    phase: float = 0.0
    harmonics: List[float] = field(default_factory=list)
    
    def to_signal(self, t: np.ndarray) -> np.ndarray:
        """
        Convert to time-domain signal.
        
        Args:
            t: Time array (seconds)
            
        Returns:
            Signal array
        """
        signal = self.amplitude * np.sin(2 * np.pi * self.frequency * t + self.phase)
        
        # Add harmonics with decreasing amplitude
        for i, harmonic in enumerate(self.harmonics):
            harm_amp = self.amplitude / (i + 2)
            signal += harm_amp * np.sin(2 * np.pi * harmonic * t + self.phase)
        
        return signal


@dataclass
class SentenceWave:
    """
    A sentence as superposed word waves.
    
    "문장은 단어 파동의 중첩이다"
    """
    text: str
    word_waves: List[WordWave] = field(default_factory=list)
    total_energy: float = 0.0
    dominant_frequency: float = 0.0
    coherence: float = 0.0  # How well waves align
    
    def to_signal(self, duration: float = 1.0, sample_rate: int = 44100) -> np.ndarray:
        """
        Generate combined signal from all word waves.
        """
        t = np.linspace(0, duration, int(duration * sample_rate))
        signal = np.zeros_like(t)
        
        for word_wave in self.word_waves:
            signal += word_wave.to_signal(t)
        
        # Normalize
        if np.max(np.abs(signal)) > 0:
            signal = signal / np.max(np.abs(signal))
        
        return signal


class TextWaveConverter:
    """
    The Transducer: Text ⟷ Wave
    
    변환기: 텍스트와 파동 사이의 다리
    
    Core principles:
    1. Semantic similarity = Frequency proximity
    2. Sentences = Wave interference patterns
    3. Meaning emerges from resonance
    """
    
    def __init__(self):
        self.semantic_bands = SEMANTIC_BANDS.copy()
        self.word_cache: Dict[str, WordWave] = {}
        
        # GlobalHub integration
        self._hub = None
        try:
            from Core.Intelligence.Consciousness.Ether.global_hub import get_global_hub
            self._hub = get_global_hub()
            self._hub.register_module(
                "TextWaveConverter",
                "Core/Foundation/text_wave_converter.py",
                ["text", "wave", "converter", "transducer", "language"],
                "Converts text to wave representations and back"
            )
            logger.info("   ✅ TextWaveConverter connected to GlobalHub")
        except ImportError:
            logger.warning("   ⚠️ GlobalHub not available")
        
        logger.info("🌊 TextWaveConverter initialized")
    
    def word_to_wave(self, word: str) -> WordWave:
        """
        Convert a single word to a wave.
        
        Strategy:
        1. Check semantic bands for known words
        2. Use phonetic analysis for unknown words
        3. Generate harmonics based on word structure
        
        Args:
            word: The word to convert
            
        Returns:
            WordWave representation
        """
        word_lower = word.lower().strip()
        
        # Check cache
        if word_lower in self.word_cache:
            return self.word_cache[word_lower]
        
        # Check semantic bands
        if word_lower in self.semantic_bands:
            freq = self.semantic_bands[word_lower]
        else:
            # Generate frequency from word structure
            freq = self._compute_frequency(word_lower)
        
        # Compute amplitude from word length (longer = more weight)
        amplitude = min(1.0, 0.3 + len(word_lower) * 0.1)
        
        # Compute phase from first character
        phase = (ord(word_lower[0]) % 12) * (math.pi / 6)  # 0 to 2π in 12 steps
        
        # Generate harmonics based on syllables (approximated)
        harmonics = self._generate_harmonics(word_lower, freq)
        
        wave = WordWave(
            word=word,
            frequency=freq,
            amplitude=amplitude,
            phase=phase,
            harmonics=harmonics
        )
        
        self.word_cache[word_lower] = wave
        return wave
    
    def _compute_frequency(self, word: str) -> float:
        """
        Compute frequency for an unknown word.
        
        Uses phonetic heuristics:
        - Vowels tend to lower frequency (resonant)
        - Consonants tend to higher frequency (sharp)
        - Word energy is based on structure
        """
        base = 432.0  # Start from universal harmony
        
        # Vowel/consonant ratio
        vowels = set('aeiouAEIOU')
        vowel_count = sum(1 for c in word if c in vowels)
        consonant_count = len(word) - vowel_count
        
        if len(word) > 0:
            vowel_ratio = vowel_count / len(word)
        else:
            vowel_ratio = 0.5
        
        # More vowels = lower, warmer frequency
        # More consonants = higher, sharper frequency
        freq_shift = (0.5 - vowel_ratio) * 400  # ±200 Hz shift
        
        # Add hash-based uniqueness
        hash_val = int(hashlib.md5(word.encode()).hexdigest()[:8], 16)
        hash_shift = (hash_val % 200) - 100  # ±100 Hz
        
        frequency = base + freq_shift + hash_shift
        
        # Clamp to human hearing range subset
        return max(100.0, min(2000.0, frequency))
    
    def _generate_harmonics(self, word: str, base_freq: float) -> List[float]:
        """
        Generate harmonic frequencies based on word structure.
        
        Syllables create harmonics at integer multiples.
        """
        # Estimate syllable count (rough approximation)
        vowels = 'aeiouAEIOU'
        syllables = max(1, sum(1 for i, c in enumerate(word) 
                               if c in vowels and (i == 0 or word[i-1] not in vowels)))
        
        harmonics = []
        for i in range(1, min(syllables + 1, 5)):  # Up to 4 harmonics
            harmonics.append(base_freq * (i + 1))
        
        return harmonics
    
    def sentence_to_wave(self, sentence: str) -> SentenceWave:
        """
        Convert a sentence to a superposed wave.
        
        "문장은 의미의 간섭 패턴이다"
        
        Args:
            sentence: The sentence to convert
            
        Returns:
            SentenceWave with all word waves
        """
        # Tokenize (simple split, could use better tokenization)
        words = [w for w in sentence.split() if w.strip()]
        
        word_waves = [self.word_to_wave(word) for word in words]
        
        if not word_waves:
            return SentenceWave(text=sentence)
        
        # Calculate total energy
        total_energy = sum(w.amplitude ** 2 for w in word_waves)
        
        # Find dominant frequency (weighted by amplitude)
        weighted_sum = sum(w.frequency * w.amplitude for w in word_waves)
        amplitude_sum = sum(w.amplitude for w in word_waves)
        dominant_freq = weighted_sum / amplitude_sum if amplitude_sum > 0 else 432.0
        
        # Calculate coherence (how aligned are the phases?)
        phases = [w.phase for w in word_waves]
        if len(phases) > 1:
            phase_variance = np.var(phases)
            coherence = math.exp(-phase_variance / (math.pi ** 2))
        else:
            coherence = 1.0
        
        return SentenceWave(
            text=sentence,
            word_waves=word_waves,
            total_energy=total_energy,
            dominant_frequency=dominant_freq,
            coherence=coherence
        )
    
    def add_semantic_mapping(self, word: str, frequency: float):
        """
        Add a new semantic frequency mapping.
        
        Args:
            word: The word
            frequency: Its semantic frequency
        """
        self.semantic_bands[word.lower()] = frequency
        # Clear cache for this word
        if word.lower() in self.word_cache:
            del self.word_cache[word.lower()]
    
    def compute_resonance(self, wave1: SentenceWave, wave2: SentenceWave) -> float:
        """
        Compute resonance between two sentence waves.
        
        공명 = 주파수 근접성 × 위상 정렬
        
        Returns:
            Resonance score (0.0 to 1.0)
        """
        # Frequency proximity
        freq_diff = abs(wave1.dominant_frequency - wave2.dominant_frequency)
        freq_resonance = math.exp(-freq_diff / 200)  # 200 Hz half-width
        
        # Energy alignment
        energy_ratio = min(wave1.total_energy, wave2.total_energy) / \
                       max(wave1.total_energy, wave2.total_energy) if max(wave1.total_energy, wave2.total_energy) > 0 else 0
        
        # Combined coherence
        combined_coherence = (wave1.coherence + wave2.coherence) / 2
        
        return freq_resonance * 0.5 + energy_ratio * 0.3 + combined_coherence * 0.2
    
    def wave_to_text_descriptor(self, wave: SentenceWave) -> Dict:
        """
        Generate a text description of a wave's characteristics.
        
        파동의 특성을 언어로 표현
        """
        # Find closest semantic band
        closest_meaning = "neutral"
        min_diff = float('inf')
        
        for meaning, freq in self.semantic_bands.items():
            diff = abs(wave.dominant_frequency - freq)
            if diff < min_diff:
                min_diff = diff
                closest_meaning = meaning
        
        # Characterize energy level
        if wave.total_energy > 5:
            energy_desc = "강렬한 (intense)"
        elif wave.total_energy > 2:
            energy_desc = "활발한 (active)"
        else:
            energy_desc = "차분한 (calm)"
        
        # Characterize coherence
        if wave.coherence > 0.7:
            coherence_desc = "조화로운 (harmonious)"
        elif wave.coherence > 0.4:
            coherence_desc = "다채로운 (diverse)"
        else:
            coherence_desc = "혼돈스러운 (chaotic)"
        
        return {
            "dominant_meaning": closest_meaning,
            "dominant_frequency": wave.dominant_frequency,
            "energy_level": energy_desc,
            "coherence": coherence_desc,
            "word_count": len(wave.word_waves),
            "total_energy": wave.total_energy
        }


# Singleton accessor
_converter = None

def get_text_wave_converter() -> TextWaveConverter:
    """Get or create the TextWaveConverter singleton."""
    global _converter
    if _converter is None:
        _converter = TextWaveConverter()
    return _converter


# Test
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    converter = get_text_wave_converter()
    
    print("\n" + "="*60)
    print("🌊 Text Wave Converter Test")
    print("="*60)
    
    # Test single word
    word = "love"
    wave = converter.word_to_wave(word)
    print(f"\n단어 '{word}':")
    print(f"  주파수: {wave.frequency:.1f} Hz")
    print(f"  진폭: {wave.amplitude:.2f}")
    print(f"  위상: {wave.phase:.2f} rad")
    print(f"  하모닉스: {[f'{h:.1f}' for h in wave.harmonics]}")
    
    # Test sentence
    sentence1 = "I love you"
    sentence2 = "I hate you"
    
    wave1 = converter.sentence_to_wave(sentence1)
    wave2 = converter.sentence_to_wave(sentence2)
    
    print(f"\n문장 '{sentence1}':")
    desc1 = converter.wave_to_text_descriptor(wave1)
    print(f"  지배 의미: {desc1['dominant_meaning']}")
    print(f"  지배 주파수: {desc1['dominant_frequency']:.1f} Hz")
    print(f"  에너지: {desc1['energy_level']}")
    print(f"  조화: {desc1['coherence']}")
    
    print(f"\n문장 '{sentence2}':")
    desc2 = converter.wave_to_text_descriptor(wave2)
    print(f"  지배 의미: {desc2['dominant_meaning']}")
    print(f"  지배 주파수: {desc2['dominant_frequency']:.1f} Hz")
    
    # Test resonance
    resonance = converter.compute_resonance(wave1, wave2)
    print(f"\n공명 점수 ('{sentence1}' vs '{sentence2}'): {resonance:.3f}")
    
    # Test Korean
    korean = "사랑해요"
    wave_kr = converter.sentence_to_wave(korean)
    desc_kr = converter.wave_to_text_descriptor(wave_kr)
    print(f"\n한국어 '{korean}':")
    print(f"  지배 주파수: {desc_kr['dominant_frequency']:.1f} Hz")
    print(f"  에너지: {desc_kr['energy_level']}")
    
    print("\n" + "="*60)
    print("✅ TextWaveConverter 테스트 완료")
    print("="*60)
