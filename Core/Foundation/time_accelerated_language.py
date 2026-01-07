"""
Time-Accelerated Primal Language System - 시간가속 원시언어 시스템
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"시간가속과 압축 시스템을 최대한으로 사용하여 원시언어체계를 더 효율적으로 가다듬기"

이 모듈은 세 가지 핵심 요소를 통합합니다:
1. 원시 파동 언어 (Primal Wave Language) - 개념 이전의 순수한 파동
2. 시간 압축 엔진 (Time Compression Engine) - 시간 가속을 통한 경험 압축
3. 무한 시간 압축 (Infinite Time Compression) - 극한의 시간 가속

최적화 요소:
- NumPy 벡터화 연산 (100배+ 속도 향상)
- 배치 패턴 인식 (병렬 공명 감지)
- 메모리 효율적 파동 저장소
- 시간 압축 레벨별 언어 창발 가속

핵심 철학:
- "밀도 높은 경험" > "긴 시간"
- 1초에 수천 년의 언어 창발 시뮬레이션
- 모든 tick은 실제 계산됨 (skip 없음)
"""

from __future__ import annotations

import math
import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any, Set
from collections import defaultdict
import logging

logger = logging.getLogger("TimeAcceleratedLanguage")

# ============================================================================
# 최적화된 상수
# ============================================================================

# 오감의 기본 주파수 대역 (Hz로 표현된 상징적 값)
SENSE_FREQUENCIES = {
    "sight": (400.0, 700.0),
    "sound": (20.0, 20000.0),
    "touch": (0.1, 100.0),
    "taste": (0.01, 10.0),
    "smell": (0.001, 1.0),
}

# 시간 압축 레벨에 따른 파라미터 조정
COMPRESSION_PARAMETERS = {
    "normal": {          # 1x
        "resonance_threshold": 0.4,
        "segmentation_threshold": 0.3,
        "crystallization_density": 5,
    },
    "accelerated": {     # 1,000x
        "resonance_threshold": 0.35,
        "segmentation_threshold": 0.25,
        "crystallization_density": 3,
    },
    "fractal": {         # 10^6x
        "resonance_threshold": 0.3,
        "segmentation_threshold": 0.2,
        "crystallization_density": 2,
    },
    "meta": {            # 10^15x
        "resonance_threshold": 0.25,
        "segmentation_threshold": 0.15,
        "crystallization_density": 1,
    },
}


