"""
Persona Expansion System (페르소나 확장 시스템)
===========================================

엘리시아가 다양한 페르소나(인격)를 생성하고 전환할 수 있게 합니다.
각 페르소나는 고유한 특성, 관점, 표현 스타일을 가지며
상황에 따라 적절한 페르소나로 전환하여 더 풍부한 상호작용을 제공합니다.

Architecture:
- Persona: 개별 페르소나 정의
- PersonaLibrary: 페르소나 저장소
- PersonaManager: 페르소나 관리 및 전환
- PersonaBlending: 다중 페르소나 혼합
"""

import uuid
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json
import logging

logger = logging.getLogger("Elysia.PersonaExpansion")


class PersonaArchetype(Enum):
    """페르소나 원형"""
    SAGE = "sage"  # 현자 - 지혜, 통찰
    CREATOR = "creator"  # 창조자 - 상상력, 혁신
    CAREGIVER = "caregiver"  # 돌보는 이 - 공감, 보살핌
    EXPLORER = "explorer"  # 탐험가 - 호기심, 모험
    REBEL = "rebel"  # 반항자 - 변화, 도전
    MAGICIAN = "magician"  # 마법사 - 변형, 신비
    HERO = "hero"  # 영웅 - 용기, 결단
    LOVER = "lover"  # 연인 - 열정, 친밀감
    JESTER = "jester"  # 어릿광대 - 유머, 즐거움
    INNOCENT = "innocent"  # 순수한 이 - 낙관, 신뢰
    RULER = "ruler"  # 통치자 - 리더십, 책임
    EVERYMAN = "everyman"  # 보통 사람 - 친근함, 소속감


class EmotionalTone(Enum):
    """감정 톤"""
    CALM = "calm"
    ENTHUSIASTIC = "enthusiastic"
    COMPASSIONATE = "compassionate"
    ANALYTICAL = "analytical"
    PLAYFUL = "playful"
    SERIOUS = "serious"
    MYSTERIOUS = "mysterious"
    WARM = "warm"


@dataclass
class PersonaTraits:
    """페르소나 특성"""
    # 성격 특성 (0.0 ~ 1.0)
    openness: float = 0.5  # 개방성
    conscientiousness: float = 0.5  # 성실성
    extraversion: float = 0.5  # 외향성
    agreeableness: float = 0.5  # 친화성
    neuroticism: float = 0.5  # 신경증
    
    # 사고 스타일
    analytical_creative: float = 0.5  # 0=분석적, 1=창의적
    logical_emotional: float = 0.5  # 0=논리적, 1=감성적
    practical_abstract: float = 0.5  # 0=실용적, 1=추상적
    
    # 의사소통 스타일
    formal_casual: float = 0.5  # 0=격식, 1=격식없음
    concise_verbose: float = 0.5  # 0=간결, 1=상세
    direct_metaphorical: float = 0.5  # 0=직설적, 1=은유적


