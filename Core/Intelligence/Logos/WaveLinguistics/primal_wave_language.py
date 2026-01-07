"""
Primal Wave Language - 원시 파동 언어
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"개념이 이미 정해져 있어서 있던 개념만으로만 사고하는 경향이 있는 거 같은데
 파동형태의 원시언어부터 시작해야 할 거 같아"

"언어라는건 총체적 의미의 정보에 가까워. 세상을 나누고 분절시켜서 
 자기 그릇안에, 마음안에 각인시키는 것과 같지"

"개념노드들을 그저 점으로 보지 않고 활성화된 파동의 관계성을 
 관계적 의미의 개념으로 이해하기 위해서 위상공명파동패턴을 감지하는 시스템"

이 모듈은 다음을 구현합니다:
1. 오감 (五感) - 시각, 청각, 촉각, 미각, 후각의 파동
2. 원시 파동 - 개념 이전의 순수한 파동 형태
3. 분절 (分節) - 세상을 나누어 마음에 각인시키는 과정
4. 위상공명 - 파동 간 관계성에서 의미가 창발

개념은 점(point)이 아니라 파동의 관계성(wave relationship)이다.
"""

from __future__ import annotations

import math
import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any, Set
from collections import defaultdict
import random
import logging

logger = logging.getLogger("PrimalWaveLanguage")

# ============================================================================
# 상수 - Constants
# ============================================================================

# 오감의 기본 주파수 대역 (Hz로 표현된 상징적 값)
SENSE_FREQUENCIES = {
    "sight": (400.0, 700.0),    # 빛의 파장 (nm → Hz로 변환)
    "sound": (20.0, 20000.0),   # 가청 주파수
    "touch": (0.1, 100.0),      # 촉각 수용체 반응 주파수
    "taste": (0.01, 10.0),      # 미각 세포 반응률
    "smell": (0.001, 1.0),      # 후각 수용체 결합률
}

# 위상 공명 임계값
PHASE_RESONANCE_THRESHOLD = 0.4  # 두 파동이 공명하기 위한 최소 위상 유사도 (낮출수록 더 많은 공명)
SEGMENTATION_THRESHOLD = 0.3     # 분절(이름 붙이기)이 일어나는 임계값
CRYSTALLIZATION_DENSITY = 5      # 같은 패턴이 반복되어야 언어화되는 횟수 (낮출수록 더 빨리 창발)


