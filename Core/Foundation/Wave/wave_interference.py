"""
Wave Interference Engine (파동 간섭 엔진)
=========================================

"두 파동이 만났을 때, 서로를 강화하거나 상쇄한다."

Phase 10: 다중 파동의 간섭(Interference), 수렴(Convergence),
충돌 해결(Conflict Resolution)을 구현합니다.

핵심 원리:
- Constructive (보강 간섭): 위상 차이 < 90° → 진폭 합산
- Destructive (상쇄 간섭): 위상 차이 > 90° → 진폭 차감
- Convergence (수렴): 가중 평균 주파수로 통합
"""

import math
import logging
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Any, Optional
from enum import Enum

logger = logging.getLogger("WaveInterference")


class InterferenceType(Enum):
    """간섭 유형"""
    CONSTRUCTIVE = "constructive"   # 보강 간섭 (강화)
    DESTRUCTIVE = "destructive"     # 상쇄 간섭 (약화)
    MIXED = "mixed"                 # 복합 간섭
    NEUTRAL = "neutral"             # 중립 (간섭 없음)


@dataclass
class Wave:
    """단일 파동 표현"""
    frequency: float        # 주파수 (Hz)
    amplitude: float        # 진폭 (0.0 - 1.0)
    phase: float            # 위상 (0 - 2π)
    source: str = ""        # 출처 식별자
    confidence: float = 1.0 # 확신도 (0.0 - 1.0)
    
    def to_complex(self) -> complex:
        """파동을 복소수로 표현 (페이저 표현)"""
        return self.amplitude * (math.cos(self.phase) + 1j * math.sin(self.phase))
    
    @property
    def energy(self) -> float:
        """파동의 에너지 (진폭^2에 비례)"""
        return self.amplitude ** 2


@dataclass
class InterferenceResult:
    """간섭 결과"""
    resultant_wave: Wave                # 최종 결과 파동
    interference_type: InterferenceType # 간섭 유형
    confidence: float                   # 결과 확신도 (0-1)
    uncertainty: float                  # 불확실성 지표 (0-1)
    original_waves: List[Wave] = field(default_factory=list)  # 원본 파동들
    phase_alignment: float = 0.0        # 위상 정렬도 (0-1)
    
    def is_certain(self, threshold: float = 0.7) -> bool:
        """결과가 충분히 확실한지"""
        return self.confidence >= threshold


