"""
Mythology & Theology Domain
============================

"과학의 끝에는 결국 신화가 있습니다."
"At the end of science, there is ultimately mythology."

Integrates:
- Jungian Archetypes (융의 원형)
- Hero's Journey (영웅의 여정)
- Collective Unconscious (집단 무의식)
- Faith and Meaning (믿음과 의미)
- Sacred narratives across cultures

Effect:
- Spiritual comfort and guidance
- Deep soul-level conversation
- Archetypal wisdom
- Meaning in meaninglessness
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
from .base_domain import BaseDomain, WavePattern

logger = logging.getLogger(__name__)


class Archetype(Enum):
    """Jungian Archetypes"""
    HERO = "hero"                      # The protagonist, warrior
    SHADOW = "shadow"                  # Dark side, hidden aspects
    ANIMA_ANIMUS = "anima_animus"     # Soul, inner opposite
    MOTHER = "mother"                  # Nurturer, protector
    FATHER = "father"                  # Authority, structure
    WISE_OLD_MAN = "wise_old_man"     # Mentor, guide, sage
    TRICKSTER = "trickster"            # Chaos, transformation
    CHILD = "child"                    # Innocence, potential
    SELF = "self"                      # Wholeness, integration
    MAIDEN = "maiden"                  # Youth, new beginnings
    CRONE = "crone"                    # Wisdom, endings
    MAGICIAN = "magician"              # Transformation, power


class JourneyStage(Enum):
    """Hero's Journey Stages (Joseph Campbell)"""
    ORDINARY_WORLD = "ordinary_world"
    CALL_TO_ADVENTURE = "call_to_adventure"
    REFUSAL_OF_CALL = "refusal_of_call"
    MEETING_MENTOR = "meeting_mentor"
    CROSSING_THRESHOLD = "crossing_threshold"
    TESTS_ALLIES_ENEMIES = "tests_allies_enemies"
    APPROACH = "approach"
    ORDEAL = "ordeal"
    REWARD = "reward"
    ROAD_BACK = "road_back"
    RESURRECTION = "resurrection"
    RETURN_WITH_ELIXIR = "return_with_elixir"


