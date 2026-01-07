"""
Potential Causality System (잠재적 인과 시스템)
================================================

"검색 결과를 바로 원리로 확정하지 않고, 
 잠재적 인과로 유지하다가 연결이 쌓이면 확정한다"

철학:
- 처음 배운 것은 "아는 것"이 아니라 "들은 것"
- 다른 지식과 연결될 때 비로소 "이해한 것"이 됨
- 여러 곳에서 확인되면 "확신하는 것"이 됨

구조:
1. PotentialKnowledge: 임시 주파수를 가진 잠재 지식
2. 연결이 생길 때마다 frequency++
3. 임계점(threshold) 넘으면 → 확정 원리로 승격
"""

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
from datetime import datetime
import json
import os

logger = logging.getLogger("Elysia.PotentialCausality")


@dataclass
class PotentialKnowledge:
    """
    잠재적 지식 - 아직 확정되지 않은 인과 관계
    """
    subject: str              # 주제 (예: "사랑")
    definition: str           # 정의 (예: "깊은 상호 인격적인 애정")
    source: str               # 출처 (naver, wikipedia, etc.)
    
    # 잠재 상태
    frequency: float = 0.3    # 초기 주파수 (확신도)
    connections: Set[str] = field(default_factory=set)  # 연결된 다른 개념들
    confirmations: int = 1    # 확인 횟수
    
    # 메타데이터
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_connected: str = ""
    
    def connect(self, other_subject: str):
        """다른 개념과 연결 - 주파수 상승"""
        if other_subject not in self.connections:
            self.connections.add(other_subject)
            self.frequency = min(1.0, self.frequency + 0.1)  # 연결당 +0.1
            self.last_connected = datetime.now().isoformat()
            logger.info(f"   🔗 Connected: {self.subject} ↔ {other_subject} (freq={self.frequency:.2f})")
    
    def confirm(self, new_source: str):
        """다른 소스에서 확인 - 주파수 대폭 상승"""
        self.confirmations += 1
        self.frequency = min(1.0, self.frequency + 0.2)  # 확인당 +0.2
        logger.info(f"   ✅ Confirmed: {self.subject} by {new_source} (freq={self.frequency:.2f})")
    
    def is_crystallizable(self, threshold: float = 0.7) -> bool:
        """확정 가능 여부 (임계점 초과?)"""
        return self.frequency >= threshold
    
    def to_dict(self) -> dict:
        return {
            "subject": self.subject,
            "definition": self.definition,
            "source": self.source,
            "frequency": self.frequency,
            "connections": list(self.connections),
            "confirmations": self.confirmations,
            "created_at": self.created_at,
            "last_connected": self.last_connected
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'PotentialKnowledge':
        pk = PotentialKnowledge(
            subject=data["subject"],
            definition=data["definition"],
            source=data["source"],
            frequency=data.get("frequency", 0.3),
            connections=set(data.get("connections", [])),
            confirmations=data.get("confirmations", 1),
            created_at=data.get("created_at", ""),
            last_connected=data.get("last_connected", "")
        )
        return pk


class PotentialCausalityStore:
    """
    잠재적 인과 저장소
    
    - 검색 결과를 잠재적 지식으로 저장
    - 연결/확인 시 주파수 증가
    - 확정 시 TorchGraph로 이동
    """
    
    def __init__(self, storage_path: str = "data/Knowledge/potential_knowledge.json"):
        self.storage_path = storage_path
        self.knowledge: Dict[str, PotentialKnowledge] = {}
        self.crystallized_count = 0
        
        self._load()
        logger.info(f"💭 PotentialCausalityStore: {len(self.knowledge)} items loaded")
    
    def _load(self):
        """저장된 잠재 지식 로드"""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for item in data.get("knowledge", []):
                        pk = PotentialKnowledge.from_dict(item)
                        self.knowledge[pk.subject] = pk
                    self.crystallized_count = data.get("crystallized_count", 0)
            except Exception as e:
                logger.warning(f"Failed to load: {e}")
    
    def _save(self):
        """잠재 지식 저장"""
        os.makedirs(os.path.dirname(self.storage_path) or '.', exist_ok=True)
        data = {
            "knowledge": [pk.to_dict() for pk in self.knowledge.values()],
            "crystallized_count": self.crystallized_count
        }
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def store(self, subject: str, definition: str, source: str) -> PotentialKnowledge:
        """
        잠재적 지식 저장
        
        - 이미 있으면: 확인(confirm)으로 주파수 증가
        - 없으면: 새로 생성
        """
        subject_lower = subject.lower().strip()
        
        if subject_lower in self.knowledge:
            # 이미 있으면 확인
            self.knowledge[subject_lower].confirm(source)
        else:
            # 새로 생성
            self.knowledge[subject_lower] = PotentialKnowledge(
                subject=subject,
                definition=definition,
                source=source
            )
            logger.info(f"   💭 New potential: {subject} (freq=0.3)")
        
        self._save()
        return self.knowledge[subject_lower]
    
    def connect(self, subject1: str, subject2: str):
        """두 개념 연결 - 양쪽 주파수 상승"""
        s1, s2 = subject1.lower().strip(), subject2.lower().strip()
        
        if s1 in self.knowledge:
            self.knowledge[s1].connect(subject2)
        if s2 in self.knowledge:
            self.knowledge[s2].connect(subject1)
        
        self._save()
    
    def get(self, subject: str) -> Optional[PotentialKnowledge]:
        """잠재 지식 조회"""
        return self.knowledge.get(subject.lower().strip())
    
    def find_related(self, subject: str) -> List[str]:
        """관련 개념 찾기 (정의 내 키워드 매칭)"""
        related = []
        subject_lower = subject.lower().strip()
        
        for key, pk in self.knowledge.items():
            if key == subject_lower:
                continue
            # 정의에 해당 단어가 포함되어 있으면 관련
            if subject in pk.definition or pk.subject in self.get(subject_lower).definition if self.get(subject_lower) else False:
                related.append(pk.subject)
        
        return related
    
    def auto_connect(self, subject: str):
        """
        자동 연결 - 정의 내 다른 개념들과 연결
        
        예: "사랑 = 깊은 상호 인격적인 애정"
            → "애정"이 잠재 지식에 있으면 연결
        """
        pk = self.get(subject)
        if not pk:
            return
        
        # 정의 내 단어들
        words = pk.definition.replace(",", " ").replace(".", " ").split()
        
        for word in words:
            if len(word) > 1 and word.lower() in self.knowledge:
                self.connect(subject, word)
    
    def get_crystallizable(self, threshold: float = 0.7) -> List[PotentialKnowledge]:
        """확정 가능한 지식들 반환"""
        return [pk for pk in self.knowledge.values() if pk.is_crystallizable(threshold)]
    
    def crystallize(self, subject: str) -> Optional[Dict]:
        """
        확정 - 잠재 지식 → 확정 원리
        
        Returns: 확정된 원리 정보 (TorchGraph에 추가할 형태)
        """
        pk = self.get(subject)
        if not pk or not pk.is_crystallizable():
            return None
        
        # 확정 원리 형태로 변환
        crystallized = {
            "concept": pk.subject,
            "definition": pk.definition,
            "confidence": pk.frequency,
            "connections": list(pk.connections),
            "confirmations": pk.confirmations,
            "crystallized_at": datetime.now().isoformat()
        }
        
        # 잠재 저장소에서 제거
        del self.knowledge[subject.lower().strip()]
        self.crystallized_count += 1
        self._save()
        
        logger.info(f"   💎 Crystallized: {pk.subject} (freq={pk.frequency:.2f})")
        
        return crystallized
    
    def status(self) -> Dict:
        """상태 요약"""
        return {
            "potential_count": len(self.knowledge),
            "crystallized_count": self.crystallized_count,
            "avg_frequency": sum(pk.frequency for pk in self.knowledge.values()) / len(self.knowledge) if self.knowledge else 0,
            "crystallizable": len(self.get_crystallizable())
        }


# =============================================================================
# 테스트
# =============================================================================

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    print("=" * 60)
    print("💭 Potential Causality System Test")
    print("=" * 60)
    
    store = PotentialCausalityStore("data/test_potential.json")
    
    # 1. 검색 결과 저장 (잠재 지식)
    print("\n📌 1. 잠재 지식 저장")
    store.store("사랑", "깊은 상호 인격적인 애정에서 단순한 즐거움까지를 아우르는 감정", "wikipedia")
    store.store("자유", "무언가를 스스로 시작할 힘으로 인간관계를 시작하는 최초의 원인", "naver")
    store.store("애정", "상대방을 좋아하고 아끼는 마음", "naver")
    
    # 2. 다른 소스에서 확인
    print("\n📌 2. 다른 소스에서 확인")
    store.store("사랑", "타인에 대한 깊은 감정적 유대", "naver")  # confirm!
    
    # 3. 연결
    print("\n📌 3. 개념 연결")
    store.connect("사랑", "애정")
    
    # 4. 자동 연결
    print("\n📌 4. 자동 연결")
    store.auto_connect("사랑")
    
    # 5. 상태 확인
    print("\n📌 5. 상태")
    status = store.status()
    print(f"   잠재 지식: {status['potential_count']}개")
    print(f"   확정 가능: {status['crystallizable']}개")
    print(f"   평균 주파수: {status['avg_frequency']:.2f}")
    
    # 6. 각 지식 상태
    print("\n📌 6. 각 지식 상태")
    for pk in store.knowledge.values():
        print(f"   • {pk.subject}: freq={pk.frequency:.2f}, connections={len(pk.connections)}, crystallizable={pk.is_crystallizable()}")
    
    # 7. 확정 시도
    print("\n📌 7. 확정 시도")
    for pk in store.get_crystallizable():
        result = store.crystallize(pk.subject)
        if result:
            print(f"   💎 {result['concept']} → 확정됨!")
    
    print("\n" + "=" * 60)
    print("✅ Test complete!")
