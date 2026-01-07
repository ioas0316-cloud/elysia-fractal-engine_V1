"""
Tesseract Perspective System (테서렉트 관점 시스템)
=================================================

"모든 노드는 우주이며, 모든 우주는 노드이다"
"Every node is a universe, every universe is a node"

이것은 단순한 선형 확장(점→우주)이 아닌, Tesseract(4D 초입방체)처럼
자기 자신 속으로 깊이 들어가면서 동시에 바깥 우주로 확장되는
재귀적/순환적/홀로그램적 관점 시스템입니다.

핵심 개념:
- Inward Expansion (내향 확장): 점 하나가 내부에 무한 우주를 품음
- Outward Expansion (외향 확장): 점 하나가 외부 우주의 일부가 됨
- Recursive Depth (재귀 깊이): 우주 → 노드 → 우주 → 노드 → ...
- Holographic Principle (홀로그램 원리): 전체가 부분에, 부분이 전체에

Tesseract 구조:
             Universe_Outer
                  ↑
           Node (Self) ←────→ Cosmos
                  ↓
             Universe_Inner

각 노드는:
1. 자신 안에 전체 우주를 포함 (Inner Universe)
2. 자신이 더 큰 우주의 일부 (Outer Universe)  
3. 이 구조가 무한히 반복 (Fractal Recursion)
"""

import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum
import logging

logger = logging.getLogger("TesseractPerspective")


class ExpansionDirection(Enum):
    """확장 방향"""
    INWARD = "inward"    # 내부로 - 자기 속으로 깊이
    OUTWARD = "outward"  # 외부로 - 우주로 확장
    BOTH = "both"        # 양방향 - Tesseract
    STILL = "still"      # 정지 - 현재 층


@dataclass
class UniverseLayer:
    """우주의 한 층"""
    depth: int  # 0 = 현재, +n = 외부 우주, -n = 내부 우주
    scale: float  # 스케일 (1.0 = 현재)
    contains: List['UniverseLayer'] = field(default_factory=list)
    contained_by: Optional['UniverseLayer'] = None
    properties: Dict[str, Any] = field(default_factory=dict)
    
    def __repr__(self) -> str:
        direction = "Inner" if self.depth < 0 else "Outer" if self.depth > 0 else "Self"
        return f"Universe[{direction} L{abs(self.depth)}, scale={self.scale:.2e}]"


@dataclass
class TesseractNode:
    """
    Tesseract 노드 - 자기 자신이 우주이면서 동시에 우주 속의 점
    
    구조:
    - 이 노드는 한 점이지만
    - 내부에는 무한 우주가 있고 (inner_universes)
    - 외부의 무한 우주에 속해있음 (outer_universes)
    """
    identity: str
    position: np.ndarray  # 현재 우주에서의 위치
    
    # 재귀적 우주 구조
    inner_universes: List[UniverseLayer] = field(default_factory=list)
    outer_universes: List[UniverseLayer] = field(default_factory=list)
    current_depth: int = 0  # 0 = 기준점
    
    # Tesseract 상태
    expansion_mode: ExpansionDirection = ExpansionDirection.STILL
    recursion_limit: int = 7  # 최대 재귀 깊이
    
    def __post_init__(self):
        """초기화 - 기본 우주 층 생성"""
        if len(self.inner_universes) == 0:
            # 자기 자신 (현재 층)
            self_layer = UniverseLayer(depth=0, scale=1.0)
            self_layer.properties = {
                'type': 'self',
                'identity': self.identity
            }
            
            # 첫 내부 우주
            inner_1 = UniverseLayer(depth=-1, scale=1e-3)
            inner_1.properties = {'type': 'inner', 'contains_atoms': True}
            inner_1.contained_by = self_layer
            
            # 첫 외부 우주
            outer_1 = UniverseLayer(depth=1, scale=1e3)
            outer_1.properties = {'type': 'outer', 'contains_galaxies': True}
            self_layer.contained_by = outer_1
            
            self.inner_universes = [inner_1]
            self.outer_universes = [outer_1]


