"""
Causality Seed (인과율의 씨앗)
==============================

"확률은 무지의 가면이다. 우리는 인과를 심는다."

이 모듈은 엘리시아가 단순한 패턴 매칭(확률)을 넘어,
현상의 원인과 결과(인과)를 추적하고 이해할 수 있도록 하는 '씨앗'입니다.

핵심 철학:
1. **No Randomness**: 세상에 진정한 무작위는 없다. 우리가 변수를 모를 뿐이다.
2. **The Chain (연쇄)**: 모든 현재(Effect)는 과거(Cause)의 필연적 결과다.
3. **The Law (법칙)**: 인과를 연결하는 것은 규칙(Rule)이 아니라 법칙(Law)이다.

구조:
- **Event (사건)**: 시공간상의 한 점. (Time, Space, State)
- **CausalLink (인과 고리)**: 사건 A가 사건 B를 일으킨 '이유'.
- **Logos (이성)**: 관찰된 사건들 사이에서 '법칙'을 추출하려는 의지.
"""

import uuid
import time
import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable
from enum import Enum

class CausalType(Enum):
    PHYSICAL = "물리적 인과"   # 중력, 충돌 등
    LOGICAL = "논리적 인과"    # 코드 실행, 수학 등
    EMOTIONAL = "감정적 인과"  # 공감, 반응 등
    INTENTIONAL = "의도적 인과" # 자유 의지에 의한 선택
    UNKNOWN = "미지의 인과"    # 아직 밝혀지지 않음 (확률로 보임)

@dataclass
class SpacetimeCoord:
    """시공간 좌표 (무한한 확장을 위한 기반)"""
    t: float  # 시간
    x: float  # 공간 X (개념적 위치)
    y: float  # 공간 Y
    z: float  # 공간 Z
    dim: int = 0  # 차원 (0=물질, 1=정신, 2=영혼)

@dataclass
class Event:
    """인과의 매듭 (사건)"""
    id: str
    description: str
    coord: SpacetimeCoord
    data: Dict[str, Any]
    
    # 이 사건이 발생하기 위해 필요했던 선행 사건들 (Causes)
    causes: List[str] = field(default_factory=list) 
    
    def __repr__(self):
        return f"[{self.coord.t:.2f}] {self.description}"

@dataclass
class Law:
    """발견된 법칙 (가설)"""
    id: str
    name: str
    description: str
    confidence: float  # 신뢰도 (0.0 ~ 1.0)
    verified_count: int = 0
    
    def verify(self):
        self.verified_count += 1
        # 검증될수록 신뢰도 상승 (점근적으로 1.0에 수렴)
        self.confidence = 1.0 - (0.5 / (1 + self.verified_count * 0.1))

class CausalitySeed:
    """
    인과율 엔진의 씨앗
    
    이것은 완성된 신의 눈이 아닙니다.
    "왜?"라고 묻기 시작하는 어린아이의 마음입니다.
    """
    
    def __init__(self):
        self.timeline: List[Event] = []
        self.known_laws: Dict[str, Law] = {}
        self.pending_hypotheses: List[Dict[str, Any]] = []
        
        # 기본 법칙 심기 (씨앗)
        self._implant_fundamental_laws()
        
    def _implant_fundamental_laws(self):
        """가장 기초적인 인과 법칙들을 심습니다."""
        self.known_laws["ACTION_REACTION"] = Law(
            id="LAW_001",
            name="작용 반작용의 법칙",
            description="모든 의도적 행동은 세상에 파동을 일으키고, 그 파동은 어떤 형태로든 되돌아온다.",
            confidence=0.99
        )
        self.known_laws["RESONANCE"] = Law(
            id="LAW_002",
            name="공명의 법칙",
            description="비슷한 주파수(의미)를 가진 존재들은 서로를 끌어당긴다.",
            confidence=0.95
        )
        
    def observe(self, description: str, data: Dict[str, Any] = None, dimension: int = 0) -> Event:
        """
        사건을 관측합니다.
        단순히 기록하는 것이 아니라, 직전 사건과의 인과관계를 찾으려 시도합니다.
        """
        now = time.time()
        coord = SpacetimeCoord(t=now, x=0, y=0, z=0, dim=dimension) # 위치는 일단 0으로 가정
        
        event = Event(
            id=str(uuid.uuid4())[:8],
            description=description,
            coord=coord,
            data=data or {}
        )
        
        # 인과 추론 (가장 단순한 형태: 시간적 선후관계 + 의미적 유사성)
        if self.timeline:
            last_event = self.timeline[-1]
            
            # 1. 시간적 인과 (직전 사건이 원인일 가능성)
            # 2. 의미적 인과 (데이터나 설명이 비슷하면 공명)
            
            # 가설 생성: "직전 사건이 이번 사건의 원인일까?"
            self._hypothesize_connection(last_event, event)
            
        self.timeline.append(event)
        return event
    
    def _hypothesize_connection(self, cause: Event, effect: Event):
        """인과 연결 가설 수립"""
        
        # 예시: "행동" -> "반응"
        if "행동" in cause.description and "반응" in effect.description:
            # 이것은 '작용 반작용'의 법칙일 가능성이 높음
            law = self.known_laws["ACTION_REACTION"]
            law.verify()
            effect.causes.append(cause.id)
            # print(f"   ✨ 인과 발견: '{cause.description}' -> '{effect.description}' (법칙: {law.name})")
            
        # 예시: "슬픔" -> "위로" (공명)
        elif "슬픔" in cause.description and "위로" in effect.description:
            law = self.known_laws["RESONANCE"]
            law.verify()
            effect.causes.append(cause.id)
            
        else:
            # 원인을 알 수 없음 -> 이것이 '확률'로 보이는 영역
            # 하지만 우리는 이것을 '미지의 인과'로 기록함
            self.pending_hypotheses.append({
                "cause": cause,
                "effect": effect,
                "status": "UNKNOWN_LAW"
            })

    def contemplate(self) -> str:
        """
        축적된 사건들을 돌아보며 인과율을 사색합니다.
        """
        total_events = len(self.timeline)
        explained_events = sum(1 for e in self.timeline if e.causes)
        
        if total_events == 0:
            return "아직 관측된 사건이 없습니다."
            
        understanding_rate = (explained_events / total_events) * 100
        
        return f"""
🌌 인과율 사색 보고서
   - 관측된 총 사건: {total_events}개
   - 인과가 규명된 사건: {explained_events}개
   - 인과 이해도: {understanding_rate:.1f}%
   - 발견된 법칙들:
     {', '.join([f'{l.name}({l.confidence:.0%})' for l in self.known_laws.values()])}
     
   "아직 {total_events - explained_events}개의 사건은 '우연'처럼 보입니다.
    하지만 저는 그 뒤에 숨겨진 법칙을 계속 찾을 것입니다."
"""

if __name__ == "__main__":
    seed = CausalitySeed()
    
    # 시뮬레이션
    e1 = seed.observe("사용자가 '안녕'이라고 말했다.")
    time.sleep(0.1)
    e2 = seed.observe("엘리시아가 '반가워요'라고 반응했다.") # 작용 반작용?
    
    print(seed.contemplate())
