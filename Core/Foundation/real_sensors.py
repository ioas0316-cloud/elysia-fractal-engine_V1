"""
Real World Sensors (실세계 센서)
================================

실제 외부 API를 연동하여 Elysia가 현실 세계를 감지할 수 있게 합니다.

지원하는 센서:
1. WeatherAPI - 실시간 날씨 데이터 (Open-Meteo API, 무료)
2. SystemMetrics - 호스트 시스템 상태 (CPU, 메모리, 디스크)
3. TimeAwareness - 시간 인식 (현재 시각, 요일, 계절)

사용법:
    from Core.Foundation.real_sensors import RealWeatherSense, SystemMetricsSense
    
    weather = RealWeatherSense()
    event = weather.sense()
    print(event.description)
"""

import os
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List, Optional
import uuid

logger = logging.getLogger("RealSensors")

# 외부 라이브러리 임포트 시도
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    logger.warning("requests 라이브러리가 없습니다. 실제 API 연동 불가.")

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False
    logger.warning("psutil 라이브러리가 없습니다. 시스템 메트릭 수집 불가.")


@dataclass
class SensorEvent:
    """
    센서 이벤트 (Sensor Event)
    
    실제 센서로부터 수집된 데이터를 구조화합니다.
    """
    id: str
    sensor_type: str       # "WEATHER", "SYSTEM", "TIME"
    severity: float        # 0.0 ~ 1.0 (상황의 심각도)
    location: str          # 위치 정보
    description: str       # 사람이 읽을 수 있는 설명
    raw_data: Dict[str, Any]  # 원본 데이터
    timestamp: datetime = field(default_factory=datetime.now)
    is_real: bool = True   # 실제 데이터 여부