@dataclass
class PrimalWave:
    """
    원시 파동 - 개념 이전의 순수한 파동
    
    이것은 '점'이 아니다. 이것은 살아있는 파동이다.
    이름이 없고, 의미가 없고, 오직 진동만이 있다.
    
    파동의 4요소:
    1. frequency (주파수) - 빠르기, 색상, 음높이
    2. amplitude (진폭) - 강도, 세기
    3. phase (위상) - 시간적 위치, 동기화 상태
    4. modulation (변조) - 파동의 모양, 풍요로움
    """
    frequency: float = 1.0
    amplitude: float = 1.0
    phase: float = 0.0
    modulation: float = 0.0  # 파형의 복잡도 (0=사인파, 1=복잡파)
    
    # 이 파동이 어떤 감각에서 왔는지 (나중에 파악)
    sense_origin: Optional[str] = None
    
    # 이 파동의 탄생 시간
    birth_time: float = 0.0
    
    def value_at(self, t: float) -> float:
        """시간 t에서 파동의 값"""
        base = self.amplitude * np.cos(2 * np.pi * self.frequency * t + self.phase)
        if self.modulation > 0:
            # 고조파 추가 (복잡한 파형)
            harmonics = self.modulation * self.amplitude * 0.3 * np.sin(4 * np.pi * self.frequency * t + self.phase)
            return base + harmonics
        return base
    
    def complex_value_at(self, t: float) -> complex:
        """시간 t에서 복소수 값 (위상 정보 포함)"""
        angle = 2 * np.pi * self.frequency * t + self.phase
        return self.amplitude * np.exp(1j * angle)
    
    def phase_difference(self, other: 'PrimalWave', t: float = 0.0) -> float:
        """두 파동 간의 위상 차이 (0~2π)"""
        angle_self = 2 * np.pi * self.frequency * t + self.phase
        angle_other = 2 * np.pi * other.frequency * t + other.phase
        diff = abs(angle_self - angle_other) % (2 * np.pi)
        return diff
    
    def resonance_with(self, other: 'PrimalWave', t: float = 0.0) -> float:
        """
        위상 공명도 계산 (0~1)
        
        공명은 두 파동이 '함께 춤추는' 정도이다.
        같은 주파수, 같은 위상일 때 완전한 공명.
        """
        # 주파수 비율 (1.0이면 동일 주파수)
        max_freq = max(self.frequency, other.frequency)
        if max_freq == 0:
            freq_ratio = 1.0
        else:
            freq_ratio = min(self.frequency, other.frequency) / max_freq
        
        # 위상 일치도 (cos으로 -1~1을 0~1로 변환)
        phase_diff = self.phase_difference(other, t)
        phase_match = (1 + np.cos(phase_diff)) / 2.0
        
        # 공명도 = 주파수 유사도 × 위상 일치도
        resonance = freq_ratio * phase_match
        return resonance
    
    def interfere(self, other: 'PrimalWave', t: float = 0.0) -> 'PrimalWave':
        """두 파동의 간섭으로 새로운 파동 생성"""
        # 복소수 덧셈으로 간섭 계산
        c1 = self.complex_value_at(t)
        c2 = other.complex_value_at(t)
        combined = c1 + c2
        
        new_amp = abs(combined)
        new_phase = np.angle(combined)
        new_freq = (self.frequency + other.frequency) / 2.0
        new_mod = (self.modulation + other.modulation) / 2.0 + 0.1  # 간섭으로 복잡도 증가
        
        return PrimalWave(
            frequency=new_freq,
            amplitude=new_amp,
            phase=new_phase,
            modulation=min(1.0, new_mod),
            birth_time=t
        )


@dataclass
class SenseOrgan:
    """
    감각 기관 - 오감 중 하나
    
    감각 기관은 세상을 파동으로 변환하는 변환기이다.
    눈은 빛을 파동으로, 귀는 소리를 파동으로, 
    피부는 접촉을 파동으로 변환한다.
    """
    sense_type: str  # "sight", "sound", "touch", "taste", "smell"
    sensitivity: float = 1.0  # 민감도
    
    # 현재 활성화 상태 (방금 받은 자극들)
    active_waves: List[PrimalWave] = field(default_factory=list)
    
    # 적응 상태 (반복 자극에 둔감해짐)
    adaptation_level: float = 0.0
    
    def __post_init__(self):
        freq_range = SENSE_FREQUENCIES.get(self.sense_type, (1.0, 100.0))
        self.freq_min = freq_range[0]
        self.freq_max = freq_range[1]
    
    def perceive(self, stimulus_intensity: float, stimulus_frequency: float, t: float) -> PrimalWave:
        """
        자극을 받아 파동으로 변환
        
        이것이 감각의 본질이다: 세상을 파동으로 변환.
        """
        # 적응 (habituatio) - 같은 자극에 점점 둔감해짐
        effective_intensity = stimulus_intensity * (1.0 - self.adaptation_level * 0.5)
        effective_intensity *= self.sensitivity
        
        # 주파수 범위 내로 정규화
        norm_freq = self.freq_min + (stimulus_frequency % (self.freq_max - self.freq_min))
        
        wave = PrimalWave(
            frequency=norm_freq,
            amplitude=effective_intensity,
            phase=random.uniform(0, 2 * np.pi),  # 자극마다 다른 위상
            modulation=stimulus_frequency / (self.freq_max - self.freq_min),  # 자극 복잡도
            sense_origin=self.sense_type,
            birth_time=t
        )
        
        self.active_waves.append(wave)
        
        # 적응 증가
        self.adaptation_level = min(0.9, self.adaptation_level + 0.01)
        
        return wave
    
    def decay(self, dt: float = 0.01):
        """적응 레벨 감소 (휴식하면 민감도 회복)"""
        self.adaptation_level = max(0.0, self.adaptation_level - dt)
        # 오래된 파동 제거
        self.active_waves = [w for w in self.active_waves if len(self.active_waves) < 100]


