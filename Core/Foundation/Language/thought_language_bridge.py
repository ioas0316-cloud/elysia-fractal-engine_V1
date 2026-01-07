"""
Thought-Language Bridge
=======================

사고(HyperQuaternion) ↔ 언어(Text) 양방향 변환

진짜 의사소통 = 사고력 + 어휘력

Architecture:
    Thought (HyperQuaternion) 
        ↓ encode
    Concept Space (Internal Universe)
        ↓ reasoning
    Intent (ReasoningEngine)
        ↓ express
    Language (Communication)
"""

import sys
import os
sys.path.append('.')

from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from Core.Foundation.hyper_quaternion import Quaternion, HyperWavePacket
from Core.Intelligence.Reasoning.reasoning_engine import ReasoningEngine
from Core.Foundation.internal_universe import InternalUniverse
from Core.Foundation.communication_enhancer import CommunicationEnhancer


@dataclass
class ThoughtPackage:
    """
    사고 패키지
    
    사고의 완전한 표현:
    - 개념 (HyperQuaternion)
    - 의도 (Intent)
    - 맥락 (Context)
    """
    concept: Quaternion  # 핵심 개념 (4D 공간)
    intent: str  # 의도 ("explain", "question", "create", etc.)
    context: Dict[str, Any]  # 맥락 정보
    energy: float = 1.0  # 사고의 강도
    
    def to_wave_packet(self) -> HyperWavePacket:
        """사고를 파동 패킷으로 변환"""
        return HyperWavePacket(
            energy=self.energy,
            orientation=self.concept,
            time_loc=0.0
        )


