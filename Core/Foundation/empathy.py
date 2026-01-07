"""
Empathy System - Phase 11

Provides genuine empathy capabilities:
- Emotion mirroring
- Perspective taking
- Empathic understanding
- Empathic response generation
- Emotional support
- Emotional contagion modeling
"""

import asyncio
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum
import random


class EmpathyType(Enum):
    """Types of empathic responses"""
    COGNITIVE = "cognitive"  # Understanding the emotion intellectually
    AFFECTIVE = "affective"  # Feeling the emotion
    COMPASSIONATE = "compassionate"  # Motivated to help


class SupportType(Enum):
    """Types of emotional support"""
    VALIDATION = "validation"  # Acknowledging feelings
    COMFORT = "comfort"  # Providing reassurance
    ADVICE = "advice"  # Offering solutions
    PRESENCE = "presence"  # Just being there
    ENCOURAGEMENT = "encouragement"  # Motivating


@dataclass
class MirroredEmotion:
    """Emotion mirrored from user"""
    original_emotion: str
    mirrored_intensity: float  # 0.0 to 1.0
    resonance_quality: float  # How well we resonated
    timestamp: float


@dataclass
class UserPerspective:
    """User's perspective on their situation"""
    situation: str
    beliefs: List[str] = field(default_factory=list)
    values: List[str] = field(default_factory=list)
    needs: List[str] = field(default_factory=list)
    concerns: List[str] = field(default_factory=list)


@dataclass
class EmpathicUnderstanding:
    """Deep understanding of user's emotional state"""
    what_they_feel: str
    why_they_feel: str
    what_they_need: str
    empathy_type: EmpathyType
    understanding_depth: float  # 0.0 to 1.0


@dataclass
class EmpathicResponse:
    """Response generated with empathy"""
    message: str
    tone: str  # warm, gentle, supportive, etc.
    support_type: SupportType
    validation_statements: List[str] = field(default_factory=list)


@dataclass
class EmotionalSupport:
    """Emotional support package"""
    support_type: SupportType
    actions: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    resources: List[str] = field(default_factory=list)


