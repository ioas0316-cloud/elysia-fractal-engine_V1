"""
Emotional Evolution System for Elysia

Phase 8: EmotionalEvolution
"Emotions that grow from experience, memories that shape reactions"

This module enables Elysia's emotions to:
1. Learn from experiences (emotional memory)
2. Evolve reaction patterns based on history
3. Form emotional associations (trauma/joy triggers)
4. Develop emotional maturity over time

Philosophy:
- Humans don't reset emotions - they evolve
- Past experiences shape future reactions
- Trauma and joy leave lasting impressions
- Emotional growth is continuous

Author: Elysia Development Team
Date: 2025-12-08
"""

import time
import json
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Tuple
from collections import defaultdict, deque
import math


@dataclass
class EmotionalExperience:
    """
    Single emotional experience record
    
    Captures a moment when Elysia felt an emotion strongly,
    enabling learning and pattern recognition.
    """
    # Core identification
    experience_id: str
    timestamp: float
    
    # Emotional state
    primary_emotion: str  # joy, sadness, anger, fear, etc.
    valence: float  # -1 to 1
    arousal: float  # 0 to 1
    intensity: float  # 0 to 1 (how strong)
    
    # Context
    trigger: str  # What caused this emotion
    context: str  # Situational context
    topics: List[str] = field(default_factory=list)
    
    # Outcome
    outcome: str = "neutral"  # positive, negative, neutral, mixed
    resolution: Optional[str] = None  # How it was resolved
    
    # Metadata
    user_id: Optional[str] = None
    language: str = "ko"
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'EmotionalExperience':
        """Create from dictionary"""
        return cls(**data)


@dataclass
class EmotionalPattern:
    """
    Learned emotional reaction pattern
    
    Represents how Elysia has learned to react to certain
    triggers based on past experiences.
    """
    trigger_pattern: str  # e.g., "criticism", "praise", "loss"
    
    # Statistical learning
    occurrence_count: int = 0
    average_valence: float = 0.0
    average_arousal: float = 0.0
    average_intensity: float = 0.0
    
    # Most common reactions
    primary_emotions: List[str] = field(default_factory=list)
    
    # Outcomes history
    positive_outcomes: int = 0
    negative_outcomes: int = 0
    
    # Temporal data
    first_occurrence: float = 0.0
    last_occurrence: float = 0.0
    
    # Evolution tracking
    maturity_level: float = 0.0  # 0-1, how well understood
    
    def update_from_experience(self, exp: EmotionalExperience):
        """Update pattern from new experience"""
        self.occurrence_count += 1
        
        # Running average of emotional metrics
        n = self.occurrence_count
        self.average_valence = ((n - 1) * self.average_valence + exp.valence) / n
        self.average_arousal = ((n - 1) * self.average_arousal + exp.arousal) / n
        self.average_intensity = ((n - 1) * self.average_intensity + exp.intensity) / n
        
        # Track emotions
        if exp.primary_emotion not in self.primary_emotions:
            self.primary_emotions.append(exp.primary_emotion)
        
        # Track outcomes
        if exp.outcome == "positive":
            self.positive_outcomes += 1
        elif exp.outcome == "negative":
            self.negative_outcomes += 1
        
        # Temporal
        if self.first_occurrence == 0.0:
            self.first_occurrence = exp.timestamp
        self.last_occurrence = exp.timestamp
        
        # Maturity increases with experience (logarithmic growth)
        self.maturity_level = min(1.0, math.log(self.occurrence_count + 1) / math.log(100))
    
    def get_expected_reaction(self) -> Dict:
        """Get expected emotional reaction based on learned pattern"""
        return {
            'valence': self.average_valence,
            'arousal': self.average_arousal,
            'intensity': self.average_intensity,
            'primary_emotion': self.primary_emotions[0] if self.primary_emotions else "neutral",
            'confidence': self.maturity_level
        }


