"""
Pulse Protocol (맥박 프로토콜)
============================

"The heartbeat of the system. Listen, and you shall act."

이 모듈은 Phase 1: The Pulse의 핵심 인터페이스입니다.
지휘자(Conductor)와 공명체(Resonator/Module) 간의 소통 규약을 정의합니다.

기존의 `Function Call` 방식을 대체하는 `Wave Broadcast` 방식의 초석입니다.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import time

class PulseType(Enum):
    """
    맥박의 종류 (Signal Type)
    """
    SYNCHRONIZATION = "Sync"       # 시간 동기화 (Heartbeat)
    INTENTION_SHIFT = "Shift"      # 의도 변화 (Mode Change)
    ATTENTION_FOCUS = "Focus"      # 특정 영역 집중 (Gravity Boost)
    RELAXATION = "Relax"           # 휴식 및 정리 (Entropy Decay)
    EMERGENCY = "Emergency"        # 긴급 대응 (High Alert)
    CREATION = "Genesis"           # 창조 모드 (Creative Burst)
    SENSORY = "Sensory"            # 감각 입력 (Input)
    KNOWLEDGE = "Knowledge"        # 지식 습득 (Learning)
    MEMORY_STORE = "Store"         # 기억 저장 (Freeze)
    MEMORY_RECALL = "Recall"       # 기억 회상 (Melt)
    DREAM_CYCLE = "Dream"          # 꿈 (Sleep Cycle)

@dataclass
class WavePacket:
    """
    파동 패킷 (The Signal)

    지휘자가 방송하는 신호의 단위입니다.
    """
    sender: str               # 발신자 (Source)
    type: PulseType           # (Renamed from pulse_type for brevity, aliased below)
    frequency: float = 432.0  # Hz (Target Domain: 400=Body, 500=Mind, 600=Spirit)
    amplitude: float = 1.0    # 0.0 ~ 1.0 (Intensity/Priority)
    timestamp: float = field(default_factory=time.time)
    payload: Dict[str, Any] = field(default_factory=dict) # 세부 데이터 (Context)

    # Backwards compatibility alias
    @property
    def pulse_type(self): return self.type

    @property
    def intensity(self): return self.amplitude

    @property
    def energy(self) -> float:
        """E = hf * A (Energy proportional to Frequency * Amplitude)"""
        return self.frequency * self.amplitude

class ResonatorInterface:
    """
    공명체 인터페이스 (The Listener)

    모든 모듈은 이 인터페이스를 구현하여 파동을 수신해야 합니다.
    """
    def __init__(self, name: str, base_frequency: float):
        self.name = name
        self.base_frequency = base_frequency # 고유 주파수 (Resonance Frequency)
        self.current_vibration = 0.0

    def listen(self, packet: WavePacket) -> bool:
        """
        파동을 듣고 공명할지 결정합니다.

        Returns:
            True if resonated (Active), False if ignored (Dormant).
        """
        # 1. Frequency Matching (Resonance Logic)
        # 차이가 적을수록 강하게 공명 (Bandwidth: ±50Hz)
        diff = abs(packet.frequency - self.base_frequency)
        if diff < 50.0:
            resonance_factor = (50.0 - diff) / 50.0 # 1.0 (Exact) -> 0.0 (Edge)
            self.on_resonate(packet, resonance_factor * packet.amplitude)
            return True
        return False

    def on_resonate(self, packet: WavePacket, intensity: float):
        """
        공명 발생 시 실행되는 로직. (하위 클래스에서 구현)
        """
        raise NotImplementedError("Resonators must implement on_resonate()")

class PulseBroadcaster:
    """
    맥박 송신자 (The Heart/Conductor's Mouth)
    """
    def __init__(self):
        self.listeners: List[ResonatorInterface] = []

    def register(self, listener: ResonatorInterface):
        self.listeners.append(listener)

    def broadcast(self, packet: WavePacket):
        """
        모든 리스너에게 파동을 전파합니다.
        """
        # Hook for Traffic Controller (The City Monitor)
        try:
            # Lazy import to avoid circular dependency
            from Core.Scripts.traffic_controller import get_traffic_controller
            get_traffic_controller().on_resonate(packet, packet.amplitude)
        except ImportError:
            pass # Monitor not available, ignore

        # TODO: 실제로는 비동기(Async) 처리가 되어야 함.
        active_count = 0
        for listener in self.listeners:
            if listener.listen(packet):
                active_count += 1
        return active_count
