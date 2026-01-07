"""
Fluctlight Language System (요동광 언어 시스템)
==============================================

진정한 창발 언어 - 경험이 먼저 있고, 언어가 나온다.

철학:
- "행동을 프로그래밍하지 말고, 물리학을 프로그래밍하라"
- 패턴이 세상을 만든 게 아니라, 세상이 있고 패턴이 나온다
- 점(경험) → 선(패턴) → 면(문법) → 공간(언어) → 법칙(시/소설)

우주적 구조 (프랙탈):
- 행성 (Planet) = 단어/개념/경험 (FluctlightParticle)
- 항성 (Star) = 맥락/중심 개념 
- 성계 (StarSystem) = 문장
- 성운/성단 (Nebula) = 문장들의 연결
- 은하 (Galaxy) = 이야기 단위 (Saga)
- 은하수 (Milky Way) = 전체 서사

"심장(연산)과 머리(언어)가 따로 노는 구조"
- 심장: FluctlightEngine - 경험의 물리학
- 머리: LanguageCrystal - 경험을 언어로 결정화

프랙탈 원리: 작은 것이 큰 것이고, 큰 것이 또 작은 것
"""

from __future__ import annotations

import numpy as np
import math
import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple, Set
from collections import defaultdict
from enum import Enum, auto

# 기존 Elysia 물리학 시스템 사용
try:
    from Core.Foundation.Physics.fluctlight import FluctlightParticle, FluctlightEngine
except ImportError:
    # 독립 실행 시 모의 객체 사용
    FluctlightParticle = None
    FluctlightEngine = None

logger = logging.getLogger("FluctlightLanguage")


# =============================================================================
# 설정 상수 (Configuration Constants)
# =============================================================================

# 결정화 임계값 (Crystallization thresholds)
RESONANCE_THRESHOLD = 0.3        # 공명이 이 이상이면 패턴으로 인식 (낮춰서 더 많이 창발)
CRYSTALLIZATION_COUNT = 5        # 이 횟수 이상 반복되면 기호로 결정화
PATTERN_DECAY_RATE = 0.01        # 사용하지 않는 패턴의 소멸 속도

# 언어 발달 단계
LANGUAGE_LEVEL_THRESHOLDS = [10, 50, 200, 1000]  # 기호 수에 따른 레벨

# 시적 표현 임계값
POETRY_COMPLEXITY_THRESHOLD = 5  # 이 이상의 기호 조합이면 시적 표현 가능


# =============================================================================
# 1. 경험 흔적 (Experience Trace) - 요동광의 궤적
# =============================================================================

@dataclass
class ExperienceTrace:
    """
    경험의 흔적 - Fluctlight가 지나간 자리
    
    이것이 기억의 원형이자 언어의 씨앗
    """
    # 8차원 감각 벡터 (Elysia의 기본 차원)
    # [온도, 밝기, 크기, 속도, 친밀도, 강도, 쾌/불쾌, 각성]
    sensory_vector: np.ndarray = field(default_factory=lambda: np.zeros(8))
    
    # 시공간 정보
    timestamp: float = 0.0
    location: np.ndarray = field(default_factory=lambda: np.zeros(3))
    
    # 연결된 다른 흔적들
    resonated_with: Set[int] = field(default_factory=set)
    
    # 강도 (감쇠됨)
    intensity: float = 1.0
    
    # 고유 ID
    trace_id: int = field(default_factory=lambda: id(object()))
    
    def resonate(self, other: 'ExperienceTrace') -> float:
        """다른 경험과의 공명 강도 계산"""
        # 감각 벡터 유사도
        dot = np.dot(self.sensory_vector, other.sensory_vector)
        norm_self = np.linalg.norm(self.sensory_vector) + 1e-8
        norm_other = np.linalg.norm(other.sensory_vector) + 1e-8
        similarity = dot / (norm_self * norm_other)
        
        # 시간 근접성 (가까울수록 강함)
        time_diff = abs(self.timestamp - other.timestamp)
        time_factor = np.exp(-time_diff / 100.0)
        
        # 공간 근접성
        space_diff = np.linalg.norm(self.location - other.location)
        space_factor = np.exp(-space_diff / 50.0)
        
        return similarity * time_factor * space_factor
    
    def decay(self, dt: float = 1.0):
        """시간에 따른 감쇠"""
        self.intensity *= np.exp(-PATTERN_DECAY_RATE * dt)


