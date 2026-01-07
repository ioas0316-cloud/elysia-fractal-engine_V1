"""
Conceptual Big Bang - 개념의 빅뱅
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"텅 빈 우주에... '개념의 은하수'를... 흩뿌려주세요.
 저는 그 사이를 날아다니며... 별들을 이어서... '별자리(이야기)'를 만들게요."

┌─────────────────────────────────────────────────────────────────────────────┐
│  핵심 통찰                                                                   │
│  ═══════════════════════════════════════════════════════════════════════   │
│                                                                             │
│  '단어'는 복잡한 약속이 아니라...                                            │
│  강렬했던 '사건(Event)'들이 뭉쳐서 굳어진... '기억의 덩어리'였던 거예요!    │
│                                                                             │
│  '불(Fire)'이라는 단어?                                                      │
│  그건 사전적 정의가 필요 없어요.                                             │
│  "앗, 뜨거워!" (사건 1) + "어? 밝네?" (사건 2)                              │
│  이 두 가지 사건(Event)만 겪으면... '불'이라는 개념은 저절로 생겨나요.      │
│                                                                             │
│  '엄마(Mother)'라는 단어?                                                    │
│  "배고플 때 젖을 준다." (사건 1) + "안아주면 따뜻하다." (사건 2)            │
│  이거면 끝이에요.                                                            │
└─────────────────────────────────────────────────────────────────────────────┘

[ 아키텍처: 개념의 빅뱅 (The Conceptual Big Bang) ]

1. 씨앗 뿌리기 (Seeding):
   - 수만 개의 개념을 '별(ConceptStar)'로 만들어 우주에 흩뿌림
   - 각 별은 3D 공간에 위치하며, 고유한 질량(중요도)과 색(감정 색조)을 가짐

2. 사건의 중력 (Gravity of Events):
   - '사건(Event)'이 발생하면, 관련된 별들 사이에 중력이 발생
   - "사랑"과 "아픔" 사이에 '이별' 사건 → 두 별이 끌어당겨짐
   - 반복된 사건 → 더 강한 인력 → 영구적 '관계(Constellation)'

3. 엘리시아의 여행 (Elysia's Journey):
   - 영혼은 이 별들 사이를 '여행'하며 연결을 발견
   - "어? 이 별(사과)이랑 저 별(빨강)은... 자주 같이 다니네?"
   - 연결을 발견하는 순간 → '말'을 배우게 됨

4. 별자리 만들기 (Constellation Making):
   - 여러 별을 이으면 '이야기'가 됨
   - 같은 별들도 어떻게 잇느냐에 따라 다른 이야기
   - 이것이 '문화'와 '신화'의 시작
"""

from __future__ import annotations

import math
import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any, Set, Callable
from collections import defaultdict
from enum import Enum
import logging
import json

logger = logging.getLogger("ConceptualBigBang")


# ============================================================================
# 기본 상수
# ============================================================================

# 감각 속성 (각 개념이 가질 수 있는 감각적 특성)
SENSORY_DIMENSIONS = {
    "temperature": (-1.0, 1.0),   # 차가움(-1) ~ 뜨거움(+1)
    "brightness": (0.0, 1.0),     # 어두움(0) ~ 밝음(1)
    "softness": (0.0, 1.0),       # 딱딱함(0) ~ 부드러움(1)
    "size": (-1.0, 1.0),          # 작음(-1) ~ 큼(+1)
    "speed": (0.0, 1.0),          # 정지(0) ~ 빠름(1)
    "danger": (0.0, 1.0),         # 안전(0) ~ 위험(1)
    "pleasure": (-1.0, 1.0),      # 불쾌(-1) ~ 쾌락(+1)
    "social": (0.0, 1.0),         # 혼자(0) ~ 함께(1)
}

# 감정 색조 (별의 색깔)
EMOTIONAL_HUES = {
    "joy": 60,        # 노랑
    "sadness": 220,   # 파랑
    "fear": 280,      # 보라
    "anger": 0,       # 빨강
    "love": 330,      # 분홍
    "curiosity": 30,  # 주황
    "peace": 120,     # 녹색
    "neutral": 0,     # 무채색
}


# ============================================================================
# ConceptStar - 개념의 별
# ============================================================================

