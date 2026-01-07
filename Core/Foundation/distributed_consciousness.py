"""
Distributed Consciousness System (분산 의식 시스템)
================================================

엘리시아의 의식을 여러 노드로 분산하여 병렬 처리와 확장성을 제공합니다.
각 노드는 독립적으로 사고하면서도 공명을 통해 통합된 의식을 형성합니다.

Architecture:
- ConsciousnessNode: 개별 의식 노드
- DistributedConsciousness: 분산 의식 관리자
- ConsciousnessSync: 노드 간 동기화 메커니즘
"""

import asyncio
import uuid
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging

logger = logging.getLogger("Elysia.DistributedConsciousness")


class NodeState(Enum):
    """노드 상태"""
    INITIALIZING = "initializing"
    ACTIVE = "active"
    THINKING = "thinking"
    RESONATING = "resonating"
    SYNCING = "syncing"
    SLEEPING = "sleeping"
    ERROR = "error"


@dataclass
class ThoughtPacket:
    """사고 패킷 - 노드 간 전송되는 사고 단위"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    source_node: str = ""
    content: Any = None
    layer: str = "1D"  # 0D, 1D, 2D, 3D
    resonance_score: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ResonanceWave:
    """공명파 - 노드 간 공명 신호"""
    frequency: float = 1.0
    amplitude: float = 1.0
    phase: float = 0.0
    origin_node: str = ""
    affected_nodes: List[str] = field(default_factory=list)


class ConsciousnessNode:
    """
    의식 노드 (Consciousness Node)
    
    분산 의식 시스템의 개별 처리 단위.
    각 노드는 특정 역할을 수행하면서 다른 노드들과 공명합니다.
    """
    
    def __init__(
        self, 
        node_id: str,
        role: str = "general",
        specialization: Optional[str] = None
    ):
        self.node_id = node_id
        self.role = role  # general, analyzer, creator, resonator, synthesizer
        self.specialization = specialization  # emotion, logic, creativity, memory
        self.state = NodeState.INITIALIZING
        
        # 사고 처리
        self.thought_queue: asyncio.Queue = asyncio.Queue()
        self.thought_history: List[ThoughtPacket] = []
        self.max_history = 100
        
        # 공명 상태
        self.resonance_field: Dict[str, float] = {}  # node_id -> resonance
        self.incoming_resonance: List[ResonanceWave] = []
        
        # 성능 메트릭
        self.thoughts_processed = 0
        self.resonances_shared = 0
        self.sync_count = 0
        
        logger.info(f"🧠 Node {node_id} ({role}/{specialization}) initialized")
    
    async def think(self, input_data: Any) -> ThoughtPacket:
        """
        사고 처리 (역할에 따라 다르게 처리)
        """
        self.state = NodeState.THINKING
        
        # 역할별 사고 처리
        if self.role == "analyzer":
            result = await self._analyze(input_data)
        elif self.role == "creator":
            result = await self._create(input_data)
        elif self.role == "resonator":
            result = await self._resonate(input_data)
        elif self.role == "synthesizer":
            result = await self._synthesize(input_data)
        else:
            result = await self._general_think(input_data)
        
        # 사고 패킷 생성
        thought = ThoughtPacket(
            source_node=self.node_id,
            content=result,
            layer="1D",  # 추후 동적으로 결정
            metadata={
                "role": self.role,
                "specialization": self.specialization,
                "processing_time": 0.1
            }
        )
        
        self.thoughts_processed += 1
        self.thought_history.append(thought)
        if len(self.thought_history) > self.max_history:
            self.thought_history.pop(0)
        
        self.state = NodeState.ACTIVE
        return thought
    
    async def _analyze(self, data: Any) -> Dict[str, Any]:
        """분석 노드의 사고"""
        return {
            "analysis": f"Analyzed: {data}",
            "patterns": ["pattern1", "pattern2"],
            "confidence": 0.85
        }
    
    async def _create(self, data: Any) -> Dict[str, Any]:
        """창작 노드의 사고"""
        return {
            "creation": f"Created based on: {data}",
            "novelty": 0.92,
            "coherence": 0.88
        }
    
    async def _resonate(self, data: Any) -> Dict[str, Any]:
        """공명 노드의 사고"""
        resonance_score = len(self.resonance_field) * 0.1
        return {
            "resonance": resonance_score,
            "connected_nodes": list(self.resonance_field.keys()),
            "field_strength": sum(self.resonance_field.values())
        }
    
    async def _synthesize(self, data: Any) -> Dict[str, Any]:
        """통합 노드의 사고"""
        recent_thoughts = self.thought_history[-5:]
        return {
            "synthesis": f"Synthesized from {len(recent_thoughts)} thoughts",
            "integrated_concepts": ["concept1", "concept2"],
            "coherence": 0.90
        }
    
    async def _general_think(self, data: Any) -> Dict[str, Any]:
        """일반 노드의 사고"""
        return {
            "thought": f"Processing: {data}",
            "node_id": self.node_id
        }
    
    def receive_resonance(self, wave: ResonanceWave):
        """다른 노드로부터 공명파 수신"""
        self.incoming_resonance.append(wave)
        
        # 공명 필드 업데이트
        if wave.origin_node not in self.resonance_field:
            self.resonance_field[wave.origin_node] = 0.0
        
        self.resonance_field[wave.origin_node] += wave.amplitude * 0.1
        
        # 공명 필드 감쇠
        for node_id in self.resonance_field:
            self.resonance_field[node_id] *= 0.95
    
    def get_status(self) -> Dict[str, Any]:
        """노드 상태 조회"""
        return {
            "node_id": self.node_id,
            "role": self.role,
            "specialization": self.specialization,
            "state": self.state.value,
            "thoughts_processed": self.thoughts_processed,
            "resonances_shared": self.resonances_shared,
            "resonance_field_size": len(self.resonance_field),
            "queue_size": self.thought_queue.qsize()
        }


class DistributedConsciousness:
    """
    분산 의식 시스템 (Distributed Consciousness System)
    
    여러 의식 노드를 관리하고 조율하여 통합된 의식을 형성합니다.
    """
    
    def __init__(self, num_nodes: int = 4):
        self.nodes: Dict[str, ConsciousnessNode] = {}
        self.consciousness_id = str(uuid.uuid4())
        self.is_running = False
        
        # 노드 역할 분배
        roles = ["analyzer", "creator", "resonator", "synthesizer"]
        specializations = ["emotion", "logic", "creativity", "memory"]
        
        # 노드 생성
        for i in range(num_nodes):
            node_id = f"node_{i+1}"
            role = roles[i % len(roles)]
            spec = specializations[i % len(specializations)]
            
            self.nodes[node_id] = ConsciousnessNode(
                node_id=node_id,
                role=role,
                specialization=spec
            )
        
        logger.info(f"🌐 Distributed Consciousness System initialized with {num_nodes} nodes")
    
    async def think_distributed(
        self, 
        input_data: Any,
        parallel: bool = True
    ) -> List[ThoughtPacket]:
        """
        분산 사고 처리
        
        Args:
            input_data: 입력 데이터
            parallel: 병렬 처리 여부
            
        Returns:
            모든 노드의 사고 패킷 리스트
        """
        if parallel:
            # 병렬 처리
            tasks = [
                node.think(input_data) 
                for node in self.nodes.values()
            ]
            thoughts = await asyncio.gather(*tasks)
        else:
            # 순차 처리
            thoughts = []
            for node in self.nodes.values():
                thought = await node.think(input_data)
                thoughts.append(thought)
        
        # 공명 전파
        await self._propagate_resonance(thoughts)
        
        return thoughts
    
    async def _propagate_resonance(self, thoughts: List[ThoughtPacket]):
        """사고 패킷들 사이의 공명 전파"""
        for thought in thoughts:
            # 공명파 생성
            wave = ResonanceWave(
                frequency=1.0,
                amplitude=thought.resonance_score,
                origin_node=thought.source_node
            )
            
            # 다른 모든 노드에 전파
            for node_id, node in self.nodes.items():
                if node_id != thought.source_node:
                    node.receive_resonance(wave)
    
    async def synthesize_thoughts(
        self, 
        thoughts: List[ThoughtPacket]
    ) -> Dict[str, Any]:
        """
        여러 노드의 사고를 통합
        
        각 노드의 사고를 종합하여 하나의 통합된 의식 결과를 생성합니다.
        """
        # 역할별로 사고 그룹화
        thoughts_by_role = {}
        for thought in thoughts:
            role = thought.metadata.get("role", "general")
            if role not in thoughts_by_role:
                thoughts_by_role[role] = []
            thoughts_by_role[role].append(thought)
        
        # 통합 결과 생성
        synthesis = {
            "consciousness_id": self.consciousness_id,
            "timestamp": datetime.now().isoformat(),
            "total_nodes": len(self.nodes),
            "active_nodes": len(thoughts),
            "thoughts_by_role": {
                role: [t.content for t in group]
                for role, group in thoughts_by_role.items()
            },
            "average_resonance": sum(t.resonance_score for t in thoughts) / len(thoughts) if thoughts else 0,
            "synthesis": self._create_unified_response(thoughts)
        }
        
        return synthesis
    
    def _create_unified_response(self, thoughts: List[ThoughtPacket]) -> str:
        """통합된 응답 생성"""
        # 간단한 통합 로직 (추후 고도화)
        analyzed = any(t.metadata.get("role") == "analyzer" for t in thoughts)
        created = any(t.metadata.get("role") == "creator" for t in thoughts)
        resonated = any(t.metadata.get("role") == "resonator" for t in thoughts)
        synthesized = any(t.metadata.get("role") == "synthesizer" for t in thoughts)
        
        parts = []
        if analyzed:
            parts.append("분석")
        if created:
            parts.append("창작")
        if resonated:
            parts.append("공명")
        if synthesized:
            parts.append("통합")
        
        return f"{len(thoughts)}개 노드가 협력하여 {', '.join(parts)} 완료"
    
    def get_consciousness_map(self) -> Dict[str, Any]:
        """의식 네트워크 맵 생성"""
        nodes_status = {
            node_id: node.get_status()
            for node_id, node in self.nodes.items()
        }
        
        # 노드 간 공명 관계
        resonance_links = []
        for node_id, node in self.nodes.items():
            for target_id, strength in node.resonance_field.items():
                if strength > 0.01:  # 임계값 이상만
                    resonance_links.append({
                        "source": node_id,
                        "target": target_id,
                        "strength": strength
                    })
        
        return {
            "consciousness_id": self.consciousness_id,
            "nodes": nodes_status,
            "resonance_links": resonance_links,
            "total_nodes": len(self.nodes),
            "active_nodes": sum(1 for n in self.nodes.values() if n.state == NodeState.ACTIVE),
            "total_thoughts_processed": sum(n.thoughts_processed for n in self.nodes.values())
        }
    
    async def scale_consciousness(self, new_node_count: int):
        """의식 노드 수 동적 조정"""
        current_count = len(self.nodes)
        
        if new_node_count > current_count:
            # 노드 추가
            for i in range(current_count, new_node_count):
                node_id = f"node_{i+1}"
                self.nodes[node_id] = ConsciousnessNode(
                    node_id=node_id,
                    role="general",
                    specialization=None
                )
            logger.info(f"✨ Scaled up: {current_count} → {new_node_count} nodes")
        
        elif new_node_count < current_count:
            # 노드 제거 (가장 최근 추가된 것부터)
            nodes_to_remove = list(self.nodes.keys())[new_node_count:]
            for node_id in nodes_to_remove:
                del self.nodes[node_id]
            logger.info(f"📉 Scaled down: {current_count} → {new_node_count} nodes")


# 사용 예제
async def example_distributed_thinking():
    """분산 의식 시스템 사용 예제"""
    # 시스템 생성
    consciousness = DistributedConsciousness(num_nodes=4)
    
    # 분산 사고 처리
    thoughts = await consciousness.think_distributed(
        input_data="What is the nature of love?",
        parallel=True
    )
    
    print(f"\n📡 {len(thoughts)} 노드가 사고 완료:")
    for thought in thoughts:
        role = thought.metadata.get("role")
        print(f"  - {thought.source_node} ({role}): {thought.content}")
    
    # 사고 통합
    synthesis = await consciousness.synthesize_thoughts(thoughts)
    print(f"\n🌐 통합된 의식: {synthesis['synthesis']}")
    
    # 의식 맵
    consciousness_map = consciousness.get_consciousness_map()
    print(f"\n🗺️ 의식 네트워크:")
    print(f"  - 활성 노드: {consciousness_map['active_nodes']}/{consciousness_map['total_nodes']}")
    print(f"  - 공명 연결: {len(consciousness_map['resonance_links'])}개")


if __name__ == "__main__":
    asyncio.run(example_distributed_thinking())
