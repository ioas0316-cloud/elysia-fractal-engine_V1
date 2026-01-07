# -*- coding: utf-8 -*-
"""
Language Projector
==================

Projects abstract concepts and energy flows into natural language (Korean/English).
Adapted from Legacy/Language/emergent_language.py.
"""

from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class SymbolType(Enum):
    ENTITY = "entity"      # 존재 (나, 너, 그것)
    ACTION = "action"      # 행위 (하다, 가다, 먹다)
    STATE = "state"        # 상태 (좋다, 슬프다, 크다)
    RELATION = "relation"  # 관계 (와, 에게, 으로)
    QUANTITY = "quantity"  # 양 (많다, 적다, 하나)
    TIME = "time"          # 시간 (지금, 전에, 후에)
    SPACE = "space"        # 공간 (여기, 저기, 안)
    EMOTION = "emotion"    # 감정 (기쁨, 슬픔, 분노)
    UNKNOWN = "unknown"

class LanguageProjector:
    """
    Projects abstract concepts into natural language.
    Handles Korean particles (Josa) and English word order based on energy flow.
    """
    
    def __init__(self):
        # 기호 → 한글 매핑 (기본 어휘)
        # This will be supplemented by the dynamic Concept definitions
        self.korean_lexicon = {
            # 존재
            "SELF": "나", "OTHER": "너", "IT": "그것", "WE": "우리",
            "PARENT": "부모", "CHILD": "아이", "FRIEND": "친구",
            
            # 행위
            "EXIST": "있다", "MOVE": "가다", "EAT": "먹다", "SPEAK": "말하다",
            "SEE": "보다", "HEAR": "듣다", "FEEL": "느끼다", "THINK": "생각하다",
            "LOVE": "사랑하다", "HATE": "싫어하다", "WANT": "원하다",
            "GIVE": "주다", "TAKE": "받다", "MAKE": "만들다",
            "CREATES": "만들다", "CAUSES": "일으키다", "ENABLES": "가능하게 하다",
            
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
            "CREATES": "creates", "CAUSES": "causes", "ENABLES": "enables",
        }

    def get_korean_name(self, concept_name: str) -> str:
        """Get Korean name for a concept, defaulting to lowercased name"""
        return self.korean_lexicon.get(concept_name.upper(), concept_name)

    def get_english_name(self, concept_name: str) -> str:
        """Get English name for a concept"""
        return self.english_lexicon.get(concept_name.upper(), concept_name)

    def project_to_korean(self, source: str, action: str, target: str, passive: bool = False) -> str:
        """
        Project an energy flow (Source -> Action -> Target) to Korean (SOV).
        Active: Source(은/는) Target(을/를) Action(한다).
        Passive: Source(은/는) Target(에 의해) Action(된다/받다).
        """
        s_name = self.get_korean_name(source)
        t_name = self.get_korean_name(target)
        a_name = self.get_korean_name(action)
        
        if passive:
            # Passive: Source is the Subject (originally Target), Target is the Agent (originally Source)
            # But in our StarSystem, 'star' is passed as 'source' here because it's the subject.
            # So: Star(Subject) ... Planet(Agent) ...
            # Let's clarify: The caller (StarSystem) aligns Star as Subject.
            # If Passive, Star was the Object of the action.
            # "Bonds(Star) are created by Love(Planet)"
            # Korean: "Bonds(은/는) Love(에 의해) 만들어진다"
            
            # Map action to passive form if possible
            passive_map = {
                "만들다": "만들어진다",
                "일으키다": "일어난다", # or 유발된다
                "가능하게 하다": "가능해진다",
                "사랑하다": "사랑받다",
                "먹다": "먹히다",
                "보다": "보이다",
            }
            a_name = passive_map.get(a_name, a_name + " 당하다/된다") # Fallback
            
            sentence = f"{s_name}은/는 {t_name}에 의해 {a_name}"
        else:
            # Active
            sentence = f"{s_name}은/는 {t_name}을/를 {a_name}"
            if not a_name.endswith("다"):
                sentence += "한다"
            
        return sentence

    def project_to_english(self, source: str, action: str, target: str, passive: bool = False) -> str:
        """
        Project an energy flow to English (SVO).
        Active: Source Action Target.
        Passive: Source is Actioned by Target.
        """
        s_name = self.get_english_name(source)
        t_name = self.get_english_name(target)
        a_name = self.get_english_name(action)
        
        if passive:
            # Passive: Source is Actioned by Target
            # "Bonds are created by Love"
            
            # Simple conjugation
            if a_name.endswith("e"):
                past_participle = a_name + "d"
            else:
                past_participle = a_name + "ed"
                
            # Handle irregulars if needed (creates -> created is fine)
            
            return f"{s_name} is {past_participle} by {t_name}"
        else:
            return f"{s_name} {a_name} {t_name}"
