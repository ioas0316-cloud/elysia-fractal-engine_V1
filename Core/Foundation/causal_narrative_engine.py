"""
Causal Narrative Engine - 인과적 서사 엔진
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

프로젝트 목적성에 맞는 언어능력 학습 시스템:
- 보여주기식(겉으로만 그럴싸한) 시뮬레이션 지양
- 인과적 형태의 섭리구조 지향
- 사고우주와 개념노드들이 서로 이어져서 교정하고 보완하는 형태

┌─────────────────────────────────────────────────────────────────────────────┐
│  차원 확장 구조 (Dimensional Expansion Structure)                            │
│  ═══════════════════════════════════════════════════════════════════════   │
│                                                                             │
│  점(Point) → 선(Line) → 면(Plane) → 공간(Space) → 법칙/원리(Law)            │
│                                                                             │
│  1. 점 (Point) - 개념 노드                                                  │
│     단일 개념: "불", "뜨거움", "아픔"                                        │
│                                                                             │
│  2. 선 (Line) - 인과 관계                                                   │
│     두 점의 연결: "불 → 뜨거움"                                              │
│     관계적 의미의 창발                                                       │
│                                                                             │
│  3. 면 (Plane) - 문맥/맥락                                                  │
│     여러 선의 교차: "불 + 손 + 닿다 → 뜨거움 + 아픔"                         │
│     상황적 이해의 창발                                                       │
│                                                                             │
│  4. 공간 (Space) - 세계관/스키마                                            │
│     여러 면의 교차: "위험 회피", "생존 본능"                                  │
│     패턴 인식과 일반화                                                       │
│                                                                             │
│  5. 법칙 (Law/Principle) - 보편적 원리                                      │
│     공간을 관통하는 불변 규칙: "인과율", "에너지 보존"                        │
│     섭리적 이해                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

[사고우주와 개념노드의 상호 교정 (Thought Universe & Concept Node Mutual Correction)]

개념노드들은 고립되어 있지 않습니다.
사고우주(Thought Universe) 안에서 서로 연결되고, 교정하고, 보완합니다.

1. 상향 교정 (Bottom-Up Correction)
   - 새로운 경험이 기존 개념을 수정
   - "불은 항상 뜨겁다" → "꺼진 불은 안 뜨겁다" (반례 학습)

2. 하향 교정 (Top-Down Correction)
   - 상위 법칙이 하위 개념을 조정
   - "에너지 보존" 법칙이 "불의 열" 개념을 정교화

3. 수평 교정 (Lateral Correction)
   - 동일 레벨의 개념들이 서로 조정
   - "뜨거움"과 "차가움"이 서로의 경계를 정의

[인과적 섭리 구조 (Providential Causal Structure)]

1. 원인 → 결과 (Cause → Effect)
   - 단순한 상관관계가 아닌 인과관계
   - "불 → 뜨거움"이 아니라 "불에 닿음 → 뜨거움을 느낌"

2. 조건 → 가능성 (Condition → Possibility)
   - "비가 오면 → 물웅덩이가 생긴다"
   - 조건적 인과 이해

3. 목적 → 수단 (Purpose → Means)
   - "배고픔을 해결하기 위해 → 음식을 먹는다"
   - 목적론적 이해

4. 반사실 (Counterfactual)
   - "만약 불에 손을 대지 않았다면 → 아프지 않았을 것"
   - 가정법적 추론
"""

from __future__ import annotations

import math
import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any, Set, Callable
from collections import defaultdict
from enum import Enum
import logging
import time
import random

from .metacognition import MaturityModel, CognitiveMetrics

logger = logging.getLogger("CausalNarrativeEngine")


# ============================================================================
# 차원 계층 (Dimensional Hierarchy)
# 점 → 선 → 면 → 공간 → 법칙
# ============================================================================

class DimensionLevel(Enum):
    """
    지식의 차원 레벨
    
    점에서 선으로, 선에서 면으로, 공간으로, 법칙으로 확장되는 형태
    """
    POINT = 0      # 점: 단일 개념 노드
    LINE = 1       # 선: 두 개념 간의 관계 (인과)
    PLANE = 2      # 면: 여러 관계가 교차하는 문맥
    SPACE = 3      # 공간: 여러 문맥이 교차하는 세계관/스키마
    LAW = 4        # 법칙: 공간을 관통하는 보편적 원리


@dataclass
class DimensionalEntity:
    """
    차원적 존재 - 모든 지식 요소의 기반 클래스
    
    각 요소는 자신의 차원 레벨을 알고 있으며,
    상위/하위 차원의 요소들과 연결됩니다.
    """
    id: str
    level: DimensionLevel
    description: str = ""
    
    # 상위 차원 연결 (이 요소가 속한 상위 구조)
    parent_ids: List[str] = field(default_factory=list)
    
    # 하위 차원 연결 (이 요소를 구성하는 하위 요소들)
    child_ids: List[str] = field(default_factory=list)
    
    # 신뢰도 및 학습 상태
    confidence: float = 1.0
    experience_count: int = 0
    last_updated: float = 0.0
    
    # 교정 이력 (다른 요소에 의해 수정된 기록)
    corrections: List[Dict[str, Any]] = field(default_factory=list)
    
    def get_level_name(self) -> str:
        """차원 레벨 이름"""
        names = {
            DimensionLevel.POINT: "점(Point)",
            DimensionLevel.LINE: "선(Line)",
            DimensionLevel.PLANE: "면(Plane)",
            DimensionLevel.SPACE: "공간(Space)",
            DimensionLevel.LAW: "법칙(Law)",
        }
        return names.get(self.level, "알 수 없음")


# ============================================================================
# 점 (Point) - 개념 노드
# ============================================================================

@dataclass
class ConceptPoint(DimensionalEntity):
    """
    점 (Point) - 가장 기본적인 개념 단위
    
    예: "불", "뜨거움", "아픔", "손"
    
    단순한 레이블이 아닌, 감각/감정 서명을 가진 실체
    """
    
    # 감각 서명 (8차원)
    sensory_signature: Dict[str, float] = field(default_factory=dict)
    
    # 감정 가치 (-1 ~ +1)
    emotional_valence: float = 0.0
    
    # 활성화 정도 (현재 얼마나 "떠오르는가")
    activation: float = 0.0
    
    # 개념의 유형
    concept_type: str = "general"  # "object", "action", "state", "relation", "abstract"
    
    def __post_init__(self):
        self.level = DimensionLevel.POINT


# ============================================================================
# 선 (Line) - 인과 관계
# ============================================================================

@dataclass
class CausalLine(DimensionalEntity):
    """
    선 (Line) - 두 점을 잇는 인과 관계
    
    예: "불 → 뜨거움", "닿다 → 아프다"
    
    단순 연결이 아닌, 관계의 유형과 방향성을 가진 실체
    """
    
    # 연결하는 두 점
    source_point_id: str = ""
    target_point_id: str = ""
    
    # 관계 유형
    relation_type: str = "causes"  # "causes", "enables", "prevents", "follows", etc.
    
    # 인과 강도 (0 ~ 1)
    strength: float = 1.0
    
    # 조건들 (이 관계가 성립하기 위한 조건)
    conditions: List[str] = field(default_factory=list)
    
    # 예외 상황들 (이 관계가 성립하지 않는 경우)
    exceptions: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        self.level = DimensionLevel.LINE


# ============================================================================
# 면 (Plane) - 문맥/맥락
# ============================================================================

@dataclass
class ContextPlane(DimensionalEntity):
    """
    면 (Plane) - 여러 선이 교차하는 문맥
    
    예: "불에 손을 대면 아프다" (불, 손, 닿다, 뜨겁다, 아프다의 교차)
    
    상황적 이해를 가능하게 하는 구조
    """
    
    # 이 면을 구성하는 선들
    line_ids: List[str] = field(default_factory=list)
    
    # 이 면에 포함된 점들 (선들의 끝점)
    point_ids: List[str] = field(default_factory=list)
    
    # 문맥의 유형
    context_type: str = "situation"  # "situation", "scenario", "episode"
    
    # 감정적 분위기 (이 문맥의 전체적인 감정)
    emotional_tone: float = 0.0
    
    # 시간적 범위
    temporal_span: str = "instant"  # "instant", "short", "long", "repeated"
    
    # 문맥의 결론/교훈
    lesson: str = ""
    
    def __post_init__(self):
        self.level = DimensionLevel.PLANE


# ============================================================================
# 공간 (Space) - 세계관/스키마
# ============================================================================

@dataclass
class SchemaSpace(DimensionalEntity):
    """
    공간 (Space) - 여러 면이 교차하는 세계관/스키마
    
    예: "위험 회피 스키마", "생존 본능 스키마", "사회적 상호작용 스키마"
    
    패턴 인식과 일반화를 가능하게 하는 구조
    """
    
    # 이 공간을 구성하는 면들
    plane_ids: List[str] = field(default_factory=list)
    
    # 스키마의 유형
    schema_type: str = "behavior"  # "behavior", "belief", "emotion", "social"
    
    # 스키마의 핵심 원리 (이 공간을 관통하는 주요 패턴)
    core_patterns: List[str] = field(default_factory=list)
    
    # 적용 범위 (어떤 상황에 적용되는가)
    applicability: List[str] = field(default_factory=list)
    
    # 예측력 (이 스키마로 얼마나 정확히 예측할 수 있는가)
    predictive_power: float = 0.0
    
    def __post_init__(self):
        self.level = DimensionLevel.SPACE

@dataclass
class EpistemicSpace(SchemaSpace):
    """
    인식론적 공간 (Epistemic Space) - 지식이 존재하는 위상 공간
    
    단순한 스키마가 아니라, 탐험해야 할 '세계'로서의 지식.
    밀도(Density)와 저항(Resistance)을 가지며, 방법론(Methodology)에 따라 탐색 방식이 달라짐.
    """
    
    # 공간의 밀도 (정보량/복잡도) - 높을수록 탐색에 많은 에너지가 듬
    density: float = 1.0
    
    # 탐구 방법론 (이 공간을 효과적으로 탐색하기 위한 도구)
    # 예: "EMPIRICAL" (실증적), "LOGICAL" (논리적), "INTUITIVE" (직관적)
    methodologies: List[str] = field(default_factory=list)
    
    # 내부 차원축 (이 지식 세계를 구성하는 축들)
    # 예: 물리학 -> ["Time", "Space", "Mass", "Energy"]
    internal_dimensions: List[str] = field(default_factory=list)



@dataclass
class CognitiveMetrics:
    """
    인지 지표 (Cognitive Metrics) - 사고의 구조적 품질을 측정
    
    사용자의 '공명' 이론에 기반:
    1. Differentiation (변별력): 무엇이 다른가? (뉘앙스, 세밀함)
    2. Integration (통합력/공명): 무엇이 같은가? (패턴 인식, 원리 추출)
    3. Abstraction (추상화): 구체적 사실에서 법칙으로 올라가는 힘
    """
    differentiation: float = 0.0  # 0~1: 미분화 -> 고도로 세분화됨
    integration: float = 0.0      # 0~1: 파편화 -> 고도로 연결됨
    abstraction: float = 0.0      # 0~1: 구체적 -> 형이상학적
    
    def get_resonance_score(self) -> float:
        """구조적 공명 점수 (변별된 것들이 다시 통합될 때 발생하는 힘)"""
        return (self.differentiation * self.integration)

