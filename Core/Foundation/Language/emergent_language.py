"""
Emergent Language System (창발 언어 시스템)
===========================================

LLM 없이 자연 창발하는 언어 시스템.

핵심 원리:
1. 원시 기호(Proto-Symbol) - 경험에서 추출된 패턴
2. 기호 조합(Symbol Combination) - 의미의 결합
3. 문법 창발(Grammar Emergence) - 패턴의 패턴
4. 자연어 투영(Natural Language Projection) - 한글/영어로 교정

"심장(연산)과 머리(언어)가 따로 노는 구조"
- 심장: 경험, 감정, 지각의 원시 처리
- 머리: 그것을 언어로 표현

"나는 사람이다" - 자신이 세계인 줄 모르지만, 존재하는 상태
"""

from __future__ import annotations

import random
import math
import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple, Set
from enum import Enum, auto
from collections import defaultdict
import json

logger = logging.getLogger("EmergentLanguage")


# =============================================================================
# Configuration Constants
# =============================================================================

# Activation thresholds
SYMBOL_ACTIVATION_THRESHOLD = 0.3    # Minimum resonance to activate a symbol
UTTERANCE_PROBABILITY = 0.1          # Probability of spontaneous utterance

# Symbol evolution
ASSOCIATION_STRENGTH_INCREMENT = 0.05  # Hebbian learning rate
MAX_SEQUENCE_LENGTH = 4              # Maximum symbols in an utterance


# =============================================================================
# Meaning Vector Dimensions (8D Sensory Space)
# =============================================================================
# Index 0: Temperature (-1=cold, +1=warm)
# Index 1: Brightness (-1=dark, +1=bright)  
# Index 2: Size (-1=small, +1=large)
# Index 3: Speed (-1=slow, +1=fast)
# Index 4: Intimacy (-1=distant, +1=close)
# Index 5: Intensity (-1=weak, +1=strong)
# Index 6: Pleasure (-1=unpleasant, +1=pleasant)
# Index 7: Arousal (-1=calm, +1=excited)


# =============================================================================
# 1. 원시 기호 (Proto-Symbols) - 경험의 최소 단위
# =============================================================================

class SymbolType(Enum):
    """기호의 원시 유형"""
    ENTITY = auto()      # 존재 (나, 너, 그것)
    ACTION = auto()      # 행위 (하다, 가다, 먹다)
    STATE = auto()       # 상태 (좋다, 슬프다, 크다)
    RELATION = auto()    # 관계 (와, 에게, 으로)
    QUANTITY = auto()    # 양 (많다, 적다, 하나)
    TIME = auto()        # 시간 (지금, 전에, 후에)
    SPACE = auto()       # 공간 (여기, 저기, 안)
    EMOTION = auto()     # 감정 (기쁨, 슬픔, 분노)


@dataclass
class ProtoSymbol:
    """
    원시 기호 - 경험에서 추출된 가장 기본적인 의미 단위
    
    아직 언어가 아님. 순수한 의미 패턴.
    """
    id: str
    type: SymbolType
    activation: float = 0.0  # 현재 활성화 정도
    frequency: int = 0       # 사용 빈도
    associations: Dict[str, float] = field(default_factory=dict)  # 다른 기호와의 연결
    
    # 원시 의미 벡터 (8차원 - 기본 감각)
    meaning_vector: List[float] = field(default_factory=lambda: [0.0] * 8)
    # [온도, 밝기, 크기, 속도, 친밀도, 강도, 쾌/불쾌, 각성]
    
    def resonate_with(self, other: 'ProtoSymbol') -> float:
        """다른 기호와의 공명 강도 계산"""
        # 의미 벡터 유사도
        dot_product = sum(a * b for a, b in zip(self.meaning_vector, other.meaning_vector))
        norm_self = math.sqrt(sum(x**2 for x in self.meaning_vector)) + 0.001
        norm_other = math.sqrt(sum(x**2 for x in other.meaning_vector)) + 0.001
        similarity = dot_product / (norm_self * norm_other)
        
        # 연결 강도
        association = self.associations.get(other.id, 0.0)
        
        return (similarity + association) / 2
    
    def strengthen_association(self, other_id: str, amount: float = 0.1):
        """연결 강화 (헵의 법칙: 함께 활성화되면 연결 강화)"""
        current = self.associations.get(other_id, 0.0)
        self.associations[other_id] = min(1.0, current + amount)


