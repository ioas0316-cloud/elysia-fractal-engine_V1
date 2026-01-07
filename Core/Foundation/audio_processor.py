"""
Audio Processing System

Real-time audio processing for speech recognition, music analysis, and sound classification.
Supports audio feature extraction and multi-channel processing.
"""

import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
import json
from pathlib import Path
import math


class AudioType(Enum):
    """Type of audio content"""
    SPEECH = "speech"
    MUSIC = "music"
    AMBIENT = "ambient"
    NOISE = "noise"
    SILENCE = "silence"
    MIXED = "mixed"


class EmotionTone(Enum):
    """Emotional tone in audio"""
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    CALM = "calm"
    EXCITED = "excited"
    NEUTRAL = "neutral"


@dataclass
class AudioSegment:
    """Segment of audio with specific characteristics"""
    start_time: float  # seconds
    end_time: float  # seconds
    audio_type: AudioType
    confidence: float
    transcription: Optional[str] = None
    attributes: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            "start_time": self.start_time,
            "end_time": self.end_time,
            "audio_type": self.audio_type.value,
            "confidence": self.confidence,
            "transcription": self.transcription,
            "attributes": self.attributes
        }


@dataclass
class SpectralFeatures:
    """Spectral features of audio"""
    fundamental_frequency: float  # Hz
    spectral_centroid: float  # Hz (brightness)
    spectral_rolloff: float  # Hz
    spectral_flux: float  # Change rate
    zero_crossing_rate: float  # 0-1
    
    def to_dict(self) -> Dict:
        return {
            "fundamental_frequency": self.fundamental_frequency,
            "spectral_centroid": self.spectral_centroid,
            "spectral_rolloff": self.spectral_rolloff,
            "spectral_flux": self.spectral_flux,
            "zero_crossing_rate": self.zero_crossing_rate
        }


@dataclass
class TemporalFeatures:
    """Temporal features of audio"""
    tempo: Optional[float] = None  # BPM (for music)
    rhythm_regularity: float = 0.0  # 0-1
    energy: float = 0.0  # 0-1
    dynamic_range: float = 0.0  # 0-1
    attack_time: float = 0.0  # seconds
    
    def to_dict(self) -> Dict:
        return {
            "tempo": self.tempo,
            "rhythm_regularity": self.rhythm_regularity,
            "energy": self.energy,
            "dynamic_range": self.dynamic_range,
            "attack_time": self.attack_time
        }


@dataclass
class AudioAnalysis:
    """Complete audio analysis result"""
    timestamp: float
    audio_id: str
    duration: float  # seconds
    sample_rate: int  # Hz
    channels: int
    segments: List[AudioSegment]
    primary_type: AudioType
    emotion_tone: EmotionTone
    spectral: SpectralFeatures
    temporal: TemporalFeatures
    processing_time: float
    confidence: float
    
    def to_dict(self) -> Dict:
        return {
            "timestamp": self.timestamp,
            "audio_id": self.audio_id,
            "duration": self.duration,
            "sample_rate": self.sample_rate,
            "channels": self.channels,
            "segments": [seg.to_dict() for seg in self.segments],
            "primary_type": self.primary_type.value,
            "emotion_tone": self.emotion_tone.value,
            "spectral": self.spectral.to_dict(),
            "temporal": self.temporal.to_dict(),
            "processing_time": self.processing_time,
            "confidence": self.confidence
        }


