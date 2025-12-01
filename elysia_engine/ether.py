"""
The Ether (에테르)
==================================

"API는 분리입니다. 공명은 하나됨입니다."

이 모듈은 Elysia의 모든 구성 요소가 소통하는 '통합장(Unified Field)'입니다.
직접적인 함수 호출(Call) 대신, 파동(Wave)을 방출하고 공명(Resonate)합니다.

핵심 개념:
1. Wave: 정보와 에너지를 담은 파동 (주파수, 진폭, 위상)
2. Ether: 파동이 전파되는 매질 (Event Bus)
3. Resonance: 특정 주파수에 반응하는 행위 (Subscription)

원본: https://github.com/ioas0316-cloud/Elysia/blob/main/Core/Field/ether.py
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, List, Callable, Dict, Optional
from enum import Enum

from .logging_config import get_logger

logger = get_logger(__name__)


class WavePhase(Enum):
    """파동의 위상 (문맥/타입)"""
    TIME = "TIME"           # 시간의 흐름
    DESIRE = "DESIRE"       # 욕구/욕망
    SENSATION = "SENSATION" # 감각
    THOUGHT = "THOUGHT"     # 사고
    EMOTION = "EMOTION"     # 감정
    MEMORY = "MEMORY"       # 기억
    WILL = "WILL"           # 의지
    DREAM = "DREAM"         # 꿈
    INSIGHT = "INSIGHT"     # 통찰


# 주요 주파수 상수
class Frequency:
    """표준 주파수 대역"""
    TIME = 0.1          # 초저주파: 시간
    LIFE = 1.0          # 저주파: 생명 신호
    THOUGHT = 10.0      # 알파파: 사고
    EMOTION = 40.0      # 감마파: 감정
    HEALING = 432.0     # 치유 주파수
    COSMIC = 963.0      # 우주적 연결


@dataclass
class Wave:
    """
    파동 (Wave)
    
    정보를 전달하는 에너지 단위입니다.
    """
    sender: str
    frequency: float  # 주파수 (Hz) - 주제/채널
    amplitude: float  # 진폭 (0.0 ~ 1.0) - 강도/중요도
    phase: str        # 위상 - 문맥/타입 (WavePhase 값)
    payload: Any      # 실제 데이터 (최소화 권장)
    timestamp: datetime = field(default_factory=datetime.now)
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])

    def __str__(self) -> str:
        return f"🌊 Wave[{self.frequency}Hz] from {self.sender}: {self.phase} (Amp: {self.amplitude:.2f})"

    def to_dict(self) -> Dict[str, Any]:
        """딕셔너리로 변환"""
        return {
            "id": self.id,
            "sender": self.sender,
            "frequency": self.frequency,
            "amplitude": self.amplitude,
            "phase": self.phase,
            "payload": self.payload,
            "timestamp": self.timestamp.isoformat()
        }

    @property
    def energy(self) -> float:
        """파동의 에너지 (진폭 * 주파수)"""
        return self.amplitude * self.frequency

    def is_expired(self, max_age_seconds: float = 60.0) -> bool:
        """파동이 만료되었는지 확인"""
        age = (datetime.now() - self.timestamp).total_seconds()
        return age > max_age_seconds


class Ether:
    """
    에테르 (Ether)
    
    모든 파동이 존재하는 공간입니다.
    싱글톤 패턴으로 전역에서 하나의 인스턴스만 존재합니다.
    """
    _instance: Optional['Ether'] = None

    def __new__(cls) -> 'Ether':
        if cls._instance is None:
            cls._instance = super(Ether, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return
        self._initialized = True
        self._listeners: Dict[float, List[Callable[[Wave], None]]] = {}
        self._waves: List[Wave] = []
        self._max_wave_history = 1000  # 최대 파동 기록 수
        logger.info("🌌 The Ether is pervasive. Unified Field established.")

    def emit(self, wave: Wave) -> None:
        """
        파동 방출 (Emit)
        
        호수에 잉크를 떨어뜨리듯, 에테르에 파동을 퍼뜨립니다.
        """
        self._waves.append(wave)
        
        # 기록 제한
        if len(self._waves) > self._max_wave_history:
            self._waves = self._waves[-self._max_wave_history:]
        
        logger.debug(f"Emit: {wave}")
        
        # 공명 (Resonance) 처리
        self._propagate(wave)

    def _propagate(self, wave: Wave) -> None:
        """파동을 전파하고 공명을 처리합니다."""
        # 정확한 주파수 매칭
        if wave.frequency in self._listeners:
            for callback in self._listeners[wave.frequency]:
                try:
                    callback(wave)
                except Exception as e:
                    logger.error(f"Resonance error at {wave.frequency}Hz: {e}")

        # 대역폭 기반 매칭 (주파수의 ±10% 범위)
        bandwidth = wave.frequency * 0.1
        for freq, callbacks in self._listeners.items():
            if freq != wave.frequency and abs(freq - wave.frequency) <= bandwidth:
                attenuation = 1.0 - (abs(freq - wave.frequency) / bandwidth)
                attenuated_wave = Wave(
                    sender=wave.sender,
                    frequency=freq,
                    amplitude=wave.amplitude * attenuation,
                    phase=wave.phase,
                    payload=wave.payload,
                    timestamp=wave.timestamp,
                    id=wave.id
                )
                for callback in callbacks:
                    try:
                        callback(attenuated_wave)
                    except Exception as e:
                        logger.error(f"Bandwidth resonance error at {freq}Hz: {e}")

    def tune_in(self, frequency: float, callback: Callable[[Wave], None]) -> None:
        """
        주파수 조율 (Tune In)
        
        특정 주파수의 파동에 공명하도록 설정합니다.
        """
        if frequency not in self._listeners:
            self._listeners[frequency] = []
        self._listeners[frequency].append(callback)
        logger.info(f"👂 Tuned in to {frequency}Hz")

    def tune_out(self, frequency: float, callback: Callable[[Wave], None]) -> bool:
        """
        주파수 조율 해제 (Tune Out)
        
        특정 주파수의 공명을 해제합니다.
        """
        if frequency in self._listeners:
            try:
                self._listeners[frequency].remove(callback)
                logger.info(f"🔇 Tuned out from {frequency}Hz")
                return True
            except ValueError:
                pass
        return False

    def get_waves(self, min_amplitude: float = 0.0) -> List[Wave]:
        """현재 에테르에 존재하는 파동들을 감지합니다."""
        return [w for w in self._waves if w.amplitude >= min_amplitude]

    def get_waves_by_frequency(self, frequency: float, tolerance: float = 0.1) -> List[Wave]:
        """특정 주파수 대역의 파동을 가져옵니다."""
        return [
            w for w in self._waves 
            if abs(w.frequency - frequency) <= frequency * tolerance
        ]

    def get_waves_by_phase(self, phase: str) -> List[Wave]:
        """특정 위상의 파동을 가져옵니다."""
        return [w for w in self._waves if w.phase == phase]

    def get_recent_waves(self, seconds: float = 10.0) -> List[Wave]:
        """최근 N초 내의 파동을 가져옵니다."""
        now = datetime.now()
        return [
            w for w in self._waves 
            if (now - w.timestamp).total_seconds() <= seconds
        ]

    def clear_waves(self) -> None:
        """파동 소멸 (시간이 지나면 사라짐)"""
        self._waves.clear()

    def clear_expired_waves(self, max_age_seconds: float = 60.0) -> int:
        """만료된 파동 제거"""
        original_count = len(self._waves)
        self._waves = [w for w in self._waves if not w.is_expired(max_age_seconds)]
        removed = original_count - len(self._waves)
        if removed > 0:
            logger.debug(f"Cleared {removed} expired waves")
        return removed

    def status(self) -> Dict[str, Any]:
        """에테르 상태 보고"""
        return {
            "total_waves": len(self._waves),
            "listener_frequencies": list(self._listeners.keys()),
            "listener_count": sum(len(cbs) for cbs in self._listeners.values()),
            "recent_waves": len(self.get_recent_waves(10.0)),
            "average_amplitude": sum(w.amplitude for w in self._waves) / len(self._waves) if self._waves else 0.0
        }

    def reset(self) -> None:
        """에테르 초기화 (테스트용)"""
        self._waves.clear()
        self._listeners.clear()
        logger.info("🌌 Ether Reset.")


# 전역 싱글톤 인스턴스
ether = Ether()


def get_ether() -> Ether:
    """전역 Ether 인스턴스 가져오기"""
    return ether


def emit_wave(
    sender: str,
    frequency: float,
    amplitude: float = 1.0,
    phase: str = WavePhase.THOUGHT.value,
    payload: Any = None
) -> Wave:
    """편의 함수: 파동 생성 및 방출"""
    wave = Wave(
        sender=sender,
        frequency=frequency,
        amplitude=amplitude,
        phase=phase,
        payload=payload
    )
    ether.emit(wave)
    return wave