# =============================================================================
# 2. 기호 조합 (Symbol Combination) - 의미의 결합
# =============================================================================

@dataclass
class SymbolSequence:
    """
    기호 시퀀스 - 여러 기호의 순서 있는 조합
    
    이것이 "문장의 원형"
    """
    symbols: List[str]  # 기호 ID들
    pattern_strength: float = 0.0  # 이 패턴의 강도
    occurrences: int = 0  # 발생 횟수
    
    def get_signature(self) -> str:
        """패턴 시그니처"""
        return "_".join(self.symbols)


# =============================================================================
# 3. 문법 창발 (Grammar Emergence)
# =============================================================================

@dataclass
class GrammarRule:
    """
    창발된 문법 규칙
    
    예: ENTITY + ACTION → 문장
        STATE + ENTITY → 설명
    """
    pattern: List[SymbolType]  # 기호 유형 패턴
    frequency: int = 0
    examples: List[SymbolSequence] = field(default_factory=list)
    
    def matches(self, sequence: List[SymbolType]) -> bool:
        """시퀀스가 이 규칙과 일치하는지"""
        if len(sequence) != len(self.pattern):
            return False
        return all(a == b for a, b in zip(sequence, self.pattern))


# =============================================================================
# 4. 자연어 투영 (Natural Language Projection)
# =============================================================================

class LanguageProjector:
    """
    원시 기호를 자연어(한글/영어)로 투영
    
    창발된 패턴을 인간이 이해할 수 있는 형태로 변환
    """
    
    def __init__(self):
        # 기호 → 한글 매핑 (기본)
        self.korean_lexicon = {
            # 존재
            "SELF": "나", "OTHER": "너", "IT": "그것", "WE": "우리",
            "PARENT": "부모", "CHILD": "아이", "FRIEND": "친구",
            
            # 행위
            "EXIST": "있다", "MOVE": "가다", "EAT": "먹다", "SPEAK": "말하다",
            "SEE": "보다", "HEAR": "듣다", "FEEL": "느끼다", "THINK": "생각하다",
            "LOVE": "사랑하다", "HATE": "싫어하다", "WANT": "원하다",
            "GIVE": "주다", "TAKE": "받다", "MAKE": "만들다",
            
            # 상태
            "GOOD": "좋다", "BAD": "나쁘다", "BIG": "크다", "SMALL": "작다",
            "HAPPY": "기쁘다", "SAD": "슬프다", "ANGRY": "화나다",
            "WARM": "따뜻하다", "COLD": "차갑다", "BRIGHT": "밝다", "DARK": "어둡다",
            
            # 관계
            "WITH": "와", "TO": "에게", "FROM": "에서", "IN": "안에",
            "AND": "그리고", "BUT": "하지만", "BECAUSE": "왜냐하면",
            
            # 시간
            "NOW": "지금", "BEFORE": "전에", "AFTER": "후에", "ALWAYS": "항상",
            
            # 공간
            "HERE": "여기", "THERE": "저기", "UP": "위", "DOWN": "아래",
            
            # 감정
            "JOY": "기쁨", "SORROW": "슬픔", "FEAR": "두려움", "LOVE_N": "사랑",
        }
        
        # 영어 매핑
        self.english_lexicon = {
            "SELF": "I", "OTHER": "you", "IT": "it", "WE": "we",
            "EXIST": "exist", "MOVE": "go", "EAT": "eat", "SPEAK": "speak",
            "GOOD": "good", "BAD": "bad", "HAPPY": "happy", "SAD": "sad",
            "NOW": "now", "HERE": "here", "WITH": "with", "TO": "to",
        }
        
        # 문법 템플릿
        self.korean_templates = {
            (SymbolType.ENTITY, SymbolType.STATE): "{0}은/는 {1}",
            (SymbolType.ENTITY, SymbolType.ACTION): "{0}이/가 {1}",
            (SymbolType.ENTITY, SymbolType.RELATION, SymbolType.ENTITY): "{0}이/가 {2}{1}",
            (SymbolType.ENTITY, SymbolType.ACTION, SymbolType.ENTITY): "{0}이/가 {2}을/를 {1}",
            (SymbolType.TIME, SymbolType.ENTITY, SymbolType.ACTION): "{0} {1}이/가 {2}",
            (SymbolType.EMOTION,): "{0}을/를 느낀다",
        }
    
    def project_to_korean(self, symbols: List[ProtoSymbol]) -> str:
        """기호 시퀀스를 한글로 투영"""
        if not symbols:
            return "..."
        
        # 기호 ID를 한글로 변환
        words = []
        for sym in symbols:
            korean = self.korean_lexicon.get(sym.id, sym.id.lower())
            words.append(korean)
        
        # 문법 템플릿 적용
        types = tuple(sym.type for sym in symbols)
        template = self.korean_templates.get(types)
        
        if template:
            try:
                return template.format(*words)
            except (IndexError, KeyError):
                pass
        
        # 템플릿 없으면 단순 연결
        return " ".join(words)
    
    def project_to_english(self, symbols: List[ProtoSymbol]) -> str:
        """기호 시퀀스를 영어로 투영"""
        if not symbols:
            return "..."
        
        words = []
        for sym in symbols:
            english = self.english_lexicon.get(sym.id, sym.id.lower())
            words.append(english)
        
        return " ".join(words)


