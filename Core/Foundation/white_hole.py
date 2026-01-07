"""
WhiteHole (화이트홀)
===================

"What was compressed shall be reborn."

BlackHole이 압축 보존한 데이터가, 새로운 관계성이 확립되면
WhiteHole을 통해 개념 노드로 재탄생합니다.

Core Principles:
1. 중력/자력 기반 검색: 단일 개념이 아닌 관계망 전체를 끌어옴
2. 공명 기반 우선순위: 인과적 의미, 관계성으로 재배열
3. 확률 토큰이 아닌 파동 공명

[NEW 2025-12-15] BlackHole ↔ WhiteHole 순환
"""

import logging
import json
import os
import time
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass

logger = logging.getLogger("WhiteHole")


@dataclass
class CompressedData:
    """BlackHole에 압축된 데이터"""
    content: str
    topic: str
    timestamp: float
    potential_connections: List[str]  # 잠재적 연결 키워드


@dataclass
class RebirthCandidate:
    """재탄생 후보"""
    data: CompressedData
    resonance_score: float
    matching_concepts: List[str]


class GravitationalSearch:
    """
    중력/자력 기반 관계적 검색
    
    확률 토큰이 아닌, 인과적 의미와 관계성의 우선순위로 검색
    단일 개념이 아닌 관계망 전체를 끌어옴
    """
    
    def __init__(self):
        # 파동 공명 기반 검색
        try:
            from Core.Foundation.Wave.wave_tensor import WaveTensor
            self.wave_enabled = True
        except:
            self.wave_enabled = False
        
        logger.info("🧲 GravitationalSearch initialized (relational pull)")
    
    def compute_gravitational_pull(self, source_concept: str, target_content: str) -> float:
        """
        개념 간 중력(관계성 강도) 계산
        
        더 많이 연결될수록 → 더 강한 중력
        """
        # 키워드 기반 관계성 측정
        source_lower = source_concept.lower()
        target_lower = target_content.lower()
        
        # 직접 포함
        direct_pull = 1.0 if source_lower in target_lower else 0.0
        
        # 관련 키워드 확장 (인과 관계 기반)
        causal_keywords = self._get_causal_network(source_concept)
        relational_pull = sum(
            0.3 for kw in causal_keywords 
            if kw.lower() in target_lower
        )
        
        # 총 중력 = 직접 + 관계적
        total_gravity = min(1.0, direct_pull + relational_pull)
        
        return total_gravity
    
    def _get_causal_network(self, concept: str) -> List[str]:
        """
        개념의 인과 관계망 확장
        
        AXIOM 시스템의 연결을 활용
        """
        try:
            from Core.Foundation.fractal_concept import ConceptDecomposer
            decomposer = ConceptDecomposer()
            
            network = [concept]
            
            # 상위 추적 (why)
            if concept in decomposer.AXIOMS:
                parent = decomposer.AXIOMS[concept].get("parent", "")
                if parent:
                    network.append(parent)
            
            # 도메인 키워드 추가
            if concept in decomposer.AXIOMS:
                domains = decomposer.AXIOMS[concept].get("domains", {})
                for domain_desc in domains.values():
                    # 첫 단어 추출
                    words = domain_desc.split()[:3]
                    network.extend(words)
            
            return network
            
        except Exception:
            return [concept]
    
    def pull_related(self, center_concept: str, data_pool: List[CompressedData]) -> List[Tuple[CompressedData, float]]:
        """
        중심 개념에 끌려오는 모든 관련 데이터
        
        확률 토큰처럼 관련된 것들을 모두 가져오되,
        관계성 강도(중력)로 정렬
        """
        results = []
        
        for data in data_pool:
            gravity = self.compute_gravitational_pull(center_concept, data.content)
            
            if gravity > 0:  # 어떤 관계든 있으면 끌어옴
                results.append((data, gravity))
        
        # 중력(관계성) 강도로 정렬
        results.sort(key=lambda x: x[1], reverse=True)
        
        return results