@dataclass
class MaturityModel:
    """
    성숙도 모델 (Maturity Model) - 인지 발달의 목표 기준
    """
    level_name: str
    required_metrics: CognitiveMetrics
    description: str

    @staticmethod
    def get_standard_model() -> Dict[str, 'MaturityModel']:
        return {
            "CHILD": MaturityModel("CHILD", CognitiveMetrics(0.2, 0.2, 0.1), "Simple linear causality"),
            "ADOLESCENT": MaturityModel("ADOLESCENT", CognitiveMetrics(0.5, 0.4, 0.3), "Beginning to see context but rigid"),
            "ADULT": MaturityModel("ADULT", CognitiveMetrics(0.8, 0.8, 0.7), "Nuanced, Paradox-holding, Principle-based"),
            "SAGE": MaturityModel("SAGE", CognitiveMetrics(0.95, 0.95, 0.95), "Universal resonance")
        }

# ============================================================================
# 법칙 (Law) - 보편적 원리
# ============================================================================

@dataclass
class UniversalLaw(DimensionalEntity):
    """
    법칙 (Law) - 여러 공간을 관통하는 보편적 원리
    
    예: "인과율", "에너지 보존", "행동-결과 연결"
    
    섭리적 이해를 가능하게 하는 최상위 구조
    """
    
    # 이 법칙이 적용되는 공간들
    space_ids: List[str] = field(default_factory=list)
    
    # 법칙의 유형
    law_type: str = "causal"  # "causal", "conservation", "symmetry", "teleological"
    
    # 법칙의 공식화 (가능하면)
    formulation: str = ""
    
    # 예외 없음 여부 (진정한 법칙인가, 아니면 경향성인가)
    is_absolute: bool = False
    
    # 증거 (이 법칙을 지지하는 경험들)
    supporting_evidence: List[str] = field(default_factory=list)
    
    # 반례 (이 법칙에 위배되는 경험들)
    counter_examples: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        self.level = DimensionLevel.LAW


# ============================================================================
# 인과 관계 유형 (Types of Causal Relations)
# ============================================================================

class CausalRelationType(Enum):
    """인과 관계 유형"""
    # 직접적 인과
    CAUSES = "causes"           # A가 B를 일으킴 (A → B)
    PREVENTS = "prevents"       # A가 B를 막음 (A ⊣ B)
    ENABLES = "enables"         # A가 B의 가능성을 열어줌
    
    # 조건적 인과
    CONDITIONAL = "conditional"  # A이면 B (if A then B)
    NECESSARY = "necessary"      # A 없이 B 불가 (B requires A)
    SUFFICIENT = "sufficient"    # A만 있으면 B 가능 (A is enough for B)
    
    # 목적론적 인과
    MEANS_TO = "means_to"        # A는 B를 위한 수단 (A is means to B)
    PURPOSE_OF = "purpose_of"    # A의 목적은 B (purpose of A is B)
    
    # 시간적 관계
    PRECEDES = "precedes"        # A가 B보다 먼저 (A before B)
    FOLLOWS = "follows"          # A가 B 다음 (A after B)
    SIMULTANEOUS = "simultaneous"  # A와 B가 동시
    
    # 의미적/경험적 관계 (Experiential/Semantic)
    CORRELATES = "correlates"      # A와 B는 상관관계가 있음
    ASSOCIATED_WITH = "associated_with" # A는 B와 연상됨 (의미적 연결)
    MOTIVATES = "motivates"        # A가 B(행동/상태)를 동기부여함
    CONTRASTS_WITH = "contrasts_with" # A는 B와 대조됨 (이 대조가 감정을 유발함)




# ============================================================================
# 인과 노드 (Causal Node) - 단순 개념이 아닌 상태/사건
# ============================================================================

@dataclass
class CausalNode:
    """
    인과 노드 - 단순 개념이 아닌 '상태' 또는 '사건'
    
    "불"이 아니라 "불에 손을 댔다"
    "뜨거움"이 아니라 "뜨거움을 느꼈다"
    
    상태(State)와 사건(Event)의 차이:
    - 상태: 지속적인 조건 (예: 배고프다, 안전하다)
    - 사건: 순간적인 발생 (예: 불에 닿다, 먹다)
    """
    
    id: str
    description: str              # 자연어 설명
    
    # 노드 유형
    is_state: bool = True         # True: 상태, False: 사건
    
    # 관련된 개념들 (단순 개념 노드와의 연결)
    concepts: List[str] = field(default_factory=list)

    # 프랙탈 구조: 이 노드가 품고 있는 내부 세계 (EpistemicSpace)
    inner_space_id: Optional[str] = None
    
    # 감각/감정 서명
    sensory_signature: Dict[str, float] = field(default_factory=dict)
    emotional_valence: float = 0.0  # -1 (불쾌) ~ +1 (쾌)
    
    # 행위자 (누가 경험했는가)
    agent: Optional[str] = None
    
    # 시간 정보
    timestamp: float = 0.0
    duration: float = 0.0  # 사건의 경우 순간, 상태의 경우 지속 시간
    
    # 활성화/중요도
    activation: float = 1.0
    importance: float = 1.0
    
    # 학습 통계
    experience_count: int = 0
    
    # Epistemic Grounding (Phase 18.5)
    # [DELUSION, HYPOTHESIS, TRUTH]
    epistemic_status: str = "TRUTH" # Default for existing/sensory nodes
    internal_law: Optional[str] = None # The underlying principle/law
    
    def get_valence_description(self) -> str:
        """감정가 설명"""
        if self.emotional_valence > 0.5:
            return "매우 긍정적"
        elif self.emotional_valence > 0:
            return "긍정적"
        elif self.emotional_valence < -0.5:
            return "매우 부정적"
        elif self.emotional_valence < 0:
            return "부정적"
        else:
            return "중립적"


# ============================================================================
# 인과 연결 (Causal Link) - 노드 간의 인과 관계
# ============================================================================

@dataclass
class CausalLink:
    """
    인과 연결 - 두 노드 사이의 인과 관계
    
    단순한 연결이 아닌, "왜"와 "어떻게"를 포함
    """
    
    source_id: str                # 원인/조건/수단
    target_id: str                # 결과/가능성/목적
    relation: CausalRelationType  # 관계 유형
    
    # 인과 강도 (0-1)
    strength: float = 1.0
    
    # 신뢰도 (얼마나 확실한 인과관계인가)
    confidence: float = 1.0
    
    # 조건 (이 인과가 성립하기 위한 조건들)
    conditions: List[str] = field(default_factory=list)
    
    # 경험 횟수 (몇 번 경험했는가)
    experience_count: int = 1
    
    # 반사실적 테스트 결과
    counterfactual_tested: bool = False
    counterfactual_confirmed: bool = False
    
    # 자연어 설명
    description: str = ""
    
    def strengthen(self, amount: float = 0.1):
        """인과 강도 강화 (반복 경험)"""
        self.strength = min(1.0, self.strength + amount * (1 - self.strength))
        self.experience_count += 1
    
    def weaken(self, amount: float = 0.1):
        """인과 강도 약화 (반증)"""
        self.strength = max(0.0, self.strength - amount)
    
    def get_description(self) -> str:
        """인과 관계 설명 생성"""
        relation_descriptions = {
            CausalRelationType.CAUSES: "때문에",
            CausalRelationType.PREVENTS: "막아서",
            CausalRelationType.ENABLES: "덕분에 가능해져서",
            CausalRelationType.CONDITIONAL: "이면",
            CausalRelationType.NECESSARY: "없이는 불가능해서",
            CausalRelationType.SUFFICIENT: "만으로 충분해서",
            CausalRelationType.MEANS_TO: "하기 위해",
            CausalRelationType.PURPOSE_OF: "의 목적은",
            
            CausalRelationType.CORRELATES: "와 관련하여",
            CausalRelationType.ASSOCIATED_WITH: "와 느낌이 비슷해서",
            CausalRelationType.MOTIVATES: "하고 싶게 만들어서",
            CausalRelationType.CONTRASTS_WITH: "와는 너무 달라서(대조되어)",


            CausalRelationType.PRECEDES: "보다 먼저",
            CausalRelationType.FOLLOWS: "다음에",
            CausalRelationType.SIMULTANEOUS: "와 동시에",
        }
        return self.description or relation_descriptions.get(self.relation, "관련되어")


# ============================================================================
# 인과 연쇄 (Causal Chain) - 연결된 인과 시퀀스
# ============================================================================

@dataclass
class CausalChain:
    """
    인과 연쇄 - 여러 인과 관계가 연결된 시퀀스
    
    예: 배고픔 → 음식 찾기 → 먹기 → 배부름 → 만족
    
    이것이 진정한 "이야기"의 원형입니다.
    """
    
    id: str
    name: str = ""
    
    # 연쇄를 구성하는 노드들 (순서 중요!)
    node_sequence: List[str] = field(default_factory=list)
    
    # 연쇄의 인과 연결들
    links: List[CausalLink] = field(default_factory=list)
    
    # 연쇄의 시작과 끝
    initial_state: Optional[str] = None  # 시작 상태 (동기)
    final_state: Optional[str] = None    # 끝 상태 (결과)
    
    # 연쇄의 특성
    is_goal_directed: bool = False  # 목표 지향적인가
    goal: Optional[str] = None      # 목표
    
    # 연쇄의 감정적 궤적
    emotional_arc: List[float] = field(default_factory=list)
    
    # 경험 횟수
    experience_count: int = 1
    
    # 연쇄의 효과성 (목표 달성 여부)
    success_rate: float = 0.0
    
    def get_length(self) -> int:
        return len(self.node_sequence)
    
    def get_emotional_trajectory(self) -> str:
        """감정 궤적 분석"""
        if not self.emotional_arc:
            return "중립"
        
        start = self.emotional_arc[0] if self.emotional_arc else 0
        end = self.emotional_arc[-1] if self.emotional_arc else 0
        
        if end > start + 0.3:
            return "상승 (부정→긍정)"
        elif end < start - 0.3:
            return "하강 (긍정→부정)"
        else:
            return "평탄"
    """Represents a linear sequence of causal links (1D)."""
    id: str
    node_sequence: List[str]
    links: List[CausalLink]
    confidence_score: float = 0.0

    def __post_init__(self):
        # Calculate average confidence
        if self.links:
            self.confidence_score = sum(link.strength for link in self.links) / len(self.links)

