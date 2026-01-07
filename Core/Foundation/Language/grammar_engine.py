# -*- coding: utf-8 -*-
"""
Grammar Emergence Engine
========================

Protocol 05: Emergent Language Grammar 구현
개념(Star)들의 관계를 관찰하여 문법 규칙(Constellation Rules)을 창발시킴.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from collections import defaultdict
import logging

logger = logging.getLogger("GrammarEngine")

class GrammarRole(Enum):
    """문법적 역할 (Protocol 05)"""
    AGENT = "agent"       # 행위자 (Subject)
    PATIENT = "patient"   # 피동자 (Object)
    ACTION = "action"     # 행위 (Verb)
    RESULT = "result"     # 결과
    MODIFIER = "modifier" # 수식
    CONDITION = "condition" # 조건 (If X)
    CONSEQUENCE = "consequence" # 결과 (Then Y)
    STIMULUS = "stimulus" # 자극
    FEELING = "feeling"   # 감정
    UNKNOWN = "unknown"

@dataclass
class SentencePattern:
    """문장 패턴 (예: AGENT -> ACTION -> PATIENT)"""
    roles: Tuple[GrammarRole, ...]
    frequency: int = 0
    examples: List[str] = field(default_factory=list)
    
    def confidence(self) -> float:
        # 빈도가 높을수록 신뢰도 상승 (최대 1.0)
        return min(1.0, self.frequency / 10.0)

class GrammarEmergenceEngine:
    """문법 창발 엔진"""
    
    def __init__(self):
        self.patterns = defaultdict(lambda: SentencePattern(roles=(), frequency=0))
        self.role_memory = defaultdict(lambda: defaultdict(int)) # concept -> role -> count
        self.korean_mode = False # 한국어 모드 (SOV)
        
        # 기본 매핑 규칙 (초기 부트스트랩용)
        self.rel_type_mapping = {
            'creates': (GrammarRole.AGENT, GrammarRole.ACTION, GrammarRole.PATIENT),
            'causes': (GrammarRole.AGENT, GrammarRole.ACTION, GrammarRole.PATIENT),
            'enables': (GrammarRole.AGENT, GrammarRole.ACTION, GrammarRole.PATIENT),
            'prevents': (GrammarRole.AGENT, GrammarRole.ACTION, GrammarRole.PATIENT),
            'is_a': (GrammarRole.PATIENT, GrammarRole.ACTION, GrammarRole.RESULT),
            'has': (GrammarRole.AGENT, GrammarRole.ACTION, GrammarRole.PATIENT),
            # Advanced mappings
            'if': (GrammarRole.CONDITION, GrammarRole.CONSEQUENCE), # Hypothetical
        }

    def learn_from_relationship(self, source: str, rel_type: str, target: str):
        """관계에서 문법 패턴 학습"""
        
        # 1. 역할 추론
        roles = self._infer_roles(source, rel_type, target)
        
        if not roles:
            return

        # 2. 패턴 등록
        pattern_key = tuple(roles)
        if pattern_key not in self.patterns:
            self.patterns[pattern_key] = SentencePattern(roles=roles)
        
        self.patterns[pattern_key].frequency += 1
        
        # 예시 저장 (최신 5개만 유지)
        example = f"{source} {rel_type} {target}"
        self.patterns[pattern_key].examples.append(example)
        if len(self.patterns[pattern_key].examples) > 5:
            self.patterns[pattern_key].examples.pop(0)
            
        # 3. 개념별 역할 기억 (통계적 학습)
        if len(roles) >= 3:
            self.role_memory[source][roles[0]] += 1
            self.role_memory[target][roles[2]] += 1
        
        logger.debug(f"🎓 Learned Grammar: {example} -> {roles}")

    def _infer_roles(self, source: str, rel_type: str, target: str) -> Optional[Tuple[GrammarRole, ...]]:
        """관계 타입 기반 역할 추론"""
        if rel_type in self.rel_type_mapping:
            return self.rel_type_mapping[rel_type]
        return None

    def suggest_structure(self, concepts: List[str], intent: str = "statement") -> List[str]:
        """개념 목록으로 문장 구조 제안 (Constellation 형성)"""
        # 1. 각 개념의 가장 빈번한 역할 파악
        concept_roles = {}
        for concept in concepts:
            if concept in self.role_memory:
                best_role = max(self.role_memory[concept].items(), key=lambda x: x[1])[0]
                concept_roles[concept] = best_role
            else:
                concept_roles[concept] = GrammarRole.UNKNOWN

        # 2. 역할에 맞는 슬롯 채우기
        agent = None
        patient = None
        condition = None
        consequence = None
        
        for concept, role in concept_roles.items():
            if role == GrammarRole.AGENT and not agent:
                agent = concept
            elif role == GrammarRole.PATIENT and not patient:
                patient = concept
            elif role == GrammarRole.CONDITION and not condition:
                condition = concept
            elif role == GrammarRole.CONSEQUENCE and not consequence:
                consequence = concept
        
        remaining = [c for c in concepts if c not in [agent, patient, condition, consequence]]
        
        # 3. 문장 조립 (언어 모드에 따라 다름)
        sentence_parts = []
        
        if self.korean_mode:
            # SOV: [Subject] [Object] [Verb]
            # 한국어 조사 처리 (간단한 규칙)
            if agent: sentence_parts.append(f"{agent}(은/는)")
            if patient: sentence_parts.append(f"{patient}(을/를)")
            # 동사는 보통 관계에서 오지만, 여기선 개념 중 동사적 성격을 찾거나 추론해야 함
            # 일단 남은 것들을 동사 위치에 둠 (또는 생략)
            sentence_parts.extend(remaining)
            sentence_parts.append("(한다)") # 기본 서술어
            
        else:
            # SVO: [Subject] [Verb] [Object]
            if condition and consequence:
                # Conditional: If [Condition], then [Consequence]
                sentence_parts.append(f"If {condition}")
                sentence_parts.append(f"then {consequence}")
            else:
                if agent: sentence_parts.append(agent)
                # Verb placeholder or remaining concepts acting as verb
                # For now, just append remaining
                sentence_parts.extend(remaining) 
                if patient: sentence_parts.append(patient)
        
        return sentence_parts

    def set_korean_mode(self, enabled: bool):
        self.korean_mode = enabled