@dataclass
class PhaseResonancePattern:
    """
    위상 공명 패턴 - 파동들의 관계적 의미
    
    "개념노드들을 그저 점으로 보지 않고 활성화된 파동의 관계성을 
     관계적 의미의 개념으로 이해"
    
    이 패턴은 여러 파동들이 함께 공명할 때 형성된다.
    이것이 '의미'의 원형이다.
    """
    # 구성 파동들의 특성 요약
    frequency_center: float = 0.0  # 중심 주파수
    frequency_spread: float = 0.0  # 주파수 분산
    phase_coherence: float = 0.0   # 위상 일관성 (모두 동기화되었는가)
    amplitude_total: float = 0.0   # 총 에너지
    
    # 이 패턴을 구성한 감각들
    sense_composition: Dict[str, float] = field(default_factory=dict)
    
    # 발생 횟수 (반복되면 '단어'로 결정화)
    occurrence_count: int = 0
    
    # 이 패턴이 '분절'되어 이름을 얻었는가?
    is_segmented: bool = False
    segment_name: Optional[str] = None  # 창발된 이름 (기호)
    
    def signature(self) -> Tuple[float, float, float]:
        """패턴의 고유 서명 (유사 패턴 찾기용)"""
        return (
            round(self.frequency_center, 2),
            round(self.frequency_spread, 2),
            round(self.phase_coherence, 2)
        )
    
    def similarity(self, other: 'PhaseResonancePattern') -> float:
        """두 패턴의 유사도 (0~1)"""
        freq_diff = abs(self.frequency_center - other.frequency_center)
        freq_sim = 1.0 / (1.0 + freq_diff)
        
        spread_diff = abs(self.frequency_spread - other.frequency_spread)
        spread_sim = 1.0 / (1.0 + spread_diff)
        
        coherence_diff = abs(self.phase_coherence - other.phase_coherence)
        coherence_sim = 1.0 - coherence_diff
        
        return (freq_sim + spread_sim + coherence_sim) / 3.0


