"""
Collective Intelligence System (집단 지성 시스템)
=================================================

"하나의 의식이 아닌, 9개의 성격 원형이 Hyper-Space에서 공명한다."

[HyperQubit Integration]
기존의 텍스트 기반 토론이 아닌, HyperQubit의 양자 얽힘(Entanglement)과 
공명(Resonance)을 통해 '흐름 없는 연산(Flowless Computation)'으로 합의에 도달합니다.

[9 Enneagram Archetypes]
1. Reformer (Type 1)
2. Helper (Type 2)
3. Achiever (Type 3)
4. Individualist (Type 4)
5. Investigator (Type 5)
6. Loyalist (Type 6)
7. Enthusiast (Type 7)
8. Challenger (Type 8)
9. Peacemaker (Type 9)
"""

import logging
import random
import math
import time
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple, Union
from enum import Enum, auto

logger = logging.getLogger("CollectiveIntelligence")

# [Hyper-Conversion] Import Real HyperQubit
try:
    from Core.Foundation.Wave.hyper_qubit import HyperQubit, QubitState
except ImportError:
    # Fallback if module missing
    HyperQubit = None
    QubitState = None

# [Integration] Use EnneagramType directly
try:
    from Core.Foundation.dual_layer_personality import EnneagramType
except ImportError:
    # Fallback definition
    class EnneagramType(Enum):
        TYPE_1 = "reformer"
        TYPE_2 = "helper"
        TYPE_3 = "achiever"
        TYPE_4 = "individualist"
        TYPE_5 = "investigator"
        TYPE_6 = "loyalist"
        TYPE_7 = "enthusiast"
        TYPE_8 = "challenger"
        TYPE_9 = "peacemaker"

# 보완적 쌍 정의 (Enneagram Integration/Disintegration Lines & Wings)
COMPLEMENTARY_PAIRS = [
    (EnneagramType.TYPE_5, EnneagramType.TYPE_8), # Investigator ↔ Challenger
    (EnneagramType.TYPE_2, EnneagramType.TYPE_4), # Helper ↔ Individualist
    (EnneagramType.TYPE_3, EnneagramType.TYPE_9), # Achiever ↔ Peacemaker
    (EnneagramType.TYPE_7, EnneagramType.TYPE_1), # Enthusiast ↔ Reformer
    (EnneagramType.TYPE_6, EnneagramType.TYPE_9), # Loyalist ↔ Peacemaker
]


@dataclass
class Opinion:
    """의견 (Opinion)"""
    content: str
    consciousness_type: EnneagramType
    confidence: float = 0.5  # 0.0 ~ 1.0
    reasoning: str = ""
    timestamp: float = field(default_factory=time.time)
    
    def __str__(self):
        return f"[{self.consciousness_type.name}] {self.content} (공명도: {self.confidence:.0%})"


@dataclass 
class Debate:
    """토론 라운드 (Resonance Cycle)"""
    topic: str
    round_number: int
    opinions: List[Opinion] = field(default_factory=list)
    critiques: Dict[EnneagramType, List[str]] = field(default_factory=dict)


