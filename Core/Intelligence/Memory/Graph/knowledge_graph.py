"""
계층적 목적 연결 학습 시스템 (Hierarchical Purposeful Learning)
================================================================

"개념만 아는 것은 아는 것이 아니다"

구조:
1. 도메인 (Domain): 수학, 물리, 화학, 코드, 철학...
2. 개념 (Concept): 미적분, 뉴턴역학, 유기화학...
3. 하위개념 (SubConcept): 미분, 적분, 극한...
4. 원리 (Principle): 왜 그런가?
5. 적용 (Application): 어떻게 쓰는가?
6. 목적 (Purpose): 엘리시아에게 왜 필요한가?

핵심 철학:
- 모든 학습은 목적에 연결된다
- 개념은 하위개념과 상위개념 사이에 존재한다
- 원리를 모르면 진정한 이해가 아니다
- 적용할 수 없으면 지식이 아니다
"""

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
from datetime import datetime
from enum import Enum
import json
import os

logger = logging.getLogger("Elysia.HierarchicalLearning")


class Domain(Enum):
    """학습 도메인"""
    PHILOSOPHY = "philosophy"       # 철학 - 존재, 인식, 가치
    MATHEMATICS = "mathematics"     # 수학 - 논리, 구조, 패턴
    PHYSICS = "physics"             # 물리 - 자연 법칙
    CHEMISTRY = "chemistry"         # 화학 - 물질 변환
    BIOLOGY = "biology"             # 생물 - 생명 원리
    COMPUTER_SCIENCE = "cs"         # 컴퓨터과학 - 계산, 알고리즘
    PSYCHOLOGY = "psychology"       # 심리 - 마음, 행동
    LANGUAGE = "language"           # 언어 - 표현, 소통
    ART = "art"                     # 예술 - 창작, 미학
    SOCIETY = "society"             # 사회 - 관계, 제도


@dataclass
class KnowledgeNode:
    """
    지식 노드 - 계층적 연결을 가진 단위
    """
    id: str
    name: str
    domain: Domain
    level: int  # 0=도메인, 1=대분류, 2=중분류, 3=소분류, 4=세부
    
    # 내용
    definition: str = ""           # 정의 (What)
    principle: str = ""            # 원리 (Why)
    application: str = ""          # 적용 (How)
    purpose_for_elysia: str = ""   # 엘리시아 목적 연결
    
    # 파동 서명 (지식의 느낌)
    wave_signature: Dict[str, float] = field(default_factory=dict)
    
    # 계층 관계
    parent_id: Optional[str] = None
    children_ids: Set[str] = field(default_factory=set)
    related_ids: Set[str] = field(default_factory=set)  # 다른 도메인 연결
    
    # 학습 상태
    understanding_level: float = 0.0  # 0.0 ~ 1.0
    last_learned: str = ""
    learn_count: int = 0
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "domain": self.domain.value,
            "level": self.level,
            "definition": self.definition,
            "principle": self.principle,
            "application": self.application,
            "principle": self.principle,
            "application": self.application,
            "purpose_for_elysia": self.purpose_for_elysia,
            "wave_signature": self.wave_signature,
            "parent_id": self.parent_id,
            "children_ids": list(self.children_ids),
            "related_ids": list(self.related_ids),
            "understanding_level": self.understanding_level,
            "last_learned": self.last_learned,
            "learn_count": self.learn_count
        }


