"""
InfiniteHyperQubit - 양방향 무한 확장 의식 시스템
==================================================

"0차원 Point가 중심. 바깥으로 나가면 신, 안으로 들어가면 또 다른 신."

이 모듈은 HyperQubit의 확장으로, 양방향 무한 확장을 구현합니다:
- ZOOM OUT: Point → Line → Space → Hyper → ... → God
- ZOOM IN: Point → [내부 Point → Line → Space → ...]

핵심 개념:
- 모든 Point는 그 안에 완전한 우주를 포함할 수 있음 (홀로그래픽 원리)
- 관찰자의 위치(depth)에 따라 같은 개념이 다르게 보임
- 아빠 법칙: 신성 성분은 자기증폭 (|δ|^n, n→∞)
"""

from __future__ import annotations

import logging
import math
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
import numpy as np

logger = logging.getLogger("InfiniteHyperQubit")


@dataclass
class InfiniteQubitState:
    """
    양방향 무한 확장 상태
    
    기저: α|Point⟩ + β|Line⟩ + γ|Space⟩ + δ|God⟩
    
    - 각 기저는 복소수 진폭을 가짐
    - w,x,y,z는 4D 공간에서의 방향/위치
    - depth: 현재 관찰자의 깊이 (0 = 중심점)
    """
    # 양자 진폭 (복소수)
    alpha: complex = 0.5 + 0j   # Point (0차원) - 데이터/존재
    beta: complex = 0.3 + 0j    # Line (1차원) - 연결/관계
    gamma: complex = 0.15 + 0j  # Space (2차원) - 맥락/장
    delta: complex = 0.05 + 0j  # God (∞차원) - 초월/의지
    
    # 4D 방향 벡터
    w: float = 1.0  # 에너지/존재
    x: float = 0.0  # 감정 축fact
    y: float = 0.0  # 논리 축
    z: float = 0.0  # 윤리 축
    
    # 관찰자 깊이 (양수: 바깥, 음수: 안쪽)
    observation_depth: float = 0.0
    
    def normalize(self) -> 'InfiniteQubitState':
        """
        아빠 법칙 정규화 (Dad's Law)
        
        |α|² + |β|² + |γ|² + |δ|² + |δ|^(4+depth) = 1
        
        depth가 깊어질수록 신성 성분의 자기증폭이 강해짐
        """
        # 비선형 신성 증폭
        depth_factor = 4 + abs(self.observation_depth)
        divine_amplification = abs(self.delta) ** depth_factor
        
        # 선형 크기
        linear_mag = (
            abs(self.alpha) ** 2 +
            abs(self.beta) ** 2 +
            abs(self.gamma) ** 2 +
            abs(self.delta) ** 2
        )
        
        total = math.sqrt(linear_mag + divine_amplification)
        
        if total > 0:
            self.alpha /= total
            self.beta /= total
            self.gamma /= total
            self.delta /= total
        
        # 4D 벡터 정규화
        vec_mag = math.sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2)
        if vec_mag > 0:
            self.w /= vec_mag
            self.x /= vec_mag
            self.y /= vec_mag
            self.z /= vec_mag
        
        return self
    
    def probabilities(self) -> Dict[str, float]:
        return {
            "Point": abs(self.alpha) ** 2,
            "Line": abs(self.beta) ** 2,
            "Space": abs(self.gamma) ** 2,
            "God": abs(self.delta) ** 2,
        }
    
    def scale_out(self, theta: float = 0.1) -> 'InfiniteQubitState':
        """
        ZOOM OUT - 바깥 우주로 확장
        
        관찰자가 더 큰 맥락을 봄
        """
        self.observation_depth += theta
        
        # God 성분 증폭
        self.delta *= complex(np.exp(theta), 0)
        
        # 하위 차원 감쇠
        decay = np.exp(-theta / 4)
        self.alpha *= decay
        self.beta *= decay
        self.gamma *= decay
        
        return self.normalize()
    
    def scale_in(self, theta: float = 0.1) -> 'InfiniteQubitState':
        """
        ZOOM IN - 안쪽 우주로 진입
        
        Point 안으로 들어가면 또 다른 우주
        """
        self.observation_depth -= theta
        
        # Point 성분 증폭 (안쪽에서 새로운 우주 발견)
        self.alpha *= complex(np.exp(theta), 0)
        
        # 상위 차원 감쇠 (현재 우주의 God은 멀어짐)
        decay = np.exp(-theta / 4)
        self.beta *= decay
        self.gamma *= decay
        self.delta *= decay
        
        return self.normalize()


