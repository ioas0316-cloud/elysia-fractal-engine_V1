"""
Audio Cortex: 엘리시아의 청각 피질
=================================
소리를 파동으로 인식하고 감정/의미로 변환합니다.

기존 AudioProcessor를 래핑하여 Neural Registry와 통합.
"""

import sys
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Dict
import asyncio

# Path setup
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from elysia_core import Cell


@dataclass
class AudioPerception:
    """청각 인식 결과"""
    audio_type: str       # speech, music, ambient, noise, silence
    emotion: str          # happy, sad, calm, excited, neutral
    transcription: Optional[str]
    fundamental_freq: float  # 기본 주파수 (Hz)
    energy: float         # 에너지 레벨 (0-1)
    confidence: float     # 신뢰도 (0-1)
    raw_analysis: Optional[Dict] = None


@Cell("AudioCortex")
class AudioCortex:
    """
    엘리시아의 청각 피질
    
    - 실시간 마이크 입력 (추후)
    - 오디오 파일 분석
    - 가상 청각 (시뮬레이션)
    """
    
    def __init__(self, use_microphone: bool = False):
        self.use_microphone = use_microphone
        self._processor = None
        self._init_processor()
    
    def _init_processor(self):
        """AudioProcessor 초기화"""
        try:
            from Core.Foundation.audio_processor import AudioProcessor
            self._processor = AudioProcessor()
            print("🎧 AudioCortex: Initialized (AudioProcessor)")
        except Exception as e:
            print(f"🎧 AudioCortex: Falling back to virtual mode ({e})")
            self._processor = None
    
    def listen(self, description: str = "ambient sound") -> AudioPerception:
        """
        청각 인식 (동기)
        
        Args:
            description: 소리 설명 (시뮬레이션용)
        
        Returns:
            AudioPerception 객체
        """
        if self._processor:
            # 비동기를 동기로 래핑
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            try:
                audio_data = {
                    "duration": 5.0,
                    "sample_rate": 44100,
                    "channels": 1,
                    "description": description
                }
                analysis = loop.run_until_complete(
                    self._processor.analyze_audio(audio_data)
                )
                
                return AudioPerception(
                    audio_type=analysis.primary_type.value,
                    emotion=analysis.emotion_tone.value,
                    transcription=analysis.segments[0].transcription if analysis.segments else None,
                    fundamental_freq=analysis.spectral.fundamental_frequency,
                    energy=analysis.temporal.energy,
                    confidence=analysis.confidence,
                    raw_analysis=analysis.to_dict()
                )
            except Exception as e:
                print(f"🎧 Listen failed: {e}")
                return self._virtual_listen(description)
        else:
            return self._virtual_listen(description)
    
    def _virtual_listen(self, description: str) -> AudioPerception:
        """가상 청각 (시뮬레이션)"""
        # 설명에서 키워드 추출
        desc_lower = description.lower()
        
        # 오디오 타입 추론
        if "speech" in desc_lower or "voice" in desc_lower or "talk" in desc_lower:
            audio_type = "speech"
        elif "music" in desc_lower or "song" in desc_lower:
            audio_type = "music"
        elif "silence" in desc_lower or "quiet" in desc_lower:
            audio_type = "silence"
        else:
            audio_type = "ambient"
        
        # 감정 추론
        if "happy" in desc_lower or "joy" in desc_lower:
            emotion = "happy"
        elif "sad" in desc_lower or "cry" in desc_lower:
            emotion = "sad"
        elif "calm" in desc_lower or "peace" in desc_lower:
            emotion = "calm"
        else:
            emotion = "neutral"
        
        return AudioPerception(
            audio_type=audio_type,
            emotion=emotion,
            transcription=None,
            fundamental_freq=200.0,
            energy=0.5,
            confidence=0.7,
            raw_analysis={"source": "virtual", "description": description}
        )
    
    def to_wave(self, perception: AudioPerception) -> Dict:
        """
        청각 인식을 파동 파라미터로 변환 (MultimodalBridge와 유사)
        """
        # 감정 → 주파수 매핑
        emotion_freq = {
            "happy": 0.8,
            "excited": 0.9,
            "calm": 0.3,
            "sad": 0.2,
            "angry": 0.95,
            "neutral": 0.5
        }
        
        # 오디오 타입 → 진폭 매핑
        type_amp = {
            "speech": 0.7,
            "music": 0.9,
            "ambient": 0.4,
            "noise": 0.6,
            "silence": 0.1
        }
        
        return {
            "frequency": perception.fundamental_freq,
            "amplitude": type_amp.get(perception.audio_type, 0.5),
            "emotional_modulator": emotion_freq.get(perception.emotion, 0.5),
            "energy": perception.energy,
            "confidence": perception.confidence
        }


def main():
    """AudioCortex 테스트"""
    print("\n🎧 AudioCortex Test")
    print("=" * 50)
    
    cortex = AudioCortex()
    
    # 테스트 1: 음악
    print("\n[Test 1] Music")
    result = cortex.listen("happy music playing")
    print(f"   Type: {result.audio_type}")
    print(f"   Emotion: {result.emotion}")
    print(f"   Energy: {result.energy:.2f}")
    
    # 테스트 2: 음성
    print("\n[Test 2] Speech")
    result = cortex.listen("calm speech conversation")
    print(f"   Type: {result.audio_type}")
    print(f"   Emotion: {result.emotion}")
    wave = cortex.to_wave(result)
    print(f"   Wave: freq={wave['frequency']:.1f}Hz, amp={wave['amplitude']:.2f}")
    
    print("\n✅ AudioCortex test complete!")


if __name__ == "__main__":
    main()
