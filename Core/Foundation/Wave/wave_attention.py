"""
Wave Attention (파동 어텐션)
============================

공명 기반 어텐션 시스템 - Softmax 대신 파동 간섭 사용

핵심 원리:
- Query = 질문하는 파동
- Keys = 기억된 파동들
- Attention Weight = 공명 강도 (간섭 진폭)

Usage:
    from Core.Foundation.Wave.wave_attention import WaveAttention
    
    attn = WaveAttention()
    weights = attn.attend(query_wave, key_waves)
"""

import logging
import numpy as np
from typing import List, Tuple, Optional
from dataclasses import dataclass

logger = logging.getLogger("WaveAttention")

# 내부 파동 시스템 임포트
try:
    from Core.Foundation.Wave.wave_tensor import WaveTensor
    WAVE_AVAILABLE = True
except ImportError:
    WAVE_AVAILABLE = False
    
try:
    from Core.Foundation.tiny_brain import get_tiny_brain
    EMBEDDING_AVAILABLE = True
except ImportError:
    EMBEDDING_AVAILABLE = False


@dataclass
class AttentionResult:
    """어텐션 결과"""
    weights: List[float]           # 각 키에 대한 가중치
    focused_indices: List[int]     # 집중된 인덱스들
    total_resonance: float         # 전체 공명 강도
    dominant_frequency: float      # 지배적 주파수