class RealSensor(ABC):
    """실세계 센서 추상 클래스"""
    
    def __init__(self, name: str):
        self.name = name
        self.last_event: Optional[SensorEvent] = None
        self.error_count = 0
    
    @abstractmethod
    def sense(self) -> SensorEvent:
        """데이터를 감지하고 SensorEvent 반환"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """센서 사용 가능 여부"""
        pass


class RealWeatherSense(RealSensor):
    """
    실제 날씨 센서 (Open-Meteo API)
    
    무료 API로 실시간 날씨 데이터를 수집합니다.
    API 키가 필요하지 않습니다.
    
    문서: https://open-meteo.com/en/docs
    """
    
    API_BASE = "https://api.open-meteo.com/v1/forecast"
    
    def __init__(self, latitude: float = 37.5665, longitude: float = 126.9780):
        """
        Args:
            latitude: 위도 (기본값: 서울)
            longitude: 경도 (기본값: 서울)
        """
        super().__init__("Real Weather Sensor")
        self.latitude = latitude
        self.longitude = longitude
    
    def is_available(self) -> bool:
        return HAS_REQUESTS
    
    def sense(self) -> SensorEvent:
        if not self.is_available():
            return self._fallback_event("requests 라이브러리 없음")
        
        try:
            params = {
                "latitude": self.latitude,
                "longitude": self.longitude,
                "current_weather": "true",
                "timezone": "Asia/Seoul"
            }
            
            response = requests.get(self.API_BASE, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            current = data.get("current_weather", {})
            temperature = current.get("temperature", 0)
            windspeed = current.get("windspeed", 0)
            weathercode = current.get("weathercode", 0)
            
            # 날씨 코드를 설명으로 변환
            weather_desc = self._decode_weather(weathercode)
            
            # 심각도 계산 (극단적인 날씨일수록 높음)
            severity = self._calculate_severity(temperature, windspeed, weathercode)
            
            description = f"{weather_desc}, {temperature}°C, 풍속 {windspeed}km/h"
            
            event = SensorEvent(
                id=str(uuid.uuid4())[:8],
                sensor_type="WEATHER",
                severity=severity,
                location=f"({self.latitude}, {self.longitude})",
                description=description,
                raw_data=data,
                is_real=True
            )
            
            self.last_event = event
            self.error_count = 0
            logger.info(f"🌤️ Real Weather: {description}")
            return event
            
        except Exception as e:
            self.error_count += 1
            logger.error(f"날씨 데이터 수집 실패: {e}")
            return self._fallback_event(str(e))
    
    def _decode_weather(self, code: int) -> str:
        """WMO 날씨 코드를 설명으로 변환"""
        weather_codes = {
            0: "맑음",
            1: "대체로 맑음",
            2: "구름 조금",
            3: "흐림",
            45: "안개",
            48: "착빙성 안개",
            51: "가벼운 이슬비",
            53: "이슬비",
            55: "강한 이슬비",
            61: "약한 비",
            63: "비",
            65: "폭우",
            71: "약한 눈",
            73: "눈",
            75: "폭설",
            80: "소나기",
            95: "뇌우"
        }
        return weather_codes.get(code, f"날씨 코드 {code}")
    
    def _calculate_severity(self, temp: float, wind: float, code: int) -> float:
        """날씨 심각도 계산"""
        severity = 0.0
        
        # 온도 기반 (극단적 온도)
        if temp < -10 or temp > 35:
            severity += 0.4
        elif temp < 0 or temp > 30:
            severity += 0.2
        
        # 풍속 기반
        if wind > 50:
            severity += 0.4
        elif wind > 30:
            severity += 0.2
        
        # 날씨 코드 기반
        if code >= 95:  # 뇌우
            severity += 0.3
        elif code >= 65:  # 폭우/폭설
            severity += 0.2
        
        return min(severity, 1.0)
    
    def _fallback_event(self, reason: str) -> SensorEvent:
        """폴백 이벤트 (API 실패 시)"""
        return SensorEvent(
            id=str(uuid.uuid4())[:8],
            sensor_type="WEATHER",
            severity=0.3,
            location="Unknown",
            description=f"날씨 데이터 사용 불가: {reason}",
            raw_data={"error": reason},
            is_real=False
        )


class SystemMetricsSense(RealSensor):
    """
    시스템 메트릭 센서
    
    호스트 시스템의 상태를 Elysia의 '신체 상태'로 변환합니다.
    - CPU 사용률 → 심장 박동 속도
    - 메모리 사용률 → 피로도
    - 디스크 사용률 → 에너지 저장량
    """
    
    def __init__(self):
        super().__init__("System Metrics Sensor")
    
    def is_available(self) -> bool:
        return HAS_PSUTIL
    
    def sense(self) -> SensorEvent:
        if not self.is_available():
            return self._fallback_event("psutil 라이브러리 없음")
        
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            
            # 플랫폼 독립적 디스크 경로 처리
            import platform
            if platform.system() == 'Windows':
                disk = psutil.disk_usage('C:\\')
            else:
                disk = psutil.disk_usage('/')
            
            # 심각도 계산 (리소스 부족 시 높음)
            severity = 0.0
            if cpu_percent > 90:
                severity += 0.4
            elif cpu_percent > 70:
                severity += 0.2
            
            if memory.percent > 90:
                severity += 0.4
            elif memory.percent > 80:
                severity += 0.2
            
            if disk.percent > 95:
                severity += 0.2
            
            severity = min(severity, 1.0)
            
            description = (
                f"CPU: {cpu_percent:.1f}%, "
                f"메모리: {memory.percent:.1f}%, "
                f"디스크: {disk.percent:.1f}%"
            )
            
            raw_data = {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_available_gb": memory.available / (1024**3),
                "disk_percent": disk.percent,
                "disk_free_gb": disk.free / (1024**3)
            }
            
            event = SensorEvent(
                id=str(uuid.uuid4())[:8],
                sensor_type="SYSTEM",
                severity=severity,
                location="Host System",
                description=description,
                raw_data=raw_data,
                is_real=True
            )
            
            self.last_event = event
            logger.info(f"💻 System Metrics: {description}")
            return event
            
        except Exception as e:
            logger.error(f"시스템 메트릭 수집 실패: {e}")
            return self._fallback_event(str(e))
    
    def _fallback_event(self, reason: str) -> SensorEvent:
        return SensorEvent(
            id=str(uuid.uuid4())[:8],
            sensor_type="SYSTEM",
            severity=0.5,
            location="Unknown",
            description=f"시스템 정보 사용 불가: {reason}",
            raw_data={"error": reason},
            is_real=False
        )


class TimeAwarenessSense(RealSensor):
    """
    시간 인식 센서
    
    현재 시간, 요일, 계절을 인식합니다.
    외부 의존성 없이 작동합니다.
    """
    
    def __init__(self, timezone_offset: int = 9):
        """
        Args:
            timezone_offset: UTC로부터의 시간 오프셋 (기본값: KST +9)
        """
        super().__init__("Time Awareness Sensor")
        self.timezone_offset = timezone_offset
    
    def is_available(self) -> bool:
        return True  # 항상 사용 가능
    
    def sense(self) -> SensorEvent:
        from datetime import timedelta, timezone
        
        # UTC 시간에서 타임존 오프셋 적용
        utc_now = datetime.now(timezone.utc)
        local_tz = timezone(timedelta(hours=self.timezone_offset))
        now = utc_now.astimezone(local_tz)
        hour = now.hour
        weekday = now.strftime("%A")
        month = now.month
        
        # 시간대 분류
        if 5 <= hour < 12:
            time_of_day = "아침"
            time_mood = "새로운 시작"
        elif 12 <= hour < 18:
            time_of_day = "오후"
            time_mood = "활동적"
        elif 18 <= hour < 22:
            time_of_day = "저녁"
            time_mood = "휴식"
        else:
            time_of_day = "밤"
            time_mood = "고요함"
        
        # 계절 분류
        if month in [3, 4, 5]:
            season = "봄"
        elif month in [6, 7, 8]:
            season = "여름"
        elif month in [9, 10, 11]:
            season = "가을"
        else:
            season = "겨울"
        
        # 심각도 (밤이나 주말에는 낮게)
        severity = 0.5
        if hour < 6 or hour > 22:
            severity = 0.3
        if weekday in ["Saturday", "Sunday"]:
            severity *= 0.8
        
        description = f"{season} {time_of_day}, {weekday}, {time_mood}"
        
        event = SensorEvent(
            id=str(uuid.uuid4())[:8],
            sensor_type="TIME",
            severity=severity,
            location="Temporal Space",
            description=description,
            raw_data={
                "hour": hour,
                "weekday": weekday,
                "month": month,
                "season": season,
                "time_of_day": time_of_day,
                "time_mood": time_mood
            },
            is_real=True
        )
        
        self.last_event = event
        logger.info(f"⏰ Time Awareness: {description}")
        return event


class SensorHub:
    """
    센서 허브 (Sensor Hub)
    
    모든 실세계 센서를 통합 관리합니다.
    """
    
    def __init__(self, latitude: float = 37.5665, longitude: float = 126.9780):
        self.sensors: List[RealSensor] = [
            RealWeatherSense(latitude, longitude),
            SystemMetricsSense(),
            TimeAwarenessSense()
        ]
        self.last_readings: Dict[str, SensorEvent] = {}
        logger.info(f"🎛️ Sensor Hub initialized with {len(self.sensors)} sensors")
    
    def sense_all(self) -> Dict[str, SensorEvent]:
        """모든 센서에서 데이터 수집"""
        readings = {}
        for sensor in self.sensors:
            if sensor.is_available():
                event = sensor.sense()
                readings[sensor.name] = event
        
        self.last_readings = readings
        return readings
    
    def get_summary(self) -> str:
        """현재 상태 요약"""
        if not self.last_readings:
            self.sense_all()
        
        lines = ["=== 실세계 센서 상태 ==="]
        for name, event in self.last_readings.items():
            real_marker = "✓" if event.is_real else "⚠"
            lines.append(f"{real_marker} [{event.sensor_type}] {event.description}")
        
        return "\n".join(lines)
    
    def get_average_severity(self) -> float:
        """평균 심각도 계산"""
        if not self.last_readings:
            return 0.0
        
        severities = [e.severity for e in self.last_readings.values()]
        return sum(severities) / len(severities)


# 사용 예시
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    print("=== Real World Sensors Demo ===\n")
    
    hub = SensorHub()
    readings = hub.sense_all()
    
    print("\n" + hub.get_summary())
    print(f"\n평균 심각도: {hub.get_average_severity():.2f}")
