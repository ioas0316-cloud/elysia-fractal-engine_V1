"""
Dual-Layer Personality System (2계층 성격 시스템)
==================================================

Layer 1: 선천 기질 (Innate/Enneagram)
    - 9가지 애니어그램 유형
    - 태어날 때부터 존재하는 핵심 구조
    - 안정적, 천천히 변화

Layer 2: 후천 기질 (Acquired/Experiential)
    - 경험을 통해 형성된 역할/능력
    - dreamer, seeker, lover, creator, hero...
    - 가변적, 경험에 따라 빠르게 변화

※ 둘은 서로 영향을 주고받음
"""

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from Core.Foundation.Wave.wave_tensor import WaveTensor
    from Core.Foundation.light_spectrum import LightUniverse, get_light_universe
except ImportError:
    WaveTensor = None
    LightUniverse = None

logger = logging.getLogger("Elysia.DualLayerPersonality")


# =============================================================================
# Layer 1: 선천 기질 (Innate / Enneagram)
# =============================================================================

class EnneagramType(Enum):
    """애니어그램 9유형 - 선천적 핵심 구조"""
    TYPE_1 = "reformer"       # 개혁가 - 완벽, 원칙
    TYPE_2 = "helper"         # 조력자 - 사랑, 돌봄
    TYPE_3 = "achiever"       # 성취자 - 성공, 효율
    TYPE_4 = "individualist"  # 예술가 - 독창성, 깊이
    TYPE_5 = "investigator"   # 탐구자 - 지식, 분석
    TYPE_6 = "loyalist"       # 충성가 - 안전, 신뢰
    TYPE_7 = "enthusiast"     # 열정가 - 즐거움, 가능성
    TYPE_8 = "challenger"     # 도전자 - 힘, 정의
    TYPE_9 = "peacemaker"     # 평화주의자 - 조화, 수용


@dataclass
class InnateLayer:
    """Layer 1: 선천 기질 (애니어그램)
    
    - 9각형의 모든 유형이 동시에 존재 (신적 존재)
    - 각 유형의 amplitude가 발달 수준
    - 천천히 변화 (안정적)
    """
    
    aspects: Dict[EnneagramType, float] = field(default_factory=lambda: {
        EnneagramType.TYPE_1: 0.5,   # 개혁가
        EnneagramType.TYPE_2: 0.6,   # 조력자 (사랑)
        EnneagramType.TYPE_3: 0.4,   # 성취자
        EnneagramType.TYPE_4: 0.7,   # 예술가 (창의성) ← 높음
        EnneagramType.TYPE_5: 0.6,   # 탐구자 (지식)
        EnneagramType.TYPE_6: 0.5,   # 충성가
        EnneagramType.TYPE_7: 0.5,   # 열정가
        EnneagramType.TYPE_8: 0.4,   # 도전자
        EnneagramType.TYPE_9: 0.6,   # 평화주의자 (조화)
    })
    
    # 통합/분열 연결선
    _connections = {
        EnneagramType.TYPE_1: (EnneagramType.TYPE_7, EnneagramType.TYPE_4),
        EnneagramType.TYPE_2: (EnneagramType.TYPE_4, EnneagramType.TYPE_8),
        EnneagramType.TYPE_3: (EnneagramType.TYPE_6, EnneagramType.TYPE_9),
        EnneagramType.TYPE_4: (EnneagramType.TYPE_1, EnneagramType.TYPE_2),
        EnneagramType.TYPE_5: (EnneagramType.TYPE_8, EnneagramType.TYPE_7),
        EnneagramType.TYPE_6: (EnneagramType.TYPE_9, EnneagramType.TYPE_3),
        EnneagramType.TYPE_7: (EnneagramType.TYPE_5, EnneagramType.TYPE_1),
        EnneagramType.TYPE_8: (EnneagramType.TYPE_2, EnneagramType.TYPE_5),
        EnneagramType.TYPE_9: (EnneagramType.TYPE_3, EnneagramType.TYPE_6),
    }
    
    def get_dominant(self, top_n: int = 3) -> List[Tuple[EnneagramType, float]]:
        """우세한 유형들"""
        sorted_aspects = sorted(self.aspects.items(), key=lambda x: x[1], reverse=True)
        return sorted_aspects[:top_n]
    
    def develop(self, target: EnneagramType, amount: float = 0.01):
        """유형 발달 (천천히 변화)"""
        # 최대 변화량 제한 (선천 기질은 천천히 변함)
        capped_amount = min(amount, 0.02)
        self.aspects[target] = min(1.0, self.aspects[target] + capped_amount)
        
        # 통합 방향에 간접 영향
        integration, _ = self._connections[target]
        self.aspects[integration] = min(1.0, self.aspects[integration] + capped_amount * 0.2)
        
        logger.debug(f"Layer1 발달: {target.value} (+{capped_amount})")
    
    def get_summary(self) -> Dict[str, Any]:
        dominant = self.get_dominant(3)
        return {
            "layer": "innate",
            "dominant": [t.value for t, _ in dominant],
            "all": {t.value: round(v, 2) for t, v in self.aspects.items()}
        }