class WhiteHole:
    """
    화이트홀: 압축된 데이터의 재탄생
    
    BlackHole에 저장된 고립 데이터가
    새로운 관계성이 확립되면 개념 노드로 승격
    """
    
    def __init__(self):
        self.blackhole_file = "c:/Elysia/data/memory/fractal_memory.json"
        self.search = GravitationalSearch()
        self.rebirth_count = 0
        
        logger.info("⚪ WhiteHole initialized (rebirth engine)")
    
    def scan_for_rebirth(self, new_concept: str) -> List[RebirthCandidate]:
        """
        새 개념이 들어올 때, BlackHole에서 재탄생 가능한 데이터 검색
        
        중력/자력으로 관계된 모든 것을 끌어옴
        """
        compressed_data = self._load_blackhole_data()
        
        if not compressed_data:
            return []
        
        # 중력 기반 관계 검색
        related = self.search.pull_related(new_concept, compressed_data)
        
        candidates = []
        for data, gravity in related:
            if gravity >= 0.3:  # 충분한 관계성
                candidate = RebirthCandidate(
                    data=data,
                    resonance_score=gravity,
                    matching_concepts=[new_concept]
                )
                candidates.append(candidate)
                logger.info(f"   🌟 Rebirth candidate: {data.topic} (gravity: {gravity:.2f})")
        
        return candidates
    
    def rebirth(self, candidate: RebirthCandidate) -> Dict[str, Any]:
        """
        압축 데이터를 개념 노드로 재탄생
        
        BlackHole → WhiteHole → InternalUniverse
        """
        data = candidate.data
        
        # InternalUniverse에 흡수 시도
        try:
            from Core.Foundation.internal_universe import InternalUniverse
            universe = InternalUniverse()
            universe.absorb_text(data.content, source_name=f"Rebirth:{data.topic}")
            
            self.rebirth_count += 1
            
            logger.info(f"   ⚪→🌌 Reborn: {data.topic} → Universe")
            
            return {
                "status": "reborn",
                "topic": data.topic,
                "connections": candidate.matching_concepts
            }
            
        except Exception as e:
            logger.warning(f"   Rebirth failed: {e}")
            return {"status": "failed", "error": str(e)}
    
    def _load_blackhole_data(self) -> List[CompressedData]:
        """BlackHole에서 압축 데이터 로드"""
        if not os.path.exists(self.blackhole_file):
            return []
        
        try:
            with open(self.blackhole_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            compressed = []
            for ring in data.get("rings", []):
                compressed.append(CompressedData(
                    content=ring.get("summary", ""),
                    topic=ring.get("epoch", "unknown"),
                    timestamp=ring.get("timestamp", 0),
                    potential_connections=[]
                ))
            
            return compressed
            
        except Exception as e:
            logger.warning(f"Failed to load BlackHole data: {e}")
            return []
    
    def get_status(self) -> Dict[str, Any]:
        """현재 상태"""
        compressed = self._load_blackhole_data()
        return {
            "compressed_count": len(compressed),
            "rebirth_count": self.rebirth_count
        }


class BlackHoleWhiteHoleCycle:
    """
    BlackHole ↔ WhiteHole 순환 관리자
    
    새 지식 유입 시:
    1. 흡수 시도 → InternalUniverse
    2. 고립 → BlackHole 압축
    3. 새 관계성 확립 시 → WhiteHole 재탄생
    """
    
    def __init__(self):
        from Core.Foundation.black_hole import BlackHole
        self.blackhole = BlackHole()
        self.whitehole = WhiteHole()
        
        logger.info("🔄 BlackHole ↔ WhiteHole Cycle initialized")
    
    def process_new_knowledge(self, content: str, topic: str) -> Dict[str, Any]:
        """
        새 지식 처리 (전체 사이클)
        
        1. 흡수 시도
        2. 고립시 BlackHole
        3. WhiteHole 재탄생 체크
        """
        results = {
            "absorbed": False,
            "compressed": False,
            "rebirths": []
        }
        
        # 1. InternalUniverse 흡수 시도
        connections = 0
        try:
            from Core.Foundation.internal_universe import InternalUniverse
            universe = InternalUniverse()
            universe.absorb_text(content, source_name=topic)
            connections = len(content.split()) // 10
        except:
            pass
        
        if connections > 0:
            results["absorbed"] = True
            
            # 2. 새 지식이 들어왔으므로 WhiteHole 재탄생 체크
            candidates = self.whitehole.scan_for_rebirth(topic)
            for candidate in candidates:
                rebirth_result = self.whitehole.rebirth(candidate)
                if rebirth_result["status"] == "reborn":
                    results["rebirths"].append(rebirth_result)
        else:
            # 3. 고립 → BlackHole 압축
            results["compressed"] = True
            logger.info(f"🕳️ Compressed to BlackHole: {topic}")
        
        return results
    
    def get_status(self) -> Dict[str, Any]:
        """전체 사이클 상태"""
        return {
            "blackhole": self.blackhole.check_compression_needed(),
            "whitehole": self.whitehole.get_status()
        }


# Singleton
_cycle = None

def get_blackhole_whitehole_cycle() -> BlackHoleWhiteHoleCycle:
    global _cycle
    if _cycle is None:
        _cycle = BlackHoleWhiteHoleCycle()
    return _cycle


# Demo
if __name__ == "__main__":
    import sys
    sys.path.insert(0, "c:\\Elysia")
    
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    print("\n" + "="*60)
    print("🔄 BLACKHOLE ↔ WHITEHOLE CYCLE DEMO")
    print("="*60)
    
    cycle = get_blackhole_whitehole_cycle()
    
    # 테스트 데이터
    test_data = [
        ("에너지는 물리학의 기본 개념이다", "Energy"),
        ("힘은 가속도를 유발한다", "Force"),
        ("엔트로피는 무질서의 측정이다", "Entropy")
    ]
    
    for content, topic in test_data:
        print(f"\n📥 Processing: {topic}")
        result = cycle.process_new_knowledge(content, topic)
        print(f"   Result: {result}")
    
    print("\n" + "="*60)
    print("📊 CYCLE STATUS")
    print("="*60)
    status = cycle.get_status()
    print(f"   {status}")
    
    print("\n" + "="*60)
    print("✅ Demo complete")
    print("="*60)
