"""
Synesthetic Wave Sensor (공감각 파동 센서)
========================================

오감(시각, 청각, 촉각, 미각, 후각)을 넘어서 모든 감각 양식을 통합하는
멀티모달 센서 시스템입니다. 각 감각을 파동으로 변환하여 처리하며,
감각 간 교차 매핑(시각→청각, 청각→촉각 등)을 통해 공감각적 경험을 생성합니다.

Architecture:
- SensoryModality: 개별 감각 양식
- WaveSensor: 파동 기반 센서
- SynestheticMapper: 감각 간 매핑
- MultimodalIntegrator: 멀티모달 통합
"""

import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging
import json

logger = logging.getLogger("Elysia.SynestheticWaveSensor")


class SensoryModality(Enum):
    """감각 양식"""
    VISUAL = "visual"  # 시각
    AUDITORY = "auditory"  # 청각
    TACTILE = "tactile"  # 촉각
    GUSTATORY = "gustatory"  # 미각
    OLFACTORY = "olfactory"  # 후각
    PROPRIOCEPTIVE = "proprioceptive"  # 고유수용감각 (신체 위치)
    VESTIBULAR = "vestibular"  # 전정감각 (균형)
    INTEROCEPTIVE = "interoceptive"  # 내수용감각 (내부 상태)
    TEMPORAL = "temporal"  # 시간감각
    SPATIAL = "spatial"  # 공간감각
    EMOTIONAL = "emotional"  # 정서감각
    SEMANTIC = "semantic"  # 의미감각


class WaveProperty(Enum):
    """파동 속성"""
    FREQUENCY = "frequency"  # 주파수
    AMPLITUDE = "amplitude"  # 진폭
    PHASE = "phase"  # 위상
    WAVELENGTH = "wavelength"  # 파장
    VELOCITY = "velocity"  # 속도
    POLARIZATION = "polarization"  # 편광/방향성


@dataclass
class SensoryWave:
    """
    감각 파동 (Sensory Wave)
    
    모든 감각 입력을 파동으로 표현합니다.
    """
    modality: SensoryModality
    timestamp: datetime = field(default_factory=datetime.now)
    
    # 파동 특성
    frequency: float = 1.0  # Hz
    amplitude: float = 1.0  # 0.0 ~ 1.0
    phase: float = 0.0  # 0 ~ 2π
    
    # 파형 데이터
    waveform: np.ndarray = field(default_factory=lambda: np.array([]))
    
    # 추가 속성
    duration: float = 0.0  # seconds
    intensity: float = 0.5  # 0.0 ~ 1.0
    quality: str = ""  # 감각 질 (예: "bright", "sharp", "warm")
    
    # 공간 정보
    spatial_location: Optional[Tuple[float, float, float]] = None  # (x, y, z)
    
    # 메타데이터
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """딕셔너리 변환"""
        return {
            "modality": self.modality.value,
            "timestamp": self.timestamp.isoformat(),
            "frequency": self.frequency,
            "amplitude": self.amplitude,
            "phase": self.phase,
            "duration": self.duration,
            "intensity": self.intensity,
            "quality": self.quality,
            "spatial_location": self.spatial_location,
            "metadata": self.metadata
        }


