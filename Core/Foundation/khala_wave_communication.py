"""
Khala Wave Communication - 칼라 파동 의사소통
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"어차피 언어는 파동이야. 모든 의사소통을 파동으로 하게 하고 
 그 파동이 어떤 의미인지를 찾아내서 언어를 명명하는거지"

젤나가 프로토콜 - 칼라 네트워크:
프로토스가 텔레파시로 직접 연결되듯이, 영혼들은 파동으로 직접 소통한다.
단어가 먼저가 아니라, 파동이 먼저다.
나중에 그 파동 패턴에 이름을 붙인다.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

핵심 철학:
1. 모든 의사소통은 파동이다 (언어 이전)
2. 파동은 감정, 의도, 상태를 직접 전달한다
3. 반복되는 파동 패턴에 나중에 이름을 붙인다
4. 언어는 파동의 '관찰/기록'이다 (본질이 아님)

"""

from __future__ import annotations

import math
import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from collections import defaultdict
import random
import time as py_time

# ============================================================================
# 상수
# ============================================================================

# 파동 특성
WAVE_DIMENSIONS = 8  # 파동의 차원 (감정, 의도, 강도 등)
RESONANCE_THRESHOLD = 0.6  # 두 파동이 '이해'되었다고 판단하는 임계값
PATTERN_MEMORY_SIZE = 100  # 기억할 수 있는 최대 파동 패턴 수
NAMING_THRESHOLD = 5  # 몇 번 반복되어야 이름을 붙이는가


@dataclass
class KhalaWave:
    """
    칼라 파동 - 순수한 의사소통의 단위
    
    이것은 '단어'가 아니다. 이것은 직접적인 감정/의도/상태의 전달이다.
    마치 프로토스의 칼라처럼, 생각과 감정이 직접 전달된다.
    
    8차원 벡터로 표현:
    - dim 0: 감정 극성 (긍정/부정)
    - dim 1: 각성 수준 (차분/흥분)
    - dim 2: 사회적 의도 (회피/접근)
    - dim 3: 정보 내용 (간단/복잡)
    - dim 4: 시간 지향 (과거/미래)
    - dim 5: 자아 관련 (타인/자신)
    - dim 6: 확실성 (불확실/확실)
    - dim 7: 강도 (약함/강함)
    """
    vector: np.ndarray  # 8차원 파동 벡터
    timestamp: float = 0.0
    sender_id: str = ""
    
    def __post_init__(self):
        if self.vector is None:
            self.vector = np.zeros(WAVE_DIMENSIONS)
        elif len(self.vector) != WAVE_DIMENSIONS:
            # 차원 맞추기
            new_vec = np.zeros(WAVE_DIMENSIONS)
            new_vec[:min(len(self.vector), WAVE_DIMENSIONS)] = self.vector[:WAVE_DIMENSIONS]
            self.vector = new_vec
    
    def resonance_with(self, other: 'KhalaWave') -> float:
        """
        두 파동의 공명도 (0~1)
        
        완전히 같은 파동 = 1.0 (완벽한 이해)
        완전히 반대 파동 = 0.0 (전혀 이해 못함)
        """
        # 코사인 유사도
        dot = np.dot(self.vector, other.vector)
        norm_self = np.linalg.norm(self.vector)
        norm_other = np.linalg.norm(other.vector)
        
        if norm_self < 1e-8 or norm_other < 1e-8:
            return 0.0
        
        similarity = dot / (norm_self * norm_other)
        # -1~1을 0~1로 변환
        return (similarity + 1.0) / 2.0
    
    def blend_with(self, other: 'KhalaWave', ratio: float = 0.5) -> 'KhalaWave':
        """두 파동의 혼합 (대화 중 감정 교류)"""
        blended = self.vector * (1 - ratio) + other.vector * ratio
        return KhalaWave(vector=blended, timestamp=max(self.timestamp, other.timestamp))
    
    def signature(self) -> Tuple[int, ...]:
        """파동의 서명 (유사 패턴 찾기용) - 각 차원을 3단계로 양자화"""
        quantized = np.round(self.vector * 2) / 2  # -1, -0.5, 0, 0.5, 1
        return tuple(quantized.tolist())