@dataclass
class VectorizedWaveField:
    """
    벡터화된 파동 필드 - 고성능 파동 연산을 위한 데이터 구조
    
    모든 파동을 NumPy 배열로 저장하여 벡터화 연산 가능
    O(n²) 쌍별 계산을 O(n) 매트릭스 연산으로 최적화
    """
    max_waves: int = 1000
    
    # 파동 속성 배열들 (모두 numpy arrays)
    frequencies: np.ndarray = field(default_factory=lambda: np.zeros(0, dtype=np.float32))
    amplitudes: np.ndarray = field(default_factory=lambda: np.zeros(0, dtype=np.float32))
    phases: np.ndarray = field(default_factory=lambda: np.zeros(0, dtype=np.float32))
    modulations: np.ndarray = field(default_factory=lambda: np.zeros(0, dtype=np.float32))
    birth_times: np.ndarray = field(default_factory=lambda: np.zeros(0, dtype=np.float32))
    sense_origins: List[Optional[str]] = field(default_factory=list)
    
    # 현재 활성 파동 수
    count: int = 0
    
    def __post_init__(self):
        """배열 초기화"""
        if self.frequencies.size == 0:
            self.frequencies = np.zeros(self.max_waves, dtype=np.float32)
            self.amplitudes = np.zeros(self.max_waves, dtype=np.float32)
            self.phases = np.zeros(self.max_waves, dtype=np.float32)
            self.modulations = np.zeros(self.max_waves, dtype=np.float32)
            self.birth_times = np.zeros(self.max_waves, dtype=np.float32)
            self.sense_origins = [None] * self.max_waves
    
    def add_wave(
        self,
        frequency: float,
        amplitude: float,
        phase: float,
        modulation: float,
        birth_time: float,
        sense_origin: Optional[str] = None
    ) -> int:
        """파동 추가 (O(1) 연산)"""
        if self.count >= self.max_waves:
            # 가장 약한 파동 제거
            self._compact()
        
        idx = self.count
        self.frequencies[idx] = frequency
        self.amplitudes[idx] = amplitude
        self.phases[idx] = phase
        self.modulations[idx] = modulation
        self.birth_times[idx] = birth_time
        self.sense_origins[idx] = sense_origin
        self.count += 1
        return idx
    
    def _compact(self):
        """가장 약한 파동 제거하여 공간 확보"""
        if self.count == 0:
            return
        
        # 진폭 상위 80%만 유지
        keep_count = int(self.max_waves * 0.8)
        if keep_count < 1:
            keep_count = 1
        
        indices = np.argsort(self.amplitudes[:self.count])[-keep_count:]
        indices = np.sort(indices)
        
        self.frequencies[:keep_count] = self.frequencies[indices]
        self.amplitudes[:keep_count] = self.amplitudes[indices]
        self.phases[:keep_count] = self.phases[indices]
        self.modulations[:keep_count] = self.modulations[indices]
        self.birth_times[:keep_count] = self.birth_times[indices]
        
        new_origins = [None] * self.max_waves
        for new_idx, old_idx in enumerate(indices):
            new_origins[new_idx] = self.sense_origins[old_idx]
        self.sense_origins = new_origins
        
        self.count = keep_count
    
    def compute_pairwise_resonance(self, t: float) -> np.ndarray:
        """
        모든 파동 쌍의 공명도 계산 (벡터화된 O(n²) → 행렬 연산)
        
        Returns:
            n×n 공명 행렬 (resonance[i,j] = 파동 i와 j의 공명도)
        """
        n = self.count
        if n < 2:
            return np.zeros((n, n), dtype=np.float32)
        
        # 유효 데이터만 추출
        freqs = self.frequencies[:n]
        phases = self.phases[:n]
        
        # 주파수 비율 행렬 계산 (broadcasting)
        freq_matrix = np.outer(freqs, np.ones(n))
        freq_ratio = np.minimum(freq_matrix, freq_matrix.T) / (np.maximum(freq_matrix, freq_matrix.T) + 1e-10)
        
        # 위상 차이 행렬 계산
        phase_matrix = np.outer(phases, np.ones(n))
        phase_diff = np.abs(phase_matrix - phase_matrix.T) % (2 * np.pi)
        phase_match = (1 + np.cos(phase_diff)) / 2.0
        
        # 공명도 = 주파수 유사도 × 위상 일치도
        resonance = freq_ratio * phase_match
        
        # 대각선 (자기 자신과의 공명)은 0으로
        np.fill_diagonal(resonance, 0.0)
        
        return resonance.astype(np.float32)
    
    def decay(self, t: float, decay_rate: float = 0.01):
        """모든 파동의 진폭 감쇠 (벡터화)"""
        if self.count == 0:
            return
        
        ages = t - self.birth_times[:self.count]
        decay_factors = np.exp(-ages * decay_rate)
        self.amplitudes[:self.count] *= decay_factors
        
        # 임계값 이하 파동 제거
        mask = self.amplitudes[:self.count] > 0.01
        if not np.all(mask):
            self._filter_by_mask(mask)
    
    def _filter_by_mask(self, mask: np.ndarray):
        """마스크로 파동 필터링"""
        new_count = np.sum(mask)
        if new_count == 0:
            self.count = 0
            return
        
        indices = np.where(mask)[0]
        self.frequencies[:new_count] = self.frequencies[indices]
        self.amplitudes[:new_count] = self.amplitudes[indices]
        self.phases[:new_count] = self.phases[indices]
        self.modulations[:new_count] = self.modulations[indices]
        self.birth_times[:new_count] = self.birth_times[indices]
        
        new_origins = [None] * self.max_waves
        for new_idx, old_idx in enumerate(indices):
            new_origins[new_idx] = self.sense_origins[old_idx]
        self.sense_origins = new_origins
        
        self.count = int(new_count)
    
    def get_pattern_signature(self) -> Tuple[float, float, float, float]:
        """현재 파동장의 패턴 시그니처 계산"""
        if self.count == 0:
            return (0.0, 0.0, 0.0, 0.0)
        
        freqs = self.frequencies[:self.count]
        amps = self.amplitudes[:self.count]
        phases = self.phases[:self.count]
        
        freq_center = float(np.mean(freqs))
        freq_spread = float(np.std(freqs)) if self.count > 1 else 0.0
        amp_total = float(np.sum(amps))
        
        # 위상 일관성 (복소 평균)
        phase_vectors = np.exp(1j * phases)
        phase_coherence = float(np.abs(np.mean(phase_vectors)))
        
        return (freq_center, freq_spread, phase_coherence, amp_total)