class WaveSensor:
    """
    파동 센서 (Wave Sensor)
    
    특정 감각 양식의 입력을 파동으로 변환합니다.
    """
    
    def __init__(self, modality: SensoryModality):
        self.modality = modality
        self.is_active = True
        self.sensitivity = 1.0  # 감도 (0.0 ~ 2.0)
        self.samples_collected = 0
        
        logger.info(f"📡 Wave sensor initialized: {modality.value}")
    
    def sense(self, input_data: Any) -> SensoryWave:
        """
        감각 입력을 파동으로 변환
        
        Args:
            input_data: 감각 입력 (양식에 따라 다름)
            
        Returns:
            SensoryWave 객체
        """
        if not self.is_active:
            logger.warning(f"⚠️ Sensor {self.modality.value} is inactive")
            return None
        
        # 양식별 변환
        if self.modality == SensoryModality.VISUAL:
            wave = self._sense_visual(input_data)
        elif self.modality == SensoryModality.AUDITORY:
            wave = self._sense_auditory(input_data)
        elif self.modality == SensoryModality.TACTILE:
            wave = self._sense_tactile(input_data)
        elif self.modality == SensoryModality.GUSTATORY:
            wave = self._sense_gustatory(input_data)
        elif self.modality == SensoryModality.OLFACTORY:
            wave = self._sense_olfactory(input_data)
        elif self.modality == SensoryModality.EMOTIONAL:
            wave = self._sense_emotional(input_data)
        elif self.modality == SensoryModality.SEMANTIC:
            wave = self._sense_semantic(input_data)
        else:
            wave = self._sense_generic(input_data)
        
        self.samples_collected += 1
        return wave
    
    def _sense_visual(self, data: Any) -> SensoryWave:
        """시각 입력 → 파동"""
        # 예: 색상 → 주파수 매핑
        if isinstance(data, dict) and "color" in data:
            color = data["color"]
            # RGB를 주파수로 변환 (빨강=400THz, 보라=800THz)
            freq = 400 + (color.get("hue", 0) / 360) * 400  # THz
            amplitude = color.get("saturation", 0.5)
            intensity = color.get("brightness", 0.5)
            quality = color.get("name", "unknown")
        else:
            freq = 500.0
            amplitude = 0.5
            intensity = 0.5
            quality = "neutral"
        
        # 파형 생성 (정현파)
        t = np.linspace(0, 0.1, 100)
        waveform = amplitude * np.sin(2 * np.pi * freq * t)
        
        return SensoryWave(
            modality=SensoryModality.VISUAL,
            frequency=freq,
            amplitude=amplitude,
            waveform=waveform,
            intensity=intensity,
            quality=quality,
            metadata={"source": "visual_sensor"}
        )
    
    def _sense_auditory(self, data: Any) -> SensoryWave:
        """청각 입력 → 파동"""
        if isinstance(data, dict):
            freq = data.get("pitch", 440.0)  # Hz (A4 = 440Hz)
            amplitude = data.get("volume", 0.5)
            duration = data.get("duration", 1.0)
            quality = data.get("timbre", "pure")
        else:
            freq = 440.0
            amplitude = 0.5
            duration = 1.0
            quality = "pure"
        
        # 파형 생성
        t = np.linspace(0, duration, int(duration * 44100))  # 44.1kHz sampling
        waveform = amplitude * np.sin(2 * np.pi * freq * t)
        
        return SensoryWave(
            modality=SensoryModality.AUDITORY,
            frequency=freq,
            amplitude=amplitude,
            waveform=waveform,
            duration=duration,
            intensity=amplitude,
            quality=quality,
            metadata={"source": "auditory_sensor"}
        )
    
    def _sense_tactile(self, data: Any) -> SensoryWave:
        """촉각 입력 → 파동"""
        if isinstance(data, dict):
            pressure = data.get("pressure", 0.5)
            texture = data.get("texture", "smooth")
            temperature = data.get("temperature", 0.5)  # 0=cold, 1=hot
            location = data.get("location", (0, 0, 0))
        else:
            pressure = 0.5
            texture = "smooth"
            temperature = 0.5
            location = (0, 0, 0)
        
        # 압력을 진폭으로, 질감을 주파수로 매핑
        freq = 10.0 if texture == "smooth" else 50.0 if texture == "rough" else 30.0
        amplitude = pressure
        
        return SensoryWave(
            modality=SensoryModality.TACTILE,
            frequency=freq,
            amplitude=amplitude,
            intensity=pressure,
            quality=texture,
            spatial_location=location,
            metadata={"temperature": temperature}
        )
    
    def _sense_gustatory(self, data: Any) -> SensoryWave:
        """미각 입력 → 파동"""
        if isinstance(data, dict):
            taste = data.get("taste", "umami")  # sweet, sour, salty, bitter, umami
            intensity = data.get("intensity", 0.5)
        else:
            taste = "umami"
            intensity = 0.5
        
        # 맛을 주파수로 매핑
        taste_freq_map = {
            "sweet": 100.0,
            "sour": 200.0,
            "salty": 150.0,
            "bitter": 250.0,
            "umami": 175.0
        }
        freq = taste_freq_map.get(taste, 150.0)
        
        return SensoryWave(
            modality=SensoryModality.GUSTATORY,
            frequency=freq,
            amplitude=intensity,
            intensity=intensity,
            quality=taste,
            metadata={"taste_type": taste}
        )
    
    def _sense_olfactory(self, data: Any) -> SensoryWave:
        """후각 입력 → 파동"""
        if isinstance(data, dict):
            scent = data.get("scent", "neutral")
            intensity = data.get("intensity", 0.5)
            pleasantness = data.get("pleasantness", 0.5)  # -1=unpleasant, 1=pleasant
        else:
            scent = "neutral"
            intensity = 0.5
            pleasantness = 0.5
        
        # 향을 주파수로 매핑
        freq = 50.0 + (pleasantness + 1) * 25.0  # 50-100 Hz
        
        return SensoryWave(
            modality=SensoryModality.OLFACTORY,
            frequency=freq,
            amplitude=intensity,
            intensity=intensity,
            quality=scent,
            metadata={"pleasantness": pleasantness}
        )
    
    def _sense_emotional(self, data: Any) -> SensoryWave:
        """정서 입력 → 파동"""
        if isinstance(data, dict):
            emotion = data.get("emotion", "neutral")
            valence = data.get("valence", 0.0)  # -1=negative, 1=positive
            arousal = data.get("arousal", 0.5)  # 0=calm, 1=excited
        else:
            emotion = "neutral"
            valence = 0.0
            arousal = 0.5
        
        # 정서를 파동으로 매핑
        freq = 1.0 + arousal * 10.0  # 1-11 Hz
        amplitude = abs(valence)
        phase = 0 if valence >= 0 else np.pi
        
        return SensoryWave(
            modality=SensoryModality.EMOTIONAL,
            frequency=freq,
            amplitude=amplitude,
            phase=phase,
            intensity=arousal,
            quality=emotion,
            metadata={"valence": valence, "arousal": arousal}
        )
    
    def _sense_semantic(self, data: Any) -> SensoryWave:
        """의미 입력 → 파동"""
        if isinstance(data, dict):
            meaning = data.get("meaning", "")
            abstractness = data.get("abstractness", 0.5)  # 0=concrete, 1=abstract
            complexity = data.get("complexity", 0.5)
        else:
            meaning = str(data)
            abstractness = 0.5
            complexity = 0.5
        
        # 의미를 파동으로 매핑
        freq = 5.0 + abstractness * 20.0  # 5-25 Hz
        amplitude = complexity
        
        return SensoryWave(
            modality=SensoryModality.SEMANTIC,
            frequency=freq,
            amplitude=amplitude,
            intensity=complexity,
            quality=meaning[:50],
            metadata={"abstractness": abstractness}
        )
    
    def _sense_generic(self, data: Any) -> SensoryWave:
        """일반 감각 입력 → 파동"""
        return SensoryWave(
            modality=self.modality,
            frequency=1.0,
            amplitude=0.5,
            intensity=0.5,
            quality="generic",
            metadata={"raw_data": str(data)}
        )


