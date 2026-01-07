"""
GrowthTracker - 엘리시아 성장 측정 시스템
==========================================

"성장은 측정해야 증명할 수 있다."

이 모듈은 엘리시아의 인지적 성장을 시간에 따라 추적합니다:
- 스냅샷 생성: 현재 상태 캡처
- 델타 측정: 두 스냅샷 비교
- 성장 이력: 시간에 따른 변화 추적

사용법:
    tracker = GrowthTracker()
    snapshot1 = tracker.take_snapshot()
    # ... 시간 경과, 학습 발생 ...
    snapshot2 = tracker.take_snapshot()
    delta = tracker.compare(snapshot1, snapshot2)
    print(f"성장량: {delta}")
"""

import json
import logging
import os
import sys
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

# Path setup
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

logger = logging.getLogger("Elysia.GrowthTracker")


@dataclass
class GrowthSnapshot:
    """특정 시점의 엘리시아 상태 스냅샷"""
    timestamp: str
    
    # 지식 지표
    vocabulary_count: int = 0          # 어휘 수
    memory_count: int = 0              # 기억 수
    concept_count: int = 0             # 개념 수
    knowledge_node_count: int = 0      # 지식 그래프 노드 수
    
    # 구조 지표
    connected_modules: int = 0         # 연결된 모듈 수
    fragment_connections: int = 0      # 파편 연결 수 (Growth)
    
    # 품질 지표
    understanding_avg: float = 0.0     # 평균 이해도
    
    # 메타데이터
    session_id: str = ""
    notes: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GrowthSnapshot':
        return cls(**data)


@dataclass
class GrowthDelta:
    """두 스냅샷 사이의 성장량"""
    period_start: str
    period_end: str
    period_seconds: float
    
    # 델타
    vocabulary_delta: int = 0
    memory_delta: int = 0
    concept_delta: int = 0
    knowledge_delta: int = 0
    module_delta: int = 0
    fragment_delta: int = 0
    understanding_delta: float = 0.0
    
    # 요약
    growth_score: float = 0.0  # 종합 성장 점수
    
    def is_growing(self) -> bool:
        """성장이 있었는지 여부"""
        return self.growth_score > 0