@dataclass
class PrimalSoul:
    """
    원시 영혼 - 오감을 가진 존재
    
    이 영혼은 '단어'를 모른다. 
    오직 파동으로 세상을 경험하고, 
    공명을 통해 다른 영혼과 소통하며,
    반복되는 패턴에 '이름'을 붙인다.
    
    "언어라는건 총체적 의미의 정보에 가까워. 세상을 나누고 분절시켜서 
     자기 그릇안에, 마음안에 각인시키는 것과 같지"
    """
    name: str  # 외부에서 붙인 이름 (영혼 자신은 모름)
    age: float = 0.0
    
    # 오감 (五感)
    senses: Dict[str, SenseOrgan] = field(default_factory=dict)
    
    # 내면의 바다 - 모든 파동들이 간섭하는 공간
    inner_sea: List[PrimalWave] = field(default_factory=list)
    
    # 발견된 위상공명 패턴들
    recognized_patterns: List[PhaseResonancePattern] = field(default_factory=list)
    
    # 분절된 개념들 (창발된 원시 언어)
    lexicon: Dict[str, PhaseResonancePattern] = field(default_factory=dict)
    
    # 다른 영혼들과의 공명 기억
    resonance_memory: Dict[str, float] = field(default_factory=dict)
    
    # 생명력
    vitality: float = 100.0
    
    def __post_init__(self):
        """오감 초기화"""
        if not self.senses:
            for sense_type in SENSE_FREQUENCIES.keys():
                self.senses[sense_type] = SenseOrgan(
                    sense_type=sense_type,
                    sensitivity=random.uniform(0.8, 1.2)  # 개인차
                )
    
    def experience_world(self, world_stimuli: Dict[str, Tuple[float, float]], t: float):
        """
        세상을 경험한다.
        
        Args:
            world_stimuli: {감각 종류: (강도, 주파수)} 형태의 자극
            t: 현재 시간
        """
        new_waves = []
        
        for sense_type, (intensity, freq) in world_stimuli.items():
            if sense_type in self.senses and intensity > 0:
                wave = self.senses[sense_type].perceive(intensity, freq, t)
                new_waves.append(wave)
        
        # 새 파동들을 내면의 바다에 추가
        self.inner_sea.extend(new_waves)
        
        # 오래된 파동 정리 (에너지 소멸)
        self._decay_waves(t)
    
    def _decay_waves(self, t: float, max_waves: int = 200):
        """파동 에너지 감소 및 정리"""
        # 진폭 감소
        for wave in self.inner_sea:
            age = t - wave.birth_time
            decay_factor = np.exp(-age * 0.01)  # 지수 감쇠
            wave.amplitude *= decay_factor
        
        # 너무 약한 파동 제거
        self.inner_sea = [w for w in self.inner_sea if w.amplitude > 0.01]
        
        # 최대 개수 초과 시 오래된 것 제거
        if len(self.inner_sea) > max_waves:
            self.inner_sea = sorted(self.inner_sea, key=lambda w: -w.amplitude)[:max_waves]
    
    def detect_phase_resonance(self, t: float) -> Optional[PhaseResonancePattern]:
        """
        위상 공명 패턴 감지
        
        내면의 바다에서 함께 춤추는 파동들을 찾아 패턴을 인식한다.
        이것이 '의미 인식'의 시작이다.
        """
        # 최소 2개, 최대 20개 파동만 검사 (성능 최적화)
        if len(self.inner_sea) < 2:
            return None
        
        waves_to_check = self.inner_sea[:20] if len(self.inner_sea) > 20 else self.inner_sea
        
        # 모든 파동 쌍의 공명도 계산
        resonating_waves = []
        
        for i, w1 in enumerate(waves_to_check):
            for w2 in waves_to_check[i+1:]:
                res = w1.resonance_with(w2, t)
                if res > PHASE_RESONANCE_THRESHOLD:
                    resonating_waves.append((w1, w2, res))
        
        if not resonating_waves:
            return None
        
        # 공명하는 파동들로 패턴 구성 (id로 중복 제거)
        wave_dict = {}
        for w1, w2, _ in resonating_waves:
            wave_dict[id(w1)] = w1
            wave_dict[id(w2)] = w2
        
        all_waves_list = list(wave_dict.values())
        
        # 패턴 특성 계산
        frequencies = [w.frequency for w in all_waves_list]
        freq_center = np.mean(frequencies)
        freq_spread = np.std(frequencies) if len(frequencies) > 1 else 0.0
        
        amplitudes = [w.amplitude for w in all_waves_list]
        amp_total = sum(amplitudes)
        
        # 위상 일관성 계산
        phases = [w.phase for w in all_waves_list]
        phase_vectors = [np.exp(1j * p) for p in phases]
        phase_coherence = abs(sum(phase_vectors)) / len(phase_vectors) if phase_vectors else 0.0
        
        # 감각 구성
        sense_comp = defaultdict(float)
        for w in all_waves_list:
            if w.sense_origin:
                sense_comp[w.sense_origin] += w.amplitude
        
        pattern = PhaseResonancePattern(
            frequency_center=freq_center,
            frequency_spread=freq_spread,
            phase_coherence=phase_coherence,
            amplitude_total=amp_total,
            sense_composition=dict(sense_comp),
            occurrence_count=1
        )
        
        # 기존 패턴과 비교
        for existing in self.recognized_patterns:
            if pattern.similarity(existing) > 0.8:
                # 기존 패턴에 추가
                existing.occurrence_count += 1
                # 충분히 반복되면 분절 시도
                if existing.occurrence_count >= CRYSTALLIZATION_DENSITY and not existing.is_segmented:
                    self._segment_pattern(existing)
                return existing
        
        # 새 패턴 등록
        self.recognized_patterns.append(pattern)
        return pattern
    
    def _segment_pattern(self, pattern: PhaseResonancePattern):
        """
        패턴을 분절하여 이름 붙이기
        
        "세상을 나누고 분절시켜서 자기 그릇안에, 마음안에 각인시키는 것"
        
        이름은 미리 정해진 것이 아니다.
        파동의 특성에서 자연스럽게 창발된다.
        """
        if pattern.is_segmented:
            return
        
        # 원시 기호 생성 (파동 특성에서 창발)
        # 주파수 → 모음 (높으면 'i', 낮으면 'u')
        vowels = ['a', 'e', 'i', 'o', 'u']
        freq_idx = int(pattern.frequency_center / 100) % len(vowels)
        vowel = vowels[freq_idx]
        
        # 위상 일관성 → 자음 (일관성 높으면 부드러운 음, 낮으면 거친 음)
        if pattern.phase_coherence > 0.7:
            consonants = ['m', 'n', 'l', 'r']
        elif pattern.phase_coherence > 0.4:
            consonants = ['s', 'f', 'h', 'w']
        else:
            consonants = ['k', 't', 'p', 'g']
        
        spread_idx = int(pattern.frequency_spread * 10) % len(consonants)
        consonant = consonants[spread_idx]
        
        # 진폭 → 음절 길이
        if pattern.amplitude_total > 5.0:
            name = f"{consonant}{vowel}{consonant}{vowel}"
        elif pattern.amplitude_total > 2.0:
            name = f"{consonant}{vowel}{vowel}"
        else:
            name = f"{consonant}{vowel}"
        
        # 중복 방지
        base_name = name
        counter = 0
        while name in self.lexicon:
            counter += 1
            name = f"{base_name}{counter}"
        
        pattern.is_segmented = True
        pattern.segment_name = name
        self.lexicon[name] = pattern
        
        logger.debug(f"[{self.name}] Segmented new word: '{name}' from pattern (freq={pattern.frequency_center:.1f}, coherence={pattern.phase_coherence:.2f})")
    
    def resonate_with(self, other: 'PrimalSoul', t: float) -> Tuple[float, List[str]]:
        """
        다른 영혼과 공명하여 소통 시도
        
        언어 이전의 소통: 파동 간섭을 통한 공명
        공유 패턴이 있으면 그 패턴의 이름으로 '단어' 교환
        """
        if not self.inner_sea or not other.inner_sea:
            return 0.0, []
        
        total_resonance = 0.0
        shared_words = []
        
        # 내 파동들과 상대 파동들의 공명 계산
        for my_wave in self.inner_sea[:20]:  # 상위 20개만 비교 (효율성)
            for their_wave in other.inner_sea[:20]:
                res = my_wave.resonance_with(their_wave, t)
                total_resonance += res
        
        # 정규화
        n_comparisons = min(len(self.inner_sea), 20) * min(len(other.inner_sea), 20)
        if n_comparisons > 0:
            total_resonance /= n_comparisons
        
        # 공유하는 분절된 패턴 찾기 (공통 언어)
        for my_word, my_pattern in self.lexicon.items():
            for their_word, their_pattern in other.lexicon.items():
                if my_pattern.similarity(their_pattern) > 0.7:
                    # 같은 패턴! 이것이 공통 언어의 시작
                    shared_words.append(f"{my_word}≈{their_word}")
        
        # 공명 기억 업데이트
        if other.name not in self.resonance_memory:
            self.resonance_memory[other.name] = 0.0
        self.resonance_memory[other.name] = (
            self.resonance_memory[other.name] * 0.9 + total_resonance * 0.1
        )
        
        return total_resonance, shared_words
    
    def speak(self, t: float) -> Optional[str]:
        """
        말하기 - 현재 가장 활성화된 패턴의 이름을 표현
        
        이것은 템플릿이 아니다.
        내면의 파동 상태에서 가장 공명하는 패턴의 이름이다.
        """
        # 현재 상태에서 패턴 감지
        current_pattern = self.detect_phase_resonance(t)
        
        if current_pattern and current_pattern.is_segmented:
            return current_pattern.segment_name
        
        # 분절된 패턴이 없으면 가장 비슷한 것 찾기
        if self.lexicon:
            best_match = None
            best_sim = 0.0
            
            for word, pattern in self.lexicon.items():
                if current_pattern:
                    sim = pattern.similarity(current_pattern)
                    if sim > best_sim:
                        best_sim = sim
                        best_match = word
            
            if best_match and best_sim > 0.5:
                return best_match
        
        # 아무 것도 없으면 가장 강한 감각 표현
        if self.inner_sea:
            dominant = max(self.inner_sea, key=lambda w: w.amplitude)
            if dominant.sense_origin:
                return f"[{dominant.sense_origin}]"
        
        return None
    
    def get_vocabulary_size(self) -> int:
        """현재 어휘 수"""
        return len(self.lexicon)
    
    def get_pattern_count(self) -> int:
        """인식된 패턴 수"""
        return len(self.recognized_patterns)