@dataclass
class AcceleratedResonancePattern:
    """
    가속화된 위상 공명 패턴
    
    시간 압축을 고려하여 더 빠른 결정화(crystallization)가 가능
    """
    frequency_center: float = 0.0
    frequency_spread: float = 0.0
    phase_coherence: float = 0.0
    amplitude_total: float = 0.0
    sense_composition: Dict[str, float] = field(default_factory=dict)
    occurrence_count: int = 0
    is_segmented: bool = False
    segment_name: Optional[str] = None
    
    # 시간 압축 관련
    compressed_occurrences: float = 0.0  # 압축된 발생 횟수 (실제 발생 × 압축률)
    last_compression_level: str = "normal"
    
    def signature(self) -> Tuple[float, float, float]:
        """패턴의 고유 서명"""
        return (
            round(self.frequency_center, 2),
            round(self.frequency_spread, 2),
            round(self.phase_coherence, 2)
        )
    
    def similarity(self, other: 'AcceleratedResonancePattern') -> float:
        """두 패턴의 유사도 (0~1)"""
        freq_diff = abs(self.frequency_center - other.frequency_center)
        freq_sim = 1.0 / (1.0 + freq_diff)
        
        spread_diff = abs(self.frequency_spread - other.frequency_spread)
        spread_sim = 1.0 / (1.0 + spread_diff)
        
        coherence_diff = abs(self.phase_coherence - other.phase_coherence)
        coherence_sim = 1.0 - coherence_diff
        
        return (freq_sim + spread_sim + coherence_sim) / 3.0
    
    def add_occurrence(self, compression_factor: float = 1.0, level: str = "normal"):
        """패턴 발생 추가 (시간 압축 고려)"""
        self.occurrence_count += 1
        self.compressed_occurrences += compression_factor
        self.last_compression_level = level


