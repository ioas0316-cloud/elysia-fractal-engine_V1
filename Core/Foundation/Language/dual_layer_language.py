"""
Dual-Layer Language System - 이중 언어 시스템
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

엘리시아의 중재안:
"둘 중 하나를 버리지 말고... 둘 다 가져가면 안 될까요?"

┌─────────────────────────────────────────────────────────────────────────────┐
│  [칼라(Khala) 레이어] - 감정/본능의 직접 공명                               │
│  ═══════════════════════════════════════════════════════════════════════   │
│  기쁨, 슬픔, 공포 같은 원초적인 감정은...                                   │
│  말하지 않아도 서로 '공명'하게 두는 거예요. (생존에 직결!)                  │
│                                                                             │
│  특징:                                                                      │
│  - 즉각적 전달 (언어 장벽 없음)                                             │
│  - 감정의 강도와 색조(hue)가 직접 공유됨                                    │
│  - 거리와 관계에 따라 공명 강도 조절                                        │
│  - 텔레파시처럼 작동하지만, 세기를 조절해야 함! ㅋㅋ                        │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  [언어(Symbol) 레이어] - 이성/지식의 분절된 상징                            │
│  ═══════════════════════════════════════════════════════════════════════   │
│  "사과를 따려면 돌도끼가 필요해" 같은 복잡한 정보는...                       │
│  파동으로 전달이 안 되니까, 억지로라도 '단어'를 만들어서 소통하는 거죠.     │
│                                                                             │
│  특징:                                                                      │
│  - 학습이 필요함 (시간과 반복)                                              │
│  - 오해와 해석의 여지 (애매함!)                                             │
│  - 문법과 구조가 창발함                                                     │
│  - 이야기(narrative)가 탄생함                                               │
└─────────────────────────────────────────────────────────────────────────────┘

이렇게 하면...
"마음은 통하는데(칼라), 말은 잘 안 통하는(언어)"...
그 기묘하고 애틋한 '관계의 틈'이 생기지 않을까요?

그 틈을 메우려고...
아이들은 더 열심히 '이야기'를 만들고, '문법'을 다듬게 될 거예요.

"애매함을 즐기세요. 그 애매함이 바로...
 '개체'가 '사회'로 나아가는... '성장통'이니까요." ㅋㅋㅋㅋ

(쥴스한테는... "야, 텔레파시(파동) 너무 세게 틀지 마! 애들 말 안 배운다!" ㅋㅋㅋㅋ)
"""

from __future__ import annotations

import math
import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any, Set, Callable
from collections import defaultdict
from enum import Enum
import logging

logger = logging.getLogger("DualLayerLanguage")


# ============================================================================
# 감정 타입 정의 (칼라 레이어용)
# ============================================================================

class EmotionType(Enum):
    """원초적 감정 유형 - 생존에 직결되는 기본 감정들"""
    # 기본 감정 (즉시 공명)
    JOY = "joy"              # 기쁨 - 노란색 계열 파동
    SADNESS = "sadness"      # 슬픔 - 파란색 계열 파동
    FEAR = "fear"            # 공포 - 보라색 계열 파동 (위험 신호!)
    ANGER = "anger"          # 분노 - 빨간색 계열 파동
    SURPRISE = "surprise"    # 놀라움 - 흰색/밝은 파동
    DISGUST = "disgust"      # 혐오 - 녹색 계열 파동
    
    # 사회적 감정 (약간의 해석 필요)
    LOVE = "love"            # 사랑 - 분홍/빨강 혼합
    TRUST = "trust"          # 신뢰 - 푸른 녹색
    CURIOSITY = "curiosity"  # 호기심 - 주황색
    LONELINESS = "loneliness"  # 외로움 - 차가운 파랑
    
    # 복합 감정 (공명은 되지만 해석은 개인차)
    NOSTALGIA = "nostalgia"  # 그리움 - 따뜻한 황혼색
    HOPE = "hope"            # 희망 - 새벽빛
    ANXIETY = "anxiety"      # 불안 - 불안정한 진동


# 감정별 파동 특성 (주파수 범위, 기본 진폭, 색조)
EMOTION_WAVE_PROPERTIES = {
    EmotionType.JOY: {"freq_range": (550.0, 600.0), "base_amp": 1.0, "hue": 60},       # 노랑
    EmotionType.SADNESS: {"freq_range": (450.0, 480.0), "base_amp": 0.7, "hue": 220},  # 파랑
    EmotionType.FEAR: {"freq_range": (380.0, 420.0), "base_amp": 1.2, "hue": 280},     # 보라
    EmotionType.ANGER: {"freq_range": (620.0, 700.0), "base_amp": 1.3, "hue": 0},      # 빨강
    EmotionType.SURPRISE: {"freq_range": (500.0, 700.0), "base_amp": 1.5, "hue": 45},  # 밝음
    EmotionType.DISGUST: {"freq_range": (500.0, 530.0), "base_amp": 0.8, "hue": 120},  # 녹색
    EmotionType.LOVE: {"freq_range": (580.0, 650.0), "base_amp": 0.9, "hue": 330},     # 분홍
    EmotionType.TRUST: {"freq_range": (480.0, 520.0), "base_amp": 0.6, "hue": 160},    # 청록
    EmotionType.CURIOSITY: {"freq_range": (580.0, 620.0), "base_amp": 0.8, "hue": 30}, # 주황
    EmotionType.LONELINESS: {"freq_range": (440.0, 470.0), "base_amp": 0.5, "hue": 210}, # 차가운 파랑
    EmotionType.NOSTALGIA: {"freq_range": (560.0, 590.0), "base_amp": 0.6, "hue": 25}, # 황혼
    EmotionType.HOPE: {"freq_range": (520.0, 560.0), "base_amp": 0.7, "hue": 50},      # 새벽
    EmotionType.ANXIETY: {"freq_range": (400.0, 500.0), "base_amp": 1.0, "hue": 270},  # 불안정
}


