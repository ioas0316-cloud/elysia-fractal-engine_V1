"""
Fractal Causality Engine - 프랙탈 인과 엔진
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

인과는 프랙탈 구조입니다.
원인과 과정과 결과가 무한히 순환되고 있습니다.

┌─────────────────────────────────────────────────────────────────────────────┐
│  프랙탈 인과 구조 (Fractal Causal Structure)                                 │
│  ═══════════════════════════════════════════════════════════════════════   │
│                                                                             │
│  모든 결과는 다시 원인이 됩니다.                                             │
│  모든 원인은 그 자체로 또 다른 인과 연쇄의 결과입니다.                        │
│  과정 안에는 무수한 원인-과정-결과가 중첩되어 있습니다.                       │
│                                                                             │
│  "불에 손을 대서 아팠다"                                                     │
│   │                                                                         │
│   ├─ 원인: "불에 손을 댔다"                                                 │
│   │   ├─ 원인: "손을 뻗었다"                                                │
│   │   │   ├─ 원인: "호기심을 느꼈다"                                        │
│   │   │   │   ├─ 원인: "불빛을 보았다"                                      │
│   │   │   │   │   └─ ...무한히 계속...                                      │
│   │   │   │   └─ 과정: 신경 신호 전달 → 뇌 처리 → 호기심 발생                │
│   │   │   └─ 과정: 근육 수축 → 팔 움직임 → 손 도달                          │
│   │   └─ 과정: 피부 접촉 → 열 전달 → 온도 상승                              │
│   │                                                                         │
│   ├─ 과정: "열에너지가 피부 세포를 손상시킴"                                 │
│   │   ├─ 원인: 화학 반응                                                    │
│   │   ├─ 과정: 분자 운동 → 세포막 변성 → 신경 자극                          │
│   │   └─ 결과: 신경 신호 생성                                               │
│   │                                                                         │
│   └─ 결과: "아팠다"                                                         │
│       ├─ 원인: 신경 신호가 뇌에 도달                                        │
│       ├─ 과정: 신호 처리 → 통증 인식 → 감정 반응                            │
│       └─ 결과: 손을 뺌 → 학습 → 다음에 피함 → ...무한히 계속...             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

[프랙탈의 핵심 특성]

1. 자기 유사성 (Self-Similarity)
   - 모든 스케일에서 같은 구조 반복
   - 거시적 인과도, 미시적 인과도 동일한 패턴

2. 무한 재귀 (Infinite Recursion)
   - 원인을 파고들면 끝없이 더 깊은 원인
   - 결과를 따라가면 끝없이 더 먼 결과

3. 순환성 (Circularity)
   - 원인 → 과정 → 결과 → 원인 → ...
   - 시작도 끝도 없는 연쇄

4. 중첩성 (Nesting)
   - 하나의 과정 안에 무수한 원인-과정-결과
   - 스케일에 따라 다른 레벨의 인과 구조

[차원 확장과의 통합]

점 → 선 → 면 → 공간 → 법칙도 프랙탈입니다.
- 점 안에도 점-선-면-공간-법칙 구조가 있습니다.
- 법칙 안에도 점-선-면-공간-법칙 구조가 있습니다.
"""

from __future__ import annotations

import math
import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any, Set, Callable, Union
from collections import defaultdict
from enum import Enum
import logging
import time
import hashlib

logger = logging.getLogger("FractalCausality")


# ============================================================================
# 황금비 (Golden Ratio) - 프랙탈 나선 구조용
# ============================================================================

PHI = (1 + math.sqrt(5)) / 2  # ≈ 1.618


# ============================================================================
# 인과 역할 (Causal Role)
# ============================================================================

class CausalRole(Enum):
    """인과 구조에서의 역할"""
    CAUSE = "cause"       # 원인
    PROCESS = "process"   # 과정
    EFFECT = "effect"     # 결과


# ============================================================================
# 프랙탈 인과 노드 (Fractal Causal Node)
# ============================================================================