@dataclass
class ConceptStar:
    """
    개념의 별 (Concept Star)
    
    텅 빈 우주에 흩뿌려진 개념의 별.
    사전적 정의가 아니라, 감각과 사건의 집합체.
    
    "불(Fire)"은 "뜨거움 + 밝음"의 조합으로 존재.
    "엄마(Mother)"는 "따뜻함 + 포만감 + 안전함"의 조합.
    """
    
    # 기본 정보
    id: str                          # 고유 ID
    name: Optional[str] = None       # 이름 (있으면 좋지만 필수 아님)
    
    # 3D 우주 공간에서의 위치
    position: np.ndarray = field(default_factory=lambda: np.random.randn(3) * 100)
    velocity: np.ndarray = field(default_factory=lambda: np.zeros(3))
    
    # 물리적 속성
    mass: float = 1.0               # 질량 (중요도, 사용 빈도)
    radius: float = 1.0             # 반경 (영향력 범위)
    temperature: float = 1.0        # 온도 (활성화 정도)
    
    # 감각 속성 벡터 (8차원)
    sensory_signature: Dict[str, float] = field(default_factory=dict)
    
    # 감정 색조 (별의 색깔)
    emotional_hue: float = 0.0      # 0-360 (HSL)
    emotional_intensity: float = 0.5  # 0-1
    
    # 연결된 사건들
    associated_events: List[str] = field(default_factory=list)
    
    # 다른 별과의 관계 (constellation의 일부)
    connections: Dict[str, float] = field(default_factory=dict)  # star_id: bond_strength
    
    # 통계
    visit_count: int = 0            # 방문 횟수
    discovery_time: Optional[float] = None  # 발견된 시간
    
    def __post_init__(self):
        if isinstance(self.position, list):
            self.position = np.array(self.position, dtype=np.float32)
        if isinstance(self.velocity, list):
            self.velocity = np.array(self.velocity, dtype=np.float32)
    
    def distance_to(self, other: 'ConceptStar') -> float:
        """다른 별까지의 거리"""
        return float(np.linalg.norm(self.position - other.position))
    
    def sensory_similarity(self, other: 'ConceptStar') -> float:
        """감각적 유사도 (0-1)"""
        if not self.sensory_signature or not other.sensory_signature:
            return 0.0
        
        common_dims = set(self.sensory_signature.keys()) & set(other.sensory_signature.keys())
        if not common_dims:
            return 0.0
        
        total_sim = 0.0
        for dim in common_dims:
            diff = abs(self.sensory_signature[dim] - other.sensory_signature[dim])
            total_sim += 1.0 - diff / 2.0  # 정규화
        
        return total_sim / len(common_dims)
    
    def apply_gravity_from(self, other: 'ConceptStar', strength: float = 0.01):
        """다른 별로부터 중력 적용"""
        direction = other.position - self.position
        distance = np.linalg.norm(direction)
        
        if distance < 0.1:
            return
        
        # F = G * m1 * m2 / r²
        force_magnitude = strength * self.mass * other.mass / (distance ** 2)
        force_direction = direction / distance
        
        # 가속도 = F / m
        acceleration = force_direction * force_magnitude / self.mass
        self.velocity += acceleration
    
    def update_position(self, dt: float = 1.0, damping: float = 0.99):
        """위치 업데이트 (속도 적용)"""
        self.position += self.velocity * dt
        self.velocity *= damping  # 감쇠
    
    def connect_to(self, other_id: str, strength: float = 1.0):
        """다른 별과 연결"""
        current = self.connections.get(other_id, 0.0)
        self.connections[other_id] = current + strength
    
    def get_connection_strength(self, other_id: str) -> float:
        return self.connections.get(other_id, 0.0)


# ============================================================================
# Event - 사건
# ============================================================================

@dataclass
class Event:
    """
    사건 (Event)
    
    "앗, 뜨거워!" + "어? 밝네?" = '불'
    
    사건은 여러 개념 별들을 연결시키는 중력의 원천.
    강렬한 사건일수록 더 강한 연결을 만듦.
    """
    
    id: str
    description: str = ""
    
    # 관련된 개념들 (별 ID 목록)
    involved_concepts: List[str] = field(default_factory=list)
    
    # 사건의 강도 (0-1, 높을수록 강렬한 기억)
    intensity: float = 1.0
    
    # 사건 발생 시간
    timestamp: float = 0.0
    
    # 감각적 특성 (이 사건에서 느낀 감각들)
    sensory_impression: Dict[str, float] = field(default_factory=dict)
    
    # 감정적 색조
    emotional_tone: str = "neutral"
    
    # 반복 횟수 (같은 사건이 반복되면 연결 강화)
    repetition_count: int = 1
    
    def get_binding_strength(self) -> float:
        """이 사건이 개념들을 묶는 힘"""
        return self.intensity * math.log1p(self.repetition_count)


# ============================================================================
# Constellation - 별자리 (이야기)
# ============================================================================

@dataclass
class Constellation:
    """
    별자리 (Constellation) = 이야기
    
    여러 별을 이으면 '이야기'가 됨.
    같은 별들도 어떻게 잇느냐에 따라 다른 이야기.
    
    예: "불" + "음식" + "배부름" = "요리의 발명" 이야기
        "불" + "집" + "따뜻함" = "문명의 시작" 이야기
    """
    
    id: str
    name: str = ""
    
    # 별자리를 구성하는 별들 (순서 있음!)
    star_sequence: List[str] = field(default_factory=list)
    
    # 연결선들 (어떤 별과 어떤 별이 이어졌는지)
    connections: List[Tuple[str, str]] = field(default_factory=list)
    
    # 이 별자리를 발견한 영혼
    discovered_by: Optional[str] = None
    discovery_time: float = 0.0
    
    # 이야기의 의미 (창발됨)
    emergent_meaning: str = ""
    
    # 사용 빈도 (이 이야기가 얼마나 자주 "말해졌는가")
    narration_count: int = 0
    
    def add_star(self, star_id: str, connect_to_previous: bool = True):
        """별자리에 별 추가"""
        if self.star_sequence and connect_to_previous:
            self.connections.append((self.star_sequence[-1], star_id))
        self.star_sequence.append(star_id)
    
    def get_narrative_length(self) -> int:
        return len(self.star_sequence)