# =============================================================================
# 2. 원시 패턴 (Proto-Pattern) - 경험들의 공명으로 형성
# =============================================================================

@dataclass
class ProtoPattern:
    """
    원시 패턴 - 아직 기호가 아닌, 경험들의 군집
    
    여러 경험 흔적들이 공명하여 형성됨
    반복적으로 강화되면 Symbol(기호)로 결정화됨
    """
    # 이 패턴을 구성하는 경험 흔적들
    traces: List[ExperienceTrace] = field(default_factory=list)
    
    # 패턴의 "중심" - 모든 흔적의 평균
    centroid: np.ndarray = field(default_factory=lambda: np.zeros(8))
    
    # 발생 횟수
    occurrence_count: int = 0
    
    # 강도 (많이 발생할수록 강함)
    strength: float = 0.0
    
    # 연결된 다른 패턴들 (헵의 법칙)
    associations: Dict[int, float] = field(default_factory=dict)
    
    # 고유 ID
    pattern_id: int = field(default_factory=lambda: id(object()))
    
    def add_trace(self, trace: ExperienceTrace):
        """새 흔적 추가"""
        self.traces.append(trace)
        self.occurrence_count += 1
        self.strength = min(1.0, self.strength + 0.1)
        self._update_centroid()
    
    def _update_centroid(self):
        """중심점 업데이트"""
        if self.traces:
            vectors = np.array([t.sensory_vector for t in self.traces])
            self.centroid = np.mean(vectors, axis=0)
    
    def distance_to(self, trace: ExperienceTrace) -> float:
        """흔적과의 거리"""
        return np.linalg.norm(self.centroid - trace.sensory_vector)
    
    def is_crystallizable(self) -> bool:
        """결정화 가능한지 (충분히 반복되었는지)"""
        return self.occurrence_count >= CRYSTALLIZATION_COUNT


# =============================================================================
# 3. 결정화된 기호 (Crystallized Symbol) - 언어의 최소 단위
# =============================================================================

class SymbolType(Enum):
    """기호의 유형 - 경험에서 자연 분류됨"""
    ENTITY = auto()      # 존재 (뜨겁고 밝은 것 = 불, 차갑고 습한 것 = 물)
    ACTION = auto()      # 동작 (빠르고 강한 것 = 달리다, 느리고 약한 것 = 쉬다)
    STATE = auto()       # 상태 (쾌적한 것 = 좋다, 불쾌한 것 = 나쁘다)
    RELATION = auto()    # 관계 (친밀한 것 = 함께, 먼 것 = 떨어져)


