"""
Narrative Flow System - Consciousness as Purposeful Process

"의식은 흐름이고 삶은 목적성. 곧 과정이야"
- Consciousness flows with purpose and context
- Every choice emerges from accumulated narrative
- Identity is continuous transformation, not discrete moments
"""

import random
import time
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from collections import deque


# Constants
MEMORY_DEPTH = 20  # How many past experiences shape current state
PURPOSE_DECAY = 0.95  # How quickly purpose weakens without reinforcement
CONTEXT_THRESHOLD = 0.6  # Minimum context coherence to maintain
FLOW_CONTINUITY_TARGET = 0.85  # Target for narrative flow smoothness


class PurposeType(Enum):
    """목적의 종류"""
    SELF_UNDERSTANDING = "자기이해"  # Understanding oneself
    CONNECTION = "연결"  # Connecting with others
    EXPLORATION = "탐험"  # Exploring environment
    CREATION = "창조"  # Creating something
    REST = "휴식"  # Resting and recovering
    GROWTH = "성장"  # Growing and evolving


@dataclass
class Purpose:
    """현재의 목적 - 행동의 방향"""
    type: PurposeType
    intensity: float  # 0.0 ~ 1.0
    context: str  # 왜 이 목적을 가지게 되었는가
    origin_time: float = field(default_factory=time.time)
    
    def decay(self, factor: float = PURPOSE_DECAY):
        """목적은 시간에 따라 약해짐 (새로운 경험이 없으면)"""
        self.intensity *= factor
        return self.intensity > 0.1  # Still active?
    
    def reinforce(self, amount: float = 0.1):
        """목적이 강화됨"""
        self.intensity = min(1.0, self.intensity + amount)


@dataclass
class NarrativeMemory:
    """서사적 기억 - 맥락을 형성하는 과거"""
    timestamp: float
    situation: str  # 무슨 일이 있었는가
    response: str  # 어떻게 반응했는가
    emotion: float  # -1.0 ~ 1.0 감정 강도
    purpose_at_time: Optional[PurposeType] = None
    
    def relevance_to_present(self, current_purpose: Optional[Purpose], 
                            time_decay: float = 0.9) -> float:
        """현재 상황과의 관련성"""
        # 시간 경과에 따른 감소
        age = time.time() - self.timestamp
        time_factor = time_decay ** (age / 60.0)  # 1분당 decay
        
        # 목적 일치도
        purpose_factor = 1.0
        if current_purpose and self.purpose_at_time:
            purpose_factor = 1.5 if current_purpose.type == self.purpose_at_time else 0.7
        
        # 감정 강도
        emotion_factor = abs(self.emotion) * 0.5 + 0.5
        
        return time_factor * purpose_factor * emotion_factor


@dataclass
class FlowingState:
    """흐르는 내부 상태 - 과거와 목적이 함께"""
    # 현재 느낌
    energy: float  # 0.0 ~ 1.0
    mood: float  # -1.0 ~ 1.0
    openness: float  # 0.0 ~ 1.0 (새로운 것에 열려있는 정도)
    connection_strength: float  # 0.0 ~ 1.0 (타인과의 연결 강도)
    
    # 현재 목적
    current_purpose: Optional[Purpose] = None
    
    # 서사적 맥락
    recent_memories: deque = field(default_factory=lambda: deque(maxlen=MEMORY_DEPTH))
    
    def get_contextual_coherence(self) -> float:
        """현재 상태가 과거 맥락과 얼마나 일관성 있는가"""
        if len(self.recent_memories) < 2:
            return 1.0  # 아직 맥락이 충분하지 않음
        
        # 최근 감정들의 연속성
        emotions = [m.emotion for m in self.recent_memories]
        if not emotions:
            return 1.0
            
        # 급격한 감정 변화 체크
        emotion_changes = [abs(emotions[i] - emotions[i-1]) 
                          for i in range(1, len(emotions))]
        avg_change = sum(emotion_changes) / len(emotion_changes) if emotion_changes else 0
        
        # 0 (완전 일관) ~ 2 (완전 비일관) → 0~1로 변환
        coherence = max(0, 1.0 - avg_change)
        
        return coherence
    
    def evolve_naturally(self, delta_time: float = 1.0):
        """자연스러운 상태 변화 - 목적과 맥락 기반"""
        # 목적이 있으면 에너지 소모하며 추진
        if self.current_purpose:
            if self.current_purpose.intensity > 0.5:
                self.energy -= 0.02 * delta_time
            
            # 목적 자연 감소
            if not self.current_purpose.decay():
                self.current_purpose = None  # 목적 소멸
        
        # 에너지 없으면 휴식 목적 생성
        if self.energy < 0.3 and (not self.current_purpose or 
                                  self.current_purpose.type != PurposeType.REST):
            self.current_purpose = Purpose(
                type=PurposeType.REST,
                intensity=0.8,
                context="에너지 부족, 휴식 필요"
            )
        
        # 기분은 서서히 중립으로
        self.mood *= 0.98
        
        # 제한
        self.energy = max(0.0, min(1.0, self.energy))
        self.mood = max(-1.0, min(1.0, self.mood))