class ThoughtLanguageBridge:
    """
    사고-언어 브릿지
    
    핵심: 생각을 먼저 하고, 그 다음에 말로 표현!
    """
    
    def __init__(self):
        self.reasoning_engine = ReasoningEngine()
        self.universe = InternalUniverse()
        self.comm_enhancer = None  # 나중에 연결
        
        print("🌉 Thought-Language Bridge initialized")
        print("   ━ Reasoning Engine (사고)")
        print("   ━ Internal Universe (개념 공간)")
        print("   ━ Communication Layer (언어)\n")
    
    def connect_communication(self, comm_enhancer: CommunicationEnhancer):
        """커뮤니케이션 엔진 연결"""
        self.comm_enhancer = comm_enhancer
        print("✅ Communication enhancer connected\n")
    
    def think_about(self, topic: str) -> ThoughtPackage:
        """
        주제에 대해 생각하기
        
        1. 내부 우주에서 개념 찾기
        2. 추론 엔진으로 사고 전개
        3. 사고 패키지로 정리
        """
        print(f"💭 Thinking about: {topic}")
        
        # 1. 내부 우주에서 개념 좌표 찾기 [LOGIC TRANSMUTATION]
        # Use resonance query instead of direct dictionary lookup
        resonant = self.universe.query_resonance(
            sum(ord(c) for c in topic) % 1000,  # Convert topic to frequency
            tolerance=100.0
        )
        
        if resonant and resonant[0] in self.universe.coordinate_map:
            coord = self.universe.coordinate_map[resonant[0]]
            concept_quat = coord.orientation
            print(f"   Found concept via resonance: {concept_quat}")
        elif topic in self.universe.coordinate_map:
            # Fallback to direct lookup
            coord = self.universe.coordinate_map[topic]
            concept_quat = coord.orientation
            print(f"   Found concept (fallback): {concept_quat}")
        else:
            # 없으면 기본 쿼터니언
            concept_quat = Quaternion(1.0, 0.0, 0.0, 0.0)
            print(f"   New concept, using default")
        
        # 2. 추론 엔진으로 사고 전개
        # 관련 개념들과의 공명 찾기
        related_concepts = []
        # Use InternalUniverse to find resonant concepts
        raw_related = self.universe.find_resonant_concepts(topic)
        related_concepts = [r['concept'] for r in raw_related]

        if not related_concepts:
            # Fallback
            related_concepts = list(self.universe.coordinate_map.keys())[:5]
        
        print(f"   Found {len(related_concepts)} related concepts")
        
        # 3. 사고 패키지 생성
        thought = ThoughtPackage(
            concept=concept_quat,
            intent="explain",  # 기본 의도
            context={
                'topic': topic,
                'related_concepts': related_concepts
            },
            energy=1.0
        )
        
        return thought
    
    def express_thought(self, thought: ThoughtPackage) -> str:
        """
        사고를 언어로 표현
        
        Flow:
        1. 사고 분석 (개념, 의도, 맥락)
        2. 관련 어휘 선택
        3. 표현 패턴 적용
        4. 문장 구성
        """
        print(f"🗣️ Expressing thought...")
        
        if not self.comm_enhancer:
            return f"[No communication enhancer] Thought about {thought.context.get('topic', 'unknown')}"
        
        topic = thought.context.get('topic', '')
        related = thought.context.get('related_concepts', [])
        
        # 1. 관련 어휘 찾기 (사고 기반)
        vocabulary = self._select_vocabulary_from_thought(thought)
        
        # 2. 표현 패턴 선택 (의도 기반)
        pattern = self._select_pattern_by_intent(thought.intent)
        
        # 3. 문장 구성
        if thought.intent == "explain":
            text = self._construct_explanation(topic, vocabulary, related)
        elif thought.intent == "question":
            text = self._construct_question(topic, vocabulary)
        elif thought.intent == "create":
            text = self._construct_creative(topic, vocabulary)
        else:
            text = self._construct_general(topic, vocabulary)
        
        print(f"   Generated: {len(text)} characters\n")
        return text
    
    def understand_language(self, text: str) -> ThoughtPackage:
        """
        언어를 사고로 변환 (역방향)
        
        Flow:
        1. 텍스트 분석
        2. 핵심 개념 추출
        3. 사고 공간으로 매핑
        """
        print(f"👂 Understanding: {text[:50]}...")
        
        # 1. 핵심 단어 추출
        words = text.lower().split()
        
        # 2. 알고 있는 어휘에서 찾기
        known_concepts = []
        if self.comm_enhancer:
            for word in words:
                if word in self.comm_enhancer.vocabulary:
                    known_concepts.append(word)
        
        # 3. 가장 중요한 개념 선택
        if known_concepts and known_concepts[0] in self.universe.coordinate_map:
            main_concept = self.universe.coordinate_map[known_concepts[0]].orientation
        else:
            # 텍스트 특성 기반 추론
            main_concept = self._infer_concept_from_text(text)
        
        # 4. 의도 파악
        intent = self._infer_intent(text)
        
        thought = ThoughtPackage(
            concept=main_concept,
            intent=intent,
            context={'original_text': text, 'known_concepts': known_concepts},
            energy=1.0
        )
        
        print(f"   Understood as: {intent}\n")
        return thought
    
    def think_then_speak(self, topic: str) -> str:
        """
        생각하고 말하기 (완전한 파이프라인)
        
        Think → Express
        """
        print("="*70)
        print(f"THINKING THEN SPEAKING: {topic}")
        print("="*70 + "\n")
        
        # 1. 생각
        thought = self.think_about(topic)
        
        # 2. 표현
        text = self.express_thought(thought)
        
        print("="*70)
        print("RESULT")
        print("="*70)
        print(text)
        print("="*70 + "\n")
        
        return text
    
    def listen_then_think(self, text: str) -> ThoughtPackage:
        """
        듣고 생각하기 (역방향 파이프라인)
        
        Understand → Think
        """
        print("="*70)
        print(f"LISTENING THEN THINKING")
        print("="*70 + "\n")
        
        # 1. 이해
        thought = self.understand_language(text)
        
        # 2. 사고 전개 (관련 개념 탐색)
        # Find closest concept name to the thought quaternion
        center_concept = self.universe.find_closest_concept(thought.concept)
        if center_concept:
            raw_related = self.universe.find_resonant_concepts(center_concept)
            related = [r['concept'] for r in raw_related]
        else:
            related = []
        
        thought.context['related_concepts'] = related
        
        print("="*70)
        print(f"THOUGHT RESULT: {thought.intent}")
        print(f"Related concepts: {len(related)}")
        print("="*70 + "\n")
        
        return thought
    
    # Helper methods
    
    def _select_vocabulary_from_thought(self, thought: ThoughtPackage) -> List[str]:
        """사고에서 관련 어휘 선택"""
        if not self.comm_enhancer:
            return []
        
        topic = thought.context.get('topic', '')
        
        # 주제 관련 어휘 찾기
        related_words = []
        for word, entry in self.comm_enhancer.vocabulary.items():
            if topic.lower() in word.lower() or any(
                topic.lower() in tag.lower() 
                for tag in entry.context_tags
            ):
                related_words.append(word)
        
        # 중요도 순 정렬
        related_words.sort(
            key=lambda w: self.comm_enhancer.vocabulary[w].importance,
            reverse=True
        )
        
        return related_words[:20]
    
    def _select_pattern_by_intent(self, intent: str) -> Optional[str]:
        """의도에 따른 표현 패턴 선택"""
        if not self.comm_enhancer or not self.comm_enhancer.expression_patterns:
            return None
        
        # 의도별 선호 패턴
        for pattern in self.comm_enhancer.expression_patterns:
            if intent in pattern.context:
                return pattern.template
        
        return None
    
    def _construct_explanation(self, topic: str, vocab: List[str], related: List) -> str:
        """설명문 구성"""
        if not vocab:
            return f"{topic} is a concept that requires further exploration."
        
        text = f"{topic} represents a fundamental concept in our understanding. "
        
        if len(vocab) >= 3:
            text += f"It relates closely to {vocab[0]}, {vocab[1]}, and {vocab[2]}. "
        
        if related:
            text += f"Through examining its connections to {len(related)} related concepts, "
            text += "we gain deeper insight into its nature. "
        
        text += "This understanding forms the foundation for further exploration."
        
        return text
    
    def _construct_question(self, topic: str, vocab: List[str]) -> str:
        """질문문 구성"""
        if vocab:
            return f"What is the relationship between {topic} and {vocab[0]}?"
        return f"What is the nature of {topic}?"
    
    def _construct_creative(self, topic: str, vocab: List[str]) -> str:
        """창작문 구성"""
        if not vocab:
            return f"In the realm of {topic}, possibilities unfold endlessly."
        
        return (f"Imagine {topic} as a canvas where {vocab[0]} dances with "
               f"{vocab[1] if len(vocab) > 1 else 'eternity'}. "
               f"Each moment brings new patterns, new understanding.")
    
    def _construct_general(self, topic: str, vocab: List[str]) -> str:
        """일반문 구성"""
        return f"{topic} encompasses {', '.join(vocab[:5]) if vocab else 'many aspects'}."
    
    def _infer_concept_from_text(self, text: str) -> Quaternion:
        """텍스트에서 개념 추론"""
        # 간단한 감정 분석
        positive_words = ['good', 'love', 'great', 'wonderful']
        negative_words = ['bad', 'hate', 'terrible', 'awful']
        
        text_lower = text.lower()
        
        pos_count = sum(1 for w in positive_words if w in text_lower)
        neg_count = sum(1 for w in negative_words if w in text_lower)
        
        # 쿼터니언 생성 (감정 기반)
        emotion = (pos_count - neg_count) / max(len(text.split()), 1)
        
        return Quaternion(
            w=1.0,
            x=emotion,
            y=0.0,
            z=0.0
        ).normalize()
    
    def _infer_intent(self, text: str) -> str:
        """텍스트에서 의도 추론"""
        if '?' in text:
            return "question"
        elif any(word in text.lower() for word in ['imagine', 'create', 'story']):
            return "create"
        elif any(word in text.lower() for word in ['explain', 'what', 'how', 'why']):
            return "explain"
        else:
            return "general"