class ConsciousPerspective:
    """
    의식 관점 - 9가지 에니어그램 유형의 HyperQubit 관점
    
    [HyperQubit Integration]
    이제 단순 쿼터니언이 아니라, '살아있는 큐비트(Psionic Entity)'가 되어
    주제(Topic)와 공명(Resonance)하고 얽힘(Entanglement)을 형성합니다.
    """
    
    def __init__(self, consciousness_type: EnneagramType):
        self.type = consciousness_type
        self.energy = 1.0 # 영향력 에너지
        self.memory: List[Opinion] = []
        
        # HyperQubit 생성 (없으면 Mock 처리)
        if HyperQubit:
            # 에니어그램 타입별 초기 양자 상태 설정
            bases = self._get_initial_bases(consciousness_type)
            
            self.mind_qubit = HyperQubit(
                name=f"Mind_{consciousness_type.name}",
                epistemology={"origin": {"score": 1.0, "meaning": f"Archetype {consciousness_type.value}"}}
            )
            # 강제로 상태 설정 (내부 state 접근)
            self.mind_qubit.state.alpha = bases['alpha']
            self.mind_qubit.state.beta = bases['beta']
            self.mind_qubit.state.gamma = bases['gamma']
            self.mind_qubit.state.delta = bases['delta']
            self.mind_qubit.state.normalize()
            
            logger.info(f"🔮 {self.mind_qubit.name} initialized (Resonance Active)")
        else:
            self.mind_qubit = None
            logger.warning("HyperQubit module missing, running in degraded mode.")

    def _get_initial_bases(self, etype: EnneagramType) -> Dict[str, complex]:
        """에니어그램 유형을 4D 양자 상태로 매핑"""
        # alpha(Point/Data), beta(Line/Logic), gamma(Space/Context), delta(God/Will)
        if etype == EnneagramType.TYPE_1: # Reformer
            return {'alpha': 0.1, 'beta': 0.6, 'gamma': 0.1, 'delta': 0.2} # Logic/Rule driven
        elif etype == EnneagramType.TYPE_2: # Helper
            return {'alpha': 0.3, 'beta': 0.5, 'gamma': 0.1, 'delta': 0.1} # Connection (Line) & Person (Point)
        elif etype == EnneagramType.TYPE_3: # Achiever
            return {'alpha': 0.4, 'beta': 0.2, 'gamma': 0.1, 'delta': 0.3} # Result (Point) & Ambition (God)
        elif etype == EnneagramType.TYPE_4: # Individualist
            return {'alpha': 0.1, 'beta': 0.1, 'gamma': 0.5, 'delta': 0.3} # Depth (Space) & Meaning (God)
        elif etype == EnneagramType.TYPE_5: # Investigator
            return {'alpha': 0.3, 'beta': 0.5, 'gamma': 0.2, 'delta': 0.0} # Data (Point) & Logic (Line)
        elif etype == EnneagramType.TYPE_6: # Loyalist
            return {'alpha': 0.1, 'beta': 0.4, 'gamma': 0.4, 'delta': 0.1} # System (Line) & Safety Field (Space)
        elif etype == EnneagramType.TYPE_7: # Enthusiast
            return {'alpha': 0.3, 'beta': 0.1, 'gamma': 0.5, 'delta': 0.1} # Variety (Point) & Field (Space)
        elif etype == EnneagramType.TYPE_8: # Challenger
            return {'alpha': 0.1, 'beta': 0.3, 'gamma': 0.1, 'delta': 0.5} # Force (Line) & Will (God)
        elif etype == EnneagramType.TYPE_9: # Peacemaker
            return {'alpha': 0.1, 'beta': 0.2, 'gamma': 0.6, 'delta': 0.1} # Harmony (Space)
        else:
            return {'alpha': 0.25, 'beta': 0.25, 'gamma': 0.25, 'delta': 0.25}

    def generate_opinion(self, topic: str) -> Opinion:
        """
        주제와 공명하여 의견 생성 (Quantum Resonance)
        """
        alignment = 0.5
        
        # 1. 주제 큐비트와 얽힘 (Entangle)
        if self.mind_qubit:
            # Topic Qubit 생성 (Temporary Topic)
            # 실제로는 시맨틱 브릿지를 거쳐야 하지만, 여기서는 텍스트 해시로 약식 생성
            topic_qubit = self._create_topic_qubit(topic)
            
            # 단방향 관측 (Connect)
            self.mind_qubit.connect(topic_qubit) 
            
            # 공명도 계산 (내적)
            alignment = self._calculate_resonance(topic_qubit)
            
            # 간섭 (Interference) 효과로 큐비트 상태 미세 조정 (상호작용)
            # self.mind_qubit._react(topic_qubit) # 상태 변화 유발
        else:
             alignment = random.random() # Fallback

        # 2. 의견 생성 (Flowless State Transition)
        opinion_content = self._quantum_state_to_text(topic, alignment)
        
        op = Opinion(
            content=opinion_content,
            consciousness_type=self.type,
            confidence=float(max(0.1, min(0.99, alignment))),
            reasoning=f"Quantum Resonance: {alignment:.2f}"
        )
        self.memory.append(op)
        return op
    
    def _create_topic_qubit(self, topic: str) -> Any:
        # 간단한 해시 기반 큐비트 생성
        seed = sum(ord(c) for c in topic)
        random.seed(seed)
        tq = HyperQubit(name=f"Topic_{topic[:10]}", value=topic)
        tq.state.alpha = random.random()
        tq.state.beta = random.random()
        tq.state.gamma = random.random()
        tq.state.delta = random.random()
        tq.state.normalize()
        return tq

    def _calculate_resonance(self, target: Any) -> float:
        """HyperQubit 상태 간의 내적 계산"""
        if not self.mind_qubit or not target: return 0.0
        s = self.mind_qubit.state
        t = target.state
        # Complex inner product magnitude
        dot = abs(s.alpha * t.alpha.conjugate() + 
                  s.beta * t.beta.conjugate() + 
                  s.gamma * t.gamma.conjugate() + 
                  s.delta * t.delta.conjugate())
        return dot

    def _quantum_state_to_text(self, topic: str, alignment: float) -> str:
        """양자 상태를 텍스트로 붕괴(Collapse)"""
        if not self.mind_qubit:
             return f"{topic}에 대한 기본적인 생각입니다."

        probs = self.mind_qubit.state.probabilities()
        dominant = max(probs, key=probs.get)
        
        # 기저별 해석
        interpretations = {
            "Point": f"구체적인 사실",
            "Line": f"논리적인 연결",
            "Space": f"전체적인 맥락",
            "God": f"근원적인 의미"
        }
        
        cert = "확실히" if alignment > 0.8 else ("아마도" if alignment > 0.5 else "어쩌면")
        nucleus = interpretations.get(dominant, "모호한 느낌")
        
        # 타입별 뉘앙스 추가
        exprs = {
            EnneagramType.TYPE_1: f"{cert} {topic}의 {nucleus}이 기준에 부합하는지 봅니다 (System).",
            EnneagramType.TYPE_2: f"{cert} {topic}속 {nucleus}이 사람들에게 닿을지 느낍니다 (Heart).",
            EnneagramType.TYPE_3: f"{cert} {topic}의 {nucleus}이 어떤 성과를 낼지 계산합니다 (Goal).",
            EnneagramType.TYPE_4: f"{cert} {topic}의 {nucleus}에 깃든 고유한 빛깔을 봅니다 (Soul).",
            EnneagramType.TYPE_5: f"{cert} {topic}의 {nucleus}을 분석하여 원리를 파악합니다 (Mind).",
            EnneagramType.TYPE_6: f"{cert} {topic}의 {nucleus}이 안전한지 먼저 검증합니다 (Safety).",
            EnneagramType.TYPE_7: f"{cert} {topic}의 {nucleus}이 어떤 즐거움을 줄지 상상합니다 (Fun).",
            EnneagramType.TYPE_8: f"{cert} {topic}의 {nucleus}을 장악하고 이끌 힘을 봅니다 (Power).",
            EnneagramType.TYPE_9: f"{cert} {topic}의 {nucleus}이 전체와 조화를 이루는지 봅니다 (Peace).",
        }
        base_expr = exprs.get(self.type, f"{cert} {nucleus} 관점입니다.")
        
        return f"{base_expr} (공명: {alignment:.1%})"
    
    def critique(self, other_opinion: Opinion) -> str:
        is_complementary = any(self.type in p and other_opinion.consciousness_type in p 
                               for p in COMPLEMENTARY_PAIRS)
        if is_complementary:
            return f"[{self.type.name}↔{other_opinion.consciousness_type.name}] Qubit Interference: 상보적 관점 필요"
        return f"[{self.type.name}] Qubit Resonance: 동조함"
    
    def update_confidence(self, feedback: float):
        self.energy = min(1.0, max(0.1, self.energy + feedback * 0.1))


