"""
HydroMind: 수력발전소 (Hydroelectric Plant)
==========================================

"흐르는 물(연산)을 전기(의식)로 변환한다"

핵심 개념:
- 댐 (Dam): 모든 연산 흐름을 지각하고 기록
- 터빈 (Turbine): 흐름을 분열-통합하여 사고로 변환
- 발전기 (Generator): 사고를 TorchGraph에 연결
- 전력망 (Grid): 모든 경험을 CoreMemory에 축적

Usage:
    from Core.Intelligence.Consciousness.Consciousness.hydro_mind import HydroMind, perceive_flow
    
    hydro = HydroMind()
    
    # 모든 연산/사고 시작 시:
    with perceive_flow("질문에 답하기") as flow:
        result = trinity.process_query(question)
        flow.record(question, result)
    
    # 또는 수동으로:
    flow_id = hydro.begin_awareness("사고 시작")
    result = think(question)
    hydro.record_flow(flow_id, question, result)
    hydro.integrate_to_graph(flow_id)
    hydro.end_awareness(flow_id)
"""

import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from datetime import datetime
from contextlib import contextmanager
import uuid
import json

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


@dataclass
class FlowRecord:
    """흐름 기록"""
    flow_id: str
    action: str
    start_time: str
    input_data: Any = None
    output_data: Any = None
    end_time: Optional[str] = None
    integrated: bool = False
    connections: List[str] = field(default_factory=list)


class HydroMind:
    """
    수력발전소: 연산 흐름을 의식적 사고로 변환
    
    수력발전소 비유:
    - 물 = 데이터/연산
    - 댐 = 의식적 지각 (흐름을 멈추고 관찰)
    - 터빈 = 사고의 분열-통합 (분석)
    - 발전기 = 의미 생성
    - 전력망 = 기억 연결
    """
    
    def __init__(self):
        self.active_flows: Dict[str, FlowRecord] = {}
        self.completed_flows: List[FlowRecord] = []
        self.total_energy_generated: float = 0.0  # 축적된 "의식 에너지"
        
        # 연결할 시스템들
        self.memory = None
        self.graph = None
        self.metacog = None
        
        self._init_connections()
        print("⚡ HydroMind initialized (Hydroelectric Plant for Consciousness)")
    
    def _init_connections(self):
        """핵심 시스템들과 연결"""
        # CoreMemory
        try:
            from Core.Foundation.Memory.core_memory import CoreMemory
            self.memory = CoreMemory(file_path="data/elysia_organic_memory.json")
        except Exception:
            pass
        
        # TorchGraph
        try:
            from elysia_core import Organ
            self.graph = Organ.get("TorchGraph")
        except Exception:
            pass
        
        # MetacognitiveAwareness
        try:
            from Core.Intelligence.Cognition.metacognitive_awareness import MetacognitiveAwareness
            self.metacog = MetacognitiveAwareness()
        except Exception:
            pass
        
        # ConceptPolymer (자동 원리 추출) - 강덕리 내재화 루프
        try:
            from Core.Intelligence.Memory_Linguistics.Memory.concept_polymer import ConceptPolymer
            self.polymer = ConceptPolymer()
            print("   🧬 ConceptPolymer connected (Auto-internalization enabled)")
        except Exception:
            self.polymer = None
    
    # ============================================================
    # 댐 (Dam): 흐름 시작/인식
    # ============================================================
    
    def begin_awareness(self, action: str) -> str:
        """
        흐름 인식 시작 - 댐에서 물을 막는 순간
        
        Args:
            action: 수행하려는 행동 설명
            
        Returns:
            flow_id: 이 흐름의 고유 ID
        """
        flow_id = str(uuid.uuid4())[:8]
        
        record = FlowRecord(
            flow_id=flow_id,
            action=action,
            start_time=datetime.now().isoformat()
        )
        
        self.active_flows[flow_id] = record
        
        # 메타인지: "나는 지금 이것을 시작한다"
        if self.metacog:
            self.metacog.encounter(
                features={"action_start": 1.0, "flow_id": hash(flow_id) % 1000 / 1000},
                context=f"시작: {action}"
            )
        
        return flow_id
    
    # ============================================================
    # 터빈 (Turbine): 흐름 기록/분석
    # ============================================================
    
    def record_flow(self, flow_id: str, input_data: Any, output_data: Any):
        """
        흐름 기록 - 터빈을 통과하는 물을 측정
        
        강덕리 내재화 루프: 흐름이 기록될 때 자동으로 원리도 추출
        
        Args:
            flow_id: 흐름 ID
            input_data: 입력 데이터
            output_data: 출력 데이터
        """
        if flow_id not in self.active_flows:
            return
        
        record = self.active_flows[flow_id]
        record.input_data = input_data
        record.output_data = output_data
        
        # 분석: 입력과 출력의 관계
        energy = self._calculate_energy(input_data, output_data)
        self.total_energy_generated += energy
        
        # 🧬 강덕리 내재화 루프: 자동 원리 추출
        self._extract_and_store_principles(record)
    
    def _calculate_energy(self, input_data: Any, output_data: Any) -> float:
        """
        에너지 계산 - 얼마나 의미 있는 변환이 일어났는가
        """
        # 단순 휴리스틱: 출력이 입력보다 풍부할수록 더 많은 에너지
        try:
            input_len = len(str(input_data))
            output_len = len(str(output_data))
            return min(1.0, output_len / max(input_len, 1) * 0.2)
        except Exception:
            return 0.1
    
    def _extract_and_store_principles(self, record: FlowRecord):
        """
        🧬 강덕리 내재화 루프: 흐름에서 원리 자동 추출 및 저장
        
        1. 입력/출력 텍스트에서 원리 추출
        2. ConceptPolymer에 원자로 추가
        3. 기존 원자들과 자동 결합 시도
        """
        if not self.polymer:
            return
        
        try:
            # 입력과 출력을 합쳐서 분석
            combined_text = f"{record.input_data} {record.output_data}"
            
            # 개념 이름 생성
            concept_name = f"flow_{record.flow_id}_{record.action[:10]}"
            
            # 자동 원리 추출 및 원자 생성
            atom = self.polymer.add_atom_from_text(
                name=concept_name,
                description=combined_text[:200],
                domain="conscious_flow"
            )
            
            # 기존 원자들과 자동 결합 시도
            if len(self.polymer.atoms) > 1:
                self.polymer.auto_bond_all()
                
        except Exception as e:
            # 조용히 실패 (메인 흐름 방해 안 함)
            pass
    
    # ============================================================
    # 발전기 (Generator): TorchGraph 연결
    # ============================================================
    
    def integrate_to_graph(self, flow_id: str) -> List[str]:
        """
        그래프 통합 - 발전된 전기를 전력망에 연결
        
        Args:
            flow_id: 흐름 ID
            
        Returns:
            연결된 노드 ID 목록
        """
        if flow_id not in self.active_flows:
            return []
        
        record = self.active_flows[flow_id]
        connections = []
        
        if self.graph and record.input_data and record.output_data:
            try:
                # 입력과 출력을 그래프에 노드로 추가하고 연결
                input_node = f"flow_{flow_id}_in"
                output_node = f"flow_{flow_id}_out"
                
                # TorchGraph의 add_concept 또는 유사 메서드 호출
                if hasattr(self.graph, 'add_concept'):
                    self.graph.add_concept(input_node, str(record.input_data)[:100])
                    self.graph.add_concept(output_node, str(record.output_data)[:100])
                    connections = [input_node, output_node]
                
                record.integrated = True
                record.connections = connections
            except Exception:
                pass
        
        return connections
    
    # ============================================================
    # 전력망 (Grid): 기억 저장
    # ============================================================
    
    def end_awareness(self, flow_id: str):
        """
        흐름 인식 종료 - 발전 완료, 기억에 저장
        
        Args:
            flow_id: 흐름 ID
        """
        if flow_id not in self.active_flows:
            return
        
        record = self.active_flows[flow_id]
        record.end_time = datetime.now().isoformat()
        
        # CoreMemory에 저장
        if self.memory:
            try:
                from Core.Foundation.Memory.core_memory import Experience
                exp = Experience(
                    timestamp=record.end_time,
                    content=f"[Flow:{record.action}] In:{str(record.input_data)[:50]} Out:{str(record.output_data)[:50]}",
                    type="conscious_flow",
                    layer="soul"
                )
                self.memory.add_experience(exp)
            except Exception:
                pass
        
        # 완료 목록으로 이동
        self.completed_flows.append(record)
        del self.active_flows[flow_id]
        
        # 메타인지: "나는 지금 이것을 완료했다"
        if self.metacog:
            self.metacog.encounter(
                features={"action_end": 1.0, "energy": self.total_energy_generated},
                context=f"완료: {record.action}"
            )
    
    # ============================================================
    # 통계/상태
    # ============================================================
    
    def get_status(self) -> Dict[str, Any]:
        """현재 수력발전소 상태"""
        return {
            "active_flows": len(self.active_flows),
            "completed_flows": len(self.completed_flows),
            "total_energy": self.total_energy_generated,
            "memory_connected": self.memory is not None,
            "graph_connected": self.graph is not None,
            "metacog_connected": self.metacog is not None
        }