class SynestheticMapper:
    """
    공감각 매퍼 (Synesthetic Mapper)
    
    한 감각 양식을 다른 감각 양식으로 변환합니다.
    예: 시각 → 청각 (색을 소리로), 청각 → 시각 (소리를 색으로)
    """
    
    def __init__(self):
        # 감각 간 매핑 규칙
        self.mapping_rules: Dict[Tuple[SensoryModality, SensoryModality], Callable] = {}
        self._initialize_default_mappings()
        
        logger.info("🌈 Synesthetic Mapper initialized")
    
    def _initialize_default_mappings(self):
        """기본 공감각 매핑 규칙 초기화"""
        # 시각 → 청각 (색 → 소리)
        self.mapping_rules[(SensoryModality.VISUAL, SensoryModality.AUDITORY)] = \
            self._map_visual_to_auditory
        
        # 청각 → 시각 (소리 → 색)
        self.mapping_rules[(SensoryModality.AUDITORY, SensoryModality.VISUAL)] = \
            self._map_auditory_to_visual
        
        # 촉각 → 청각 (질감 → 소리)
        self.mapping_rules[(SensoryModality.TACTILE, SensoryModality.AUDITORY)] = \
            self._map_tactile_to_auditory
        
        # 정서 → 시각 (감정 → 색)
        self.mapping_rules[(SensoryModality.EMOTIONAL, SensoryModality.VISUAL)] = \
            self._map_emotional_to_visual
        
        # 의미 → 정서 (의미 → 감정)
        self.mapping_rules[(SensoryModality.SEMANTIC, SensoryModality.EMOTIONAL)] = \
            self._map_semantic_to_emotional
    
    def map(
        self, 
        source_wave: SensoryWave, 
        target_modality: SensoryModality
    ) -> SensoryWave:
        """
        감각 변환
        
        Args:
            source_wave: 원본 감각 파동
            target_modality: 목표 감각 양식
            
        Returns:
            변환된 감각 파동
        """
        mapping_key = (source_wave.modality, target_modality)
        
        if mapping_key in self.mapping_rules:
            mapper_func = self.mapping_rules[mapping_key]
            result = mapper_func(source_wave)
            logger.debug(
                f"🔄 Mapped {source_wave.modality.value} → {target_modality.value}"
            )
            return result
        else:
            # 일반 변환 (주파수 스케일링)
            return self._generic_map(source_wave, target_modality)
    
    def _map_visual_to_auditory(self, wave: SensoryWave) -> SensoryWave:
        """시각 → 청각 변환 (색 → 소리)"""
        # 빛의 주파수를 소리 주파수로 스케일링
        # 빛: 400-800 THz → 소리: 20-20000 Hz
        audio_freq = (wave.frequency - 400) / 400 * 19980 + 20
        
        # 밝기 → 음량
        audio_amplitude = wave.intensity
        
        return SensoryWave(
            modality=SensoryModality.AUDITORY,
            frequency=audio_freq,
            amplitude=audio_amplitude,
            intensity=audio_amplitude,
            quality=f"sound_of_{wave.quality}",
            metadata={
                "source_modality": "visual",
                "original_frequency": wave.frequency
            }
        )
    
    def _map_auditory_to_visual(self, wave: SensoryWave) -> SensoryWave:
        """청각 → 시각 변환 (소리 → 색)"""
        # 소리 주파수를 색 주파수로 변환
        # 소리: 20-20000 Hz → 빛: 400-800 THz
        visual_freq = (wave.frequency - 20) / 19980 * 400 + 400
        
        # 음량 → 밝기
        visual_intensity = wave.amplitude
        
        return SensoryWave(
            modality=SensoryModality.VISUAL,
            frequency=visual_freq,
            amplitude=visual_intensity,
            intensity=visual_intensity,
            quality=f"color_of_{wave.quality}",
            metadata={
                "source_modality": "auditory",
                "original_frequency": wave.frequency
            }
        )
    
    def _map_tactile_to_auditory(self, wave: SensoryWave) -> SensoryWave:
        """촉각 → 청각 변환 (질감 → 소리)"""
        # 질감을 소리로 변환
        audio_freq = wave.frequency * 20  # 촉각 주파수 증폭
        audio_amplitude = wave.amplitude
        
        return SensoryWave(
            modality=SensoryModality.AUDITORY,
            frequency=audio_freq,
            amplitude=audio_amplitude,
            intensity=audio_amplitude,
            quality=f"sound_of_{wave.quality}_texture",
            metadata={"source_modality": "tactile"}
        )
    
    def _map_emotional_to_visual(self, wave: SensoryWave) -> SensoryWave:
        """정서 → 시각 변환 (감정 → 색)"""
        # 감정을 색으로 변환
        # 긍정적 감정 → 따뜻한 색 (빨강/주황), 부정적 → 차가운 색 (파랑/보라)
        valence = wave.metadata.get("valence", 0)
        
        if valence > 0:
            # 긍정적: 400-600 THz (빨강-노랑)
            visual_freq = 400 + valence * 200
            quality = "warm"
        else:
            # 부정적: 600-800 THz (초록-보라)
            visual_freq = 600 + abs(valence) * 200
            quality = "cool"
        
        return SensoryWave(
            modality=SensoryModality.VISUAL,
            frequency=visual_freq,
            amplitude=wave.intensity,
            intensity=wave.intensity,
            quality=quality,
            metadata={"source_emotion": wave.quality}
        )
    
    def _map_semantic_to_emotional(self, wave: SensoryWave) -> SensoryWave:
        """의미 → 정서 변환"""
        # 의미의 추상성 → 각성도
        abstractness = wave.metadata.get("abstractness", 0.5)
        
        # 복잡도 → 정서 강도
        arousal = wave.intensity
        
        return SensoryWave(
            modality=SensoryModality.EMOTIONAL,
            frequency=1.0 + arousal * 10.0,
            amplitude=wave.amplitude,
            intensity=arousal,
            quality="contemplative",
            metadata={
                "valence": 0.0,
                "arousal": arousal,
                "source_meaning": wave.quality
            }
        )
    
    def _generic_map(
        self, 
        source: SensoryWave, 
        target_modality: SensoryModality
    ) -> SensoryWave:
        """일반 변환 (매핑 규칙이 없을 때)"""
        return SensoryWave(
            modality=target_modality,
            frequency=source.frequency,
            amplitude=source.amplitude,
            intensity=source.intensity,
            quality=f"mapped_from_{source.modality.value}",
            metadata={"source_modality": source.modality.value}
        )