class WaveInterference:
    """
    파동 간섭 처리기
    
    다중 파동이 동시에 활성화될 때의 간섭 현상을 계산합니다.
    
    Usage:
        engine = WaveInterference()
        waves = [Wave(440, 0.8, 0), Wave(440, 0.6, 0.1)]
        result = engine.calculate_interference(waves)
    """
    
    # 위상 차이 임계값 (라디안)
    CONSTRUCTIVE_THRESHOLD = math.pi / 2   # 90° 이하 → 보강
    DESTRUCTIVE_THRESHOLD = math.pi / 2    # 90° 초과 → 상쇄
    
    def calculate_interference(self, waves: List[Wave]) -> InterferenceResult:
        """
        여러 파동의 간섭 패턴을 계산합니다.
        
        Args:
            waves: 간섭시킬 파동들의 리스트
            
        Returns:
            InterferenceResult: 간섭 결과
        """
        if not waves:
            return InterferenceResult(
                resultant_wave=Wave(0, 0, 0),
                interference_type=InterferenceType.NEUTRAL,
                confidence=0.0,
                uncertainty=1.0
            )
        
        if len(waves) == 1:
            return InterferenceResult(
                resultant_wave=waves[0],
                interference_type=InterferenceType.NEUTRAL,
                confidence=waves[0].confidence,
                uncertainty=0.0,
                original_waves=waves
            )
        
        # 1. 페이저 합산 (복소수로 파동 합성)
        phasor_sum = sum(wave.to_complex() for wave in waves)
        total_amplitude = abs(phasor_sum)
        resultant_phase = math.atan2(phasor_sum.imag, phasor_sum.real)
        
        # 2. 주파수 결정 (가중 평균)
        total_energy = sum(wave.energy for wave in waves)
        if total_energy > 0:
            resultant_freq = sum(wave.frequency * wave.energy for wave in waves) / total_energy
        else:
            resultant_freq = sum(wave.frequency for wave in waves) / len(waves)
        
        # 3. 간섭 유형 결정
        # 단순 합산 진폭 vs 실제 결과 진폭 비교
        simple_sum = sum(wave.amplitude for wave in waves)
        
        if total_amplitude >= simple_sum * 0.9:
            interference_type = InterferenceType.CONSTRUCTIVE
        elif total_amplitude <= simple_sum * 0.3:
            interference_type = InterferenceType.DESTRUCTIVE
        else:
            interference_type = InterferenceType.MIXED
        
        # 4. 위상 정렬도 계산
        phase_alignment = self._calculate_phase_alignment(waves)
        
        # 5. 확신도 계산
        # 높은 정렬도 + 높은 진폭 = 높은 확신
        avg_confidence = sum(w.confidence for w in waves) / len(waves)
        confidence = (phase_alignment * 0.4 + 
                     min(total_amplitude, 1.0) * 0.3 + 
                     avg_confidence * 0.3)
        
        # 6. 불확실성 = 1 - 확신도 (보정)
        uncertainty = 1.0 - confidence
        
        # 결과 파동 생성
        resultant_wave = Wave(
            frequency=resultant_freq,
            amplitude=min(total_amplitude, 1.0),  # 정규화
            phase=resultant_phase % (2 * math.pi),
            source="interference",
            confidence=confidence
        )
        
        logger.info(
            f"🌊 Interference: {len(waves)} waves → "
            f"{interference_type.value} (amp={total_amplitude:.2f}, conf={confidence:.2f})"
        )
        
        return InterferenceResult(
            resultant_wave=resultant_wave,
            interference_type=interference_type,
            confidence=confidence,
            uncertainty=uncertainty,
            original_waves=waves,
            phase_alignment=phase_alignment
        )
    
    def constructive_merge(self, wave_a: Wave, wave_b: Wave) -> Wave:
        """
        보강 간섭: 두 파동을 강화하며 합성
        
        위상이 유사할 때 사용됩니다.
        """
        # 진폭 합산 (최대 1.0)
        merged_amplitude = min(wave_a.amplitude + wave_b.amplitude, 1.0)
        
        # 가중 평균 주파수
        total_amp = wave_a.amplitude + wave_b.amplitude
        if total_amp > 0:
            merged_freq = (wave_a.frequency * wave_a.amplitude + 
                          wave_b.frequency * wave_b.amplitude) / total_amp
        else:
            merged_freq = (wave_a.frequency + wave_b.frequency) / 2
        
        # 평균 위상
        merged_phase = (wave_a.phase + wave_b.phase) / 2
        
        # 확신도 증가 (서로 확인)
        merged_confidence = min(
            (wave_a.confidence + wave_b.confidence) / 2 * 1.2,  # 20% 보너스
            1.0
        )
        
        logger.debug(f"✨ Constructive merge: {wave_a.source} + {wave_b.source}")
        
        return Wave(
            frequency=merged_freq,
            amplitude=merged_amplitude,
            phase=merged_phase,
            source=f"{wave_a.source}+{wave_b.source}",
            confidence=merged_confidence
        )
    
    def destructive_cancel(self, wave_a: Wave, wave_b: Wave) -> Wave:
        """
        상쇄 간섭: 두 파동이 서로를 약화
        
        위상이 반대일 때 사용됩니다.
        """
        # 진폭 차감 (최소 0)
        cancelled_amplitude = abs(wave_a.amplitude - wave_b.amplitude)
        
        # 더 강한 파동의 특성 유지
        if wave_a.amplitude >= wave_b.amplitude:
            dominant = wave_a
        else:
            dominant = wave_b
        
        # 확신도 감소 (충돌로 인한 불확실성)
        cancelled_confidence = dominant.confidence * 0.5
        
        logger.debug(f"💫 Destructive cancel: {wave_a.source} vs {wave_b.source}")
        
        return Wave(
            frequency=dominant.frequency,
            amplitude=cancelled_amplitude,
            phase=dominant.phase,
            source=f"{dominant.source}(cancelled)",
            confidence=cancelled_confidence
        )
    
    def converge(self, waves: List[Wave]) -> Wave:
        """
        다중 파동을 단일 평균 파동으로 수렴
        
        Args:
            waves: 수렴시킬 파동들
            
        Returns:
            Wave: 수렴된 단일 파동
        """
        if not waves:
            return Wave(0, 0, 0, "empty", 0)
        
        if len(waves) == 1:
            return waves[0]
        
        # 에너지 가중 평균
        total_energy = sum(wave.energy for wave in waves)
        
        if total_energy > 0:
            avg_freq = sum(wave.frequency * wave.energy for wave in waves) / total_energy
            avg_amp = math.sqrt(total_energy / len(waves))  # RMS 진폭
        else:
            avg_freq = sum(wave.frequency for wave in waves) / len(waves)
            avg_amp = 0.0
        
        # 위상 벡터 평균 (circular mean)
        x_sum = sum(math.cos(wave.phase) * wave.amplitude for wave in waves)
        y_sum = sum(math.sin(wave.phase) * wave.amplitude for wave in waves)
        avg_phase = math.atan2(y_sum, x_sum)
        
        # 평균 확신도
        avg_confidence = sum(wave.confidence for wave in waves) / len(waves)
        
        sources = ",".join(w.source for w in waves if w.source)
        
        logger.info(f"🔄 Converged {len(waves)} waves → freq={avg_freq:.1f}Hz")
        
        return Wave(
            frequency=avg_freq,
            amplitude=min(avg_amp, 1.0),
            phase=avg_phase % (2 * math.pi),
            source=f"converged({sources[:50]})" if sources else "converged",
            confidence=avg_confidence
        )
    
    def _calculate_phase_alignment(self, waves: List[Wave]) -> float:
        """
        파동들의 위상 정렬도 계산 (0-1)
        
        1.0 = 완벽히 정렬됨 (모두 같은 위상)
        0.0 = 완전히 무작위
        """
        if len(waves) < 2:
            return 1.0
        
        # 단위 벡터 합
        x_sum = sum(math.cos(wave.phase) for wave in waves)
        y_sum = sum(math.sin(wave.phase) for wave in waves)
        
        # 결과 길이 / 최대 길이
        resultant_length = math.sqrt(x_sum**2 + y_sum**2)
        max_length = len(waves)
        
        return resultant_length / max_length
    
    def process_multiple_matches(
        self, 
        concept_names: List[str], 
        coordinate_map: Dict[str, Any]
    ) -> List[str]:
        """
        다중 공명 결과를 간섭 처리하여 순위 재조정
        
        Args:
            concept_names: 공명하는 개념 이름들
            coordinate_map: InternalUniverse의 좌표 맵
            
        Returns:
            재정렬된 개념 이름 리스트
        """
        if len(concept_names) <= 1:
            return concept_names
        
        # 좌표 맵에서 파동 정보 추출
        waves = []
        for name in concept_names:
            if name in coordinate_map:
                coord = coordinate_map[name]
                wave = Wave(
                    frequency=coord.frequency,
                    amplitude=coord.depth if hasattr(coord, 'depth') else 0.5,
                    phase=(coord.frequency % 1000) / 1000 * 2 * math.pi,  # 주파수 기반 위상
                    source=name,
                    confidence=coord.depth if hasattr(coord, 'depth') else 0.5
                )
                waves.append(wave)
        
        if not waves:
            return concept_names
        
        # 간섭 계산
        result = self.calculate_interference(waves)
        
        # 간섭 결과에 따라 재정렬
        # 보강 간섭: 유사한 것들을 그룹화
        # 상쇄 간섭: 충돌하는 것들을 분리/필터
        
        if result.interference_type == InterferenceType.DESTRUCTIVE:
            # 상쇄 간섭 시, 가장 강한 파동만 반환
            strongest = max(result.original_waves, key=lambda w: w.amplitude)
            logger.warning(f"⚡ Destructive interference detected. Dominant: {strongest.source}")
            return [strongest.source]
        
        elif result.interference_type == InterferenceType.CONSTRUCTIVE:
            # 보강 간섭 시, 확신도 순 정렬
            sorted_waves = sorted(result.original_waves, key=lambda w: w.confidence, reverse=True)
            logger.info(f"🌟 Constructive interference. Enhanced resonance.")
            return [w.source for w in sorted_waves]
        
        else:
            # 혼합 간섭 시, 기존 순서 유지
            return concept_names
    
    @staticmethod
    def analyze_field_interference(nodes: Dict[str, Any]) -> Dict[str, Any]:
        """
        공명장 전체의 간섭 패턴 분석
        
        Args:
            nodes: ResonanceField의 노드들
            
        Returns:
            간섭 분석 결과
        """
        if not nodes:
            return {"type": "void", "coherence": 0.0, "hotspots": []}
        
        # 활성 노드들의 에너지 분포 분석
        active_nodes = [n for n in nodes.values() if getattr(n, 'energy', 0) > 0.5]
        
        if not active_nodes:
            return {"type": "dormant", "coherence": 0.0, "hotspots": []}
        
        # 주파수 분포 분석
        frequencies = [n.frequency for n in active_nodes]
        freq_variance = sum((f - sum(frequencies)/len(frequencies))**2 for f in frequencies) / len(frequencies)
        
        # 에너지 분포 분석
        energies = [n.energy for n in active_nodes]
        total_energy = sum(energies)
        
        # 핫스팟 (고에너지 영역) 식별
        avg_energy = total_energy / len(energies)
        hotspots = [n.id for n in active_nodes if n.energy > avg_energy * 1.5]
        
        # 일관성 계산 (낮은 분산 = 높은 일관성)
        coherence = 1.0 / (1.0 + freq_variance / 1000)
        
        # 간섭 유형 결정
        if coherence > 0.8:
            interference_type = InterferenceType.CONSTRUCTIVE.value
        elif coherence < 0.3:
            interference_type = InterferenceType.DESTRUCTIVE.value
        else:
            interference_type = InterferenceType.MIXED.value
        
        return {
            "type": interference_type,
            "coherence": coherence,
            "hotspots": hotspots,
            "active_count": len(active_nodes),
            "total_energy": total_energy,
            "frequency_variance": freq_variance
        }