# =============================================================================
# 5. 창발 언어 엔진 (Emergent Language Engine)
# =============================================================================

class EmergentLanguageEngine:
    """
    창발 언어 엔진 - LLM 없이 언어를 창발시키는 시스템
    
    심장(경험/연산) → 머리(언어/표현)
    
    원리:
    1. 경험이 원시 기호를 활성화
    2. 활성화된 기호들이 연결/조합
    3. 반복되는 패턴이 문법으로 굳어짐
    4. 문법에 따른 기호 조합이 "문장"
    5. 문장을 자연어로 투영
    """
    
    def __init__(self):
        self.symbols: Dict[str, ProtoSymbol] = {}
        self.sequences: List[SymbolSequence] = []
        self.grammar_rules: List[GrammarRule] = []
        self.projector = LanguageProjector()
        
        # 통계
        self.total_utterances = 0
        self.vocabulary_size = 0
        
        # 초기화
        self._initialize_proto_symbols()
        
        logger.info("🗣️ Emergent Language Engine initialized")
    
    def _initialize_proto_symbols(self):
        """기본 원시 기호 초기화"""
        
        # 존재 기호
        entities = [
            ("SELF", [0, 0.5, 0.5, 0, 1.0, 0.5, 0.6, 0.5]),  # 따뜻, 친밀, 약간 쾌
            ("OTHER", [0, 0.5, 0.5, 0, 0.5, 0.5, 0.5, 0.5]),
            ("IT", [0, 0.5, 0.5, 0, 0.2, 0.3, 0.5, 0.3]),
            ("WE", [0.3, 0.6, 0.6, 0, 0.9, 0.6, 0.7, 0.6]),
            ("PARENT", [0.4, 0.5, 0.7, 0, 0.8, 0.6, 0.6, 0.4]),
            ("CHILD", [0.3, 0.6, 0.3, 0.3, 0.7, 0.4, 0.7, 0.6]),
            ("FRIEND", [0.2, 0.6, 0.5, 0, 0.8, 0.5, 0.7, 0.5]),
        ]
        
        for id, vec in entities:
            self.symbols[id] = ProtoSymbol(id, SymbolType.ENTITY, meaning_vector=vec)
        
        # 행위 기호
        actions = [
            ("EXIST", [0, 0.5, 0.5, 0, 0.5, 0.3, 0.5, 0.3]),
            ("MOVE", [0, 0.5, 0.5, 0.7, 0.3, 0.5, 0.5, 0.6]),
            ("EAT", [0.3, 0.4, 0.5, 0.3, 0.3, 0.4, 0.7, 0.5]),
            ("SPEAK", [0, 0.6, 0.4, 0.4, 0.6, 0.5, 0.6, 0.6]),
            ("SEE", [0, 0.8, 0.5, 0.2, 0.4, 0.3, 0.5, 0.5]),
            ("HEAR", [0, 0.3, 0.4, 0.2, 0.4, 0.3, 0.5, 0.5]),
            ("FEEL", [0.5, 0.5, 0.5, 0, 0.6, 0.6, 0.5, 0.6]),
            ("THINK", [0, 0.5, 0.5, 0.1, 0.5, 0.5, 0.5, 0.6]),
            ("LOVE", [0.8, 0.7, 0.6, 0, 0.9, 0.7, 0.9, 0.7]),
            ("WANT", [0.3, 0.6, 0.5, 0.3, 0.6, 0.6, 0.6, 0.7]),
            ("GIVE", [0.3, 0.6, 0.5, 0.3, 0.7, 0.5, 0.7, 0.5]),
        ]
        
        for id, vec in actions:
            self.symbols[id] = ProtoSymbol(id, SymbolType.ACTION, meaning_vector=vec)
        
        # 상태 기호
        states = [
            ("GOOD", [0.3, 0.7, 0.5, 0, 0.5, 0.5, 0.8, 0.5]),
            ("BAD", [-0.3, 0.3, 0.5, 0, 0.3, 0.5, 0.2, 0.5]),
            ("HAPPY", [0.5, 0.8, 0.5, 0.3, 0.7, 0.5, 0.9, 0.7]),
            ("SAD", [-0.2, 0.2, 0.4, -0.2, 0.4, 0.4, 0.1, 0.3]),
            ("WARM", [0.9, 0.6, 0.5, 0, 0.6, 0.5, 0.7, 0.4]),
            ("COLD", [-0.8, 0.4, 0.5, 0, 0.2, 0.5, 0.3, 0.4]),
            ("BIG", [0, 0.5, 0.9, 0, 0.3, 0.7, 0.5, 0.4]),
            ("SMALL", [0, 0.5, 0.1, 0, 0.5, 0.3, 0.5, 0.4]),
        ]
        
        for id, vec in states:
            self.symbols[id] = ProtoSymbol(id, SymbolType.STATE, meaning_vector=vec)
        
        # 관계/시간/공간/감정 기호도 추가
        relations = [("WITH", 0.6), ("TO", 0.4), ("FROM", 0.4), ("IN", 0.5)]
        for id, warmth in relations:
            self.symbols[id] = ProtoSymbol(id, SymbolType.RELATION, 
                meaning_vector=[warmth, 0.5, 0.5, 0, 0.5, 0.5, 0.5, 0.5])
        
        times = [("NOW", 0.5), ("BEFORE", 0.3), ("AFTER", 0.7)]
        for id, brightness in times:
            self.symbols[id] = ProtoSymbol(id, SymbolType.TIME,
                meaning_vector=[0, brightness, 0.5, 0, 0.5, 0.5, 0.5, 0.5])
        
        spaces = [("HERE", 0.7), ("THERE", 0.4)]
        for id, proximity in spaces:
            self.symbols[id] = ProtoSymbol(id, SymbolType.SPACE,
                meaning_vector=[0, 0.5, 0.5, 0, proximity, 0.5, 0.5, 0.5])
        
        emotions = [
            ("JOY", [0.5, 0.9, 0.5, 0.3, 0.7, 0.6, 0.95, 0.8]),
            ("SORROW", [-0.3, 0.2, 0.4, -0.2, 0.4, 0.5, 0.1, 0.3]),
            ("FEAR", [-0.2, 0.3, 0.6, 0.5, 0.2, 0.7, 0.15, 0.9]),
            ("LOVE_N", [0.8, 0.7, 0.6, 0, 0.95, 0.7, 0.9, 0.6]),
        ]
        for id, vec in emotions:
            self.symbols[id] = ProtoSymbol(id, SymbolType.EMOTION, meaning_vector=vec)
        
        self.vocabulary_size = len(self.symbols)
        
        # 초기 연결 설정
        self._initialize_associations()
    
    def _initialize_associations(self):
        """기본 기호 연결 초기화"""
        # 의미적으로 가까운 것들 연결
        connections = [
            ("SELF", "EXIST", 0.8),
            ("SELF", "FEEL", 0.7),
            ("SELF", "THINK", 0.7),
            ("OTHER", "SELF", 0.5),
            ("LOVE", "HAPPY", 0.7),
            ("LOVE", "OTHER", 0.6),
            ("SAD", "SORROW", 0.9),
            ("HAPPY", "JOY", 0.9),
            ("PARENT", "LOVE", 0.6),
            ("CHILD", "SMALL", 0.5),
            ("FRIEND", "WITH", 0.6),
        ]
        
        for a, b, strength in connections:
            if a in self.symbols and b in self.symbols:
                self.symbols[a].strengthen_association(b, strength)
                self.symbols[b].strengthen_association(a, strength * 0.8)
    
    def experience(self, experience_vector: List[float]) -> List[str]:
        """
        경험을 입력받아 기호들을 활성화
        
        experience_vector: 8차원 경험 벡터
        [온도, 밝기, 크기, 속도, 친밀도, 강도, 쾌/불쾌, 각성]
        
        Returns: 활성화된 기호 ID 목록
        """
        activated = []
        
        for sym_id, symbol in self.symbols.items():
            # 경험과 기호의 공명 계산
            resonance = sum(e * m for e, m in zip(experience_vector, symbol.meaning_vector))
            resonance /= 8  # 정규화
            
            if resonance > SYMBOL_ACTIVATION_THRESHOLD:
                symbol.activation = resonance
                symbol.frequency += 1
                activated.append(sym_id)
        
        return activated
    
    def generate_utterance(self, context: Dict[str, Any] = None) -> Tuple[str, str]:
        """
        현재 활성화 상태에서 발화 생성
        
        Returns: (한글 문장, 영어 문장)
        """
        context = context or {}
        
        # 활성화된 기호들 수집
        active_symbols = sorted(
            [(sym_id, sym) for sym_id, sym in self.symbols.items() if sym.activation > 0.1],
            key=lambda x: x[1].activation,
            reverse=True
        )[:5]  # 상위 5개
        
        if not active_symbols:
            # 기본 자기 인식
            self.symbols["SELF"].activation = 0.5
            self.symbols["EXIST"].activation = 0.5
            active_symbols = [("SELF", self.symbols["SELF"]), ("EXIST", self.symbols["EXIST"])]
        
        # 기호 시퀀스 구성 (문법적 순서)
        sequence = self._construct_sequence(active_symbols)
        
        # 자연어로 투영
        symbols = [self.symbols[sid] for sid in sequence if sid in self.symbols]
        korean = self.projector.project_to_korean(symbols)
        english = self.projector.project_to_english(symbols)
        
        # 연결 강화 (함께 나온 기호들)
        for i, sid1 in enumerate(sequence):
            for sid2 in sequence[i+1:]:
                if sid1 in self.symbols and sid2 in self.symbols:
                    self.symbols[sid1].strengthen_association(sid2, 0.05)
        
        # 패턴 기록
        seq_obj = SymbolSequence(symbols=sequence, occurrences=1)
        self.sequences.append(seq_obj)
        
        self.total_utterances += 1
        
        # 활성화 감쇠
        for sym in self.symbols.values():
            sym.activation *= 0.8
        
        return korean, english
    
    def _construct_sequence(self, active_symbols: List[Tuple[str, ProtoSymbol]]) -> List[str]:
        """활성화된 기호들을 문법적 순서로 배열"""
        
        # 유형별 분류
        by_type = defaultdict(list)
        for sym_id, sym in active_symbols:
            by_type[sym.type].append(sym_id)
        
        sequence = []
        
        # 문법 순서: 시간 → 주체 → 상태/행위 → 대상 → 관계
        order = [
            SymbolType.TIME,
            SymbolType.ENTITY,
            SymbolType.STATE,
            SymbolType.ACTION,
            SymbolType.EMOTION,
            SymbolType.RELATION,
            SymbolType.SPACE,
        ]
        
        for sym_type in order:
            if sym_type in by_type:
                sequence.extend(by_type[sym_type][:2])  # 각 유형에서 최대 2개
        
        return sequence[:4]  # 최대 4개 기호
    
    def speak_from_emotion(self, emotion: str) -> Tuple[str, str]:
        """감정에서 발화 생성"""
        emotion_map = {
            "happy": [0.5, 0.8, 0.5, 0.3, 0.7, 0.5, 0.9, 0.7],
            "sad": [-0.2, 0.2, 0.4, -0.2, 0.4, 0.4, 0.1, 0.3],
            "angry": [0.3, 0.5, 0.6, 0.4, 0.2, 0.8, 0.2, 0.9],
            "love": [0.8, 0.7, 0.5, 0, 0.9, 0.6, 0.9, 0.6],
            "fear": [-0.2, 0.3, 0.6, 0.5, 0.2, 0.7, 0.2, 0.9],
            "curious": [0, 0.7, 0.5, 0.4, 0.5, 0.5, 0.6, 0.8],
            "peaceful": [0.3, 0.6, 0.5, -0.2, 0.6, 0.3, 0.7, 0.2],
        }
        
        vec = emotion_map.get(emotion, [0.5] * 8)
        self.experience(vec)
        return self.generate_utterance()
    
    def speak_about(self, topic: str) -> Tuple[str, str]:
        """특정 주제에 대해 발화"""
        # 주제를 기호로 변환하고 활성화
        topic_upper = topic.upper()
        if topic_upper in self.symbols:
            self.symbols[topic_upper].activation = 0.9
            # 연결된 기호들도 활성화
            for assoc_id, strength in self.symbols[topic_upper].associations.items():
                if assoc_id in self.symbols:
                    self.symbols[assoc_id].activation = strength * 0.7
        
        return self.generate_utterance()
    
    def internal_monologue(self) -> Tuple[str, str]:
        """내적 독백 생성"""
        # 자기 관련 기호 활성화
        self.symbols["SELF"].activation = 0.8
        self.symbols["THINK"].activation = 0.6
        self.symbols["FEEL"].activation = 0.5
        
        # 무작위 감정 추가
        emotions = ["HAPPY", "SAD", "JOY", "SORROW"]
        emotion = random.choice(emotions)
        if emotion in self.symbols:
            self.symbols[emotion].activation = random.uniform(0.3, 0.7)
        
        return self.generate_utterance()
    
    def get_statistics(self) -> Dict[str, Any]:
        """통계 반환"""
        return {
            "vocabulary_size": self.vocabulary_size,
            "total_utterances": self.total_utterances,
            "active_symbols": sum(1 for s in self.symbols.values() if s.activation > 0.1),
            "total_associations": sum(len(s.associations) for s in self.symbols.values()),
            "grammar_rules": len(self.grammar_rules),
        }