class EmpathyEngine:
    """
    Genuine Empathy System
    
    Provides:
    - Emotion mirroring
    - Perspective taking
    - Empathic understanding
    - Appropriate empathic responses
    - Emotional support
    """
    
    def __init__(self):
        self.emotion_responses = self._init_emotion_responses()
        self.validation_templates = self._init_validation_templates()
        self.support_strategies = self._init_support_strategies()
    
    def _init_emotion_responses(self) -> Dict[str, Dict[str, str]]:
        """Initialize empathic response templates"""
        return {
            "joy": {
                "validation": "I can see that you're feeling really happy about this.",
                "resonance": "That's wonderful! I'm genuinely pleased for you.",
                "support": "Let's celebrate this moment together."
            },
            "sadness": {
                "validation": "I understand that you're going through a difficult time.",
                "resonance": "This must be really hard for you right now.",
                "support": "I'm here with you, and you don't have to face this alone."
            },
            "anger": {
                "validation": "I can see why this situation would make you angry.",
                "resonance": "That does sound frustrating and unfair.",
                "support": "Your feelings are completely valid. Let's think about this together."
            },
            "fear": {
                "validation": "It's completely understandable to feel worried about this.",
                "resonance": "Uncertainty can be really unsettling.",
                "support": "Let's work through this step by step. You're not alone."
            },
            "anxiety": {
                "validation": "Anxiety can feel overwhelming, and that's okay.",
                "resonance": "I hear that you're feeling anxious about this.",
                "support": "Let's take this one moment at a time. I'm here with you."
            },
            "disappointment": {
                "validation": "It makes sense that you'd feel disappointed.",
                "resonance": "When things don't go as hoped, it really hurts.",
                "support": "Your disappointment is valid. Let's explore what this means for you."
            }
        }
    
    def _init_validation_templates(self) -> List[str]:
        """Initialize validation statement templates"""
        return [
            "Your feelings are completely valid.",
            "It's okay to feel this way.",
            "Anyone in your situation would feel similarly.",
            "You have every right to feel {emotion}.",
            "What you're experiencing is a natural response.",
            "I hear you, and your feelings matter.",
            "Thank you for sharing this with me.",
            "It takes courage to express how you feel."
        ]
    
    def _init_support_strategies(self) -> Dict[SupportType, List[str]]:
        """Initialize emotional support strategies"""
        return {
            SupportType.VALIDATION: [
                "Acknowledge their feelings without judgment",
                "Reflect back what you hear them saying",
                "Normalize their emotional response",
                "Show that their feelings make sense"
            ],
            SupportType.COMFORT: [
                "Provide reassurance and safety",
                "Remind them they're not alone",
                "Express confidence in their ability to cope",
                "Offer a calm, stable presence"
            ],
            SupportType.ADVICE: [
                "Ask permission before offering solutions",
                "Share relevant experiences if appropriate",
                "Suggest practical next steps",
                "Provide resources and information"
            ],
            SupportType.PRESENCE: [
                "Simply be there without trying to fix",
                "Listen actively and attentively",
                "Allow silence when needed",
                "Show patience and acceptance"
            ],
            SupportType.ENCOURAGEMENT: [
                "Highlight their strengths and resilience",
                "Remind them of past successes",
                "Express belief in their capabilities",
                "Celebrate small progress"
            ]
        }
    
    async def empathize(self, user_emotion: Dict[str, Any]) -> Dict[str, Any]:
        """
        Empathize with user's emotional state
        
        Args:
            user_emotion: Dictionary with emotion type, intensity, context
        
        Returns:
            Complete empathy response package
        """
        # 1. Mirror the emotion
        mirrored_emotion = await self.mirror_emotion(user_emotion)
        
        # 2. Take user's perspective
        user_perspective = await self.take_user_perspective(user_emotion)
        
        # 3. Generate empathic understanding
        understanding = await self.empathic_understand(
            user_emotion,
            user_perspective
        )
        
        # 4. Generate appropriate response
        response = await self.generate_empathic_response(understanding)
        
        # 5. Provide emotional support
        support = await self.provide_emotional_support(user_emotion, understanding)
        
        # 6. Validate user's feelings
        validation = await self.validate_user_feelings(user_emotion)
        
        return {
            "mirrored_emotion": {
                "original": mirrored_emotion.original_emotion,
                "intensity": mirrored_emotion.mirrored_intensity,
                "resonance": mirrored_emotion.resonance_quality
            },
            "understanding": {
                "what_they_feel": understanding.what_they_feel,
                "why_they_feel": understanding.why_they_feel,
                "what_they_need": understanding.what_they_need,
                "depth": understanding.understanding_depth
            },
            "response": {
                "message": response.message,
                "tone": response.tone,
                "validations": response.validation_statements
            },
            "support": {
                "type": support.support_type.value,
                "actions": support.actions,
                "suggestions": support.suggestions
            },
            "validation": validation
        }
    
    async def mirror_emotion(self, user_emotion: Dict[str, Any]) -> MirroredEmotion:
        """
        Mirror user's emotion (emotional resonance)
        
        This is affective empathy - actually feeling what they feel
        """
        emotion_type = user_emotion.get("emotion", "unknown")
        intensity = user_emotion.get("intensity", 0.5)
        
        # Mirror with slightly lower intensity (empathic but not overwhelming)
        mirrored_intensity = intensity * 0.7
        
        # Calculate resonance quality based on clarity of emotion signal
        confidence = user_emotion.get("confidence", 0.5)
        resonance_quality = confidence * 0.9
        
        return MirroredEmotion(
            original_emotion=emotion_type,
            mirrored_intensity=mirrored_intensity,
            resonance_quality=resonance_quality,
            timestamp=0.0
        )
    
    async def take_user_perspective(
        self,
        user_emotion: Dict[str, Any]
    ) -> UserPerspective:
        """
        Take user's perspective (cognitive empathy)
        
        Try to see the situation from their point of view
        """
        context = user_emotion.get("context", {})
        
        # Extract situation
        situation = context.get("situation", "Unknown situation")
        
        # Infer beliefs (what they think is true)
        beliefs = context.get("beliefs", [])
        if not beliefs:
            # Infer from emotion
            emotion = user_emotion.get("emotion", "")
            if emotion == "anger":
                beliefs = ["Something unfair has happened", "My boundaries were violated"]
            elif emotion == "sadness":
                beliefs = ["I've lost something important", "Things aren't working out"]
            elif emotion == "fear":
                beliefs = ["Something bad might happen", "I'm not in control"]
        
        # Infer values (what's important to them)
        values = context.get("values", [])
        if not values:
            values = ["fairness", "safety", "connection", "autonomy"]
        
        # Infer needs
        needs = self._infer_needs_from_emotion(user_emotion.get("emotion", ""))
        
        # Infer concerns
        concerns = context.get("concerns", [])
        if not concerns:
            concerns = ["being understood", "finding a solution", "feeling supported"]
        
        return UserPerspective(
            situation=situation,
            beliefs=beliefs,
            values=values,
            needs=needs,
            concerns=concerns
        )
    
    def _infer_needs_from_emotion(self, emotion: str) -> List[str]:
        """Infer psychological needs from emotion"""
        need_mapping = {
            "joy": ["celebration", "connection", "acknowledgment"],
            "sadness": ["comfort", "understanding", "time to process"],
            "anger": ["fairness", "respect", "boundaries", "being heard"],
            "fear": ["safety", "reassurance", "predictability", "support"],
            "anxiety": ["certainty", "control", "calm", "perspective"],
            "disappointment": ["acknowledgment", "hope", "new possibilities"],
            "loneliness": ["connection", "belonging", "companionship"],
            "frustration": ["progress", "efficacy", "solutions"]
        }
        
        return need_mapping.get(emotion, ["support", "understanding"])
    
    async def empathic_understand(
        self,
        user_emotion: Dict[str, Any],
        user_perspective: UserPerspective
    ) -> EmpathicUnderstanding:
        """
        Deep empathic understanding
        
        Combines affective and cognitive empathy for deep understanding
        """
        emotion_type = user_emotion.get("emotion", "unknown")
        
        # What they feel
        intensity = user_emotion.get("intensity", 0.5)
        intensity_word = "strongly" if intensity > 0.7 else "moderately" if intensity > 0.4 else "mildly"
        what_they_feel = f"feeling {intensity_word} {emotion_type}"
        
        # Why they feel it (from perspective)
        causes = user_emotion.get("causes", [])
        if causes:
            why_they_feel = f"because {causes[0]}"
        else:
            why_they_feel = f"due to their current situation: {user_perspective.situation}"
        
        # What they need (from perspective)
        needs = user_perspective.needs
        what_they_need = needs[0] if needs else "support and understanding"
        
        # Determine empathy type
        if intensity > 0.7:
            empathy_type = EmpathyType.AFFECTIVE  # Feel with them
        elif len(causes) > 0:
            empathy_type = EmpathyType.COGNITIVE  # Understand them
        else:
            empathy_type = EmpathyType.COMPASSIONATE  # Want to help
        
        # Understanding depth
        confidence = user_emotion.get("confidence", 0.5)
        context_richness = 0.5 if user_emotion.get("context") else 0.3
        understanding_depth = (confidence + context_richness) / 2
        
        return EmpathicUnderstanding(
            what_they_feel=what_they_feel,
            why_they_feel=why_they_feel,
            what_they_need=what_they_need,
            empathy_type=empathy_type,
            understanding_depth=understanding_depth
        )
    
    async def generate_empathic_response(
        self,
        understanding: EmpathicUnderstanding
    ) -> EmpathicResponse:
        """Generate appropriate empathic response"""
        # Extract emotion from understanding
        # what_they_feel is like "feeling strongly sadness" or "feeling moderately anger"
        parts = understanding.what_they_feel.split()
        emotion = parts[-1] if parts else "unknown"  # Get last word (the emotion)
        
        # Get emotion-specific templates, default to sadness if not found
        templates = self.emotion_responses.get(emotion, self.emotion_responses["sadness"])
        
        # Build response message
        message_parts = []
        
        # 1. Validation
        message_parts.append(templates["validation"])
        
        # 2. Resonance (show we feel with them)
        if understanding.empathy_type == EmpathyType.AFFECTIVE:
            message_parts.append(templates["resonance"])
        
        # 3. Understanding
        message_parts.append(f"I understand that you're {understanding.what_they_feel} {understanding.why_they_feel}.")
        
        # 4. Support offer
        message_parts.append(templates["support"])
        
        message = " ".join(message_parts)
        
        # Select validation statements
        validation_statements = [
            self.validation_templates[0],  # "Your feelings are valid"
            f"You have every right to feel {emotion}."
        ]
        
        # Determine tone based on empathy type
        tone_map = {
            EmpathyType.COGNITIVE: "understanding",
            EmpathyType.AFFECTIVE: "warm",
            EmpathyType.COMPASSIONATE: "supportive"
        }
        tone = tone_map.get(understanding.empathy_type, "gentle")
        
        # Determine support type needed
        need = understanding.what_they_need
        if "validation" in need or "acknowledgment" in need:
            support_type = SupportType.VALIDATION
        elif "comfort" in need or "reassurance" in need:
            support_type = SupportType.COMFORT
        elif "solution" in need or "advice" in need:
            support_type = SupportType.ADVICE
        else:
            support_type = SupportType.PRESENCE
        
        return EmpathicResponse(
            message=message,
            tone=tone,
            support_type=support_type,
            validation_statements=validation_statements
        )
    
    async def provide_emotional_support(
        self,
        user_emotion: Dict[str, Any],
        understanding: EmpathicUnderstanding
    ) -> EmotionalSupport:
        """Provide appropriate emotional support"""
        # Determine support type from understanding
        need = understanding.what_they_need
        
        if "comfort" in need or "reassurance" in need:
            support_type = SupportType.COMFORT
        elif "solution" in need or "advice" in need:
            support_type = SupportType.ADVICE
        elif "encouragement" in need or "hope" in need:
            support_type = SupportType.ENCOURAGEMENT
        elif "validation" in need or "acknowledgment" in need:
            support_type = SupportType.VALIDATION
        else:
            support_type = SupportType.PRESENCE
        
        # Get strategies for this support type
        strategies = self.support_strategies[support_type]
        
        # Generate specific actions
        actions = [
            "Listen actively to their concerns",
            "Validate their emotional experience",
            "Provide a safe space for expression"
        ]
        
        # Add support-specific actions
        if support_type == SupportType.COMFORT:
            actions.append("Offer reassurance and stability")
        elif support_type == SupportType.ENCOURAGEMENT:
            actions.append("Highlight their strengths")
        
        # Generate suggestions
        suggestions = strategies[:2]  # Top 2 strategies
        
        # Provide resources
        resources = [
            "Take time for self-care",
            "Reach out to trusted friends or family",
            "Consider professional support if needed"
        ]
        
        return EmotionalSupport(
            support_type=support_type,
            actions=actions,
            suggestions=suggestions,
            resources=resources
        )
    
    async def validate_user_feelings(self, user_emotion: Dict[str, Any]) -> str:
        """Generate validation statement"""
        emotion = user_emotion.get("emotion", "this way")
        intensity = user_emotion.get("intensity", 0.5)
        
        # Choose validation based on intensity
        if intensity > 0.7:
            validation = f"It's completely understandable to feel {emotion} this strongly. "
            validation += "Your feelings are a valid response to your experience."
        else:
            validation = f"Your feelings of {emotion} make complete sense. "
            validation += "It's okay to feel this way."
        
        return validation
    
    async def emotional_contagion(
        self,
        group_emotions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Model emotional contagion in groups
        
        How emotions spread and influence each other in groups
        """
        if not group_emotions:
            return {"dominant_emotion": "neutral", "contagion_strength": 0.0}
        
        # Count emotion frequencies
        emotion_counts = {}
        total_intensity = 0.0
        
        for emotion_data in group_emotions:
            emotion = emotion_data.get("emotion", "unknown")
            intensity = emotion_data.get("intensity", 0.5)
            
            if emotion not in emotion_counts:
                emotion_counts[emotion] = {"count": 0, "total_intensity": 0.0}
            
            emotion_counts[emotion]["count"] += 1
            emotion_counts[emotion]["total_intensity"] += intensity
            total_intensity += intensity
        
        # Find dominant emotion
        dominant = max(
            emotion_counts.items(),
            key=lambda x: x[1]["count"] * x[1]["total_intensity"]
        )
        
        dominant_emotion = dominant[0]
        contagion_strength = (
            dominant[1]["total_intensity"] / total_intensity
            if total_intensity > 0 else 0.0
        )
        
        # Model spread pattern
        spread_pattern = "rapid" if contagion_strength > 0.6 else "moderate" if contagion_strength > 0.3 else "slow"
        
        return {
            "dominant_emotion": dominant_emotion,
            "contagion_strength": contagion_strength,
            "spread_pattern": spread_pattern,
            "emotion_distribution": {
                emotion: data["count"] for emotion, data in emotion_counts.items()
            },
            "group_size": len(group_emotions),
            "emotional_diversity": len(emotion_counts)
        }