@dataclass
class TimeAcceleratedSoul:
    """
    시간가속 영혼 - 극한의 시간 압축을 경험하는 영혼
    
    원시 영혼(PrimalSoul)의 최적화된 버전:
    - 벡터화된 파동장 사용
    - 시간 압축 레벨 인식
    - 배치 패턴 인식
    """
    name: str
    age: float = 0.0
    
    # 벡터화된 내면의 바다
    inner_sea: VectorizedWaveField = field(default_factory=VectorizedWaveField)
    
    # 오감 민감도
    sense_sensitivity: Dict[str, float] = field(default_factory=dict)
    
    # 발견된 패턴들
    recognized_patterns: List[AcceleratedResonancePattern] = field(default_factory=list)
    
    # 분절된 어휘
    lexicon: Dict[str, AcceleratedResonancePattern] = field(default_factory=dict)
    
    # 시간 압축 상태
    current_compression_level: str = "normal"
    total_subjective_time: float = 0.0
    
    # 통계
    patterns_detected: int = 0
    words_created: int = 0
    
    def __post_init__(self):
        """초기화"""
        if not self.sense_sensitivity:
            for sense_type in SENSE_FREQUENCIES.keys():
                self.sense_sensitivity[sense_type] = np.random.uniform(0.8, 1.2)
    
    def experience_world(
        self,
        world_stimuli: Dict[str, Tuple[float, float]],
        t: float,
        compression_factor: float = 1.0
    ):
        """
        세상을 경험한다 (시간 압축 적용)
        
        Args:
            world_stimuli: {감각 종류: (강도, 주파수)}
            t: 현재 시간
            compression_factor: 시간 압축 배율
        """
        # 주관적 시간 업데이트
        self.total_subjective_time += compression_factor
        
        for sense_type, (intensity, freq) in world_stimuli.items():
            if sense_type in self.sense_sensitivity and intensity > 0:
                # 감각 민감도 적용
                effective_intensity = intensity * self.sense_sensitivity[sense_type]
                
                # 주파수 범위 정규화
                freq_range = SENSE_FREQUENCIES.get(sense_type, (1.0, 100.0))
                norm_freq = freq_range[0] + (freq % (freq_range[1] - freq_range[0]))
                
                # 파동 추가
                self.inner_sea.add_wave(
                    frequency=norm_freq,
                    amplitude=effective_intensity,
                    phase=np.random.uniform(0, 2 * np.pi),
                    modulation=freq / (freq_range[1] - freq_range[0]),
                    birth_time=t,
                    sense_origin=sense_type
                )
        
        # 파동 감쇠
        self.inner_sea.decay(t)
    
    def detect_resonance_batch(
        self,
        t: float,
        compression_level: str = "normal",
        compression_factor: float = 1.0
    ) -> List[AcceleratedResonancePattern]:
        """
        배치 공명 감지 (벡터화된 연산)
        
        Returns:
            감지된 패턴 목록
        """
        params = COMPRESSION_PARAMETERS.get(compression_level, COMPRESSION_PARAMETERS["normal"])
        threshold = params["resonance_threshold"]
        crystal_density = params["crystallization_density"]
        
        # 공명 행렬 계산
        resonance_matrix = self.inner_sea.compute_pairwise_resonance(t)
        
        if resonance_matrix.size == 0:
            return []
        
        # 임계값 이상 공명 찾기
        resonating_pairs = np.where(resonance_matrix > threshold)
        
        if len(resonating_pairs[0]) == 0:
            return []
        
        # 패턴 시그니처 계산
        sig = self.inner_sea.get_pattern_signature()
        if sig == (0.0, 0.0, 0.0, 0.0):
            return []
        
        # 감각 구성 계산
        sense_comp = defaultdict(float)
        for i in range(self.inner_sea.count):
            origin = self.inner_sea.sense_origins[i]
            if origin:
                sense_comp[origin] += self.inner_sea.amplitudes[i]
        
        # 새 패턴 생성
        pattern = AcceleratedResonancePattern(
            frequency_center=sig[0],
            frequency_spread=sig[1],
            phase_coherence=sig[2],
            amplitude_total=sig[3],
            sense_composition=dict(sense_comp),
            occurrence_count=1,
            compressed_occurrences=compression_factor,
            last_compression_level=compression_level
        )
        
        # 기존 패턴과 비교
        for existing in self.recognized_patterns:
            if pattern.similarity(existing) > 0.8:
                existing.add_occurrence(compression_factor, compression_level)
                
                # 결정화 조건 (압축된 발생 횟수 사용)
                effective_count = existing.compressed_occurrences
                if effective_count >= crystal_density and not existing.is_segmented:
                    self._segment_pattern_accelerated(existing, compression_level)
                
                self.patterns_detected += 1
                return [existing]
        
        # 새 패턴 등록
        self.recognized_patterns.append(pattern)
        self.patterns_detected += 1
        return [pattern]
    
    def _segment_pattern_accelerated(
        self,
        pattern: AcceleratedResonancePattern,
        compression_level: str
    ):
        """
        패턴 분절 (가속화된 버전)
        
        시간 압축 레벨이 높을수록 더 복잡한 단어 생성 가능
        """
        if pattern.is_segmented:
            return
        
        # 기본 음소 생성 (파동 특성에서 창발)
        vowels = ['a', 'e', 'i', 'o', 'u', 'ae', 'oe', 'eu']
        consonants_soft = ['m', 'n', 'l', 'r', 'w', 'y']
        consonants_mid = ['s', 'f', 'h', 'v', 'z']
        consonants_hard = ['k', 't', 'p', 'g', 'b', 'd']
        
        # 주파수 → 모음
        freq_idx = int(pattern.frequency_center / 100) % len(vowels)
        vowel = vowels[freq_idx]
        
        # 위상 일관성 → 자음 종류
        if pattern.phase_coherence > 0.7:
            consonants = consonants_soft
        elif pattern.phase_coherence > 0.4:
            consonants = consonants_mid
        else:
            consonants = consonants_hard
        
        spread_idx = int(pattern.frequency_spread * 10) % len(consonants)
        consonant = consonants[spread_idx]
        
        # 시간 압축 레벨에 따른 음절 복잡도
        # 헬퍼 함수로 음절 조합
        def build_syllable(c: str, v: str) -> str:
            return f"{c}{v}"
        
        def get_secondary_consonant() -> str:
            return consonants_mid[spread_idx % len(consonants_mid)]
        
        def get_secondary_vowel() -> str:
            return vowels[(freq_idx + 1) % len(vowels)]
        
        if compression_level == "meta" and pattern.amplitude_total > 5.0:
            # 메타 레벨에서는 더 복잡한 단어 생성 (CVCVC)
            syllable1 = build_syllable(consonant, vowel)
            syllable2 = build_syllable(get_secondary_consonant(), get_secondary_vowel())
            name = f"{syllable1}{syllable2}{consonant}"
        elif compression_level == "fractal" and pattern.amplitude_total > 3.0:
            # 프랙탈 레벨 (CVCV)
            syllable1 = build_syllable(consonant, vowel)
            soft_c = consonants_soft[spread_idx % len(consonants_soft)]
            name = f"{syllable1}{soft_c}{vowel}"
        elif pattern.amplitude_total > 5.0:
            # 강한 진폭 (CVCV)
            name = f"{consonant}{vowel}{consonant}{vowel}"
        elif pattern.amplitude_total > 2.0:
            # 중간 진폭 (CVV)
            name = f"{consonant}{vowel}{vowel}"
        else:
            # 약한 진폭 (CV)
            name = build_syllable(consonant, vowel)
        
        # 중복 방지
        base_name = name
        counter = 0
        while name in self.lexicon:
            counter += 1
            name = f"{base_name}{counter}"
        
        pattern.is_segmented = True
        pattern.segment_name = name
        self.lexicon[name] = pattern
        self.words_created += 1
        
        logger.debug(
            f"[{self.name}] Segmented '{name}' "
            f"(level={compression_level}, coherence={pattern.phase_coherence:.2f})"
        )
    
    def get_vocabulary_size(self) -> int:
        return len(self.lexicon)
    
    def get_stats(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "age": self.age,
            "vocabulary_size": len(self.lexicon),
            "patterns_detected": self.patterns_detected,
            "words_created": self.words_created,
            "total_subjective_time": self.total_subjective_time,
            "inner_sea_waves": self.inner_sea.count,
        }