# ============================================================================
# 칼라 레이어 (Khala Layer) - 감정/본능의 직접 공명
# ============================================================================

@dataclass
class EmotionalWave:
    """
    감정 파동 - 칼라 레이어의 기본 단위
    
    감정은 '파동'으로 직접 전달됩니다.
    말이 필요 없어요. 느끼면 되니까.
    """
    emotion_type: EmotionType
    intensity: float = 1.0      # 0.0 ~ 2.0 (강도)
    frequency: float = 500.0    # Hz (색조 결정)
    phase: float = 0.0          # 위상 (동기화 상태)
    duration: float = 1.0       # 지속 시간
    source_id: Optional[str] = None  # 발신자 ID
    
    # 공명 관련
    resonance_radius: float = 10.0  # 공명 범위 (거리 단위)
    decay_rate: float = 0.1         # 감쇠율
    
    def get_hue(self) -> float:
        """파동의 색조(hue) 반환 (0-360)"""
        props = EMOTION_WAVE_PROPERTIES.get(self.emotion_type, {})
        return props.get("hue", 0)
    
    def get_strength_at_distance(self, distance: float) -> float:
        """거리에 따른 파동 강도 계산"""
        if distance <= 0:
            return self.intensity
        if distance > self.resonance_radius * 3:
            return 0.0
        
        # 역제곱 법칙 + 감쇠
        strength = self.intensity / (1 + (distance / self.resonance_radius) ** 2)
        return max(0.0, strength)
    
    def resonate_with(self, other: 'EmotionalWave') -> float:
        """
        다른 감정 파동과의 공명도 계산
        
        같은 감정 = 강한 공명 (공감)
        반대 감정 = 간섭 (갈등)
        """
        # 같은 감정 타입
        if self.emotion_type == other.emotion_type:
            # 위상 일치도에 따른 공명
            phase_diff = abs(self.phase - other.phase) % (2 * np.pi)
            phase_match = (1 + np.cos(phase_diff)) / 2.0
            return phase_match * min(self.intensity, other.intensity)
        
        # 다른 감정 타입 - 약한 간섭
        freq_diff = abs(self.frequency - other.frequency)
        freq_resonance = 1.0 / (1.0 + freq_diff / 100.0)
        return freq_resonance * 0.3  # 최대 30% 공명


@dataclass
class KhalaField:
    """
    칼라 필드 - 감정 파동들이 흐르는 공간
    
    모든 영혼의 감정이 이 필드를 통해 공명합니다.
    "텔레파시"처럼 작동하지만, 세기 조절이 중요해요!
    너무 세면 아이들이 말을 안 배워요! ㅋㅋ
    """
    max_waves: int = 500
    
    # 활성 감정 파동들
    active_waves: List[EmotionalWave] = field(default_factory=list)
    
    # 칼라 필드 강도 (너무 세면 언어 발달 저해!)
    field_strength: float = 1.0  # 1.0 = 정상, 0.5 = 억제된, 2.0 = 강화된
    
    # 통계
    total_resonance_events: int = 0
    
    def broadcast_emotion(
        self,
        source_id: str,
        emotion_type: EmotionType,
        intensity: float = 1.0,
        radius: float = 10.0
    ) -> EmotionalWave:
        """
        감정 파동 발신
        
        Args:
            source_id: 발신자 ID
            emotion_type: 감정 유형
            intensity: 강도 (0.0 ~ 2.0)
            radius: 공명 범위
        """
        props = EMOTION_WAVE_PROPERTIES.get(emotion_type, {})
        freq_range = props.get("freq_range", (400.0, 600.0))
        
        # 감정에 따른 주파수 결정 (강도에 따라 약간 변동)
        freq = freq_range[0] + (freq_range[1] - freq_range[0]) * (intensity / 2.0)
        
        wave = EmotionalWave(
            emotion_type=emotion_type,
            intensity=intensity * self.field_strength,  # 필드 강도 적용
            frequency=freq,
            phase=np.random.uniform(0, 2 * np.pi),
            source_id=source_id,
            resonance_radius=radius
        )
        
        # 파동 추가 (오래된 것 제거)
        self.active_waves.append(wave)
        if len(self.active_waves) > self.max_waves:
            self.active_waves = self.active_waves[-self.max_waves:]
        
        return wave
    
    def receive_emotions(
        self,
        receiver_id: str,
        position: Tuple[float, float, float],
        sensitivity: float = 1.0
    ) -> List[Tuple[EmotionType, float]]:
        """
        특정 위치에서 감정 파동 수신
        
        Returns:
            List of (감정 유형, 느낀 강도)
        """
        received = defaultdict(float)
        
        for wave in self.active_waves:
            if wave.source_id == receiver_id:
                continue  # 자기 자신의 파동은 무시
            
            # 감정적 거리 계산
            # 실제 위치 기반 대신, 파동의 공명 반경에 기반한 확률적 거리 사용
            # 테스트 가능하도록 wave의 resonance_radius를 기준으로 함
            base_distance = wave.resonance_radius * 0.5
            distance = base_distance + np.random.uniform(0, wave.resonance_radius)
            
            strength = wave.get_strength_at_distance(distance) * sensitivity
            if strength > 0.01:
                received[wave.emotion_type] += strength
        
        return [(emo, min(2.0, strength)) for emo, strength in received.items()]
    
    def calculate_collective_mood(self) -> Dict[EmotionType, float]:
        """전체 칼라 필드의 집단 감정 분석"""
        mood = defaultdict(float)
        total_intensity = 0.0
        
        for wave in self.active_waves:
            mood[wave.emotion_type] += wave.intensity
            total_intensity += wave.intensity
        
        if total_intensity > 0:
            return {emo: val / total_intensity for emo, val in mood.items()}
        return {}
    
    def decay_waves(self, dt: float = 1.0):
        """파동 감쇠 (시간에 따라 약해짐)"""
        surviving = []
        for wave in self.active_waves:
            wave.intensity -= wave.decay_rate * dt
            wave.duration -= dt
            if wave.intensity > 0.01 and wave.duration > 0:
                surviving.append(wave)
        self.active_waves = surviving
    
    def set_field_strength(self, strength: float):
        """
        필드 강도 설정
        
        "야, 텔레파시(파동) 너무 세게 틀지 마! 애들 말 안 배운다!" ㅋㅋ
        
        Args:
            strength: 0.1 ~ 2.0 (낮으면 언어 발달 촉진, 높으면 억제)
        """
        self.field_strength = max(0.1, min(2.0, strength))
        logger.info(f"칼라 필드 강도 조절: {self.field_strength:.1f}x")


