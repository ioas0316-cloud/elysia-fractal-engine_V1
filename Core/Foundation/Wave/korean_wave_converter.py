"""
한글 파동 언어 변환기 (Korean Wave Language Converter)
======================================================

"파동언어를 한글로, 한글을 파동언어로"

당신의 고민: "파동언어를 한글로, 언어로 해체하려고 얼마나 용을 써왔는지..."
해결책: 이 변환기가 한글과 파동을 연결합니다.

핵심 아이디어:
- 한글 자모음 → 주파수 매핑
- 감정/의미 → 파동 패턴
- 문장 → 파동 시퀀스
"""

import logging
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
import numpy as np
from Core.Foundation.ether import Wave, ether

logger = logging.getLogger("KoreanWaveConverter")

# Constants
UNIVERSE_FREQUENCY = 432.0  # Hz - Universe base frequency
FREQUENCY_MODULATION = 0.1  # Modulation factor for text frequency


# 한글 자모음 → 주파수 매핑
KOREAN_FREQUENCY_MAP = {
    # 자음 (Consonants) - 낮은 주파수 (100-500Hz)
    'ㄱ': 100.0,  # 가벼운
    'ㄴ': 150.0,  # 부드러운
    'ㄷ': 200.0,  # 단단한
    'ㄹ': 250.0,  # 흐르는
    'ㅁ': 300.0,  # 감싸는
    'ㅂ': 350.0,  # 터지는
    'ㅅ': 400.0,  # 스치는
    'ㅇ': 450.0,  # 울리는
    'ㅈ': 500.0,  # 떨리는
    'ㅊ': 550.0,  # 쏟아지는
    'ㅋ': 600.0,  # 튀는
    'ㅌ': 650.0,  # 탁한
    'ㅍ': 700.0,  # 퍼지는
    'ㅎ': 750.0,  # 숨 쉬는
    
    # 모음 (Vowels) - 높은 주파수 (800-1200Hz)
    'ㅏ': 800.0,   # 밝은
    'ㅓ': 850.0,   # 어두운
    'ㅗ': 900.0,   # 둥근
    'ㅜ': 950.0,   # 깊은
    'ㅡ': 1000.0,  # 평평한
    'ㅣ': 1050.0,  # 날카로운
    'ㅐ': 1100.0,  # 선명한
    'ㅔ': 1150.0,  # 부드러운
    'ㅑ': 1200.0,  # 경쾌한
    'ㅕ': 1250.0,  # 그윽한
    'ㅛ': 1300.0,  # 높은
    'ㅠ': 1350.0,  # 애절한
}

# 감정 → 주파수 매핑 (Solfeggio + Custom)
EMOTION_FREQUENCY_MAP = {
    # 긍정적 감정
    '사랑': 528.0,    # Love (Solfeggio)
    '기쁨': 396.0,    # Joy
    '평화': 432.0,    # Peace (Universe frequency)
    '희망': 852.0,    # Hope (Solfeggio)
    '자유': 963.0,    # Freedom (Solfeggio)
    '용기': 741.0,    # Courage (Solfeggio)
    '치유': 285.0,    # Healing (Solfeggio)
    
    # 부정적 감정
    '두려움': 100.0,  # Fear
    '슬픔': 150.0,    # Sadness
    '분노': 200.0,    # Anger
    '불안': 250.0,    # Anxiety
    
    # 중립/상태
    '생각': 10.0,     # Thought (Alpha)
    '명상': 7.5,      # Meditation (Theta)
    '꿈': 4.0,        # Dream (Delta)
    '집중': 40.0,     # Focus (Gamma)
}

# 의미 → 위상(Phase) 매핑
MEANING_PHASE_MAP = {
    '질문': 'QUESTION',
    '답변': 'ANSWER',
    '명령': 'COMMAND',
    '욕망': 'DESIRE',
    '감각': 'SENSATION',
    '사고': 'THOUGHT',
    '행동': 'ACTION',
    '반성': 'REFLECTION',
}


@dataclass
class KoreanWavePattern:
    """한글로 표현된 파동 패턴"""
    text: str           # 원본 한글 텍스트
    frequencies: List[float]  # 주파수 리스트
    amplitudes: List[float]   # 진폭 리스트
    phase: str          # 위상 (의미/타입)
    emotion: str        # 감정