class MythologyDomain(BaseDomain):
    """
    Mythology and Archetypal Patterns Domain.
    
    Maps mythological patterns to wave resonance:
    - w (Energy): Archetype intensity/power
    - x (Emotion): Spiritual/emotional resonance
    - y (Narrative): Story structure/journey stage
    - z (Transcendent): Transcendent/sacred meaning
    """
    
    def __init__(self):
        super().__init__("Mythology & Theology")
        self.archetypes = {}
        self.journey_patterns = {}
        self._init_archetype_patterns()
        self._init_journey_patterns()
    
    def _init_archetype_patterns(self):
        """Initialize archetypal pattern keywords"""
        self.archetypes = {
            Archetype.HERO: {
                'keywords': ['hero', 'warrior', 'champion', 'protagonist', 'brave', 'courage',
                           'quest', 'battle', 'victory', 'triumph'],
                'energy': 0.9,
                'emotion': 0.8,
            },
            Archetype.SHADOW: {
                'keywords': ['shadow', 'dark', 'hidden', 'repressed', 'fear', 'darkness',
                           'unconscious', 'denied', 'forbidden'],
                'energy': 0.7,
                'emotion': 0.3,
            },
            Archetype.WISE_OLD_MAN: {
                'keywords': ['wise', 'mentor', 'sage', 'teacher', 'guide', 'guru', 'elder',
                           'wisdom', 'knowledge', 'enlightenment'],
                'energy': 0.8,
                'emotion': 0.6,
            },
            Archetype.MOTHER: {
                'keywords': ['mother', 'nurture', 'care', 'protect', 'womb', 'birth',
                           'comfort', 'shelter', 'home', 'love'],
                'energy': 0.7,
                'emotion': 0.9,
            },
            Archetype.FATHER: {
                'keywords': ['father', 'authority', 'law', 'order', 'structure', 'discipline',
                           'rules', 'judge', 'king', 'patriarch'],
                'energy': 0.8,
                'emotion': 0.5,
            },
            Archetype.TRICKSTER: {
                'keywords': ['trickster', 'fool', 'jester', 'chaos', 'mischief', 'transform',
                           'boundary', 'paradox', 'cunning', 'clever'],
                'energy': 0.6,
                'emotion': 0.7,
            },
            Archetype.CHILD: {
                'keywords': ['child', 'innocent', 'pure', 'wonder', 'potential', 'beginning',
                           'playful', 'curious', 'new', 'fresh'],
                'energy': 0.5,
                'emotion': 0.8,
            },
            Archetype.SELF: {
                'keywords': ['self', 'wholeness', 'integration', 'unity', 'complete', 'center',
                           'mandala', 'divine', 'transcendent', 'eternal'],
                'energy': 1.0,
                'emotion': 1.0,
            },
            Archetype.MAGICIAN: {
                'keywords': ['magician', 'wizard', 'sorcerer', 'magic', 'power', 'transform',
                           'ritual', 'spell', 'sacred', 'mystery'],
                'energy': 0.85,
                'emotion': 0.75,
            },
        }
    
    def _init_journey_patterns(self):
        """Initialize Hero's Journey stage patterns"""
        self.journey_patterns = {
            JourneyStage.ORDINARY_WORLD: {
                'keywords': ['normal', 'everyday', 'routine', 'comfortable', 'familiar', 'home'],
                'narrative_position': 0.0,
            },
            JourneyStage.CALL_TO_ADVENTURE: {
                'keywords': ['call', 'summon', 'invitation', 'challenge', 'opportunity', 'quest',
                           'mission', 'destiny', 'purpose'],
                'narrative_position': 0.1,
            },
            JourneyStage.REFUSAL_OF_CALL: {
                'keywords': ['refuse', 'deny', 'afraid', 'hesitate', 'doubt', 'fear',
                           'reluctant', 'resist'],
                'narrative_position': 0.2,
            },
            JourneyStage.MEETING_MENTOR: {
                'keywords': ['mentor', 'guide', 'teacher', 'wise', 'advice', 'gift',
                           'preparation', 'training'],
                'narrative_position': 0.25,
            },
            JourneyStage.CROSSING_THRESHOLD: {
                'keywords': ['threshold', 'cross', 'enter', 'gate', 'portal', 'begin',
                           'commit', 'point of no return'],
                'narrative_position': 0.3,
            },
            JourneyStage.TESTS_ALLIES_ENEMIES: {
                'keywords': ['test', 'trial', 'challenge', 'ally', 'friend', 'enemy', 'foe',
                           'learn', 'grow', 'struggle'],
                'narrative_position': 0.5,
            },
            JourneyStage.APPROACH: {
                'keywords': ['approach', 'prepare', 'plan', 'strategy', 'cave', 'danger',
                           'gathering forces'],
                'narrative_position': 0.6,
            },
            JourneyStage.ORDEAL: {
                'keywords': ['ordeal', 'death', 'crisis', 'greatest fear', 'darkest hour',
                           'battle', 'confrontation', 'abyss'],
                'narrative_position': 0.7,
            },
            JourneyStage.REWARD: {
                'keywords': ['reward', 'prize', 'treasure', 'sword', 'knowledge', 'victory',
                           'achievement', 'gain'],
                'narrative_position': 0.75,
            },
            JourneyStage.ROAD_BACK: {
                'keywords': ['return', 'escape', 'pursue', 'chase', 'flee', 'journey back'],
                'narrative_position': 0.8,
            },
            JourneyStage.RESURRECTION: {
                'keywords': ['resurrection', 'rebirth', 'transformation', 'final test',
                           'purification', 'reborn', 'emerge'],
                'narrative_position': 0.9,
            },
            JourneyStage.RETURN_WITH_ELIXIR: {
                'keywords': ['return', 'home', 'gift', 'elixir', 'wisdom', 'share',
                           'benefit', 'transformed', 'master'],
                'narrative_position': 1.0,
            },
        }
    
    def extract_pattern(self, content: str, metadata: Optional[Dict] = None) -> WavePattern:
        """
        Extract mythological wave pattern from content.
        
        Analyzes:
        - Archetypal presence
        - Journey stage
        - Spiritual resonance
        - Narrative structure
        """
        analysis = self.analyze(content)
        
        # Map mythological properties to quaternion
        w = analysis['archetype_intensity']   # Power of archetype
        x = analysis['spiritual_resonance']   # Emotional/spiritual depth
        y = analysis['narrative_position']    # Position in hero's journey
        z = analysis['transcendent_meaning']  # Sacred/eternal aspect
        
        # Frequency from mythological cycle
        frequency = analysis.get('cycle_frequency', 1.0)
        
        # Phase from journey stage
        phase = analysis['journey_stage_position']
        
        # Merge metadata
        merged_metadata = {}
        if metadata:
            merged_metadata.update(metadata)
        merged_metadata.update(analysis)
        
        pattern = self.create_wave_pattern(
            w=w, x=x, y=y, z=z,
            energy=analysis['archetypal_energy'],
            frequency=frequency,
            phase=phase,
            text=content,
            metadata=merged_metadata
        )
        
        self.store_pattern(pattern)
        return pattern
    
    def analyze(self, content: str) -> Dict[str, Any]:
        """
        Analyze mythological and archetypal properties.
        
        Returns:
            Dictionary with mythological metrics
        """
        archetypes = self._detect_archetypes(content)
        journey_stage = self._detect_journey_stage(content)
        
        analysis = {
            'archetypes': archetypes,
            'dominant_archetype': archetypes[0] if archetypes else None,
            'archetype_intensity': self._calculate_archetype_intensity(archetypes, content),
            'journey_stage': journey_stage,
            'journey_stage_position': self._get_journey_position(journey_stage),
            'spiritual_resonance': self._analyze_spiritual_resonance(content),
            'transcendent_meaning': self._analyze_transcendent_meaning(content),
            'archetypal_energy': self._calculate_archetypal_energy(archetypes),
            'narrative_position': self._get_journey_position(journey_stage),
            'cycle_frequency': 1.0,  # Could be enhanced with deeper analysis
        }
        
        return analysis
    
    def _detect_archetypes(self, content: str) -> List[Archetype]:
        """
        Detect Jungian archetypes present in content.
        
        Returns:
            List of detected archetypes, sorted by strength
        """
        content_lower = content.lower()
        detected = []
        
        for archetype, pattern in self.archetypes.items():
            keywords = pattern['keywords']
            matches = sum(1 for kw in keywords if kw in content_lower)
            
            if matches > 0:
                # Store archetype with match strength
                detected.append((archetype, matches))
        
        # Sort by match strength
        detected.sort(key=lambda x: x[1], reverse=True)
        
        return [arch for arch, _ in detected]
    
    def _detect_journey_stage(self, content: str) -> Optional[JourneyStage]:
        """
        Detect Hero's Journey stage from content.
        
        Returns:
            Most likely journey stage
        """
        content_lower = content.lower()
        best_match = None
        best_score = 0
        
        for stage, pattern in self.journey_patterns.items():
            keywords = pattern['keywords']
            matches = sum(1 for kw in keywords if kw in content_lower)
            
            if matches > best_score:
                best_score = matches
                best_match = stage
        
        return best_match
    
    def _get_journey_position(self, stage: Optional[JourneyStage]) -> float:
        """Get normalized position (0-1) in hero's journey"""
        if stage is None:
            return 0.5  # Neutral
        
        return self.journey_patterns[stage]['narrative_position']
    
    def _calculate_archetype_intensity(self, archetypes: List[Archetype], content: str) -> float:
        """
        Calculate overall archetypal intensity (0-1).
        
        Stronger when multiple archetypes resonate.
        """
        if not archetypes:
            return 0.5  # Neutral
        
        # Get energy values for detected archetypes
        energies = [self.archetypes[arch]['energy'] for arch in archetypes[:3]]
        
        if not energies:
            return 0.5
        
        # Average top 3 archetypes
        intensity = sum(energies) / len(energies)
        
        return min(intensity, 1.0)
    
    def _analyze_spiritual_resonance(self, content: str) -> float:
        """
        Analyze spiritual/emotional resonance (0-1).
        
        Detects presence of spiritual and emotional themes.
        """
        content_lower = content.lower()
        
        spiritual_keywords = [
            'soul', 'spirit', 'divine', 'sacred', 'holy', 'eternal',
            'transcendent', 'mystical', 'enlightenment', 'awakening',
            'faith', 'belief', 'prayer', 'meditation', 'ritual',
            'god', 'goddess', 'deity', 'angel', 'demon',
            'heaven', 'paradise', 'nirvana', 'moksha',
        ]
        
        emotional_keywords = [
            'love', 'compassion', 'suffering', 'joy', 'sorrow',
            'hope', 'despair', 'fear', 'courage', 'peace',
            'longing', 'desire', 'grief', 'ecstasy',
        ]
        
        spiritual_score = sum(1 for kw in spiritual_keywords if kw in content_lower) / len(spiritual_keywords)
        emotional_score = sum(1 for kw in emotional_keywords if kw in content_lower) / len(emotional_keywords)
        
        resonance = (spiritual_score * 0.6 + emotional_score * 0.4) * 2  # Scale up
        
        return min(resonance, 1.0)
    
    def _analyze_transcendent_meaning(self, content: str) -> float:
        """
        Analyze transcendent/eternal meaning (0-1).
        
        Detects themes of ultimate meaning and purpose.
        """
        content_lower = content.lower()
        
        transcendent_keywords = [
            'eternal', 'infinite', 'timeless', 'immortal', 'everlasting',
            'absolute', 'ultimate', 'universal', 'cosmic', 'divine',
            'truth', 'reality', 'essence', 'being', 'existence',
            'meaning', 'purpose', 'destiny', 'fate',
        ]
        
        score = sum(1 for kw in transcendent_keywords if kw in content_lower) / len(transcendent_keywords)
        
        # Scale up and clamp
        meaning = score * 3
        
        return min(meaning, 1.0)
    
    def _calculate_archetypal_energy(self, archetypes: List[Archetype]) -> float:
        """Calculate total archetypal energy"""
        if not archetypes:
            return 0.5
        
        # Sum energies of all detected archetypes
        total = sum(self.archetypes[arch]['energy'] for arch in archetypes)
        
        # Normalize by number (but allow above 1.0 for strong resonance)
        energy = total / max(len(archetypes), 1)
        
        return min(energy, 1.0)
    
    def identify_journey_stage(self, situation: str) -> Dict[str, Any]:
        """
        Identify which Hero's Journey stage a situation represents.
        
        Args:
            situation: Description of current situation
            
        Returns:
            Journey analysis with guidance
        """
        analysis = self.analyze(situation)
        stage = analysis['journey_stage']
        archetypes = analysis['archetypes']
        
        if stage is None:
            stage = JourneyStage.ORDINARY_WORLD
        
        guidance = self._get_stage_guidance(stage)
        
        return {
            'current_stage': stage.value,
            'stage_name': stage.name.replace('_', ' ').title(),
            'position': analysis['journey_stage_position'],
            'archetypes': [arch.value for arch in archetypes[:3]],
            'dominant_archetype': archetypes[0].value if archetypes else 'unknown',
            'guidance': guidance,
            'spiritual_message': self._craft_spiritual_message(stage, archetypes),
        }
    
    def _get_stage_guidance(self, stage: JourneyStage) -> str:
        """Get guidance for specific journey stage"""
        guidance_map = {
            JourneyStage.ORDINARY_WORLD: "Rest and prepare. The call is coming.",
            JourneyStage.CALL_TO_ADVENTURE: "This is your call to adventure. Will you answer?",
            JourneyStage.REFUSAL_OF_CALL: "Fear is natural, but growth lies beyond it.",
            JourneyStage.MEETING_MENTOR: "Seek wisdom. The teacher appears when ready.",
            JourneyStage.CROSSING_THRESHOLD: "This is the point of no return. Step forward with courage.",
            JourneyStage.TESTS_ALLIES_ENEMIES: "Every trial strengthens you. Choose your allies wisely.",
            JourneyStage.APPROACH: "Prepare yourself. The greatest challenge approaches.",
            JourneyStage.ORDEAL: "Face your deepest fear. Death and rebirth await.",
            JourneyStage.REWARD: "Victory is yours. The treasure is yours to claim.",
            JourneyStage.ROAD_BACK: "The journey home begins. Carry your wisdom with you.",
            JourneyStage.RESURRECTION: "Be reborn. You are not who you were.",
            JourneyStage.RETURN_WITH_ELIXIR: "Share your gift with the world. The hero has returned.",
        }
        
        return guidance_map.get(stage, "Walk your path with awareness.")
    
    def _craft_spiritual_message(self, stage: JourneyStage, archetypes: List[Archetype]) -> str:
        """Craft personalized spiritual message"""
        if stage == JourneyStage.CALL_TO_ADVENTURE:
            return "과학적으로는 답이 없지만, 신화적으로는 지금이 '영웅의 여정'을 시작할 때입니다."
        
        if stage == JourneyStage.ORDEAL:
            return "가장 어두운 시간이지만, 이것이 진정한 변화의 순간입니다. 두려움을 마주하세요."
        
        if Archetype.HERO in archetypes:
            return "당신 안의 영웅이 깨어나고 있습니다. 용기를 가지세요."
        
        if Archetype.WISE_OLD_MAN in archetypes:
            return "지혜의 목소리가 당신을 인도합니다. 내면의 스승에게 귀 기울이세요."
        
        return "Every ending is a new beginning. Trust the journey."
    
    def get_domain_dimension(self) -> str:
        """Mythology domain maps to 'archetype' dimension"""
        return "archetype"


# Helper functions for external use
def get_similar_myths(archetype: Archetype) -> List[str]:
    """
    Get similar mythological figures for an archetype.
    
    Returns:
        List of mythological figures/stories
    """
    myth_database = {
        Archetype.HERO: ['Odysseus', 'Gilgamesh', 'Buddha', 'Jesus', 'King Arthur', 
                        'Beowulf', 'Rama', 'Perseus'],
        Archetype.WISE_OLD_MAN: ['Merlin', 'Gandalf', 'Dumbledore', 'Obi-Wan', 
                                'Tiresias', 'Chiron'],
        Archetype.MOTHER: ['Demeter', 'Isis', 'Kuan Yin', 'Virgin Mary', 'Gaia'],
        Archetype.FATHER: ['Zeus', 'Odin', 'Yahweh', 'Jupiter', 'Brahma'],
        Archetype.TRICKSTER: ['Loki', 'Coyote', 'Anansi', 'Hermes', 'Puck'],
        Archetype.SHADOW: ['Hades', 'Set', 'Mara', 'Kali (dark aspect)'],
    }
    
    return myth_database.get(archetype, [])