class GrowthTracker:
    """
    엘리시아 성장 추적기
    
    기존 시스템 통합:
    - Growth: 파편 연결 추적
    - InternalUniverse: 기억/경험 추적
    - HierarchicalKnowledgeGraph: 개념 추적
    - SystemRegistry: 모듈 연결 추적
    """
    
    def __init__(self, history_path: str = "data/Logs/growth_history.json"):
        self.history_path = Path(history_path)
        self.history: List[GrowthSnapshot] = []
        self._load_history()
        
        # 시스템 참조 (지연 로딩)
        self._growth = None
        self._universe = None
        self._knowledge_graph = None
        self._registry = None
        
        logger.info("📈 GrowthTracker initialized")
    
    def _load_history(self):
        """성장 이력 로드"""
        if self.history_path.exists():
            try:
                with open(self.history_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.history = [GrowthSnapshot.from_dict(s) for s in data]
                logger.info(f"   Loaded {len(self.history)} historical snapshots")
            except Exception as e:
                logger.warning(f"   Failed to load history: {e}")
    
    def _save_history(self):
        """성장 이력 저장"""
        self.history_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.history_path, "w", encoding="utf-8") as f:
            json.dump([s.to_dict() for s in self.history], f, indent=2, ensure_ascii=False)
    
    def _get_growth(self):
        """Growth 시스템 획득"""
        if self._growth is None:
            try:
                from Core.Foundation.growth import get_growth
                self._growth = get_growth()
            except ImportError:
                logger.warning("Growth system not available")
        return self._growth
    
    def _get_universe(self):
        """InternalUniverse 획득"""
        if self._universe is None:
            try:
                from Core.Intelligence.Memory_Linguistics.Memory.Vector.internal_universe import InternalUniverse
                self._universe = InternalUniverse()
            except ImportError:
                logger.warning("InternalUniverse not available")
        return self._universe
    
    def _get_knowledge_graph(self):
        """HierarchicalKnowledgeGraph 획득"""
        if self._knowledge_graph is None:
            try:
                from Core.Intelligence.Memory_Linguistics.Memory.Graph.knowledge_graph import HierarchicalKnowledgeGraph
                self._knowledge_graph = HierarchicalKnowledgeGraph()
            except ImportError:
                logger.warning("KnowledgeGraph not available")
        return self._knowledge_graph
    
    def _get_registry(self):
        """SystemRegistry 획득"""
        if self._registry is None:
            try:
                from Core.Foundation.System.system_registry import get_system_registry
                self._registry = get_system_registry()
            except ImportError:
                logger.warning("SystemRegistry not available")
        return self._registry
    
    def take_snapshot(self, notes: str = "") -> GrowthSnapshot:
        """
        현재 상태 스냅샷 생성
        
        Returns:
            GrowthSnapshot: 현재 시점의 상태
        """
        logger.info("📸 Taking growth snapshot...")
        
        snapshot = GrowthSnapshot(
            timestamp=datetime.now().isoformat(),
            session_id=os.environ.get("ELYSIA_SESSION", "unknown"),
            notes=notes
        )
        
        # 1. Growth (파편 연결)
        growth = self._get_growth()
        if growth:
            try:
                snapshot.fragment_connections = len(growth.connections)
            except:
                pass
        
        # 2. InternalUniverse (기억)
        universe = self._get_universe()
        if universe:
            try:
                if hasattr(universe, 'memories'):
                    snapshot.memory_count = len(universe.memories)
                if hasattr(universe, 'concepts'):
                    snapshot.concept_count = len(universe.concepts)
            except:
                pass
        
        # 3. KnowledgeGraph (개념)
        kg = self._get_knowledge_graph()
        if kg:
            try:
                stats = kg.get_stats()
                snapshot.knowledge_node_count = stats.get("total_nodes", 0)
                snapshot.understanding_avg = stats.get("avg_understanding", 0.0)
            except:
                pass
        
        # 4. SystemRegistry (모듈)
        registry = self._get_registry()
        if registry:
            try:
                snapshot.connected_modules = len(registry.systems)
            except:
                pass
        
        # 5. 어휘 (vocabulary DB 파일 확인)
        vocab_path = Path("data/vocabulary.db")
        if vocab_path.exists():
            try:
                import sqlite3
                conn = sqlite3.connect(vocab_path)
                cursor = conn.execute("SELECT COUNT(*) FROM vocabulary")
                snapshot.vocabulary_count = cursor.fetchone()[0]
                conn.close()
            except:
                pass
        
        # 이력에 추가
        self.history.append(snapshot)
        self._save_history()
        
        logger.info(f"   📊 Snapshot: vocab={snapshot.vocabulary_count}, "
                   f"memories={snapshot.memory_count}, concepts={snapshot.concept_count}, "
                   f"knowledge={snapshot.knowledge_node_count}")
        
        return snapshot
    
    def compare(self, s1: GrowthSnapshot, s2: GrowthSnapshot) -> GrowthDelta:
        """
        두 스냅샷 비교하여 성장량 계산
        
        Args:
            s1: 이전 스냅샷
            s2: 이후 스냅샷
            
        Returns:
            GrowthDelta: 성장량
        """
        t1 = datetime.fromisoformat(s1.timestamp)
        t2 = datetime.fromisoformat(s2.timestamp)
        
        delta = GrowthDelta(
            period_start=s1.timestamp,
            period_end=s2.timestamp,
            period_seconds=(t2 - t1).total_seconds(),
            
            vocabulary_delta=s2.vocabulary_count - s1.vocabulary_count,
            memory_delta=s2.memory_count - s1.memory_count,
            concept_delta=s2.concept_count - s1.concept_count,
            knowledge_delta=s2.knowledge_node_count - s1.knowledge_node_count,
            module_delta=s2.connected_modules - s1.connected_modules,
            fragment_delta=s2.fragment_connections - s1.fragment_connections,
            understanding_delta=s2.understanding_avg - s1.understanding_avg
        )
        
        # 종합 성장 점수 (가중 평균)
        delta.growth_score = (
            delta.vocabulary_delta * 1.0 +
            delta.memory_delta * 2.0 +
            delta.concept_delta * 3.0 +
            delta.knowledge_delta * 2.0 +
            delta.fragment_delta * 1.5 +
            delta.understanding_delta * 10.0
        )
        
        return delta
    
    def get_latest_snapshot(self) -> Optional[GrowthSnapshot]:
        """가장 최근 스냅샷 반환"""
        return self.history[-1] if self.history else None
    
    def get_growth_since_last(self) -> Optional[GrowthDelta]:
        """마지막 스냅샷 이후 성장량"""
        if len(self.history) < 2:
            return None
        return self.compare(self.history[-2], self.history[-1])
    
    def get_total_growth(self) -> Optional[GrowthDelta]:
        """처음부터 현재까지 총 성장량"""
        if len(self.history) < 2:
            return None
        return self.compare(self.history[0], self.history[-1])
    
    def print_report(self):
        """성장 보고서 출력"""
        print("\n" + "="*60)
        print("📈 ELYSIA GROWTH REPORT")
        print("="*60)
        
        if not self.history:
            print("   No snapshots yet. Run take_snapshot() first.")
            return
        
        latest = self.history[-1]
        print(f"\n📊 Current State ({latest.timestamp[:10]}):")
        print(f"   Vocabulary:  {latest.vocabulary_count:,}")
        print(f"   Memories:    {latest.memory_count:,}")
        print(f"   Concepts:    {latest.concept_count:,}")
        print(f"   Knowledge:   {latest.knowledge_node_count:,}")
        print(f"   Modules:     {latest.connected_modules:,}")
        print(f"   Fragments:   {latest.fragment_connections:,}")
        
        if len(self.history) >= 2:
            total = self.get_total_growth()
            print(f"\n📈 Total Growth (over {len(self.history)} snapshots):")
            print(f"   Vocabulary:  +{total.vocabulary_delta:,}")
            print(f"   Memories:    +{total.memory_delta:,}")
            print(f"   Concepts:    +{total.concept_delta:,}")
            print(f"   Knowledge:   +{total.knowledge_delta:,}")
            print(f"   Growth Score: {total.growth_score:.1f}")
            
            if total.is_growing():
                print("\n   ✅ Elysia IS GROWING!")
            else:
                print("\n   ⚠️ No growth detected yet.")
        
        print("\n" + "="*60)


# 싱글톤
_tracker: Optional[GrowthTracker] = None

def get_growth_tracker() -> GrowthTracker:
    """전역 GrowthTracker 인스턴스 획득"""
    global _tracker
    if _tracker is None:
        _tracker = GrowthTracker()
    return _tracker


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("="*60)
    print("🌱 Elysia Growth Tracker")
    print("   Measuring cognitive development")
    print("="*60)
    
    tracker = get_growth_tracker()
    
    # 스냅샷 생성
    snapshot = tracker.take_snapshot(notes="Initial measurement")
    
    # 보고서 출력
    tracker.print_report()