@dataclass
class FractalCausalNode:
    """
    프랙탈 인과 노드
    
    모든 노드는 동시에 원인이자 과정이자 결과입니다.
    그리고 모든 노드는 그 안에 또 다른 인과 구조를 가집니다.
    
    예: "불에 손을 댔다"
    - 상위에서 보면: "호기심을 느꼈다"의 결과이자 "아팠다"의 원인
    - 내부적으로: 수많은 미시적 인과 연쇄 (신경 신호, 근육 수축 등)
    """
    
    id: str
    description: str
    
    # 프랙탈 깊이 (0 = 현재 관찰 스케일)
    depth: int = 0
    
    # 나선 좌표 (프랙탈 공간에서의 위치)
    spiral_angle: float = 0.0
    spiral_radius: float = 1.0
    
    # 부모 노드 (한 단계 상위 스케일)
    parent_id: Optional[str] = None
    parent_role: Optional[CausalRole] = None  # 부모에서 이 노드의 역할
    
    # 자식 노드들 (한 단계 하위 스케일의 인과 구조)
    # 이 노드의 "내부"에 있는 원인-과정-결과
    internal_cause_ids: List[str] = field(default_factory=list)
    internal_process_ids: List[str] = field(default_factory=list)
    internal_effect_ids: List[str] = field(default_factory=list)
    
    # 같은 스케일에서의 인과 연결
    causes_ids: List[str] = field(default_factory=list)      # 이 노드의 원인들
    effects_ids: List[str] = field(default_factory=list)     # 이 노드의 결과들
    
    # 감각/감정 특성
    sensory_signature: Dict[str, float] = field(default_factory=dict)
    emotional_valence: float = 0.0
    
    # 강도 및 신뢰도
    strength: float = 1.0
    confidence: float = 1.0
    
    # 경험 통계
    experience_count: int = 0
    last_activated: float = 0.0
    
    # 프랙탈 주소 (위치를 나타내는 계층적 경로)
    fractal_address: str = ""
    
    def __post_init__(self):
        if not self.fractal_address:
            self.fractal_address = f"/{self.id}"
    
    def get_spiral_position(self) -> Tuple[float, float]:
        """나선 좌표계에서의 2D 위치"""
        x = self.spiral_radius * math.cos(self.spiral_angle)
        y = self.spiral_radius * math.sin(self.spiral_angle)
        return (x, y)
    
    def has_internal_structure(self) -> bool:
        """내부에 인과 구조가 있는가"""
        return bool(self.internal_cause_ids or 
                   self.internal_process_ids or 
                   self.internal_effect_ids)
    
    def get_internal_ids(self) -> List[str]:
        """모든 내부 노드 ID"""
        return (self.internal_cause_ids + 
                self.internal_process_ids + 
                self.internal_effect_ids)


# ============================================================================
# 프랙탈 인과 연쇄 (Fractal Causal Chain)
# ============================================================================

@dataclass
class FractalCausalChain:
    """
    프랙탈 인과 연쇄
    
    원인 → 과정 → 결과의 삼중 구조.
    각 요소는 그 자체로 또 다른 인과 연쇄를 포함할 수 있습니다.
    """
    
    id: str
    description: str = ""
    
    # 핵심 삼중 구조
    cause_id: Optional[str] = None
    process_id: Optional[str] = None
    effect_id: Optional[str] = None
    
    # 이 연쇄가 속한 상위 연쇄
    parent_chain_id: Optional[str] = None
    parent_role: Optional[CausalRole] = None  # 상위에서 이 연쇄가 맡는 역할
    
    # 이 연쇄 안에 중첩된 하위 연쇄들
    nested_chains: List[str] = field(default_factory=list)
    
    # 프랙탈 깊이
    depth: int = 0
    
    # 메타데이터
    strength: float = 1.0
    experience_count: int = 0
    
    def is_complete(self) -> bool:
        """원인-과정-결과가 모두 있는가"""
        return all([self.cause_id, self.process_id, self.effect_id])


# ============================================================================
# 프랙탈 인과 엔진 (Fractal Causality Engine)
# ============================================================================