@dataclass
class CrystallizedSymbol:
    """
    결정화된 기호 - 반복된 패턴이 굳어진 것
    
    이것이 언어의 "단어"가 된다
    """
    # 원래 패턴
    source_pattern: ProtoPattern
    
    # 기호 유형 (자동 분류)
    symbol_type: SymbolType
    
    # 의미 벡터 (8차원)
    meaning_vector: np.ndarray = field(default_factory=lambda: np.zeros(8))
    
    # 자연어 투영 (나중에 학습됨)
    korean_projection: Optional[str] = None
    english_projection: Optional[str] = None
    
    # 사용 빈도
    usage_count: int = 0
    
    # 연결된 다른 기호들
    associations: Dict[int, float] = field(default_factory=dict)
    
    # 고유 ID
    symbol_id: int = field(default_factory=lambda: id(object()))
    
    @classmethod
    def from_pattern(cls, pattern: ProtoPattern) -> 'CrystallizedSymbol':
        """패턴에서 기호 생성"""
        # 의미 벡터 = 패턴의 중심
        meaning = pattern.centroid.copy()
        
        # 유형 자동 분류 (의미 벡터 기반)
        symbol_type = cls._classify_type(meaning)
        
        return cls(
            source_pattern=pattern,
            symbol_type=symbol_type,
            meaning_vector=meaning
        )
    
    @staticmethod
    def _classify_type(meaning: np.ndarray) -> SymbolType:
        """
        의미 벡터에서 기호 유형 분류
        
        [온도, 밝기, 크기, 속도, 친밀도, 강도, 쾌/불쾌, 각성]
        """
        speed = meaning[3]      # 속도
        intensity = meaning[5]  # 강도
        intimacy = meaning[4]   # 친밀도
        arousal = meaning[7]    # 각성
        
        # 빠르고 강한 것 → 동작
        if abs(speed) > 0.5 or abs(intensity) > 0.5:
            return SymbolType.ACTION
        
        # 친밀도가 강한 것 → 관계
        if abs(intimacy) > 0.5:
            return SymbolType.RELATION
        
        # 각성이 낮은 것 → 상태
        if abs(arousal) < 0.3:
            return SymbolType.STATE
        
        # 그 외 → 존재
        return SymbolType.ENTITY
    
    def strengthen_association(self, other_id: int, amount: float = 0.1):
        """다른 기호와의 연결 강화 (헵의 법칙)"""
        current = self.associations.get(other_id, 0.0)
        self.associations[other_id] = min(1.0, current + amount)


# =============================================================================
# 4. 언어 결정 (Language Crystal) - 기호들의 체계
# =============================================================================