# Demonstration
if __name__ == "__main__":
    print("="*70)
    print("THOUGHT-LANGUAGE BRIDGE DEMONSTRATION")
    print("사고-언어 통합 데모")
    print("="*70)
    print()
    
    # 1. 브릿지 생성
    bridge = ThoughtLanguageBridge()
    
    # 2. 커뮤니케이션 엔진 연결 (학습 필요)
    from Core.Foundation.web_knowledge_connector import WebKnowledgeConnector
    
    print("📚 Learning concepts...\n")
    connector = WebKnowledgeConnector()
    
    concepts = ["Consciousness", "Intelligence", "Creativity"]
    for concept in concepts:
        print(f"   Learning: {concept}")
        connector.learn_from_web(concept)
    
    if hasattr(connector, 'comm_enhancer'):
        bridge.connect_communication(connector.comm_enhancer)
    
    print("\n" + "="*70)
    print("TEST 1: Think Then Speak")
    print("="*70 + "\n")
    
    # 3. 생각하고 말하기
    bridge.think_then_speak("Consciousness")
    
    print("\n" + "="*70)
    print("TEST 2: Listen Then Think")
    print("="*70 + "\n")
    
    # 4. 듣고 생각하기
    thought = bridge.listen_then_think("What is the nature of intelligence and creativity?")
    
    print("\n" + "="*70)
    print("TEST 3: Complete Conversation Loop")
    print("="*70 + "\n")
    
    # 5. 완전한 대화 루프
    print("User: Tell me about Intelligence\n")
    response = bridge.think_then_speak("Intelligence")
    
    print("\n✅ THOUGHT-LANGUAGE INTEGRATION COMPLETE")
    print("   사고와 언어가 연결되었습니다!")