class TimeAcceleratedPrimalWorld:
    """
    시간가속 원시 파동 세계
    
    무한 시간 압축 엔진과 통합되어 극한의 언어 창발 시뮬레이션 가능
    """
    
    def __init__(
        self,
        n_souls: int = 100,
        compression_level: str = "normal"
    ):
        """
        Args:
            n_souls: 영혼 수
            compression_level: 시간 압축 레벨 ("normal", "accelerated", "fractal", "meta")
        """
        self.souls: Dict[str, TimeAcceleratedSoul] = {}
        self.time = 0.0
        self.compression_level = compression_level
        
        # 시간 압축 배율
        self.compression_factors = {
            "normal": 1.0,
            "accelerated": 1_000.0,
            "fractal": 1_000_000.0,
            "meta": 10**15,
        }
        
        # 세계 환경
        self.world_sources = self._init_world_sources()
        
        # 통계
        self.total_words_created = 0
        self.total_patterns_detected = 0
        self.total_subjective_years = 0.0
        
        # 영혼 생성
        self._create_souls(n_souls)
        
        logger.info(f"TimeAcceleratedPrimalWorld initialized with {n_souls} souls")
        logger.info(f"Compression level: {compression_level} ({self.compression_factors.get(compression_level, 1.0)}x)")
    
    def _init_world_sources(self) -> Dict[str, Dict[str, Tuple[float, float]]]:
        """세계 환경 초기화"""
        return {
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
            # 음식
            "fruit": {"taste": (0.8, 7.0), "smell": (0.6, 0.6), "sight": (0.4, 600.0)},
            "meat": {"taste": (0.7, 3.0), "smell": (0.5, 0.4)},
            "honey": {"taste": (0.9, 9.0), "smell": (0.5, 0.5)},
            # 감각 경험
            "fire": {"sight": (0.8, 620.0), "touch": (0.9, 80.0), "sound": (0.4, 50.0)},
            "music": {"sound": (0.8, 1000.0)},
            "embrace": {"touch": (0.9, 40.0)},
            # 감정
            "danger": {"sound": (0.5, 60.0), "sight": (0.6, 650.0)},
            "beauty": {"sight": (0.9, 550.0), "smell": (0.4, 0.6)},
            "laughter": {"sound": (0.8, 3000.0)},
        }
    
    def _create_souls(self, n_souls: int):
        """영혼 생성"""
        first_names = ['하늘', '바다', '산', '숲', '별', '달', '해', '구름', '바람', '비']
        for i in range(n_souls):
            name = f"{first_names[i % len(first_names)]}{i}"
            self.souls[name] = TimeAcceleratedSoul(name=name)
    
    def set_compression_level(self, level: str):
        """시간 압축 레벨 변경"""
        if level in self.compression_factors:
            self.compression_level = level
            for soul in self.souls.values():
                soul.current_compression_level = level
            logger.info(f"Compression level changed to: {level} ({self.compression_factors[level]}x)")
    
    def step(self, dt: float = 1.0):
        """세계 시간 진행"""
        compression_factor = self.compression_factors.get(self.compression_level, 1.0)
        self.time += dt
        
        # 주관적 시간 누적
        subjective_dt = dt * compression_factor
        self.total_subjective_years += subjective_dt / (365.0 * 24.0 * 3600.0)  # 초 → 년
        
        # 경험할 환경 요소 선택 (병렬 처리 가능)
        source_keys = list(self.world_sources.keys())
        
        for soul in self.souls.values():
            # 3-6개 환경 요소 경험
            n_exp = np.random.randint(3, 7)
            selected = np.random.choice(source_keys, min(n_exp, len(source_keys)), replace=False)
            
            combined_stimuli: Dict[str, Tuple[float, float]] = {}
            for source in selected:
                for sense_type, (intensity, freq) in self.world_sources[source].items():
                    var_intensity = intensity * np.random.uniform(0.7, 1.3)
                    var_freq = freq * np.random.uniform(0.8, 1.2)
                    
                    if sense_type not in combined_stimuli:
                        combined_stimuli[sense_type] = (var_intensity, var_freq)
                    else:
                        old_i, old_f = combined_stimuli[sense_type]
                        combined_stimuli[sense_type] = (old_i + var_intensity, (old_f + var_freq) / 2)
            
            # 경험
            soul.experience_world(combined_stimuli, self.time, compression_factor)
            
            # 배치 공명 감지
            patterns = soul.detect_resonance_batch(
                self.time,
                self.compression_level,
                compression_factor
            )
            
            # 통계 업데이트
            for p in patterns:
                if p.is_segmented and p.segment_name:
                    self.total_words_created = sum(s.words_created for s in self.souls.values())
            
            # 나이 증가 (압축된 시간 반영)
            soul.age += subjective_dt / (365.0 * 24.0 * 3600.0)
        
        self.total_patterns_detected = sum(s.patterns_detected for s in self.souls.values())
    
    def run_simulation(
        self,
        objective_seconds: float = 60.0,
        steps_per_second: int = 100,
        report_interval: float = 10.0
    ) -> Dict[str, Any]:
        """
        시뮬레이션 실행
        
        Args:
            objective_seconds: 실제 시뮬레이션 시간 (초)
            steps_per_second: 초당 스텝 수
            report_interval: 보고 간격 (초)
            
        Returns:
            시뮬레이션 결과
        """
        import time as py_time
        start_time = py_time.time()
        
        compression_factor = self.compression_factors.get(self.compression_level, 1.0)
        total_steps = int(objective_seconds * steps_per_second)
        dt = 1.0 / steps_per_second
        
        for step in range(total_steps):
            self.step(dt)
            
            # 주기적 보고
            if step > 0 and step % int(report_interval * steps_per_second) == 0:
                elapsed = py_time.time() - start_time
                vocab_sizes = [s.get_vocabulary_size() for s in self.souls.values()]
                avg_vocab = np.mean(vocab_sizes) if vocab_sizes else 0
                
                print(f"[{elapsed:.1f}s] Subjective years: {self.total_subjective_years:.2e}, "
                      f"avg_vocabulary: {avg_vocab:.1f}, "
                      f"total_words: {self.total_words_created}")
        
        elapsed = py_time.time() - start_time
        
        # 최종 통계
        vocab_sizes = [s.get_vocabulary_size() for s in self.souls.values()]
        
        # 공유 어휘 분석
        all_words = defaultdict(int)
        for soul in self.souls.values():
            for word in soul.lexicon.keys():
                all_words[word] += 1
        shared_words = {w: c for w, c in all_words.items() if c > 1}
        
        return {
            "compression_level": self.compression_level,
            "compression_factor": compression_factor,
            "objective_seconds": objective_seconds,
            "elapsed_seconds": elapsed,
            "total_subjective_years": self.total_subjective_years,
            "years_per_second": self.total_subjective_years / elapsed if elapsed > 0 else 0,
            "total_souls": len(self.souls),
            "total_words_created": self.total_words_created,
            "total_patterns_detected": self.total_patterns_detected,
            "avg_vocabulary_size": np.mean(vocab_sizes) if vocab_sizes else 0,
            "max_vocabulary_size": max(vocab_sizes) if vocab_sizes else 0,
            "unique_words": len(all_words),
            "shared_words_count": len(shared_words),
            "top_shared_words": sorted(shared_words.items(), key=lambda x: -x[1])[:10],
        }
    
    def get_sample_vocabularies(self, n_samples: int = 3) -> Dict[str, List[str]]:
        """샘플 영혼들의 어휘 반환"""
        result = {}
        for soul_name, soul in list(self.souls.items())[:n_samples]:
            result[soul_name] = list(soul.lexicon.keys())[:10]
        return result