@dataclass  
class WavePattern:
    """
    파동 패턴 - 반복되는 파동의 원형
    
    이것이 나중에 '단어'가 된다.
    처음에는 이름이 없다. 반복되면 이름을 붙인다.
    """
    centroid: np.ndarray  # 패턴의 중심 벡터
    occurrence_count: int = 0  # 발생 횟수
    first_seen: float = 0.0  # 처음 관찰된 시간
    last_seen: float = 0.0  # 마지막 관찰된 시간
    
    # 이름 (반복되면 붙음)
    name: Optional[str] = None
    
    # 이 패턴을 가장 많이 사용한 영혼들
    frequent_users: Dict[str, int] = field(default_factory=dict)
    
    # 상황 정보 (어떤 상황에서 발생했는가)
    contexts: List[str] = field(default_factory=list)
    
    def similarity(self, wave: KhalaWave) -> float:
        """파동과 이 패턴의 유사도"""
        dot = np.dot(self.centroid, wave.vector)
        norm_c = np.linalg.norm(self.centroid)
        norm_w = np.linalg.norm(wave.vector)
        
        if norm_c < 1e-8 or norm_w < 1e-8:
            return 0.0
        
        sim = dot / (norm_c * norm_w)
        return (sim + 1.0) / 2.0
    
    def update(self, wave: KhalaWave, context: str = ""):
        """새 파동으로 패턴 업데이트"""
        # 이동 평균으로 중심 업데이트
        alpha = 1.0 / (self.occurrence_count + 1)
        self.centroid = (1 - alpha) * self.centroid + alpha * wave.vector
        
        self.occurrence_count += 1
        self.last_seen = wave.timestamp
        
        if wave.sender_id:
            self.frequent_users[wave.sender_id] = self.frequent_users.get(wave.sender_id, 0) + 1
        
        if context and len(self.contexts) < 20:
            self.contexts.append(context)