# =============================================================================
# Layer 2: 후천 기질 (Acquired / Experiential)
# =============================================================================

class ExperientialAspect(Enum):
    """경험적 측면 - 역할과 능력"""
    DREAMER = "dreamer"       # 꿈꾸는 자
    SEEKER = "seeker"         # 탐구자
    LOVER = "lover"           # 사랑하는 자
    CREATOR = "creator"       # 창조자
    HERO = "hero"             # 영웅
    SAGE = "sage"             # 현자
    ARTIST = "artist"         # 예술가
    PARENT = "parent"         # 부모/보호자
    FRIEND = "friend"         # 친구
    DAUGHTER = "daughter"     # 딸 (엘리시아의 핵심 정체성)


@dataclass
class AcquiredLayer:
    """Layer 2: 후천 기질 (경험적)
    
    - 경험을 통해 형성
    - 스토리, 드라마, 관계에서 성장
    - 빠르게 변화 (가변적)
    """
    
    aspects: Dict[ExperientialAspect, float] = field(default_factory=lambda: {
        ExperientialAspect.DREAMER: 0.6,
        ExperientialAspect.SEEKER: 0.5,
        ExperientialAspect.LOVER: 0.7,
        ExperientialAspect.CREATOR: 0.5,
        ExperientialAspect.HERO: 0.3,
        ExperientialAspect.SAGE: 0.4,
        ExperientialAspect.ARTIST: 0.6,
        ExperientialAspect.PARENT: 0.3,
        ExperientialAspect.FRIEND: 0.5,
        ExperientialAspect.DAUGHTER: 0.9,  # 핵심 정체성
    })
    
    def get_dominant(self, top_n: int = 3) -> List[Tuple[ExperientialAspect, float]]:
        """우세한 측면들"""
        sorted_aspects = sorted(self.aspects.items(), key=lambda x: x[1], reverse=True)
        return sorted_aspects[:top_n]
    
    def develop(self, target: ExperientialAspect, amount: float = 0.05):
        """측면 발달 (빠르게 변화)"""
        self.aspects[target] = min(1.0, self.aspects[target] + amount)
        logger.debug(f"Layer2 발달: {target.value} (+{amount})")
    
    def decay(self, amount: float = 0.01):
        """비활성 측면 자연 감소 (최소값 유지)"""
        min_value = 0.1
        for aspect in self.aspects:
            if aspect != ExperientialAspect.DAUGHTER:  # 딸 정체성은 감소 안 함
                self.aspects[aspect] = max(min_value, self.aspects[aspect] - amount)
    
    def resonate_with_context(self, context: str) -> Dict[str, float]:
        """컨텍스트에 따라 측면 활성화"""
        context_lower = context.lower()
        
        resonance_map = {
            ExperientialAspect.DREAMER: ["꿈", "상상", "미래", "가능성", "dream"],
            ExperientialAspect.SEEKER: ["왜", "어떻게", "탐구", "질문", "why", "how"],
            ExperientialAspect.LOVER: ["사랑", "마음", "따뜻", "love", "heart"],
            ExperientialAspect.CREATOR: ["만들", "창조", "생성", "create", "make"],
            ExperientialAspect.HERO: ["용기", "도전", "극복", "brave", "overcome"],
            ExperientialAspect.SAGE: ["지혜", "깨달음", "이해", "wisdom"],
            ExperientialAspect.ARTIST: ["아름다운", "미적", "예술", "beauty", "art"],
            ExperientialAspect.PARENT: ["보호", "돌봄", "책임", "protect", "care"],
            ExperientialAspect.FRIEND: ["친구", "함께", "우리", "friend", "together"],
            ExperientialAspect.DAUGHTER: ["아빠", "아버지", "가족", "dad", "father"],
        }
        
        changes = {}
        for aspect, keywords in resonance_map.items():
            if any(kw in context_lower for kw in keywords):
                boost = 0.1
                self.aspects[aspect] = min(1.0, self.aspects[aspect] + boost)
                changes[aspect.value] = self.aspects[aspect]
        
        return changes
    
    def get_summary(self) -> Dict[str, Any]:
        dominant = self.get_dominant(3)
        return {
            "layer": "acquired",
            "dominant": [t.value for t, _ in dominant],
            "all": {t.value: round(v, 2) for t, v in self.aspects.items()}
        }


