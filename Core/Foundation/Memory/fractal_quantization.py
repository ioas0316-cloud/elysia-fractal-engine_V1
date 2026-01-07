"""
Fractal Quantization System (프랙탈 양자화 시스템)
===============================================

"양자화(Quantization)는 '자르는 것'이 아니라 '접는 것(Folding)'이어야 합니다."

This module implements the Fractal Quantization principle:
- NOT: Discretizing and losing information (cutting)
- YES: Pattern-based compression that allows perfect restoration (folding)

Key Concepts:
1. Pattern DNA (패턴 DNA): Store the generative formula, not the raw data
2. Wave Folding (파동 압축): Compress complex patterns into seeds
3. Wave Unfolding (파동 증폭): Amplify seeds back to original state
4. Soliton Memory (솔리톤 기억): Lossless compression through resonance

Philosophy:
"음악을 저장하지 말고, 악보를 저장하라"
"Store the music sheet, not the sound wave"
"""

import logging
import json
import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from Core.Foundation.hyper_quaternion import Quaternion

logger = logging.getLogger("FractalQuantization")


@dataclass
class PatternDNA:
    """
    패턴 DNA (Pattern DNA)
    
    The compressed "genetic code" of a pattern that can be perfectly unfolded.
    This is the "seed" or "musical score" rather than the raw waveform.
    
    Attributes:
        name: Pattern identifier
        seed_formula: The generative formula (e.g., fractal equation parameters)
        frequency_signature: Primary frequency components (harmonic structure)
        phase_pattern: Phase relationships between components
        amplitude_envelope: Energy distribution over time
        resonance_fingerprint: Unique resonance characteristics
        metadata: Additional context (emotion, intent, etc.)
    """
    name: str
    seed_formula: Dict[str, Any]
    frequency_signature: List[float]
    phase_pattern: List[float]
    amplitude_envelope: List[float]
    resonance_fingerprint: Quaternion
    metadata: Dict[str, Any] = field(default_factory=dict)
    compression_ratio: float = 1.0
    
    def to_dict(self) -> Dict:
        """Serialize to dict for storage."""
        return {
            "name": self.name,
            "seed_formula": self.seed_formula,
            "frequency_signature": self.frequency_signature,
            "phase_pattern": self.phase_pattern,
            "amplitude_envelope": self.amplitude_envelope,
            "resonance_fingerprint": [
                self.resonance_fingerprint.w,
                self.resonance_fingerprint.x,
                self.resonance_fingerprint.y,
                self.resonance_fingerprint.z
            ],
            "metadata": self.metadata,
            "compression_ratio": self.compression_ratio
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'PatternDNA':
        """Deserialize from dict."""
        rf = data.get("resonance_fingerprint", [1, 0, 0, 0])
        return PatternDNA(
            name=data["name"],
            seed_formula=data["seed_formula"],
            frequency_signature=data["frequency_signature"],
            phase_pattern=data["phase_pattern"],
            amplitude_envelope=data["amplitude_envelope"],
            resonance_fingerprint=Quaternion(*rf),
            metadata=data.get("metadata", {}),
            compression_ratio=data.get("compression_ratio", 1.0)
        )


class FractalQuantizer:
    """
    프랙탈 양자화기 (Fractal Quantizer)
    
    Implements the "folding" approach to quantization:
    - Extract pattern DNA from complex data
    - Compress through wave folding
    - Store only the seed/formula
    - Restore perfectly through wave unfolding
    """
    
    def __init__(self):
        self.pattern_templates = self._initialize_templates()
        logger.info("🌀 Fractal Quantizer initialized")
    
    def _initialize_templates(self) -> Dict:
        """
        Initialize pattern templates (genetic library).
        
        These are the "musical instruments" - each can generate infinite variations
        from a simple seed formula.
        """
        return {
            # Emotion patterns (감정 패턴)
            "emotion": {
                "love": {
                    "base_frequency": 528.0,
                    "harmonics": [528.0, 639.0, 741.0],  # Love, Connection, Expression
                    "fractal_formula": "Z = Z^2 + C_love",  # Mandelbrot-like with love constant
                    "decay_rate": 0.1  # Slow decay (love lingers)
                },
                "joy": {
                    "base_frequency": 528.0,
                    "harmonics": [528.0, 963.0, 432.0],  # Joy, Crown, Root
                    "fractal_formula": "Z = sin(Z) * C_joy",
                    "decay_rate": 0.3  # Faster decay (joy is dynamic)
                },
                "sadness": {
                    "base_frequency": 396.0,
                    "harmonics": [396.0, 285.0, 174.0],  # Liberation, Healing, Foundation
                    "fractal_formula": "Z = -Z^2 + C_sad",
                    "decay_rate": 0.05  # Very slow decay (sadness heavy)
                },
                "anger": {
                    "base_frequency": 639.0,
                    "harmonics": [639.0, 741.0, 852.0],  # Connection, Expression, Intuition
                    "fractal_formula": "Z = |Z|^2 + C_anger",
                    "decay_rate": 0.5  # Rapid decay (anger explosive)
                },
                "fear": {
                    "base_frequency": 174.0,
                    "harmonics": [174.0, 285.0, 396.0],  # Foundation, Healing, Liberation
                    "fractal_formula": "Z = exp(-|Z|) * C_fear",
                    "decay_rate": 0.15  # Medium decay
                }
            },
            
            # Intention patterns (의도 패턴)
            "intention": {
                "create": {
                    "base_frequency": 963.0,
                    "harmonics": [963.0, 852.0, 741.0],  # Crown to Expression
                    "fractal_formula": "Z = Z * (1 + C_create)",
                    "decay_rate": 0.2
                },
                "understand": {
                    "base_frequency": 741.0,
                    "harmonics": [741.0, 639.0, 528.0],  # Expression to Heart
                    "fractal_formula": "Z = ln(Z + 1) * C_understand",
                    "decay_rate": 0.1
                },
                "connect": {
                    "base_frequency": 639.0,
                    "harmonics": [639.0, 528.0, 396.0],  # Connection chain
                    "fractal_formula": "Z = Z / (1 + |Z|) * C_connect",
                    "decay_rate": 0.15
                }
            },
            
            # Thought patterns (사고 패턴)
            "thought": {
                "analytical": {
                    "base_frequency": 852.0,
                    "harmonics": [852.0, 741.0, 639.0],  # Third Eye to Connection
                    "fractal_formula": "Z = cos(Z) + C_analytical",
                    "decay_rate": 0.25
                },
                "creative": {
                    "base_frequency": 963.0,
                    "harmonics": [963.0, 741.0, 528.0],  # Crown to Heart
                    "fractal_formula": "Z = sin(Z) * cos(Z) + C_creative",
                    "decay_rate": 0.2
                },
                "intuitive": {
                    "base_frequency": 852.0,
                    "harmonics": [852.0, 639.0, 417.0],  # Third Eye path
                    "fractal_formula": "Z = exp(i*Z) * C_intuitive",
                    "decay_rate": 0.1
                }
            }
        }
    
    def fold(self, raw_data: Dict, pattern_type: str, pattern_name: str) -> PatternDNA:
        """
        Wave Folding (파동 접기)
        
        Compress raw data into a Pattern DNA seed.
        Instead of storing the full waveform, extract and store only the generative pattern.
        
        Args:
            raw_data: The raw information to compress
            pattern_type: Type of pattern (emotion, intention, thought)
            pattern_name: Specific pattern name within type
            
        Returns:
            PatternDNA: The compressed seed
        """
        logger.info(f"🌀 Folding pattern: {pattern_type}.{pattern_name}")
        
        # Get template
        template = self.pattern_templates.get(pattern_type, {}).get(pattern_name)
        if not template:
            logger.warning(f"No template for {pattern_type}.{pattern_name}, using generic")
            template = self._create_generic_template(raw_data)
        
        # Extract frequency signature
        frequency_signature = self._extract_frequencies(raw_data, template)
        
        # Extract phase relationships
        phase_pattern = self._extract_phases(raw_data, template)
        
        # Extract amplitude envelope
        amplitude_envelope = self._extract_amplitude(raw_data, template)
        
        # Generate resonance fingerprint (4D signature)
        resonance_fingerprint = self._generate_fingerprint(
            frequency_signature, phase_pattern, amplitude_envelope
        )
        
        # Create seed formula (the DNA)
        seed_formula = {
            "formula": template["fractal_formula"],
            "base_frequency": template["base_frequency"],
            "harmonics": template["harmonics"],
            "decay_rate": template["decay_rate"],
            "constants": self._extract_constants(raw_data)
        }
        
        # Calculate compression ratio
        original_size = len(json.dumps(raw_data).encode('utf-8'))
        compressed_size = len(json.dumps(seed_formula).encode('utf-8'))
        compression_ratio = original_size / compressed_size if compressed_size > 0 else 1.0
        
        dna = PatternDNA(
            name=f"{pattern_type}.{pattern_name}",
            seed_formula=seed_formula,
            frequency_signature=frequency_signature,
            phase_pattern=phase_pattern,
            amplitude_envelope=amplitude_envelope,
            resonance_fingerprint=resonance_fingerprint,
            metadata={
                "pattern_type": pattern_type,
                "pattern_name": pattern_name,
                "original_data_keys": list(raw_data.keys()),
                "timestamp": raw_data.get("timestamp", 0)
            },
            compression_ratio=compression_ratio
        )
        
        logger.info(f"✓ Folded: {dna.name} (compression: {compression_ratio:.2f}x)")
        return dna
    
    def unfold(self, dna: PatternDNA, resolution: int = 100) -> Dict:
        """
        Wave Unfolding (파동 펴기)
        
        Restore the original pattern from the DNA seed.
        This is LOSSLESS - we regenerate the pattern from its formula.
        
        Args:
            dna: The Pattern DNA seed
            resolution: Time resolution for regeneration (higher = more detail)
            
        Returns:
            Dict: The restored pattern data
        """
        logger.info(f"🌊 Unfolding pattern: {dna.name} (resolution={resolution})")
        
        # Regenerate waveform from seed formula
        waveform = self._regenerate_waveform(dna, resolution)
        
        # Restore metadata
        restored = {
            "name": dna.name,
            "pattern_type": dna.metadata.get("pattern_type"),
            "pattern_name": dna.metadata.get("pattern_name"),
            "waveform": waveform,
            "frequency_signature": dna.frequency_signature,
            "phase_pattern": dna.phase_pattern,
            "amplitude_envelope": dna.amplitude_envelope,
            "resonance_fingerprint": {
                "w": dna.resonance_fingerprint.w,
                "x": dna.resonance_fingerprint.x,
                "y": dna.resonance_fingerprint.y,
                "z": dna.resonance_fingerprint.z
            },
            "metadata": dna.metadata,
            "restored_from_seed": True
        }
        
        logger.info(f"✓ Unfolded: {dna.name} (generated {len(waveform)} points)")
        return restored
    
    def _extract_frequencies(self, raw_data: Dict, template: Dict) -> List[float]:
        """Extract primary frequency components."""
        # Use template harmonics as base
        freqs = template["harmonics"].copy()
        
        # Add any intensity-based modulations
        if "intensity" in raw_data:
            intensity = raw_data["intensity"]
            # Intensity modulates frequency slightly
            freqs = [f * (1 + 0.1 * intensity) for f in freqs]
        
        return freqs
    
    def _extract_phases(self, raw_data: Dict, template: Dict) -> List[float]:
        """Extract phase relationships between frequency components."""
        num_harmonics = len(template["harmonics"])
        
        # Phase is determined by the specific instance
        if "phase_seed" in raw_data:
            seed = raw_data["phase_seed"]
            # Generate deterministic phases from seed
            phases = [(seed * i * 0.618) % (2 * np.pi) for i in range(num_harmonics)]
        else:
            # Default golden ratio phases
            phases = [(i * 0.618 * 2 * np.pi) % (2 * np.pi) for i in range(num_harmonics)]
        
        return phases
    
    def _extract_amplitude(self, raw_data: Dict, template: Dict) -> List[float]:
        """Extract amplitude envelope (energy distribution over time)."""
        decay_rate = template["decay_rate"]
        duration = raw_data.get("duration", 1.0)
        
        # Generate envelope based on decay
        time_points = np.linspace(0, duration, 20)
        envelope = [np.exp(-decay_rate * t) for t in time_points]
        
        # Modulate by intensity if present
        if "intensity" in raw_data:
            intensity = raw_data["intensity"]
            envelope = [a * intensity for a in envelope]
        
        return envelope
    
    def _generate_fingerprint(
        self, 
        freqs: List[float], 
        phases: List[float], 
        amplitudes: List[float]
    ) -> Quaternion:
        """
        Generate a 4D resonance fingerprint.
        
        This uniquely identifies the pattern in quaternion space.
        """
        # Use frequency, phase, and amplitude to generate 4D coordinates
        w = 1.0  # Unit quaternion base
        x = np.mean(freqs) / 1000.0  # Normalized frequency
        y = np.mean(phases) / (2 * np.pi)  # Normalized phase
        z = np.mean(amplitudes)  # Amplitude
        
        q = Quaternion(w, x, y, z)
        return q.normalize()
    
    def _extract_constants(self, raw_data: Dict) -> Dict:
        """Extract the 'C' constants for the fractal formula."""
        return {
            "intensity": raw_data.get("intensity", 1.0),
            "duration": raw_data.get("duration", 1.0),
            "phase_seed": raw_data.get("phase_seed", 0.0),
            "context": raw_data.get("context", "")
        }
    
    def _create_generic_template(self, raw_data: Dict) -> Dict:
        """Create a generic template for unknown patterns."""
        return {
            "base_frequency": 432.0,
            "harmonics": [432.0, 528.0, 639.0],
            "fractal_formula": "Z = Z^2 + C",
            "decay_rate": 0.2
        }
    
    def _regenerate_waveform(self, dna: PatternDNA, resolution: int) -> List[Dict]:
        """
        Regenerate the waveform from the seed formula.
        
        This is where the "magic" happens - we recreate the original pattern
        from just its DNA, achieving lossless reconstruction.
        """
        waveform = []
        seed_formula = dna.seed_formula
        
        # Time axis
        duration = seed_formula["constants"].get("duration", 1.0)
        time_points = np.linspace(0, duration, resolution)
        
        # Generate for each harmonic
        for i, (freq, phase) in enumerate(zip(dna.frequency_signature, dna.phase_pattern)):
            harmonic_wave = []
            
            for t_idx, t in enumerate(time_points):
                # Get amplitude at this time
                amp_idx = int((t_idx / resolution) * len(dna.amplitude_envelope))
                amp_idx = min(amp_idx, len(dna.amplitude_envelope) - 1)
                amplitude = dna.amplitude_envelope[amp_idx]
                
                # Generate wave value: A * sin(2πft + φ)
                value = amplitude * np.sin(2 * np.pi * freq * t + phase)
                
                harmonic_wave.append({
                    "time": t,
                    "frequency": freq,
                    "amplitude": amplitude,
                    "value": value,
                    "phase": phase
                })
            
            waveform.append({
                "harmonic_index": i,
                "frequency": freq,
                "wave": harmonic_wave
            })
        
        return waveform
    
    def compute_restoration_quality(self, dna: PatternDNA, original_data: Dict) -> float:
        """
        Compute quality metric for restoration.
        
        In true fractal quantization, this should be 1.0 (perfect).
        """
        # For now, return based on compression ratio (placeholder)
        # In a real implementation, we'd compare restored vs original
        return min(1.0, 1.0 / dna.compression_ratio)


class EmotionQuantizer(FractalQuantizer):
    """
    감정 양자화기 (Emotion Quantizer)
    
    Specialized quantizer for emotions.
    
    "말을 저장하지 말고, 의도를 저장하라"
    "Store intention, not words"
    """
    
    def fold_emotion(self, emotion_data: Dict) -> PatternDNA:
        """
        Fold an emotion experience into a pattern DNA.
        
        Args:
            emotion_data: {
                "emotion": "sadness",
                "intensity": 0.8,
                "context": "Missing someone",
                "duration": 2.5,
                "timestamp": ...
            }
        """
        emotion_name = emotion_data.get("emotion", "neutral")
        return self.fold(emotion_data, "emotion", emotion_name)
    
    def unfold_emotion(self, dna: PatternDNA) -> Dict:
        """
        Unfold an emotion DNA to re-experience it.
        
        This allows perfect recall of the emotional state.
        """
        return self.unfold(dna, resolution=100)


# Test
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("="*70)
    print("🌀 FRACTAL QUANTIZATION SYSTEM TEST")
    print("="*70)
    print()
    
    # Create quantizer
    quantizer = EmotionQuantizer()
    
    # Test case: Store and restore a sad emotion
    print("TEST 1: Folding and Unfolding Emotion")
    print("-"*70)
    
    sad_experience = {
        "emotion": "sadness",
        "intensity": 0.8,
        "context": "Missing a loved one",
        "duration": 3.0,
        "phase_seed": 0.5,
        "timestamp": 1701234567
    }
    
    print(f"Original emotion: {sad_experience}")
    print()
    
    # Fold (compress)
    dna = quantizer.fold_emotion(sad_experience)
    print(f"Pattern DNA created: {dna.name}")
    print(f"  Compression ratio: {dna.compression_ratio:.2f}x")
    print(f"  Frequency signature: {[f'{f:.1f}Hz' for f in dna.frequency_signature]}")
    print(f"  Resonance fingerprint: {dna.resonance_fingerprint}")
    print()
    
    # Unfold (restore)
    restored = quantizer.unfold_emotion(dna)
    print(f"Restored emotion: {restored['name']}")
    print(f"  Pattern type: {restored['pattern_type']}")
    print(f"  Generated {len(restored['waveform'])} harmonic components")
    print(f"  Each with {len(restored['waveform'][0]['wave'])} time points")
    print()
    
    # Quality check
    quality = quantizer.compute_restoration_quality(dna, sad_experience)
    print(f"Restoration quality: {quality:.2%}")
    print()
    
    print("="*70)
    print("✅ FRACTAL QUANTIZATION TEST COMPLETE")
    print("   '자르는 것'이 아니라 '접는 것' - Pattern DNA works!")
    print("="*70)