class MultimodalIntegrator:
    """
    멀티모달 통합기 (Multimodal Integrator)
    
    여러 감각 양식의 입력을 통합하여 통합된 지각을 생성합니다.
    """
    
    def __init__(self):
        self.sensors: Dict[SensoryModality, WaveSensor] = {}
        self.mapper = SynestheticMapper()
        self.active_waves: List[SensoryWave] = []
        self.integration_history: List[Dict[str, Any]] = []
        
        # 모든 감각 양식에 대한 센서 생성
        for modality in SensoryModality:
            self.sensors[modality] = WaveSensor(modality)
        
        logger.info("🌊 Multimodal Integrator initialized")
    
    def sense_multimodal(
        self, 
        inputs: Dict[SensoryModality, Any]
    ) -> List[SensoryWave]:
        """
        멀티모달 감각 입력 처리
        
        Args:
            inputs: {감각양식: 입력데이터} 딕셔너리
            
        Returns:
            모든 감각 파동 리스트
        """
        waves = []
        
        for modality, input_data in inputs.items():
            if modality in self.sensors:
                wave = self.sensors[modality].sense(input_data)
                if wave:
                    waves.append(wave)
        
        self.active_waves = waves
        return waves
    
    def create_synesthetic_experience(
        self, 
        source_wave: SensoryWave,
        target_modalities: List[SensoryModality]
    ) -> List[SensoryWave]:
        """
        공감각 경험 생성
        
        하나의 감각을 여러 다른 감각으로 변환합니다.
        
        Args:
            source_wave: 원본 감각 파동
            target_modalities: 변환할 목표 감각 양식 리스트
            
        Returns:
            변환된 감각 파동 리스트
        """
        synesthetic_waves = [source_wave]  # 원본 포함
        
        for target in target_modalities:
            if target != source_wave.modality:
                mapped_wave = self.mapper.map(source_wave, target)
                synesthetic_waves.append(mapped_wave)
        
        logger.info(
            f"🌈 Created synesthetic experience: " +
            f"{source_wave.modality.value} → " +
            f"{', '.join(m.value for m in target_modalities)}"
        )
        
        return synesthetic_waves
    
    def integrate_waves(
        self, 
        waves: List[SensoryWave]
    ) -> Dict[str, Any]:
        """
        여러 감각 파동을 통합
        
        Returns:
            통합된 지각 표현
        """
        if not waves:
            return {}
        
        # 모달리티별 그룹화
        by_modality = {}
        for wave in waves:
            modality = wave.modality.value
            if modality not in by_modality:
                by_modality[modality] = []
            by_modality[modality].append(wave)
        
        # 통합 메트릭 계산
        avg_frequency = np.mean([w.frequency for w in waves])
        avg_amplitude = np.mean([w.amplitude for w in waves])
        avg_intensity = np.mean([w.intensity for w in waves])
        
        # 공명 점수 계산 (파동들이 얼마나 조화로운가)
        resonance_score = self._calculate_resonance(waves)
        
        integration = {
            "timestamp": datetime.now().isoformat(),
            "num_modalities": len(by_modality),
            "total_waves": len(waves),
            "modalities": list(by_modality.keys()),
            "waves_by_modality": {
                mod: [w.to_dict() for w in ws]
                for mod, ws in by_modality.items()
            },
            "integrated_metrics": {
                "average_frequency": avg_frequency,
                "average_amplitude": avg_amplitude,
                "average_intensity": avg_intensity,
                "resonance_score": resonance_score
            },
            "description": self._generate_integrated_description(waves)
        }
        
        self.integration_history.append(integration)
        return integration
    
    def _calculate_resonance(self, waves: List[SensoryWave]) -> float:
        """파동들 간의 공명 점수 계산"""
        if len(waves) < 2:
            return 1.0
        
        # 주파수 유사도
        frequencies = [w.frequency for w in waves]
        freq_std = np.std(frequencies)
        freq_resonance = 1.0 / (1.0 + freq_std)
        
        # 진폭 유사도
        amplitudes = [w.amplitude for w in waves]
        amp_std = np.std(amplitudes)
        amp_resonance = 1.0 / (1.0 + amp_std)
        
        # 종합 공명 점수
        resonance = (freq_resonance + amp_resonance) / 2.0
        return resonance
    
    def _generate_integrated_description(self, waves: List[SensoryWave]) -> str:
        """통합된 지각 설명 생성"""
        modalities = [w.modality.value for w in waves]
        qualities = [w.quality for w in waves if w.quality]
        
        return (
            f"Integrated perception from {len(set(modalities))} modalities: " +
            f"{', '.join(set(modalities))}. " +
            f"Qualities: {', '.join(qualities[:3])}"
        )
    
    def get_status(self) -> Dict[str, Any]:
        """통합기 상태"""
        return {
            "total_sensors": len(self.sensors),
            "active_waves": len(self.active_waves),
            "integration_count": len(self.integration_history),
            "sensors_status": {
                mod.value: {
                    "active": sensor.is_active,
                    "samples": sensor.samples_collected
                }
                for mod, sensor in self.sensors.items()
            }
        }