class KoreanWaveConverter:
    """
    한글 ↔ 파동 변환기
    
    사용법:
        converter = KoreanWaveConverter()
        
        # 한글 → 파동
        wave = converter.korean_to_wave("사랑해", emotion="사랑")
        ether.emit(wave)
        
        # 파동 → 한글
        text = converter.wave_to_korean(wave)
    """
    
    def __init__(self):
        self.char_freq_map = KOREAN_FREQUENCY_MAP
        self.emotion_freq_map = EMOTION_FREQUENCY_MAP
        self.phase_map = MEANING_PHASE_MAP
        logger.info("🌊 한글 파동 변환기 초기화됨")
    
    def korean_to_wave(
        self,
        text: str,
        emotion: str = "생각",
        meaning: str = "사고",
        amplitude: float = 1.0
    ) -> Wave:
        """
        한글 → 파동 변환
        
        Args:
            text: 한글 텍스트
            emotion: 감정 (사랑, 기쁨, 두려움 등)
            meaning: 의미/타입 (질문, 답변 등)
            amplitude: 진폭 (강도)
        
        Returns:
            Wave 객체
        """
        # 1. 감정 주파수 선택
        emotion_freq = self.emotion_freq_map.get(emotion, 432.0)
        
        # 2. 텍스트를 자모음 주파수로 분해
        char_frequencies = []
        for char in text:
            # 한글 자모 분해 (간단 버전)
            if char in self.char_freq_map:
                char_frequencies.append(self.char_freq_map[char])
        
        # 3. 평균 주파수 계산 (텍스트의 "색깔")
        if char_frequencies:
            text_freq = sum(char_frequencies) / len(char_frequencies)
        else:
            # 기본값
            text_freq = UNIVERSE_FREQUENCY  # 기본값
        
        # 4. 감정과 텍스트 주파수를 조합
        # 감정이 주파수, 텍스트가 변조(modulation)
        combined_freq = emotion_freq + (text_freq - UNIVERSE_FREQUENCY) * FREQUENCY_MODULATION  # 미세 조정
        
        # 5. 위상 선택
        phase = self.phase_map.get(meaning, "THOUGHT")
        
        # 6. Wave 객체 생성
        wave = Wave(
            sender="KoreanConverter",
            frequency=combined_freq,
            amplitude=amplitude,
            phase=phase,
            payload={
                "text": text,
                "emotion": emotion,
                "char_frequencies": char_frequencies[:5],  # 처음 5개만
                "language": "korean"
            }
        )
        
        logger.info(f"🌊 한글 → 파동: '{text}' → {combined_freq:.1f}Hz ({emotion})")
        return wave
    
    def wave_to_korean(self, wave: Wave) -> str:
        """
        파동 → 한글 변환 (해석)
        
        Args:
            wave: Wave 객체
        
        Returns:
            한글 해석
        """
        # payload에서 원본 텍스트 추출
        if isinstance(wave.payload, dict) and "text" in wave.payload:
            return wave.payload["text"]
        
        # 주파수로부터 감정 추론
        emotion = self._frequency_to_emotion(wave.frequency)
        
        # 위상으로부터 의미 추론
        meaning = self._phase_to_meaning(wave.phase)
        
        # 진폭으로부터 강도 추론
        intensity = "강한 " if wave.amplitude > 0.7 else ""
        
        interpretation = f"{intensity}{emotion}의 {meaning}"
        logger.info(f"🌊 파동 → 한글: {wave.frequency:.1f}Hz → '{interpretation}'")
        
        return interpretation
    
    def _frequency_to_emotion(self, freq: float) -> str:
        """주파수 → 감정 추론"""
        # 가장 가까운 감정 찾기
        closest_emotion = "알 수 없는 감정"
        min_diff = float('inf')
        
        for emotion, emotion_freq in self.emotion_freq_map.items():
            diff = abs(freq - emotion_freq)
            if diff < min_diff:
                min_diff = diff
                closest_emotion = emotion
        
        return closest_emotion
    
    def _phase_to_meaning(self, phase: str) -> str:
        """위상 → 의미 추론"""
        # 역매핑
        for meaning, phase_code in self.phase_map.items():
            if phase_code == phase:
                return meaning
        return "메시지"
    
    def sentence_to_wave_sequence(
        self,
        sentence: str,
        base_emotion: str = "생각"
    ) -> List[Wave]:
        """
        문장 → 파동 시퀀스 변환
        
        한 문장을 여러 파동으로 분해 (각 단어마다)
        
        Args:
            sentence: 한글 문장
            base_emotion: 기본 감정
        
        Returns:
            Wave 리스트
        """
        words = sentence.split()
        waves = []
        
        for i, word in enumerate(words):
            # 문장 내 위치에 따라 진폭 조절
            amplitude = 1.0 - (i * 0.1)  # 점점 약해짐
            amplitude = max(amplitude, 0.3)  # 최소 0.3
            
            wave = self.korean_to_wave(
                text=word,
                emotion=base_emotion,
                amplitude=amplitude
            )
            waves.append(wave)
        
        logger.info(f"🌊 문장 분해: {len(words)}개 단어 → {len(waves)}개 파동")
        return waves
    
    def emit_korean(
        self,
        text: str,
        emotion: str = "생각",
        meaning: str = "사고"
    ):
        """
        한글을 파동으로 변환하여 Ether에 방출
        
        편의 함수 - 한 번에 변환+방출
        """
        wave = self.korean_to_wave(text, emotion, meaning)
        ether.emit(wave)
        logger.info(f"✉️ 파동 방출: '{text}' ({emotion})")
        return wave
    
    def create_emotion_dictionary(self) -> Dict[str, float]:
        """
        감정 사전 반환
        
        사용자가 자신만의 감정-주파수 매핑을 추가할 수 있도록
        """
        return self.emotion_freq_map.copy()
    
    def add_custom_emotion(self, emotion: str, frequency: float):
        """사용자 정의 감정 추가"""
        self.emotion_freq_map[emotion] = frequency
        logger.info(f"➕ 새 감정 추가: {emotion} = {frequency}Hz")


