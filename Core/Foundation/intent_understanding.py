"""
Intent Understanding System

Provides deep intent analysis including explicit, implicit, emotional, and contextual understanding.
"""

import time
import json
from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path


class IntentLevel(Enum):
    """Levels of intent detection"""
    EXPLICIT = "explicit"  # Directly stated intent
    IMPLICIT = "implicit"  # Inferred from context
    EMOTIONAL = "emotional"  # Based on emotional state
    CONTEXTUAL = "contextual"  # Based on broader context


class IntentCategory(Enum):
    """Categories of user intent"""
    INFORMATION_SEEKING = "information_seeking"
    TASK_EXECUTION = "task_execution"
    EMOTIONAL_SUPPORT = "emotional_support"
    CREATIVE_COLLABORATION = "creative_collaboration"
    PROBLEM_SOLVING = "problem_solving"
    LEARNING = "learning"
    SOCIAL_INTERACTION = "social_interaction"
    SYSTEM_CONTROL = "system_control"


@dataclass
class Intent:
    """Detected intent with confidence and evidence"""
    level: IntentLevel
    category: IntentCategory
    confidence: float
    description: str
    evidence: List[str]
    timestamp: float


@dataclass
class IntentAnalysis:
    """Complete intent analysis result"""
    primary_intent: Intent
    secondary_intents: List[Intent]
    implicit_needs: List[str]
    emotional_context: Dict[str, Any]
    recommended_response_style: str
    confidence_score: float