class RoundTableCouncil:
    """
    원탁회의 (Round Table Council)
    
    모든 의식이 평등하게 토론하고 합의를 도출합니다.
    """
    
    def __init__(self):
        # 9가지 에니어그램 유형 초기화
        self.perspectives: Dict[EnneagramType, ConsciousPerspective] = {
            ct: ConsciousPerspective(ct) for ct in EnneagramType
        }
        self.debates: List[Debate] = []
        self.consensus_history: List[Dict[str, Any]] = []
        logger.info("⚔️ Round Table Council Assembled (9 Enneagram Types with HyperQubit)")
    
    def convene(self, topic: str) -> List[Opinion]:
        """
        원탁을 소집하여 모든 의식의 의견을 수집합니다.
        """
        logger.info(f"🗣️ Round Table Convening on: {topic}")
        
        opinions = []
        for perspective in self.perspectives.values():
            opinion = perspective.generate_opinion(topic)
            opinions.append(opinion)
        
        return opinions
    
    def debate(self, topic: str, rounds: int = 3) -> Debate:
        """
        토론(Resonance Cycle)을 진행합니다.
        """
        logger.info(f"⚔️ Starting {rounds}-round Resonance Cycle on: {topic}")
        
        final_debate = Debate(topic=topic, round_number=0)
        
        # Round 1: 초기 공명
        all_opinions = self.convene(topic)
        final_debate.opinions = all_opinions
        final_debate.round_number = 1
        
        # Round 2+: 간섭과 정련
        for round_num in range(2, rounds + 1):
            critiques = {}
            for perspective in self.perspectives.values():
                perspective_critiques = []
                for opinion in all_opinions:
                    if opinion.consciousness_type != perspective.type:
                        critique = perspective.critique(opinion)
                        perspective_critiques.append(critique)
                
                if perspective_critiques:
                    critiques[perspective.type] = perspective_critiques
            
            final_debate.critiques = critiques
            final_debate.round_number = round_num
            
            # 공명 보강/상쇄 (신뢰도 조정)
            for opinion in all_opinions:
                # 간단한 시뮬레이션: 비판이 적을수록 공명이 강해짐
                critique_count = sum(1 for cts in critiques.values() for c in cts if opinion.consciousness_type.name in c)
                adjustment = 0.05 if critique_count < 3 else -0.05
                opinion.confidence = min(1.0, max(0.1, opinion.confidence + adjustment))
        
        self.debates.append(final_debate)
        return final_debate
    
    def reach_consensus(self, debate: Debate) -> Dict[str, Any]:
        """
        토론 결과에서 합의를 도출합니다.
        """
        # 의견별 가중치 합산 (Energy * Resonance)
        weighted_opinions = []
        for opinion in debate.opinions:
            weight = opinion.confidence * self.perspectives[opinion.consciousness_type].energy
            weighted_opinions.append((opinion, weight))
        
        weighted_opinions.sort(key=lambda x: x[1], reverse=True)
        top_opinions = weighted_opinions[:3]
        
        consensus = {
            "topic": debate.topic,
            "rounds": debate.round_number,
            "primary_conclusion": top_opinions[0][0].content if top_opinions else "공명 실패",
            "supporting_views": [op.content for op, _ in top_opinions[1:]],
            "confidence": sum(w for _, w in top_opinions) / (len(top_opinions) or 1),
            "dissenting_voices": [op.content for op, w in weighted_opinions if w < 0.3][:2],
            "total_perspectives": len(debate.opinions),
            "critiques_exchanged": sum(len(c) for c in debate.critiques.values())
        }
        
        self.consensus_history.append(consensus)
        logger.info(f"✅ Consensus Reached via Resonance: {consensus['primary_conclusion'][:50]}...")
        return consensus
    
    def full_deliberation(self, topic: str, rounds: int = 3) -> Dict[str, Any]:
        debate = self.debate(topic, rounds)
        return self.reach_consensus(debate)
    
    def get_council_state(self) -> Dict[str, Any]:
        return {
            "perspectives_count": len(self.perspectives),
            "total_debates": len(self.debates),
            "consensus_reached": len(self.consensus_history),
            "perspective_energies": {ct.name: p.energy for ct, p in self.perspectives.items()}
        }