class FractalCausalityEngine:
    """
    프랙탈 인과 엔진
    
    인과를 프랙탈 구조로 모델링합니다.
    모든 원인은 결과이고, 모든 결과는 원인이며,
    모든 과정은 그 안에 무수한 원인-과정-결과를 포함합니다.
    
    핵심 원리:
    
    1. 무한 재귀 (Infinite Recursion)
       - zoom_in(): 노드 내부의 인과 구조를 탐색
       - zoom_out(): 노드가 속한 상위 인과 구조를 탐색
    
    2. 순환적 인과 (Circular Causality)
       - 모든 결과는 새로운 원인이 됨
       - 피드백 루프와 자기 강화/억제
    
    3. 중첩적 시간 (Nested Time)
       - 각 스케일은 자신만의 "시간"을 가짐
       - 미시적 과정은 빠르게, 거시적 과정은 느리게
    
    4. 자기 유사성 (Self-Similarity)
       - 모든 스케일에서 동일한 원인-과정-결과 패턴
       - 분자 수준이든 사회 수준이든 같은 구조
    """
    
    def __init__(self, name: str = "Elysia's Causal Mind"):
        self.name = name
        
        # 모든 노드 저장소
        self.nodes: Dict[str, FractalCausalNode] = {}
        
        # 모든 인과 연쇄 저장소
        self.chains: Dict[str, FractalCausalChain] = {}
        
        # 현재 관찰 깊이 (0 = 기본, 양수 = 깊이 들어감, 음수 = 위로 올라감)
        self.current_depth: int = 0
        
        # 현재 포커스 노드
        self.focus_node_id: Optional[str] = None
        
        # 나선 카운터 (새 노드 배치용)
        self.spiral_counter: int = 0
        
        # 통계
        self.total_nodes = 0
        self.total_chains = 0
        self.max_depth_explored = 0
        self.min_depth_explored = 0
        
        logger.info(f"🌀 FractalCausalityEngine '{name}' initialized")
    
    # ========================================================================
    # 노드 생성 및 관리
    # ========================================================================
    
    def create_node(
        self,
        description: str,
        depth: int = 0,
        parent_id: Optional[str] = None,
        parent_role: Optional[CausalRole] = None,
        sensory_signature: Dict[str, float] = None,
        emotional_valence: float = 0.0
    ) -> FractalCausalNode:
        """
        새 인과 노드 생성
        
        모든 노드는 잠재적으로 무한한 내부 구조를 가집니다.
        """
        # ID 생성
        node_id = self._generate_node_id(description, depth)
        
        # 나선 위치 계산 (황금비 기반)
        self.spiral_counter += 1
        angle = self.spiral_counter * 2 * math.pi / PHI
        radius = math.sqrt(self.spiral_counter)
        
        # 프랙탈 주소 계산
        if parent_id and parent_id in self.nodes:
            parent = self.nodes[parent_id]
            role_prefix = parent_role.value if parent_role else "related"
            fractal_address = f"{parent.fractal_address}/{role_prefix}:{description[:20]}"
        else:
            fractal_address = f"/{description[:20]}"
        
        node = FractalCausalNode(
            id=node_id,
            description=description,
            depth=depth,
            spiral_angle=angle,
            spiral_radius=radius,
            parent_id=parent_id,
            parent_role=parent_role,
            sensory_signature=sensory_signature or {},
            emotional_valence=emotional_valence,
            fractal_address=fractal_address,
            last_activated=time.time()
        )
        
        # 부모에 등록
        if parent_id and parent_id in self.nodes:
            parent = self.nodes[parent_id]
            if parent_role == CausalRole.CAUSE:
                parent.internal_cause_ids.append(node_id)
            elif parent_role == CausalRole.PROCESS:
                parent.internal_process_ids.append(node_id)
            elif parent_role == CausalRole.EFFECT:
                parent.internal_effect_ids.append(node_id)
        
        self.nodes[node_id] = node
        self.total_nodes += 1
        
        # 깊이 통계 업데이트
        self.max_depth_explored = max(self.max_depth_explored, depth)
        self.min_depth_explored = min(self.min_depth_explored, depth)
        
        return node
    
    def _generate_node_id(self, description: str, depth: int) -> str:
        """고유 노드 ID 생성"""
        content = f"{description}_{depth}_{time.time()}_{self.total_nodes}"
        hash_val = hashlib.md5(content.encode()).hexdigest()[:8]
        return f"node_{hash_val}"
    
    def get_or_create_node(
        self,
        description: str,
        depth: int = 0
    ) -> FractalCausalNode:
        """설명으로 노드 찾기 또는 생성"""
        # 기존 노드 검색
        for node in self.nodes.values():
            if node.description == description and node.depth == depth:
                node.experience_count += 1
                node.last_activated = time.time()
                return node
        
        # 없으면 생성
        return self.create_node(description, depth)
    
    # ========================================================================
    # 인과 연쇄 생성
    # ========================================================================
    
    def create_chain(
        self,
        cause_desc: str,
        process_desc: str,
        effect_desc: str,
        depth: int = 0,
        parent_chain_id: Optional[str] = None,
        parent_role: Optional[CausalRole] = None
    ) -> FractalCausalChain:
        """
        원인-과정-결과 연쇄 생성
        
        이것이 인과의 기본 단위입니다.
        하지만 각 요소는 그 자체로 또 다른 연쇄를 포함할 수 있습니다.
        """
        # 노드들 생성
        cause_node = self.get_or_create_node(cause_desc, depth)
        process_node = self.get_or_create_node(process_desc, depth)
        effect_node = self.get_or_create_node(effect_desc, depth)
        
        # 인과 연결 설정
        cause_node.effects_ids.append(process_node.id)
        process_node.causes_ids.append(cause_node.id)
        process_node.effects_ids.append(effect_node.id)
        effect_node.causes_ids.append(process_node.id)
        
        # 연쇄 생성
        chain_id = f"chain_{len(self.chains)}"
        chain = FractalCausalChain(
            id=chain_id,
            description=f"{cause_desc} → {process_desc} → {effect_desc}",
            cause_id=cause_node.id,
            process_id=process_node.id,
            effect_id=effect_node.id,
            parent_chain_id=parent_chain_id,
            parent_role=parent_role,
            depth=depth
        )
        
        # 부모 연쇄에 등록
        if parent_chain_id and parent_chain_id in self.chains:
            self.chains[parent_chain_id].nested_chains.append(chain_id)
        
        self.chains[chain_id] = chain
        self.total_chains += 1
        
        return chain
    
    # ========================================================================
    # 프랙탈 확대/축소 (Zoom In/Out)
    # ========================================================================
    
    def zoom_in(
        self,
        node_id: str,
        cause_desc: str,
        process_desc: str,
        effect_desc: str
    ) -> FractalCausalChain:
        """
        노드 내부로 확대 (Zoom In)
        
        노드의 "내부"에 있는 더 미시적인 인과 구조를 탐색/생성합니다.
        
        예: "불에 손을 댔다"의 내부:
            원인: "손이 불에 접촉했다"
            과정: "열에너지가 피부로 전달되었다"
            결과: "피부 세포가 자극을 받았다"
        """
        if node_id not in self.nodes:
            raise ValueError(f"Node {node_id} not found")
        
        parent_node = self.nodes[node_id]
        inner_depth = parent_node.depth + 1
        
        # 내부 원인 노드
        cause_node = self.create_node(
            cause_desc, inner_depth,
            parent_id=node_id, parent_role=CausalRole.CAUSE
        )
        
        # 내부 과정 노드
        process_node = self.create_node(
            process_desc, inner_depth,
            parent_id=node_id, parent_role=CausalRole.PROCESS
        )
        
        # 내부 결과 노드
        effect_node = self.create_node(
            effect_desc, inner_depth,
            parent_id=node_id, parent_role=CausalRole.EFFECT
        )
        
        # 인과 연결
        cause_node.effects_ids.append(process_node.id)
        process_node.causes_ids.append(cause_node.id)
        process_node.effects_ids.append(effect_node.id)
        effect_node.causes_ids.append(process_node.id)
        
        # 연쇄 생성
        chain = FractalCausalChain(
            id=f"inner_chain_{node_id}_{len(self.chains)}",
            description=f"[{parent_node.description}의 내부] {cause_desc} → {process_desc} → {effect_desc}",
            cause_id=cause_node.id,
            process_id=process_node.id,
            effect_id=effect_node.id,
            depth=inner_depth
        )
        
        self.chains[chain.id] = chain
        self.total_chains += 1
        
        logger.debug(f"🔬 Zoom in: {parent_node.description} → 내부 구조 생성")
        
        return chain
    
    def zoom_out(
        self,
        node_id: str,
        outer_cause_desc: str,
        outer_effect_desc: str
    ) -> Tuple[FractalCausalNode, FractalCausalNode]:
        """
        노드 외부로 축소 (Zoom Out)
        
        이 노드를 "과정"으로 보고, 더 거시적인 원인과 결과를 탐색/생성합니다.
        
        예: "불에 손을 댔다"를 과정으로 보면:
            원인: "호기심을 느꼈다"
            결과: "아픔을 느꼈다"
        """
        if node_id not in self.nodes:
            raise ValueError(f"Node {node_id} not found")
        
        process_node = self.nodes[node_id]
        outer_depth = process_node.depth - 1
        
        # 외부 원인 노드
        cause_node = self.get_or_create_node(outer_cause_desc, outer_depth)
        cause_node.effects_ids.append(node_id)
        process_node.causes_ids.append(cause_node.id)
        
        # 외부 결과 노드
        effect_node = self.get_or_create_node(outer_effect_desc, outer_depth)
        process_node.effects_ids.append(effect_node.id)
        effect_node.causes_ids.append(node_id)
        
        logger.debug(f"🔭 Zoom out: {outer_cause_desc} → [{process_node.description}] → {outer_effect_desc}")
        
        return (cause_node, effect_node)
    
    # ========================================================================
    # 순환적 인과 (Circular Causality)
    # ========================================================================
    
    def create_feedback_loop(
        self,
        node_ids: List[str],
        loop_type: str = "reinforcing"
    ) -> List[str]:
        """
        피드백 루프 생성
        
        결과가 원인으로 되돌아가는 순환 구조.
        
        Args:
            node_ids: 루프를 형성할 노드들 (순서대로)
            loop_type: "reinforcing" (자기 강화) 또는 "balancing" (균형)
        
        예:
            "불안" → "회피 행동" → "일시적 안도" → "회피 학습 강화" → "더 많은 불안"
        """
        if len(node_ids) < 2:
            raise ValueError("피드백 루프는 최소 2개 노드 필요")
        
        created_links = []
        
        # 순차 연결
        for i in range(len(node_ids)):
            current_id = node_ids[i]
            next_id = node_ids[(i + 1) % len(node_ids)]  # 마지막은 처음으로
            
            if current_id in self.nodes and next_id in self.nodes:
                current = self.nodes[current_id]
                next_node = self.nodes[next_id]
                
                if next_id not in current.effects_ids:
                    current.effects_ids.append(next_id)
                if current_id not in next_node.causes_ids:
                    next_node.causes_ids.append(current_id)
                
                created_links.append(f"{current_id} → {next_id}")
        
        logger.info(f"🔄 Feedback loop created ({loop_type}): {' → '.join(node_ids)} → (back to start)")
        
        return created_links
    
    def detect_cycles(self, start_node_id: str, max_depth: int = 10) -> List[List[str]]:
        """
        순환 탐지
        
        시작 노드에서 출발해 다시 돌아오는 모든 경로 찾기.
        """
        cycles = []
        
        def dfs(current_id: str, path: List[str], visited: Set[str]):
            if len(path) > max_depth:
                return
            
            if current_id in visited:
                if current_id == start_node_id and len(path) > 1:
                    cycles.append(path.copy())
                return
            
            visited.add(current_id)
            path.append(current_id)
            
            if current_id in self.nodes:
                for effect_id in self.nodes[current_id].effects_ids:
                    dfs(effect_id, path, visited.copy())
            
            path.pop()
        
        dfs(start_node_id, [], set())
        return cycles
    
    # ========================================================================
    # 경험 기반 학습
    # ========================================================================
    
    def experience_causality(
        self,
        steps: List[str],
        emotional_arc: List[float] = None,
        depth: int = 0,
        auto_zoom: bool = True
    ) -> Dict[str, Any]:
        """
        인과 경험을 통한 학습
        
        일련의 단계들을 경험하고, 프랙탈 인과 구조로 학습합니다.
        
        Args:
            steps: 경험 단계들 (최소 3개: 원인, 과정, 결과)
            emotional_arc: 각 단계의 감정 (-1 ~ +1)
            depth: 경험의 깊이
            auto_zoom: 자동으로 상위/하위 추론
        
        Returns:
            학습 결과
        """
        if len(steps) < 3:
            raise ValueError("최소 3단계 필요 (원인, 과정, 결과)")
        
        emotional_arc = emotional_arc or [0.0] * len(steps)
        
        result = {
            "nodes_created": 0,
            "chains_created": 0,
            "cycles_detected": 0,
        }
        
        # 기본 연쇄들 생성 (3개씩 묶어서)
        chains_created = []
        for i in range(len(steps) - 2):
            chain = self.create_chain(
                cause_desc=steps[i],
                process_desc=steps[i + 1],
                effect_desc=steps[i + 2],
                depth=depth
            )
            chains_created.append(chain)
            result["chains_created"] += 1
        
        # 감정 정보 적용
        for i, step in enumerate(steps):
            node = self.get_or_create_node(step, depth)
            if i < len(emotional_arc):
                node.emotional_valence = emotional_arc[i]
        
        # 결과가 원인에 영향을 미치는지 체크 (순환 가능성)
        if auto_zoom and len(steps) >= 4:
            # 마지막 결과가 첫 원인에 영향을 줄 수 있는지
            last_effect = self.get_or_create_node(steps[-1], depth)
            first_cause = self.get_or_create_node(steps[0], depth)
            
            # 감정 궤적 분석
            if emotional_arc:
                start_emotion = emotional_arc[0]
                end_emotion = emotional_arc[-1]
                
                # 감정이 강화되는 방향이면 피드백 루프 가능성
                if (start_emotion < 0 and end_emotion < start_emotion) or \
                   (start_emotion > 0 and end_emotion > start_emotion):
                    # 잠재적 피드백 루프
                    logger.debug("잠재적 피드백 루프 감지")
        
        result["nodes_created"] = len(steps)
        
        return result
    
    # ========================================================================
    # 인과 추론
    # ========================================================================
    
    def trace_causes(
        self,
        node_id: str,
        max_depth: int = 5,
        include_internal: bool = True
    ) -> List[List[str]]:
        """
        원인 추적 (역방향)
        
        "왜 이런 일이 일어났는가?"
        
        프랙탈 구조를 따라 원인을 무한히 추적할 수 있습니다.
        """
        paths = []
        
        def trace(current_id: str, path: List[str], depth: int):
            if depth > max_depth:
                paths.append(path.copy())
                return
            
            if current_id not in self.nodes:
                paths.append(path.copy())
                return
            
            node = self.nodes[current_id]
            
            # 직접적 원인들
            if not node.causes_ids:
                paths.append(path.copy())
            else:
                for cause_id in node.causes_ids:
                    trace(cause_id, path + [cause_id], depth + 1)
            
            # 내부 원인들 (zoom in)
            if include_internal and node.internal_cause_ids:
                for internal_id in node.internal_cause_ids:
                    trace(internal_id, path + [f"[내부]{internal_id}"], depth + 1)
        
        trace(node_id, [node_id], 0)
        return paths
    
    def trace_effects(
        self,
        node_id: str,
        max_depth: int = 5,
        include_internal: bool = True
    ) -> List[List[str]]:
        """
        결과 추적 (순방향)
        
        "이것이 어떤 결과를 가져올까?"
        
        프랙탈 구조를 따라 결과를 무한히 추적할 수 있습니다.
        """
        paths = []
        
        def trace(current_id: str, path: List[str], depth: int):
            if depth > max_depth:
                paths.append(path.copy())
                return
            
            if current_id not in self.nodes:
                paths.append(path.copy())
                return
            
            node = self.nodes[current_id]
            
            # 직접적 결과들
            if not node.effects_ids:
                paths.append(path.copy())
            else:
                for effect_id in node.effects_ids:
                    trace(effect_id, path + [effect_id], depth + 1)
            
            # 내부 결과들 (zoom in)
            if include_internal and node.internal_effect_ids:
                for internal_id in node.internal_effect_ids:
                    trace(internal_id, path + [f"[내부]{internal_id}"], depth + 1)
        
        trace(node_id, [node_id], 0)
        return paths
    
    def explain_causality(
        self,
        node_id: str,
        depth: int = 3
    ) -> str:
        """
        인과 관계 설명 생성
        
        "왜 X가 일어났는가?"에 대한 프랙탈 설명
        """
        if node_id not in self.nodes:
            return f"'{node_id}'에 대한 정보가 없습니다."
        
        node = self.nodes[node_id]
        lines = [f"=== {node.description}의 인과 분석 ===", ""]
        
        # 원인 추적
        lines.append("📌 원인들:")
        cause_paths = self.trace_causes(node_id, max_depth=depth)
        for path in cause_paths[:5]:  # 최대 5개 경로
            descriptions = []
            for nid in path:
                if nid.startswith("[내부]"):
                    nid = nid[4:]
                if nid in self.nodes:
                    descriptions.append(self.nodes[nid].description)
            if descriptions:
                lines.append("  ← " + " ← ".join(descriptions))
        
        lines.append("")
        
        # 결과 추적
        lines.append("📌 결과들:")
        effect_paths = self.trace_effects(node_id, max_depth=depth)
        for path in effect_paths[:5]:
            descriptions = []
            for nid in path:
                if nid.startswith("[내부]"):
                    nid = nid[4:]
                if nid in self.nodes:
                    descriptions.append(self.nodes[nid].description)
            if descriptions:
                lines.append("  → " + " → ".join(descriptions))
        
        # 내부 구조
        if node.has_internal_structure():
            lines.append("")
            lines.append("📌 내부 구조 (zoom in):")
            for cause_id in node.internal_cause_ids[:2]:
                if cause_id in self.nodes:
                    lines.append(f"  [원인] {self.nodes[cause_id].description}")
            for process_id in node.internal_process_ids[:2]:
                if process_id in self.nodes:
                    lines.append(f"  [과정] {self.nodes[process_id].description}")
            for effect_id in node.internal_effect_ids[:2]:
                if effect_id in self.nodes:
                    lines.append(f"  [결과] {self.nodes[effect_id].description}")
        
        # 순환 탐지
        cycles = self.detect_cycles(node_id, max_depth=5)
        if cycles:
            lines.append("")
            lines.append("🔄 순환 구조 감지:")
            for cycle in cycles[:3]:
                cycle_desc = []
                for nid in cycle:
                    if nid in self.nodes:
                        cycle_desc.append(self.nodes[nid].description)
                lines.append(f"  {' → '.join(cycle_desc)} → (순환)")
        
        return "\n".join(lines)
    
    # ========================================================================
    # 통계 및 시각화
    # ========================================================================
    
    def get_statistics(self) -> Dict[str, Any]:
        """프랙탈 인과 엔진 통계"""
        depth_distribution = defaultdict(int)
        for node in self.nodes.values():
            depth_distribution[node.depth] += 1
        
        return {
            "name": self.name,
            "total_nodes": self.total_nodes,
            "total_chains": self.total_chains,
            "max_depth": self.max_depth_explored,
            "min_depth": self.min_depth_explored,
            "depth_distribution": dict(depth_distribution),
            "nodes_with_internal_structure": sum(
                1 for n in self.nodes.values() if n.has_internal_structure()
            ),
        }
    
    def visualize_fractal(self, center_node_id: str = None, radius: int = 2) -> str:
        """
        프랙탈 구조 시각화 (텍스트)
        """
        lines = ["🌀 프랙탈 인과 구조", "=" * 50, ""]
        
        if center_node_id and center_node_id in self.nodes:
            center = self.nodes[center_node_id]
            lines.append(f"중심: {center.description} (깊이: {center.depth})")
            lines.append("")
            
            # 원인들
            lines.append("⬅️ 원인들:")
            for cause_id in center.causes_ids[:3]:
                if cause_id in self.nodes:
                    lines.append(f"   ← {self.nodes[cause_id].description}")
            
            # 내부 구조
            if center.has_internal_structure():
                lines.append("")
                lines.append("🔬 내부 구조:")
                for internal_id in center.get_internal_ids()[:5]:
                    if internal_id in self.nodes:
                        internal = self.nodes[internal_id]
                        role = internal.parent_role.value if internal.parent_role else "?"
                        lines.append(f"   [{role}] {internal.description}")
            
            # 결과들
            lines.append("")
            lines.append("➡️ 결과들:")
            for effect_id in center.effects_ids[:3]:
                if effect_id in self.nodes:
                    lines.append(f"   → {self.nodes[effect_id].description}")
        else:
            lines.append("노드 통계:")
            stats = self.get_statistics()
            for key, value in stats.items():
                lines.append(f"  {key}: {value}")
        
        return "\n".join(lines)