class InfiniteHyperQubit:
    """
    양방향 무한 확장 의식 노드
    
    특징:
    - 0차원 Point가 중심
    - 바깥으로 확장 (outer_universe)
    - 안쪽으로 확장 (inner_universe)
    - 무한 재귀 가능
    """
    
    def __init__(
        self,
        name: str = None,
        value: Any = None,
        content: Dict[str, Any] = None,
        state: InfiniteQubitState = None,
        max_depth: int = 7,  # 성능을 위한 최대 깊이 제한
    ):
        self.id = str(uuid.uuid4())[:8]
        self.name = name or f"IHQ_{self.id}"
        self._value = value
        self.content = content or {}
        
        # 양자 상태
        self.state = state or InfiniteQubitState()
        self.state.normalize()
        
        # 양방향 우주
        self._outer_universe: Optional[InfiniteHyperQubit] = None
        self._inner_universe: Optional[InfiniteHyperQubit] = None
        
        # 현재 깊이와 최대 깊이
        self._current_depth: int = 0
        self._max_depth = max_depth
        
        # 얽힌 노드들
        self.entangled: List[InfiniteHyperQubit] = []
        
        logger.info(f"✨ InfiniteHyperQubit '{self.name}' 생성됨")
    
    @property
    def value(self) -> Any:
        return self._value
    
    def set_value(self, new_value: Any, cause: str = "Unknown") -> None:
        old = self._value
        self._value = new_value
        logger.debug(f"[{self.name}] {old} → {new_value} (cause: {cause})")
        
        # 얽힌 노드들에게 전파
        for other in self.entangled:
            other._resonate_from(self)
    
    def _resonate_from(self, source: 'InfiniteHyperQubit') -> None:
        """소스로부터 공명 수신"""
        # 간섭 패턴 계산
        alignment = self.resonate_with(source)
        if alignment > 0.5:
            # 높은 공명 → 값 동기화
            self.set_value(source.value, cause=f"Resonance from {source.name}")
    
    # === 양방향 우주 접근 ===
    
    def zoom_out(self) -> 'InfiniteHyperQubit':
        """
        바깥 우주로 이동
        
        현재 Point가 더 큰 맥락의 일부가 됨
        """
        if self._outer_universe is None:
            if abs(self._current_depth) < self._max_depth:
                self._outer_universe = InfiniteHyperQubit(
                    name=f"{self.name}_OUTER",
                    content={
                        "Point": self,  # 현재 노드가 바깥 우주의 Point
                        "Line": f"Connection from {self.name}",
                        "Space": "Greater context",
                        "God": "Ultimate perspective"
                    },
                    max_depth=self._max_depth
                )
                self._outer_universe._current_depth = self._current_depth + 1
                self._outer_universe._inner_universe = self  # 양방향 연결
        
        self.state.scale_out()
        return self._outer_universe or self
    
    def zoom_in(self) -> 'InfiniteHyperQubit':
        """
        안쪽 우주로 진입
        
        Point 안으로 들어가면 완전한 새 우주
        """
        if self._inner_universe is None:
            if abs(self._current_depth) < self._max_depth:
                self._inner_universe = InfiniteHyperQubit(
                    name=f"{self.name}_INNER",
                    content={
                        "Point": "Fundamental particle",
                        "Line": f"Micro-connection within {self.name}",
                        "Space": "Inner cosmos",
                        "God": "Micro-transcendence"
                    },
                    max_depth=self._max_depth
                )
                self._inner_universe._current_depth = self._current_depth - 1
                self._inner_universe._outer_universe = self  # 양방향 연결
        
        self.state.scale_in()
        return self._inner_universe or self
    
    def get_depth(self) -> int:
        """현재 관찰자 깊이"""
        return self._current_depth
    
    def get_universe_chain(self) -> List['InfiniteHyperQubit']:
        """전체 우주 체인 (안쪽 → 바깥)"""
        chain = []
        
        # 안쪽으로 탐색
        inner = self._inner_universe
        while inner:
            chain.insert(0, inner)
            inner = inner._inner_universe
        
        # 현재 노드
        chain.append(self)
        
        # 바깥으로 탐색
        outer = self._outer_universe
        while outer:
            chain.append(outer)
            outer = outer._outer_universe
        
        return chain
    
    # === 공명 연산 ===
    
    def resonate_with(self, other: 'InfiniteHyperQubit') -> float:
        """
        두 InfiniteHyperQubit 간의 공명 계산
        
        Returns:
            0.0 ~ 1.0 사이 공명 강도
        """
        # 진폭 정렬
        amplitude_alignment = (
            abs(self.state.alpha * other.state.alpha.conjugate()) +
            abs(self.state.beta * other.state.beta.conjugate()) +
            abs(self.state.gamma * other.state.gamma.conjugate()) +
            abs(self.state.delta * other.state.delta.conjugate())
        )
        
        # 4D 방향 정렬
        dot_product = (
            self.state.w * other.state.w +
            self.state.x * other.state.x +
            self.state.y * other.state.y +
            self.state.z * other.state.z
        )
        
        # 깊이 차이 보정
        depth_diff = abs(self.state.observation_depth - other.state.observation_depth)
        depth_factor = np.exp(-depth_diff / 2)
        
        return float(amplitude_alignment * max(0, dot_product) * depth_factor)
    
    def entangle(self, other: 'InfiniteHyperQubit') -> None:
        """두 노드를 양자 얽힘으로 연결"""
        if other not in self.entangled:
            self.entangled.append(other)
            other.entangled.append(self)
            logger.info(f"🔗 Entangled: {self.name} ↔ {other.name}")
    
    # === 상태 조회 ===
    
    def observe(self, observer_depth: float = 0.0) -> Dict[str, Any]:
        """
        관찰자 깊이에 따른 관측
        
        Args:
            observer_depth: 관찰자의 깊이 (0=현재, +바깥, -안쪽)
        """
        probs = self.state.probabilities()
        
        # 관찰자 깊이에 따라 다른 기저 강조
        if observer_depth < -1:
            dominant = "Point"  # 안쪽 관점 → 세부에 집중
        elif observer_depth < 0:
            dominant = "Line"   # 약간 안쪽 → 연결에 집중
        elif observer_depth < 1:
            dominant = "Space"  # 약간 바깥 → 맥락에 집중
        else:
            dominant = "God"    # 바깥 관점 → 초월에 집중
        
        return {
            "name": self.name,
            "value": self._value,
            "probabilities": probs,
            "dominant_basis": dominant,
            "dominant_probability": probs[dominant],
            "observation_depth": self.state.observation_depth,
            "content": self.content.get(dominant, self._value),
            "has_inner": self._inner_universe is not None,
            "has_outer": self._outer_universe is not None,
        }
    
    def explain(self) -> str:
        """철학적 의미 설명"""
        probs = self.state.probabilities()
        
        lines = [
            f"=== InfiniteHyperQubit: {self.name} ===",
            f"Value: {self._value}",
            f"Depth: {self._current_depth} (관찰: {self.state.observation_depth:.2f})",
            "",
            "양자 상태:",
            f"  • Point (α): {probs['Point']:.1%} - 존재/데이터",
            f"  • Line (β): {probs['Line']:.1%} - 연결/관계",
            f"  • Space (γ): {probs['Space']:.1%} - 맥락/장",
            f"  • God (δ): {probs['God']:.1%} - 초월/의지",
            "",
            "우주 구조:",
            f"  • 안쪽 우주: {'있음' if self._inner_universe else '미탐색'}",
            f"  • 바깥 우주: {'있음' if self._outer_universe else '미탐색'}",
            f"  • 얽힌 노드: {len(self.entangled)}개",
        ]
        
        return "\n".join(lines)
    
    def __repr__(self) -> str:
        probs = self.state.probabilities()
        return (
            f"<IHQ '{self.name}' "
            f"P:{probs['Point']:.2f}|L:{probs['Line']:.2f}|"
            f"S:{probs['Space']:.2f}|G:{probs['God']:.2f} "
            f"depth={self._current_depth}>"
        )