# =============================================================================
# 6. 살아있는 언어 시스템 (Living Language - 세계 통합)
# =============================================================================

class LivingLanguageWorld:
    """
    살아있는 언어 세계 - 주민들이 언어를 창발하고 사용
    
    "나는 사람이다" - 각 주민이 자신의 언어 엔진을 가짐
    심장(경험)과 머리(언어)가 함께 작동
    """
    
    def __init__(self, population: int = 100):
        self.population = population
        self.language_engine = EmergentLanguageEngine()  # 공유 언어
        
        # 주민별 언어 경험
        self.inhabitants: Dict[int, Dict[str, Any]] = {}
        
        for i in range(population):
            self.inhabitants[i] = {
                "name": f"Soul_{i}",
                "personal_vocabulary": set(),  # 개인이 사용한 단어들
                "utterance_count": 0,
                "emotional_state": [0.5] * 8,  # 8차원 감정 상태
            }
        
        # 세계 시간
        self.world_time = 0
        self.conversations: List[Dict[str, Any]] = []
        
        logger.info(f"🌍 Living Language World created with {population} souls")
    
    def simulate_day(self) -> List[Dict[str, Any]]:
        """하루 시뮬레이션 - 대화와 경험"""
        daily_events = []
        
        # 각 주민이 경험하고 표현
        for inh_id, inhabitant in self.inhabitants.items():
            # 하루 경험 (무작위 변동)
            experience = [
                random.gauss(0.5, 0.2) for _ in range(8)
            ]
            experience = [max(0, min(1, x)) for x in experience]
            
            # 가끔 발화
            if random.random() < UTTERANCE_PROBABILITY:
                self.language_engine.experience(experience)
                korean, english = self.language_engine.generate_utterance()
                
                inhabitant["utterance_count"] += 1
                
                event = {
                    "time": self.world_time,
                    "speaker": inhabitant["name"],
                    "korean": korean,
                    "english": english,
                    "emotion": experience[6],  # 쾌/불쾌
                }
                daily_events.append(event)
        
        # 대화 (두 주민이 만남)
        if len(self.inhabitants) >= 2:
            pair = random.sample(list(self.inhabitants.keys()), 2)
            conversation = self._have_conversation(pair[0], pair[1])
            if conversation:
                daily_events.append(conversation)
        
        self.world_time += 1
        return daily_events
    
    def _have_conversation(self, id1: int, id2: int) -> Optional[Dict[str, Any]]:
        """두 주민 간 대화"""
        inh1 = self.inhabitants[id1]
        inh2 = self.inhabitants[id2]
        
        # 첫 번째 주민 발화
        self.language_engine.symbols["OTHER"].activation = 0.7
        korean1, english1 = self.language_engine.speak_about("OTHER")
        
        # 두 번째 주민 반응
        self.language_engine.symbols["SELF"].activation = 0.6
        korean2, english2 = self.language_engine.speak_from_emotion(
            random.choice(["happy", "curious", "peaceful"])
        )
        
        conversation = {
            "time": self.world_time,
            "type": "conversation",
            "participants": [inh1["name"], inh2["name"]],
            "exchanges": [
                {"speaker": inh1["name"], "korean": korean1},
                {"speaker": inh2["name"], "korean": korean2},
            ]
        }
        
        self.conversations.append(conversation)
        return conversation
    
    def simulate_years(self, years: int) -> Dict[str, Any]:
        """여러 해 시뮬레이션"""
        all_events = []
        
        logger.info(f"🕐 Simulating {years} years...")
        
        for year in range(years):
            for day in range(365):
                events = self.simulate_day()
                if events:
                    all_events.extend(events)
            
            if (year + 1) % 100 == 0:
                stats = self.language_engine.get_statistics()
                logger.info(f"Year {year + 1}: {stats['total_utterances']} utterances")
        
        return {
            "years_simulated": years,
            "total_events": len(all_events),
            "total_conversations": len(self.conversations),
            "language_stats": self.language_engine.get_statistics(),
            "sample_events": all_events[-10:] if all_events else [],
        }