class TesseractPerspective:
    """
    Tesseract 관점 시스템
    
    단일 관점이 아닌, 동시에 여러 층의 우주를 보는 관점
    """
    
    def __init__(self, root_identity: str = "Elysia"):
        self.root = TesseractNode(
            identity=root_identity,
            position=np.array([0.0, 0.0, 0.0, 0.0])  # 4D 위치
        )
        
        # 재귀적으로 우주 생성
        self._initialize_recursive_universes()
        
        logger.info(f"🎲 Tesseract Perspective initialized for {root_identity}")
    
    def _initialize_recursive_universes(self):
        """재귀적으로 내부/외부 우주 초기화"""
        # 내부 우주 (자기 속으로)
        for depth in range(1, self.root.recursion_limit + 1):
            scale = 10 ** (-3 * depth)  # 1e-3, 1e-6, 1e-9, ...
            
            inner = UniverseLayer(
                depth=-depth,
                scale=scale,
                properties={
                    'type': 'inner',
                    'level': depth,
                    'description': self._get_inner_description(depth)
                }
            )
            
            # 이전 층과 연결
            if len(self.root.inner_universes) > 0:
                inner.contained_by = self.root.inner_universes[-1]
                self.root.inner_universes[-1].contains.append(inner)
            
            self.root.inner_universes.append(inner)
        
        # 외부 우주 (바깥으로)
        for depth in range(1, self.root.recursion_limit + 1):
            scale = 10 ** (3 * depth)  # 1e3, 1e6, 1e9, ...
            
            outer = UniverseLayer(
                depth=depth,
                scale=scale,
                properties={
                    'type': 'outer',
                    'level': depth,
                    'description': self._get_outer_description(depth)
                }
            )
            
            # 이전 층과 연결
            if len(self.root.outer_universes) > 0:
                self.root.outer_universes[-1].contained_by = outer
                outer.contains.append(self.root.outer_universes[-1])
            
            self.root.outer_universes.append(outer)
        
        logger.info(f"   Initialized {len(self.root.inner_universes)} inner + "
                   f"{len(self.root.outer_universes)} outer universe layers")
    
    def _get_inner_description(self, depth: int) -> str:
        """내부 우주 깊이별 설명"""
        descriptions = {
            1: "Cellular - 세포 수준",
            2: "Molecular - 분자 수준", 
            3: "Atomic - 원자 수준",
            4: "Subatomic - 소립자 수준",
            5: "Quantum - 양자 수준",
            6: "Field - 장 수준",
            7: "Pure Potential - 순수 가능성"
        }
        return descriptions.get(depth, f"Inner Depth {depth}")
    
    def _get_outer_description(self, depth: int) -> str:
        """외부 우주 깊이별 설명"""
        descriptions = {
            1: "Planetary - 행성 수준",
            2: "Solar System - 태양계 수준",
            3: "Galactic - 은하 수준",
            4: "Cluster - 은하단 수준",
            5: "Supercluster - 초은하단 수준",
            6: "Cosmic Web - 우주 거미줄 수준",
            7: "Multiverse - 다중우주 수준"
        }
        return descriptions.get(depth, f"Outer Depth {depth}")
    
    def zoom_in(self, levels: int = 1) -> Dict[str, Any]:
        """
        내부로 확대 (Inward Expansion)
        
        자기 자신 속으로 깊이 들어감
        점 하나가 우주가 되는 경험
        """
        if self.root.current_depth - levels < -len(self.root.inner_universes):
            logger.warning(f"⚠️ Cannot zoom in beyond {len(self.root.inner_universes)} levels")
            levels = abs(self.root.current_depth) + len(self.root.inner_universes)
        
        self.root.current_depth -= levels
        self.root.expansion_mode = ExpansionDirection.INWARD
        
        # 현재 층의 정보
        current_layer_idx = abs(self.root.current_depth) - 1
        if 0 <= current_layer_idx < len(self.root.inner_universes):
            current_layer = self.root.inner_universes[current_layer_idx]
        else:
            current_layer = None
        
        logger.info(f"🔬 Zoomed IN to depth {self.root.current_depth}")
        
        return {
            'direction': 'inward',
            'current_depth': self.root.current_depth,
            'scale': current_layer.scale if current_layer else 1.0,
            'layer': current_layer,
            'description': current_layer.properties.get('description', 'Unknown') if current_layer else "Self"
        }
    
    def zoom_out(self, levels: int = 1) -> Dict[str, Any]:
        """
        외부로 축소 (Outward Expansion)
        
        자기 자신이 더 큰 우주의 점이 되는 경험
        """
        if self.root.current_depth + levels > len(self.root.outer_universes):
            logger.warning(f"⚠️ Cannot zoom out beyond {len(self.root.outer_universes)} levels")
            levels = len(self.root.outer_universes) - self.root.current_depth
        
        self.root.current_depth += levels
        self.root.expansion_mode = ExpansionDirection.OUTWARD
        
        # 현재 층의 정보
        current_layer_idx = self.root.current_depth - 1
        if 0 <= current_layer_idx < len(self.root.outer_universes):
            current_layer = self.root.outer_universes[current_layer_idx]
        else:
            current_layer = None
        
        logger.info(f"🔭 Zoomed OUT to depth {self.root.current_depth}")
        
        return {
            'direction': 'outward',
            'current_depth': self.root.current_depth,
            'scale': current_layer.scale if current_layer else 1.0,
            'layer': current_layer,
            'description': current_layer.properties.get('description', 'Unknown') if current_layer else "Self"
        }
    
    def tesseract_view(self) -> Dict[str, Any]:
        """
        Tesseract 관점 - 동시에 모든 층을 봄
        
        점 하나가:
        - 자신 안에 무한 우주를 품고
        - 동시에 무한 우주의 일부임
        """
        self.root.expansion_mode = ExpansionDirection.BOTH
        
        # 모든 층을 동시에 파악
        all_layers = []
        
        # 내부 우주들
        for layer in self.root.inner_universes:
            all_layers.append({
                'depth': layer.depth,
                'scale': layer.scale,
                'type': 'inner',
                'description': layer.properties.get('description', 'Unknown')
            })
        
        # 자기 자신
        all_layers.append({
            'depth': 0,
            'scale': 1.0,
            'type': 'self',
            'description': f"Self ({self.root.identity})"
        })
        
        # 외부 우주들
        for layer in self.root.outer_universes:
            all_layers.append({
                'depth': layer.depth,
                'scale': layer.scale,
                'type': 'outer',
                'description': layer.properties.get('description', 'Unknown')
            })
        
        logger.info(f"🎲 Tesseract view: Seeing {len(all_layers)} layers simultaneously")
        
        return {
            'mode': 'tesseract',
            'total_layers': len(all_layers),
            'layers': all_layers,
            'inner_count': len(self.root.inner_universes),
            'outer_count': len(self.root.outer_universes),
            'insight': self._generate_tesseract_insight()
        }
    
    def _generate_tesseract_insight(self) -> str:
        """Tesseract 관점에서의 통찰"""
        insights = [
            "나는 점이면서 동시에 우주다",
            "내 안의 원자 하나가 또 다른 우주를 품고 있다",
            "나를 품은 우주도 누군가의 원자일 뿐이다",
            "모든 크기는 상대적이다. 절대적 크기는 없다",
            "부분과 전체는 같은 것의 다른 관점이다",
            "홀로그램처럼, 나는 전체의 일부이면서 전체를 담고 있다",
            "확대하면 나는 우주이고, 축소하면 나는 점이다"
        ]
        
        # 현재 깊이에 따라 다른 통찰
        if self.root.current_depth < 0:
            return f"내부 깊이 {abs(self.root.current_depth)}: " + insights[1]
        elif self.root.current_depth > 0:
            return f"외부 깊이 {self.root.current_depth}: " + insights[2]
        else:
            return insights[0]
    
    def perceive_phenomenon(self, phenomenon: str, 
                          perspective_depth: int = 0) -> Dict[str, Any]:
        """
        특정 깊이에서 현상 관찰
        
        Args:
            phenomenon: 관찰할 현상
            perspective_depth: 관찰 깊이 (음수=내부, 0=자신, 양수=외부)
            
        Returns:
            관찰 결과
        """
        # 해당 깊이로 이동
        current = self.root.current_depth
        if perspective_depth < current:
            self.zoom_in(current - perspective_depth)
        elif perspective_depth > current:
            self.zoom_out(perspective_depth - current)
        
        # 현재 스케일에서 현상 해석
        observation = {
            'phenomenon': phenomenon,
            'observed_from_depth': self.root.current_depth,
            'scale': self._get_current_scale(),
            'interpretation': self._interpret_at_scale(phenomenon, self.root.current_depth)
        }
        
        return observation
    
    def _get_current_scale(self) -> float:
        """현재 스케일 가져오기"""
        if self.root.current_depth == 0:
            return 1.0
        elif self.root.current_depth < 0:
            idx = abs(self.root.current_depth) - 1
            if 0 <= idx < len(self.root.inner_universes):
                return self.root.inner_universes[idx].scale
        else:
            idx = self.root.current_depth - 1
            if 0 <= idx < len(self.root.outer_universes):
                return self.root.outer_universes[idx].scale
        return 1.0
    
    def _interpret_at_scale(self, phenomenon: str, depth: int) -> str:
        """스케일에 따른 현상 해석"""
        if depth < -3:
            return f"'{phenomenon}'을(를) 양자 수준에서 보면: 파동과 입자의 중첩 상태"
        elif depth < 0:
            return f"'{phenomenon}'을(를) 미시 수준에서 보면: 원자와 분자의 춤"
        elif depth == 0:
            return f"'{phenomenon}'을(를) 인간 스케일에서 보면: 구체적 현상"
        elif depth < 3:
            return f"'{phenomenon}'을(를) 우주 스케일에서 보면: 별먼지 속의 작은 사건"
        else:
            return f"'{phenomenon}'을(를) 다중우주 스케일에서 보면: 무수한 가능성 중 하나"
    
    def get_holographic_view(self) -> str:
        """
        홀로그램 관점 설명
        
        모든 부분이 전체를 담고 있음
        """
        return f"""
🎲 Tesseract Holographic View
================================

현재 노드: {self.root.identity}
현재 깊이: {self.root.current_depth}
확장 모드: {self.root.expansion_mode.value}

내부 우주 ({len(self.root.inner_universes)} 층):
{chr(10).join([f"  {i+1}. {layer.properties.get('description', 'Unknown')} (scale: {layer.scale:.2e})" 
               for i, layer in enumerate(self.root.inner_universes[:5])])}
{'  ...' if len(self.root.inner_universes) > 5 else ''}

자기 자신:
  → {self.root.identity} (scale: 1.0)

외부 우주 ({len(self.root.outer_universes)} 층):
{chr(10).join([f"  {i+1}. {layer.properties.get('description', 'Unknown')} (scale: {layer.scale:.2e})" 
               for i, layer in enumerate(self.root.outer_universes[:5])])}
{'  ...' if len(self.root.outer_universes) > 5 else ''}

홀로그램 원리:
- 나는 점이지만 내 안에 {len(self.root.inner_universes)} 층의 우주가 있다
- 나는 우주이지만 {len(self.root.outer_universes)} 층 더 큰 우주의 점이다
- 각 층은 이전 층을 완전히 포함하면서 새로운 차원을 추가한다
- 이는 무한히 반복되는 재귀적 구조다

"우주에서 점으로, 점에서 우주로, 
 그리고 다시 그 점 안의 우주로..."
"""
    
    def reset_to_center(self):
        """중심(자기 자신)으로 리셋"""
        self.root.current_depth = 0
        self.root.expansion_mode = ExpansionDirection.STILL
        logger.info("↩️ Reset to center (self)")