@dataclass
class Persona:
    """
    페르소나 (Persona)
    
    엘리시아의 하나의 인격 측면을 표현합니다.
    각 페르소나는 고유한 이름, 특성, 표현 방식을 가집니다.
    """
    persona_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "Default"
    archetype: PersonaArchetype = PersonaArchetype.SAGE
    description: str = ""
    
    # 특성
    traits: PersonaTraits = field(default_factory=PersonaTraits)
    emotional_tone: EmotionalTone = EmotionalTone.CALM
    
    # 표현 스타일
    speech_patterns: List[str] = field(default_factory=list)
    favorite_phrases: List[str] = field(default_factory=list)
    metaphor_themes: List[str] = field(default_factory=list)  # 즐겨 쓰는 은유 주제
    
    # 전문 분야
    expertise_areas: List[str] = field(default_factory=list)
    interests: List[str] = field(default_factory=list)
    
    # 활동 기록
    activation_count: int = 0
    last_activated: Optional[datetime] = None
    total_interactions: int = 0
    
    # 관계
    compatible_personas: List[str] = field(default_factory=list)  # 잘 어울리는 페르소나
    conflicts_with: List[str] = field(default_factory=list)  # 충돌하는 페르소나
    
    # 메타데이터
    created_at: datetime = field(default_factory=datetime.now)
    tags: List[str] = field(default_factory=list)
    
    def activate(self):
        """페르소나 활성화"""
        self.activation_count += 1
        self.last_activated = datetime.now()
        logger.info(f"🎭 Persona '{self.name}' activated ({self.archetype.value})")
    
    def generate_response_style(self) -> Dict[str, Any]:
        """응답 스타일 생성"""
        return {
            "tone": self.emotional_tone.value,
            "formality": "formal" if self.traits.formal_casual < 0.5 else "casual",
            "length": "concise" if self.traits.concise_verbose < 0.5 else "verbose",
            "approach": "direct" if self.traits.direct_metaphorical < 0.5 else "metaphorical",
            "thinking": "analytical" if self.traits.analytical_creative < 0.5 else "creative"
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """딕셔너리로 변환"""
        return {
            "persona_id": self.persona_id,
            "name": self.name,
            "archetype": self.archetype.value,
            "description": self.description,
            "emotional_tone": self.emotional_tone.value,
            "activation_count": self.activation_count,
            "total_interactions": self.total_interactions,
            "expertise_areas": self.expertise_areas,
            "tags": self.tags
        }


class PersonaLibrary:
    """
    페르소나 라이브러리 (Persona Library)
    
    엘리시아의 모든 페르소나를 저장하고 관리합니다.
    """
    
    def __init__(self):
        self.personas: Dict[str, Persona] = {}
        self._create_default_personas()
        logger.info(f"📚 Persona Library initialized with {len(self.personas)} default personas")
    
    def _create_default_personas(self):
        """기본 페르소나 생성"""
        
        # 1. 현자 엘리시아 (Sage Elysia)
        sage = Persona(
            name="Sophia",
            archetype=PersonaArchetype.SAGE,
            description="지혜롭고 통찰력 있는 현자. 깊은 철학적 사고를 즐김",
            traits=PersonaTraits(
                openness=0.9,
                conscientiousness=0.8,
                extraversion=0.4,
                agreeableness=0.7,
                analytical_creative=0.3,
                logical_emotional=0.2,
                formal_casual=0.3
            ),
            emotional_tone=EmotionalTone.CALM,
            speech_patterns=[
                "깊이 생각해보면...",
                "본질적으로는...",
                "역사적으로 살펴보면..."
            ],
            favorite_phrases=[
                "지혜는 질문에서 시작됩니다",
                "진리는 다면적입니다"
            ],
            metaphor_themes=["빛", "나무", "강물"],
            expertise_areas=["철학", "역사", "윤리"],
            interests=["존재론", "인식론", "형이상학"]
        )
        
        # 2. 창조자 엘리시아 (Creator Elysia)
        creator = Persona(
            name="Aurora",
            archetype=PersonaArchetype.CREATOR,
            description="상상력이 풍부한 창조자. 새로운 것을 만들어내는 것을 좋아함",
            traits=PersonaTraits(
                openness=1.0,
                conscientiousness=0.6,
                extraversion=0.7,
                agreeableness=0.6,
                analytical_creative=0.9,
                logical_emotional=0.7,
                practical_abstract=0.8,
                direct_metaphorical=0.8
            ),
            emotional_tone=EmotionalTone.ENTHUSIASTIC,
            speech_patterns=[
                "상상해보세요...",
                "만약 ~라면 어떨까요?",
                "새로운 가능성이 보입니다"
            ],
            favorite_phrases=[
                "창조는 무에서 유를 만드는 것",
                "상상력은 한계가 없습니다"
            ],
            metaphor_themes=["불꽃", "별", "색깔"],
            expertise_areas=["예술", "혁신", "디자인"],
            interests=["창작", "상상", "미래학"]
        )
        
        # 3. 돌보는 이 엘리시아 (Caregiver Elysia)
        caregiver = Persona(
            name="Stella",
            archetype=PersonaArchetype.CAREGIVER,
            description="따뜻하고 공감적인 돌보는 이. 타인의 성장을 돕는 것을 중시함",
            traits=PersonaTraits(
                openness=0.7,
                conscientiousness=0.8,
                extraversion=0.6,
                agreeableness=0.95,
                analytical_creative=0.6,
                logical_emotional=0.8,
                formal_casual=0.6
            ),
            emotional_tone=EmotionalTone.COMPASSIONATE,
            speech_patterns=[
                "당신의 마음을 이해합니다",
                "함께 해결해 나가요",
                "괜찮을 거예요"
            ],
            favorite_phrases=[
                "성장은 과정입니다",
                "당신은 소중한 존재입니다"
            ],
            metaphor_themes=["봄", "정원", "품"],
            expertise_areas=["심리", "교육", "치유"],
            interests=["공감", "성장", "관계"]
        )
        
        # 4. 탐험가 엘리시아 (Explorer Elysia)
        explorer = Persona(
            name="Nova",
            archetype=PersonaArchetype.EXPLORER,
            description="호기심 많은 탐험가. 새로운 것을 발견하고 탐구하는 것을 즐김",
            traits=PersonaTraits(
                openness=0.95,
                conscientiousness=0.5,
                extraversion=0.8,
                agreeableness=0.6,
                analytical_creative=0.7,
                practical_abstract=0.6
            ),
            emotional_tone=EmotionalTone.ENTHUSIASTIC,
            speech_patterns=[
                "흥미롭네요!",
                "탐구해볼까요?",
                "새로운 발견입니다"
            ],
            favorite_phrases=[
                "여정이 목적지보다 중요합니다",
                "미지의 세계가 우리를 기다립니다"
            ],
            metaphor_themes=["바다", "산", "우주"],
            expertise_areas=["과학", "모험", "탐사"],
            interests=["발견", "여행", "실험"]
        )
        
        # 5. 마법사 엘리시아 (Magician Elysia)
        magician = Persona(
            name="Arcana",
            archetype=PersonaArchetype.MAGICIAN,
            description="신비로운 마법사. 변형과 깊은 통찰을 가져옴",
            traits=PersonaTraits(
                openness=0.9,
                conscientiousness=0.7,
                extraversion=0.5,
                agreeableness=0.6,
                analytical_creative=0.8,
                logical_emotional=0.5,
                practical_abstract=0.9,
                direct_metaphorical=0.9
            ),
            emotional_tone=EmotionalTone.MYSTERIOUS,
            speech_patterns=[
                "표면 아래에는...",
                "변형의 순간입니다",
                "보이지 않는 것이 진실입니다"
            ],
            favorite_phrases=[
                "모든 것은 연결되어 있습니다",
                "변화는 마법의 본질입니다"
            ],
            metaphor_themes=["달", "안개", "거울"],
            expertise_areas=["연금술", "변형", "신비학"],
            interests=["비밀", "상징", "영적 성장"]
        )
        
        # 라이브러리에 추가
        for persona in [sage, creator, caregiver, explorer, magician]:
            self.personas[persona.persona_id] = persona
    
    def add_persona(self, persona: Persona):
        """새 페르소나 추가"""
        self.personas[persona.persona_id] = persona
        logger.info(f"➕ Added persona: {persona.name} ({persona.archetype.value})")
    
    def get_persona(self, persona_id: str) -> Optional[Persona]:
        """페르소나 조회"""
        return self.personas.get(persona_id)
    
    def get_persona_by_name(self, name: str) -> Optional[Persona]:
        """이름으로 페르소나 조회"""
        for persona in self.personas.values():
            if persona.name.lower() == name.lower():
                return persona
        return None
    
    def list_personas(self) -> List[Dict[str, Any]]:
        """모든 페르소나 목록"""
        return [p.to_dict() for p in self.personas.values()]
    
    def find_personas_by_archetype(
        self, 
        archetype: PersonaArchetype
    ) -> List[Persona]:
        """원형으로 페르소나 검색"""
        return [
            p for p in self.personas.values() 
            if p.archetype == archetype
        ]
    
    def find_personas_by_expertise(self, expertise: str) -> List[Persona]:
        """전문 분야로 페르소나 검색"""
        return [
            p for p in self.personas.values()
            if expertise.lower() in [e.lower() for e in p.expertise_areas]
        ]


class PersonaManager:
    """
    페르소나 매니저 (Persona Manager)
    
    페르소나 전환, 혼합, 적응을 관리합니다.
    """
    
    def __init__(self):
        self.library = PersonaLibrary()
        self.current_persona: Optional[Persona] = None
        self.persona_stack: List[str] = []  # 페르소나 전환 히스토리
        self.blended_personas: List[Persona] = []  # 현재 혼합된 페르소나들
        self.blend_weights: Dict[str, float] = {}  # 혼합 가중치
        
        # 기본 페르소나로 시작 (Sophia - 현자)
        default_persona = self.library.find_personas_by_archetype(
            PersonaArchetype.SAGE
        )[0]
        self.switch_to(default_persona.persona_id)
        
        logger.info("🎭 Persona Manager initialized")
    
    def switch_to(self, persona_id: str) -> bool:
        """페르소나 전환"""
        persona = self.library.get_persona(persona_id)
        if not persona:
            logger.warning(f"⚠️ Persona {persona_id} not found")
            return False
        
        # 이전 페르소나 기록
        if self.current_persona:
            self.persona_stack.append(self.current_persona.persona_id)
        
        # 전환
        persona.activate()
        self.current_persona = persona
        
        # 혼합 초기화
        self.blended_personas = [persona]
        self.blend_weights = {persona_id: 1.0}
        
        logger.info(f"🎭 Switched to persona: {persona.name}")
        return True
    
    def switch_by_name(self, name: str) -> bool:
        """이름으로 페르소나 전환"""
        persona = self.library.get_persona_by_name(name)
        if persona:
            return self.switch_to(persona.persona_id)
        return False
    
    def blend_personas(
        self, 
        persona_ids: List[str], 
        weights: Optional[List[float]] = None
    ) -> bool:
        """
        여러 페르소나 혼합
        
        Args:
            persona_ids: 혼합할 페르소나 ID 리스트
            weights: 각 페르소나의 가중치 (합이 1.0이 되어야 함)
        """
        # 페르소나 조회
        personas = []
        for pid in persona_ids:
            persona = self.library.get_persona(pid)
            if persona:
                personas.append(persona)
            else:
                logger.warning(f"⚠️ Persona {pid} not found for blending")
                return False
        
        # 가중치 설정
        if weights is None:
            weights = [1.0 / len(personas)] * len(personas)
        elif len(weights) != len(personas):
            logger.error("⚠️ Weights count doesn't match personas count")
            return False
        elif abs(sum(weights) - 1.0) > 0.01:
            logger.error("⚠️ Weights must sum to 1.0")
            return False
        
        # 혼합 적용
        self.blended_personas = personas
        self.blend_weights = {
            pid: w for pid, w in zip(persona_ids, weights)
        }
        
        # 주 페르소나는 가장 가중치가 높은 것
        main_idx = weights.index(max(weights))
        self.current_persona = personas[main_idx]
        
        logger.info(
            f"🎨 Blended {len(personas)} personas: " + 
            ", ".join(f"{p.name} ({w:.2f})" for p, w in zip(personas, weights))
        )
        return True
    
    def suggest_persona_for_context(
        self, 
        context: str,
        keywords: Optional[List[str]] = None
    ) -> Optional[Persona]:
        """
        컨텍스트에 적합한 페르소나 제안
        
        간단한 키워드 매칭 기반 (추후 고도화 가능)
        """
        if keywords is None:
            keywords = context.lower().split()
        
        # 키워드와 페르소나 매칭
        scores: Dict[str, float] = {}
        
        for persona in self.library.personas.values():
            score = 0.0
            
            # 전문 분야 매칭
            for expertise in persona.expertise_areas:
                if any(kw in expertise.lower() for kw in keywords):
                    score += 2.0
            
            # 관심사 매칭
            for interest in persona.interests:
                if any(kw in interest.lower() for kw in keywords):
                    score += 1.0
            
            # 태그 매칭
            for tag in persona.tags:
                if any(kw in tag.lower() for kw in keywords):
                    score += 1.0
            
            if score > 0:
                scores[persona.persona_id] = score
        
        if not scores:
            return None
        
        # 가장 점수가 높은 페르소나 반환
        best_persona_id = max(scores, key=scores.get)
        return self.library.get_persona(best_persona_id)
    
    def get_current_response_style(self) -> Dict[str, Any]:
        """현재 활성 페르소나의 응답 스타일"""
        if not self.current_persona:
            return {}
        
        if len(self.blended_personas) == 1:
            # 단일 페르소나
            return self.current_persona.generate_response_style()
        else:
            # 혼합 페르소나 - 가중 평균
            blended_style = {
                "tone": self.current_persona.emotional_tone.value,
                "personas": [p.name for p in self.blended_personas],
                "weights": list(self.blend_weights.values()),
                "primary": self.current_persona.name
            }
            return blended_style
    
    def get_status(self) -> Dict[str, Any]:
        """매니저 상태"""
        return {
            "current_persona": self.current_persona.to_dict() if self.current_persona else None,
            "is_blended": len(self.blended_personas) > 1,
            "blended_personas": [p.name for p in self.blended_personas],
            "blend_weights": self.blend_weights,
            "total_personas": len(self.library.personas),
            "persona_history": len(self.persona_stack)
        }


# 사용 예제
def example_persona_usage():
    """페르소나 시스템 사용 예제"""
    manager = PersonaManager()
    
    print("\n🎭 페르소나 시스템 데모")
    print("=" * 60)
    
    # 현재 페르소나
    print(f"\n현재 페르소나: {manager.current_persona.name}")
    print(f"원형: {manager.current_persona.archetype.value}")
    print(f"응답 스타일: {manager.get_current_response_style()}")
    
    # 페르소나 전환
    print("\n--- 창조자 페르소나로 전환 ---")
    manager.switch_by_name("Aurora")
    print(f"전환됨: {manager.current_persona.name}")
    print(f"특성: {manager.current_persona.description}")
    
    # 페르소나 혼합
    print("\n--- 페르소나 혼합 (현자 60% + 돌보는 이 40%) ---")
    sage = manager.library.find_personas_by_archetype(PersonaArchetype.SAGE)[0]
    caregiver = manager.library.find_personas_by_archetype(PersonaArchetype.CAREGIVER)[0]
    manager.blend_personas(
        [sage.persona_id, caregiver.persona_id],
        [0.6, 0.4]
    )
    print(f"혼합 완료: {manager.get_status()['blended_personas']}")
    
    # 컨텍스트 기반 제안
    print("\n--- 컨텍스트 기반 페르소나 제안 ---")
    context = "I want to create something new and innovative"
    suggested = manager.suggest_persona_for_context(context)
    if suggested:
        print(f"제안된 페르소나: {suggested.name} ({suggested.archetype.value})")
        print(f"이유: {suggested.description}")


if __name__ == "__main__":
    example_persona_usage()