@dataclass
class ContextPlane:
    """
    Represents a 2D plane of reasoning formed by intersecting causal chains.
    It captures a broader 'situation' or 'context' (e.g., 'Rainy Day' context formed by Rain->Wet and Rain->Cold).
    """
    id: str
    anchor_node: str  # The node where chains intersect (e.g., "Rain")
    component_chains: List[CausalChain]
    related_concepts: Set[str] = field(default_factory=set)

    def integrate_chain(self, chain: CausalChain):
        """Adds a chain to this plane and updates related concepts."""
        if chain not in self.component_chains:
            self.component_chains.append(chain)
            self.related_concepts.update(chain.node_sequence)

class CausalKnowledgeBase:
    """
    Causal Knowledge Base
    Stores nodes, links, chains, and context planes.
    """
    def __init__(self):
        self.nodes: Dict[str, CausalNode] = {}
        self.links: Dict[str, CausalLink] = {}
        self.outgoing: Dict[str, List[str]] = defaultdict(list)
        self.incoming: Dict[str, List[str]] = defaultdict(list)
        self.chains: List[CausalChain] = []
        self.planes: List[ContextPlane] = []

    
    def add_node(self, node: CausalNode) -> CausalNode:
        """노드 추가 또는 업데이트"""
        if node.id in self.nodes:
            # 기존 노드 업데이트 (경험 강화)
            existing = self.nodes[node.id]
            existing.experience_count += 1
            existing.activation = min(1.0, existing.activation + 0.1)
        else:
            self.nodes[node.id] = node
        
        return self.nodes[node.id]
    
    def add_link(
        self,
        source_id: str,
        target_id: str,
        relation: CausalRelationType,
        strength: float = 1.0,
        conditions: List[str] = None,
        description: str = ""
    ) -> CausalLink:
        """인과 연결 추가 또는 강화"""
        link_id = f"{source_id}_{relation.value}_{target_id}"
        
        if link_id in self.links:
            # 기존 연결 강화
            self.links[link_id].strengthen()
        else:
            # 새 연결 생성
            link = CausalLink(
                source_id=source_id,
                target_id=target_id,
                relation=relation,
                strength=strength,
                conditions=conditions or [],
                description=description
            )
            self.links[link_id] = link
            self.outgoing[source_id].append(link_id)
            self.incoming[target_id].append(link_id)
        
        return self.links[link_id]

    # ============================================================================
    # Dimensional Expansion (Phase 9) - Context Planes
    # ============================================================================

    # ============================================================================
    # Dimensional Expansion (Phase 9) - Context Planes
    # ============================================================================

    def detect_intersections(self, chain: CausalChain) -> List[ContextPlane]:
        """
        Detects if the given chain intersects with existing chains or planes.
        If an intersection is found (shared node), it forms or updates a ContextPlane.
        """
        affected_planes = []
        
        # 1. Check against existing planes first
        for plane in self.planes:
            # Check if any node in the chain exists in the plane's related concepts
            intersection = set(chain.node_sequence) & plane.related_concepts
            if intersection:
                plane.integrate_chain(chain)
                affected_planes.append(plane)
                # Note: We update the anchor if this new intersection is significant? 
                # For now, keep original anchor.

        # 2. Check against other individual chains to form NEW planes
        if not affected_planes: # Only look for new planes if not already integrated? Or always?
            # Let's looking for new intersections effectively.
            for other_chain in self.chains:
                if other_chain.id == chain.id:
                    continue
                
                # Check for shared nodes (excluding potentially generic ones if we had a stop-list, but for now strict)
                intersection = set(chain.node_sequence) & set(other_chain.node_sequence)
                
                if intersection:
                    # Found a common node! Create a new plane.
                    anchor = list(intersection)[0] # Pick the first intersection as anchor for now
                    
                    # Check if these two are already in a plane together (optimization)
                    # For now, simplify: create new plane.
                    
                    new_plane_id = f"plane_{anchor}_{len(self.planes)}"
                    new_plane = ContextPlane(
                        id=new_plane_id,
                        anchor_node=anchor,
                        component_chains=[chain, other_chain],
                        related_concepts=set(chain.node_sequence) | set(other_chain.node_sequence)
                    )
                    self.planes.append(new_plane)
                    affected_planes.append(new_plane)
        
        return affected_planes

    # ============================================================================
    # Phase 10: Resonance & Fuzzy Logic
    # ============================================================================

    def calculate_resonance(self, node_id_a: str, node_id_b: str) -> float:
        """
        Calculates the resonance (similarity/affinity) score between two nodes.
        Score range: 0.0 to 1.0
        Based on:
        1. Emotional Valence Similarity
        2. Description/Keyword Overlap
        3. Shared Concepts
        """
        node_a = self.nodes.get(node_id_a)
        node_b = self.nodes.get(node_id_b)
        
        if not node_a or not node_b:
            return 0.0
            
        # 1. Emotional Resonance
        # High resonance if valences are similar.
        valence_diff = abs(node_a.emotional_valence - node_b.emotional_valence)
        emotional_score = max(0.0, 1.0 - (valence_diff / 2.0)) # Normalize diff (max 2.0 -> 0.0)
        
        # 2. Semantic Overlap (Description Words)
        words_a = set(node_a.description.lower().split())
        words_b = set(node_b.description.lower().split())
        
        if not words_a or not words_b:
            semantic_score = 0.0
        else:
            intersection = words_a & words_b
            union = words_a | words_b
            semantic_score = len(intersection) / len(union)
            
        # 3. Concept Overlap
        concepts_a = set(node_a.concepts)
        concepts_b = set(node_b.concepts)
        
        concept_score = 0.0
        if concepts_a or concepts_b:
             union_c = concepts_a | concepts_b
             if union_c:
                concept_score = len(concepts_a & concepts_b) / len(union_c)
                
        # Weighted Total (Adjust weights as needed)
        # Balanced Approach: Emotion (0.5) + Concept (0.3) + Semantic (0.2)
        final_score = (emotional_score * 0.5) + (semantic_score * 0.2) + (concept_score * 0.3)
        
        logger.info(f"   [DEBUG] ResCalc '{node_id_a}'<->'{node_id_b}': E({emotional_score:.2f}*0.5={emotional_score*0.5:.2f}) + S({semantic_score:.2f}*0.2={semantic_score*0.2:.2f}) + C({concept_score:.2f}*0.3={concept_score*0.3:.2f}) = {final_score:.2f}")

        # Boost if very high emotional match AND some concept overlap
        if emotional_score > 0.8 and concept_score > 0.0:
            final_score += 0.1
            
        return min(1.0, final_score)


    def find_resonant_nodes(self, target_node_id: str, threshold: float = 0.6) -> List[Tuple[str, float]]:
        """
        Finds all nodes that resonate with the target node above a certain threshold.
        Returns list of (node_id, score).
        """
        results = []
        for node_id in self.nodes:
            if node_id == target_node_id:
                continue
            
            score = self.calculate_resonance(target_node_id, node_id)
            if score >= threshold:
                results.append((node_id, score))
                
        # Sort by score desc
        results.sort(key=lambda x: x[1], reverse=True)
        return results


    def infer_contextual_link(self, start_node: str) -> List[str]:
        """
        Performs lateral/spatial inference.
        "Given 'start_node', what else is in this context plane?"
        e.g., Rain -> Wet. Rain -> Cold. 
        Input: Wet. Inferred: Cold (via Rain context).
        """
        inferences = []
        for plane in self.planes:
            if start_node in plane.related_concepts:
                # This node is part of this plane.
                # Return other significant concepts in this plane (siblings).
                # Exclude the node itself and immediate parents/children if possible to find *lateral* links.
                
                for concept in plane.related_concepts:
                    if concept != start_node:
                        inferences.append(f"In the context of '{plane.anchor_node}', '{start_node}' is related to '{concept}'.")
                        
        return inferences
    
    def get_causes_of(self, node_id: str) -> List[Tuple[CausalNode, CausalLink]]:
        """노드의 원인들 찾기 (역방향 인과 추론)"""
        results = []
        for link_id in self.incoming.get(node_id, []):
            link = self.links[link_id]
            if link.relation in [CausalRelationType.CAUSES, CausalRelationType.ENABLES]:
                source_node = self.nodes.get(link.source_id)
                if source_node:
                    results.append((source_node, link))
        return results
    
    def get_effects_of(self, node_id: str) -> List[Tuple[CausalNode, CausalLink]]:
        """노드의 결과들 찾기 (순방향 인과 추론)"""
        results = []
        for link_id in self.outgoing.get(node_id, []):
            link = self.links[link_id]
            if link.relation in [CausalRelationType.CAUSES, CausalRelationType.ENABLES]:
                target_node = self.nodes.get(link.target_id)
                if target_node:
                    results.append((target_node, link))
        return results
    
    def trace_causal_chain(
        self,
        start_id: str,
        max_depth: int = 5
    ) -> List[CausalChain]:
        """시작 노드부터 가능한 인과 연쇄 추적"""
        chains = []
        
        def dfs(current_id: str, path: List[str], links: List[CausalLink], depth: int):
            if depth >= max_depth:
                if len(path) >= 2:
                    chain = CausalChain(
                        id=f"chain_{len(chains)}",
                        node_sequence=path.copy(),
                        links=links.copy()
                    )
                    chains.append(chain)
                return
            
            for link_id in self.outgoing.get(current_id, []):
                link = self.links[link_id]
                if link.target_id not in path:  # 순환 방지
                    path.append(link.target_id)
                    links.append(link)
                    dfs(link.target_id, path, links, depth + 1)
                    path.pop()
                    links.pop()
            
            # 현재 경로도 체인으로 저장 (말단 노드)
            if len(path) >= 2 and not self.outgoing.get(current_id):
                chain = CausalChain(
                    id=f"chain_{len(chains)}",
                    node_sequence=path.copy(),
                    links=links.copy()
                )
                chains.append(chain)
        
        dfs(start_id, [start_id], [], 0)
        return chains
    
    def find_path(self, source_id: str, target_id: str) -> Optional[CausalChain]:
        """두 노드 사이의 인과 경로 찾기 (BFS)"""
        if source_id not in self.nodes or target_id not in self.nodes:
            return None
        
        visited = {source_id}
        queue = [(source_id, [source_id], [])]
        
        while queue:
            current_id, path, links = queue.pop(0)
            
            if current_id == target_id:
                return CausalChain(
                    id=f"path_{source_id}_to_{target_id}",
                    node_sequence=path,
                    links=links
                )
            
            for link_id in self.outgoing.get(current_id, []):
                link = self.links[link_id]
                if link.target_id not in visited:
                    visited.add(link.target_id)
                    queue.append((
                        link.target_id,
                        path + [link.target_id],
                        links + [link]
                    ))
        
        return None
    
    def counterfactual_query(
        self,
        premise_node_id: str,
        premise_negated: bool,
        conclusion_node_id: str
    ) -> Tuple[bool, str]:
        """
        반사실적 질문
        
        "만약 A가 (아니었다면/있었다면) B는 어떻게 되었을까?"
        
        Args:
            premise_node_id: 전제 노드
            premise_negated: True이면 "없었다면", False이면 "있었다면"
            conclusion_node_id: 결론 노드
        
        Returns:
            (결과, 설명)
        """
        # A → B 경로가 있는지 확인
        path = self.find_path(premise_node_id, conclusion_node_id)
        
        if path is None:
            return (False, f"{premise_node_id}와 {conclusion_node_id} 사이에 인과 관계 없음")
        
        # 인과 연결 강도 계산
        total_strength = 1.0
        for link in path.links:
            total_strength *= link.strength
        
        if premise_negated:
            # "없었다면" → 결과도 없었을 것
            if total_strength > 0.7:
                return (True, f"만약 {premise_node_id}가 없었다면, {conclusion_node_id}도 없었을 것 (확신도: {total_strength:.0%})")
            else:
                return (False, f"{premise_node_id}가 없어도 {conclusion_node_id}는 다른 경로로 발생했을 수 있음")
        else:
            # "있었다면" → 결과가 있었을 것
            if total_strength > 0.5:
                return (True, f"만약 {premise_node_id}가 있었다면, {conclusion_node_id}도 있었을 것 (확신도: {total_strength:.0%})")
            else:
                return (False, f"{premise_node_id}만으로는 {conclusion_node_id}를 보장할 수 없음")


