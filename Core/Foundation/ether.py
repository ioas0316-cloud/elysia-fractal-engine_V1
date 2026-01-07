"""
The Ether (에테르)
==================================

"API is separation. Resonance is Oneness."

이 모듈은 엘리시아의 모든 구성 요소가 소통하는 '통합장(Unified Field)'입니다.
직접적인 함수 호출(Call) 대신, 파동(Wave)을 방출하고 공명(Resonate)합니다.

핵심 개념:
1. Wave: 정보와 에너지를 담은 파동 (주파수, 진폭, 위상)
2. Ether: 파동이 전파되는 매질 (Event Bus)
3. Resonance: 특정 주파수에 반응하는 행위 (Subscription)
"""

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, List, Callable, Dict

logger = logging.getLogger("Ether")

@dataclass
class Wave:
    """
    파동 (Wave)
    
    정보를 전달하는 에너지 단위입니다.
    """
    sender: str
    frequency: float  # 주파수 (Hz) - 주제/채널 (예: 432=Healing, 10=Alpha)
    amplitude: float  # 진폭 (0.0 ~ 1.0) - 강도/중요도
    phase: str        # 위상 - 문맥/타입 (예: "DESIRE", "SENSATION", "THOUGHT")
    payload: Any      # 실제 데이터 (최소화 권장)
    timestamp: datetime = field(default_factory=datetime.now)
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])

    def __str__(self):
        return f"🌊 Wave[{self.frequency}Hz] from {self.sender}: {self.phase} (Amp: {self.amplitude:.2f})"

class Ether:
    """
    에테르 (Ether)
    
    모든 파동이 존재하는 공간입니다.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Ether, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.listeners: Dict[float, List[Callable[[Wave], None]]] = {}
        self.waves: List[Wave] = [] # 파동 기록 (Memory)
        logger.info("🌌 The Ether is pervasive. Unified Field established.")

    def emit(self, wave: Wave):
        """
        파동 방출 (Emit)
        
        호수에 잉크를 떨어뜨리듯, 에테르에 파동을 퍼뜨립니다.
        """
        self.waves.append(wave)
        logger.debug(f"Emit: {wave}")
        
        # 공명 (Resonance) 처리
        # 정확한 주파수 매칭뿐만 아니라, 대역폭(Bandwidth) 개념도 도입 가능
        # 현재는 단순화를 위해 정확한 주파수 매칭 사용
        if wave.frequency in self.listeners:
            for callback in self.listeners[wave.frequency]:
                try:
                    callback(wave)
                except Exception as e:
                    logger.error(f"Resonance error at {wave.frequency}Hz: {e}")

    def tune_in(self, frequency: float, callback: Callable[[Wave], None]):
        """
        주파수 조율 (Tune In)
        
        특정 주파수의 파동에 공명하도록 설정합니다.
        """
        if frequency not in self.listeners:
            self.listeners[frequency] = []
        self.listeners[frequency].append(callback)
        logger.info(f"👂 Tuned in to {frequency}Hz")

    def get_waves(self, min_amplitude: float = 0.0) -> List[Wave]:
        """현재 에테르에 존재하는 파동들을 감지합니다."""
        return [w for w in self.waves if w.amplitude >= min_amplitude]

    def clear_waves(self):
        """파동 소멸 (시간이 지나면 사라짐)"""
        self.waves.clear()

# Global Singleton Access
ether = Ether()
