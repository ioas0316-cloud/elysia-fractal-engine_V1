# -*- coding: utf-8 -*-
"""
ConceptExtractor - 진짜 개념 추출
===================================

단순 단어 추출이 아닌 진짜 개념의 정의, 속성, 의미를 추출
"""

import re
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import logging

# Optional import
try:
    from Core.Intelligence.Intelligence.korean_mapping import get_korean_name
except ImportError:
    def get_korean_name(name: str) -> str:
        return name  # Fallback: return as-is

logger = logging.getLogger("ConceptExtractor")

@dataclass
class ConceptDefinition:
    """개념 정의"""
    name: str
    kr_name: str = ""  # 한국어 이름
    description: str = ""
    properties: Dict[str, Any] = field(default_factory=dict)
    type: str = "general"  # emotion, action, object, abstract...
    context: str = ""
    
    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'kr_name': self.kr_name,
            'description': self.description,
            'properties': self.properties,
            'type': self.type
        }


class ConceptExtractor:
    """텍스트에서 진짜 개념 추출 (한국어/영어 지원)"""
    
    # 정의 패턴 (영어 + 한국어)
    DEFINITION_PATTERNS = [
        # 영어
        r"(\w+) is (an? )?(.+?)(?:\.|,|;|$)",  # X is Y
        r"(\w+) means (.+?)(?:\.|,|;|$)",      # X means Y
        r"(\w+): (.+?)(?:\.|,|;|$)",           # X: Y
        
        # 한국어 - 정의
        r"(.+?)[은는이가]\s+(.+?)이다",           # X은/는/이/가 Y이다
        r"(.+?)[은는]\s+(.+?)입니다",            # X은/는 Y입니다
        r"(.+?)(?:이)?란\s+(.+?)이다",           # X란 Y이다
        r"(.+?)(?:이)?라는\s+것은\s+(.+)",       # X라는 것은 Y
        r"(.+?)[을를]\s+(.+?)(?:이)?라고\s+한다", # X를 Y라고 한다
    ]
    
    # 속성 패턴 (영어 + 한국어)
    PROPERTY_PATTERNS = [
        # 영어
        r"(\w+) has (.+?)(?:\.|,|;|$)",        # X has Y
        r"(\w+) (?:is|are) (\w+) (?:and|,)",   # X is adj
        
        # 한국어
        r"(.+?)[은는이가]\s+(.+?)(?:하다|있다|없다)",  # X은 Y하다
        r"(.+?)[의]\s+(.+?)[은는이가]",                # X의 Y은
    ]
    
    # 개념 타입 키워드 (영어 + 한국어)
    TYPE_KEYWORDS = {
        'emotion': [
            'feel', 'emotion', 'affection', 'feeling',
            '감정', '느낌', '기분', '사랑', '슬픔', '기쁨', '행복', '화'
        ],
        'action': [
            'do', 'make', 'create', 'move', 'go',
            '하다', '만들다', '가다', '오다', '움직이다'
        ],
        'object': [
            'thing', 'item', 'object',
            '것', '물건', '사물'
        ],
        'abstract': [
            'concept', 'idea', 'principle',
            '개념', '생각', '원리', '철학'
        ],
        'relation': [
            '관계', '사이', '친구', '가족', '아빠', '엄마'
        ],
        'wisdom': [
            '지혜', '명언', '교훈', '진리'
        ],
    }
    
    def __init__(self):
        self.stopwords = {
            # 영어
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at',
            'to', 'for', 'of', 'as', 'by', 'with', 'from', 'is', 'are',
            # 한국어 (조사, 어미)
            '은', '는', '이', '가', '을', '를', '에', '의', '와', '과',
            '도', '만', '요', '야', '아', '어', '고', '지', '게'
        }
    
    def extract_concepts(self, text: str) -> List[ConceptDefinition]:
        """텍스트에서 개념 추출"""
        concepts = []
        
        # 문장 분리
        sentences = re.split(r'[.!?]+', text)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            # 정의 패턴 매칭
            for pattern in self.DEFINITION_PATTERNS:
                matches = re.finditer(pattern, sentence, re.IGNORECASE)
                for match in matches:
                    name = match.group(1).strip()
                    
                    # 불용어 제거
                    if name.lower() in self.stopwords:
                        continue
                    
                    # 정의 추출
                    if len(match.groups()) >= 3:
                        description = match.group(3).strip()
                    else:
                        description = match.group(2).strip() if len(match.groups()) >= 2 else ""
                    
                    # 개념 타입 추론
                    concept_type = self._infer_type(sentence)
                    
                    # 속성 추출
                    properties = self._extract_properties(sentence)
                    
                    concept = ConceptDefinition(
                        name=name,
                        kr_name=get_korean_name(name),  # 한국어 매핑!
                        description=description,
                        properties=properties,
                        type=concept_type,
                        context=sentence
                    )
                    
                    concepts.append(concept)
                    logger.info(f"📝 Concept: {name} = {description[:50]}...")
        
        # 중복 제거 (이름 기준)
        unique_concepts = {}
        for c in concepts:
            if c.name not in unique_concepts:
                unique_concepts[c.name] = c
            else:
                # 정의가 더 길면 업데이트
                if len(c.description) > len(unique_concepts[c.name].description):
                    unique_concepts[c.name] = c
        
        return list(unique_concepts.values())
    
    def _infer_type(self, text: str) -> str:
        """문맥에서 개념 타입 추론"""
        text_lower = text.lower()
        
        for concept_type, keywords in self.TYPE_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return concept_type
        
        return "general"
    
    def _extract_properties(self, text: str) -> Dict[str, Any]:
        """텍스트에서 속성 추출"""
        properties = {}
        
        # 간단한 형용사 추출
        # "X is Y" 형태에서 Y가 형용사면 속성으로
        adjectives = ['positive', 'negative', 'high', 'low', 'intense', 
                     'deep', 'strong', 'weak', 'big', 'small']
        
        for adj in adjectives:
            if adj in text.lower():
                # 문맥에 따라 속성 결정
                if adj in ['positive', 'negative']:
                    properties['valence'] = adj
                elif adj in ['high', 'low', 'intense', 'deep', 'strong', 'weak']:
                    properties['intensity'] = adj
                elif adj in ['big', 'small']:
                    properties['size'] = adj
        
        return properties


# 테스트
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    extractor = ConceptExtractor()
    
    test_text = """
    Love is an intense feeling of deep affection.
    Love creates emotional bonds between people.
    Freedom means the power to act without constraint.
    """
    
    concepts = extractor.extract_concepts(test_text)
    
    print("\n개념 추출 결과:")
    for c in concepts:
        print(f"\n이름: {c.name}")
        print(f"정의: {c.description}")
        print(f"속성: {c.properties}")
        print(f"타입: {c.type}")
