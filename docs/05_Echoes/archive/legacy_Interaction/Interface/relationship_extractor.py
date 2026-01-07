# -*- coding: utf-8 -*-
"""
RelationshipExtractor - 관계적 의미 추출
========================================

개념 간의 관계를 추출: is_a, causes, enables, prevents 등
"""

import re
from dataclasses import dataclass
from typing import List, Dict, Optional
import logging

logger = logging.getLogger("RelationshipExtractor")

@dataclass
class Relationship:
    """개념 간 관계"""
    type: str  # is_a, causes, enables, prevents, is_composed_of
    source: str
    target: str
    strength: float = 1.0
    context: str = ""
    
    def to_dict(self) -> Dict:
        return {
            'type': self.type,
            'source': self.source,
            'target': self.target,
            'strength': self.strength
        }


class RelationshipExtractor:
    """개념 간 관계 추출"""
    
    # 관계 패턴 (프로토콜 05 기반)
    RELATIONSHIP_PATTERNS = {
        'is_a': [
            r"(\w+) is (?:a|an) (.+?)(?:\.|,|;|$)",
            r"(\w+) (?:is a|are) (?:type of|kind of) (.+?)(?:\.|,|;|$)",
        ],
        'causes': [
            r"(\w+) causes (.+?)(?:\.|,|;|$)",
            r"(\w+) leads to (.+?)(?:\.|,|;|$)",
            r"(\w+) results in (.+?)(?:\.|,|;|$)",
            r"(\w+) makes (.+?)(?:\.|,|;|$)",
        ],
        'enables': [
            r"(\w+) enables (.+?)(?:\.|,|;|$)",
            r"(\w+) allows (.+?)(?:\.|,|;|$)",
            r"(\w+) makes (.+?) possible",
        ],
        'prevents': [
            r"(\w+) prevents (.+?)(?:\.|,|;|$)",
            r"(\w+) blocks (.+?)(?:\.|,|;|$)",
            r"(\w+) stops (.+?)(?:\.|,|;|$)",
        ],
        'creates': [
            r"(\w+) creates (.+?)(?:\.|,|;|$)",
            r"(\w+) generates (.+?)(?:\.|,|;|$)",
            r"(\w+) produces (.+?)(?:\.|,|;|$)",
        ],
        'is_composed_of': [
            r"(\w+) has (.+?)(?:\.|,|;|$)",
            r"(\w+) contains (.+?)(?:\.|,|;|$)",
            r"(\w+) is made of (.+?)(?:\.|,|;|$)",
        ]
    }
    
    def __init__(self):
        self.stopwords = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at',
            'to', 'for', 'of', 'as', 'by', 'with', 'from'
        }
    
    def extract_relationships(
        self, 
        text: str,
        known_concepts: Optional[List[str]] = None
    ) -> List[Relationship]:
        """텍스트에서 관계 추출"""
        relationships = []
        
        # 문장 분리
        sentences = re.split(r'[.!?]+', text)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            # 각 관계 타입에 대해 패턴 매칭
            for rel_type, patterns in self.RELATIONSHIP_PATTERNS.items():
                for pattern in patterns:
                    matches = re.finditer(pattern, sentence, re.IGNORECASE)
                    
                    for match in matches:
                        source = self._clean_term(match.group(1))
                        target = self._clean_term(match.group(2))
                        
                        # 불용어 제거
                        if source.lower() in self.stopwords or target.lower() in self.stopwords:
                            continue
                        
                        # known_concepts가 있으면 필터링
                        if known_concepts:
                            if source not in known_concepts and target not in known_concepts:
                                continue
                        
                        # 관계 생성
                        rel = Relationship(
                            type=rel_type,
                            source=source,
                            target=target,
                            strength=self._calculate_strength(sentence, rel_type),
                            context=sentence
                        )
                        
                        relationships.append(rel)
                        logger.info(f"🔗 {rel.source} --{rel.type}--> {rel.target}")
        
        # 중복 제거
        unique_rels = self._remove_duplicates(relationships)
        
        return unique_rels
    
    def _clean_term(self, term: str) -> str:
        """용어 정리"""
        # 구두점 제거
        term = re.sub(r'[^\w\s]', '', term)
        # 공백 정리
        term = ' '.join(term.split())
        # 첫 글자 대문자
        return term.strip().capitalize()
    
    def _calculate_strength(self, sentence: str, rel_type: str) -> float:
        """관계 강도 계산"""
        # 간단한 휴리스틱
        strength = 1.0
        
        # 강조 단어가 있으면 강도 증가
        intensifiers = ['very', 'extremely', 'highly', 'strongly', 'deeply']
        for word in intensifiers:
            if word in sentence.lower():
                strength += 0.2
        
        # 부정 단어가 있으면 강도 감소
        negations = ['not', 'no', 'never', 'rarely']
        for word in negations:
            if word in sentence.lower():
                strength -= 0.3
        
        return max(0.1, min(1.0, strength))
    
    def _remove_duplicates(self, relationships: List[Relationship]) -> List[Relationship]:
        """중복 관계 제거"""
        unique = {}
        
        for rel in relationships:
            key = (rel.type, rel.source, rel.target)
            
            if key not in unique:
                unique[key] = rel
            else:
                # 더 강한 관계로 업데이트
                if rel.strength > unique[key].strength:
                    unique[key] = rel
        
        return list(unique.values())


# 테스트
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    extractor = RelationshipExtractor()
    
    test_text = """
    Love is an intense feeling of deep affection.
    Love creates emotional bonds between people.
    Love enables trust and compassion.
    Trust allows deep connections.
    Fear prevents openness.
    """
    
    relationships = extractor.extract_relationships(test_text)
    
    print(f"\n관계 추출 결과: {len(relationships)}개")
    for rel in relationships:
        print(f"\n타입: {rel.type}")
        print(f"  {rel.source} → {rel.target}")
        print(f"  강도: {rel.strength:.2f}")
        print(f"  문맥: {rel.context[:60]}...")