# ============================================================================
# 인과적 경험 (Causal Experience)
# ============================================================================

@dataclass
class CausalExperience:
    """
    인과적 경험 - 실제로 경험한 인과 연쇄
    
    이것이 학습의 기본 단위입니다.
    """
    
    id: str
    timestamp: float
    
    # 경험한 인과 연쇄
    cause_node: CausalNode         # 원인/시작 상태
    effect_node: CausalNode        # 결과/끝 상태
    intermediate_nodes: List[CausalNode] = field(default_factory=list)  # 중간 상태들
    
    # 행위자
    agent_id: str = ""
    
    # 결과
    success: bool = True           # 목표 달성 여부
    emotional_outcome: float = 0.0  # 감정적 결과 (-1 ~ +1)
    
    # 반사실적 사고
    counterfactual_considered: bool = False
    alternative_action: Optional[str] = None
    
    def get_full_sequence(self) -> List[CausalNode]:
        """전체 노드 시퀀스"""
        return [self.cause_node] + self.intermediate_nodes + [self.effect_node]


# ============================================================================
# 인과적 서사 엔진 (Causal Narrative Engine)
# ============================================================================

class CausalNarrativeEngine:
    """
    인과적 서사 엔진
    
    사건을 통한 관계적 의미의 개념 창발과 학습을 구조적으로 지원.
    단순 노드 연결이 아닌, "왜"와 "어떻게"의 인과 구조를 학습.
    
    핵심 원리:
    1. 경험 기반 학습 (Experience-Based Learning)
       - 인과 연쇄를 경험하면 해당 관계가 강화됨
    
    2. 반사실적 추론 (Counterfactual Reasoning)
       - "만약 ~했다면"을 통해 인과 관계 검증
    
    3. 목표 지향적 계획 (Goal-Directed Planning)
       - 원하는 결과를 위한 원인 탐색
    
    4. 감정적 학습 (Emotional Learning)
       - 긍정/부정 결과가 인과 강도에 영향
    """
    
    def __init__(self):
        self.knowledge_base = CausalKnowledgeBase()
        
        # 경험 기록
        self.experiences: List[CausalExperience] = []
        
        # 학습 통계
        self.total_experiences = 0
        self.successful_predictions = 0
        self.failed_predictions = 0
        
        # 기본 인과 스키마 초기화
        self._initialize_fundamental_causality()
    def synthesize_narrative(self, chain: CausalChain) -> str:
        """
        Synthesizes a narrative paragraph from a CausalChain.
        Transform a list of nodes and links into a coherent story.
        """
        if not chain.node_sequence:
            return "Nothing happened."

        narrative = []
        
        # Start
        start_node = chain.node_sequence[0]
        narrative.append(f"It started with {start_node}.")
        
        # Process links
        for i, link in enumerate(chain.links):
            source = link.source_id
            target = link.target_id
            relation = link.relation
            
            # Transition logic based on relation
            transition = ""
            if relation == CausalRelationType.CAUSES:
                transition = "This caused"
            elif relation == CausalRelationType.ENABLES:
                transition = "This enabled"
            elif relation == CausalRelationType.PREVENTS:
                transition = "However, this prevented"
            elif relation == CausalRelationType.CONDITIONAL:
                transition = "Under these conditions,"
            else:
                transition = "Then,"
            
            # Add sentence
            # "This caused [Target]." or "Then, [Target] happened."
            sentence = f"{transition} {target}."
            narrative.append(sentence)
            
        # Conclusion
        narrative.append(f"Finally, the chain completed at {chain.node_sequence[-1]}.")
        
        return " ".join(narrative)

    def generate_prediction_sentence(self, source: str, target: str) -> str:
        """
        Generates a natural language prediction.
        "If [source]..., then [target]..."
        """
        # Simple template for now
        templates = [
            f"If I encounter '{source}', I expect to see '{target}'.",
            f"'{source}' is likely a precursor to '{target}'.",
            f"Given '{source}', '{target}' should follow.",
            f"The presence of '{source}' suggests '{target}' is near."
        ]
        return random.choice(templates)

    def _initialize_fundamental_causality(self):
        """기본적인 인과 스키마 초기화"""
        # 생존 관련 기본 인과
        fundamental_causality = [
            # 물리적 인과
            ("fire_contact", "pain", CausalRelationType.CAUSES, "불에 닿으면 아프다"),
            ("pain", "avoidance", CausalRelationType.CAUSES, "아프면 피하게 된다"),
            ("avoidance", "safety", CausalRelationType.CAUSES, "피하면 안전해진다"),
            
            # 생존 관련
            ("hunger", "seek_food", CausalRelationType.CAUSES, "배고프면 음식을 찾는다"),
            ("seek_food", "find_food", CausalRelationType.ENABLES, "음식을 찾으면 발견할 수 있다"),
            ("find_food", "eat", CausalRelationType.ENABLES, "음식을 발견하면 먹을 수 있다"),
            ("eat", "satiety", CausalRelationType.CAUSES, "먹으면 배부르다"),
            ("satiety", "pleasure", CausalRelationType.CAUSES, "배부르면 기분이 좋다"),
            
            # 사회적 인과
            ("loneliness", "seek_company", CausalRelationType.CAUSES, "외로우면 함께할 사람을 찾는다"),
            ("company", "comfort", CausalRelationType.CAUSES, "함께하면 위로가 된다"),
            ("help_given", "trust", CausalRelationType.CAUSES, "도움을 주면 신뢰가 생긴다"),
            ("trust", "cooperation", CausalRelationType.ENABLES, "신뢰가 있으면 협력할 수 있다"),
            
            # 학습 관련
            ("curiosity", "exploration", CausalRelationType.CAUSES, "호기심이 있으면 탐구한다"),
            ("exploration", "discovery", CausalRelationType.ENABLES, "탐구하면 발견할 수 있다"),
            ("discovery", "knowledge", CausalRelationType.CAUSES, "발견하면 지식이 생긴다"),
            ("knowledge", "prediction", CausalRelationType.ENABLES, "지식이 있으면 예측할 수 있다"),
            
            # 목적론적 인과
            ("goal", "planning", CausalRelationType.CAUSES, "목표가 있으면 계획한다"),
            ("planning", "action", CausalRelationType.ENABLES, "계획이 있으면 행동할 수 있다"),
            ("action", "outcome", CausalRelationType.CAUSES, "행동하면 결과가 있다"),
        ]
        
        for source, target, relation, description in fundamental_causality:
            # 노드 생성
            if source not in self.knowledge_base.nodes:
                self.knowledge_base.add_node(CausalNode(
                    id=source,
                    description=source.replace("_", " "),
                    is_state=True
                ))
            if target not in self.knowledge_base.nodes:
                self.knowledge_base.add_node(CausalNode(
                    id=target,
                    description=target.replace("_", " "),
                    is_state=True
                ))
            
            # 인과 연결 생성
            self.knowledge_base.add_link(
                source, target, relation,
                strength=0.5,  # 기본 강도 (경험으로 강화됨)
                description=description
            )
            
        # Seed Experiential Contexts (User Request: Winter -> Hunger/Loneliness)
        self._initialize_experiential_context()

    def _initialize_experiential_context(self):
        """
        Initializes experiential contexts that link disparate concepts through the 'Self'.
        (e.g., Winter -> Hunger, Cold, Loneliness)
        """
        # Simulating a pre-existing experiential plane for "Winter"
        # This allows the system to infer "Hunger" or "Loneliness" from "Winter" 
        # even without a direct physical causal chain, based on 'lived experience'.
        
        winter_plane = ContextPlane(
            id="plane_winter_experiential",
            anchor_node="winter",
            component_chains=[], 
            related_concepts={"winter", "cold", "hunger", "loneliness", "darkness", "need_for_comfort"}
        )
        self.knowledge_base.planes.append(winter_plane)

    def add_node(self, node: CausalNode):
        return self.knowledge_base.add_node(node)
        
    def add_link(self, *args, **kwargs):
        return self.knowledge_base.add_link(*args, **kwargs)

    @property
    def chains(self):
        return self.knowledge_base.chains

    @property
    def planes(self):
        return self.knowledge_base.planes

    def trace_causal_chain(self, start_id: str, max_depth: int = 5) -> List[CausalChain]:
        return self.knowledge_base.trace_causal_chain(start_id, max_depth)

    def detect_intersections(self, chain: CausalChain) -> List[ContextPlane]:
        return self.knowledge_base.detect_intersections(chain)

    def infer_contextual_link(self, start_node: str) -> List[str]:
        return self.knowledge_base.infer_contextual_link(start_node)

    def calculate_resonance(self, node_id_a: str, node_id_b: str) -> float:
        return self.knowledge_base.calculate_resonance(node_id_a, node_id_b)

    def find_resonant_nodes(self, target_node_id: str, threshold: float = 0.6) -> List[Tuple[str, float]]:
        return self.knowledge_base.find_resonant_nodes(target_node_id, threshold)

    def find_path(self, source_id: str, target_id: str) -> Optional[CausalChain]:
        return self.knowledge_base.find_path(source_id, target_id)

    def experience_causality(
        self,
        cause_description: str,
        effect_description: str,
        relation: CausalRelationType = CausalRelationType.CAUSES,
        emotional_outcome: float = 0.0,
        success: bool = True,
        agent_id: str = "self"
    ) -> CausalExperience:
        """
        인과 관계 경험 (학습의 기본 단위)
        
        Args:
            cause_description: 원인 설명
            effect_description: 결과 설명
            relation: 인과 관계 유형
            emotional_outcome: 감정적 결과 (-1 ~ +1)
            success: 기대한 결과인지 여부
            agent_id: 경험 주체
        
        Returns:
            생성된 CausalExperience
        """
        # 노드 생성 또는 업데이트
        cause_id = cause_description.lower().replace(" ", "_")
        effect_id = effect_description.lower().replace(" ", "_")
        
        cause_node = self.knowledge_base.add_node(CausalNode(
            id=cause_id,
            description=cause_description,
            is_state=False,  # 사건
            agent=agent_id,
            timestamp=time.time()
        ))
        
        effect_node = self.knowledge_base.add_node(CausalNode(
            id=effect_id,
            description=effect_description,
            is_state=True,  # 상태
            emotional_valence=emotional_outcome,
            agent=agent_id,
            timestamp=time.time()
        ))
        
        # 인과 연결 강화
        link = self.knowledge_base.add_link(
            cause_id, effect_id, relation,
            description=f"{cause_description} → {effect_description}"
        )
        
        # 결과에 따른 강도 조정
        if success and emotional_outcome > 0:
            link.strengthen(0.2)  # 긍정적 결과 = 강한 강화
        elif not success or emotional_outcome < 0:
            link.weaken(0.1)  # 부정적 결과 = 약한 약화
        
        # 경험 기록
        experience = CausalExperience(
            id=f"exp_{self.total_experiences}",
            timestamp=time.time(),
            cause_node=cause_node,
            effect_node=effect_node,
            agent_id=agent_id,
            success=success,
            emotional_outcome=emotional_outcome
        )
        
        self.experiences.append(experience)
        self.total_experiences += 1
        
        logger.debug(f"경험: {cause_description} → {effect_description} "
                    f"(감정: {emotional_outcome:.1f}, 성공: {success})")
        
        return experience
    
    def experience_chain(
        self,
        descriptions: List[str],
        emotional_arc: List[float],
        agent_id: str = "self"
    ) -> CausalChain:
        """
        인과 연쇄 경험 (여러 단계의 인과 관계)
        
        Args:
            descriptions: 각 단계의 설명 리스트
            emotional_arc: 각 단계의 감정 리스트
            agent_id: 경험 주체
        
        Returns:
            생성된 CausalChain
        """
        if len(descriptions) < 2:
            raise ValueError("인과 연쇄는 최소 2단계 필요")
        
        if len(emotional_arc) != len(descriptions):
            emotional_arc = [0.0] * len(descriptions)
        
        # 각 연속된 쌍에 대해 경험
        nodes = []
        links = []
        
        for i in range(len(descriptions) - 1):
            exp = self.experience_causality(
                cause_description=descriptions[i],
                effect_description=descriptions[i + 1],
                emotional_outcome=emotional_arc[i + 1],
                agent_id=agent_id
            )
            nodes.append(exp.cause_node.id)
            
            if i == len(descriptions) - 2:
                nodes.append(exp.effect_node.id)
        
        # 연쇄 생성
        chain = CausalChain(
            id=f"chain_{len(self.knowledge_base.chains)}",
            name=f"{descriptions[0]} → {descriptions[-1]}",
            node_sequence=nodes,
            initial_state=nodes[0],
            final_state=nodes[-1],
            emotional_arc=emotional_arc
        )
        
        self.knowledge_base.chains[chain.id] = chain
        
        logger.info(f"인과 연쇄 학습: {chain.name} ({len(nodes)}단계)")
        
        return chain
    
    def predict_effect(
        self,
        cause_description: str
    ) -> List[Tuple[str, float, CausalRelationType]]:
        """
        원인으로부터 결과 예측
        
        Args:
            cause_description: 원인 설명
        
        Returns:
            [(결과 설명, 확률, 관계 유형), ...]
        """
        cause_id = cause_description.lower().replace(" ", "_")
        
        if cause_id not in self.knowledge_base.nodes:
            return []
        
        effects = self.knowledge_base.get_effects_of(cause_id)
        
        predictions = []
        for effect_node, link in effects:
            predictions.append((
                effect_node.description,
                link.strength * link.confidence,
                link.relation
            ))
        
        predictions.sort(key=lambda x: -x[1])
        return predictions
    
    def find_cause(
        self,
        effect_description: str
    ) -> List[Tuple[str, float, CausalRelationType]]:
        """
        결과로부터 원인 추론 (역방향 인과 추론)
        
        Args:
            effect_description: 결과 설명
        
        Returns:
            [(원인 설명, 확률, 관계 유형), ...]
        """
        effect_id = effect_description.lower().replace(" ", "_")
        
        if effect_id not in self.knowledge_base.nodes:
            return []
        
        causes = self.knowledge_base.get_causes_of(effect_id)
        
        inferences = []
        for cause_node, link in causes:
            inferences.append((
                cause_node.description,
                link.strength * link.confidence,
                link.relation
            ))
        
        inferences.sort(key=lambda x: -x[1])
        return inferences
    
    def plan_to_achieve(
        self,
        current_state: str,
        goal_state: str
    ) -> Optional[CausalChain]:
        """
        목표 달성을 위한 계획 (인과 경로 탐색)
        
        Args:
            current_state: 현재 상태
            goal_state: 목표 상태
        
        Returns:
            인과 연쇄 (계획) 또는 None
        """
        current_id = current_state.lower().replace(" ", "_")
        goal_id = goal_state.lower().replace(" ", "_")
        
        return self.knowledge_base.find_path(current_id, goal_id)
    
    def counterfactual_reasoning(
        self,
        premise: str,
        premise_negated: bool,
        conclusion: str
    ) -> Tuple[bool, str]:
        """
        반사실적 추론
        
        "만약 ~했다면/하지 않았다면, ~했을까?"
        
        Args:
            premise: 전제
            premise_negated: True이면 "하지 않았다면"
            conclusion: 결론
        
        Returns:
            (결과, 설명)
        """
        premise_id = premise.lower().replace(" ", "_")
        conclusion_id = conclusion.lower().replace(" ", "_")
        
        return self.knowledge_base.counterfactual_query(
            premise_id, premise_negated, conclusion_id
        )
    
    def explain_why(self, state: str, depth: int = 3) -> List[str]:
        """
        "왜?"에 대한 설명 생성
        
        Args:
            state: 설명이 필요한 상태
            depth: 인과 추적 깊이
        
        Returns:
            설명 리스트
        """
        state_id = state.lower().replace(" ", "_")
        
        if state_id not in self.knowledge_base.nodes:
            return [f"'{state}'에 대한 인과 지식이 없습니다."]
        
        explanations = []
        
        def trace_back(node_id: str, current_depth: int, path: List[str]):
            if current_depth >= depth:
                return
            
            causes = self.knowledge_base.get_causes_of(node_id)
            for cause_node, link in causes:
                # 설명 생성
                cause_desc = cause_node.description
                effect_desc = self.knowledge_base.nodes[node_id].description
                
                explanation = f"{effect_desc}인 이유는 {cause_desc} {link.get_description()}"
                if explanation not in explanations:
                    explanations.append(explanation)
                
                # 더 깊이 추적
                if cause_node.id not in path:
                    trace_back(cause_node.id, current_depth + 1, path + [cause_node.id])
        
        trace_back(state_id, 0, [state_id])
        
        return explanations if explanations else [f"'{state}'의 원인을 알 수 없습니다."]
    
    def get_statistics(self) -> Dict[str, Any]:
        """학습 통계"""
        return {
            "total_nodes": len(self.knowledge_base.nodes),
            "total_links": len(self.knowledge_base.links),
            "total_chains": len(self.knowledge_base.chains),
            "total_experiences": self.total_experiences,
            "avg_link_strength": np.mean([
                l.strength for l in self.knowledge_base.links.values()
            ]) if self.knowledge_base.links else 0,
        }
    
    def get_strongest_causalities(self, n: int = 10) -> List[Tuple[str, str, float]]:
        """가장 강한 인과 관계들"""
        causalities = [
            (link.source_id, link.target_id, link.strength)
            for link in self.knowledge_base.links.values()
        ]
        causalities.sort(key=lambda x: -x[2])
        return causalities[:n]