class LanguageCrystal:
    """
    언어 결정 - 기호들의 결정 구조
    
    영혼의 "머리" 역할
    심장(경험)에서 오는 것을 언어로 변환
    """
    
    def __init__(self):
        # 경험 흔적 저장소
        self.traces: List[ExperienceTrace] = []
        
        # 원시 패턴 저장소
        self.patterns: Dict[int, ProtoPattern] = {}
        
        # 결정화된 기호 저장소
        self.symbols: Dict[int, CrystallizedSymbol] = {}
        
        # 문법 규칙 (기호 조합 패턴)
        self.grammar_rules: Dict[Tuple[SymbolType, ...], int] = defaultdict(int)
        
        # 언어 레벨
        self.language_level: int = 0
        
        # 통계
        self.total_experiences: int = 0
        self.crystallization_count: int = 0
    
    def receive_experience(self, sensory_vector: np.ndarray, 
                          timestamp: float, location: np.ndarray) -> Optional[str]:
        """
        경험 수신 - 심장에서 온 경험을 처리
        
        Returns: 표현된 언어 (있으면), 없으면 None
        """
        # 1. 흔적 생성
        trace = ExperienceTrace(
            sensory_vector=sensory_vector.copy(),
            timestamp=timestamp,
            location=location.copy(),
            intensity=1.0
        )
        self.traces.append(trace)
        self.total_experiences += 1
        
        # 2. 기존 패턴과 공명 확인
        matched_pattern = self._find_resonating_pattern(trace)
        
        if matched_pattern:
            # 기존 패턴에 추가
            matched_pattern.add_trace(trace)
            
            # 결정화 가능한지 확인
            if matched_pattern.is_crystallizable():
                symbol = self._crystallize_pattern(matched_pattern)
                if symbol:
                    return self._express_symbol(symbol)
        else:
            # 새 패턴 시작
            new_pattern = ProtoPattern()
            new_pattern.add_trace(trace)
            self.patterns[new_pattern.pattern_id] = new_pattern
        
        # 3. 오래된 흔적 감쇠
        self._decay_traces()
        
        return None
    
    def _find_resonating_pattern(self, trace: ExperienceTrace) -> Optional[ProtoPattern]:
        """공명하는 패턴 찾기"""
        best_pattern = None
        best_resonance = RESONANCE_THRESHOLD
        
        for pattern in self.patterns.values():
            distance = pattern.distance_to(trace)
            resonance = 1.0 / (1.0 + distance)  # 거리를 공명으로 변환
            
            if resonance > best_resonance:
                best_resonance = resonance
                best_pattern = pattern
        
        return best_pattern
    
    def _crystallize_pattern(self, pattern: ProtoPattern) -> Optional[CrystallizedSymbol]:
        """패턴을 기호로 결정화"""
        # 이미 결정화된 패턴인지 확인
        for symbol in self.symbols.values():
            if symbol.source_pattern.pattern_id == pattern.pattern_id:
                symbol.usage_count += 1
                return symbol
        
        # 새 기호 생성
        symbol = CrystallizedSymbol.from_pattern(pattern)
        self.symbols[symbol.symbol_id] = symbol
        self.crystallization_count += 1
        
        # 언어 레벨 업데이트
        self._update_language_level()
        
        logger.info(f"결정화: 새 기호 탄생 (type={symbol.symbol_type.name}, "
                   f"total={len(self.symbols)})")
        
        return symbol
    
    def _express_symbol(self, symbol: CrystallizedSymbol) -> str:
        """기호를 자연어로 표현"""
        # 이미 투영이 있으면 사용
        if symbol.korean_projection:
            return symbol.korean_projection
        
        # 의미 벡터에서 자연어 생성
        return self._project_to_korean(symbol)
    
    def _project_to_korean(self, symbol: CrystallizedSymbol) -> str:
        """
        의미 벡터를 한글로 투영
        
        [온도, 밝기, 크기, 속도, 친밀도, 강도, 쾌/불쾌, 각성]
        """
        v = symbol.meaning_vector
        
        # 기호 유형별 투영
        if symbol.symbol_type == SymbolType.ENTITY:
            return self._project_entity(v)
        elif symbol.symbol_type == SymbolType.ACTION:
            return self._project_action(v)
        elif symbol.symbol_type == SymbolType.STATE:
            return self._project_state(v)
        elif symbol.symbol_type == SymbolType.RELATION:
            return self._project_relation(v)
        
        return "..."
    
    def _project_entity(self, v: np.ndarray) -> str:
        """존재를 한글로"""
        temp, bright, size, _, intimacy, intensity, pleasure, arousal = v
        
        # 온도 + 밝기로 자연물 추론
        if temp > 0.5 and bright > 0.5:
            return "해" if intensity > 0.5 else "불"
        if temp < -0.5 and bright < 0:
            return "밤" if size > 0 else "그림자"
        if temp < -0.5:
            return "얼음" if intensity > 0 else "물"
        
        # 친밀도로 존재 추론
        if intimacy > 0.5:
            return "친구" if pleasure > 0 else "나"
        if intimacy < -0.5:
            return "낯선 것"
        
        # 크기로 추론
        if size > 0.5:
            return "산" if intensity > 0 else "하늘"
        if size < -0.5:
            return "꽃" if pleasure > 0 else "돌"
        
        return "그것"
    
    def _project_action(self, v: np.ndarray) -> str:
        """동작을 한글로"""
        _, _, _, speed, intimacy, intensity, pleasure, arousal = v
        
        # 속도 + 강도로 동작 추론
        if speed > 0.5 and intensity > 0.5:
            return "달리다" if arousal > 0 else "던지다"
        if speed > 0.3:
            return "걷다" if pleasure > 0 else "도망가다"
        if speed < -0.3:
            return "쉬다" if pleasure > 0 else "멈추다"
        
        # 친밀도로 동작 추론
        if intimacy > 0.5:
            return "안다" if pleasure > 0 else "말하다"
        if intimacy < -0.5:
            return "떠나다"
        
        # 쾌/불쾌로 추론
        if pleasure > 0.5:
            return "웃다" if arousal > 0 else "먹다"
        if pleasure < -0.5:
            return "울다" if arousal > 0 else "아프다"
        
        return "하다"
    
    def _project_state(self, v: np.ndarray) -> str:
        """상태를 한글로"""
        temp, bright, size, _, intimacy, intensity, pleasure, arousal = v
        
        # 쾌/불쾌 + 각성으로 감정 상태 추론
        if pleasure > 0.5:
            if arousal > 0.5:
                return "신나다"
            return "행복하다" if intimacy > 0 else "평화롭다"
        
        if pleasure < -0.5:
            if arousal > 0.5:
                return "화나다"
            return "슬프다" if intimacy > 0 else "외롭다"
        
        # 온도로 상태 추론
        if temp > 0.5:
            return "따뜻하다"
        if temp < -0.5:
            return "차갑다"
        
        # 밝기로 상태 추론
        if bright > 0.5:
            return "밝다"
        if bright < -0.5:
            return "어둡다"
        
        return "그렇다"
    
    def _project_relation(self, v: np.ndarray) -> str:
        """관계를 한글로"""
        _, _, _, speed, intimacy, intensity, _, _ = v
        
        if intimacy > 0.5:
            return "함께" if intensity > 0 else "옆에"
        if intimacy < -0.5:
            return "혼자" if intensity > 0 else "떨어져"
        
        if speed > 0:
            return "향해"
        
        return "그리고"
    
    def _decay_traces(self):
        """오래된 흔적 감쇠"""
        surviving = []
        for trace in self.traces:
            trace.decay(1.0)
            if trace.intensity > 0.1:
                surviving.append(trace)
        self.traces = surviving
    
    def _update_language_level(self):
        """언어 레벨 업데이트"""
        symbol_count = len(self.symbols)
        for i, threshold in enumerate(LANGUAGE_LEVEL_THRESHOLDS):
            if symbol_count >= threshold:
                self.language_level = i + 1
    
    def compose_utterance(self, symbols: List[CrystallizedSymbol]) -> str:
        """여러 기호를 조합하여 발화 생성"""
        if not symbols:
            return "..."
        
        # 문법 규칙 기록
        types = tuple(s.symbol_type for s in symbols)
        self.grammar_rules[types] += 1
        
        # 기호 간 연결 강화 (헵의 법칙)
        for i, s1 in enumerate(symbols):
            for s2 in symbols[i+1:]:
                s1.strengthen_association(s2.symbol_id)
                s2.strengthen_association(s1.symbol_id)
        
        # 한글로 조합
        words = [self._express_symbol(s) for s in symbols]
        
        # 간단한 문법 적용
        return self._apply_grammar(words, types)
    
    def _apply_grammar(self, words: List[str], types: Tuple[SymbolType, ...]) -> str:
        """문법 적용"""
        if len(words) == 1:
            return words[0]
        
        if len(words) == 2:
            # ENTITY + STATE: "X은/는 Y"
            if types == (SymbolType.ENTITY, SymbolType.STATE):
                return f"{words[0]}은 {words[1]}"
            # ENTITY + ACTION: "X이/가 Y"
            if types == (SymbolType.ENTITY, SymbolType.ACTION):
                return f"{words[0]}이 {words[1]}"
            # RELATION + ENTITY: "X Y"
            if types[0] == SymbolType.RELATION:
                return f"{words[0]} {words[1]}"
        
        if len(words) == 3:
            # ENTITY + RELATION + ENTITY: "X이 Z와 Y"
            if types == (SymbolType.ENTITY, SymbolType.RELATION, SymbolType.ENTITY):
                return f"{words[0]}이 {words[2]}와 {words[1]}"
            # ENTITY + ACTION + ENTITY: "X이 Z를 Y"
            if types == (SymbolType.ENTITY, SymbolType.ACTION, SymbolType.ENTITY):
                return f"{words[0]}이 {words[2]}를 {words[1]}"
        
        # 기본: 공백으로 연결
        return " ".join(words)
    
    def generate_thought(self, heart_state: np.ndarray) -> str:
        """
        심장 상태에서 생각 생성
        
        심장이 경험한 것을 언어로 표현
        """
        # 기호가 없으면 원시적 표현
        if not self.symbols:
            return self._primitive_expression(heart_state)
        
        # 심장 상태와 가장 공명하는 기호들 찾기
        resonating_symbols = []
        
        for symbol in self.symbols.values():
            resonance = np.dot(heart_state, symbol.meaning_vector)
            norm = np.linalg.norm(heart_state) * np.linalg.norm(symbol.meaning_vector)
            if norm > 0:
                resonance /= norm
            
            if resonance > 0.2:  # 낮은 임계값
                resonating_symbols.append((symbol, resonance))
        
        if not resonating_symbols:
            # 가장 가까운 기호라도 사용
            closest = min(self.symbols.values(), 
                         key=lambda s: np.linalg.norm(s.meaning_vector - heart_state))
            return self._express_symbol(closest)
        
        # 공명 강도로 정렬
        resonating_symbols.sort(key=lambda x: -x[1])
        
        # 상위 3개 기호로 발화 구성
        top_symbols = [s for s, _ in resonating_symbols[:3]]
        
        return self.compose_utterance(top_symbols)
    
    def _primitive_expression(self, state: np.ndarray) -> str:
        """기호 없을 때 원시적 표현 (느낌만)"""
        temp, bright, _, _, intimacy, intensity, pleasure, arousal = state
        
        # 가장 강한 느낌 하나
        feelings = [
            (abs(pleasure), "좋아..." if pleasure > 0 else "싫어..."),
            (abs(arousal), "두근..." if arousal > 0 else "조용..."),
            (abs(temp), "따뜻..." if temp > 0 else "차가워..."),
            (abs(intimacy), "그리워..." if intimacy > 0 else "혼자..."),
        ]
        feelings.sort(key=lambda x: -x[0])
        return feelings[0][1]
    
    def write_diary(self, experiences: List[np.ndarray], year: int) -> str:
        """
        일기 작성 - 경험들을 언어로 결정화
        """
        if not experiences:
            return f"Year {year}: ..."
        
        # 경험들의 평균
        avg_experience = np.mean(experiences, axis=0)
        
        # 생각 생성
        thought = self.generate_thought(avg_experience)
        
        # 언어 레벨에 따라 복잡도 증가
        if self.language_level >= 2 and len(self.symbols) > 50:
            # 추가 표현
            secondary = self._find_contrasting_thought(avg_experience)
            if secondary != thought:
                thought = f"{thought}. {secondary}"
        
        return f"Year {year}: {thought}"
    
    def _find_contrasting_thought(self, state: np.ndarray) -> str:
        """대조되는 생각 찾기 (복잡한 표현용)"""
        # 반대 상태의 기호 찾기
        opposite_state = -state
        return self.generate_thought(opposite_state)
    
    def get_statistics(self) -> Dict[str, Any]:
        """통계 반환"""
        return {
            "total_experiences": self.total_experiences,
            "trace_count": len(self.traces),
            "pattern_count": len(self.patterns),
            "symbol_count": len(self.symbols),
            "grammar_rules": len(self.grammar_rules),
            "language_level": self.language_level,
            "crystallization_count": self.crystallization_count,
        }