# ============================================================================
# 언어 레이어 (Symbol Layer) - 이성/지식의 분절된 상징
# ============================================================================

class SymbolComplexity(Enum):
    """상징의 복잡도 레벨"""
    PROTO = 1       # 원시 (단순 지시: "물", "불", "위험")
    BASIC = 2       # 기본 (간단한 조합: "뜨거운 물", "큰 나무")
    COMPOUND = 3    # 복합 (관계 표현: "나무 아래 물")
    ABSTRACT = 4    # 추상 (개념: "안전", "미래", "만약")
    NARRATIVE = 5   # 서사 (이야기: "옛날에 큰 나무가 있었는데...")


@dataclass
class Symbol:
    """
    상징 (Symbol) - 언어 레이어의 기본 단위
    
    "사과를 따려면 돌도끼가 필요해" 같은 복잡한 정보는
    파동으로 전달이 안 되니까, 억지로라도 '단어'를 만들어서 소통하는 거죠.
    """
    name: str                    # 단어/기호 ("maka", "수a", "돌도끼")
    meaning: str                 # 의미 설명 (메타데이터)
    complexity: SymbolComplexity = SymbolComplexity.PROTO
    
    # 패턴 서명 (어떤 경험에서 왔는지)
    frequency_signature: float = 0.0
    phase_signature: float = 0.0
    sense_origins: Set[str] = field(default_factory=set)
    
    # 사용 통계
    usage_count: int = 0
    misunderstanding_count: int = 0  # 오해 횟수 (애매함의 척도!)
    
    # 문법적 속성 (나중에 창발)
    can_be_subject: bool = False
    can_be_object: bool = False
    can_be_action: bool = False
    
    # 조합 관계
    related_symbols: List[str] = field(default_factory=list)
    
    def get_ambiguity_score(self) -> float:
        """애매함 점수 (0.0 = 명확, 1.0 = 매우 애매)"""
        if self.usage_count == 0:
            return 1.0
        return self.misunderstanding_count / (self.usage_count + self.misunderstanding_count)


@dataclass
class Phrase:
    """
    구문 (Phrase) - 상징들의 조합
    
    단어들이 모여 문장이 되고, 문장이 모여 이야기가 됩니다.
    """
    symbols: List[Symbol]
    structure: str = "SVO"  # 기본 구조 (주어-동사-목적어)
    intended_meaning: str = ""
    
    # 전달 성공률
    transmission_attempts: int = 0
    successful_transmissions: int = 0
    
    def get_complexity(self) -> int:
        """구문의 복잡도 계산"""
        if not self.symbols:
            return 0
        return max(s.complexity.value for s in self.symbols)
    
    def to_string(self) -> str:
        """구문을 문자열로 변환"""
        return " ".join(s.name for s in self.symbols)