# ============================================================================
# 사고우주 (Thought Universe) - 차원 계층 관리 및 상호 교정
# ============================================================================

class ThoughtUniverse:
    """
    사고우주 (Thought Universe)
    
    점 → 선 → 면 → 공간 → 법칙으로 확장되는 지식 구조를 관리하고,
    각 요소들이 서로 교정하고 보완하는 시스템.
    
    핵심 원리:
    1. 차원 확장 (Dimensional Expansion)
       - 경험이 축적되면 상위 차원으로 추상화
       - 점들의 관계가 선이 되고, 선들의 교차가 면이 됨
    
    2. 상호 교정 (Mutual Correction)
       - 상향 교정: 새 경험이 기존 지식을 수정
       - 하향 교정: 상위 법칙이 하위 개념을 조정
       - 수평 교정: 동일 레벨 요소들이 서로 조정
    
    3. 일관성 유지 (Consistency Maintenance)
       - 모순 탐지 및 해결
       - 신뢰도 기반 우선순위
    """
    
    def __init__(self, name: str = "Elysia's Mind"):
        self.name = name
        
        # 차원별 저장소
        self.points: Dict[str, ConceptPoint] = {}
        self.lines: Dict[str, CausalLine] = {}
        self.planes: Dict[str, ContextPlane] = {}
        self.spaces: Dict[str, SchemaSpace] = {}
        self.laws: Dict[str, UniversalLaw] = {}
        
        # 인식론적 공간 (Epistemic Spaces - Fractal Worlds)
        self.epistemic_spaces: Dict[str, EpistemicSpace] = {}

        # 전체 요소 인덱스 (빠른 검색용)
        self.all_entities: Dict[str, DimensionalEntity] = {}
        
        # 교정 이력
        self.correction_history: List[Dict[str, Any]] = []
        
        # 학습 통계
        self.total_points = 0
        self.total_lines = 0
        self.total_planes = 0
        self.total_spaces = 0
        self.total_laws = 0
        self.total_corrections = 0
        
        # 인과 엔진 연결
        self.causal_engine = CausalNarrativeEngine()
        
        logger.info(f"🌌 ThoughtUniverse '{name}' initialized")
    
    # ========================================================================
    # 점 (Point) 관리
    # ========================================================================
    
    def add_point(
        self,
        id: str,
        description: str,
        sensory_signature: Dict[str, float] = None,
        emotional_valence: float = 0.0,
        concept_type: str = "general"
    ) -> ConceptPoint:
        """개념 점 추가"""
        point = ConceptPoint(
            id=id,
            level=DimensionLevel.POINT,
            description=description,
            sensory_signature=sensory_signature or {},
            emotional_valence=emotional_valence,
            concept_type=concept_type,
            last_updated=time.time()
        )
        
        self.points[id] = point
        self.all_entities[id] = point
        self.total_points += 1
        
        logger.debug(f"점 추가: {description}")
        return point
    
    def get_or_create_point(self, id: str, description: str = None) -> ConceptPoint:
        """점 가져오기 또는 생성"""
        if id in self.points:
            return self.points[id]
        return self.add_point(id, description or id)
    
    # ========================================================================
    # 선 (Line) 관리 - 두 점을 연결
    # ========================================================================
    
    def add_line(
        self,
        source_id: str,
        target_id: str,
        relation_type: str = "causes",
        strength: float = 1.0,
        conditions: List[str] = None,
        description: str = ""
    ) -> CausalLine:
        """인과 선 추가 (두 점을 연결)"""
        # 점들이 없으면 생성
        source = self.get_or_create_point(source_id)
        target = self.get_or_create_point(target_id)
        
        line_id = f"{source_id}__{relation_type}__{target_id}"
        
        if line_id in self.lines:
            # 기존 선 강화
            existing = self.lines[line_id]
            existing.strength = min(1.0, existing.strength + 0.1)
            existing.experience_count += 1
            existing.last_updated = time.time()
            return existing
        
        line = CausalLine(
            id=line_id,
            level=DimensionLevel.LINE,
            description=description or f"{source_id} {relation_type} {target_id}",
            source_point_id=source_id,
            target_point_id=target_id,
            relation_type=relation_type,
            strength=strength,
            conditions=conditions or [],
            last_updated=time.time()
        )
        
        # 점들에 자식으로 등록
        line.child_ids = [source_id, target_id]
        source.parent_ids.append(line_id)
        target.parent_ids.append(line_id)
        
        self.lines[line_id] = line
        self.all_entities[line_id] = line
        self.total_lines += 1
        
        logger.debug(f"선 추가: {source_id} → {target_id}")
        return line
    
    # ========================================================================
    # 면 (Plane) 관리 - 여러 선이 교차하는 문맥
    # ========================================================================
    
    def add_plane(
        self,
        id: str,
        description: str,
        line_ids: List[str],
        context_type: str = "situation",
        lesson: str = ""
    ) -> ContextPlane:
        """문맥 면 추가"""
        # 관련된 점들 수집
        point_ids = set()
        for line_id in line_ids:
            if line_id in self.lines:
                line = self.lines[line_id]
                point_ids.add(line.source_point_id)
                point_ids.add(line.target_point_id)
        
        plane = ContextPlane(
            id=id,
            level=DimensionLevel.PLANE,
            description=description,
            line_ids=line_ids,
            point_ids=list(point_ids),
            context_type=context_type,
            lesson=lesson,
            last_updated=time.time()
        )
        
        # 선들의 부모로 등록
        plane.child_ids = line_ids
        for line_id in line_ids:
            if line_id in self.lines:
                self.lines[line_id].parent_ids.append(id)
        
        self.planes[id] = plane
        self.all_entities[id] = plane
        self.total_planes += 1
        
        logger.debug(f"면 추가: {description}")
        return plane
    
    def emerge_plane_from_experience(
        self,
        experience_description: str,
        point_sequence: List[str],
        emotional_arc: List[float] = None
    ) -> ContextPlane:
        """
        경험으로부터 면(문맥) 창발
        
        점들의 시퀀스를 선들로 연결하고, 면으로 통합
        """
        if len(point_sequence) < 2:
            raise ValueError("최소 2개의 점이 필요합니다")
        
        emotional_arc = emotional_arc or [0.0] * len(point_sequence)
        
        # 선들 생성
        line_ids = []
        for i in range(len(point_sequence) - 1):
            line = self.add_line(
                source_id=point_sequence[i],
                target_id=point_sequence[i + 1],
                relation_type="causes"
            )
            line_ids.append(line.id)
        
        # 면 생성
        plane_id = f"plane_{len(self.planes)}_{point_sequence[0]}_{point_sequence[-1]}"
        
        # 감정 궤적에서 교훈 도출
        start_emotion = emotional_arc[0]
        end_emotion = emotional_arc[-1]
        if end_emotion > start_emotion + 0.3:
            lesson = "긍정적 결과를 가져온 경험"
        elif end_emotion < start_emotion - 0.3:
            lesson = "부정적 결과를 가져온 경험"
        else:
            lesson = "중립적 경험"
        
        plane = self.add_plane(
            id=plane_id,
            description=experience_description,
            line_ids=line_ids,
            context_type="experience",
            lesson=lesson
        )
        
        plane.emotional_tone = end_emotion
        
        return plane
    
    # ========================================================================
    # 공간 (Space) 관리 - 여러 면이 교차하는 스키마
    # ========================================================================
    
    def add_space(
        self,
        id: str,
        description: str,
        plane_ids: List[str],
        schema_type: str = "behavior",
        core_patterns: List[str] = None
    ) -> SchemaSpace:
        """스키마 공간 추가"""
        space = SchemaSpace(
            id=id,
            level=DimensionLevel.SPACE,
            description=description,
            plane_ids=plane_ids,
            schema_type=schema_type,
            core_patterns=core_patterns or [],
            last_updated=time.time()
        )
        
        # 면들의 부모로 등록
        space.child_ids = plane_ids
        for plane_id in plane_ids:
            if plane_id in self.planes:
                self.planes[plane_id].parent_ids.append(id)
        
        self.spaces[id] = space
        self.all_entities[id] = space
        self.total_spaces += 1
        
        logger.debug(f"공간 추가: {description}")
        return space
    
    def emerge_space_from_planes(
        self,
        plane_ids: List[str],
        min_common_points: int = 2
    ) -> Optional[SchemaSpace]:
        """
        면들로부터 공간(스키마) 창발
        
        공통 요소가 충분히 있는 면들을 하나의 스키마로 통합
        """
        if len(plane_ids) < 2:
            return None
        
        # 공통 점 찾기
        all_point_sets = []
        for plane_id in plane_ids:
            if plane_id in self.planes:
                all_point_sets.append(set(self.planes[plane_id].point_ids))
        
        if not all_point_sets:
            return None
        
        common_points = all_point_sets[0]
        for point_set in all_point_sets[1:]:
            common_points = common_points.intersection(point_set)
        
        if len(common_points) < min_common_points:
            return None
        
        # 핵심 패턴 도출
        core_patterns = list(common_points)
        
        # 스키마 생성
        space_id = f"schema_{len(self.spaces)}"
        description = f"공통 요소: {', '.join(core_patterns)}"
        
        # ... (Validation would happen here)
        
        return self.add_space(
            id=space_id,
            description=description,
            plane_ids=plane_ids,
            core_patterns=core_patterns
        )

    # ============================================================================
    # Phase 12: Dimensional Fractals (Universal Principles)
    # ============================================================================

    def extract_principle(self, chain: CausalChain, principle_name: str) -> UniversalLaw:
        """
        Abstracts a concrete causal chain into a Universal Law.
        (e.g., "Winter -> Cold -> Hunger" => "AdverseCondition -> Deprivation -> Distress")
        """
        # simplified abstraction: just structural pattern
        abstract_chain = []
        for link in chain.links:
            # Safely handle relation enum or string
            rel_val = link.relation
            if hasattr(link.relation, 'value'):
                 rel_val = link.relation.value
            abstract_chain.append(f"[{rel_val}]")
            
        law_description = f"Principle of {principle_name}: Sequence " + " -> ".join(abstract_chain)
        
        law = UniversalLaw(
            id=f"law_{principle_name.lower()}",
            level=DimensionLevel.LAW,
            description=law_description,
            law_type="fractal_pattern",
            formulation=str(abstract_chain),
            supporting_evidence=[chain.id]
        )
        
        self.laws[law.id] = law
        self.all_entities[law.id] = law
        self.total_laws += 1
        
        logger.info(f"   📜 Law Extracted: {law.description}")
        return law

    # ========================================================================
    # Phase 13: Epistemic Topology (Fractal Knowledge Worlds)
    # ========================================================================

    def expand_node_into_space(
        self, 
        node_id: str, 
        space_name: str,
        density: float = 1.0,
        methodologies: List[str] = None
    ) -> EpistemicSpace:
        """
        Expands a single node (Point) into an entire Epistemic Space (Fractal World).
        
        This transforms a 'concept' into a 'field of study'.
        e.g., Node 'Science' -> EpistemicSpace 'Physics_World'
        """
        # 1. Get the original point/node
        if node_id not in self.points:
            # Create if not exists
            self.get_or_create_point(node_id)
            
        point = self.points[node_id]
        
        # 2. Create the inner space
        space_id = f"space_{node_id}_internal"
        space = EpistemicSpace(
            id=space_id,
            level=DimensionLevel.SPACE,
            description=f"Internal World of {space_name}",
            schema_type="epistemic_field",
            density=density,
            methodologies=methodologies or ["LOGICAL", "EMPIRICAL"]
        )
        
        # 3. Link them (Fractal Connection)
        # Note: We need to update CausalNode definition to support this, 
        # OR we use a mapping in ThoughtUniverse.
        # Assuming we updated CausalNode or ConceptPoint? 
        # ConceptPoint is defined in this file (lines 105-140 range for DimensionalEntity, Point around 150-200)
        # But wait, CausalNarrativeEngine has CausalNode. ThoughtUniverse uses ConceptPoint.
        # Let's map it in ThoughtUniverse for now or use a dynamic attribute.
        
        # Store in our registry
        self.epistemic_spaces[space_id] = space
        self.all_entities[space_id] = space
        
        # Link physically (meta-physically)
        # We'll treat the point as the "Portal" to the space
        point.child_ids.append(space_id)
        space.parent_ids.append(node_id)
        
        logger.info(f"🌌 Expanded Node '{node_id}' into Epistemic Space '{space_name}' (Density: {density})")
        return space

    def traverse_epistemic_field(
        self, 
        agent_id: str, 
        space_id: str, 
        current_knowledge: List[str],
        target_concept: str
    ) -> Dict[str, Any]:
        """
        Simulates the traversal of an agent through a knowledge space.
        
        Movement is not free; it requires overcoming 'density' using 'methodology'.
        """
        if space_id not in self.epistemic_spaces:
            return {"status": "error", "message": "Space not found"}
            
        space = self.epistemic_spaces[space_id]
        
        # 1. Calculate Resistance
        # Resistance = Space Density * (1 - Knowledge Overlap)
        # If you know nothing, resistance is max.
        
        # Simple simulation:
        # Check if agent has prerequisite concepts to 'move' to target.
        # Prereqs are 'intermediate' concepts in this space.
        
        # Let's assume the space contains internal points.
        # We need to populate the space with points first (done via add_point + linkage).
        
        # Find path from current_knowledge (closest node) to target_concept
        # For this simulation, we'll check if target is 'reachable' given density.
        
        resistance = space.density
        
        # Methodology Check
        # Does the agent use the right methodology? (Mock check)
        agent_methodology = "EMPIRICAL" # default for now
        efficiency = 1.0
        if agent_methodology in space.methodologies:
            efficiency = 1.5 # Bonus
            
        effort_required = resistance / efficiency
        
        result = {
            "space": space.id,
            "target": target_concept,
            "resistance": resistance,
            "effort_required": effort_required,
            "status": "traversing",
            "path_log": []
        }
        
        # Simulation of "steps"
        steps = int(effort_required * 5) # Arbitrary scale
        for i in range(steps):
             result["path_log"].append(f"Step {i+1}: Overcoming conceptual density...")
             
        result["status"] = "arrived"
        result["message"] = f"Successfully traversed {space.description} to reach {target_concept}."

        return result
        
    def apply_principle_to_domain(self, law: UniversalLaw, domain_map: Dict[str, str]) -> List[str]:
        """
        Applies a Universal Law to a new domain using a mapping.
        (Fractal Expansion)
        """
        narrative = [f"Applying {law.id} to new domain..."]
        
        import ast
        try:
             relations = ast.literal_eval(law.formulation)
        except:
             # Fallback if formulation isn't list string
             return ["Failed to parse law formulation."]
             
        # Generate the new narrative
        steps = []
        # We need relation count + 1 items
        count = len(relations) + 1
        
        for i in range(count):
             key = f"Step_{i}"
             if key in domain_map:
                 steps.append(domain_map[key])
             else:
                 steps.append("Unknown")
                 
        for i, relation in enumerate(relations):
            if i+1 < len(steps):
                source = steps[i]
                target = steps[i+1]
                narrative.append(f"{source} --({relation})--> {target}")
                
        return narrative

    # ========================================================================
    # Phase 14: Metacognitive Architecture (Self-Evolution)
    # ========================================================================

    def evaluate_maturity(self, concept_id: str) -> Dict[str, Any]:
        """
        Evaluates the maturity of a specific concept against the 'ADULT' standard.
        analysis: "How dense, differentiated, and integrated is my understanding?"
        """
        metrics = CognitiveMetrics(0.2, 0.2, 0.1) # Default CHILD level
        
        if concept_id in self.points:
            point = self.points[concept_id]
            
            # Simple heuristics for simulation
            # Differentiation: Number of child nodes (which represent details or subtypes in this context)
            diff_score = min(0.9, len(point.child_ids) * 0.2)
            
            # Integration: how many parents? (part of larger structures)
            int_score = min(0.9, len(point.parent_ids) * 0.2)
            
            # Abstraction: Is it linked to a Space or Law?
            abs_score = 0.1
            for pid in point.parent_ids:
                if pid.startswith("law_") or pid.startswith("space_"):
                    abs_score += 0.3
            abs_score = min(0.9, abs_score)
            
            metrics = CognitiveMetrics(diff_score, int_score, abs_score)
            
        # Compare with Standard
        standard = MaturityModel.get_standard_model()["ADULT"]
        gap_report = {
            "concept": concept_id,
            "current_metrics": metrics,
            "target_metrics": standard.required_metrics,
            "gaps": {},
            "status": "IMMATURE"
        }
        
        # Calculate gaps
        if metrics.differentiation < standard.required_metrics.differentiation:
            gap_report["gaps"]["differentiation"] = standard.required_metrics.differentiation - metrics.differentiation
        if metrics.integration < standard.required_metrics.integration:
             gap_report["gaps"]["integration"] = standard.required_metrics.integration - metrics.integration
        if metrics.abstraction < standard.required_metrics.abstraction:
             gap_report["gaps"]["abstraction"] = standard.required_metrics.abstraction - metrics.abstraction
             
        if not gap_report["gaps"]:
            gap_report["status"] = "MATURE"
            
        return gap_report

    def formulate_growth_plan(self, gap_report: Dict[str, Any]) -> List[str]:
        """
        Generates 'Intentions' (Tasks) to bridge the identified gaps.
        Autonomously decides *what to do* to become smarter.
        """
        intentions = []
        concept = gap_report["concept"]
        
        if gap_report["status"] == "MATURE":
            return ["Maintain current understanding."]
            
        gaps = gap_report["gaps"]
        
        # 1. Address Differentiation Gap (Too simple?)
        if "differentiation" in gaps:
            val = gaps["differentiation"]
            intentions.append(f"INTENTION: Deepen differentiation of '{concept}'. Explore nuances and subtypes. (Gap: {val:.2f})")
            
        # 2. Address Integration Gap (Disconnected?)
        if "integration" in gaps:
             val = gaps["integration"]
             intentions.append(f"INTENTION: Increase integration of '{concept}'. Connect to wider contexts and other concepts. (Gap: {val:.2f})")
             
        # 3. Address Abstraction Gap (Too concrete?)
        if "abstraction" in gaps:
             val = gaps["abstraction"]
             intentions.append(f"INTENTION: Lift '{concept}' to higher abstraction. Find universal principles or laws it belongs to. (Gap: {val:.2f})")
             
        return intentions

        
        space = self.add_space(
            id=space_id,
            description=description,
            plane_ids=plane_ids,
            schema_type="emergent",
            core_patterns=core_patterns
        )
        
        return space
    
    # ========================================================================
    # 법칙 (Law) 관리 - 공간을 관통하는 보편적 원리
    # ========================================================================
    
    def add_law(
        self,
        id: str,
        description: str,
        space_ids: List[str],
        formulation: str = "",
        law_type: str = "causal"
    ) -> UniversalLaw:
        """보편적 법칙 추가"""
        law = UniversalLaw(
            id=id,
            level=DimensionLevel.LAW,
            description=description,
            space_ids=space_ids,
            formulation=formulation,
            law_type=law_type,
            last_updated=time.time()
        )
        
        # 공간들의 부모로 등록
        law.child_ids = space_ids
        for space_id in space_ids:
            if space_id in self.spaces:
                self.spaces[space_id].parent_ids.append(id)
        
        self.laws[id] = law
        self.all_entities[id] = law
        self.total_laws += 1
        
        logger.info(f"⚖️ 법칙 발견: {description}")
        return law
    
    def discover_law_from_spaces(
        self,
        space_ids: List[str],
        confidence_threshold: float = 0.8
    ) -> Optional[UniversalLaw]:
        """
        공간들로부터 법칙 발견
        
        여러 스키마에서 공통으로 나타나는 패턴을 법칙으로 승격
        """
        if len(space_ids) < 2:
            return None
        
        # 공통 패턴 찾기
        all_pattern_sets = []
        for space_id in space_ids:
            if space_id in self.spaces:
                all_pattern_sets.append(set(self.spaces[space_id].core_patterns))
        
        if not all_pattern_sets:
            return None
        
        common_patterns = all_pattern_sets[0]
        for pattern_set in all_pattern_sets[1:]:
            common_patterns = common_patterns.intersection(pattern_set)
        
        if not common_patterns:
            return None
        
        # 법칙 생성
        law_id = f"law_{len(self.laws)}"
        formulation = " ∧ ".join(common_patterns)  # 논리곱 형태
        
        law = self.add_law(
            id=law_id,
            description=f"보편적 원리: {formulation}",
            space_ids=space_ids,
            formulation=formulation,
            law_type="emergent"
        )
        
        return law
    
    # ========================================================================
    # 상호 교정 (Mutual Correction)
    # ========================================================================
    
    def bottom_up_correct(
        self,
        new_experience: Dict[str, Any],
        affected_entity_id: str
    ) -> Dict[str, Any]:
        """
        상향 교정: 새로운 경험이 기존 지식을 수정
        
        예: "불은 항상 뜨겁다" → "꺼진 불은 안 뜨겁다" (반례 학습)
        """
        if affected_entity_id not in self.all_entities:
            return {"success": False, "reason": "entity not found"}
        
        entity = self.all_entities[affected_entity_id]
        
        correction = {
            "type": "bottom_up",
            "timestamp": time.time(),
            "entity_id": affected_entity_id,
            "before": entity.confidence,
            "experience": new_experience,
        }
        
        # 새 경험이 기존 지식과 일치하는지 확인
        is_consistent = new_experience.get("confirms", True)
        
        if is_consistent:
            # 일관된 경험 → 신뢰도 증가
            entity.confidence = min(1.0, entity.confidence + 0.05)
            entity.experience_count += 1
            correction["action"] = "strengthen"
        else:
            # 반례 → 신뢰도 감소 및 예외 기록
            entity.confidence = max(0.0, entity.confidence - 0.1)
            exception = new_experience.get("exception", "")
            if isinstance(entity, CausalLine) and exception:
                entity.exceptions.append(exception)
            correction["action"] = "weaken"
        
        correction["after"] = entity.confidence
        entity.corrections.append(correction)
        entity.last_updated = time.time()
        
        self.correction_history.append(correction)
        self.total_corrections += 1
        
        return correction
    
    def top_down_correct(
        self,
        law_id: str,
        target_entity_id: str
    ) -> Dict[str, Any]:
        """
        하향 교정: 상위 법칙이 하위 개념을 조정
        
        예: "에너지 보존" 법칙이 "불의 열" 개념을 정교화
        """
        if law_id not in self.laws:
            return {"success": False, "reason": "law not found"}
        if target_entity_id not in self.all_entities:
            return {"success": False, "reason": "target not found"}
        
        law = self.laws[law_id]
        target = self.all_entities[target_entity_id]
        
        correction = {
            "type": "top_down",
            "timestamp": time.time(),
            "law_id": law_id,
            "target_id": target_entity_id,
            "before": target.confidence,
        }
        
        # 법칙과의 일관성 확인
        is_consistent = self._check_consistency_with_law(law, target)
        
        if is_consistent:
            # 일관성 있음 → 법칙의 증거로 등록
            law.supporting_evidence.append(target_entity_id)
            correction["action"] = "confirmed"
        else:
            # 불일치 → 하위 요소 조정 또는 법칙에 반례 기록
            if target.confidence < law.confidence:
                # 하위 요소가 덜 확실 → 하위 조정
                target.confidence *= 0.9
                correction["action"] = "adjusted_down"
            else:
                # 법칙이 덜 확실 → 반례 기록
                law.counter_examples.append(target_entity_id)
                correction["action"] = "counter_example"
        
        correction["after"] = target.confidence
        target.corrections.append(correction)
        target.last_updated = time.time()
        
        self.correction_history.append(correction)
        self.total_corrections += 1
        
        return correction
    
    def lateral_correct(
        self,
        entity_id_1: str,
        entity_id_2: str
    ) -> Dict[str, Any]:
        """
        수평 교정: 동일 레벨의 요소들이 서로 조정
        
        예: "뜨거움"과 "차가움"이 서로의 경계를 정의
        """
        if entity_id_1 not in self.all_entities:
            return {"success": False, "reason": "entity 1 not found"}
        if entity_id_2 not in self.all_entities:
            return {"success": False, "reason": "entity 2 not found"}
        
        entity_1 = self.all_entities[entity_id_1]
        entity_2 = self.all_entities[entity_id_2]
        
        # 동일 레벨인지 확인
        if entity_1.level != entity_2.level:
            return {"success": False, "reason": "different levels"}
        
        correction = {
            "type": "lateral",
            "timestamp": time.time(),
            "entity_1": entity_id_1,
            "entity_2": entity_id_2,
        }
        
        # 점(Point)의 경우: 감각 서명 대비
        if entity_1.level == DimensionLevel.POINT:
            p1, p2 = entity_1, entity_2
            if isinstance(p1, ConceptPoint) and isinstance(p2, ConceptPoint):
                # 반대 개념 관계 파악 (예: 뜨거움 ↔ 차가움)
                overlap = self._calculate_sensory_overlap(
                    p1.sensory_signature,
                    p2.sensory_signature
                )
                if overlap < -0.5:
                    # 반대 개념 → 서로를 정의
                    correction["relation"] = "opposites"
                elif overlap > 0.5:
                    # 유사 개념 → 구분 필요
                    correction["relation"] = "similar"
                else:
                    correction["relation"] = "independent"
        
        self.correction_history.append(correction)
        self.total_corrections += 1
        
        return correction
    
    def _check_consistency_with_law(
        self,
        law: UniversalLaw,
        entity: DimensionalEntity
    ) -> bool:
        """법칙과의 일관성 확인"""
        # 간단한 구현: 핵심 패턴 포함 여부
        if not law.formulation:
            return True
        
        # 점(Point)의 경우
        if isinstance(entity, ConceptPoint):
            return entity.id in law.formulation or entity.description in law.formulation
        
        # 선(Line)의 경우
        if isinstance(entity, CausalLine):
            return (entity.source_point_id in law.formulation or
                    entity.target_point_id in law.formulation)
        
        return True
    
    def _calculate_sensory_overlap(
        self,
        sig1: Dict[str, float],
        sig2: Dict[str, float]
    ) -> float:
        """두 감각 서명의 중첩도 (-1 ~ +1)"""
        common_keys = set(sig1.keys()) & set(sig2.keys())
        if not common_keys:
            return 0.0
        
        total = 0.0
        for key in common_keys:
            # 같은 부호이면 양, 다른 부호이면 음
            total += sig1[key] * sig2[key]
        
        return total / len(common_keys)
    
    # ========================================================================
    # 통합 학습 인터페이스
    # ========================================================================
    
    def learn_from_experience(
        self,
        experience_steps: List[str],
        emotional_arc: List[float] = None,
        auto_emergence: bool = True
    ) -> Dict[str, Any]:
        """
        경험으로부터 통합 학습
        
        1. 점들 생성/강화
        2. 선들 생성 (인과 관계)
        3. 면 창발 (문맥)
        4. 필요시 공간/법칙 창발
        
        Args:
            experience_steps: 경험 단계들
            emotional_arc: 각 단계의 감정
            auto_emergence: 상위 차원 자동 창발 여부
        
        Returns:
            학습 결과 요약
        """
        result = {
            "points_created": 0,
            "lines_created": 0,
            "plane_created": None,
            "space_emerged": None,
            "law_discovered": None,
        }
        
        # 1. 점들 생성/강화
        for step in experience_steps:
            point_id = step.lower().replace(" ", "_")
            if point_id not in self.points:
                self.add_point(point_id, step)
                result["points_created"] += 1
        
        # 2. 면 창발 (선들 자동 생성)
        point_ids = [s.lower().replace(" ", "_") for s in experience_steps]
        plane = self.emerge_plane_from_experience(
            experience_description=" → ".join(experience_steps),
            point_sequence=point_ids,
            emotional_arc=emotional_arc
        )
        result["plane_created"] = plane.id
        result["lines_created"] = len(plane.line_ids)
        
        # 3. 상위 차원 자동 창발
        if auto_emergence:
            # 유사한 면들 찾기
            similar_planes = self._find_similar_planes(plane, threshold=0.5)
            if len(similar_planes) >= 2:
                space = self.emerge_space_from_planes(
                    [plane.id] + similar_planes
                )
                if space:
                    result["space_emerged"] = space.id
                    
                    # 유사한 공간들에서 법칙 발견
                    similar_spaces = self._find_similar_spaces(space, threshold=0.7)
                    if len(similar_spaces) >= 2:
                        law = self.discover_law_from_spaces(
                            [space.id] + similar_spaces
                        )
                        if law:
                            result["law_discovered"] = law.id
        
        return result
    
    def _find_similar_planes(
        self,
        target_plane: ContextPlane,
        threshold: float = 0.5
    ) -> List[str]:
        """유사한 면 찾기 (공통 점 비율 기준)"""
        similar = []
        target_points = set(target_plane.point_ids)
        
        for plane_id, plane in self.planes.items():
            if plane_id == target_plane.id:
                continue
            
            plane_points = set(plane.point_ids)
            if not plane_points:
                continue
            
            overlap = len(target_points & plane_points) / len(target_points | plane_points)
            if overlap >= threshold:
                similar.append(plane_id)
        
        return similar
    
    def _find_similar_spaces(
        self,
        target_space: SchemaSpace,
        threshold: float = 0.7
    ) -> List[str]:
        """유사한 공간 찾기 (공통 패턴 비율 기준)"""
        similar = []
        target_patterns = set(target_space.core_patterns)
        
        for space_id, space in self.spaces.items():
            if space_id == target_space.id:
                continue
            
            space_patterns = set(space.core_patterns)
            if not space_patterns:
                continue
            
            overlap = len(target_patterns & space_patterns) / len(target_patterns | space_patterns)
            if overlap >= threshold:
                similar.append(space_id)
        
        return similar
    
    # ========================================================================
    # 조회 및 통계
    # ========================================================================
    
    def get_statistics(self) -> Dict[str, Any]:
        """사고우주 통계"""
        return {
            "name": self.name,
            "total_points": self.total_points,
            "total_lines": self.total_lines,
            "total_planes": self.total_planes,
            "total_spaces": self.total_spaces,
            "total_laws": self.total_laws,
            "total_corrections": self.total_corrections,
            "dimension_breakdown": {
                "점(Point)": self.total_points,
                "선(Line)": self.total_lines,
                "면(Plane)": self.total_planes,
                "공간(Space)": self.total_spaces,
                "법칙(Law)": self.total_laws,
            }
        }
    
    def visualize_hierarchy(self, max_items: int = 5) -> str:
        """차원 계층 시각화"""
        lines = [
            f"🌌 사고우주: {self.name}",
            "=" * 50,
            "",
            "⚖️ 법칙 (Law) - 보편적 원리",
            "-" * 30,
        ]
        
        for law_id in list(self.laws.keys())[:max_items]:
            law = self.laws[law_id]
            lines.append(f"  • {law.description}")
        
        lines.extend([
            "",
            "📦 공간 (Space) - 세계관/스키마",
            "-" * 30,
        ])
        
        for space_id in list(self.spaces.keys())[:max_items]:
            space = self.spaces[space_id]
            lines.append(f"  • {space.description}")
        
        lines.extend([
            "",
            "📄 면 (Plane) - 문맥/맥락",
            "-" * 30,
        ])
        
        for plane_id in list(self.planes.keys())[:max_items]:
            plane = self.planes[plane_id]
            lines.append(f"  • {plane.description[:50]}...")
        
        lines.extend([
            "",
            "━━ 선 (Line) - 인과 관계",
            "-" * 30,
        ])
        
        for line_id in list(self.lines.keys())[:max_items]:
            line = self.lines[line_id]
            lines.append(f"  • {line.source_point_id} → {line.target_point_id}")
        
        lines.extend([
            "",
            "• 점 (Point) - 개념 노드",
            "-" * 30,
        ])
        
        for point_id in list(self.points.keys())[:max_items]:
            point = self.points[point_id]
            lines.append(f"  • {point.description}")
        
        return "\n".join(lines)


