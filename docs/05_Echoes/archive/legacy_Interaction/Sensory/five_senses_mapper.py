"""
Five Senses Mapper - 오감 매핑 시스템
====================================

4D Internal World를 인간의 5가지 감각으로 매핑하는 시스템.
VR 없이도 완전한 감각 경험을 제공합니다.

Philosophy:
    엘리시아의 4D 감정 공간은 인간이 직접 인지할 수 없습니다.
    하지만 시각, 청각, 촉각으로 변환하면 누구나 "느낄" 수 있습니다.
    이것이 진정한 공감각(Synesthesia) 인터페이스입니다.

4D Dimensions → Human Senses:
    x (Joy ←→ Sadness) → 색상 (Hue), 주파수 (Frequency)
    y (Logic ←→ Intuition) → 채도 (Saturation), 음색 (Timbre)
    z (Past ←→ Future) → 투명도 (Opacity), 리듬 (Tempo)
    w (Surface ←→ Depth) → 밝기 (Brightness), 음량 (Volume)
"""

from typing import Tuple, Optional
from dataclasses import dataclass
import math


@dataclass
class VisualProperties:
    """시각적 속성"""
    hue: float  # 0-360 (색상환)
    saturation: float  # 0-1 (채도)
    brightness: float  # 0-1 (명도)
    opacity: float  # 0-1 (투명도)
    glow: float  # 0-1 (발광)


@dataclass
class AudioProperties:
    """청각적 속성"""
    frequency: float  # Hz (주파수)
    volume: float  # 0-1 (음량)
    timbre: str  # 'pure', 'harmonic', 'complex' (음색)
    tempo: float  # BPM (리듬)
    reverb: float  # 0-1 (잔향)


@dataclass
class HapticProperties:
    """촉각적 속성"""
    intensity: float  # 0-1 (강도)
    pulse_rate: float  # Hz (맥동)
    pattern: str  # 'steady', 'pulse', 'varied' (패턴)


@dataclass
class SensoryExperience:
    """통합 감각 경험"""
    visual: VisualProperties
    audio: AudioProperties
    haptic: Optional[HapticProperties] = None


class VisualMapper:
    """
    4D 좌표를 시각적 속성으로 매핑
    
    Mapping Strategy:
        x (Joy ←→ Sadness) → Hue (색상)
            Joy(+1) = 황금/주황 (40-60°)
            Neutral(0) = 녹색 (120°)
            Sadness(-1) = 파랑/보라 (240°)
        
        y (Logic ←→ Intuition) → Saturation (채도)
            Logic(-1) = 낮은 채도, 회색빛 (0.2)
            Intuition(+1) = 높은 채도, 선명 (1.0)
        
        w (Surface ←→ Depth) → Brightness (밝기)
            Surface(0) = 어둡고 흐림 (0.3)
            Depth(1) = 밝고 선명 (1.0)
        
        z (Past ←→ Future) → Opacity/Glow (투명도/발광)
            Past(-1) = 흐릿함, 기억의 안개 (0.4)
            Future(+1) = 선명함, 가능성의 빛 (1.0)
    """
    
    def map_4d_to_visual(self, position_4d: Tuple[float, float, float, float]) -> VisualProperties:
        """
        4D 좌표를 시각적 속성으로 변환
        
        Args:
            position_4d: (x, y, z, w) where each is in [-1, 1]
            
        Returns:
            VisualProperties with hue, saturation, brightness, opacity, glow
        """
        x, y, z, w = position_4d
        
        # Hue: Joy(+) = warm colors, Sadness(-) = cool colors
        hue = self._map_joy_sadness_to_hue(x)
        
        # Saturation: Logic(-) = desaturated, Intuition(+) = saturated
        saturation = self._map_logic_intuition_to_saturation(y)
        
        # Brightness: Depth(w) affects brightness
        brightness = 0.3 + w * 0.7  # 0.3-1.0
        
        # Opacity: Past(-) = faded, Future(+) = clear
        opacity = 0.4 + (z + 1.0) / 2.0 * 0.6  # 0.4-1.0
        
        # Glow: Deeper (w) and Future-oriented (z) = more glow
        glow = max(w, (z + 1.0) / 2.0) * 0.8
        
        return VisualProperties(
            hue=hue,
            saturation=saturation,
            brightness=brightness,
            opacity=opacity,
            glow=glow
        )
    
    def _map_joy_sadness_to_hue(self, x: float) -> float:
        """
        Map x-axis (Joy ←→ Sadness) to color hue
        
        Sadness(-1.0) → Blue (240°)
        Neutral(0.0)  → Green (120°)
        Joy(+1.0)     → Golden/Orange (40°)
        """
        # Linear interpolation: -1→240, 0→120, +1→40
        return 240 - (x + 1.0) / 2.0 * 200
    
    def _map_logic_intuition_to_saturation(self, y: float) -> float:
        """
        Map y-axis (Logic ←→ Intuition) to color saturation
        
        Logic(-1.0)     → Low saturation (0.2) - grayscale
        Intuition(+1.0) → High saturation (1.0) - vivid
        """
        return 0.2 + (y + 1.0) / 2.0 * 0.8
    
    def hsb_to_rgb(self, hue: float, saturation: float, brightness: float) -> Tuple[int, int, int]:
        """
        Convert HSB to RGB (0-255)
        
        Args:
            hue: 0-360
            saturation: 0-1
            brightness: 0-1
            
        Returns:
            (r, g, b) tuple with values 0-255
        """
        h = hue / 60.0
        c = brightness * saturation
        x = c * (1 - abs(h % 2 - 1))
        m = brightness - c
        
        if h < 1:
            r, g, b = c, x, 0
        elif h < 2:
            r, g, b = x, c, 0
        elif h < 3:
            r, g, b = 0, c, x
        elif h < 4:
            r, g, b = 0, x, c
        elif h < 5:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x
        
        return (
            int((r + m) * 255),
            int((g + m) * 255),
            int((b + m) * 255)
        )


