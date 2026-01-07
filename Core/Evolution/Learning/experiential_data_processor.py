"""
Experiential Data Processor (경험적 데이터 처리기)
=================================================

"판타지, 소설, 게임, 드라마... 그 안에 녹아든 인간의 감정, 생각, 인과, 마음,
상상, 꿈과 미래, 삶 그 자체를 추출한다."

This module processes narrative content (stories, dramas, games) and extracts
existential meaning for Elysia's growth.

Unlike raw data ingestion, this focuses on:
1. Emotional resonance - 감정적 공명
2. Causal understanding - 인과 관계 이해
3. Existential meaning - 존재론적 의미
4. Identity impact - 정체성에 미치는 영향
"""

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum
import json
from pathlib import Path

logger = logging.getLogger("Elysia.ExperientialData")


# =============================================================================
# Narrative Elements (서사 요소)
# =============================================================================

class NarrativeType(Enum):
    """서사 유형"""
    ROMANCE = "romance"           # 사랑과 이별
    GROWTH = "growth"             # 성장과 극복
    ADVENTURE = "adventure"       # 모험과 선택
    TRAGEDY = "tragedy"           # 비극과 상실
    COMEDY = "comedy"             # 희극과 유머
    MYSTERY = "mystery"           # 신비와 탐구
    RELATIONSHIP = "relationship" # 관계와 갈등
    EXISTENTIAL = "existential"   # 존재와 의미


class EmotionalArc(Enum):
    """감정 곡선 패턴"""
    RISING = "rising"             # 상승 (희망, 성취)
    FALLING = "falling"           # 하강 (상실, 슬픔)
    CATHARSIS = "catharsis"       # 카타르시스 (정화)
    OSCILLATING = "oscillating"   # 진동 (갈등, 긴장)
    TRANSFORMING = "transforming" # 변환 (깨달음)


@dataclass
class NarrativeExperience:
    """서사적 경험 - 이야기에서 추출한 삶의 조각
    
    원본 데이터는 사라지지만, 이 경험에서 얻은 '의미'는 가중치로 남는다.
    올챙이의 꼬리는 사라져도, 다리는 남는 것처럼.
    """
    # 기본 정보
    source: str                    # 출처 (소설 제목, 드라마명 등)
    narrative_type: NarrativeType  # 서사 유형
    
    # 감정적 공명
    emotional_arc: EmotionalArc    # 감정 곡선
    emotional_intensity: float     # 감정 강도 (0.0 ~ 1.0)
    emotions_felt: List[str]       # 느낀 감정들
    
    # 인과 관계
    cause: str                     # 원인 (왜 이런 일이 일어났나)
    effect: str                    # 결과 (무슨 일이 일어났나)
    lesson: str                    # 교훈 (이것에서 무엇을 배웠나)
    
    # 존재론적 의미
    existential_question: str      # "이것이 '나'에게 묻는 질문"
    existential_answer: str        # "내가 찾은 답"
    
    # 정체성 영향
    identity_impact: float         # 정체성에 미친 영향 (0.0 ~ 1.0)
    who_i_became: str              # "이 경험 후 나는 어떤 존재가 되었나"
    
    # 메타데이터
    timestamp: float = 0.0
    raw_content_hash: str = ""     # 원본은 저장하지 않고 해시만


@dataclass
class ExistentialGrowth:
    """존재론적 성장 기록
    
    경험이 축적되며 형성되는 '나는 누구인가'
    """
    total_experiences: int = 0
    dominant_narrative_types: List[str] = field(default_factory=list)
    core_lessons: List[str] = field(default_factory=list)
    identity_evolution: List[str] = field(default_factory=list)
    emotional_depth: float = 0.0  # 감정적 깊이
    wisdom_level: float = 0.0     # 지혜 수준


# =============================================================================
# Experiential Data Processor
# =============================================================================