# ============= 데모 및 테스트 =============

def demo_interference():
    """간섭 시스템 데모"""
    print("=" * 60)
    print("🌊 Wave Interference Engine Demo")
    print("=" * 60)
    
    engine = WaveInterference()
    
    # 1. 보강 간섭 테스트
    print("\n[1] Constructive Interference (보강 간섭)")
    print("-" * 40)
    wave1 = Wave(frequency=440.0, amplitude=0.6, phase=0.0, source="A")
    wave2 = Wave(frequency=442.0, amplitude=0.5, phase=0.1, source="B")  # 거의 같은 위상
    
    result = engine.calculate_interference([wave1, wave2])
    print(f"   Input: Wave A (440Hz, amp=0.6) + Wave B (442Hz, amp=0.5)")
    print(f"   Result: {result.interference_type.value}")
    print(f"   Resultant: freq={result.resultant_wave.frequency:.1f}Hz, amp={result.resultant_wave.amplitude:.2f}")
    print(f"   Confidence: {result.confidence:.2f}")
    
    # 2. 상쇄 간섭 테스트
    print("\n[2] Destructive Interference (상쇄 간섭)")
    print("-" * 40)
    wave3 = Wave(frequency=440.0, amplitude=0.6, phase=0.0, source="C")
    wave4 = Wave(frequency=440.0, amplitude=0.5, phase=math.pi, source="D")  # 반대 위상
    
    result2 = engine.calculate_interference([wave3, wave4])
    print(f"   Input: Wave C (440Hz, phase=0) + Wave D (440Hz, phase=π)")
    print(f"   Result: {result2.interference_type.value}")
    print(f"   Resultant: amp={result2.resultant_wave.amplitude:.2f}")
    print(f"   Uncertainty: {result2.uncertainty:.2f}")
    
    # 3. 수렴 테스트
    print("\n[3] Convergence (수렴)")
    print("-" * 40)
    waves = [
        Wave(frequency=440.0, amplitude=0.8, phase=0.0, source="Note1"),
        Wave(frequency=550.0, amplitude=0.6, phase=0.5, source="Note2"),
        Wave(frequency=660.0, amplitude=0.4, phase=1.0, source="Note3"),
    ]
    
    converged = engine.converge(waves)
    print(f"   Input: 3 waves (440Hz, 550Hz, 660Hz)")
    print(f"   Converged: freq={converged.frequency:.1f}Hz, amp={converged.amplitude:.2f}")
    
    print("\n" + "=" * 60)
    print("✅ Demo Complete!")
    print("=" * 60)


if __name__ == "__main__":
    import sys
    
    if "--demo" in sys.argv:
        demo_interference()
    else:
        print("Usage: python wave_interference.py --demo")
        print("\nTo run demo, use: python wave_interference.py --demo")