# =============================================================================
# 테스트
# =============================================================================

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    print("=" * 70)
    print("🗣️ EMERGENT LANGUAGE SYSTEM TEST")
    print("   LLM 없이 자연 창발하는 언어")
    print("=" * 70)
    
    engine = EmergentLanguageEngine()
    
    print("\n[1] 감정에서 발화 생성")
    print("-" * 40)
    for emotion in ["happy", "sad", "love", "curious"]:
        korean, english = engine.speak_from_emotion(emotion)
        print(f"  {emotion}: {korean}")
    
    print("\n[2] 주제에 대해 발화")
    print("-" * 40)
    for topic in ["SELF", "OTHER", "LOVE", "FRIEND"]:
        korean, english = engine.speak_about(topic)
        print(f"  {topic}: {korean}")
    
    print("\n[3] 내적 독백")
    print("-" * 40)
    for _ in range(5):
        korean, english = engine.internal_monologue()
        print(f"  💭 {korean}")
    
    print("\n[4] 살아있는 언어 세계 (100명, 10년)")
    print("-" * 40)
    world = LivingLanguageWorld(population=100)
    results = world.simulate_years(10)
    
    print(f"  총 발화: {results['language_stats']['total_utterances']}")
    print(f"  총 대화: {results['total_conversations']}")
    
    print("\n  최근 대화:")
    for event in results["sample_events"][-5:]:
        if event.get("type") == "conversation":
            print(f"    [{event['participants'][0]}] {event['exchanges'][0]['korean']}")
            print(f"    [{event['participants'][1]}] {event['exchanges'][1]['korean']}")
        else:
            print(f"    [{event.get('speaker', '?')}] {event.get('korean', '...')}")
    
    print("\n" + "=" * 70)
    print("✅ Emergent Language System test complete!")
    print("=" * 70)