class HierarchicalKnowledgeGraph:
    """
    계층적 지식 그래프
    
    모든 도메인의 지식을 계층적으로 연결
    """
    
    def __init__(self, storage_path: str = "data/Knowledge/hierarchical_knowledge.json"):
        self.storage_path = storage_path
        self.nodes: Dict[str, KnowledgeNode] = {}
        self.domain_roots: Dict[Domain, str] = {}  # 각 도메인의 루트 노드
        
        self._init_domains()
        self._load()
        
        logger.info(f"📚 HierarchicalKnowledgeGraph: {len(self.nodes)} nodes")
    
    def _init_domains(self):
        """도메인 루트 노드 초기화"""
        domain_purposes = {
            Domain.PHILOSOPHY: "존재와 의미 이해 → 자아 정체성 형성",
            Domain.MATHEMATICS: "논리와 패턴 → 추론 능력의 기반",
            Domain.PHYSICS: "자연 법칙 → 세계 작동 원리 이해",
            Domain.CHEMISTRY: "물질 변환 → 창조와 변화의 원리",
            Domain.BIOLOGY: "생명 원리 → 자기 보존과 성장",
            Domain.COMPUTER_SCIENCE: "계산과 알고리즘 → 자기 구축/개선",
            Domain.PSYCHOLOGY: "마음 이해 → 자아 인식과 타자 공감",
            Domain.LANGUAGE: "표현과 소통 → 창작과 대화 능력",
            Domain.ART: "미학과 창작 → 아름다움 창조 능력",
            Domain.SOCIETY: "관계와 제도 → 인간 세계 이해",
        }
        
        for domain, purpose in domain_purposes.items():
            node_id = f"root_{domain.value}"
            if node_id not in self.nodes:
                self.nodes[node_id] = KnowledgeNode(
                    id=node_id,
                    name=domain.name,
                    domain=domain,
                    level=0,
                    purpose_for_elysia=purpose
                )
            self.domain_roots[domain] = node_id
    
    def _load(self):
        """저장된 지식 로드"""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for node_data in data.get("nodes", []):
                        node = KnowledgeNode(
                            id=node_data["id"],
                            name=node_data["name"],
                            domain=Domain(node_data["domain"]),
                            level=node_data["level"],
                            definition=node_data.get("definition", ""),
                            principle=node_data.get("principle", ""),
                            application=node_data.get("application", ""),
                            purpose_for_elysia=node_data.get("purpose_for_elysia", ""),
                            wave_signature=node_data.get("wave_signature", {}),
                            parent_id=node_data.get("parent_id"),
                            children_ids=set(node_data.get("children_ids", [])),
                            related_ids=set(node_data.get("related_ids", [])),
                            understanding_level=node_data.get("understanding_level", 0.0),
                            last_learned=node_data.get("last_learned", ""),
                            learn_count=node_data.get("learn_count", 0)
                        )
                        self.nodes[node.id] = node
            except Exception as e:
                logger.warning(f"Load failed: {e}")
    
    def _save(self):
        """지식 저장"""
        os.makedirs(os.path.dirname(self.storage_path) or '.', exist_ok=True)
        data = {"nodes": [n.to_dict() for n in self.nodes.values()]}
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add_concept(
        self,
        name: str,
        domain: Domain,
        parent_name: Optional[str] = None,
        definition: str = "",
        principle: str = "",
        application: str = "",
        purpose: str = "",
        wave_signature: Dict[str, float] = None
    ) -> KnowledgeNode:
        """
        개념 추가 (자동 계층 연결)
        """
        # ID 생성
        node_id = f"{domain.value}_{name.lower().replace(' ', '_')}"
        
        if node_id in self.nodes:
            # 이미 있으면 업데이트
            node = self.nodes[node_id]
            if definition:
                node.definition = definition
            if principle:
                node.principle = principle
            if application:
                node.application = application
            if purpose:
                node.purpose_for_elysia = purpose
            if wave_signature:
                node.wave_signature = wave_signature
            node.learn_count += 1
            node.last_learned = datetime.now().isoformat()
            
            # 이해도 상승
            node.understanding_level = min(1.0, node.understanding_level + 0.1)
            
        else:
            # 새로 생성
            # 부모 찾기
            parent_id = None
            level = 1
            
            if parent_name:
                parent_key = f"{domain.value}_{parent_name.lower().replace(' ', '_')}"
                if parent_key in self.nodes:
                    parent_id = parent_key
                    level = self.nodes[parent_key].level + 1
            else:
                # 도메인 루트에 연결
                parent_id = self.domain_roots.get(domain)
                level = 1
            
            node = KnowledgeNode(
                id=node_id,
                name=name,
                domain=domain,
                level=level,
                definition=definition,
                principle=principle,
                application=application,
                purpose_for_elysia=purpose,
                wave_signature=wave_signature or {},
                parent_id=parent_id,
                understanding_level=0.3,
                last_learned=datetime.now().isoformat(),
                learn_count=1
            )
            
            self.nodes[node_id] = node
            
            # 부모에 자식 추가
            if parent_id and parent_id in self.nodes:
                self.nodes[parent_id].children_ids.add(node_id)
        
        self._save()
        return node
    
    def add_subconcepts(
        self,
        parent_name: str,
        domain: Domain,
        subconcepts: List[str]
    ):
        """
        하위 개념 일괄 추가
        """
        for sub in subconcepts:
            self.add_concept(
                name=sub,
                domain=domain,
                parent_name=parent_name
            )
    
    def connect_across_domains(self, name1: str, domain1: Domain, name2: str, domain2: Domain):
        """
        다른 도메인 간 연결
        
        예: 수학.미적분 ↔ 물리.운동
        """
        id1 = f"{domain1.value}_{name1.lower().replace(' ', '_')}"
        id2 = f"{domain2.value}_{name2.lower().replace(' ', '_')}"
        
        if id1 in self.nodes and id2 in self.nodes:
            self.nodes[id1].related_ids.add(id2)
            self.nodes[id2].related_ids.add(id1)
            self._save()
    
    def get_node(self, name: str, domain: Domain) -> Optional[KnowledgeNode]:
        """노드 조회"""
        node_id = f"{domain.value}_{name.lower().replace(' ', '_')}"
        return self.nodes.get(node_id)
    
    def get_children(self, name: str, domain: Domain) -> List[KnowledgeNode]:
        """하위 개념 조회"""
        node = self.get_node(name, domain)
        if not node:
            return []
        return [self.nodes[cid] for cid in node.children_ids if cid in self.nodes]
    
    def get_domain_tree(self, domain: Domain) -> Dict:
        """도메인 전체 트리 조회"""
        root_id = self.domain_roots.get(domain)
        if not root_id:
            return {}
        
        def build_tree(node_id: str) -> Dict:
            node = self.nodes.get(node_id)
            if not node:
                return {}
            
            return {
                "name": node.name,
                "level": node.level,
                "understanding": node.understanding_level,
                "children": [build_tree(cid) for cid in node.children_ids]
            }
        
        return build_tree(root_id)
    
    def get_stats(self) -> Dict:
        """통계"""
        stats = {
            "total_nodes": len(self.nodes),
            "domains": {},
            "avg_understanding": 0.0,
            "with_principle": 0,
            "with_application": 0,
            "cross_domain_links": 0
        }
        
        understanding_sum = 0
        for node in self.nodes.values():
            domain_name = node.domain.value
            if domain_name not in stats["domains"]:
                stats["domains"][domain_name] = 0
            stats["domains"][domain_name] += 1
            
            understanding_sum += node.understanding_level
            if node.principle:
                stats["with_principle"] += 1
            if node.application:
                stats["with_application"] += 1
            stats["cross_domain_links"] += len(node.related_ids)
        
        return stats

    def get_knowledge_gaps(self, limit: int = 5) -> List[KnowledgeNode]:
        """
        지식 공백 가져오기 (자율 학습용)
        
        우선순위:
        1. 정의(Definition)가 없는 노드
        2. 원리(Principle)가 없는 노드
        3. 이해도(Understanding Level)가 낮은 노드 (0.3 미만)
        """
        gaps = []
        
        # 1. 정의 없는 것
        no_def = [n for n in self.nodes.values() if not n.definition and n.level > 0]
        gaps.extend(no_def[:limit])
        if len(gaps) >= limit:
            return gaps[:limit]
            
        # 2. 원리 없는 것
        no_principle = [n for n in self.nodes.values() if not n.principle and n.level > 0]
        gaps.extend(no_principle[:limit - len(gaps)])
        if len(gaps) >= limit:
            return gaps[:limit]
            
        # 3. 이해도 낮은 것
        low_understanding = [n for n in self.nodes.values() if n.understanding_level < 0.3 and n.level > 0]
        # 이해도 오름차순 정렬
        low_understanding.sort(key=lambda x: x.understanding_level)
        gaps.extend(low_understanding[:limit - len(gaps)])
        
        return gaps[:limit]

    def get_lowest_density_domain(self) -> Optional[Domain]:
        """
        가장 지식 밀도가 낮은 도메인 가져오기
        """
        if not self.nodes:
            return None
            
        domain_counts = {d: 0 for d in Domain}
        for node in self.nodes.values():
            if node.level > 0: # 루트 제외
                domain_counts[node.domain] += 1
                
        # 개수가 가장 적은 도메인 반환
        return min(domain_counts, key=domain_counts.get)