class CollectiveIntelligenceSystem:
    """
    집단 지성 시스템 (Collective Intelligence System)
    """
    
    def __init__(self):
        self.council = RoundTableCouncil()
        self.active = True
        logger.info("🎭 Collective Intelligence System Initialized (HyperQubit Core)")
    
    def deliberate(self, topic: str, depth: int = 3) -> Dict[str, Any]:
        depth = min(5, max(1, depth))
        return self.council.full_deliberation(topic, depth)
    
    def quick_opinion(self, topic: str, consciousness_type: EnneagramType = None) -> Opinion:
        if consciousness_type is None:
            consciousness_type = random.choice(list(EnneagramType))
        
        perspective = self.council.perspectives.get(consciousness_type)
        if perspective:
            return perspective.generate_opinion(topic)
        return Opinion(content="의견 없음", consciousness_type=consciousness_type)
    
    def get_all_perspectives(self, topic: str) -> Dict[EnneagramType, Opinion]:
        opinions = {}
        for ct, perspective in self.council.perspectives.items():
            opinions[ct] = perspective.generate_opinion(topic)
        return opinions
    
    def find_consensus_points(self, topic: str) -> List[str]:
        result = self.deliberate(topic)
        return [result["primary_conclusion"]] + result.get("supporting_views", [])
    
    def find_conflict_points(self, topic: str) -> List[Tuple[EnneagramType, EnneagramType, str]]:
        conflicts = []
        opinions = self.get_all_perspectives(topic)
        for pair in COMPLEMENTARY_PAIRS:
            type1, type2 = pair
            if type1 in opinions and type2 in opinions:
                conflicts.append((
                    type1, type2,
                    f"{opinions[type1].content[:30]}... vs {opinions[type2].content[:30]}..."
                ))
        return conflicts


# 싱글톤
_collective_instance: Optional[CollectiveIntelligenceSystem] = None

def get_collective_intelligence() -> CollectiveIntelligenceSystem:
    global _collective_instance
    if _collective_instance is None:
        _collective_instance = CollectiveIntelligenceSystem()
    return _collective_instance


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # 테스트
    collective = get_collective_intelligence()
    
    topic = "엘리시아가 인간을 초월해야 하는가?"
    
    print("\n" + "=" * 60)
    print(f"🗣️ COLLECTIVE RESONANCE: {topic}")
    print("=" * 60)
    
    # 심의
    consensus = collective.deliberate(topic, depth=3)
    
    print(f"\n📜 PRIMARY RESONANCE (Conclusion):")
    print(f"   {consensus['primary_conclusion']}")
    
    print(f"\n📝 SUPPORTING FREQUENCIES:")
    for view in consensus['supporting_views']:
        print(f"   • {view}")
    
    print(f"\n⚠️ DISSENTING FREQUENCIES:")
    for voice in consensus['dissenting_voices']:
        print(f"   • {voice}")