class WaveAttention:
    """
    파동 기반 어텐션 시스템
    
    Transformer Attention vs Wave Attention:
    - Transformer: attention = softmax(QK^T / sqrt(d))
    - Wave: attention = resonance(query_wave, key_waves)
    
    장점:
    - 위상(Phase) 정보 보존
    - 자연스러운 정규화 (진폭 기반)
    - 연속적이고 부드러운 집중
    """
    
    def __init__(self, threshold: float = 0.1):
        """
        Args:
            threshold: 최소 공명 임계값 (이 이하는 무시)
        """
        self.threshold = threshold
        self.brain = get_tiny_brain() if EMBEDDING_AVAILABLE else None
        
        logger.info("🌊 WaveAttention initialized")
    
    def text_to_wave(self, text: str) -> Optional[dict]:
        """
        텍스트 → 파동 변환
        
        임베딩 벡터를 파동 속성으로 변환합니다.
        """
        if not self.brain:
            return None
        
        # 임베딩 획득
        embedding = self.brain.get_embedding(text)
        if not embedding or len(embedding) == 0:
            return None
        
        embedding = np.array(embedding)
        
        # 파동 속성 추출
        # Frequency: 임베딩의 에너지 (L2 norm)
        energy = np.linalg.norm(embedding)
        frequency = 200 + (energy * 50)  # 200~700 Hz
        
        # Amplitude: 임베딩의 분산 (명확성)
        amplitude = min(1.0, np.var(embedding) * 10)
        
        # Phase: 주성분 방향
        phase = np.arctan2(embedding[0], embedding[1]) if len(embedding) > 1 else 0.0
        
        # 딕셔너리로 반환 (WaveTensor와 호환 가능)
        return {
            "frequency": frequency, 
            "amplitude": amplitude, 
            "phase": phase, 
            "embedding": embedding
        }
    
    def calculate_resonance(self, wave1, wave2) -> float:
        """
        두 파동 간의 공명도 계산
        
        공명 = 주파수 유사도 × 위상 일치도 × 진폭 곱
        """
        if wave1 is None or wave2 is None:
            return 0.0
        
        # WaveTensor인 경우
        if WAVE_AVAILABLE and hasattr(wave1, 'frequency'):
            freq_sim = 1.0 / (1.0 + abs(wave1.frequency - wave2.frequency) / 100)
            phase_sim = (1 + np.cos(wave1.phase - wave2.phase)) / 2
            amp_product = wave1.amplitude * wave2.amplitude
            return freq_sim * phase_sim * amp_product
        
        # 딕셔너리인 경우
        if isinstance(wave1, dict) and isinstance(wave2, dict):
            freq_sim = 1.0 / (1.0 + abs(wave1["frequency"] - wave2["frequency"]) / 100)
            phase_sim = (1 + np.cos(wave1["phase"] - wave2["phase"])) / 2
            amp_product = wave1["amplitude"] * wave2["amplitude"]
            
            # 임베딩 코사인 유사도 추가 (있으면)
            if "embedding" in wave1 and "embedding" in wave2:
                emb1 = wave1["embedding"]
                emb2 = wave2["embedding"]
                cos_sim = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2) + 1e-8)
                return freq_sim * phase_sim * amp_product * (0.5 + 0.5 * cos_sim)
            
            return freq_sim * phase_sim * amp_product
        
        return 0.0
    
    def attend(self, query_wave, key_waves: List) -> AttentionResult:
        """
        파동 어텐션 수행
        
        Args:
            query_wave: 질문 파동
            key_waves: 키 파동들의 리스트
            
        Returns:
            AttentionResult: 어텐션 가중치 및 집중 정보
        """
        if not key_waves:
            return AttentionResult(weights=[], focused_indices=[], total_resonance=0.0, dominant_frequency=0.0)
        
        # 각 키와의 공명 계산
        resonances = [self.calculate_resonance(query_wave, k) for k in key_waves]
        
        # 총 공명
        total = sum(resonances) + 1e-8
        
        # 가중치 정규화 (자연스러운 softmax 대체)
        weights = [r / total for r in resonances]
        
        # 임계값 이상인 것만 집중
        focused = [i for i, w in enumerate(weights) if w > self.threshold]
        
        # 지배 주파수 (가장 강한 공명의 주파수)
        if resonances:
            max_idx = resonances.index(max(resonances))
            if hasattr(key_waves[max_idx], 'frequency'):
                dominant_freq = key_waves[max_idx].frequency
            elif isinstance(key_waves[max_idx], dict):
                dominant_freq = key_waves[max_idx].get("frequency", 0)
            else:
                dominant_freq = 0
        else:
            dominant_freq = 0
        
        return AttentionResult(
            weights=weights,
            focused_indices=focused,
            total_resonance=total,
            dominant_frequency=dominant_freq
        )
    
    def attend_text(self, query: str, keys: List[str]) -> AttentionResult:
        """
        텍스트 기반 어텐션 (편의 메서드)
        
        Args:
            query: 질문 텍스트
            keys: 키 텍스트들
            
        Returns:
            AttentionResult
        """
        query_wave = self.text_to_wave(query)
        key_waves = [self.text_to_wave(k) for k in keys]
        
        return self.attend(query_wave, key_waves)
    
    def focus_topk(self, query: str, keys: List[str], k: int = 3) -> List[Tuple[str, float]]:
        """
        상위 K개에 집중
        
        Args:
            query: 질문
            keys: 후보들
            k: 선택할 개수
            
        Returns:
            [(key, weight), ...] 상위 K개
        """
        result = self.attend_text(query, keys)
        
        # 가중치와 키 쌍으로 정렬
        pairs = list(zip(keys, result.weights))
        pairs.sort(key=lambda x: x[1], reverse=True)
        
        return pairs[:k]


# 싱글톤
_attention = None

def get_wave_attention() -> WaveAttention:
    global _attention
    if _attention is None:
        _attention = WaveAttention()
    return _attention


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    print("🌊 WAVE ATTENTION TEST")
    print("=" * 50)
    
    attn = get_wave_attention()
    
    # 테스트
    query = "사랑이란 무엇인가?"
    keys = ["기쁨", "슬픔", "연결", "고독", "희망"]
    
    print(f"\n질문: {query}")
    print(f"후보: {keys}")
    
    top3 = attn.focus_topk(query, keys, k=3)
    
    print("\n🎯 집중 결과:")
    for key, weight in top3:
        bar = "█" * int(weight * 20)
        print(f"   {key}: {weight:.3f} {bar}")
    
    print("\n✅ Wave Attention works!")