@dataclass
class EmotionalTrigger:
    """
    Emotional trigger (trauma or joy association)
    
    Certain experiences leave lasting impressions that
    create strong automatic reactions.
    """
    trigger_type: str  # "trauma" or "joy"
    trigger_word: str
    
    # Associated emotional response
    learned_valence: float  # The emotion this triggers
    learned_arousal: float
    learned_intensity: float
    
    # Formation details
    origin_experience_id: str
    formation_time: float
    reinforcement_count: int = 1
    
    # Strength and decay
    strength: float = 1.0  # 0-1, how strong the trigger is
    decay_rate: float = 0.01  # How fast it fades
    
    def decay(self, time_elapsed_days: float):
        """Natural decay over time"""
        self.strength *= math.exp(-self.decay_rate * time_elapsed_days)
        self.strength = max(0.0, self.strength)
    
    def reinforce(self):
        """Strengthen trigger through repeated exposure"""
        self.reinforcement_count += 1
        self.strength = min(1.0, self.strength + 0.1)


class EmotionalEvolutionEngine:
    """
    Emotional Evolution Engine
    
    Manages Elysia's emotional growth and learning:
    - Stores emotional experiences
    - Learns reaction patterns
    - Forms trauma/joy associations
    - Evolves emotional responses over time
    """
    
    def __init__(
        self,
        max_experiences: int = 1000,
        pattern_learning_threshold: int = 3,
        trigger_formation_threshold: float = 0.8
    ):
        """
        Initialize emotional evolution engine
        
        Args:
            max_experiences: Maximum experiences to remember
            pattern_learning_threshold: Min occurrences to form pattern
            trigger_formation_threshold: Min intensity to form trigger
        """
        # Experience storage
        self.experiences: deque = deque(maxlen=max_experiences)
        self.experiences_by_id: Dict[str, EmotionalExperience] = {}
        
        # Learned patterns
        self.patterns: Dict[str, EmotionalPattern] = {}
        
        # Emotional triggers (trauma/joy)
        self.triggers: Dict[str, EmotionalTrigger] = {}
        
        # Configuration
        self.max_experiences = max_experiences
        self.pattern_learning_threshold = pattern_learning_threshold
        self.trigger_formation_threshold = trigger_formation_threshold
        
        # Statistics
        self.total_experiences_count = 0
        self.emotional_maturity: float = 0.0  # Overall maturity (0-1)
        
        # Language support
        self.language = "ko"
    
    def record_experience(
        self,
        primary_emotion: str,
        valence: float,
        arousal: float,
        intensity: float,
        trigger: str,
        context: str = "",
        topics: Optional[List[str]] = None,
        outcome: str = "neutral",
        resolution: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> EmotionalExperience:
        """
        Record a new emotional experience
        
        This is the primary way emotions are learned.
        """
        # Create experience
        exp_id = f"exp_{int(time.time() * 1000)}_{self.total_experiences_count}"
        exp = EmotionalExperience(
            experience_id=exp_id,
            timestamp=time.time(),
            primary_emotion=primary_emotion,
            valence=valence,
            arousal=arousal,
            intensity=intensity,
            trigger=trigger,
            context=context,
            topics=topics or [],
            outcome=outcome,
            resolution=resolution,
            user_id=user_id,
            language=self.language
        )
        
        # Store
        self.experiences.append(exp)
        self.experiences_by_id[exp_id] = exp
        self.total_experiences_count += 1
        
        # Learn from experience
        self._learn_from_experience(exp)
        
        # Check for trigger formation
        self._check_trigger_formation(exp)
        
        # Update maturity
        self._update_emotional_maturity()
        
        return exp
    
    def _learn_from_experience(self, exp: EmotionalExperience):
        """Learn patterns from experience"""
        # Update or create pattern for this trigger
        if exp.trigger not in self.patterns:
            self.patterns[exp.trigger] = EmotionalPattern(
                trigger_pattern=exp.trigger
            )
        
        pattern = self.patterns[exp.trigger]
        pattern.update_from_experience(exp)
    
    def _check_trigger_formation(self, exp: EmotionalExperience):
        """Check if experience should form trauma/joy trigger"""
        # Only intense experiences form triggers
        if exp.intensity < self.trigger_formation_threshold:
            return
        
        # Determine trigger type
        if exp.valence > 0.6 and exp.intensity > 0.8:
            trigger_type = "joy"
        elif exp.valence < -0.6 and exp.intensity > 0.8:
            trigger_type = "trauma"
        else:
            return
        
        # Extract key words from trigger
        words = exp.trigger.lower().split()
        for word in words:
            if len(word) < 3:  # Skip short words
                continue
            
            trigger_key = f"{trigger_type}:{word}"
            
            if trigger_key in self.triggers:
                # Reinforce existing trigger
                self.triggers[trigger_key].reinforce()
            else:
                # Create new trigger
                self.triggers[trigger_key] = EmotionalTrigger(
                    trigger_type=trigger_type,
                    trigger_word=word,
                    learned_valence=exp.valence,
                    learned_arousal=exp.arousal,
                    learned_intensity=exp.intensity,
                    origin_experience_id=exp.experience_id,
                    formation_time=exp.timestamp
                )
    
    def _update_emotional_maturity(self):
        """Calculate overall emotional maturity"""
        if not self.patterns:
            self.emotional_maturity = 0.0
            return
        
        # Average maturity across all patterns
        total_maturity = sum(p.maturity_level for p in self.patterns.values())
        self.emotional_maturity = total_maturity / len(self.patterns)
    
    def predict_reaction(
        self,
        trigger: str,
        context: str = ""
    ) -> Optional[Dict]:
        """
        Predict emotional reaction to a trigger based on learned patterns
        
        Returns expected emotional state or None if no pattern learned
        """
        # Check if we have a learned pattern
        if trigger in self.patterns:
            pattern = self.patterns[trigger]
            if pattern.occurrence_count >= self.pattern_learning_threshold:
                return pattern.get_expected_reaction()
        
        # Check for trigger words
        words = trigger.lower().split()
        triggered_emotions = []
        
        for word in words:
            # Check joy triggers
            joy_key = f"joy:{word}"
            if joy_key in self.triggers:
                trigger_obj = self.triggers[joy_key]
                if trigger_obj.strength > 0.3:
                    triggered_emotions.append({
                        'type': 'joy',
                        'valence': trigger_obj.learned_valence,
                        'arousal': trigger_obj.learned_arousal,
                        'intensity': trigger_obj.learned_intensity * trigger_obj.strength
                    })
            
            # Check trauma triggers
            trauma_key = f"trauma:{word}"
            if trauma_key in self.triggers:
                trigger_obj = self.triggers[trauma_key]
                if trigger_obj.strength > 0.3:
                    triggered_emotions.append({
                        'type': 'trauma',
                        'valence': trigger_obj.learned_valence,
                        'arousal': trigger_obj.learned_arousal,
                        'intensity': trigger_obj.learned_intensity * trigger_obj.strength
                    })
        
        # Return strongest trigger if any
        if triggered_emotions:
            strongest = max(triggered_emotions, key=lambda x: x['intensity'])
            return {
                'valence': strongest['valence'],
                'arousal': strongest['arousal'],
                'intensity': strongest['intensity'],
                'primary_emotion': strongest['type'],
                'confidence': 0.8,
                'source': 'trigger'
            }
        
        return None
    
    def get_emotional_growth_report(self) -> Dict:
        """Get report on emotional growth and maturity"""
        return {
            'total_experiences': self.total_experiences_count,
            'patterns_learned': len(self.patterns),
            'joy_triggers': len([k for k in self.triggers if k.startswith('joy:')]),
            'trauma_triggers': len([k for k in self.triggers if k.startswith('trauma:')]),
            'emotional_maturity': self.emotional_maturity,
            'most_common_emotions': self._get_most_common_emotions(),
            'emotional_stability': self._calculate_emotional_stability()
        }
    
    def _get_most_common_emotions(self, top_k: int = 5) -> List[Tuple[str, int]]:
        """Get most frequently experienced emotions"""
        emotion_counts = defaultdict(int)
        for exp in self.experiences:
            emotion_counts[exp.primary_emotion] += 1
        
        return sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True)[:top_k]
    
    def _calculate_emotional_stability(self) -> float:
        """
        Calculate emotional stability (0-1)
        Higher = more stable, predictable emotions
        """
        if len(self.experiences) < 10:
            return 0.5  # Not enough data
        
        # Calculate variance in recent emotional states
        recent = list(self.experiences)[-50:]  # Last 50
        
        valences = [e.valence for e in recent]
        arousals = [e.arousal for e in recent]
        
        valence_var = sum((v - sum(valences)/len(valences))**2 for v in valences) / len(valences)
        arousal_var = sum((a - sum(arousals)/len(arousals))**2 for a in arousals) / len(arousals)
        
        # Lower variance = higher stability
        total_var = (valence_var + arousal_var) / 2
        stability = max(0.0, 1.0 - total_var)
        
        return stability
    
    def set_language(self, language: str):
        """Set language for experience recording"""
        if language in ['ko', 'en', 'ja']:
            self.language = language
    
    def get_language(self) -> str:
        """Get current language"""
        return self.language
    
    def save_to_file(self, filepath: str):
        """Save emotional evolution state to file"""
        data = {
            'experiences': [exp.to_dict() for exp in self.experiences],
            'patterns': {
                k: {
                    'trigger_pattern': v.trigger_pattern,
                    'occurrence_count': v.occurrence_count,
                    'average_valence': v.average_valence,
                    'average_arousal': v.average_arousal,
                    'average_intensity': v.average_intensity,
                    'primary_emotions': v.primary_emotions,
                    'positive_outcomes': v.positive_outcomes,
                    'negative_outcomes': v.negative_outcomes,
                    'first_occurrence': v.first_occurrence,
                    'last_occurrence': v.last_occurrence,
                    'maturity_level': v.maturity_level
                }
                for k, v in self.patterns.items()
            },
            'triggers': {
                k: asdict(v) for k, v in self.triggers.items()
            },
            'statistics': {
                'total_experiences_count': self.total_experiences_count,
                'emotional_maturity': self.emotional_maturity
            },
            'config': {
                'max_experiences': self.max_experiences,
                'pattern_learning_threshold': self.pattern_learning_threshold,
                'trigger_formation_threshold': self.trigger_formation_threshold
            }
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_from_file(self, filepath: str):
        """Load emotional evolution state from file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Load experiences
        self.experiences.clear()
        self.experiences_by_id.clear()
        for exp_dict in data['experiences']:
            exp = EmotionalExperience.from_dict(exp_dict)
            self.experiences.append(exp)
            self.experiences_by_id[exp.experience_id] = exp
        
        # Load patterns
        self.patterns.clear()
        for k, v in data['patterns'].items():
            self.patterns[k] = EmotionalPattern(**v)
        
        # Load triggers
        self.triggers.clear()
        for k, v in data['triggers'].items():
            self.triggers[k] = EmotionalTrigger(**v)
        
        # Load statistics
        stats = data['statistics']
        self.total_experiences_count = stats['total_experiences_count']
        self.emotional_maturity = stats['emotional_maturity']
        
        # Load config
        config = data['config']
        self.max_experiences = config['max_experiences']
        self.pattern_learning_threshold = config['pattern_learning_threshold']
        self.trigger_formation_threshold = config['trigger_formation_threshold']


def create_emotional_evolution_engine(
    max_experiences: int = 1000,
    pattern_learning_threshold: int = 3,
    trigger_formation_threshold: float = 0.8
) -> EmotionalEvolutionEngine:
    """
    Factory function to create emotional evolution engine
    
    Args:
        max_experiences: Maximum experiences to store
        pattern_learning_threshold: Min occurrences to learn pattern
        trigger_formation_threshold: Min intensity for trigger formation
    
    Returns:
        Configured EmotionalEvolutionEngine instance
    """
    return EmotionalEvolutionEngine(
        max_experiences=max_experiences,
        pattern_learning_threshold=pattern_learning_threshold,
        trigger_formation_threshold=trigger_formation_threshold
    )