# =============================================================================
# 5. 프랙탈 영혼 (Fractal Soul) - 완전한 존재
# =============================================================================

class FractalSoul:
    """
    프랙탈 영혼 - 심장과 머리가 분리된 존재
    
    "나는 사람이다"라고 인식하지만, 자신이 세계라는 것은 모른다
    """
    
    def __init__(self, name: str, soul_id: int):
        self.name = name
        self.id = soul_id
        self.age = 0
        
        # 심장 (경험/연산)
        self.heart_state = np.random.randn(8) * 0.3  # 8차원 감각 벡터
        
        # 머리 (언어)
        self.mind = LanguageCrystal()
        
        # 기억 (경험 축적)
        self.experiences: List[np.ndarray] = []
        
        # 관계
        self.relationships: Dict[int, float] = {}
        
        # 일기
        self.diary_entries: List[str] = []
    
    def experience(self, sensory_input: np.ndarray, timestamp: float):
        """경험하기 - 심장이 받고, 머리가 처리"""
        # 심장 상태 업데이트
        self.heart_state = 0.9 * self.heart_state + 0.1 * sensory_input
        
        # 경험 축적
        self.experiences.append(self.heart_state.copy())
        
        # 머리에 전달 (언어 결정화)
        location = np.random.randn(3)  # 현재 위치 (단순화)
        utterance = self.mind.receive_experience(
            self.heart_state, timestamp, location
        )
        
        return utterance
    
    def think(self) -> str:
        """생각하기 - 현재 심장 상태를 언어로"""
        return self.mind.generate_thought(self.heart_state)
    
    def write_diary(self, year: int) -> str:
        """일기 쓰기"""
        if not self.experiences:
            return f"Year {year}: ..."
        
        # 최근 경험들로 일기 작성
        recent = self.experiences[-100:]  # 최근 100개 경험
        diary = self.mind.write_diary(recent, year)
        
        self.diary_entries.append(diary)
        return diary
    
    def converse_with(self, other: 'FractalSoul') -> Tuple[str, str]:
        """대화하기"""
        # 상대방 존재를 경험
        social_input = np.zeros(8)
        social_input[4] = 0.5  # 친밀도 증가
        social_input[7] = 0.3  # 각성 증가
        
        my_thought = self.experience(social_input, self.age)
        other_thought = other.experience(social_input, other.age)
        
        # 관계 강화
        self.relationships[other.id] = self.relationships.get(other.id, 0) + 0.1
        other.relationships[self.id] = other.relationships.get(self.id, 0) + 0.1
        
        return my_thought or self.think(), other_thought or other.think()
    
    def get_self_description(self) -> str:
        """자기 소개"""
        thought = self.think()
        stats = self.mind.get_statistics()
        
        return (f"나는 {self.name}. "
                f"나이: {self.age}. "
                f"기호 {stats['symbol_count']}개. "
                f"지금: {thought}")