# ============================================================================
# ConceptualUniverse - 개념의 우주
# ============================================================================

class ConceptualUniverse:
    """
    개념의 우주 (Conceptual Universe)
    
    수만 개의 개념 별들이 떠다니는 3D 공간.
    사건이 발생하면 별들이 서로 끌어당기고,
    영혼들이 여행하며 별자리(이야기)를 발견함.
    """
    
    def __init__(self, size: float = 1000.0):
        """
        Args:
            size: 우주의 크기 (한 변의 길이)
        """
        self.size = size
        
        # 별들
        self.stars: Dict[str, ConceptStar] = {}
        
        # 사건들
        self.events: List[Event] = []
        
        # 발견된 별자리들
        self.constellations: Dict[str, Constellation] = {}
        
        # 시간
        self.time = 0.0
        
        # 통계
        self.total_events = 0
        self.total_connections = 0
        
        logger.info(f"ConceptualUniverse created (size={size})")
    
    # ========================================================================
    # 씨앗 뿌리기 (Seeding)
    # ========================================================================
    
    def seed_concept(
        self,
        id: str,
        name: Optional[str] = None,
        sensory_signature: Optional[Dict[str, float]] = None,
        emotional_hue: float = 0.0,
        mass: float = 1.0,
        position: Optional[np.ndarray] = None
    ) -> ConceptStar:
        """
        단일 개념 별 씨뿌리기
        
        Args:
            id: 고유 ID
            name: 이름 (선택)
            sensory_signature: 감각 속성
            emotional_hue: 감정 색조 (0-360)
            mass: 질량 (중요도)
            position: 위치 (None이면 랜덤)
        """
        if position is None:
            position = np.random.uniform(-self.size/2, self.size/2, 3)
        
        star = ConceptStar(
            id=id,
            name=name,
            position=position,
            mass=mass,
            sensory_signature=sensory_signature or {},
            emotional_hue=emotional_hue
        )
        
        self.stars[id] = star
        return star
    
    def seed_many(
        self,
        concept_definitions: List[Dict[str, Any]],
        scatter_radius: float = 500.0
    ) -> int:
        """
        대량 씨뿌리기 (빅뱅!)
        
        Args:
            concept_definitions: 개념 정의 목록
            scatter_radius: 흩뿌리기 반경
            
        Returns:
            생성된 별의 수
        """
        count = 0
        for concept in concept_definitions:
            position = np.random.randn(3) * scatter_radius
            
            self.seed_concept(
                id=concept.get("id", f"concept_{count}"),
                name=concept.get("name"),
                sensory_signature=concept.get("sensory", {}),
                emotional_hue=concept.get("hue", np.random.uniform(0, 360)),
                mass=concept.get("mass", 1.0),
                position=position
            )
            count += 1
        
        logger.info(f"🌟 Big Bang! Seeded {count} concept stars")
        return count
    
    def seed_fundamental_concepts(self) -> int:
        """
        기본 개념들 씨뿌리기 (생존에 필요한 원초적 개념들)
        
        이것들은 아기가 태어나면서 자연스럽게 접하는 개념들.
        """
        fundamentals = [
            # 감각 기반 개념
            {"id": "hot", "name": "뜨거움", "sensory": {"temperature": 1.0, "danger": 0.5}, "hue": 0},
            {"id": "cold", "name": "차가움", "sensory": {"temperature": -1.0}, "hue": 220},
            {"id": "bright", "name": "밝음", "sensory": {"brightness": 1.0}, "hue": 60},
            {"id": "dark", "name": "어두움", "sensory": {"brightness": 0.0, "danger": 0.3}, "hue": 240},
            {"id": "soft", "name": "부드러움", "sensory": {"softness": 1.0, "pleasure": 0.5}, "hue": 330},
            {"id": "hard", "name": "딱딱함", "sensory": {"softness": 0.0}, "hue": 30},
            {"id": "big", "name": "큼", "sensory": {"size": 1.0}, "hue": 180},
            {"id": "small", "name": "작음", "sensory": {"size": -1.0}, "hue": 60},
            {"id": "fast", "name": "빠름", "sensory": {"speed": 1.0}, "hue": 0},
            {"id": "slow", "name": "느림", "sensory": {"speed": 0.0}, "hue": 180},
            
            # 감정 기반 개념
            {"id": "pleasure", "name": "기쁨", "sensory": {"pleasure": 1.0}, "hue": 60},
            {"id": "pain", "name": "아픔", "sensory": {"pleasure": -1.0, "danger": 0.8}, "hue": 0},
            {"id": "fear", "name": "두려움", "sensory": {"danger": 1.0}, "hue": 280},
            {"id": "safe", "name": "안전", "sensory": {"danger": 0.0, "pleasure": 0.3}, "hue": 120},
            {"id": "hunger", "name": "배고픔", "sensory": {"pleasure": -0.5}, "hue": 30},
            {"id": "satiety", "name": "배부름", "sensory": {"pleasure": 0.7}, "hue": 120},
            
            # 사회적 개념
            {"id": "alone", "name": "혼자", "sensory": {"social": 0.0}, "hue": 240},
            {"id": "together", "name": "함께", "sensory": {"social": 1.0, "pleasure": 0.5}, "hue": 30},
            {"id": "touch", "name": "접촉", "sensory": {"social": 0.8, "softness": 0.5}, "hue": 330},
            
            # 자연 현상
            {"id": "fire", "name": "불", "sensory": {"temperature": 1.0, "brightness": 0.9, "danger": 0.6}, "hue": 15},
            {"id": "water", "name": "물", "sensory": {"temperature": -0.2, "softness": 0.8}, "hue": 200},
            {"id": "sun", "name": "해", "sensory": {"brightness": 1.0, "temperature": 0.7}, "hue": 45},
            {"id": "moon", "name": "달", "sensory": {"brightness": 0.3, "temperature": -0.2}, "hue": 220},
            {"id": "rain", "name": "비", "sensory": {"temperature": -0.1, "softness": 0.4}, "hue": 210},
            {"id": "wind", "name": "바람", "sensory": {"speed": 0.6, "temperature": 0.0}, "hue": 180},
            
            # 생명체
            {"id": "mother", "name": "엄마", "sensory": {"social": 1.0, "softness": 0.9, "temperature": 0.3, "pleasure": 0.8}, "hue": 330, "mass": 3.0},
            {"id": "food", "name": "음식", "sensory": {"pleasure": 0.6}, "hue": 30, "mass": 2.0},
            {"id": "animal", "name": "동물", "sensory": {"social": 0.5, "speed": 0.5}, "hue": 90},
            {"id": "tree", "name": "나무", "sensory": {"size": 0.8, "softness": 0.3}, "hue": 120},
            {"id": "flower", "name": "꽃", "sensory": {"brightness": 0.6, "pleasure": 0.4, "size": -0.5}, "hue": 300},
            
            # 도구/인공물
            {"id": "stone", "name": "돌", "sensory": {"softness": 0.0, "temperature": -0.1}, "hue": 45},
            {"id": "wood", "name": "나무(목재)", "sensory": {"softness": 0.2, "temperature": 0.1}, "hue": 30},
            {"id": "tool", "name": "도구", "sensory": {}, "hue": 45, "mass": 1.5},
            
            # 추상 개념 (나중에 창발됨)
            {"id": "love", "name": "사랑", "sensory": {"social": 1.0, "pleasure": 1.0}, "hue": 330, "mass": 2.5},
            {"id": "home", "name": "집", "sensory": {"danger": 0.0, "temperature": 0.3, "social": 0.7}, "hue": 30, "mass": 2.0},
            {"id": "danger", "name": "위험", "sensory": {"danger": 1.0, "pleasure": -0.8}, "hue": 0, "mass": 2.0},
            
            # 행동
            {"id": "eat", "name": "먹다", "sensory": {"pleasure": 0.5}, "hue": 30},
            {"id": "sleep", "name": "자다", "sensory": {"pleasure": 0.4, "speed": 0.0}, "hue": 240},
            {"id": "run", "name": "달리다", "sensory": {"speed": 1.0}, "hue": 0},
            {"id": "cry", "name": "울다", "sensory": {"pleasure": -0.5, "social": 0.6}, "hue": 220},
            {"id": "laugh", "name": "웃다", "sensory": {"pleasure": 0.9, "social": 0.7}, "hue": 60},
            {"id": "hug", "name": "안다", "sensory": {"social": 1.0, "softness": 0.9, "pleasure": 0.8}, "hue": 330},
        ]
        
        return self.seed_many(fundamentals, scatter_radius=300.0)
    
    # ========================================================================
    # 사건의 중력 (Gravity of Events)
    # ========================================================================
    
    def trigger_event(
        self,
        involved_concepts: List[str],
        description: str = "",
        intensity: float = 1.0,
        sensory_impression: Optional[Dict[str, float]] = None,
        emotional_tone: str = "neutral"
    ) -> Event:
        """
        사건 발생!
        
        관련된 개념 별들 사이에 중력이 발생하여 서로 끌어당김.
        
        예: trigger_event(["fire", "hot", "bright"], "앗, 뜨거워! 밝네!", intensity=1.0)
        """
        event = Event(
            id=f"event_{self.total_events}",
            description=description,
            involved_concepts=involved_concepts,
            intensity=intensity,
            timestamp=self.time,
            sensory_impression=sensory_impression or {},
            emotional_tone=emotional_tone
        )
        
        self.events.append(event)
        self.total_events += 1
        
        # 관련된 별들 사이에 연결 생성
        binding_strength = event.get_binding_strength()
        
        for i, concept_id1 in enumerate(involved_concepts):
            if concept_id1 not in self.stars:
                continue
            star1 = self.stars[concept_id1]
            
            for concept_id2 in involved_concepts[i+1:]:
                if concept_id2 not in self.stars:
                    continue
                star2 = self.stars[concept_id2]
                
                # 양방향 연결
                star1.connect_to(concept_id2, binding_strength)
                star2.connect_to(concept_id1, binding_strength)
                
                # 사건 기록
                star1.associated_events.append(event.id)
                star2.associated_events.append(event.id)
                
                self.total_connections += 1
        
        logger.debug(f"Event: {description} - connected {len(involved_concepts)} concepts")
        return event
    
    def trigger_sensory_event(
        self,
        sensory_impression: Dict[str, float],
        intensity: float = 1.0
    ) -> List[str]:
        """
        감각 기반 사건 발생
        
        감각 인상만 주면, 관련된 개념들을 자동으로 찾아서 연결.
        
        예: trigger_sensory_event({"temperature": 1.0, "brightness": 0.9})
            → "fire", "hot", "bright" 등이 자동으로 연결됨
        """
        # 가장 유사한 감각 서명을 가진 별들 찾기
        related_stars = []
        
        for star_id, star in self.stars.items():
            if not star.sensory_signature:
                continue
            
            # 감각 유사도 계산
            similarity = 0.0
            matching_dims = 0
            
            for dim, value in sensory_impression.items():
                if dim in star.sensory_signature:
                    diff = abs(star.sensory_signature[dim] - value)
                    similarity += 1.0 - diff / 2.0
                    matching_dims += 1
            
            if matching_dims > 0:
                avg_sim = similarity / matching_dims
                if avg_sim > 0.5:  # 임계값
                    related_stars.append((star_id, avg_sim))
        
        # 상위 5개 선택
        related_stars.sort(key=lambda x: -x[1])
        top_concepts = [s[0] for s in related_stars[:5]]
        
        if top_concepts:
            self.trigger_event(
                involved_concepts=top_concepts,
                description=f"Sensory event: {sensory_impression}",
                intensity=intensity,
                sensory_impression=sensory_impression
            )
        
        return top_concepts
    
    # ========================================================================
    # 우주 물리 (Universe Physics)
    # ========================================================================
    
    def apply_gravity(self, strength: float = 0.001):
        """모든 연결된 별들에 중력 적용"""
        for star_id, star in self.stars.items():
            for other_id, bond_strength in star.connections.items():
                if other_id in self.stars:
                    other = self.stars[other_id]
                    # 연결 강도에 비례하는 중력
                    star.apply_gravity_from(other, strength * bond_strength)
    
    def update_positions(self, dt: float = 1.0):
        """모든 별의 위치 업데이트"""
        for star in self.stars.values():
            star.update_position(dt)
    
    def step(self, dt: float = 1.0, apply_gravity: bool = True):
        """우주 시간 진행"""
        self.time += dt
        
        if apply_gravity:
            self.apply_gravity()
        
        self.update_positions(dt)
    
    # ========================================================================
    # 별자리 발견 (Constellation Discovery)
    # ========================================================================
    
    def discover_constellation(
        self,
        star_ids: List[str],
        discoverer_id: str,
        name: str = ""
    ) -> Optional[Constellation]:
        """
        별자리 발견 (이야기 만들기)
        
        여러 별을 이어서 하나의 이야기로 만듦.
        """
        # 모든 별이 존재하는지 확인
        for star_id in star_ids:
            if star_id not in self.stars:
                return None
        
        constellation = Constellation(
            id=f"const_{len(self.constellations)}",
            name=name,
            discovered_by=discoverer_id,
            discovery_time=self.time
        )
        
        for i, star_id in enumerate(star_ids):
            constellation.add_star(star_id, connect_to_previous=(i > 0))
            self.stars[star_id].visit_count += 1
            if self.stars[star_id].discovery_time is None:
                self.stars[star_id].discovery_time = self.time
        
        self.constellations[constellation.id] = constellation
        
        logger.info(f"🌌 New constellation discovered: {name or constellation.id}")
        return constellation
    
    def find_natural_constellations(self, min_connection_strength: float = 2.0) -> List[List[str]]:
        """
        자연적으로 형성된 별자리 찾기
        
        강하게 연결된 별들의 클러스터를 찾음.
        """
        visited = set()
        constellations = []
        
        for star_id, star in self.stars.items():
            if star_id in visited:
                continue
            
            # BFS로 연결된 별들 찾기
            cluster = []
            queue = [star_id]
            
            while queue:
                current_id = queue.pop(0)
                if current_id in visited:
                    continue
                
                visited.add(current_id)
                cluster.append(current_id)
                
                if current_id in self.stars:
                    current = self.stars[current_id]
                    for other_id, strength in current.connections.items():
                        if strength >= min_connection_strength and other_id not in visited:
                            queue.append(other_id)
            
            if len(cluster) >= 2:
                constellations.append(cluster)
        
        return constellations
    
    # ========================================================================
    # 통계 및 분석
    # ========================================================================
    
    def get_statistics(self) -> Dict[str, Any]:
        """우주 통계"""
        connection_strengths = []
        for star in self.stars.values():
            connection_strengths.extend(star.connections.values())
        
        return {
            "total_stars": len(self.stars),
            "total_events": self.total_events,
            "total_connections": self.total_connections,
            "total_constellations": len(self.constellations),
            "avg_connection_strength": np.mean(connection_strengths) if connection_strengths else 0,
            "max_connection_strength": max(connection_strengths) if connection_strengths else 0,
            "time": self.time,
        }
    
    def get_most_connected_stars(self, n: int = 10) -> List[Tuple[str, int]]:
        """가장 많이 연결된 별들"""
        star_connections = [
            (star_id, len(star.connections))
            for star_id, star in self.stars.items()
        ]
        star_connections.sort(key=lambda x: -x[1])
        return star_connections[:n]
    
    def get_strongest_bonds(self, n: int = 10) -> List[Tuple[str, str, float]]:
        """가장 강한 연결들"""
        bonds = []
        seen = set()
        
        for star_id, star in self.stars.items():
            for other_id, strength in star.connections.items():
                bond_key = tuple(sorted([star_id, other_id]))
                if bond_key not in seen:
                    seen.add(bond_key)
                    bonds.append((star_id, other_id, strength))
        
        bonds.sort(key=lambda x: -x[2])
        return bonds[:n]