@dataclass
class KhalaSoul:
    """
    칼라 영혼 - 파동으로 소통하는 존재
    
    이 영혼은 언어를 '쓰지 않는다'.
    직접 파동을 보내고 받는다.
    마치 프로토스처럼.
    """
    id: str
    
    # 현재 내면 상태 (8차원 파동)
    inner_state: np.ndarray = field(default_factory=lambda: np.random.randn(WAVE_DIMENSIONS) * 0.3)
    
    # 기억된 파동 패턴들 (나중에 '어휘'가 됨)
    known_patterns: List[WavePattern] = field(default_factory=list)
    
    # 다른 영혼들과의 연결 강도
    connections: Dict[str, float] = field(default_factory=dict)
    
    # 통계
    waves_sent: int = 0
    waves_received: int = 0
    successful_communications: int = 0
    
    def generate_wave(self, intent: str = "") -> KhalaWave:
        """
        파동 생성 - 현재 상태와 의도를 파동으로 변환
        
        언어가 아니다. 직접적인 감정/의도의 표현이다.
        """
        # 기본은 현재 내면 상태
        wave_vec = self.inner_state.copy()
        
        # 의도에 따라 변조
        if intent == "greeting":
            wave_vec[0] += 0.5   # 긍정
            wave_vec[2] += 0.5   # 접근
            wave_vec[7] += 0.3   # 중간 강도
        elif intent == "question":
            wave_vec[6] -= 0.5   # 불확실
            wave_vec[3] += 0.3   # 정보 요청
        elif intent == "joy":
            wave_vec[0] += 0.8   # 긍정
            wave_vec[1] += 0.6   # 흥분
            wave_vec[7] += 0.5   # 강함
        elif intent == "sadness":
            wave_vec[0] -= 0.6   # 부정
            wave_vec[1] -= 0.4   # 차분
            wave_vec[7] += 0.4   # 강함
        elif intent == "fear":
            wave_vec[0] -= 0.4   # 부정
            wave_vec[1] += 0.7   # 흥분
            wave_vec[2] -= 0.6   # 회피
        elif intent == "love":
            wave_vec[0] += 0.9   # 매우 긍정
            wave_vec[2] += 0.8   # 접근
            wave_vec[5] -= 0.3   # 타인 지향
            wave_vec[7] += 0.7   # 강함
        elif intent == "curiosity":
            wave_vec[3] += 0.5   # 정보
            wave_vec[4] += 0.3   # 미래 지향
            wave_vec[6] -= 0.3   # 불확실
        elif intent == "anger":
            wave_vec[0] -= 0.7   # 부정
            wave_vec[1] += 0.8   # 흥분
            wave_vec[7] += 0.9   # 매우 강함
        else:
            # 랜덤 변동
            wave_vec += np.random.randn(WAVE_DIMENSIONS) * 0.2
        
        # 정규화 (-1 ~ 1)
        wave_vec = np.clip(wave_vec, -1.0, 1.0)
        
        wave = KhalaWave(
            vector=wave_vec,
            timestamp=py_time.time(),
            sender_id=self.id
        )
        
        self.waves_sent += 1
        return wave
    
    def receive_wave(self, wave: KhalaWave, context: str = "") -> float:
        """
        파동 수신 - 상대의 파동을 '이해'한다
        
        Returns:
            이해도 (0~1)
        """
        self.waves_received += 1
        
        # 현재 내 상태와의 공명
        my_wave = KhalaWave(vector=self.inner_state.copy())
        resonance = my_wave.resonance_with(wave)
        
        # 내 상태도 영향 받음 (감정 전이)
        influence = 0.1 * resonance  # 이해할수록 더 영향 받음
        self.inner_state = (1 - influence) * self.inner_state + influence * wave.vector
        
        # 연결 강도 업데이트
        if wave.sender_id:
            old_conn = self.connections.get(wave.sender_id, 0.0)
            self.connections[wave.sender_id] = old_conn + resonance * 0.1
        
        # 이해했으면 성공
        if resonance > RESONANCE_THRESHOLD:
            self.successful_communications += 1
        
        # 패턴 기억
        self._remember_pattern(wave, context)
        
        return resonance
    
    def _remember_pattern(self, wave: KhalaWave, context: str = ""):
        """파동 패턴을 기억"""
        # 비슷한 패턴이 있는지 찾기
        best_match = None
        best_sim = 0.0
        
        for pattern in self.known_patterns:
            sim = pattern.similarity(wave)
            if sim > best_sim:
                best_sim = sim
                best_match = pattern
        
        if best_match and best_sim > 0.7:
            # 기존 패턴 업데이트
            best_match.update(wave, context)
            
            # 충분히 반복되면 이름 붙이기
            if best_match.occurrence_count >= NAMING_THRESHOLD and best_match.name is None:
                best_match.name = self._generate_name(best_match)
        else:
            # 새 패턴 등록
            if len(self.known_patterns) < PATTERN_MEMORY_SIZE:
                new_pattern = WavePattern(
                    centroid=wave.vector.copy(),
                    occurrence_count=1,
                    first_seen=wave.timestamp,
                    last_seen=wave.timestamp
                )
                if wave.sender_id:
                    new_pattern.frequent_users[wave.sender_id] = 1
                if context:
                    new_pattern.contexts.append(context)
                self.known_patterns.append(new_pattern)
    
    def _generate_name(self, pattern: WavePattern) -> str:
        """
        패턴에 이름 붙이기
        
        파동의 특성에서 자연스럽게 이름이 생성된다.
        이것이 '언어'의 탄생이다.
        """
        vec = pattern.centroid
        
        # 각 차원의 특성에서 음소 생성
        # dim 0 (감정): 긍정=밝은 모음, 부정=어두운 모음
        if vec[0] > 0.3:
            vowel1 = random.choice(['a', 'e', 'i'])
        elif vec[0] < -0.3:
            vowel1 = random.choice(['o', 'u'])
        else:
            vowel1 = random.choice(['a', 'e', 'i', 'o', 'u'])
        
        # dim 1 (각성): 흥분=거센소리, 차분=부드러운소리
        if vec[1] > 0.3:
            consonant1 = random.choice(['k', 't', 'p', 'ch'])
        elif vec[1] < -0.3:
            consonant1 = random.choice(['m', 'n', 'l', 'r'])
        else:
            consonant1 = random.choice(['s', 'h', 'w', 'y'])
        
        # dim 2 (사회적): 접근=열린소리, 회피=닫힌소리
        if vec[2] > 0.3:
            vowel2 = random.choice(['a', 'o'])
        else:
            vowel2 = random.choice(['i', 'u'])
        
        # dim 7 (강도): 강함=긴 이름, 약함=짧은 이름
        if vec[7] > 0.5:
            consonant2 = random.choice(['k', 't', 'n', 'm'])
            name = f"{consonant1}{vowel1}{consonant2}{vowel2}"
        elif vec[7] > 0:
            name = f"{consonant1}{vowel1}{vowel2}"
        else:
            name = f"{consonant1}{vowel1}"
        
        return name
    
    def get_vocabulary(self) -> Dict[str, WavePattern]:
        """명명된 패턴들 (어휘)"""
        return {p.name: p for p in self.known_patterns if p.name is not None}
    
    def describe_wave(self, wave: KhalaWave) -> str:
        """파동을 설명 (명명된 패턴이 있으면 그 이름 사용)"""
        for pattern in self.known_patterns:
            if pattern.name and pattern.similarity(wave) > 0.7:
                return pattern.name
        
        # 이름 없으면 파동 특성 설명
        vec = wave.vector
        parts = []
        if vec[0] > 0.3:
            parts.append("positive")
        elif vec[0] < -0.3:
            parts.append("negative")
        if vec[1] > 0.3:
            parts.append("excited")
        elif vec[1] < -0.3:
            parts.append("calm")
        if vec[7] > 0.5:
            parts.append("strong")
        
        return "+".join(parts) if parts else "neutral"