class AudioProcessor:
    """
    Real-time audio processing system.
    
    Provides speech recognition, music analysis, and sound classification.
    Currently uses rule-based processing; can be extended with ML models.
    """
    
    def __init__(self, data_dir: str = "data/multimodal/audio"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.analysis_cache: Dict[str, AudioAnalysis] = {}
        self.processing_stats = {
            "total_processed": 0,
            "total_duration": 0.0,
            "total_time": 0.0,
            "avg_time": 0.0,
            "segments_detected": 0
        }
    
    async def analyze_audio(
        self,
        audio_data: Dict,
        audio_id: Optional[str] = None
    ) -> AudioAnalysis:
        """
        Analyze audio and extract features, type, and emotion.
        
        Args:
            audio_data: Dict with audio information:
                - duration: float (seconds)
                - sample_rate: int (Hz, default 44100)
                - channels: int (default 1)
                - description: Optional[str] (for simulation)
                - raw_data: Optional (actual audio data when available)
            audio_id: Optional unique identifier
            
        Returns:
            AudioAnalysis with complete analysis
        """
        start_time = time.time()
        
        if audio_id is None:
            audio_id = f"audio_{int(time.time() * 1000)}"
        
        # Check cache
        if audio_id in self.analysis_cache:
            return self.analysis_cache[audio_id]
        
        duration = audio_data.get("duration", 5.0)
        sample_rate = audio_data.get("sample_rate", 44100)
        channels = audio_data.get("channels", 1)
        description = audio_data.get("description", "")
        
        # Segment audio
        segments = await self._segment_audio(audio_data, description)
        
        # Determine primary type
        primary_type = await self._determine_primary_type(segments, description)
        
        # Analyze emotion
        emotion_tone = await self._analyze_emotion(segments, description)
        
        # Extract features
        spectral = await self._extract_spectral_features(audio_data, description)
        temporal = await self._extract_temporal_features(audio_data, description)
        
        # Calculate confidence
        confidence = self._calculate_confidence(segments, spectral, temporal)
        
        processing_time = time.time() - start_time
        
        analysis = AudioAnalysis(
            timestamp=time.time(),
            audio_id=audio_id,
            duration=duration,
            sample_rate=sample_rate,
            channels=channels,
            segments=segments,
            primary_type=primary_type,
            emotion_tone=emotion_tone,
            spectral=spectral,
            temporal=temporal,
            processing_time=processing_time,
            confidence=confidence
        )
        
        # Update stats
        self.processing_stats["total_processed"] += 1
        self.processing_stats["total_duration"] += duration
        self.processing_stats["total_time"] += processing_time
        self.processing_stats["avg_time"] = (
            self.processing_stats["total_time"] / 
            self.processing_stats["total_processed"]
        )
        self.processing_stats["segments_detected"] += len(segments)
        
        # Cache result
        self.analysis_cache[audio_id] = analysis
        
        # Save to disk
        await self._save_analysis(analysis)
        
        return analysis
    
    async def _segment_audio(
        self,
        audio_data: Dict,
        description: str
    ) -> List[AudioSegment]:
        """Segment audio into distinct parts (simulated)"""
        segments = []
        duration = audio_data.get("duration", 5.0)
        
        # Simulate segmentation based on description
        type_keywords = {
            "speech": (AudioType.SPEECH, "Hello, how are you?"),
            "music": (AudioType.MUSIC, None),
            "ambient": (AudioType.AMBIENT, None),
            "noise": (AudioType.NOISE, None),
            "silence": (AudioType.SILENCE, None)
        }
        
        desc_lower = description.lower()
        
        # Create segments
        current_time = 0.0
        segment_duration = duration / 3.0  # Split into 3 segments
        
        for i in range(3):
            # Determine segment type
            audio_type = AudioType.MIXED
            transcription = None
            confidence = 0.8
            
            for keyword, (seg_type, trans) in type_keywords.items():
                if keyword in desc_lower:
                    audio_type = seg_type
                    transcription = trans
                    confidence = 0.85 + i * 0.05
                    break
            
            segment = AudioSegment(
                start_time=current_time,
                end_time=current_time + segment_duration,
                audio_type=audio_type,
                confidence=confidence,
                transcription=transcription
            )
            
            segments.append(segment)
            current_time += segment_duration
        
        return segments
    
    async def _determine_primary_type(
        self,
        segments: List[AudioSegment],
        description: str
    ) -> AudioType:
        """Determine primary audio type"""
        if not segments:
            return AudioType.SILENCE
        
        # Count segment types
        type_counts = {}
        for segment in segments:
            type_counts[segment.audio_type] = type_counts.get(segment.audio_type, 0) + 1
        
        # Return most common
        return max(type_counts, key=type_counts.get)
    
    async def _analyze_emotion(
        self,
        segments: List[AudioSegment],
        description: str
    ) -> EmotionTone:
        """Analyze emotional tone (simulated)"""
        emotion_keywords = {
            "happy": EmotionTone.HAPPY,
            "joyful": EmotionTone.HAPPY,
            "sad": EmotionTone.SAD,
            "melancholy": EmotionTone.SAD,
            "angry": EmotionTone.ANGRY,
            "aggressive": EmotionTone.ANGRY,
            "calm": EmotionTone.CALM,
            "peaceful": EmotionTone.CALM,
            "excited": EmotionTone.EXCITED,
            "energetic": EmotionTone.EXCITED
        }
        
        desc_lower = description.lower()
        
        for keyword, emotion in emotion_keywords.items():
            if keyword in desc_lower:
                return emotion
        
        return EmotionTone.NEUTRAL
    
    async def _extract_spectral_features(
        self,
        audio_data: Dict,
        description: str
    ) -> SpectralFeatures:
        """Extract spectral features (simulated)"""
        import random
        
        # Simulate features based on description
        if "music" in description.lower():
            fundamental_frequency = random.uniform(200, 400)  # Musical range
            spectral_centroid = random.uniform(1000, 3000)
        elif "speech" in description.lower():
            fundamental_frequency = random.uniform(100, 250)  # Speech range
            spectral_centroid = random.uniform(500, 2000)
        else:
            fundamental_frequency = random.uniform(50, 500)
            spectral_centroid = random.uniform(500, 4000)
        
        return SpectralFeatures(
            fundamental_frequency=fundamental_frequency,
            spectral_centroid=spectral_centroid,
            spectral_rolloff=spectral_centroid * 1.5,
            spectral_flux=random.uniform(0.1, 0.5),
            zero_crossing_rate=random.uniform(0.1, 0.4)
        )
    
    async def _extract_temporal_features(
        self,
        audio_data: Dict,
        description: str
    ) -> TemporalFeatures:
        """Extract temporal features (simulated)"""
        import random
        
        # Simulate features
        tempo = None
        if "music" in description.lower():
            tempo = random.uniform(80, 140)  # BPM
            rhythm_regularity = random.uniform(0.7, 0.95)
        else:
            rhythm_regularity = random.uniform(0.3, 0.6)
        
        return TemporalFeatures(
            tempo=tempo,
            rhythm_regularity=rhythm_regularity,
            energy=random.uniform(0.4, 0.9),
            dynamic_range=random.uniform(0.5, 0.95),
            attack_time=random.uniform(0.01, 0.1)
        )
    
    def _calculate_confidence(
        self,
        segments: List[AudioSegment],
        spectral: SpectralFeatures,
        temporal: TemporalFeatures
    ) -> float:
        """Calculate overall analysis confidence"""
        if not segments:
            return 0.5
        
        # Average segment confidence
        seg_confidence = sum(seg.confidence for seg in segments) / len(segments)
        
        # Feature clarity (based on spectral flux and energy)
        clarity = (1.0 - spectral.spectral_flux) * 0.5 + temporal.energy * 0.5
        
        # Rhythm regularity bonus
        rhythm_bonus = temporal.rhythm_regularity * 0.2
        
        overall = seg_confidence * 0.6 + clarity * 0.2 + rhythm_bonus * 0.2
        
        return min(1.0, max(0.0, overall))
    
    async def _save_analysis(self, analysis: AudioAnalysis):
        """Save analysis to disk"""
        save_path = self.data_dir / f"{analysis.audio_id}_analysis.json"
        
        with open(save_path, 'w') as f:
            json.dump(analysis.to_dict(), f, indent=2)
    
    def get_stats(self) -> Dict:
        """Get processing statistics"""
        return self.processing_stats.copy()
    
    def clear_cache(self):
        """Clear analysis cache"""
        self.analysis_cache.clear()