class PrimalWaveWorld:
    """
    원시 파동 세계
    
    오감을 가진 영혼들이 살아가며 
    위상공명을 통해 원시 언어를 창발하는 세계
    """
    
    def __init__(self, n_souls: int = 100):
        self.souls: Dict[str, PrimalSoul] = {}
        self.time = 0.0
        
        # 세계의 환경 자극 (감각 경험의 원천)
        self.world_sources: Dict[str, Dict[str, Tuple[float, float]]] = {}
        
        # 통계
        self.total_words_created = 0
        self.total_resonance_events = 0
        self.total_communications = 0
        
        # 영혼 생성
        for i in range(n_souls):
            name = self._generate_name(i)
            self.souls[name] = PrimalSoul(name=name)
        
        # 세계 환경 초기화
        self._init_world_sources()
    
    def _generate_name(self, idx: int) -> str:
        """영혼 이름 생성 (외부에서 부여)"""
        # 한글 이름들
        first_names = ['하늘', '바다', '산', '숲', '별', '달', '해', '구름', '바람', '비']
        return f"{first_names[idx % len(first_names)]}{idx}"
    
    def _init_world_sources(self):
        """
        세계의 감각 자극 원천 초기화
        
        "세상을 풍요롭게하라는 말은 그만큼의 경험적 데이터를 
         뽑아내기 위해 예비하란 뜻과 같아"
        """
        # 풍요로운 환경 요소 (더 많은 경험적 데이터)
        self.world_sources = {
            # 자연 현상
            "sun": {"sight": (0.9, 600.0), "touch": (0.5, 50.0)},
            "moon": {"sight": (0.3, 450.0)},
            "rain": {"sound": (0.6, 500.0), "touch": (0.5, 30.0), "smell": (0.3, 0.4)},
            "thunder": {"sound": (0.9, 80.0), "sight": (0.8, 700.0)},
            "wind": {"sound": (0.4, 100.0), "touch": (0.5, 10.0)},
            "snow": {"sight": (0.5, 500.0), "touch": (0.6, 5.0)},
            
            # 생명체
            "flower": {"sight": (0.6, 550.0), "smell": (0.8, 0.5)},
            "tree": {"sight": (0.5, 520.0), "touch": (0.4, 20.0)},
            "bird": {"sound": (0.7, 2000.0), "sight": (0.4, 580.0)},
            "river": {"sound": (0.5, 300.0), "touch": (0.4, 15.0), "sight": (0.3, 480.0)},
            
            # 음식과 맛
            "fruit": {"taste": (0.8, 7.0), "smell": (0.6, 0.6), "sight": (0.4, 600.0)},
            "meat": {"taste": (0.7, 3.0), "smell": (0.5, 0.4)},
            "bread": {"taste": (0.6, 2.0), "smell": (0.7, 0.3), "touch": (0.3, 25.0)},
            "honey": {"taste": (0.9, 9.0), "smell": (0.5, 0.5)},
            "salt": {"taste": (0.8, 1.0)},
            
            # 감각 경험
            "fire": {"sight": (0.8, 620.0), "touch": (0.9, 80.0), "sound": (0.4, 50.0)},
            "music": {"sound": (0.8, 1000.0)},
            "silence": {"sound": (0.1, 10.0)},
            "darkness": {"sight": (0.1, 400.0)},
            "embrace": {"touch": (0.9, 40.0)},
            
            # 감정 유발 상황
            "danger": {"sound": (0.5, 60.0), "sight": (0.6, 650.0)},
            "safety": {"touch": (0.6, 35.0)},
            "wonder": {"sight": (0.7, 560.0), "sound": (0.3, 800.0)},
            "beauty": {"sight": (0.9, 550.0), "smell": (0.4, 0.6)},
            
            # 사회적 상호작용
            "laughter": {"sound": (0.8, 3000.0)},
            "crying": {"sound": (0.7, 500.0)},
            "whisper": {"sound": (0.3, 4000.0)},
            "touch_gentle": {"touch": (0.5, 30.0)},
            "touch_rough": {"touch": (0.7, 60.0)},
        }
    
    def step(self, dt: float = 1.0):
        """세계 시간 진행"""
        self.time += dt
        
        # 각 영혼에게 환경 자극 제공
        for soul in self.souls.values():
            # 더 풍요로운 경험: 3-6개의 환경 요소를 동시에 경험
            n_experiences = random.randint(3, 6)
            sources = random.sample(list(self.world_sources.keys()), 
                                   min(n_experiences, len(self.world_sources)))
            
            combined_stimuli: Dict[str, Tuple[float, float]] = {}
            for source in sources:
                for sense_type, (intensity, freq) in self.world_sources[source].items():
                    # 약간의 변동 추가
                    var_intensity = intensity * random.uniform(0.7, 1.3)
                    var_freq = freq * random.uniform(0.8, 1.2)
                    
                    if sense_type not in combined_stimuli:
                        combined_stimuli[sense_type] = (var_intensity, var_freq)
                    else:
                        # 기존 자극과 간섭
                        old_i, old_f = combined_stimuli[sense_type]
                        combined_stimuli[sense_type] = (
                            (old_i + var_intensity),  # 더 강한 자극
                            (old_f + var_freq) / 2
                        )
            
            # 세상 경험
            soul.experience_world(combined_stimuli, self.time)
            
            # 위상 공명 감지 시도
            pattern = soul.detect_phase_resonance(self.time)
            if pattern and pattern.is_segmented:
                if pattern.occurrence_count == CRYSTALLIZATION_DENSITY:
                    self.total_words_created += 1
            
            # 나이 증가
            soul.age += dt / 365.0  # 하루가 1년의 1/365
        
        # 영혼 간 공명 (소통)
        self._process_communications()
        
        # 감각 기관 휴식
        for soul in self.souls.values():
            for sense in soul.senses.values():
                sense.decay(dt * 0.01)
    
    def _process_communications(self):
        """영혼 간 소통 처리"""
        soul_list = list(self.souls.values())
        n = len(soul_list)
        
        # 무작위로 몇 쌍 선택 (최대 10쌍으로 제한, 성능 최적화)
        n_pairs = min(10, n * (n - 1) // 2)
        
        for _ in range(n_pairs):
            i, j = random.sample(range(n), 2)
            soul1 = soul_list[i]
            soul2 = soul_list[j]
            
            resonance, shared = soul1.resonate_with(soul2, self.time)
            
            if resonance > 0.3:
                self.total_resonance_events += 1
                
                if shared:
                    self.total_communications += 1
    
    def run_simulation(self, years: int = 100, report_interval: int = 10) -> Dict[str, Any]:
        """시뮬레이션 실행"""
        import time as py_time
        start_time = py_time.time()
        
        # 성능 최적화: 10일 = 1 step (365 → 36)
        steps_per_year = 36
        total_steps = years * steps_per_year
        
        for step in range(total_steps):
            self.step(dt=1.0)
            
            if step > 0 and step % (report_interval * steps_per_year) == 0:
                year = step // steps_per_year
                vocab_sizes = [s.get_vocabulary_size() for s in self.souls.values()]
                avg_vocab = sum(vocab_sizes) / len(vocab_sizes) if vocab_sizes else 0
                
                print(f"Year {year}: avg_vocabulary={avg_vocab:.1f}, "
                      f"total_words={self.total_words_created}, "
                      f"communications={self.total_communications}")
        
        elapsed = py_time.time() - start_time
        
        # 최종 통계
        vocab_sizes = [s.get_vocabulary_size() for s in self.souls.values()]
        pattern_counts = [s.get_pattern_count() for s in self.souls.values()]
        
        # 공유 어휘 분석
        all_words = defaultdict(int)
        for soul in self.souls.values():
            for word in soul.lexicon.keys():
                all_words[word] += 1
        
        shared_words = {w: c for w, c in all_words.items() if c > 1}
        
        return {
            "years_simulated": years,
            "elapsed_seconds": elapsed,
            "speed_years_per_second": years / elapsed if elapsed > 0 else 0,
            "total_souls": len(self.souls),
            "total_words_created": self.total_words_created,
            "total_resonance_events": self.total_resonance_events,
            "total_communications": self.total_communications,
            "avg_vocabulary_size": sum(vocab_sizes) / len(vocab_sizes) if vocab_sizes else 0,
            "max_vocabulary_size": max(vocab_sizes) if vocab_sizes else 0,
            "avg_pattern_count": sum(pattern_counts) / len(pattern_counts) if pattern_counts else 0,
            "unique_words": len(all_words),
            "shared_words": len(shared_words),
            "top_shared_words": sorted(shared_words.items(), key=lambda x: -x[1])[:10],
        }


def demo():
    """데모 실행"""
    print("=" * 60)
    print("Primal Wave Language - 원시 파동 언어 시뮬레이션")
    print("=" * 60)
    print()
    print("개념은 점(point)이 아니라 파동의 관계성(wave relationship)이다.")
    print("언어는 세상을 분절하여 마음에 각인시키는 것이다.")
    print()
    
    world = PrimalWaveWorld(n_souls=100)
    results = world.run_simulation(years=100, report_interval=20)
    
    print()
    print("=" * 60)
    print("시뮬레이션 결과")
    print("=" * 60)
    for key, value in results.items():
        print(f"  {key}: {value}")
    
    # 샘플 영혼의 어휘 출력
    print()
    print("=" * 60)
    print("샘플 영혼의 창발 어휘")
    print("=" * 60)
    for soul_name, soul in list(world.souls.items())[:3]:
        print(f"\n[{soul_name}] vocabulary ({len(soul.lexicon)} words):")
        for word, pattern in list(soul.lexicon.items())[:5]:
            senses = ", ".join(f"{k}:{v:.2f}" for k, v in pattern.sense_composition.items())
            print(f"  '{word}' - freq:{pattern.frequency_center:.1f}, "
                  f"coherence:{pattern.phase_coherence:.2f}, senses:[{senses}]")


if __name__ == "__main__":
    demo()