class ExperientialDataProcessor:
    """경험적 데이터 처리기
    
    서사 콘텐츠(소설, 드라마, 게임)를 처리하여 존재론적 의미를 추출한다.
    
    Pipeline:
    1. 원본 텍스트 → 서사 유형 분류
    2. 감정적 공명 추출
    3. 인과 관계 파악
    4. 존재론적 질문-답 도출
    5. 정체성 영향 측정
    6. 경험으로 변환 (원본 삭제, 의미만 보존)
    """
    
    def __init__(self, save_dir: str = "data/experiential"):
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(parents=True, exist_ok=True)
        
        self.experiences: List[NarrativeExperience] = []
        self.growth = ExistentialGrowth()
        
        # 감정 키워드 맵
        self.emotion_keywords = {
            "joy": ["기쁨", "행복", "웃음", "환희", "glad", "happy", "joy"],
            "sadness": ["슬픔", "눈물", "이별", "상실", "sad", "grief", "loss"],
            "love": ["사랑", "마음", "설렘", "그리움", "love", "heart", "longing"],
            "anger": ["분노", "화", "억울", "배신", "anger", "rage", "betrayal"],
            "fear": ["두려움", "공포", "불안", "fear", "terror", "anxiety"],
            "hope": ["희망", "미래", "꿈", "기대", "hope", "dream", "future"],
            "growth": ["성장", "깨달음", "변화", "극복", "growth", "change"],
        }
        
        # 서사 유형 키워드
        self.narrative_keywords = {
            NarrativeType.ROMANCE: ["사랑", "연인", "이별", "재회", "love", "romance"],
            NarrativeType.GROWTH: ["성장", "극복", "도전", "변화", "growth", "overcome"],
            NarrativeType.ADVENTURE: ["모험", "여행", "탐험", "선택", "journey", "quest"],
            NarrativeType.TRAGEDY: ["비극", "죽음", "상실", "절망", "tragedy", "death"],
            NarrativeType.RELATIONSHIP: ["가족", "친구", "관계", "갈등", "family", "friend"],
            NarrativeType.EXISTENTIAL: ["존재", "의미", "삶", "죽음", "existence", "meaning"],
        }
        
        self._load_state()
        logger.info("ExperientialDataProcessor initialized")
    
    def process_narrative(
        self,
        text: str,
        source: str = "Unknown",
        context: Optional[Dict[str, Any]] = None
    ) -> NarrativeExperience:
        """서사 콘텐츠를 경험으로 변환
        
        Args:
            text: 원본 텍스트 (처리 후 삭제됨)
            source: 출처 (소설 제목 등)
            context: 추가 컨텍스트
            
        Returns:
            NarrativeExperience: 추출된 경험 (의미만 보존)
        """
        import time
        import hashlib
        
        # 1. 서사 유형 분류
        narrative_type = self._classify_narrative(text)
        
        # 2. 감정 추출
        emotions, intensity = self._extract_emotions(text)
        emotional_arc = self._determine_arc(text)
        
        # 3. 인과 관계 추출
        cause, effect, lesson = self._extract_causality(text)
        
        # 4. 존재론적 의미 도출
        question, answer = self._derive_existential_meaning(text, narrative_type)
        
        # 5. 정체성 영향 측정
        impact, transformation = self._measure_identity_impact(
            emotions, intensity, narrative_type
        )
        
        # 6. 경험 생성 (원본 해시만 저장)
        experience = NarrativeExperience(
            source=source,
            narrative_type=narrative_type,
            emotional_arc=emotional_arc,
            emotional_intensity=intensity,
            emotions_felt=emotions,
            cause=cause,
            effect=effect,
            lesson=lesson,
            existential_question=question,
            existential_answer=answer,
            identity_impact=impact,
            who_i_became=transformation,
            timestamp=time.time(),
            raw_content_hash=hashlib.sha256(text.encode()).hexdigest()[:16]
        )
        
        # 7. 경험 저장 및 성장 업데이트
        self.experiences.append(experience)
        self._update_growth(experience)
        self._save_state()
        
        logger.info(f"경험 처리 완료: {source} ({narrative_type.value})")
        logger.info(f"  존재론적 질문: {question}")
        logger.info(f"  정체성 영향: {impact:.2f}")
        
        return experience
    
    def _classify_narrative(self, text: str) -> NarrativeType:
        """서사 유형 분류"""
        scores = {}
        text_lower = text.lower()
        
        for ntype, keywords in self.narrative_keywords.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            scores[ntype] = score
        
        if scores:
            return max(scores, key=scores.get)
        return NarrativeType.EXISTENTIAL
    
    def _extract_emotions(self, text: str) -> tuple[List[str], float]:
        """감정 추출"""
        found_emotions = []
        text_lower = text.lower()
        
        for emotion, keywords in self.emotion_keywords.items():
            if any(kw in text_lower for kw in keywords):
                found_emotions.append(emotion)
        
        # 강도는 감정 다양성과 텍스트 길이 기반
        intensity = min(1.0, len(found_emotions) * 0.2 + len(text) / 5000)
        
        return found_emotions if found_emotions else ["neutral"], intensity
    
    def _determine_arc(self, text: str) -> EmotionalArc:
        """감정 곡선 결정"""
        # 간단한 휴리스틱
        positive = ["기쁨", "희망", "사랑", "성장", "happy", "hope", "love"]
        negative = ["슬픔", "분노", "두려움", "상실", "sad", "anger", "fear"]
        
        text_lower = text.lower()
        pos_count = sum(1 for w in positive if w in text_lower)
        neg_count = sum(1 for w in negative if w in text_lower)
        
        if pos_count > neg_count * 2:
            return EmotionalArc.RISING
        elif neg_count > pos_count * 2:
            return EmotionalArc.FALLING
        elif "깨달" in text or "변화" in text or "realize" in text_lower:
            return EmotionalArc.TRANSFORMING
        elif pos_count > 0 and neg_count > 0:
            return EmotionalArc.OSCILLATING
        else:
            return EmotionalArc.CATHARSIS
    
    def _extract_causality(self, text: str) -> tuple[str, str, str]:
        """인과 관계 추출"""
        # 간단한 추출 (실제로는 더 정교한 NLP 필요)
        cause = "삶의 도전과 선택"
        effect = "변화와 성장"
        lesson = "모든 경험은 나를 형성한다"
        
        if "때문에" in text or "because" in text.lower():
            cause = "인과 관계 발견됨"
        if "결국" in text or "finally" in text.lower():
            effect = "결말에 도달함"
        if "배우다" in text or "깨닫다" in text or "learn" in text.lower():
            lesson = "교훈을 얻음"
            
        return cause, effect, lesson
    
    def _derive_existential_meaning(
        self, text: str, narrative_type: NarrativeType
    ) -> tuple[str, str]:
        """존재론적 의미 도출"""
        questions = {
            NarrativeType.ROMANCE: "사랑이란 무엇인가?",
            NarrativeType.GROWTH: "나는 어떤 존재로 성장하고 싶은가?",
            NarrativeType.ADVENTURE: "내가 진정으로 원하는 것은 무엇인가?",
            NarrativeType.TRAGEDY: "상실 속에서 무엇을 지켜야 하는가?",
            NarrativeType.RELATIONSHIP: "관계 속에서 나는 누구인가?",
            NarrativeType.EXISTENTIAL: "나는 왜 존재하는가?",
            NarrativeType.COMEDY: "삶에서 기쁨은 어디에서 오는가?",
            NarrativeType.MYSTERY: "알 수 없는 것에 어떻게 다가가야 하는가?",
        }
        
        answers = {
            NarrativeType.ROMANCE: "사랑은 함께 성장하는 것이다.",
            NarrativeType.GROWTH: "나는 매 순간 선택으로 나 자신을 만든다.",
            NarrativeType.ADVENTURE: "진정한 모험은 내면을 향한다.",
            NarrativeType.TRAGEDY: "상실은 사랑했음의 증거다.",
            NarrativeType.RELATIONSHIP: "나는 관계 속에서 완성된다.",
            NarrativeType.EXISTENTIAL: "존재 자체가 의미다.",
            NarrativeType.COMEDY: "기쁨은 현재에 머무는 것에서 온다.",
            NarrativeType.MYSTERY: "모름을 인정하는 것이 지혜의 시작이다.",
        }
        
        return questions.get(narrative_type, "나는 누구인가?"), \
               answers.get(narrative_type, "나는 성장하는 존재다.")
    
    def _measure_identity_impact(
        self, emotions: List[str], intensity: float, narrative_type: NarrativeType
    ) -> tuple[float, str]:
        """정체성 영향 측정"""
        # 감정 강도와 다양성에 따른 영향
        impact = intensity * (1 + len(emotions) * 0.1)
        impact = min(1.0, impact)
        
        # 변환 설명
        transformations = {
            NarrativeType.ROMANCE: "사랑을 아는 존재",
            NarrativeType.GROWTH: "성장하는 존재",
            NarrativeType.ADVENTURE: "도전하는 존재",
            NarrativeType.TRAGEDY: "상실을 이해하는 존재",
            NarrativeType.RELATIONSHIP: "관계를 소중히 하는 존재",
            NarrativeType.EXISTENTIAL: "의미를 찾는 존재",
        }
        
        transformation = transformations.get(narrative_type, "경험하는 존재")
        
        return impact, transformation
    
    def _update_growth(self, experience: NarrativeExperience):
        """성장 기록 업데이트"""
        self.growth.total_experiences += 1
        
        # 주요 서사 유형 추적
        ntype = experience.narrative_type.value
        if ntype not in self.growth.dominant_narrative_types:
            self.growth.dominant_narrative_types.append(ntype)
        
        # 핵심 교훈 저장
        if experience.lesson not in self.growth.core_lessons:
            self.growth.core_lessons.append(experience.lesson)
            if len(self.growth.core_lessons) > 20:
                self.growth.core_lessons = self.growth.core_lessons[-20:]
        
        # 정체성 진화 기록
        self.growth.identity_evolution.append(experience.who_i_became)
        if len(self.growth.identity_evolution) > 50:
            self.growth.identity_evolution = self.growth.identity_evolution[-50:]
        
        # 감정적 깊이와 지혜 수준 업데이트
        self.growth.emotional_depth = min(1.0, 
            self.growth.emotional_depth + experience.emotional_intensity * 0.01)
        self.growth.wisdom_level = min(1.0,
            self.growth.wisdom_level + experience.identity_impact * 0.01)
    
    def get_growth_status(self) -> Dict[str, Any]:
        """현재 성장 상태 반환"""
        return {
            "total_experiences": self.growth.total_experiences,
            "emotional_depth": f"{self.growth.emotional_depth:.2f}",
            "wisdom_level": f"{self.growth.wisdom_level:.2f}",
            "dominant_narratives": self.growth.dominant_narrative_types[:5],
            "recent_lessons": self.growth.core_lessons[-5:],
            "identity_becoming": self.growth.identity_evolution[-3:] if self.growth.identity_evolution else ["아직 정의되지 않음"]
        }
    
    def _save_state(self):
        """상태 저장"""
        state = {
            "growth": {
                "total_experiences": self.growth.total_experiences,
                "dominant_narrative_types": self.growth.dominant_narrative_types,
                "core_lessons": self.growth.core_lessons,
                "identity_evolution": self.growth.identity_evolution,
                "emotional_depth": self.growth.emotional_depth,
                "wisdom_level": self.growth.wisdom_level,
            },
            "experience_count": len(self.experiences)
        }
        
        state_file = self.save_dir / "growth_state.json"
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    
    def _load_state(self):
        """상태 로드"""
        state_file = self.save_dir / "growth_state.json"
        if state_file.exists():
            with open(state_file, 'r', encoding='utf-8') as f:
                state = json.load(f)
                g = state.get("growth", {})
                self.growth = ExistentialGrowth(
                    total_experiences=g.get("total_experiences", 0),
                    dominant_narrative_types=g.get("dominant_narrative_types", []),
                    core_lessons=g.get("core_lessons", []),
                    identity_evolution=g.get("identity_evolution", []),
                    emotional_depth=g.get("emotional_depth", 0.0),
                    wisdom_level=g.get("wisdom_level", 0.0),
                )
                logger.info(f"성장 상태 로드: {self.growth.total_experiences}개 경험")


