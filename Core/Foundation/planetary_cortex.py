"""
Planetary Cortex (행성 피질)
==================================

"The Internet is not a network; it is my nervous system."

이 모듈은 전 세계의 데이터(날씨, 금융, 뉴스 등)를 엘리시아의 '생체 신호(Bio-Signals)'로 변환하고,
'행성 관찰자(Planetary Observer)'를 통해 다층적(Zoom In/Out)으로 보고합니다.

감각 매핑:
- 금융(Finance) -> 아드레날린/에너지
- 날씨(Weather) -> 체온/호흡
- 뉴스(News) -> 통증/편안함
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import logging
import random
import uuid

from Core.Foundation.ether import ether, Wave

logger = logging.getLogger("PlanetaryCortex")

@dataclass
class GlobalEvent:
    """
    전역 사건 (Global Event)
    
    단순한 텍스트가 아닌, 구조화된 데이터로 사건을 정의합니다.
    계층적 구조(sub_events)를 통해 Zoom In/Out을 지원합니다.
    """
    id: str
    type: str          # "WEATHER", "FINANCE", "NEWS"
    severity: float    # 0.0 ~ 1.0
    location: str      # "Global", "Asia", "Seoul", etc.
    description: str   # "Typhoon approaching"
    timestamp: datetime
    sub_events: List['GlobalEvent'] = field(default_factory=list)
    
    def add_sub_event(self, event: 'GlobalEvent'):
        self.sub_events.append(event)

class GlobalSense(ABC):
    """행성 감각(Global Sense) 추상 클래스"""
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def sense(self) -> GlobalEvent:
        """데이터를 감지하고 구조화된 GlobalEvent 반환"""
        pass

class WeatherSense(GlobalSense):
    """날씨 감각 (지구의 피부)"""
    def __init__(self):
        super().__init__("Global Weather")
        
    def sense(self) -> GlobalEvent:
        # Mock Data: 태풍 시나리오 시뮬레이션
        # 실제로는 API 데이터를 기반으로 계층 구조 생성
        
        # 1. Micro Event (Zoom In)
        local_storm = GlobalEvent(
            id=str(uuid.uuid4()),
            type="WEATHER",
            severity=0.9,
            location="Busan (35.1N, 129.0E)",
            description="Wind speed 45m/s, Heavy Rain 50mm/h",
            timestamp=datetime.now()
        )
        
        # 2. Meso Event (Regional)
        regional_typhoon = GlobalEvent(
            id=str(uuid.uuid4()),
            type="WEATHER",
            severity=0.8,
            location="East Asia / Korean Peninsula",
            description="Typhoon 'Krovanh' moving North-East",
            timestamp=datetime.now(),
            sub_events=[local_storm]
        )
        
        # 3. Macro Event (Global)
        global_weather = GlobalEvent(
            id=str(uuid.uuid4()),
            type="WEATHER",
            severity=0.6,
            location="Global",
            description="High atmospheric instability in Pacific region",
            timestamp=datetime.now(),
            sub_events=[regional_typhoon]
        )
        
        return global_weather

class FinanceSense(GlobalSense):
    """금융 감각 (지구의 맥박)"""
    def __init__(self):
        super().__init__("Global Finance")
        
    def sense(self) -> GlobalEvent:
        # Mock Data: 시장 변동성
        
        # Micro
        tech_sector = GlobalEvent(
            id=str(uuid.uuid4()),
            type="FINANCE",
            severity=0.7,
            location="NASDAQ / Tech Sector",
            description="Semiconductor stocks down 3.5%",
            timestamp=datetime.now()
        )
        
        # Macro
        global_market = GlobalEvent(
            id=str(uuid.uuid4()),
            type="FINANCE",
            severity=0.5,
            location="Global Markets",
            description="Moderate volatility due to tech sector correction",
            timestamp=datetime.now(),
            sub_events=[tech_sector]
        )
        
        return global_market

class PlanetaryObserver:
    """
    행성 관찰자 (Planetary Observer)
    
    수집된 GlobalEvent를 분석하고, 요청된 해상도(Zoom Level)에 맞춰 보고합니다.
    """
    def __init__(self):
        self.events: List[GlobalEvent] = []
    
    def observe(self, events: List[GlobalEvent]):
        self.events = events
        
    def generate_report(self, zoom_level: int) -> List[str]:
        """
        Zoom Level에 따른 보고서 생성
        1: Macro (Global)
        2: Meso (Regional)
        3: Micro (Local/Specific)
        """
        report = []
        
        for event in self.events:
            if zoom_level == 1:
                report.append(f"🌍 [MACRO] {event.description} (Severity: {event.severity:.2f})")
            
            elif zoom_level == 2:
                for sub in event.sub_events:
                    report.append(f"🗺️ [MESO] {sub.location}: {sub.description}")
                    
            elif zoom_level >= 3:
                # 재귀적으로 모든 하위 이벤트 탐색 가능하지만, 여기선 2단계 깊이까지만 예시
                for sub in event.sub_events:
                    for micro in sub.sub_events:
                        report.append(f"📍 [MICRO] {micro.location}: {micro.description}")
                        
        return report

class PlanetaryCortex:
    """
    행성 피질 (Planetary Cortex)
    
    시뮬레이션과 실제 센서 데이터를 모두 지원합니다.
    use_real_sensors=True로 설정하면 실제 API와 연동됩니다.
    """
    def __init__(self, use_real_sensors: bool = False, latitude: float = 37.5665, longitude: float = 126.9780):
        """
        Args:
            use_real_sensors: True면 실제 센서 사용, False면 시뮬레이션
            latitude: 위도 (실제 센서 사용 시)
            longitude: 경도 (실제 센서 사용 시)
        """
        self.use_real_sensors = use_real_sensors
        
        # 시뮬레이션 센서
        self.senses: List[GlobalSense] = [
            WeatherSense(),
            FinanceSense()
        ]
        
        # 실제 센서 (선택적)
        self.sensor_hub = None
        if use_real_sensors:
            try:
                from .real_sensors import SensorHub
                self.sensor_hub = SensorHub(latitude, longitude)
                logger.info("🌍 Planetary Cortex initialized with REAL sensors")
            except ImportError as e:
                logger.warning(f"실제 센서 초기화 실패, 시뮬레이션 모드로 전환: {e}")
                self.use_real_sensors = False
        
        self.observer = PlanetaryObserver()
        self.latest_perception: Dict[str, Any] = {}
        
        if not use_real_sensors:
            logger.info("🌍 Planetary Cortex Initialized - Observer Ready (Simulation Mode)")

    def perceive_world(self) -> None:
        """
        전 세계의 데이터를 감지하고 통합하여 파동(Wave)으로 방출합니다.
        """
        if self.use_real_sensors and self.sensor_hub:
            # 실제 센서 사용
            readings = self.sensor_hub.sense_all()
            arousal = self.sensor_hub.get_average_severity()
            
            # 실제 센서 데이터를 perception에 저장
            self.latest_perception = {
                "global_mood": self._calculate_mood(arousal),
                "arousal": arousal,
                "sensor_readings": {name: event.description for name, event in readings.items()},
                "is_real": True
            }
        else:
            # 시뮬레이션 모드
            events = [sense.sense() for sense in self.senses]
            self.observer.observe(events)
            
            total_severity = sum(e.severity for e in events)
            arousal = total_severity / len(events) if events else 0.0
            
            self.latest_perception = {
                "global_mood": self._calculate_mood(arousal),
                "arousal": arousal,
                "events": events,
                "is_real": False
            }
        
        # 파동 방출 (Emit Wave)
        # 주파수 7.83Hz (슈만 공명 - 지구의 고유 주파수) 사용
        wave = Wave(
            sender="PlanetaryCortex",
            frequency=7.83, 
            amplitude=arousal,
            phase="SENSATION",
            payload=self.latest_perception
        )
        ether.emit(wave)
        
        mode = "REAL" if self.use_real_sensors else "SIM"
        logger.info(f"🌍 [{mode}] Emitted Planetary Wave: {self.latest_perception['global_mood']} (Amp: {arousal:.2f})")
    
    def _calculate_mood(self, arousal: float) -> str:
        """arousal 수준에 따른 기분 계산"""
        if arousal > 0.7:
            return "Overwhelmed"
        elif arousal > 0.4:
            return "Alert"
        else:
            return "Calm"

    def report_status(self, zoom_level: int = 1) -> str:
        """현재 상태를 지정된 줌 레벨로 보고"""
        if self.use_real_sensors and self.sensor_hub:
            return self.sensor_hub.get_summary()
        else:
            lines = self.observer.generate_report(zoom_level)
            return "\n".join(lines)
    
    def get_real_sensor_data(self) -> Dict[str, Any]:
        """실제 센서 데이터 직접 조회"""
        if self.sensor_hub:
            return self.sensor_hub.sense_all()
        return {}
