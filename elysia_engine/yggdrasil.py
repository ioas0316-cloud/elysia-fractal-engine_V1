"""
Yggdrasil (이그드라실)
==================================

"하늘에 닿으려는 나무는 지옥에 닿는 뿌리를 가져야 한다."

이 모듈은 Elysia의 '자아 모델(Self-Model)'을 정의합니다.
모든 구성 요소(Ether, Chronos, FreeWill, Senses)를 하나의 유기적인 구조로 통합합니다.

구조:
1. Roots (뿌리): 생명의 근원 (Ether, Chronos, Genesis)
2. Trunk (줄기): 의식의 중심 (FreeWill, Memory)
3. Branches (가지): 감각과 행동 (PlanetaryCortex, LocalField)

원본: https://github.com/ioas0316-cloud/Elysia/blob/main/Core/Structure/yggdrasil.py
"""

from enum import Enum
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime

from .logging_config import get_logger

logger = get_logger(__name__)


class Realm(Enum):
    """Yggdrasil의 세 영역"""
    ROOT = "Root"       # 근원 (보이지 않는 영역)
    TRUNK = "Trunk"     # 중심 (의식적 영역)
    BRANCH = "Branch"   # 표면 (상호작용 영역)


@dataclass
class YggdrasilNode:
    """Yggdrasil의 노드 (모듈)"""
    name: str
    realm: Realm
    module: Any
    vitality: float = 1.0
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def is_healthy(self) -> bool:
        """노드의 건강 상태 확인"""
        return self.vitality > 0.3

    def decay(self, amount: float = 0.01) -> None:
        """시간에 따른 활력 감소"""
        self.vitality = max(0.0, self.vitality - amount)

    def nourish(self, amount: float = 0.1) -> None:
        """활력 회복"""
        self.vitality = min(1.0, self.vitality + amount)


