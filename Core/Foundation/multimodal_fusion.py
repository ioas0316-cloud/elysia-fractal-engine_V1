"""
Multimodal Fusion System

Fuses information from multiple modalities (vision, audio, haptic) to create
unified understanding and enable cross-modal reasoning.
"""

import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
import json
from pathlib import Path

from .vision_processor import ImageAnalysis, VisionProcessor
from .audio_processor import AudioAnalysis, AudioProcessor


class FusionStrategy(Enum):
    """Strategy for fusing multimodal information"""
    EARLY_FUSION = "early"  # Combine raw features
    LATE_FUSION = "late"  # Combine decisions
    HYBRID_FUSION = "hybrid"  # Combine both
    ATTENTION_FUSION = "attention"  # Attention-weighted


@dataclass
class ModalityContribution:
    """Contribution of each modality to final result"""
    modality: str
    confidence: float
    weight: float  # 0-1
    key_insights: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "modality": self.modality,
            "confidence": self.confidence,
            "weight": self.weight,
            "key_insights": self.key_insights
        }


@dataclass
class CrossModalCorrespondence:
    """Correspondence between modalities"""
    source_modality: str
    target_modality: str
    correspondence_type: str  # e.g., "temporal_sync", "semantic_match"
    strength: float  # 0-1
    description: str
    
    def to_dict(self) -> Dict:
        return {
            "source_modality": self.source_modality,
            "target_modality": self.target_modality,
            "correspondence_type": self.correspondence_type,
            "strength": self.strength,
            "description": self.description
        }


@dataclass
class FusionResult:
    """Result of multimodal fusion"""
    timestamp: float
    fusion_id: str
    modalities: List[str]
    strategy: FusionStrategy
    contributions: List[ModalityContribution]
    correspondences: List[CrossModalCorrespondence]
    unified_description: str
    unified_confidence: float
    processing_time: float
    insights: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            "timestamp": self.timestamp,
            "fusion_id": self.fusion_id,
            "modalities": self.modalities,
            "strategy": self.strategy.value,
            "contributions": [c.to_dict() for c in self.contributions],
            "correspondences": [c.to_dict() for c in self.correspondences],
            "unified_description": self.unified_description,
            "unified_confidence": self.unified_confidence,
            "processing_time": self.processing_time,
            "insights": self.insights
        }