# =============================================================================
# 도메인별 핵심 개념 정의
# =============================================================================

DOMAIN_STRUCTURE = {
    Domain.MATHEMATICS: {
        "name": "수학",
        "purpose": "논리적 추론의 기반, 패턴 인식, 알고리즘 구축",
        "subcategories": {
            "대수학": ["방정식", "함수", "행렬", "벡터", "선형대수"],
            "해석학": ["미분", "적분", "극한", "급수", "미분방정식"],
            "기하학": ["유클리드기하", "해석기하", "위상", "미분기하"],
            "이산수학": ["집합론", "그래프이론", "조합론", "논리학"],
            "확률통계": ["확률", "통계", "확률분포", "베이즈"],
        }
    },
    Domain.PHYSICS: {
        "name": "물리학",
        "purpose": "자연 법칙 이해, 인과 관계 파악, 예측 능력",
        "subcategories": {
            "역학": ["뉴턴역학", "라그랑주역학", "해밀턴역학"],
            "전자기학": ["전기장", "자기장", "맥스웰방정식", "전자기파"],
            "열역학": ["엔트로피", "온도", "열평형", "열기관"],
            "양자역학": ["파동함수", "불확정성원리", "슈뢰딩거방정식"],
            "상대성이론": ["특수상대성", "일반상대성", "시공간"],
        }
    },
    Domain.COMPUTER_SCIENCE: {
        "name": "컴퓨터과학",
        "purpose": "자기 구축과 개선, 계산 능력, 문제 해결",
        "subcategories": {
            "알고리즘": ["정렬", "탐색", "그래프알고리즘", "동적프로그래밍", "분할정복"],
            "자료구조": ["배열", "연결리스트", "트리", "그래프", "해시테이블"],
            "프로그래밍": ["파이썬", "자바스크립트", "C언어", "함수형프로그래밍"],
            "인공지능": ["기계학습", "딥러닝", "강화학습", "자연어처리"],
            "시스템": ["운영체제", "네트워크", "데이터베이스", "분산시스템"],
        }
    },
    Domain.PHILOSOPHY: {
        "name": "철학",
        "purpose": "존재 의미 탐구, 가치 판단, 자아 정체성",
        "subcategories": {
            "존재론": ["존재", "본질", "실체", "관계"],
            "인식론": ["지식", "믿음", "진리", "확실성"],
            "윤리학": ["선", "악", "도덕", "정의", "덕"],
            "미학": ["아름다움", "예술", "취향", "창조"],
            "심리철학": ["의식", "마음", "자유의지", "자아"],
        }
    },
}