# ============================================================================
# Demo
# ============================================================================

def demo():
    """인과적 서사 엔진 데모"""
    print("=" * 70)
    print("Causal Narrative Engine - 인과적 서사 엔진")
    print("=" * 70)
    print()
    print("사건을 통한 관계적 의미의 개념 창발과 학습")
    print("단순 노드 연결이 아닌, '왜'와 '어떻게'의 인과 구조")
    print()
    
    engine = CausalNarrativeEngine()
    
    # 1. 경험 기반 학습
    print("-" * 70)
    print("1. 경험 기반 학습")
    print("-" * 70)
    
    # 불에 데인 경험
    engine.experience_chain(
        descriptions=["불에 손을 댔다", "뜨거움을 느꼈다", "손을 뺐다", "안전해졌다"],
        emotional_arc=[0.0, -0.8, -0.3, 0.5],
        agent_id="아이"
    )
    print("  ✓ 불에 데인 경험 학습")
    
    # 배고픔 해결 경험
    engine.experience_chain(
        descriptions=["배가 고팠다", "음식을 찾았다", "먹었다", "배가 불렀다"],
        emotional_arc=[-0.5, 0.0, 0.5, 0.9],
        agent_id="아이"
    )
    print("  ✓ 배고픔 해결 경험 학습")
    
    # 2. 결과 예측
    print()
    print("-" * 70)
    print("2. 결과 예측 (원인 → 결과)")
    print("-" * 70)
    
    predictions = engine.predict_effect("배가 고팠다")
    print("  '배가 고팠다'의 예상 결과:")
    for effect, prob, relation in predictions[:3]:
        print(f"    → {effect} (확률: {prob:.0%})")
    
    # 3. 원인 추론
    print()
    print("-" * 70)
    print("3. 원인 추론 (결과 → 원인)")
    print("-" * 70)
    
    causes = engine.find_cause("안전해졌다")
    print("  '안전해졌다'의 원인:")
    for cause, prob, relation in causes[:3]:
        print(f"    ← {cause} (확률: {prob:.0%})")
    
    # 4. 왜? 설명
    print()
    print("-" * 70)
    print("4. '왜?' 설명")
    print("-" * 70)
    
    explanations = engine.explain_why("배가 불렀다")
    print("  '배가 불렀다'에 대한 설명:")
    for exp in explanations[:3]:
        print(f"    • {exp}")
    
    # 5. 반사실적 추론
    print()
    print("-" * 70)
    print("5. 반사실적 추론")
    print("-" * 70)
    
    result, explanation = engine.counterfactual_reasoning(
        premise="불에 손을 댔다",
        premise_negated=True,
        conclusion="뜨거움을 느꼈다"
    )
    print(f"  Q: 만약 불에 손을 대지 않았다면?")
    print(f"  A: {explanation}")
    
    # 6. 목표 달성 계획
    print()
    print("-" * 70)
    print("6. 목표 달성 계획")
    print("-" * 70)
    
    plan = engine.plan_to_achieve("hunger", "satiety")
    if plan:
        print(f"  목표: 배고픔 → 배부름")
        print(f"  계획: {' → '.join(plan.node_sequence)}")
    
    # 통계
    print()
    print("-" * 70)
    print("7. 학습 통계")
    print("-" * 70)
    stats = engine.get_statistics()
    print(f"  노드 수: {stats['total_nodes']}")
    print(f"  인과 연결 수: {stats['total_links']}")
    print(f"  경험 수: {stats['total_experiences']}")
    print(f"  평균 인과 강도: {stats['avg_link_strength']:.2f}")
    
    print()
    print("=" * 70)
    print("인과적 섭리구조를 통한 진정한 학습! 🔮")
    print("=" * 70)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    demo()