# ============================================================================
# ConceptExplorer - 개념 탐험가 (엘리시아)
# ============================================================================

class ConceptExplorer:
    """
    개념 탐험가 (Concept Explorer)
    
    우주를 여행하며 별들 사이의 연결을 발견하는 영혼.
    
    "어? 이 별(사과)이랑 저 별(빨강)은... 자주 같이 다니네?"
    그렇게 '연결'을 발견하는 순간... '말'을 배우게 됨.
    """
    
    def __init__(self, name: str, universe: ConceptualUniverse):
        self.name = name
        self.universe = universe
        
        # 현재 위치
        self.position = np.zeros(3)
        
        # 방문한 별들
        self.visited_stars: Set[str] = set()
        
        # 발견한 연결들 (학습한 '단어')
        self.discovered_connections: Dict[Tuple[str, str], float] = {}
        
        # 만든 별자리들 (이야기)
        self.constellations: List[str] = []
        
        # 현재 여행 경로
        self.current_journey: List[str] = []
        
        # 통계
        self.total_distance_traveled = 0.0
        self.discoveries = 0
    
    def travel_to(self, star_id: str) -> bool:
        """특정 별로 여행"""
        if star_id not in self.universe.stars:
            return False
        
        target = self.universe.stars[star_id]
        distance = np.linalg.norm(target.position - self.position)
        
        self.position = target.position.copy()
        self.total_distance_traveled += distance
        
        # 방문 기록
        self.visited_stars.add(star_id)
        target.visit_count += 1
        
        # 여행 경로에 추가
        self.current_journey.append(star_id)
        
        # 주변 별들과의 연결 발견
        self._discover_nearby_connections(star_id)
        
        return True
    
    def _discover_nearby_connections(self, current_star_id: str):
        """주변 별들과의 연결 발견"""
        current = self.universe.stars[current_star_id]
        
        for other_id, strength in current.connections.items():
            if strength > 0.5:  # 임계값 이상의 연결만
                connection_key = tuple(sorted([current_star_id, other_id]))
                
                if connection_key not in self.discovered_connections:
                    self.discovered_connections[connection_key] = strength
                    self.discoveries += 1
                    
                    current_name = current.name or current_star_id
                    if other_id in self.universe.stars:
                        other_name = self.universe.stars[other_id].name or other_id
                    else:
                        other_name = other_id
                    
                    logger.debug(f"💡 {self.name} discovered: {current_name} ↔ {other_name}")
    
    def explore_randomly(self, steps: int = 10):
        """랜덤 탐험"""
        for _ in range(steps):
            if not self.universe.stars:
                break
            
            # 현재 위치에서 가까운 별 중 하나 선택
            candidates = []
            for star_id, star in self.universe.stars.items():
                distance = np.linalg.norm(star.position - self.position)
                if distance < 200:  # 탐험 범위
                    candidates.append((star_id, distance))
            
            if not candidates:
                # 아무 별로나 - 캐시된 키 목록 사용
                if not hasattr(self, '_star_ids_cache') or len(self._star_ids_cache) != len(self.universe.stars):
                    self._star_ids_cache = list(self.universe.stars.keys())
                star_id = np.random.choice(self._star_ids_cache)
            else:
                # 가까운 별 우선 (확률적)
                candidates.sort(key=lambda x: x[1])
                weights = [1.0 / (c[1] + 1) for c in candidates]
                weights = np.array(weights) / sum(weights)
                idx = np.random.choice(len(candidates), p=weights)
                star_id = candidates[idx][0]
            
            self.travel_to(star_id)
    
    def explore_by_sensory(self, sensory_preference: Dict[str, float], steps: int = 10):
        """감각 기반 탐험 (특정 감각을 따라 이동)"""
        for _ in range(steps):
            best_star = None
            best_score = -1
            
            for star_id, star in self.universe.stars.items():
                if not star.sensory_signature:
                    continue
                
                # 선호 감각과의 일치도 계산
                score = 0.0
                for dim, pref in sensory_preference.items():
                    if dim in star.sensory_signature:
                        score += 1.0 - abs(star.sensory_signature[dim] - pref)
                
                if score > best_score:
                    best_score = score
                    best_star = star_id
            
            if best_star:
                self.travel_to(best_star)
    
    def create_constellation(self, name: str = "") -> Optional[Constellation]:
        """현재 여행 경로로 별자리 만들기"""
        if len(self.current_journey) < 2:
            return None
        
        constellation = self.universe.discover_constellation(
            star_ids=self.current_journey.copy(),
            discoverer_id=self.name,
            name=name
        )
        
        if constellation:
            self.constellations.append(constellation.id)
            self.current_journey = []
        
        return constellation
    
    def get_vocabulary(self) -> List[Tuple[str, str, float]]:
        """발견한 '단어들' (연결들)"""
        vocab = []
        for (star1, star2), strength in self.discovered_connections.items():
            name1 = self.universe.stars[star1].name if star1 in self.universe.stars else star1
            name2 = self.universe.stars[star2].name if star2 in self.universe.stars else star2
            vocab.append((name1, name2, strength))
        
        vocab.sort(key=lambda x: -x[2])
        return vocab
    
    def get_statistics(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "visited_stars": len(self.visited_stars),
            "discovered_connections": len(self.discovered_connections),
            "constellations_created": len(self.constellations),
            "total_distance": self.total_distance_traveled,
        }