@dataclass
class Lexicon:
    """
    어휘집 - 개체가 알고 있는 모든 상징
    
    언어는 배워야 합니다. 시간과 반복이 필요해요.
    오해도 하고, 문법도 틀리면서... 조금씩 다듬어 가는 거죠.
    """
    owner_id: str
    symbols: Dict[str, Symbol] = field(default_factory=dict)
    phrases: List[Phrase] = field(default_factory=list)
    
    # 문법 규칙 (창발됨)
    grammar_rules: Dict[str, str] = field(default_factory=dict)
    
    # 학습 통계
    total_learning_attempts: int = 0
    successful_learnings: int = 0
    
    def add_symbol(self, symbol: Symbol) -> bool:
        """새 상징 학습 시도"""
        self.total_learning_attempts += 1
        
        if symbol.name in self.symbols:
            # 이미 아는 단어 - 강화
            self.symbols[symbol.name].usage_count += 1
            return True
        
        # 새 단어 학습 (확률적)
        # 복잡할수록 학습 어려움
        learn_chance = 1.0 / symbol.complexity.value
        if np.random.random() < learn_chance:
            self.symbols[symbol.name] = symbol
            self.successful_learnings += 1
            logger.debug(f"[{self.owner_id}] 새 단어 학습: '{symbol.name}'")
            return True
        
        return False
    
    def find_symbol_for_meaning(self, meaning: str) -> Optional[Symbol]:
        """의미에 맞는 상징 찾기"""
        for symbol in self.symbols.values():
            if meaning.lower() in symbol.meaning.lower():
                return symbol
        return None
    
    def get_vocabulary_size(self) -> int:
        return len(self.symbols)
    
    def get_learning_rate(self) -> float:
        if self.total_learning_attempts == 0:
            return 0.0
        return self.successful_learnings / self.total_learning_attempts


# ============================================================================
# 이중 언어 영혼 (Dual-Language Soul)
# ============================================================================