class KhalaNetwork:
    """
    칼라 네트워크 - 파동으로 연결된 영혼들의 집합체
    
    모든 소통은 파동이다.
    언어는 나중에 발견된다.
    """
    
    def __init__(self, n_souls: int = 100):
        self.souls: Dict[str, KhalaSoul] = {}
        self.time = 0.0
        
        # 네트워크 전체에서 발견된 공유 패턴들
        self.shared_patterns: List[WavePattern] = []
        
        # 통계
        self.total_communications = 0
        self.successful_understandings = 0
        
        # 상황/맥락 목록 (경험을 풍요롭게)
        self.contexts = [
            "meeting", "parting", "eating", "danger", "safety",
            "sunrise", "sunset", "rain", "storm", "peace",
            "conflict", "cooperation", "discovery", "loss", "gain",
            "birth", "death", "celebration", "mourning", "play",
            "work", "rest", "dream", "nightmare", "love",
            "rejection", "acceptance", "confusion", "clarity", "wonder"
        ]
        
        # 영혼 생성
        for i in range(n_souls):
            soul_id = f"soul_{i}"
            self.souls[soul_id] = KhalaSoul(id=soul_id)
    
    def step(self):
        """한 틱 진행"""
        self.time += 1
        
        soul_list = list(self.souls.values())
        n = len(soul_list)
        
        # 랜덤 소통 (n/2 쌍)
        n_communications = max(1, n // 2)
        
        for _ in range(n_communications):
            # 두 영혼 선택
            idx1, idx2 = random.sample(range(n), 2)
            soul1 = soul_list[idx1]
            soul2 = soul_list[idx2]
            
            # 상황 선택
            context = random.choice(self.contexts)
            
            # 의도 선택
            intents = ["greeting", "question", "joy", "sadness", 
                      "fear", "love", "curiosity", "anger", ""]
            intent = random.choice(intents)
            
            # 파동 교환
            wave1 = soul1.generate_wave(intent)
            wave2 = soul2.generate_wave(random.choice(intents))
            
            # 서로의 파동 수신
            res1 = soul1.receive_wave(wave2, context)
            res2 = soul2.receive_wave(wave1, context)
            
            self.total_communications += 2
            
            if res1 > RESONANCE_THRESHOLD:
                self.successful_understandings += 1
            if res2 > RESONANCE_THRESHOLD:
                self.successful_understandings += 1
        
        # 내면 상태 변동 (일상의 변화)
        for soul in soul_list:
            soul.inner_state += np.random.randn(WAVE_DIMENSIONS) * 0.05
            soul.inner_state = np.clip(soul.inner_state, -1.0, 1.0)
    
    def run_simulation(self, ticks: int = 1000, report_interval: int = 100) -> Dict[str, Any]:
        """시뮬레이션 실행"""
        start_time = py_time.time()
        
        for tick in range(ticks):
            self.step()
            
            if tick > 0 and tick % report_interval == 0:
                # 어휘 통계
                vocab_sizes = [len(s.get_vocabulary()) for s in self.souls.values()]
                avg_vocab = sum(vocab_sizes) / len(vocab_sizes) if vocab_sizes else 0
                
                print(f"Tick {tick}: avg_vocabulary={avg_vocab:.1f}, "
                      f"communications={self.total_communications}, "
                      f"understanding_rate={self.successful_understandings/max(1,self.total_communications)*100:.1f}%")
        
        elapsed = py_time.time() - start_time
        
        # 공유 어휘 분석
        all_patterns = defaultdict(list)
        for soul in self.souls.values():
            for pattern in soul.known_patterns:
                if pattern.name:
                    sig = pattern.centroid.round(1).tobytes()
                    all_patterns[sig].append((soul.id, pattern.name, pattern))
        
        # 여러 영혼이 비슷한 파동에 같은 이름을 붙인 경우 = 공유 언어
        shared_language = {}
        for sig, entries in all_patterns.items():
            if len(entries) > 1:
                # 가장 많이 사용된 이름
                names = [e[1] for e in entries]
                most_common = max(set(names), key=names.count)
                shared_language[most_common] = len(entries)
        
        # 결과 수집
        vocab_sizes = [len(s.get_vocabulary()) for s in self.souls.values()]
        
        return {
            "ticks_simulated": ticks,
            "elapsed_seconds": elapsed,
            "speed_ticks_per_second": ticks / elapsed if elapsed > 0 else 0,
            "total_souls": len(self.souls),
            "total_communications": self.total_communications,
            "successful_understandings": self.successful_understandings,
            "understanding_rate": self.successful_understandings / max(1, self.total_communications),
            "avg_vocabulary_size": sum(vocab_sizes) / len(vocab_sizes) if vocab_sizes else 0,
            "max_vocabulary_size": max(vocab_sizes) if vocab_sizes else 0,
            "shared_language_words": len(shared_language),
            "top_shared_words": sorted(shared_language.items(), key=lambda x: -x[1])[:10],
        }


def demo():
    """데모"""
    print("=" * 70)
    print("Khala Wave Communication - 칼라 파동 의사소통")
    print("=" * 70)
    print()
    print("\"모든 의사소통을 파동으로 하게 하고")
    print(" 그 파동이 어떤 의미인지를 찾아내서 언어를 명명하는거지\"")
    print()
    
    network = KhalaNetwork(n_souls=50)
    results = network.run_simulation(ticks=500, report_interval=100)
    
    print()
    print("=" * 70)
    print("결과")
    print("=" * 70)
    for key, value in results.items():
        if 'top_shared' not in str(key):
            print(f"  {key}: {value}")
    
    print()
    print("=" * 70)
    print("창발된 언어 (공유된 파동 패턴의 이름들)")
    print("=" * 70)
    if results.get('top_shared_words'):
        for word, count in results['top_shared_words']:
            print(f"  \"{word}\" - {count}명이 공유")
    
    # 샘플 영혼의 어휘
    print()
    print("=" * 70)
    print("샘플 영혼의 어휘 (파동 → 이름)")
    print("=" * 70)
    for soul_id, soul in list(network.souls.items())[:3]:
        vocab = soul.get_vocabulary()
        print(f"\n[{soul_id}] {len(vocab)}개 단어:")
        for name, pattern in list(vocab.items())[:5]:
            vec = pattern.centroid
            mood = "긍정" if vec[0] > 0.3 else ("부정" if vec[0] < -0.3 else "중립")
            energy = "흥분" if vec[1] > 0.3 else ("차분" if vec[1] < -0.3 else "보통")
            print(f"  \"{name}\" - {mood}, {energy}, {pattern.occurrence_count}회 관찰")


if __name__ == "__main__":
    demo()
