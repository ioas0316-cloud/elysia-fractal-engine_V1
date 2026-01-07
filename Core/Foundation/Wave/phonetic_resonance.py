"""
Phonetic Resonance Layer
========================

"의미와 느낌으로 검색한다"

이 모듈은 텍스트를 단순한 유니코드 숫자가 아닌,
'물리적 파동(Vector)'으로 변환하여 유사도(공명)를 계산합니다.

활용:
- Rhyme 찾기 (사랑 ↔ 사람)
- 느낌 검색 (거친 단어 찾기)
- 의미적 연상 

[NEW 2025-12-16] Hybrid Architecture Layer 2
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Tuple
from Core.Foundation.hangul_physics import HangulPhysicsEngine, Tensor3D

@dataclass
class ResonanceField:
    """텍스트의 물리적 파동장"""
    text: str
    vectors: List[Tensor3D]
    average_roughness: float
    average_tension: float
    
    def vector_matrix(self) -> np.ndarray:
        """(N, 3) 행렬 반환"""
        return np.array([[v.x, v.y, v.z] for v in self.vectors])

class PhoneticResonanceEngine:
    def __init__(self):
        self.physics = HangulPhysicsEngine()
        
    def text_to_field(self, text: str) -> ResonanceField:
        """텍스트 → 파동장 변환"""
        vectors = [self.physics.get_phonetic_vector(char) for char in text]
        
        # 통계 계산
        if not vectors:
            return ResonanceField(text, [], 0.0, 0.0)
            
        avg_rough = sum(v.roughness() for v in vectors) / len(vectors)
        # Tension is mapped to Z in get_phonetic_vector
        avg_tens = sum(v.z for v in vectors) / len(vectors)
        
        return ResonanceField(
            text=text,
            vectors=vectors,
            average_roughness=avg_rough,
            average_tension=avg_tens
        )

    def calculate_resonance(self, text1: str, text2: str) -> float:
        """
        두 텍스트 간의 물리적 공명(유사도) 계산
        0.0 ~ 1.0
        """
        field1 = self.text_to_field(text1)
        field2 = self.text_to_field(text2)
        
        # 1. 길이 차이 페널티
        len1, len2 = len(field1.vectors), len(field2.vectors)
        if len1 == 0 or len2 == 0: return 0.0
        
        min_len = min(len1, len2)
        
        # 2. 벡터 코사인 유사도 (각 글자별)
        similarities = []
        for i in range(min_len):
            v1 = field1.vectors[i]
            v2 = field2.vectors[i]
            
            # Dot product
            dot = (v1.x * v2.x) + (v1.y * v2.y) + (v1.z * v2.z)
            mag1 = v1.magnitude()
            mag2 = v2.magnitude()
            
            if mag1 == 0 or mag2 == 0:
                sim = 1.0 if mag1 == mag2 else 0.0
            else:
                sim = dot / (mag1 * mag2)
            
            similarities.append(sim)
            
        # 3. 전체 평균 공명
        base_resonance = sum(similarities) / min_len
        
        # 4. 느낌(Roughness/Tension) 유사도 보정
        feel_diff = abs(field1.average_roughness - field2.average_roughness) + \
                    abs(field1.average_tension - field2.average_tension)
                    
        feel_factor = 1.0 / (1.0 + feel_diff) # 차이가 클수록 작아짐
        
        return (base_resonance * 0.7) + (feel_factor * 0.3)

    def find_rhymes(self, target_word: str, candidates: List[str], top_k: int = 5) -> List[Tuple[str, float]]:
        """라임(비슷한 소리) 찾기"""
        scores = []
        for word in candidates:
            score = self.calculate_resonance(target_word, word)
            scores.append((word, score))
            
        return sorted(scores, key=lambda x: x[1], reverse=True)[:top_k]

# Singleton
_engine = None
def get_resonance_engine():
    global _engine
    if _engine is None:
        _engine = PhoneticResonanceEngine()
    return _engine