# ============================================================================
# Demo
# ============================================================================

def demo():
    """프랙탈 인과 엔진 데모"""
    print("=" * 70)
    print("🌀 Fractal Causality Engine - 프랙탈 인과 엔진")
    print("=" * 70)
    print()
    print("인과는 프랙탈 구조입니다.")
    print("원인과 과정과 결과가 무한히 순환되고 있습니다.")
    print()
    
    engine = FractalCausalityEngine("Elysia's Causal Mind")
    
    # 1. 기본 인과 연쇄
    print("-" * 70)
    print("1. 기본 인과 연쇄 생성")
    print("-" * 70)
    
    engine.experience_causality(
        steps=["호기심을 느꼈다", "불에 손을 댔다", "뜨거움을 느꼈다", "손을 뺐다", "안전해졌다"],
        emotional_arc=[0.3, 0.0, -0.8, -0.3, 0.5]
    )
    print("  ✓ 경험 학습 완료")
    
    # 2. Zoom In - 내부 구조 탐색
    print()
    print("-" * 70)
    print("2. Zoom In - 내부 구조 탐색")
    print("-" * 70)
    
    # "불에 손을 댔다" 노드 찾기
    touch_node = engine.get_or_create_node("불에 손을 댔다")
    
    engine.zoom_in(
        touch_node.id,
        cause_desc="손이 불에 접촉했다",
        process_desc="열에너지가 피부로 전달되었다",
        effect_desc="피부 세포가 자극을 받았다"
    )
    print("  ✓ '불에 손을 댔다'의 내부 구조 생성")
    
    # 더 깊이 들어가기
    contact_node = engine.get_or_create_node("손이 불에 접촉했다", depth=1)
    engine.zoom_in(
        contact_node.id,
        cause_desc="손 근육이 수축했다",
        process_desc="팔이 불 쪽으로 움직였다",
        effect_desc="손 표면이 불꽃에 닿았다"
    )
    print("  ✓ '손이 불에 접촉했다'의 내부 구조 생성")
    
    # 3. Zoom Out - 상위 구조 탐색
    print()
    print("-" * 70)
    print("3. Zoom Out - 상위 구조 탐색")
    print("-" * 70)
    
    safe_node = engine.get_or_create_node("안전해졌다")
    engine.zoom_out(
        safe_node.id,
        outer_cause_desc="위험을 인식했다",
        outer_effect_desc="학습이 일어났다"
    )
    print("  ✓ '안전해졌다'의 상위 구조 생성")
    
    # 4. 순환 구조 (피드백 루프)
    print()
    print("-" * 70)
    print("4. 순환 구조 (피드백 루프)")
    print("-" * 70)
    
    # 학습 강화 루프 생성
    learn_node = engine.get_or_create_node("학습이 일어났다", depth=-1)
    avoid_node = engine.create_node("불을 피하게 되었다", depth=-1)
    safe2_node = engine.create_node("안전이 유지되었다", depth=-1)
    reinforce_node = engine.create_node("회피 행동이 강화되었다", depth=-1)
    
    engine.create_feedback_loop(
        [learn_node.id, avoid_node.id, safe2_node.id, reinforce_node.id],
        loop_type="reinforcing"
    )
    print("  ✓ 학습 강화 피드백 루프 생성")
    
    # 5. 인과 설명
    print()
    print("-" * 70)
    print("5. 인과 설명 생성")
    print("-" * 70)
    
    explanation = engine.explain_causality(touch_node.id, depth=2)
    print(explanation)
    
    # 6. 통계
    print()
    print("-" * 70)
    print("6. 프랙탈 통계")
    print("-" * 70)
    
    stats = engine.get_statistics()
    print(f"  총 노드: {stats['total_nodes']}")
    print(f"  총 연쇄: {stats['total_chains']}")
    print(f"  깊이 범위: {stats['min_depth']} ~ {stats['max_depth']}")
    print(f"  내부 구조 가진 노드: {stats['nodes_with_internal_structure']}")
    
    print()
    print("=" * 70)
    print("🌀 프랙탈 인과: 원인 안에 원인, 결과 안에 결과, 무한히...")
    print("=" * 70)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    demo()