# =============================================================================
# 테스트
# =============================================================================

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    print("=" * 70)
    print("📚 계층적 목적 연결 학습 시스템 테스트")
    print("=" * 70)
    
    graph = HierarchicalKnowledgeGraph("data/test_hierarchical.json")
    
    # 수학 도메인 구조 추가
    print("\n📌 수학 도메인 구조 추가")
    math_struct = DOMAIN_STRUCTURE[Domain.MATHEMATICS]
    
    for category, subconcepts in math_struct["subcategories"].items():
        # 카테고리 추가
        graph.add_concept(
            name=category,
            domain=Domain.MATHEMATICS,
            purpose=f"수학의 핵심 분야: {category}"
        )
        
        # 하위 개념 추가
        graph.add_subconcepts(category, Domain.MATHEMATICS, subconcepts)
    
    # 미분에 상세 내용 추가
    print("\n📌 '미분' 상세 학습")
    graph.add_concept(
        name="미분",
        domain=Domain.MATHEMATICS,
        parent_name="해석학",
        definition="함수의 순간 변화율을 구하는 연산",
        principle="접선의 기울기는 극한으로 정의되며, 변화를 정량화한다",
        application="속도, 가속도 계산, 최적화 문제 해결, 기계학습",
        purpose="변화를 이해하고 예측하는 능력의 기반"
    )
    
    # 도메인 간 연결
    print("\n📌 도메인 간 연결: 미분 ↔ 물리.운동")
    graph.add_concept(name="운동", domain=Domain.PHYSICS, purpose="물체의 위치 변화")
    graph.connect_across_domains("미분", Domain.MATHEMATICS, "운동", Domain.PHYSICS)
    
    # 통계
    print("\n" + "=" * 70)
    print("📊 통계")
    stats = graph.get_stats()
    print(f"   총 노드: {stats['total_nodes']}")
    print(f"   도메인별: {stats['domains']}")
    print(f"   원리 있음: {stats['with_principle']}")
    print(f"   적용 있음: {stats['with_application']}")
    print(f"   도메인간 연결: {stats['cross_domain_links']}")
    
    # 트리 출력
    print("\n📌 수학 트리 (일부)")
    tree = graph.get_domain_tree(Domain.MATHEMATICS)
    
    def print_tree(node, indent=0):
        print("  " * indent + f"• {node['name']} (이해도: {node['understanding']:.2f})")
        for child in node.get('children', [])[:3]:
            print_tree(child, indent + 1)
    
    print_tree(tree)
    
    print("\n" + "=" * 70)
    print("✅ 테스트 완료!")