class MultimodalFusion:
    """
    Multimodal fusion system for integrating vision, audio, and other modalities.
    
    Creates unified understanding by combining information from multiple sources.
    """
    
    def __init__(self, data_dir: str = "data/multimodal/fusion"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.vision_processor = VisionProcessor()
        self.audio_processor = AudioProcessor()
        
        self.fusion_cache: Dict[str, FusionResult] = {}
        self.processing_stats = {
            "total_fusions": 0,
            "total_time": 0.0,
            "avg_time": 0.0,
            "modality_combinations": {}
        }
    
    async def fuse_vision_audio(
        self,
        vision_analysis: Optional[ImageAnalysis] = None,
        audio_analysis: Optional[AudioAnalysis] = None,
        vision_data: Optional[Dict] = None,
        audio_data: Optional[Dict] = None,
        strategy: FusionStrategy = FusionStrategy.HYBRID_FUSION
    ) -> FusionResult:
        """
        Fuse vision and audio information.
        
        Args:
            vision_analysis: Pre-computed vision analysis
            audio_analysis: Pre-computed audio analysis
            vision_data: Raw vision data (if analysis not provided)
            audio_data: Raw audio data (if analysis not provided)
            strategy: Fusion strategy to use
            
        Returns:
            FusionResult with unified understanding
        """
        start_time = time.time()
        
        # Process modalities if needed
        if vision_analysis is None and vision_data is not None:
            vision_analysis = await self.vision_processor.analyze_image(vision_data)
        
        if audio_analysis is None and audio_data is not None:
            audio_analysis = await self.audio_processor.analyze_audio(audio_data)
        
        modalities = []
        if vision_analysis:
            modalities.append("vision")
        if audio_analysis:
            modalities.append("audio")
        
        fusion_id = f"fusion_{int(time.time() * 1000)}"
        
        # Analyze contributions
        contributions = await self._analyze_contributions(
            vision_analysis, audio_analysis
        )
        
        # Find correspondences
        correspondences = await self._find_correspondences(
            vision_analysis, audio_analysis
        )
        
        # Create unified description
        unified_description = await self._create_unified_description(
            vision_analysis, audio_analysis, correspondences
        )
        
        # Calculate unified confidence
        unified_confidence = self._calculate_unified_confidence(
            contributions, correspondences
        )
        
        # Extract insights
        insights = await self._extract_insights(
            vision_analysis, audio_analysis, correspondences
        )
        
        processing_time = time.time() - start_time
        
        result = FusionResult(
            timestamp=time.time(),
            fusion_id=fusion_id,
            modalities=modalities,
            strategy=strategy,
            contributions=contributions,
            correspondences=correspondences,
            unified_description=unified_description,
            unified_confidence=unified_confidence,
            processing_time=processing_time,
            insights=insights
        )
        
        # Update stats
        self.processing_stats["total_fusions"] += 1
        self.processing_stats["total_time"] += processing_time
        self.processing_stats["avg_time"] = (
            self.processing_stats["total_time"] / 
            self.processing_stats["total_fusions"]
        )
        
        combo_key = "+".join(sorted(modalities))
        self.processing_stats["modality_combinations"][combo_key] = (
            self.processing_stats["modality_combinations"].get(combo_key, 0) + 1
        )
        
        # Cache and save
        self.fusion_cache[fusion_id] = result
        await self._save_fusion(result)
        
        return result
    
    async def _analyze_contributions(
        self,
        vision_analysis: Optional[ImageAnalysis],
        audio_analysis: Optional[AudioAnalysis]
    ) -> List[ModalityContribution]:
        """Analyze contribution of each modality"""
        contributions = []
        
        if vision_analysis:
            insights = []
            if vision_analysis.objects:
                insights.append(f"{len(vision_analysis.objects)} objects detected")
            insights.append(f"Scene: {vision_analysis.scene.primary_scene}")
            
            contrib = ModalityContribution(
                modality="vision",
                confidence=vision_analysis.confidence,
                weight=0.5,
                key_insights=insights
            )
            contributions.append(contrib)
        
        if audio_analysis:
            insights = []
            insights.append(f"Audio type: {audio_analysis.primary_type.value}")
            insights.append(f"Emotion: {audio_analysis.emotion_tone.value}")
            if audio_analysis.temporal.tempo:
                insights.append(f"Tempo: {audio_analysis.temporal.tempo:.0f} BPM")
            
            contrib = ModalityContribution(
                modality="audio",
                confidence=audio_analysis.confidence,
                weight=0.5,
                key_insights=insights
            )
            contributions.append(contrib)
        
        # Normalize weights
        total_weight = sum(c.weight for c in contributions)
        if total_weight > 0:
            for contrib in contributions:
                contrib.weight /= total_weight
        
        return contributions
    
    async def _find_correspondences(
        self,
        vision_analysis: Optional[ImageAnalysis],
        audio_analysis: Optional[AudioAnalysis]
    ) -> List[CrossModalCorrespondence]:
        """Find correspondences between modalities"""
        correspondences = []
        
        if vision_analysis and audio_analysis:
            # Temporal synchronization
            if abs(vision_analysis.timestamp - audio_analysis.timestamp) < 1.0:
                correspondences.append(CrossModalCorrespondence(
                    source_modality="vision",
                    target_modality="audio",
                    correspondence_type="temporal_sync",
                    strength=0.9,
                    description="Vision and audio temporally synchronized"
                ))
            
            # Emotional consistency
            scene_mood = vision_analysis.scene.mood
            audio_emotion = audio_analysis.emotion_tone.value
            
            mood_emotion_match = {
                ("calm", "calm"): 0.95,
                ("energetic", "excited"): 0.9,
                ("calm", "happy"): 0.7,
                ("energetic", "happy"): 0.8
            }
            
            match_strength = mood_emotion_match.get((scene_mood, audio_emotion), 0.5)
            
            correspondences.append(CrossModalCorrespondence(
                source_modality="vision",
                target_modality="audio",
                correspondence_type="emotional_consistency",
                strength=match_strength,
                description=f"Visual mood '{scene_mood}' and audio emotion '{audio_emotion}'"
            ))
            
            # Activity level
            scene_complexity = vision_analysis.scene.complexity
            audio_energy = audio_analysis.temporal.energy
            
            if abs(scene_complexity - audio_energy) < 0.3:
                correspondences.append(CrossModalCorrespondence(
                    source_modality="vision",
                    target_modality="audio",
                    correspondence_type="activity_match",
                    strength=0.8,
                    description="Visual complexity matches audio energy"
                ))
        
        return correspondences
    
    async def _create_unified_description(
        self,
        vision_analysis: Optional[ImageAnalysis],
        audio_analysis: Optional[AudioAnalysis],
        correspondences: List[CrossModalCorrespondence]
    ) -> str:
        """Create unified description from all modalities"""
        parts = []
        
        if vision_analysis:
            scene = vision_analysis.scene
            parts.append(
                f"A {scene.mood} {scene.primary_scene} scene with {scene.lighting} lighting"
            )
            if vision_analysis.objects:
                obj_str = ", ".join(obj.label for obj in vision_analysis.objects[:3])
                parts.append(f"featuring {obj_str}")
        
        if audio_analysis:
            parts.append(
                f"accompanied by {audio_analysis.emotion_tone.value} {audio_analysis.primary_type.value}"
            )
            if audio_analysis.temporal.tempo:
                parts.append(f"at {audio_analysis.temporal.tempo:.0f} BPM")
        
        # Add correspondence insights
        strong_correspondences = [c for c in correspondences if c.strength > 0.7]
        if strong_correspondences:
            parts.append("with strong cross-modal consistency")
        
        return ". ".join(parts) + "."
    
    def _calculate_unified_confidence(
        self,
        contributions: List[ModalityContribution],
        correspondences: List[CrossModalCorrespondence]
    ) -> float:
        """Calculate unified confidence score"""
        if not contributions:
            return 0.0
        
        # Weighted average of modality confidences
        modality_conf = sum(
            c.confidence * c.weight for c in contributions
        )
        
        # Correspondence bonus
        if correspondences:
            avg_correspondence = sum(c.strength for c in correspondences) / len(correspondences)
            correspondence_bonus = avg_correspondence * 0.2
        else:
            correspondence_bonus = 0.0
        
        # Multi-modal bonus (having multiple modalities increases confidence)
        multi_modal_bonus = min(0.1, (len(contributions) - 1) * 0.1)
        
        unified = modality_conf + correspondence_bonus + multi_modal_bonus
        
        return min(1.0, max(0.0, unified))
    
    async def _extract_insights(
        self,
        vision_analysis: Optional[ImageAnalysis],
        audio_analysis: Optional[AudioAnalysis],
        correspondences: List[CrossModalCorrespondence]
    ) -> Dict:
        """Extract key insights from fusion"""
        insights = {
            "modality_alignment": "high" if any(c.strength > 0.8 for c in correspondences) else "moderate",
            "dominant_modality": None,
            "cross_modal_enhancements": []
        }
        
        # Determine dominant modality
        if vision_analysis and audio_analysis:
            if vision_analysis.confidence > audio_analysis.confidence:
                insights["dominant_modality"] = "vision"
            else:
                insights["dominant_modality"] = "audio"
        elif vision_analysis:
            insights["dominant_modality"] = "vision"
        elif audio_analysis:
            insights["dominant_modality"] = "audio"
        
        # Cross-modal enhancements
        for corr in correspondences:
            if corr.strength > 0.7:
                insights["cross_modal_enhancements"].append(
                    f"{corr.correspondence_type}: {corr.description}"
                )
        
        return insights
    
    async def _save_fusion(self, result: FusionResult):
        """Save fusion result to disk"""
        save_path = self.data_dir / f"{result.fusion_id}_fusion.json"
        
        with open(save_path, 'w') as f:
            json.dump(result.to_dict(), f, indent=2)
    
    def get_stats(self) -> Dict:
        """Get processing statistics"""
        return self.processing_stats.copy()
    
    def clear_cache(self):
        """Clear fusion cache"""
        self.fusion_cache.clear()