# 사용 예제
def example_synesthetic_sensing():
    """공감각 센서 사용 예제"""
    integrator = MultimodalIntegrator()
    
    print("\n🌊 공감각 파동 센서 데모")
    print("=" * 60)
    
    # 1. 멀티모달 입력
    print("\n--- 멀티모달 감각 입력 ---")
    inputs = {
        SensoryModality.VISUAL: {
            "color": {"hue": 240, "saturation": 0.8, "brightness": 0.6, "name": "blue"}
        },
        SensoryModality.AUDITORY: {
            "pitch": 440.0, "volume": 0.7, "duration": 1.0, "timbre": "clear"
        },
        SensoryModality.EMOTIONAL: {
            "emotion": "joy", "valence": 0.8, "arousal": 0.6
        }
    }
    
    waves = integrator.sense_multimodal(inputs)
    print(f"감지된 파동: {len(waves)}개")
    for wave in waves:
        print(f"  - {wave.modality.value}: freq={wave.frequency:.2f}, amp={wave.amplitude:.2f}")
    
    # 2. 공감각 경험 생성
    print("\n--- 공감각 변환 (청각 → 시각, 촉각) ---")
    audio_wave = waves[1]  # 청각 파동
    synesthetic = integrator.create_synesthetic_experience(
        audio_wave,
        [SensoryModality.VISUAL, SensoryModality.TACTILE]
    )
    print(f"생성된 공감각 경험: {len(synesthetic)}개 감각")
    for wave in synesthetic:
        print(f"  - {wave.modality.value}: {wave.quality}")
    
    # 3. 통합
    print("\n--- 감각 통합 ---")
    integration = integrator.integrate_waves(waves)
    print(f"통합 결과:")
    print(f"  - 양식 수: {integration['num_modalities']}")
    print(f"  - 공명 점수: {integration['integrated_metrics']['resonance_score']:.3f}")
    print(f"  - 설명: {integration['description']}")


if __name__ == "__main__":
    example_synesthetic_sensing()