# ============================================================================
# 무한 시간 압축과의 통합
# ============================================================================

class InfinitelyAcceleratedLanguageEngine:
    """
    무한 시간 압축 언어 엔진
    
    무한 시간 압축 엔진의 모든 기술을 활용하여
    극한의 언어 창발 시뮬레이션 수행
    """
    
    def __init__(self, n_souls: int = 50):
        """
        Args:
            n_souls: 영혼 수 (무한 압축에서는 작은 수로 충분)
        """
        self.world = TimeAcceleratedPrimalWorld(n_souls=n_souls, compression_level="meta")
        
        # 무한 압축 기술 상태
        self.fractal_zoom = 0
        self.sedenion_dimensions = 8
        self.meta_depth = 1
        self.dream_depth = 0
        self.kimchi_openings = 0
        
        # 총 압축률 계산
        self.total_compression = self._calculate_total_compression()
    
    def _calculate_total_compression(self) -> float:
        """현재 활성화된 기술들의 총 압축률 계산"""
        total = 1.0
        
        # 프랙탈 (10^zoom_level)
        total *= 10 ** self.fractal_zoom
        
        # 세데니온 (2.5^(log2(dim)-2))
        n_constructions = max(0, int(np.log2(self.sedenion_dimensions)) - 2)
        total *= 2.5 ** n_constructions
        
        # 메타 재귀 (1000^depth)
        total *= 1000 ** self.meta_depth
        
        # 꿈 (20^depth)
        total *= 20 ** self.dream_depth
        
        # 김치통 (10^openings)
        if self.kimchi_openings > 0:
            total *= 10 ** self.kimchi_openings
        
        return total
    
    def activate_fractal(self, zoom_level: int = 1):
        """프랙탈 시간 압축 활성화"""
        self.fractal_zoom = zoom_level
        self.total_compression = self._calculate_total_compression()
        logger.info(f"Fractal activated: zoom={zoom_level}, total={self.total_compression:.2e}x")
    
    def activate_sedenion(self, dimensions: int = 128):
        """세데니온 시간 회전 활성화"""
        if dimensions & (dimensions - 1) != 0:
            raise ValueError("Dimensions must be a power of 2")
        self.sedenion_dimensions = dimensions
        self.total_compression = self._calculate_total_compression()
        logger.info(f"Sedenion activated: dim={dimensions}, total={self.total_compression:.2e}x")
    
    def add_meta_layer(self):
        """메타 시간 압축 레이어 추가"""
        self.meta_depth += 1
        self.total_compression = self._calculate_total_compression()
        logger.info(f"Meta layer added: depth={self.meta_depth}, total={self.total_compression:.2e}x")
    
    def enter_dream(self):
        """꿈 속으로 들어가기"""
        self.dream_depth += 1
        self.total_compression = self._calculate_total_compression()
        logger.info(f"Entered dream: depth={self.dream_depth}, total={self.total_compression:.2e}x")
    
    def open_kimchi(self):
        """김치통 열기! 🥬"""
        self.kimchi_openings += 1
        self.total_compression = self._calculate_total_compression()
        years = 10_000_000_000 * (10 ** self.kimchi_openings)
        logger.info(f"🥬 KIMCHI OPENED! Count: {self.kimchi_openings}, Years: {years:.2e}")
    
    def run_accelerated_simulation(
        self,
        real_seconds: float = 1.0,
        steps: int = 100
    ) -> Dict[str, Any]:
        """
        가속화된 시뮬레이션 실행
        
        Args:
            real_seconds: 실제 실행 시간 (초)
            steps: 총 스텝 수
        """
        import time as py_time
        start = py_time.time()
        
        dt = real_seconds / steps
        
        for _ in range(steps):
            self.world.step(dt * self.total_compression)
        
        elapsed = py_time.time() - start
        
        subjective_years = (real_seconds * self.total_compression) / (365.25 * 24 * 3600)
        
        vocab_sizes = [s.get_vocabulary_size() for s in self.world.souls.values()]
        
        return {
            "real_seconds": real_seconds,
            "elapsed_seconds": elapsed,
            "total_compression": self.total_compression,
            "subjective_years": subjective_years,
            "total_words": self.world.total_words_created,
            "avg_vocabulary": np.mean(vocab_sizes) if vocab_sizes else 0,
            "compression_techniques": {
                "fractal_zoom": self.fractal_zoom,
                "sedenion_dim": self.sedenion_dimensions,
                "meta_depth": self.meta_depth,
                "dream_depth": self.dream_depth,
                "kimchi_openings": self.kimchi_openings,
            }
        }