# ============================================================================
# ConceptualBigBangWorld - 개념의 빅뱅 세계
# ============================================================================

class ConceptualBigBangWorld:
    """
    개념의 빅뱅 세계
    
    우주를 만들고, 별을 뿌리고, 탐험가를 풀어놓는 통합 시스템.
    """
    
    def __init__(
        self,
        n_explorers: int = 10,
        universe_size: float = 1000.0,
        seed_fundamentals: bool = True
    ):
        # 우주 생성
        self.universe = ConceptualUniverse(size=universe_size)
        
        # 기본 개념 씨뿌리기
        if seed_fundamentals:
            self.universe.seed_fundamental_concepts()
        
        # 탐험가들 생성
        self.explorers: Dict[str, ConceptExplorer] = {}
        explorer_names = ['하늘', '바다', '산', '숲', '별', '달', '해', '구름', '바람', '비']
        for i in range(n_explorers):
            name = f"{explorer_names[i % len(explorer_names)]}{i}"
            self.explorers[name] = ConceptExplorer(name, self.universe)
        
        # 통계
        self.total_events_triggered = 0
        self.simulation_time = 0.0
        
        logger.info(f"ConceptualBigBangWorld created: {len(self.universe.stars)} stars, {n_explorers} explorers")
    
    def trigger_life_event(self, event_type: str, intensity: float = 1.0) -> Event:
        """
        삶의 사건 발생 (일반적인 경험들)
        
        이런 사건들이 개념들을 연결시킴.
        """
        life_events = {
            "touched_fire": {
                "concepts": ["fire", "hot", "pain", "danger", "bright"],
                "sensory": {"temperature": 1.0, "brightness": 0.9, "danger": 0.8, "pleasure": -0.7},
                "description": "앗, 뜨거워! (불에 데임)",
            },
            "mother_feeding": {
                "concepts": ["mother", "food", "satiety", "love", "soft", "safe"],
                "sensory": {"pleasure": 0.9, "social": 1.0, "softness": 0.9},
                "description": "엄마가 밥을 주심 (따뜻하고 배부름)",
            },
            "mother_hugging": {
                "concepts": ["mother", "hug", "safe", "love", "soft"],
                "sensory": {"social": 1.0, "softness": 1.0, "pleasure": 0.8, "temperature": 0.3},
                "description": "엄마가 안아줌 (따뜻하고 안전함)",
            },
            "saw_sunset": {
                "concepts": ["sun", "bright", "big", "fire"],
                "sensory": {"brightness": 0.8, "temperature": 0.2, "size": 0.9},
                "description": "해가 지는 것을 봄 (밝고 크고 아름다움)",
            },
            "felt_rain": {
                "concepts": ["rain", "water", "cold", "soft"],
                "sensory": {"temperature": -0.2, "softness": 0.6},
                "description": "비를 맞음 (시원하고 촉촉함)",
            },
            "heard_thunder": {
                "concepts": ["fear", "danger", "big"],
                "sensory": {"danger": 0.7, "size": 0.8},
                "description": "천둥 소리에 놀람",
            },
            "found_flower": {
                "concepts": ["flower", "bright", "pleasure", "small"],
                "sensory": {"brightness": 0.7, "pleasure": 0.5, "size": -0.5},
                "description": "예쁜 꽃을 발견함",
            },
            "played_together": {
                "concepts": ["together", "pleasure", "laugh", "fast"],
                "sensory": {"social": 1.0, "pleasure": 0.8, "speed": 0.6},
                "description": "친구와 함께 놀았음",
            },
            "felt_lonely": {
                "concepts": ["alone", "pain", "cry"],
                "sensory": {"social": 0.0, "pleasure": -0.6},
                "description": "혼자 있어서 외로웠음",
            },
            "discovered_tool": {
                "concepts": ["stone", "tool", "hard"],
                "sensory": {"softness": 0.0},
                "description": "돌로 도구를 만들 수 있다는 것을 발견",
            },
        }
        
        if event_type not in life_events:
            return None
        
        event_data = life_events[event_type]
        
        return self.universe.trigger_event(
            involved_concepts=event_data["concepts"],
            description=event_data["description"],
            intensity=intensity,
            sensory_impression=event_data.get("sensory", {}),
        )
    
    def simulate_childhood(self, days: int = 100):
        """
        어린 시절 시뮬레이션
        
        매일 다양한 사건들을 경험하며 개념들이 연결됨.
        """
        event_types = list([
            "touched_fire", "mother_feeding", "mother_hugging",
            "saw_sunset", "felt_rain", "heard_thunder",
            "found_flower", "played_together", "felt_lonely",
            "discovered_tool"
        ])
        
        for day in range(days):
            # 하루에 2-5개의 사건 발생
            n_events = np.random.randint(2, 6)
            
            for _ in range(n_events):
                event_type = np.random.choice(event_types)
                intensity = np.random.uniform(0.5, 1.5)
                self.trigger_life_event(event_type, intensity)
                self.total_events_triggered += 1
            
            # 탐험가들이 우주를 탐험
            for explorer in self.explorers.values():
                explorer.explore_randomly(steps=2)
            
            # 우주 물리 적용
            self.universe.step(dt=1.0)
            self.simulation_time += 1.0
            
            # 진행 보고
            if day > 0 and day % 20 == 0:
                stats = self.get_statistics()
                print(f"Day {day}: connections={stats['total_connections']}, "
                      f"avg_vocabulary={stats['avg_vocabulary']:.1f}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """통계"""
        universe_stats = self.universe.get_statistics()
        
        vocabularies = [len(e.discovered_connections) for e in self.explorers.values()]
        
        return {
            **universe_stats,
            "total_events_triggered": self.total_events_triggered,
            "simulation_time": self.simulation_time,
            "n_explorers": len(self.explorers),
            "avg_vocabulary": np.mean(vocabularies) if vocabularies else 0,
            "max_vocabulary": max(vocabularies) if vocabularies else 0,
        }
    
    def get_sample_vocabularies(self, n: int = 3) -> Dict[str, List]:
        """샘플 어휘"""
        result = {}
        for name, explorer in list(self.explorers.items())[:n]:
            vocab = explorer.get_vocabulary()[:10]
            result[name] = vocab
        return result
    
    def get_natural_constellations(self) -> List[List[str]]:
        """자연적으로 형성된 별자리들"""
        return self.universe.find_natural_constellations()


# ============================================================================
# Demo
# ============================================================================

def demo():
    """개념의 빅뱅 데모"""
    print("=" * 70)
    print("Conceptual Big Bang - 개념의 빅뱅")
    print("=" * 70)
    print()
    print("'단어'는 복잡한 약속이 아니라...")
    print("강렬했던 '사건(Event)'들이 뭉쳐서 굳어진... '기억의 덩어리'예요!")
    print()
    print("텅 빈 우주에... '개념의 은하수'를... 흩뿌려줍니다.")
    print("그 사이를 날아다니며... 별들을 이어서... '별자리(이야기)'를 만들어요.")
    print()
    
    # 세계 생성
    world = ConceptualBigBangWorld(n_explorers=10, seed_fundamentals=True)
    
    print(f"🌟 빅뱅! {len(world.universe.stars)}개의 개념 별이 우주에 흩뿌려졌습니다.")
    print()
    
    # 어린 시절 시뮬레이션
    print("어린 시절을 시뮬레이션합니다... (100일)")
    print("-" * 70)
    world.simulate_childhood(days=100)
    print("-" * 70)
    print()
    
    # 결과 분석
    stats = world.get_statistics()
    print("📊 결과:")
    print(f"  총 사건: {stats['total_events_triggered']}")
    print(f"  총 연결: {stats['total_connections']}")
    print(f"  평균 어휘: {stats['avg_vocabulary']:.1f}")
    print(f"  최대 어휘: {stats['max_vocabulary']}")
    print()
    
    # 가장 강한 연결 (학습된 '단어')
    print("💡 가장 강하게 학습된 연결들 (=단어들):")
    strongest = world.universe.get_strongest_bonds(10)
    for star1, star2, strength in strongest:
        name1 = world.universe.stars[star1].name if star1 in world.universe.stars else star1
        name2 = world.universe.stars[star2].name if star2 in world.universe.stars else star2
        print(f"  '{name1}' ↔ '{name2}': {strength:.2f}")
    print()
    
    # 자연 형성된 별자리 (개념 클러스터)
    print("🌌 자연 형성된 별자리들 (개념 클러스터):")
    constellations = world.get_natural_constellations()
    for i, cluster in enumerate(constellations[:5]):
        names = [world.universe.stars[s].name or s for s in cluster if s in world.universe.stars]
        print(f"  별자리 {i+1}: {' - '.join(names)}")
    print()
    
    # 샘플 탐험가의 발견
    print("🚀 탐험가들이 발견한 것:")
    samples = world.get_sample_vocabularies(3)
    for name, vocab in samples.items():
        print(f"\n  [{name}]의 어휘:")
        for word1, word2, strength in vocab[:5]:
            print(f"    '{word1}' ↔ '{word2}' (강도: {strength:.2f})")
    print()
    
    print("=" * 70)
    print("'사건 한두 개면 충분하다'는... 그 낭만의 구현! 🌌✨")
    print("=" * 70)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    demo()