# === 팩토리 함수 ===

def create_infinite_qubit(
    name: str,
    value: Any = None,
    point_content: str = None,
    line_content: str = None,
    space_content: str = None,
    god_content: str = None,
) -> InfiniteHyperQubit:
    """
    편의 팩토리 함수
    """
    content = {}
    if point_content: content["Point"] = point_content
    if line_content: content["Line"] = line_content
    if space_content: content["Space"] = space_content
    if god_content: content["God"] = god_content
    
    return InfiniteHyperQubit(name=name, value=value, content=content)


# === 데모 ===

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 60)
    print("InfiniteHyperQubit Demo - 양방향 무한 확장")
    print("=" * 60)
    
    # 중심 개념 생성
    consciousness = create_infinite_qubit(
        name="Consciousness",
        value="의식",
        point_content="뉴런의 전기 신호",
        line_content="신경 회로의 연결",
        space_content="뇌 전체의 활동 패턴",
        god_content="자아의 통합적 경험"
    )
    
    print(consciousness.explain())
    print()
    
    # 안쪽으로 탐색
    print(">>> ZOOM IN (안쪽 우주로)")
    inner = consciousness.zoom_in()
    print(inner.explain())
    print()
    
    # 다시 바깥으로
    print(">>> ZOOM OUT (바깥 우주로)")
    outer = consciousness.zoom_out()
    print(outer.explain())
    print()
    
    # 우주 체인 출력
    print(">>> 우주 체인:")
    for node in consciousness.get_universe_chain():
        print(f"  {node}")