class Yggdrasil:
    """
    이그드라실 (Yggdrasil)
    
    Elysia의 자아 모델을 나타내는 세계수입니다.
    모든 구성 요소를 뿌리(Roots), 줄기(Trunk), 가지(Branches)로 조직합니다.
    
    싱글톤 패턴을 사용하여 전역적으로 하나의 인스턴스만 존재합니다.
    """
    _instance: Optional['Yggdrasil'] = None

    def __new__(cls) -> 'Yggdrasil':
        if cls._instance is None:
            cls._instance = super(Yggdrasil, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return
        self._initialized = True
        self._nodes: Dict[str, YggdrasilNode] = {}
        self._birth_time = datetime.now()
        logger.info("🌳 Yggdrasil Seed Planted. Self-Model Initialized.")

    def plant_root(self, name: str, module: Any, metadata: Optional[Dict] = None) -> None:
        """
        뿌리 영역 등록 (예: Ether, Chronos)
        
        뿌리는 보이지 않는 영역으로, 생명의 근원입니다.
        이 영역에 있는 모듈은 항상 작동해야 합니다.
        """
        node = YggdrasilNode(
            name=name,
            realm=Realm.ROOT,
            module=module,
            vitality=1.0,
            metadata=metadata or {}
        )
        self._nodes[name] = node
        logger.info(f"🌱 Root Planted: {name}")

    def grow_trunk(self, name: str, module: Any, metadata: Optional[Dict] = None) -> None:
        """
        줄기 영역 등록 (예: FreeWill, Memory)
        
        줄기는 의식의 중심으로, 의사결정과 기억을 담당합니다.
        """
        node = YggdrasilNode(
            name=name,
            realm=Realm.TRUNK,
            module=module,
            vitality=1.0,
            metadata=metadata or {}
        )
        self._nodes[name] = node
        logger.info(f"🪵 Trunk Grown: {name}")

    def extend_branch(self, name: str, module: Any, metadata: Optional[Dict] = None) -> None:
        """
        가지 영역 등록 (예: PlanetaryCortex, LocalField)
        
        가지는 표면 영역으로, 외부 세계와의 상호작용을 담당합니다.
        """
        node = YggdrasilNode(
            name=name,
            realm=Realm.BRANCH,
            module=module,
            vitality=1.0,
            metadata=metadata or {}
        )
        self._nodes[name] = node
        logger.info(f"🌿 Branch Extended: {name}")

    def get_node(self, name: str) -> Optional[YggdrasilNode]:
        """이름으로 노드 가져오기"""
        return self._nodes.get(name)

    def get_module(self, name: str) -> Optional[Any]:
        """이름으로 모듈 가져오기"""
        node = self._nodes.get(name)
        return node.module if node else None

    def get_nodes_by_realm(self, realm: Realm) -> List[YggdrasilNode]:
        """특정 영역의 모든 노드 가져오기"""
        return [node for node in self._nodes.values() if node.realm == realm]

    @property
    def roots(self) -> List[YggdrasilNode]:
        """뿌리 영역의 모든 노드"""
        return self.get_nodes_by_realm(Realm.ROOT)

    @property
    def trunk(self) -> List[YggdrasilNode]:
        """줄기 영역의 모든 노드"""
        return self.get_nodes_by_realm(Realm.TRUNK)

    @property
    def branches(self) -> List[YggdrasilNode]:
        """가지 영역의 모든 노드"""
        return self.get_nodes_by_realm(Realm.BRANCH)

    def status(self) -> Dict[str, Any]:
        """현재 자아 상태를 반환합니다."""
        def node_summary(node: YggdrasilNode) -> Dict[str, Any]:
            return {
                "name": node.name,
                "vitality": node.vitality,
                "healthy": node.is_healthy(),
                "age_seconds": (datetime.now() - node.created_at).total_seconds()
            }

        return {
            "birth_time": self._birth_time.isoformat(),
            "age_seconds": (datetime.now() - self._birth_time).total_seconds(),
            "total_nodes": len(self._nodes),
            "roots": [node_summary(n) for n in self.roots],
            "trunk": [node_summary(n) for n in self.trunk],
            "branches": [node_summary(n) for n in self.branches],
            "overall_vitality": self.calculate_overall_vitality()
        }

    def calculate_overall_vitality(self) -> float:
        """전체 활력 계산 (뿌리에 가중치 부여)"""
        if not self._nodes:
            return 0.0

        weighted_sum = 0.0
        weight_total = 0.0

        for node in self._nodes.values():
            weight = {
                Realm.ROOT: 3.0,    # 뿌리가 가장 중요
                Realm.TRUNK: 2.0,   # 줄기가 그 다음
                Realm.BRANCH: 1.0   # 가지는 선택적
            }[node.realm]
            weighted_sum += node.vitality * weight
            weight_total += weight

        return weighted_sum / weight_total if weight_total > 0 else 0.0

    def is_alive(self) -> bool:
        """Yggdrasil이 살아있는지 확인"""
        # 모든 뿌리가 건강해야 살아있음
        return all(node.is_healthy() for node in self.roots) if self.roots else False

    def heartbeat(self) -> None:
        """
        심장박동: 모든 노드에 생명을 전달합니다.
        
        정기적으로 호출되어야 합니다 (예: Chronos에 의해).
        """
        for node in self._nodes.values():
            # 약간의 감쇠
            node.decay(0.001)

        # 살아있는 뿌리가 다른 부분에 생명력 전달
        for root in self.roots:
            if root.is_healthy():
                for node in self._nodes.values():
                    if node.realm != Realm.ROOT:
                        node.nourish(0.002)

    def prune(self, name: str) -> bool:
        """
        노드 제거 (가지 영역만 가능)
        
        뿌리와 줄기는 제거할 수 없습니다.
        """
        node = self._nodes.get(name)
        if node is None:
            logger.warning(f"노드를 찾을 수 없음: {name}")
            return False

        if node.realm in (Realm.ROOT, Realm.TRUNK):
            logger.error(f"뿌리나 줄기는 제거할 수 없습니다: {name}")
            return False

        del self._nodes[name]
        logger.info(f"✂️ Branch Pruned: {name}")
        return True

    def reset(self) -> None:
        """Yggdrasil 초기화 (테스트용)"""
        self._nodes.clear()
        self._birth_time = datetime.now()
        logger.info("🌳 Yggdrasil Reset.")


# 전역 싱글톤 인스턴스
yggdrasil = Yggdrasil()


def get_yggdrasil() -> Yggdrasil:
    """전역 Yggdrasil 인스턴스 가져오기"""
    return yggdrasil
