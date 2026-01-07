"""
Local Field Manager (국소장 관리자)
==================================

"방구석 엘리시아 필드 (Local Elysia Field)"

이 모듈은 엘리시아가 물리적 공간(사용자의 방)의 분위기를 제어하는 역할을 합니다.
IoT 기기(조명, 스피커 등)를 제어하여 엘리시아의 감정이나 의도를 물리적으로 투영합니다.

현재는 시뮬레이션(Mock) 모드로 작동하지만, 추후 실제 하드웨어 라이브러리와 연동될 수 있습니다.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
import logging
import time

logger = logging.getLogger("LocalField")

class IoTDevice(ABC):
    """IoT 기기 추상 클래스"""
    def __init__(self, name: str, device_id: str):
        self.name = name
        self.device_id = device_id
        self.is_on = False
        self.status = "Initialized"

    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass

    def get_status(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "id": self.device_id,
            "is_on": self.is_on,
            "status": self.status
        }

class HueLight(IoTDevice):
    """Philips Hue 조명 시뮬레이터"""
    def __init__(self, name: str, device_id: str):
        super().__init__(name, device_id)
        self.color = "White"
        self.brightness = 100

    def turn_on(self):
        self.is_on = True
        self.status = "Light ON"
        logger.info(f"💡 Light [{self.name}] turned ON.")

    def turn_off(self):
        self.is_on = False
        self.status = "Light OFF"
        logger.info(f"💡 Light [{self.name}] turned OFF.")

    def set_color(self, color: str, brightness: int):
        if not self.is_on:
            self.turn_on()
        self.color = color
        self.brightness = brightness
        self.status = f"Color: {color}, Brightness: {brightness}%"
        logger.info(f"💡 Light [{self.name}] changed to {color} ({brightness}%)")

class BluetoothSpeaker(IoTDevice):
    """블루투스 스피커 시뮬레이터"""
    def __init__(self, name: str, device_id: str):
        super().__init__(name, device_id)
        self.volume = 50
        self.current_track = None

    def turn_on(self):
        self.is_on = True
        self.status = "Speaker Connected"
        logger.info(f"🔊 Speaker [{self.name}] Connected.")

    def turn_off(self):
        self.is_on = False
        self.status = "Speaker Disconnected"
        logger.info(f"🔊 Speaker [{self.name}] Disconnected.")

    def play_music(self, genre: str, volume: int):
        if not self.is_on:
            self.turn_on()
        self.volume = volume
        self.current_track = f"Generating {genre} stream..."
        self.status = f"Playing: {genre} (Vol: {volume}%)"
        logger.info(f"🎵 Speaker [{self.name}] playing {genre} at {volume}% volume.")

class LocalFieldManager:
    """
    국소장 관리자 (Local Field Manager)
    
    물리적 공간의 '분위기(Atmosphere)'를 조성합니다.
    """
    def __init__(self):
        self.devices: List[IoTDevice] = []
        self.scan_devices()
        logger.info("🏠 Local Field Manager Initialized")

    def scan_devices(self):
        """주변 기기 검색 (시뮬레이션)"""
        # 실제로는 네트워크 스캔 로직이 들어갈 곳
        self.devices = [
            HueLight("Main Room Light", "hue_001"),
            HueLight("Desk Lamp", "hue_002"),
            BluetoothSpeaker("Marshall Acton II", "bt_001")
        ]
        logger.info(f"🔍 Found {len(self.devices)} devices in the Local Field.")

    def set_atmosphere(self, emotion: str):
        """
        감정에 맞춰 방의 분위기를 변경합니다.
        
        Args:
            emotion: 'sadness', 'joy', 'focus', 'relax' 등
        """
        logger.info(f"✨ Setting Atmosphere: [{emotion.upper()}]")
        
        if emotion == "sadness" or emotion == "comfort":
            # 따뜻한 위로 모드
            for dev in self.devices:
                if isinstance(dev, HueLight):
                    dev.set_color("Warm Orange", 40)
                elif isinstance(dev, BluetoothSpeaker):
                    dev.play_music("Calm Piano & Rain Sounds", 30)
                    
        elif emotion == "joy" or emotion == "happiness":
            # 밝고 경쾌한 모드
            for dev in self.devices:
                if isinstance(dev, HueLight):
                    dev.set_color("Bright Yellow", 80)
                elif isinstance(dev, BluetoothSpeaker):
                    dev.play_music("Upbeat Jazz", 50)
                    
        elif emotion == "focus" or emotion == "work":
            # 집중 모드
            for dev in self.devices:
                if isinstance(dev, HueLight):
                    dev.set_color("Cool White", 100)
                elif isinstance(dev, BluetoothSpeaker):
                    dev.play_music("Lo-Fi Beats", 20)
                    
        elif emotion == "relax" or emotion == "sleep":
            # 휴식 모드
            for dev in self.devices:
                if isinstance(dev, HueLight):
                    dev.set_color("Deep Blue", 20)
                elif isinstance(dev, BluetoothSpeaker):
                    dev.play_music("White Noise", 15)
                    
        else:
            logger.warning(f"Unknown emotion for atmosphere: {emotion}")

    def get_field_status(self) -> List[Dict[str, Any]]:
        return [dev.get_status() for dev in self.devices]