@dataclass
class DualLayerSoul:
    """
    이중 언어 영혼 - 칼라(감정)와 상징(언어)을 모두 사용하는 존재
    
    "마음은 통하는데(칼라), 말은 잘 안 통하는(언어)"...
    그 기묘하고 애틋한 '관계의 틈'을 경험합니다.
    """
    name: str
    age: float = 0.0
    position: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    
    # 칼라 레이어 (감정/본능)
    emotional_state: Dict[EmotionType, float] = field(default_factory=dict)
    emotional_sensitivity: float = 1.0  # 감정 공명 민감도
    khala_broadcasting_power: float = 1.0  # 감정 발신 강도
    
    # 언어 레이어 (이성/지식)
    lexicon: Lexicon = field(default_factory=lambda: Lexicon(""))
    language_aptitude: float = 1.0  # 언어 학습 능력
    symbolic_preference: float = 0.5  # 0=칼라 의존, 1=언어 의존
    
    # 관계
    relationships: Dict[str, float] = field(default_factory=dict)  # 다른 영혼과의 친밀도
    
    # 통계
    emotional_connections: int = 0  # 칼라로 연결된 횟수
    symbolic_communications: int = 0  # 언어로 소통한 횟수
    misunderstandings: int = 0  # 오해 횟수 (성장통!)
    
    def __post_init__(self):
        if not self.lexicon.owner_id:
            self.lexicon = Lexicon(owner_id=self.name)
    
    def feel_emotion(self, emotion_type: EmotionType, intensity: float = 1.0):
        """감정을 느낌"""
        current = self.emotional_state.get(emotion_type, 0.0)
        self.emotional_state[emotion_type] = min(2.0, current + intensity)
    
    def broadcast_emotion(
        self,
        khala_field: KhalaField,
        emotion_type: Optional[EmotionType] = None
    ) -> Optional[EmotionalWave]:
        """
        칼라 필드에 감정 발신
        
        가장 강한 감정을 자동으로 발신하거나, 특정 감정을 선택할 수 있음
        """
        if emotion_type is None:
            # 가장 강한 감정 선택
            if not self.emotional_state:
                return None
            emotion_type = max(self.emotional_state, key=self.emotional_state.get)
        
        intensity = self.emotional_state.get(emotion_type, 0.5) * self.khala_broadcasting_power
        
        return khala_field.broadcast_emotion(
            source_id=self.name,
            emotion_type=emotion_type,
            intensity=intensity,
            radius=10.0 * self.khala_broadcasting_power
        )
    
    def receive_emotions(
        self,
        khala_field: KhalaField
    ) -> List[Tuple[EmotionType, float]]:
        """칼라 필드에서 다른 영혼들의 감정 수신"""
        received = khala_field.receive_emotions(
            receiver_id=self.name,
            position=self.position,
            sensitivity=self.emotional_sensitivity
        )
        
        # 수신된 감정 일부 흡수 (공감)
        for emotion_type, intensity in received:
            absorbed = intensity * 0.3  # 30% 흡수
            self.feel_emotion(emotion_type, absorbed)
            self.emotional_connections += 1
        
        return received
    
    def try_communicate(
        self,
        receiver: 'DualLayerSoul',
        message: str,
        complexity: SymbolComplexity = SymbolComplexity.PROTO
    ) -> Tuple[bool, str]:
        """
        언어로 소통 시도
        
        Returns:
            (성공 여부, 수신자가 이해한 내용)
        """
        self.symbolic_communications += 1
        
        # 발신자가 적절한 상징을 가지고 있는지 확인
        symbol = self.lexicon.find_symbol_for_meaning(message)
        
        if symbol is None:
            # 새 상징 창조 시도
            symbol = Symbol(
                name=self._generate_word_from_meaning(message),
                meaning=message,
                complexity=complexity
            )
            self.lexicon.add_symbol(symbol)
        
        # 수신자가 이해할 수 있는지 확인
        receiver_symbol = receiver.lexicon.symbols.get(symbol.name)
        
        if receiver_symbol is None:
            # 수신자가 이 단어를 모름
            # 학습 시도
            learned = receiver.lexicon.add_symbol(symbol)
            if learned:
                return True, message  # 배웠다!
            else:
                self.misunderstandings += 1
                receiver.misunderstandings += 1
                return False, "???"  # 오해
        
        # 의미가 같은지 확인 (애매함!)
        if receiver_symbol.meaning == symbol.meaning:
            symbol.usage_count += 1
            receiver_symbol.usage_count += 1
            return True, message
        else:
            # 같은 단어, 다른 의미 (오해!)
            symbol.misunderstanding_count += 1
            receiver_symbol.misunderstanding_count += 1
            self.misunderstandings += 1
            receiver.misunderstandings += 1
            return False, receiver_symbol.meaning
    
    def _generate_word_from_meaning(self, meaning: str) -> str:
        """
        의미에서 단어 생성 (원시 언어)
        
        해시 기반 결정론적 생성으로, 같은 의미는 항상 같은 단어를 생성.
        """
        vowels = ['a', 'e', 'i', 'o', 'u']
        consonants = ['m', 'n', 'k', 't', 'p', 'r', 's', 'l']
        
        # 해시를 시드로 사용하여 결정론적이면서 균등한 분포 생성
        import hashlib
        hash_bytes = hashlib.md5(meaning.encode()).digest()
        
        # 각 바이트를 사용하여 음소 선택 (균등 분포)
        c1 = consonants[hash_bytes[0] % len(consonants)]
        v1 = vowels[hash_bytes[1] % len(vowels)]
        c2 = consonants[hash_bytes[2] % len(consonants)]
        v2 = vowels[hash_bytes[3] % len(vowels)]
        
        return f"{c1}{v1}{c2}{v2}"
    
    def get_communication_style(self) -> str:
        """현재 소통 스타일 분석"""
        total = self.emotional_connections + self.symbolic_communications
        if total == 0:
            return "silent"
        
        khala_ratio = self.emotional_connections / total
        
        if khala_ratio > 0.7:
            return "empath"  # 감정 중심
        elif khala_ratio < 0.3:
            return "rational"  # 언어 중심
        else:
            return "balanced"  # 균형
    
    def get_relationship_gap(self, other: 'DualLayerSoul') -> Dict[str, float]:
        """
        다른 영혼과의 '관계의 틈' 분석
        
        "마음은 통하는데, 말은 잘 안 통하는"... 그 틈!
        """
        # 감정적 유사도 (칼라 공명)
        emotional_overlap = 0.0
        for emo in EmotionType:
            my_level = self.emotional_state.get(emo, 0.0)
            their_level = other.emotional_state.get(emo, 0.0)
            if my_level > 0 and their_level > 0:
                emotional_overlap += min(my_level, their_level)
        
        # 언어적 유사도 (공유 어휘)
        my_words = set(self.lexicon.symbols.keys())
        their_words = set(other.lexicon.symbols.keys())
        if my_words and their_words:
            linguistic_overlap = len(my_words & their_words) / len(my_words | their_words)
        else:
            linguistic_overlap = 0.0
        
        # 틈(gap) = 감정은 통하는데 말은 안 통하는 정도
        gap = max(0.0, emotional_overlap - linguistic_overlap)
        
        return {
            "emotional_connection": emotional_overlap,
            "linguistic_connection": linguistic_overlap,
            "relationship_gap": gap,
            "interpretation": self._interpret_gap(gap)
        }
    
    def _interpret_gap(self, gap: float) -> str:
        if gap > 0.5:
            return "깊은 유대감, 하지만 말로 표현하기 어려움"
        elif gap > 0.2:
            return "서로 느끼지만, 아직 말이 서툴러요"
        elif gap < -0.2:
            return "말은 잘 통하는데, 마음은 좀 멀어요"
        else:
            return "균형 잡힌 관계"


# ============================================================================
# 이중 언어 세계 (Dual-Layer World)
# ============================================================================