# 전역 변환기 인스턴스
korean_wave = KoreanWaveConverter()


# ============================================================================
# Test / Demo
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🌊 한글 파동 언어 변환기 테스트")
    print("="*70)
    
    converter = KoreanWaveConverter()
    
    # 1. 한글 → 파동
    print("\n1️⃣ 한글 → 파동 변환")
    print("-" * 70)
    
    test_phrases = [
        ("안녕하세요", "기쁨", "질문"),
        ("사랑해요", "사랑", "답변"),
        ("도와주세요", "불안", "명령"),
        ("감사합니다", "평화", "답변"),
    ]
    
    for text, emotion, meaning in test_phrases:
        wave = converter.korean_to_wave(text, emotion, meaning)
        print(f"  '{text}' ({emotion})")
        print(f"    → 주파수: {wave.frequency:.1f}Hz")
        print(f"    → 위상: {wave.phase}")
        print(f"    → 진폭: {wave.amplitude:.2f}")
        print()
    
    # 2. 파동 → 한글
    print("2️⃣ 파동 → 한글 해석")
    print("-" * 70)
    
    wave = converter.korean_to_wave("행복해요", "기쁨")
    interpretation = converter.wave_to_korean(wave)
    print(f"  파동: {wave}")
    print(f"  해석: {interpretation}")
    print()
    
    # 3. 문장 → 파동 시퀀스
    print("3️⃣ 문장 → 파동 시퀀스")
    print("-" * 70)
    
    sentence = "나는 Elysia입니다. 함께 성장해요."
    waves = converter.sentence_to_wave_sequence(sentence, "희망")
    for i, wave in enumerate(waves, 1):
        print(f"  {i}. {wave.payload['text']} → {wave.frequency:.1f}Hz")
    print()
    
    # 4. Ether 통합 테스트
    print("4️⃣ Ether 통합 테스트")
    print("-" * 70)
    
    # 리스너 등록
    def on_love_wave(wave: Wave):
        print(f"  💖 사랑의 파동 감지: {wave.payload.get('text', 'Unknown')}")
    
    # 528Hz (사랑)에 튜닝
    ether.tune_in(528.0, on_love_wave)
    
    # 파동 방출
    converter.emit_korean("너를 사랑해", emotion="사랑")
    
    print()
    
    # 5. 감정 사전
    print("5️⃣ 감정 사전")
    print("-" * 70)
    
    emotions = converter.create_emotion_dictionary()
    print("  사용 가능한 감정:")
    for emotion, freq in sorted(emotions.items(), key=lambda x: x[1]):
        print(f"    {emotion}: {freq}Hz")
    
    print("\n" + "="*70)
    print("✅ 테스트 완료!")
    print("\n💡 이제 한글을 파동으로, 파동을 한글로 변환할 수 있습니다!")
    print("="*70 + "\n")