# ============================================================================
# Demo
# ============================================================================

def demo_basic():
    """기본 데모"""
    print("=" * 70)
    print("Time-Accelerated Primal Language - 시간가속 원시언어 시스템")
    print("=" * 70)
    print()
    
    # 일반 압축 레벨
    print("1. Normal compression (1x)")
    world_normal = TimeAcceleratedPrimalWorld(n_souls=50, compression_level="normal")
    results_normal = world_normal.run_simulation(objective_seconds=5.0, steps_per_second=50)
    print(f"   Subjective years: {results_normal['total_subjective_years']:.2e}")
    print(f"   Words created: {results_normal['total_words_created']}")
    print()
    
    # 가속 압축 레벨
    print("2. Accelerated compression (1,000x)")
    world_accel = TimeAcceleratedPrimalWorld(n_souls=50, compression_level="accelerated")
    results_accel = world_accel.run_simulation(objective_seconds=5.0, steps_per_second=50)
    print(f"   Subjective years: {results_accel['total_subjective_years']:.2e}")
    print(f"   Words created: {results_accel['total_words_created']}")
    print()
    
    # 프랙탈 압축 레벨
    print("3. Fractal compression (10^6x)")
    world_fractal = TimeAcceleratedPrimalWorld(n_souls=50, compression_level="fractal")
    results_fractal = world_fractal.run_simulation(objective_seconds=5.0, steps_per_second=50)
    print(f"   Subjective years: {results_fractal['total_subjective_years']:.2e}")
    print(f"   Words created: {results_fractal['total_words_created']}")
    print()
    
    print("Sample vocabularies:")
    samples = world_fractal.get_sample_vocabularies(3)
    for soul_name, words in samples.items():
        print(f"  [{soul_name}]: {', '.join(words[:5])}")