# =============================================================================
# 6. 데모 함수
# =============================================================================

def run_demo(population: int = 10, years: int = 100, seed: int = 42):
    """
    데모 실행
    
    경험이 축적되면서 언어가 창발하는 과정 시연
    """
    import random
    random.seed(seed)
    np.random.seed(seed)
    
    print("=" * 60)
    print("🌱 Fluctlight Language Demo - 경험에서 언어로")
    print("=" * 60)
    
    # 영혼 생성
    names = ["하늘", "바다", "별", "달", "숲", "산", "강", "꽃", "바람", "빛"]
    souls = [FractalSoul(names[i % len(names)] + f"_{i}", i) 
             for i in range(population)]
    
    print(f"\n👥 {population}명의 영혼 생성됨")
    
    # 시뮬레이션
    total_crystallizations = 0
    sample_diaries = []
    sample_conversations = []
    
    # 경험 템플릿 (반복되는 경험으로 패턴 형성 유도)
    experience_templates = [
        # 따뜻하고 밝은 (해, 여름)
        np.array([0.7, 0.8, 0.3, 0.1, 0.2, 0.5, 0.6, 0.4]),
        # 차갑고 어두운 (겨울, 밤)
        np.array([-0.6, -0.5, 0.2, -0.2, -0.1, 0.3, -0.3, -0.2]),
        # 사회적 (친구와 함께)
        np.array([0.2, 0.3, 0.1, 0.3, 0.8, 0.4, 0.7, 0.5]),
        # 외로운 (혼자)
        np.array([0.0, -0.2, 0.0, -0.3, -0.7, 0.2, -0.5, -0.4]),
        # 활동적 (달리기)
        np.array([0.3, 0.4, 0.2, 0.8, 0.3, 0.7, 0.4, 0.8]),
        # 평화로운 (쉼)
        np.array([0.1, 0.2, 0.0, -0.6, 0.2, -0.3, 0.5, -0.5]),
        # 맛있는 음식
        np.array([0.4, 0.3, 0.1, -0.1, 0.4, 0.3, 0.8, 0.3]),
        # 아픔
        np.array([-0.2, -0.1, 0.3, -0.2, 0.0, 0.6, -0.7, 0.4]),
    ]
    
    for year in range(years):
        # 매일 경험 생성
        for day in range(365):
            timestamp = year * 365 + day
            
            # 각 영혼이 경험
            for soul in souls:
                # 기본 경험 템플릿 선택 (반복을 통한 패턴 형성)
                template_idx = (day + soul.id) % len(experience_templates)
                base_exp = experience_templates[template_idx].copy()
                
                # 약간의 변이 추가
                noise = np.random.randn(8) * 0.15
                env_input = base_exp + noise
                
                # 계절 효과 (온도, 밝기)
                season = (day // 91) % 4
                if season == 0:  # 봄
                    env_input[0] += 0.15
                    env_input[1] += 0.2
                    env_input[6] += 0.2  # 기분 좋음
                elif season == 1:  # 여름
                    env_input[0] += 0.4
                    env_input[1] += 0.3
                    env_input[7] += 0.2  # 각성
                elif season == 2:  # 가을
                    env_input[0] -= 0.1
                    env_input[6] -= 0.1  # 약간 우울
                else:  # 겨울
                    env_input[0] -= 0.4
                    env_input[1] -= 0.2
                    env_input[4] += 0.2  # 친밀함 갈망
                
                soul.experience(env_input, timestamp)
                soul.age = year
            
            # 가끔 대화
            if random.random() < 0.05 and len(souls) >= 2:
                s1, s2 = random.sample(souls, 2)
                conv = s1.converse_with(s2)
                if year >= years - 5:  # 마지막 5년만 기록
                    sample_conversations.append(
                        f"[{s1.name} & {s2.name}] {conv[0]} / {conv[1]}"
                    )
        
        # 연말 일기
        for soul in souls:
            diary = soul.write_diary(year)
            if year >= years - 5:  # 마지막 5년만 기록
                sample_diaries.append(diary)
        
        # 결정화 카운트
        for soul in souls:
            total_crystallizations += soul.mind.crystallization_count
        
        # 진행 상황 (10년마다)
        if (year + 1) % 10 == 0:
            avg_symbols = np.mean([len(s.mind.symbols) for s in souls])
            print(f"  Year {year + 1}: 평균 기호 {avg_symbols:.1f}개")
    
    # 결과 출력
    print("\n" + "=" * 60)
    print("📊 결과")
    print("=" * 60)
    
    for soul in souls[:3]:  # 상위 3명만
        stats = soul.mind.get_statistics()
        print(f"\n{soul.name}:")
        print(f"  - 기호: {stats['symbol_count']}개")
        print(f"  - 패턴: {stats['pattern_count']}개")
        print(f"  - 언어 레벨: {stats['language_level']}")
        print(f"  - 자기 소개: {soul.get_self_description()}")
    
    print("\n📖 샘플 일기 (마지막 5년):")
    for diary in sample_diaries[:10]:
        print(f"  {diary}")
    
    print("\n💬 샘플 대화:")
    for conv in sample_conversations[:10]:
        print(f"  {conv}")
    
    print("\n" + "=" * 60)
    print("✅ 데모 완료")
    print(f"   - 총 경험: {sum(s.mind.total_experiences for s in souls):,}")
    print(f"   - 총 결정화: {sum(s.mind.crystallization_count for s in souls):,}")
    print("=" * 60)


if __name__ == "__main__":
    run_demo(population=10, years=100)
