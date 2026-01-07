"""
Multimodal Integration Module

Complete multimodal integration with vision, audio, and haptic processing.
Phase 8 of the Elysia roadmap.
"""

from .vision_processor import (
    VisionProcessor, 
    ImageAnalysis, 
    ObjectCategory,
    DetectedObject,
    BoundingBox,
    SceneDescription,
    VisualFeatures
)
from .audio_processor import (
    AudioProcessor, 
    AudioAnalysis,
    AudioType,
    EmotionTone,
    AudioSegment,
    SpectralFeatures,
    TemporalFeatures
)
from .multimodal_fusion import (
    MultimodalFusion, 
    FusionResult, 
    FusionStrategy,
    ModalityContribution,
    CrossModalCorrespondence
)

__all__ = [
    # Vision
    "VisionProcessor",
    "ImageAnalysis",
    "ObjectCategory",
    "DetectedObject",
    "BoundingBox",
    "SceneDescription",
    "VisualFeatures",
    # Audio
    "AudioProcessor",
    "AudioAnalysis",
    "AudioType",
    "EmotionTone",
    "AudioSegment",
    "SpectralFeatures",
    "TemporalFeatures",
    # Fusion
    "MultimodalFusion",
    "FusionResult",
    "FusionStrategy",
    "ModalityContribution",
    "CrossModalCorrespondence",
]