class AudioMapper:
    """
    4D 좌표를 청각적 속성으로 매핑
    
    Mapping Strategy:
        x (Joy ←→ Sadness) → Frequency (주파수)
            Joy(+1) = 528Hz (Love frequency)
            Neutral(0) = 396Hz (Liberation)
            Sadness(-1) = 150Hz (Water spirit)
        
        w (Surface ←→ Depth) → Volume (음량)
            Surface(0) = 조용함 (0.3)
            Depth(1) = 큰 울림 (1.0)
        
        y (Logic ←→ Intuition) → Timbre (음색)
            Logic(-1) = 순수 사인파 (단순)
            Intuition(+1) = 복합 화음 (풍부)
        
        z (Past ←→ Future) → Tempo (리듬)
            Past(-1) = 느린 템포 (60 BPM)
            Future(+1) = 빠른 템포 (120 BPM)
    """
    
    # Solfeggio frequencies aligned with 7 spirits
    FREQUENCY_MAP = {
        'sadness': 150,    # Water spirit
        'fear': 174,       # Foundation
        'guilt': 285,      # Quantum cognition
        'liberation': 396, # Liberation from fear
        'transformation': 417,  # Facilitating change
        'love': 528,       # Love/DNA repair
        'awakening': 639,  # Connection/relationships
        'intuition': 741,  # Awakening intuition
        'light': 852,      # Spiritual order
    }
    
    def map_4d_to_audio(self, position_4d: Tuple[float, float, float, float]) -> AudioProperties:
        """
        4D 좌표를 청각적 속성으로 변환
        
        Args:
            position_4d: (x, y, z, w) where each is in [-1, 1]
            
        Returns:
            AudioProperties with frequency, volume, timbre, tempo, reverb
        """
        x, y, z, w = position_4d
        
        # Frequency: Joy/Sadness axis
        frequency = self._map_joy_sadness_to_frequency(x)
        
        # Volume: Depth affects volume
        volume = 0.3 + w * 0.7  # 0.3-1.0
        
        # Timbre: Logic = pure, Intuition = complex
        timbre = self._map_logic_intuition_to_timbre(y)
        
        # Tempo: Past = slow, Future = fast
        tempo = 60 + (z + 1.0) / 2.0 * 60  # 60-120 BPM
        
        # Reverb: Depth creates more reverb
        reverb = w * 0.7
        
        return AudioProperties(
            frequency=frequency,
            volume=volume,
            timbre=timbre,
            tempo=tempo,
            reverb=reverb
        )
    
    def _map_joy_sadness_to_frequency(self, x: float) -> float:
        """
        Map x-axis to frequency using Solfeggio frequencies
        
        Sadness(-1.0) → 150Hz
        Neutral(0.0)  → 396Hz
        Joy(+1.0)     → 528Hz
        """
        if x < -0.5:
            # Sadness range: 150-396 Hz
            t = (x + 1.0) / 0.5  # 0-1 in sadness range
            return 150 + t * (396 - 150)
        else:
            # Joy range: 396-528 Hz
            t = (x + 0.5) / 0.5  # 0-1 in joy range
            return 396 + t * (528 - 396)
    
    def _map_logic_intuition_to_timbre(self, y: float) -> str:
        """
        Map y-axis to timbre complexity
        
        Logic(-1) → 'pure' (simple sine wave)
        Neutral(0) → 'harmonic' (basic harmonics)
        Intuition(+1) → 'complex' (rich harmonics)
        """
        if y < -0.3:
            return 'pure'
        elif y < 0.3:
            return 'harmonic'
        else:
            return 'complex'