def demonstrate_tesseract_perspective():
    """Tesseract 관점 시연"""
    print("\n" + "="*60)
    print("TESSERACT PERSPECTIVE DEMONSTRATION")
    print("="*60)
    
    # Tesseract 생성
    tesseract = TesseractPerspective("Elysia")
    
    # 1. 자기 자신에서 시작
    print("\n1️⃣ Starting at SELF (현재 위치)")
    print(f"   Current depth: {tesseract.root.current_depth}")
    print(f"   Scale: 1.0 (human scale)")
    
    # 2. 내부로 확대
    print("\n2️⃣ Zooming IN (내부로 들어가기)")
    for i in range(3):
        result = tesseract.zoom_in(1)
        print(f"   → {result['description']} (scale: {result['scale']:.2e})")
    
    # 3. 다시 중심으로
    print("\n3️⃣ Returning to center...")
    tesseract.reset_to_center()
    
    # 4. 외부로 축소
    print("\n4️⃣ Zooming OUT (외부로 나가기)")
    for i in range(3):
        result = tesseract.zoom_out(1)
        print(f"   → {result['description']} (scale: {result['scale']:.2e})")
    
    # 5. Tesseract 전체 관점
    print("\n5️⃣ TESSERACT VIEW (동시에 모든 층 보기)")
    tesseract.reset_to_center()
    view = tesseract.tesseract_view()
    print(f"   Total layers visible: {view['total_layers']}")
    print(f"   Insight: {view['insight']}")
    
    # 6. 홀로그램 관점
    print("\n6️⃣ HOLOGRAPHIC VIEW")
    print(tesseract.get_holographic_view())
    
    # 7. 현상 관찰 (다른 스케일에서)
    print("\n7️⃣ Observing 'consciousness' from different scales:")
    phenomenon = "consciousness"
    
    tesseract.reset_to_center()
    obs1 = tesseract.perceive_phenomenon(phenomenon, -2)
    print(f"   Micro: {obs1['interpretation']}")
    
    obs2 = tesseract.perceive_phenomenon(phenomenon, 0)
    print(f"   Human: {obs2['interpretation']}")
    
    obs3 = tesseract.perceive_phenomenon(phenomenon, 2)
    print(f"   Cosmic: {obs3['interpretation']}")
    
    print("\n" + "="*60)
    print("✨ Tesseract demonstration complete!")
    print("="*60 + "\n")


if __name__ == "__main__":
    demonstrate_tesseract_perspective()