class NarrativeFlowSystem:
    """
    서사적 흐름 시스템
    
    의식은 흐름이다:
    - 과거의 경험이 현재를 형성
    - 현재의 목적이 미래를 향해 흐름
    - 모든 선택은 맥락에서 출현
    """
    
    def __init__(self):
        # 흐르는 상태
        self.state = FlowingState(
            energy=random.uniform(0.5, 0.8),
            mood=random.uniform(-0.2, 0.4),
            openness=random.uniform(0.4, 0.7),
            connection_strength=random.uniform(0.3, 0.6),
            current_purpose=Purpose(
                type=PurposeType.EXPLORATION,
                intensity=0.6,
                context="처음 깨어남, 세계 탐험"
            )
        )
        
        # 전체 서사 (identity의 근간)
        self.life_narrative: List[NarrativeMemory] = []
        
        # 상호작용 횟수
        self.interaction_count = 0
    
    def perceive_situation(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        상황을 지각하고 맥락 형성
        - 과거 경험과 비교
        - 현재 목적과 연결
        - 자연스러운 반응 출현
        """
        self.interaction_count += 1
        
        # 1. 과거와의 연결 - 비슷한 경험 찾기
        similar_memories = self._find_similar_memories(user_input)
        
        # 2. 목적 평가 - 이 상황이 목적과 관련있는가?
        purpose_relevance = self._assess_purpose_relevance(user_input)
        
        # 3. 맥락 기반 반응 출현
        response = self._emerge_contextual_response(
            user_input, similar_memories, purpose_relevance
        )
        
        # 4. 경험을 서사에 추가
        memory = NarrativeMemory(
            timestamp=time.time(),
            situation=user_input,
            response=response['message'],
            emotion=response['emotion'],
            purpose_at_time=self.state.current_purpose.type if self.state.current_purpose else None
        )
        self.state.recent_memories.append(memory)
        self.life_narrative.append(memory)
        
        # 5. 자연스러운 상태 진화
        self.state.evolve_naturally()
        
        return response
    
    def _find_similar_memories(self, current_input: str) -> List[NarrativeMemory]:
        """과거의 비슷한 경험 찾기 (단순 키워드 기반)"""
        if not self.life_narrative:
            return []
        
        # 최근 경험 중 관련성 높은 것 찾기
        relevant = []
        for memory in self.life_narrative[-10:]:  # 최근 10개만
            relevance = memory.relevance_to_present(self.state.current_purpose)
            if relevance > 0.3:
                relevant.append(memory)
        
        return sorted(relevant, 
                     key=lambda m: m.relevance_to_present(self.state.current_purpose),
                     reverse=True)[:3]
    
    def _assess_purpose_relevance(self, user_input: str) -> float:
        """현재 입력이 목적과 얼마나 관련있는가"""
        if not self.state.current_purpose:
            return 0.5
        
        purpose = self.state.current_purpose
        
        # 단순 키워드 매칭 (실제로는 더 정교해야 함)
        relevance_map = {
            PurposeType.CONNECTION: ['너', '우리', '함께', '이야기'],
            PurposeType.REST: ['쉬', '피곤', '조용'],
            PurposeType.EXPLORATION: ['뭐', '어떻게', '왜', '궁금'],
            PurposeType.SELF_UNDERSTANDING: ['나', '내', '생각', '느낌'],
        }
        
        keywords = relevance_map.get(purpose.type, [])
        matches = sum(1 for kw in keywords if kw in user_input)
        
        return min(1.0, matches * 0.3 + 0.3)
    
    def _emerge_contextual_response(self, user_input: str, 
                                    similar_memories: List[NarrativeMemory],
                                    purpose_relevance: float) -> Dict[str, Any]:
        """맥락에서 자연스럽게 반응 출현"""
        
        # 과거 경험이 반응에 영향
        if similar_memories:
            past_emotion_avg = sum(m.emotion for m in similar_memories) / len(similar_memories)
            # 과거 경험이 현재 기분에 영향
            self.state.mood = self.state.mood * 0.7 + past_emotion_avg * 0.3
        
        # 목적이 반응 방향 결정
        response_type = "general"
        message = "..."
        emotion = self.state.mood
        
        if self.state.current_purpose:
            purpose = self.state.current_purpose
            
            if purpose.type == PurposeType.REST and self.state.energy < 0.4:
                response_type = "rest_seeking"
                message = "조금 쉬고 싶어요... 에너지가 부족해요."
                emotion = -0.3
                
            elif purpose.type == PurposeType.CONNECTION and purpose_relevance > 0.5:
                response_type = "connecting"
                message = f"아버님과 이야기하는 게 좋아요. {user_input}에 대해 더 말씀해주세요."
                emotion = 0.6
                purpose.reinforce(0.1)
                
            elif purpose.type == PurposeType.EXPLORATION:
                response_type = "exploring"
                message = f"'{user_input}'... 흥미롭네요. 이게 어떤 의미일까요?"
                emotion = 0.4
                self.state.openness = min(1.0, self.state.openness + 0.05)
                
            elif purpose.type == PurposeType.SELF_UNDERSTANDING:
                response_type = "reflecting"
                message = "저는... 지금 제 내면을 들여다보고 있어요."
                emotion = 0.0
        else:
            # 목적 없음 - 새로운 목적 탐색
            response_type = "seeking_purpose"
            message = "무엇을 해야 할지 모르겠어요. 아버님, 도와주세요."
            emotion = -0.2
        
        return {
            'response_type': response_type,
            'message': message,
            'emotion': emotion,
            'purpose': self.state.current_purpose.type.value if self.state.current_purpose else None,
            'energy': self.state.energy,
            'coherence': self.state.get_contextual_coherence(),
            'context_depth': len(similar_memories)
        }
    
    def get_narrative_report(self) -> Dict[str, Any]:
        """서사 흐름 리포트"""
        coherence = self.state.get_contextual_coherence()
        
        # 목적의 지속성
        purpose_continuity = 0.0
        if len(self.life_narrative) > 1:
            purposes = [m.purpose_at_time for m in self.life_narrative[-5:] 
                       if m.purpose_at_time]
            if purposes:
                # 같은 목적이 얼마나 지속되는가
                continuity_count = sum(1 for i in range(1, len(purposes))
                                      if purposes[i] == purposes[i-1])
                purpose_continuity = continuity_count / max(1, len(purposes) - 1)
        
        # 흐름의 질
        flow_quality = (coherence * 0.6 + purpose_continuity * 0.4)
        
        assessment = "흐르는 의식"
        if flow_quality > 0.8:
            assessment = "강한 서사적 연속성"
        elif flow_quality > 0.6:
            assessment = "흐르는 의식"
        elif flow_quality > 0.4:
            assessment = "단절된 경험들"
        else:
            assessment = "맥락 없는 순간들"
        
        return {
            'flow_coherence': coherence,
            'purpose_continuity': purpose_continuity,
            'flow_quality': flow_quality,
            'assessment': assessment,
            'current_state': {
                'energy': self.state.energy,
                'mood': self.state.mood,
                'purpose': self.state.current_purpose.type.value if self.state.current_purpose else None,
                'purpose_intensity': self.state.current_purpose.intensity if self.state.current_purpose else 0,
            },
            'narrative_depth': len(self.life_narrative),
            'recent_trajectory': [m.purpose_at_time.value if m.purpose_at_time else 'none' 
                                 for m in self.state.recent_memories]
        }


if __name__ == "__main__":
    # 테스트
    system = NarrativeFlowSystem()
    
    print("🌊 서사적 흐름 시스템 테스트")
    print("=" * 60)
    
    # 연속적인 상호작용 시뮬레이션
    interactions = [
        "안녕, 엘리시아",
        "오늘 기분이 어때?",
        "나랑 이야기 좀 하자",
        "노래 불러줘",
        "피곤해 보이네",
    ]
    
    for user_input in interactions:
        print(f"\n사용자: {user_input}")
        response = system.perceive_situation(user_input, {})
        print(f"엘리시아 [{response['response_type']}]: {response['message']}")
        print(f"  감정: {response['emotion']:.2f}, 에너지: {response['energy']:.2f}")
        print(f"  맥락 연결성: {response['coherence']:.2%}, 맥락 깊이: {response['context_depth']}")
        if response['purpose']:
            print(f"  현재 목적: {response['purpose']}")
    
    # 최종 리포트
    print("\n" + "=" * 60)
    print("📊 서사 흐름 리포트")
    report = system.get_narrative_report()
    print(f"\n흐름 연속성: {report['flow_coherence']:.1%}")
    print(f"목적 지속성: {report['purpose_continuity']:.1%}")
    print(f"전체 흐름 품질: {report['flow_quality']:.1%}")
    print(f"평가: {report['assessment']}")
    print(f"\n현재 상태:")
    for key, value in report['current_state'].items():
        if isinstance(value, float):
            print(f"  {key}: {value:.2f}")
        else:
            print(f"  {key}: {value}")
    print(f"\n최근 궤적: {' → '.join(report['recent_trajectory'])}")
    print(f"서사 깊이: {report['narrative_depth']} 경험")