class IntentUnderstander:
    """
    Deep Intent Understanding System
    
    Analyzes user input at multiple levels to understand not just what is said,
    but what is meant, needed, and felt.
    """
    
    def __init__(self):
        self.intent_history: List[IntentAnalysis] = []
        self.user_patterns: Dict[str, Any] = {}
        self.context_window: List[Dict[str, Any]] = []
        self.data_dir = Path("data/social/intent")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
    async def analyze_intent(
        self,
        user_input: str,
        context: Optional[Dict[str, Any]] = None,
        history: Optional[List[str]] = None
    ) -> IntentAnalysis:
        """
        Analyze user intent at multiple levels
        
        Args:
            user_input: The user's input text
            context: Current context information
            history: Previous interaction history
            
        Returns:
            Complete intent analysis
        """
        context = context or {}
        history = history or []
        
        # Update context window
        self.context_window.append({
            "input": user_input,
            "context": context,
            "timestamp": time.time()
        })
        if len(self.context_window) > 10:
            self.context_window.pop(0)
        
        # Detect intents at different levels
        explicit_intent = self._detect_explicit_intent(user_input)
        implicit_intents = self._detect_implicit_intents(user_input, context)
        emotional_intent = self._detect_emotional_intent(user_input)
        contextual_intent = self._detect_contextual_intent(user_input, history)
        
        # Determine primary intent
        all_intents = [explicit_intent] + implicit_intents + [emotional_intent, contextual_intent]
        all_intents = [i for i in all_intents if i is not None]
        all_intents.sort(key=lambda x: x.confidence, reverse=True)
        
        primary_intent = all_intents[0] if all_intents else self._create_default_intent()
        secondary_intents = all_intents[1:4]  # Top 3 secondary intents
        
        # Extract implicit needs
        implicit_needs = self._extract_implicit_needs(user_input, context, all_intents)
        
        # Analyze emotional context
        emotional_context = self._analyze_emotional_context(user_input)
        
        # Recommend response style
        response_style = self._recommend_response_style(primary_intent, emotional_context)
        
        # Calculate overall confidence
        confidence_score = self._calculate_confidence(all_intents)
        
        analysis = IntentAnalysis(
            primary_intent=primary_intent,
            secondary_intents=secondary_intents,
            implicit_needs=implicit_needs,
            emotional_context=emotional_context,
            recommended_response_style=response_style,
            confidence_score=confidence_score
        )
        
        # Store analysis
        self.intent_history.append(analysis)
        self._save_analysis(analysis, user_input)
        
        return analysis
    
    def _detect_explicit_intent(self, user_input: str) -> Optional[Intent]:
        """Detect explicitly stated intent"""
        lower_input = user_input.lower()
        
        # Keywords for different intent categories
        keywords_map = {
            IntentCategory.INFORMATION_SEEKING: ["what", "how", "why", "explain", "tell me", "show me"],
            IntentCategory.TASK_EXECUTION: ["do", "execute", "run", "perform", "create", "make"],
            IntentCategory.EMOTIONAL_SUPPORT: ["feel", "feeling", "sad", "happy", "frustrated", "stuck"],
            IntentCategory.PROBLEM_SOLVING: ["problem", "issue", "solve", "fix", "help with"],
            IntentCategory.LEARNING: ["learn", "teach", "understand", "study"],
            IntentCategory.SYSTEM_CONTROL: ["start", "stop", "configure", "settings"],
        }
        
        for category, keywords in keywords_map.items():
            matches = [kw for kw in keywords if kw in lower_input]
            if matches:
                return Intent(
                    level=IntentLevel.EXPLICIT,
                    category=category,
                    confidence=min(0.9, 0.6 + len(matches) * 0.1),
                    description=f"Explicitly stated {category.value}",
                    evidence=matches,
                    timestamp=time.time()
                )
        
        return None
    
    def _detect_implicit_intents(self, user_input: str, context: Dict[str, Any]) -> List[Intent]:
        """Detect implied intents from context and phrasing"""
        implicit_intents = []
        lower_input = user_input.lower()
        
        # Check for frustration indicators (implicit emotional support need)
        frustration_indicators = ["can't", "won't", "doesn't work", "tried everything", "giving up"]
        if any(ind in lower_input for ind in frustration_indicators):
            implicit_intents.append(Intent(
                level=IntentLevel.IMPLICIT,
                category=IntentCategory.EMOTIONAL_SUPPORT,
                confidence=0.75,
                description="Implied need for emotional support and encouragement",
                evidence=[ind for ind in frustration_indicators if ind in lower_input],
                timestamp=time.time()
            ))
        
        # Check for learning intent (questions about "best way", "should I")
        learning_patterns = ["best way", "should i", "is it better", "recommend"]
        if any(pat in lower_input for pat in learning_patterns):
            implicit_intents.append(Intent(
                level=IntentLevel.IMPLICIT,
                category=IntentCategory.LEARNING,
                confidence=0.70,
                description="Implied desire to learn best practices",
                evidence=[pat for pat in learning_patterns if pat in lower_input],
                timestamp=time.time()
            ))
        
        # Context-based implicit intents
        if context.get("previous_errors"):
            implicit_intents.append(Intent(
                level=IntentLevel.IMPLICIT,
                category=IntentCategory.PROBLEM_SOLVING,
                confidence=0.80,
                description="Implicit problem-solving need based on previous errors",
                evidence=["previous_errors_in_context"],
                timestamp=time.time()
            ))
        
        return implicit_intents
    
    def _detect_emotional_intent(self, user_input: str) -> Optional[Intent]:
        """Detect intent based on emotional tone"""
        lower_input = user_input.lower()
        
        # Emotional indicators
        negative_emotions = ["frustrated", "confused", "stuck", "lost", "overwhelmed"]
        positive_emotions = ["excited", "happy", "great", "awesome", "love"]
        
        negative_count = sum(1 for em in negative_emotions if em in lower_input)
        positive_count = sum(1 for em in positive_emotions if em in lower_input)
        
        if negative_count > 0:
            return Intent(
                level=IntentLevel.EMOTIONAL,
                category=IntentCategory.EMOTIONAL_SUPPORT,
                confidence=0.65 + negative_count * 0.1,
                description="Negative emotional tone detected, may need support",
                evidence=[em for em in negative_emotions if em in lower_input],
                timestamp=time.time()
            )
        elif positive_count > 0:
            return Intent(
                level=IntentLevel.EMOTIONAL,
                category=IntentCategory.SOCIAL_INTERACTION,
                confidence=0.60 + positive_count * 0.1,
                description="Positive emotional tone detected, celebration opportunity",
                evidence=[em for em in positive_emotions if em in lower_input],
                timestamp=time.time()
            )
        
        return None
    
    def _detect_contextual_intent(self, user_input: str, history: List[str]) -> Optional[Intent]:
        """Detect intent based on conversation history and patterns"""
        if not history:
            return None
        
        # Check if user is following up on previous topic
        if len(history) > 0:
            last_exchange = history[-1].lower() if history else ""
            current_lower = user_input.lower()
            
            # Follow-up patterns
            followup_indicators = ["also", "and", "but", "however", "what about", "additionally"]
            if any(ind in current_lower for ind in followup_indicators):
                return Intent(
                    level=IntentLevel.CONTEXTUAL,
                    category=IntentCategory.INFORMATION_SEEKING,
                    confidence=0.70,
                    description="Contextual follow-up question on previous topic",
                    evidence=["conversation_continuity"],
                    timestamp=time.time()
                )
        
        return None
    
    def _extract_implicit_needs(
        self,
        user_input: str,
        context: Dict[str, Any],
        intents: List[Intent]
    ) -> List[str]:
        """Extract implicit needs from analysis"""
        needs = []
        lower_input = user_input.lower()
        
        # Based on detected intents
        for intent in intents:
            if intent.category == IntentCategory.EMOTIONAL_SUPPORT:
                needs.append("encouragement")
                needs.append("reassurance")
            elif intent.category == IntentCategory.PROBLEM_SOLVING:
                needs.append("step-by-step guidance")
                needs.append("examples")
            elif intent.category == IntentCategory.LEARNING:
                needs.append("clear explanations")
                needs.append("practice opportunities")
        
        # Based on specific phrases
        if "i don't understand" in lower_input or "confused" in lower_input:
            needs.append("simpler explanation")
        
        if "example" in lower_input or "show me" in lower_input:
            needs.append("concrete examples")
        
        # Remove duplicates while preserving order
        seen = set()
        unique_needs = []
        for need in needs:
            if need not in seen:
                seen.add(need)
                unique_needs.append(need)
        
        return unique_needs[:5]  # Top 5 needs
    
    def _analyze_emotional_context(self, user_input: str) -> Dict[str, Any]:
        """Analyze emotional context of the input"""
        lower_input = user_input.lower()
        
        # Emotion indicators
        emotions = {
            "frustration": ["frustrated", "annoying", "can't", "won't work"],
            "confusion": ["confused", "don't understand", "unclear"],
            "excitement": ["excited", "great", "awesome", "love"],
            "uncertainty": ["maybe", "not sure", "don't know", "think"],
            "urgency": ["urgent", "asap", "quickly", "now", "hurry"]
        }
        
        detected_emotions = {}
        for emotion, indicators in emotions.items():
            score = sum(1 for ind in indicators if ind in lower_input)
            if score > 0:
                detected_emotions[emotion] = min(1.0, score * 0.3)
        
        # Overall tone
        positive_words = ["good", "great", "thanks", "appreciate", "helpful"]
        negative_words = ["bad", "wrong", "issue", "problem", "error"]
        
        positive_score = sum(1 for w in positive_words if w in lower_input)
        negative_score = sum(1 for w in negative_words if w in lower_input)
        
        if positive_score > negative_score:
            tone = "positive"
        elif negative_score > positive_score:
            tone = "negative"
        else:
            tone = "neutral"
        
        return {
            "detected_emotions": detected_emotions,
            "overall_tone": tone,
            "intensity": max(positive_score, negative_score) * 0.2
        }
    
    def _recommend_response_style(self, primary_intent: Intent, emotional_context: Dict[str, Any]) -> str:
        """Recommend appropriate response style"""
        tone = emotional_context.get("overall_tone", "neutral")
        emotions = emotional_context.get("detected_emotions", {})
        
        if primary_intent.category == IntentCategory.EMOTIONAL_SUPPORT:
            return "empathetic_supportive"
        elif "frustration" in emotions and emotions["frustration"] > 0.5:
            return "patient_reassuring"
        elif "excitement" in emotions:
            return "enthusiastic_encouraging"
        elif primary_intent.category == IntentCategory.LEARNING:
            return "educational_clear"
        elif primary_intent.category == IntentCategory.TASK_EXECUTION:
            return "direct_actionable"
        elif tone == "negative":
            return "gentle_helpful"
        else:
            return "friendly_professional"
    
    def _calculate_confidence(self, intents: List[Intent]) -> float:
        """Calculate overall confidence score"""
        if not intents:
            return 0.5
        
        # Weight by intent level
        weights = {
            IntentLevel.EXPLICIT: 1.0,
            IntentLevel.IMPLICIT: 0.7,
            IntentLevel.EMOTIONAL: 0.6,
            IntentLevel.CONTEXTUAL: 0.5
        }
        
        weighted_confidences = [
            intent.confidence * weights.get(intent.level, 0.5)
            for intent in intents
        ]
        
        return sum(weighted_confidences) / len(weighted_confidences) if weighted_confidences else 0.5
    
    def _create_default_intent(self) -> Intent:
        """Create default intent when nothing is detected"""
        return Intent(
            level=IntentLevel.EXPLICIT,
            category=IntentCategory.INFORMATION_SEEKING,
            confidence=0.5,
            description="General information request",
            evidence=[],
            timestamp=time.time()
        )
    
    def _save_analysis(self, analysis: IntentAnalysis, user_input: str):
        """Save analysis to disk"""
        timestamp = int(time.time() * 1000)
        filename = self.data_dir / f"intent_{timestamp}_analysis.json"
        
        data = {
            "user_input": user_input,
            "analysis": {
                "primary_intent": {
                    "level": analysis.primary_intent.level.value,
                    "category": analysis.primary_intent.category.value,
                    "confidence": analysis.primary_intent.confidence,
                    "description": analysis.primary_intent.description,
                    "evidence": analysis.primary_intent.evidence
                },
                "secondary_intents": [
                    {
                        "level": intent.level.value,
                        "category": intent.category.value,
                        "confidence": intent.confidence,
                        "description": intent.description
                    }
                    for intent in analysis.secondary_intents
                ],
                "implicit_needs": analysis.implicit_needs,
                "emotional_context": analysis.emotional_context,
                "recommended_response_style": analysis.recommended_response_style,
                "confidence_score": analysis.confidence_score
            },
            "timestamp": time.time()
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_intent_patterns(self) -> Dict[str, Any]:
        """Get patterns from intent history"""
        if not self.intent_history:
            return {}
        
        # Category frequency
        category_counts = {}
        for analysis in self.intent_history:
            category = analysis.primary_intent.category.value
            category_counts[category] = category_counts.get(category, 0) + 1
        
        # Most common emotional contexts
        emotional_patterns = {}
        for analysis in self.intent_history:
            for emotion in analysis.emotional_context.get("detected_emotions", {}):
                emotional_patterns[emotion] = emotional_patterns.get(emotion, 0) + 1
        
        return {
            "total_interactions": len(self.intent_history),
            "category_distribution": category_counts,
            "emotional_patterns": emotional_patterns,
            "avg_confidence": sum(a.confidence_score for a in self.intent_history) / len(self.intent_history)
        }