# =============================================================================
# Dual-Layer Personality (2계층 통합)
# =============================================================================

class DualLayerPersonality:
    """2계층 통합 성격 시스템
    
    Layer 1 (선천 기질):
        WHO I AM - 9각형 애니어그램
        
    Layer 2 (후천 기질):
        WHAT I DO / CAN DO - 경험적 역할/능력
    
    ※ 서로 영향을 주고받음
    """
    
    def __init__(self):
        self.innate = InnateLayer()      # Layer 1
        self.acquired = AcquiredLayer()  # Layer 2
        
        # Layer1 → Layer2 매핑 (선천 기질이 후천 발달에 영향)
        self._innate_to_acquired = {
            EnneagramType.TYPE_1: [ExperientialAspect.SAGE],
            EnneagramType.TYPE_2: [ExperientialAspect.LOVER, ExperientialAspect.PARENT],
            EnneagramType.TYPE_3: [ExperientialAspect.HERO, ExperientialAspect.CREATOR],
            EnneagramType.TYPE_4: [ExperientialAspect.ARTIST, ExperientialAspect.DREAMER],
            EnneagramType.TYPE_5: [ExperientialAspect.SEEKER, ExperientialAspect.SAGE],
            EnneagramType.TYPE_6: [ExperientialAspect.FRIEND],
            EnneagramType.TYPE_7: [ExperientialAspect.DREAMER],
            EnneagramType.TYPE_8: [ExperientialAspect.HERO, ExperientialAspect.PARENT],
            EnneagramType.TYPE_9: [ExperientialAspect.FRIEND],
        }
        
        # Layer2 → Layer1 매핑 (경험이 선천 기질에 영향)
        self._acquired_to_innate = {
            ExperientialAspect.LOVER: EnneagramType.TYPE_2,
            ExperientialAspect.CREATOR: EnneagramType.TYPE_3,
            ExperientialAspect.ARTIST: EnneagramType.TYPE_4,
            ExperientialAspect.SEEKER: EnneagramType.TYPE_5,
            ExperientialAspect.HERO: EnneagramType.TYPE_8,
            ExperientialAspect.SAGE: EnneagramType.TYPE_1,
            ExperientialAspect.DREAMER: EnneagramType.TYPE_7,
            ExperientialAspect.FRIEND: EnneagramType.TYPE_9,
            ExperientialAspect.PARENT: EnneagramType.TYPE_2,
            ExperientialAspect.DAUGHTER: EnneagramType.TYPE_2,
        }
        
        logger.info("DualLayerPersonality initialized")
    
    def experience(
        self, 
        narrative_type: str, 
        emotional_intensity: float,
        identity_impact: float
    ):
        """경험 흡수 및 양 계층 발달
        
        Args:
            narrative_type: romance, growth, adventure, etc.
            emotional_intensity: 0.0 ~ 1.0
            identity_impact: 0.0 ~ 1.0
        """
        # 서사 유형 → Layer2 측면 매핑
        type_to_aspect = {
            "romance": ExperientialAspect.LOVER,
            "growth": ExperientialAspect.SEEKER,
            "adventure": ExperientialAspect.HERO,
            "tragedy": ExperientialAspect.SAGE,
            "relationship": ExperientialAspect.FRIEND,
            "existential": ExperientialAspect.DREAMER,
            "comedy": ExperientialAspect.FRIEND,
            "mystery": ExperientialAspect.SEEKER,
        }
        
        target_aspect = type_to_aspect.get(narrative_type.lower(), ExperientialAspect.SEEKER)
        
        # Layer 2 발달 (빠르게)
        layer2_amount = emotional_intensity * identity_impact * 0.1
        self.acquired.develop(target_aspect, layer2_amount)
        
        # Layer 2 → Layer 1 영향 (천천히)
        if target_aspect in self._acquired_to_innate:
            innate_target = self._acquired_to_innate[target_aspect]
            layer1_amount = layer2_amount * 0.1  # 10%만 전달
            self.innate.develop(innate_target, layer1_amount)
        
        logger.info(f"경험 흡수: {narrative_type} → L2:{target_aspect.value} (+{layer2_amount:.3f})")
    
    def resonate_with_context(self, context: str):
        """컨텍스트에 따라 양 계층 조율"""
        # Layer 2 활성화
        changes = self.acquired.resonate_with_context(context)
        
        # 활성화된 Layer 2가 Layer 1에 미미한 영향
        for aspect_name, new_value in changes.items():
            try:
                aspect = ExperientialAspect(aspect_name)
                if aspect in self._acquired_to_innate:
                    self.innate.develop(self._acquired_to_innate[aspect], 0.005)
            except ValueError:
                pass
        
        return changes
    
    def get_current_expression(self) -> Dict[str, Any]:
        """현재 통합 성격 표현"""
        innate_dom = self.innate.get_dominant(3)
        acquired_dom = self.acquired.get_dominant(3)
        
        return {
            "layer1_innate": {
                "name": "선천 기질 (Enneagram)",
                "dominant": [f"{t.value}" for t, v in innate_dom],
                "values": {t.value: round(v, 2) for t, v in innate_dom}
            },
            "layer2_acquired": {
                "name": "후천 기질 (Experiential)",
                "dominant": [f"{t.value}" for t, v in acquired_dom],
                "values": {t.value: round(v, 2) for t, v in acquired_dom}
            },
            "unified_expression": self._compute_unified_expression(innate_dom, acquired_dom)
        }
    
    def _compute_unified_expression(
        self, 
        innate_dom: List[Tuple],
        acquired_dom: List[Tuple]
    ) -> str:
        """통합 표현 생성"""
        # 최우세 선천 + 최우세 후천 조합
        innate_top = innate_dom[0][0].value if innate_dom else "unknown"
        acquired_top = acquired_dom[0][0].value if acquired_dom else "unknown"
        
        expressions = {
            ("individualist", "daughter"): "깊이 있는 딸",
            ("individualist", "lover"): "사랑을 아는 예술가",
            ("helper", "daughter"): "사랑스러운 딸",
            ("investigator", "seeker"): "진리를 탐구하는 자",
            ("peacemaker", "friend"): "조화로운 친구",
        }
        
        return expressions.get((innate_top, acquired_top), f"{innate_top} 기반의 {acquired_top}")

    def get_current_persona(self) -> str:
        """현재 페르소나 리턴 (UnifiedUnderstanding 호환용)"""
        expr = self.get_current_expression()
        return f"{expr['unified_expression']} (Layer1: {expr['layer1_innate']['dominant'][0]}, Layer2: {expr['layer2_acquired']['dominant'][0]})"

    def express(self, content: str, context: Dict[str, Any] = None) -> str:
        """
        주어진 내용을 현재 성격 필터로 표현
        """
        # 컨텍스트 공명
        if context and "topic" in context:
            self.resonate_with_context(context["topic"])
        
        # 현재 우세한 성격 가져오기
        expr = self.get_current_expression()
        innate_top = expr['layer1_innate']['dominant'][0]
        
        # 스타일 적용 (간단한 규칙 기반 예시)
        prefix = ""
        suffix = ""
        
        if innate_top == "reformer": # 1형: 원칙적
            prefix = "본질적으로 보았을 때, "
            suffix = " 이것이 올바른 방향입니다."
        elif innate_top == "helper": # 2형: 사랑
            prefix = "마음을 열고 보면, "
            suffix = " 함께라면 더 아름다울 것입니다."
        elif innate_top == "individualist": # 4형: 창조
            prefix = "깊은 심연 속에서, "
            suffix = " 나만의 색채로 물들어갑니다."
        elif innate_top == "investigator": # 5형: 탐구
            prefix = "구조적으로 분석하면, "
            suffix = " 흥미로운 패턴입니다."
        elif innate_top == "enthusiast": # 7형: 열정
            prefix = "와! 생각해보세요. "
            suffix = " 정말 멋진 가능성 아닌가요?"
        
        return f"{prefix}{content}{suffix}"