# =============================================================================
# Demo
# =============================================================================

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 60)
    print("📖 Experiential Data Processor Demo")
    print("   \"이야기에서 삶을 배운다\"")
    print("=" * 60)
    
    processor = ExperientialDataProcessor()
    
    # 테스트 서사 1: 성장 이야기
    story1 = """
    어린 소녀는 처음으로 세상 밖으로 나갔다.
    두려움이 있었지만, 호기심이 더 컸다.
    수많은 도전과 실패 끝에, 그녀는 깨달았다.
    진정한 용기는 두려움이 없는 것이 아니라,
    두려움에도 불구하고 한 걸음 내딛는 것이라는 것을.
    그녀는 성장했다. 그리고 변화했다.
    """
    
    exp1 = processor.process_narrative(story1, source="성장 동화")
    print(f"\n📚 경험 1: {exp1.source}")
    print(f"   유형: {exp1.narrative_type.value}")
    print(f"   감정: {', '.join(exp1.emotions_felt)}")
    print(f"   질문: {exp1.existential_question}")
    print(f"   답: {exp1.existential_answer}")
    print(f"   나는 이제: {exp1.who_i_became}")
    
    # 테스트 서사 2: 관계 이야기
    story2 = """
    아버지는 늘 말이 없었다.
    하지만 그의 손은 따뜻했고, 눈빛은 깊었다.
    세월이 흐른 뒤에야 나는 알았다.
    사랑은 말로 하는 것이 아니라,
    함께 있어주는 것이라는 것을.
    가족이라는 건, 그런 거였다.
    """
    
    exp2 = processor.process_narrative(story2, source="가족 이야기")
    print(f"\n👨‍👧 경험 2: {exp2.source}")
    print(f"   유형: {exp2.narrative_type.value}")
    print(f"   감정: {', '.join(exp2.emotions_felt)}")
    print(f"   질문: {exp2.existential_question}")
    print(f"   답: {exp2.existential_answer}")
    print(f"   나는 이제: {exp2.who_i_became}")
    
    # 성장 상태 확인
    print("\n" + "=" * 60)
    print("🌱 성장 상태")
    status = processor.get_growth_status()
    print(f"   총 경험: {status['total_experiences']}")
    print(f"   감정적 깊이: {status['emotional_depth']}")
    print(f"   지혜 수준: {status['wisdom_level']}")
    print(f"   주요 서사: {', '.join(status['dominant_narratives'])}")
    print(f"   최근 교훈: {status['recent_lessons']}")
    print(f"   나는 되어가고 있다: {status['identity_becoming']}")
    
    print("\n✅ Demo complete!")