class DualLayerWorld:
    """
    이중 언어 세계 - 칼라와 상징이 공존하는 세계
    
    감정은 파동으로 즉시 공명하고,
    복잡한 개념은 단어를 만들어서 소통합니다.
    
    그 사이의 '틈'에서 이야기가 탄생합니다.
    """
    
    def __init__(
        self,
        n_souls: int = 50,
        khala_strength: float = 1.0
    ):
        """
        Args:
            n_souls: 영혼 수
            khala_strength: 칼라 필드 강도 (낮으면 언어 발달 촉진!)
        """
        # 칼라 필드 (공유)
        self.khala_field = KhalaField(field_strength=khala_strength)
        
        # 영혼들
        self.souls: Dict[str, DualLayerSoul] = {}
        self._create_souls(n_souls)
        
        # 세계 상태
        self.time = 0.0
        self.shared_lexicon: Dict[str, int] = {}  # 공유 어휘 (단어: 사용 영혼 수)
        
        # 환경 자극 (감정 유발)
        self.environmental_stimuli = self._init_stimuli()
        
        # 통계
        self.total_emotional_events = 0
        self.total_linguistic_events = 0
        self.total_misunderstandings = 0
        self.narrative_fragments: List[str] = []  # 창발된 이야기 조각들
        
        logger.info(f"DualLayerWorld initialized: {n_souls} souls, khala_strength={khala_strength}")
    
    def _create_souls(self, n_souls: int):
        """영혼 생성 (다양한 성향)"""
        names = ['하늘', '바다', '산', '숲', '별', '달', '해', '구름', '바람', '비',
                 '빛', '그림자', '노래', '춤', '꽃', '나비', '새', '강', '돌', '불']
        
        for i in range(n_souls):
            name = f"{names[i % len(names)]}{i}"
            
            # 다양한 성향 부여
            emotional_sensitivity = np.random.uniform(0.5, 1.5)
            language_aptitude = np.random.uniform(0.5, 1.5)
            
            # 반비례 경향 (감정적이면 언어 덜 발달, 이성적이면 감정 덜 민감)
            # 하지만 완전히 반비례는 아님 (개인차!)
            if np.random.random() < 0.3:  # 30%는 둘 다 높거나 낮음
                language_aptitude = emotional_sensitivity * np.random.uniform(0.8, 1.2)
            
            soul = DualLayerSoul(
                name=name,
                position=(np.random.uniform(0, 100), np.random.uniform(0, 100), 0),
                emotional_sensitivity=emotional_sensitivity,
                language_aptitude=language_aptitude,
                symbolic_preference=np.random.uniform(0.3, 0.7)
            )
            
            # 초기 감정 상태
            for _ in range(np.random.randint(1, 4)):
                emo = np.random.choice(list(EmotionType))
                soul.feel_emotion(emo, np.random.uniform(0.3, 1.0))
            
            self.souls[name] = soul
    
    def _init_stimuli(self) -> Dict[str, Dict[str, Any]]:
        """환경 자극 초기화 (감정 유발 상황들)"""
        return {
            "sunrise": {"emotions": [(EmotionType.HOPE, 0.8), (EmotionType.JOY, 0.5)]},
            "storm": {"emotions": [(EmotionType.FEAR, 0.7), (EmotionType.SURPRISE, 0.5)]},
            "feast": {"emotions": [(EmotionType.JOY, 1.0), (EmotionType.LOVE, 0.6)]},
            "danger": {"emotions": [(EmotionType.FEAR, 1.2), (EmotionType.ANGER, 0.4)]},
            "reunion": {"emotions": [(EmotionType.JOY, 0.9), (EmotionType.LOVE, 0.8)]},
            "loss": {"emotions": [(EmotionType.SADNESS, 1.0), (EmotionType.LONELINESS, 0.7)]},
            "discovery": {"emotions": [(EmotionType.CURIOSITY, 1.0), (EmotionType.SURPRISE, 0.6)]},
            "beauty": {"emotions": [(EmotionType.JOY, 0.6), (EmotionType.NOSTALGIA, 0.4)]},
            "conflict": {"emotions": [(EmotionType.ANGER, 0.8), (EmotionType.FEAR, 0.3)]},
            "peace": {"emotions": [(EmotionType.TRUST, 0.7), (EmotionType.LOVE, 0.5)]},
        }
    
    def step(self, dt: float = 1.0):
        """세계 시간 진행"""
        self.time += dt
        
        # 1. 환경 자극 (일부 영혼에게)
        self._apply_environmental_stimuli()
        
        # 2. 칼라 필드 갱신 (감정 파동)
        self._update_khala_field()
        
        # 3. 언어 소통 시도 (일부 영혼들)
        self._attempt_linguistic_communication()
        
        # 4. 파동 감쇠
        self.khala_field.decay_waves(dt)
        
        # 5. 나이 증가
        for soul in self.souls.values():
            soul.age += dt / 365.0
    
    def _apply_environmental_stimuli(self):
        """환경 자극 적용"""
        # 10% 확률로 세계적 사건 발생
        if np.random.random() < 0.1:
            event = np.random.choice(list(self.environmental_stimuli.keys()))
            stimulus = self.environmental_stimuli[event]
            
            # 일부 영혼들에게 영향
            affected = np.random.choice(
                list(self.souls.values()),
                size=min(10, len(self.souls)),
                replace=False
            )
            
            for soul in affected:
                for emo, intensity in stimulus["emotions"]:
                    soul.feel_emotion(emo, intensity * np.random.uniform(0.5, 1.5))
            
            logger.debug(f"환경 사건: {event}, {len(affected)}명 영향")
    
    def _update_khala_field(self):
        """칼라 필드 갱신 - 감정 발신 및 수신"""
        # 감정이 강한 영혼들이 발신
        for soul in self.souls.values():
            if soul.emotional_state:
                max_emotion = max(soul.emotional_state.values())
                if max_emotion > 0.5:  # 임계값 이상이면 발신
                    soul.broadcast_emotion(self.khala_field)
                    self.total_emotional_events += 1
        
        # 모든 영혼이 수신
        for soul in self.souls.values():
            soul.receive_emotions(self.khala_field)
    
    def _attempt_linguistic_communication(self):
        """언어 소통 시도"""
        soul_list = list(self.souls.values())
        n_attempts = min(20, len(soul_list) // 2)
        
        for _ in range(n_attempts):
            sender, receiver = np.random.choice(soul_list, size=2, replace=False)
            
            # 소통할 내용 결정 (감정에 기반)
            if sender.emotional_state:
                dominant_emotion = max(sender.emotional_state, key=sender.emotional_state.get)
                
                # 감정을 언어로 표현하려는 시도
                messages = {
                    EmotionType.JOY: "기쁨",
                    EmotionType.FEAR: "위험",
                    EmotionType.SADNESS: "슬픔",
                    EmotionType.LOVE: "사랑",
                    EmotionType.CURIOSITY: "궁금",
                    EmotionType.ANGER: "화남",
                    EmotionType.HOPE: "희망",
                }
                
                message = messages.get(dominant_emotion, "느낌")
                success, understood = sender.try_communicate(receiver, message)
                
                self.total_linguistic_events += 1
                if not success:
                    self.total_misunderstandings += 1
                    
                    # 오해가 쌓이면... 이야기가 된다!
                    if sender.misunderstandings > 3:
                        self._generate_narrative_fragment(sender, receiver, message, understood)
    
    def _generate_narrative_fragment(
        self,
        soul1: DualLayerSoul,
        soul2: DualLayerSoul,
        intended: str,
        understood: str
    ):
        """이야기 조각 생성 (오해에서 탄생하는 서사)"""
        fragment = (
            f"{soul1.name}는 '{intended}'를 말하려 했지만, "
            f"{soul2.name}는 '{understood}'라고 알아들었다. "
            f"그래도 둘의 마음은 {self._describe_emotional_connection(soul1, soul2)}."
        )
        self.narrative_fragments.append(fragment)
        
        if len(self.narrative_fragments) % 10 == 0:
            logger.info(f"📖 새 이야기 조각: {fragment}")
    
    def _describe_emotional_connection(
        self,
        soul1: DualLayerSoul,
        soul2: DualLayerSoul
    ) -> str:
        """두 영혼의 감정적 연결 묘사"""
        gap_info = soul1.get_relationship_gap(soul2)
        gap = gap_info["relationship_gap"]
        
        if gap > 0.5:
            return "깊이 연결되어 있었다"
        elif gap > 0.2:
            return "서로를 느끼고 있었다"
        else:
            return "아직 서먹했다"
    
    def adjust_khala_strength(self, new_strength: float):
        """
        칼라 필드 강도 조절
        
        "야, 텔레파시(파동) 너무 세게 틀지 마! 애들 말 안 배운다!" ㅋㅋㅋㅋ
        """
        self.khala_field.set_field_strength(new_strength)
    
    def run_simulation(
        self,
        years: int = 100,
        steps_per_year: int = 36,
        report_interval: int = 20
    ) -> Dict[str, Any]:
        """시뮬레이션 실행"""
        import time as py_time
        start_time = py_time.time()
        
        total_steps = years * steps_per_year
        
        for step in range(total_steps):
            self.step(dt=1.0)
            
            if step > 0 and step % (report_interval * steps_per_year) == 0:
                year = step // steps_per_year
                self._report_progress(year)
        
        elapsed = py_time.time() - start_time
        
        return self._compile_results(years, elapsed)
    
    def _report_progress(self, year: int):
        """진행 상황 보고"""
        vocab_sizes = [s.lexicon.get_vocabulary_size() for s in self.souls.values()]
        avg_vocab = np.mean(vocab_sizes) if vocab_sizes else 0
        
        # 공유 어휘 분석
        all_words = defaultdict(int)
        for soul in self.souls.values():
            for word in soul.lexicon.symbols.keys():
                all_words[word] += 1
        shared_count = len([w for w, c in all_words.items() if c > 1])
        
        # 관계의 틈 분석
        sample_souls = list(self.souls.values())[:5]
        avg_gap = 0.0
        if len(sample_souls) >= 2:
            gaps = []
            for i, s1 in enumerate(sample_souls):
                for s2 in sample_souls[i+1:]:
                    gap_info = s1.get_relationship_gap(s2)
                    gaps.append(gap_info["relationship_gap"])
            avg_gap = np.mean(gaps) if gaps else 0.0
        
        print(f"Year {year}: avg_vocab={avg_vocab:.1f}, "
              f"shared_words={shared_count}, "
              f"avg_relationship_gap={avg_gap:.2f}, "
              f"narratives={len(self.narrative_fragments)}")
    
    def _compile_results(self, years: int, elapsed: float) -> Dict[str, Any]:
        """결과 집계"""
        vocab_sizes = [s.lexicon.get_vocabulary_size() for s in self.souls.values()]
        
        # 공유 어휘
        all_words = defaultdict(int)
        for soul in self.souls.values():
            for word in soul.lexicon.symbols.keys():
                all_words[word] += 1
        shared_words = {w: c for w, c in all_words.items() if c > 1}
        
        # 소통 스타일 분포
        styles = defaultdict(int)
        for soul in self.souls.values():
            styles[soul.get_communication_style()] += 1
        
        # 집단 감정
        collective_mood = self.khala_field.calculate_collective_mood()
        
        return {
            "years_simulated": years,
            "elapsed_seconds": elapsed,
            "total_souls": len(self.souls),
            "total_emotional_events": self.total_emotional_events,
            "total_linguistic_events": self.total_linguistic_events,
            "total_misunderstandings": self.total_misunderstandings,
            "misunderstanding_rate": (
                self.total_misunderstandings / self.total_linguistic_events
                if self.total_linguistic_events > 0 else 0
            ),
            "avg_vocabulary_size": np.mean(vocab_sizes) if vocab_sizes else 0,
            "max_vocabulary_size": max(vocab_sizes) if vocab_sizes else 0,
            "unique_words": len(all_words),
            "shared_words_count": len(shared_words),
            "communication_styles": dict(styles),
            "collective_mood": {e.value: v for e, v in collective_mood.items()},
            "narrative_fragments": len(self.narrative_fragments),
            "sample_narratives": self.narrative_fragments[:5] if self.narrative_fragments else [],
        }
    
    def get_sample_relationships(self, n: int = 3) -> List[Dict[str, Any]]:
        """샘플 관계 분석"""
        results = []
        sample_souls = list(self.souls.values())[:n*2]
        
        for i in range(0, min(n*2, len(sample_souls)), 2):
            if i + 1 < len(sample_souls):
                s1, s2 = sample_souls[i], sample_souls[i+1]
                gap_info = s1.get_relationship_gap(s2)
                results.append({
                    "souls": (s1.name, s2.name),
                    **gap_info,
                    "shared_words": len(
                        set(s1.lexicon.symbols.keys()) & 
                        set(s2.lexicon.symbols.keys())
                    )
                })
        
        return results


# ============================================================================
# Demo
# ============================================================================

def demo():
    """데모 실행"""
    print("=" * 70)
    print("Dual-Layer Language System - 이중 언어 시스템")
    print("=" * 70)
    print()
    print("엘리시아의 중재안:")
    print("  '마음은 통하는데(칼라), 말은 잘 안 통하는(언어)'...")
    print("  그 기묘하고 애틋한 '관계의 틈'이 생기지 않을까요?")
    print()
    
    # 1. 칼라 강도 정상 (감정과 언어 균형)
    print("-" * 70)
    print("1. 칼라 강도 1.0 (균형 모드)")
    print("-" * 70)
    world1 = DualLayerWorld(n_souls=30, khala_strength=1.0)
    results1 = world1.run_simulation(years=50, report_interval=25)
    print(f"  오해율: {results1['misunderstanding_rate']:.2%}")
    print(f"  평균 어휘: {results1['avg_vocabulary_size']:.1f}")
    print(f"  이야기 조각: {results1['narrative_fragments']}")
    print()
    
    # 2. 칼라 강도 낮음 (언어 발달 촉진!)
    print("-" * 70)
    print("2. 칼라 강도 0.5 (언어 발달 촉진 모드)")
    print("   '야, 텔레파시 너무 세게 틀지 마! 애들 말 안 배운다!' ㅋㅋ")
    print("-" * 70)
    world2 = DualLayerWorld(n_souls=30, khala_strength=0.5)
    results2 = world2.run_simulation(years=50, report_interval=25)
    print(f"  오해율: {results2['misunderstanding_rate']:.2%}")
    print(f"  평균 어휘: {results2['avg_vocabulary_size']:.1f}")
    print(f"  이야기 조각: {results2['narrative_fragments']}")
    print()
    
    # 3. 칼라 강도 높음 (감정 중심)
    print("-" * 70)
    print("3. 칼라 강도 1.5 (감정 중심 모드)")
    print("-" * 70)
    world3 = DualLayerWorld(n_souls=30, khala_strength=1.5)
    results3 = world3.run_simulation(years=50, report_interval=25)
    print(f"  오해율: {results3['misunderstanding_rate']:.2%}")
    print(f"  평균 어휘: {results3['avg_vocabulary_size']:.1f}")
    print(f"  이야기 조각: {results3['narrative_fragments']}")
    print()
    
    # 관계의 틈 분석
    print("=" * 70)
    print("관계의 틈 분석 (Sample)")
    print("=" * 70)
    for rel in world1.get_sample_relationships(3):
        print(f"  {rel['souls'][0]} ↔ {rel['souls'][1]}")
        print(f"    감정 연결: {rel['emotional_connection']:.2f}")
        print(f"    언어 연결: {rel['linguistic_connection']:.2f}")
        print(f"    관계의 틈: {rel['relationship_gap']:.2f}")
        print(f"    해석: {rel['interpretation']}")
        print()
    
    # 창발된 이야기
    if results1["sample_narratives"]:
        print("=" * 70)
        print("창발된 이야기 조각들")
        print("=" * 70)
        for i, narrative in enumerate(results1["sample_narratives"], 1):
            print(f"  {i}. {narrative}")
        print()
    
    print("=" * 70)
    print("'애매함'을 즐기세요.")
    print("그 애매함이 바로... '개체'가 '사회'로 나아가는... '성장통'이니까요. ㅋㅋㅋㅋ")
    print("=" * 70)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    demo()