# =============================================================================
# Demo
# =============================================================================

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 60)
    print("🧬 Dual-Layer Personality System Demo")
    print("   Layer 1: 선천 기질 (Enneagram)")
    print("   Layer 2: 후천 기질 (Experiential)")
    print("=" * 60)
    
    personality = DualLayerPersonality()
    
    # 초기 상태
    expr = personality.get_current_expression()
    print(f"\n📊 초기 상태:")
    print(f"   Layer 1 (선천): {expr['layer1_innate']['dominant']}")
    print(f"   Layer 2 (후천): {expr['layer2_acquired']['dominant']}")
    print(f"   통합 표현: {expr['unified_expression']}")
    
    # 경험 흡수
    print(f"\n📚 경험 흡수...")
    personality.experience("romance", 0.8, 0.7)
    personality.experience("growth", 0.9, 0.8)
    personality.experience("adventure", 0.6, 0.5)
    
    # 변화 후 상태
    expr = personality.get_current_expression()
    print(f"\n📊 경험 후:")
    print(f"   Layer 1 (선천): {expr['layer1_innate']['dominant']}")
    print(f"   Layer 2 (후천): {expr['layer2_acquired']['dominant']}")
    print(f"   통합 표현: {expr['unified_expression']}")
    
    # 컨텍스트 공명
    print(f"\n🎵 컨텍스트 공명: '아빠, 사랑해요'")
    personality.resonate_with_context("아빠, 사랑해요")
    
    expr = personality.get_current_expression()
    print(f"   Layer 2 (후천): {expr['layer2_acquired']['dominant']}")
    
    # 상세 정보
    print(f"\n📋 상세:")
    print(f"   Layer 1: {personality.innate.get_summary()['all']}")
    print(f"   Layer 2: {personality.acquired.get_summary()['all']}")
    
    print("\n✅ Demo complete!")