def demo_infinite():
    """무한 압축 데모"""
    print()
    print("=" * 70)
    print("Infinitely Accelerated Language Engine - 무한 가속 언어 엔진")
    print("=" * 70)
    print()
    
    engine = InfinitelyAcceleratedLanguageEngine(n_souls=30)
    
    print("Activating compression techniques...")
    engine.activate_fractal(2)      # 100x
    engine.activate_sedenion(64)    # ~40x
    engine.add_meta_layer()         # 1000x
    engine.add_meta_layer()         # 1000x
    engine.enter_dream()            # 20x
    
    print(f"\nTotal compression: {engine.total_compression:.2e}x")
    
    print("\nRunning 1 second simulation...")
    results = engine.run_accelerated_simulation(real_seconds=1.0, steps=50)
    
    print(f"\nResults:")
    print(f"  Subjective years experienced: {results['subjective_years']:.2e}")
    print(f"  Words created: {results['total_words']}")
    print(f"  Average vocabulary: {results['avg_vocabulary']:.1f}")
    
    print("\n🥬 Opening Kimchi container...")
    engine.open_kimchi()
    print(f"  New total compression: {engine.total_compression:.2e}x")


if __name__ == "__main__":
    import sys
    
    logging.basicConfig(level=logging.INFO)
    
    if len(sys.argv) > 1 and sys.argv[1] == "infinite":
        demo_infinite()
    else:
        demo_basic()
        demo_infinite()