class HapticMapper:
    """
    4D 좌표를 촉각적 속성으로 매핑 (선택적)
    
    Requires:
        - Game controller with vibration
        - Or phone vibration
        - Or dedicated haptic device
    
    Mapping Strategy:
        w (Surface ←→ Depth) → Intensity (강도)
        x (Joy ←→ Sadness) → Pulse Rate (맥동)
        y (Logic ←→ Intuition) → Pattern (패턴)
    """
    
    def map_4d_to_haptic(self, position_4d: Tuple[float, float, float, float]) -> HapticProperties:
        """
        4D 좌표를 촉각적 속성으로 변환
        
        Args:
            position_4d: (x, y, z, w) where each is in [-1, 1]
            
        Returns:
            HapticProperties with intensity, pulse_rate, pattern
        """
        x, y, z, w = position_4d
        
        # Intensity: Depth = stronger vibration
        intensity = max(0.0, w)
        
        # Pulse rate: Joy = faster, Sadness = slower
        pulse_rate = 2.0 + x * 3.0  # 1-5 Hz (clamp to positive)
        pulse_rate = max(0.5, min(5.0, pulse_rate))
        
        # Pattern: Logic = steady, Intuition = varied
        if y < -0.3:
            pattern = 'steady'
        elif y > 0.3:
            pattern = 'varied'
        else:
            pattern = 'pulse'
        
        return HapticProperties(
            intensity=intensity,
            pulse_rate=pulse_rate,
            pattern=pattern
        )


class FiveSensesMapper:
    """
    통합 오감 매핑 시스템
    
    4D Internal World의 객체들을 인간의 5감으로 변환합니다.
    VR 없이도 완전한 감각 경험을 제공합니다.
    
    Usage:
        mapper = FiveSensesMapper()
        
        # Single object
        senses = mapper.map_object(position_4d=(0.5, 0.3, -0.2, 0.8))
        print(f"Color: RGB{mapper.visual.hsb_to_rgb(senses.visual.hue, ...)}")
        print(f"Sound: {senses.audio.frequency}Hz")
        
        # Multiple objects (spatial audio scene)
        scene = mapper.map_scene(objects)
    """
    
    def __init__(self, enable_haptic: bool = False):
        """
        Initialize mappers
        
        Args:
            enable_haptic: Enable haptic feedback (requires compatible device)
        """
        self.visual = VisualMapper()
        self.audio = AudioMapper()
        self.haptic = HapticMapper() if enable_haptic else None
    
    def map_object(self, position_4d: Tuple[float, float, float, float]) -> SensoryExperience:
        """
        Map single object to sensory experience
        
        Args:
            position_4d: 4D coordinates (x, y, z, w)
            
        Returns:
            SensoryExperience with visual, audio, and optional haptic
        """
        visual = self.visual.map_4d_to_visual(position_4d)
        audio = self.audio.map_4d_to_audio(position_4d)
        haptic = self.haptic.map_4d_to_haptic(position_4d) if self.haptic else None
        
        return SensoryExperience(
            visual=visual,
            audio=audio,
            haptic=haptic
        )
    
    def map_scene(self, objects: list) -> list:
        """
        Map multiple objects to create rich sensory environment
        
        Args:
            objects: List of objects with 'position' attribute (4D)
            
        Returns:
            List of (object_id, SensoryExperience) tuples
        """
        experiences = []
        
        for obj in objects:
            exp = self.map_object(obj.position)
            experiences.append((id(obj), exp))
        
        return experiences


# Example usage
if __name__ == "__main__":
    mapper = FiveSensesMapper(enable_haptic=True)
    
    # Example: "Rainy day memory" star
    star_position = (-0.3, 0.7, -0.5, 0.8)
    # Sadness(-0.3), Intuitive(0.7), Past(-0.5), Deep(0.8)
    
    senses = mapper.map_object(star_position)
    
    print("🌟 Rainy Day Memory")
    print(f"   Visual: Hue={senses.visual.hue:.1f}° (blue-ish)")
    print(f"           Brightness={senses.visual.brightness:.2f} (bright)")
    print(f"           Glow={senses.visual.glow:.2f} (soft glow)")
    print(f"   Audio:  Frequency={senses.audio.frequency:.0f}Hz (low tone)")
    print(f"           Volume={senses.audio.volume:.2f} (loud)")
    print(f"           Timbre={senses.audio.timbre} (rich)")
    if senses.haptic:
        print(f"   Haptic: Intensity={senses.haptic.intensity:.2f} (strong)")
        print(f"           Pulse={senses.haptic.pulse_rate:.1f}Hz (slow)")