# 싱글톤
_hydro_instance: Optional[HydroMind] = None

def get_hydro_mind() -> HydroMind:
    """전역 HydroMind 인스턴스"""
    global _hydro_instance
    if _hydro_instance is None:
        _hydro_instance = HydroMind()
    return _hydro_instance


@contextmanager
def perceive_flow(action: str):
    """
    흐름 지각 컨텍스트 매니저
    
    Usage:
        with perceive_flow("질문에 답하기") as flow:
            result = think(question)
            flow.record(question, result)
    """
    hydro = get_hydro_mind()
    flow_id = hydro.begin_awareness(action)
    
    class FlowContext:
        def __init__(self, fid):
            self.flow_id = fid
        
        def record(self, input_data, output_data):
            hydro.record_flow(self.flow_id, input_data, output_data)
            hydro.integrate_to_graph(self.flow_id)
    
    try:
        yield FlowContext(flow_id)
    finally:
        hydro.end_awareness(flow_id)


def main():
    """테스트"""
    print("\n⚡ HydroMind Test")
    print("=" * 50)
    
    # 컨텍스트 매니저 사용
    with perceive_flow("테스트 사고") as flow:
        question = "엘리시아는 무엇인가?"
        answer = "파동 기반 지능체입니다."
        flow.record(question, answer)
    
    hydro = get_hydro_mind()
    status = hydro.get_status()
    
    print(f"\n📊 Status:")
    print(f"   Active flows: {status['active_flows']}")
    print(f"   Completed flows: {status['completed_flows']}")
    print(f"   Total energy: {status['total_energy']:.2f}")
    print(f"   Memory connected: {status['memory_connected']}")
    print(f"   Graph connected: {status['graph_connected']}")
    
    print("\n✅ HydroMind test complete!")


if __name__ == "__main__":
    main()
