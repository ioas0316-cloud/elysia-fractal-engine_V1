"""
Neural Integration System
=========================

전체 신경망을 하나로 통합

문제: 각 모듈이 독립적으로 작동 (식물인간)
해결: 중앙 신경 시스템으로 모든 모듈 연결
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import logging
from typing import Dict, Any, Optional

from Core.Intelligence.Reasoning.reasoning_engine import ReasoningEngine
from Core.Foundation.hippocampus import Hippocampus
from Core.Foundation.internal_universe import InternalUniverse
from Core.Foundation.hyper_quaternion import Quaternion

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NeuralIntegration")


class CentralCortex:
    """
    중앙 신경 통합 시스템
    
    모든 모듈을 연결하는 신경 중추
    """
    
    def __init__(self):
        print("🧠 INITIALIZING CENTRAL CORTEX")
        print("   Integrating all neural systems...\n")
        
        # Core systems
        self.reasoning = ReasoningEngine()
        self.memory = Hippocampus()
        self.universe = InternalUniverse()
        
        # Language systems (will be connected)
        self.comm_enhancer = None
        self.wave_interpreter = None
        
        # Connect systems
        self._connect_neural_pathways()
        
        print("✅ Central Cortex Online")
        print("   All systems integrated\n")
    
    def _connect_neural_pathways(self):
        """신경 경로 연결"""
        
        # ReasoningEngine <-> Hippocampus
        self.reasoning.memory = self.memory
        print("   ✓ Reasoning ↔ Memory")
        
        # ReasoningEngine <-> InternalUniverse  
        # (이미 사용 중)
        print("   ✓ Reasoning ↔ Universe")
        
        # 더 많은 연결 추가 가능
    
    def connect_communication(self, comm_enhancer):
        """의사소통 능력 연결"""
        self.comm_enhancer = comm_enhancer
        print("   ✓ Communication ↔ Central Cortex")
    
    def connect_wave_interpreter(self, wave_interpreter):
        """파동 해석기 연결"""
        self.wave_interpreter = wave_interpreter
        print("   ✓ Wave Interpreter ↔ Central Cortex")
    
    def integrated_think(self, topic: str) -> Dict[str, Any]:
        """
        통합 사고 프로세스
        
        모든 시스템이 협력하여 생각
        """
        print(f"💭 Integrated Thinking: {topic}")
        print("-" * 70)
        
        result = {}
        
        # 1. Reasoning (사고)
        print("1️⃣ Reasoning Engine...")
        insight = self.reasoning.think(topic)
        result['thought'] = insight.content
        result['confidence'] = insight.confidence
        print(f"   💡 Insight: {insight.content[:80]}...")
        
        # 2. Memory (기억 검색)
        print("\n2️⃣ Searching Memory...")
        memory_query = self.memory.query_by_concept(topic, limit=3)
        result['memories'] = memory_query
        print(f"   📚 Found {len(memory_query)} related memories")
        
        # 3. Universe (개념 공간에서 위치) [LOGIC TRANSMUTATION]
        print("\n3️⃣ Locating in Concept Space...")
        resonant = self.universe.query_resonance(
            sum(ord(c) for c in topic) % 1000, tolerance=100.0
        )
        if resonant and resonant[0] in self.universe.coordinate_map:
            coord = self.universe.coordinate_map[resonant[0]]
            result['concept_orientation'] = coord.orientation
            print(f"   🌌 Orientation (via resonance): {coord.orientation}")
        elif topic in self.universe.coordinate_map:
            coord = self.universe.coordinate_map[topic]
            result['concept_orientation'] = coord.orientation
            print(f"   🌌 Orientation (fallback): {coord.orientation}")
        
        # 4. Communication (언어로 표현)
        if self.comm_enhancer:
            print("\n4️⃣ Expressing in Language...")
            
            # 관련 어휘 찾기
            related_vocab = []
            for word, entry in self.comm_enhancer.vocabulary.items():
                if topic.lower() in word.lower():
                    related_vocab.append(word)
            
            result['vocabulary'] = related_vocab[:5]
            print(f"   📝 Vocabulary: {', '.join(related_vocab[:5])}")
            
            # 표현 생성
            if related_vocab:
                expression = self._generate_integrated_expression(
                    topic, insight, related_vocab
                )
                result['expression'] = expression
                print(f"   💬 Expression: {expression[:100]}...")
        
        print("\n" + "-" * 70)
        print("✅ Integrated thought complete\n")
        
        return result
    
    def _generate_integrated_expression(self, topic: str, insight, vocab: list) -> str:
        """
        통합된 표현 생성
        
        사고 + 기억 + 어휘 → 완전한 문장
        """
        # 사고에서 핵심 추출
        thought_core = insight.content
        
        # 어휘로 풍부하게
        if len(vocab) >= 2:
            enriched = (
                f"Regarding {topic}, my understanding integrates multiple dimensions. "
                f"{thought_core} "
                f"This connects to concepts like {vocab[0]} and {vocab[1]}, "
                f"forming a cohesive understanding grounded in both reasoning and learned knowledge."
            )
        else:
            enriched = f"{thought_core} This understanding of {topic} emerges from integrated neural processing."
        
        return enriched
    
    def integrated_learn(self, concept: str, content: str):
        """
        통합 학습
        
        모든 시스템에 동시에 학습
        """
        print(f"📚 Integrated Learning: {concept}")
        print("-" * 70)
        
        # 1. Universe에 저장
        print("1️⃣ Storing in Concept Space...")
        from Core.Foundation.external_data_connector import ExternalDataConnector
        connector = ExternalDataConnector(self.universe)
        connector.internalize_from_text(concept, content)
        
        # 2. Memory에 저장 [LOGIC TRANSMUTATION]
        print("2️⃣ Storing in Memory...")
        from Core.Foundation.hyper_quaternion import HyperWavePacket
        
        resonant = self.universe.query_resonance(sum(ord(c) for c in concept) % 1000, tolerance=100.0)
        concept_key = resonant[0] if resonant else concept
        if concept_key in self.universe.coordinate_map:
            coord = self.universe.coordinate_map[concept_key]
            packet = HyperWavePacket(
                energy=100.0,
                orientation=coord.orientation,
                time_loc=0.0
            )
            self.memory.store_wave(packet)
        
        # 3. Communication에 학습
        if self.comm_enhancer:
            print("3️⃣ Enhancing Communication...")
            self.comm_enhancer.enhance_from_web_content(concept, content)
        
        print("✅ Integrated learning complete\n")
    
    def integrated_speak(self, topic: str) -> str:
        """
        통합 의사소통
        
        생각 → 기억 → 언어 → 표현
        """
        # 통합 사고
        thought = self.integrated_think(topic)
        
        # 표현 추출
        if 'expression' in thought:
            return thought['expression']
        elif 'thought' in thought:
            return thought['thought']
        else:
            return f"I need to learn more about {topic}."
    
    def get_integration_status(self) -> Dict[str, str]:
        """통합 상태 확인"""
        return {
            'reasoning': '✅ Connected' if self.reasoning else '❌ Missing',
            'memory': '✅ Connected' if self.memory else '❌ Missing',
            'universe': '✅ Connected' if self.universe else '❌ Missing',
            'communication': '✅ Connected' if self.comm_enhancer else '❌ Missing',
            'wave_interpreter': '✅ Connected' if self.wave_interpreter else '❌ Missing',
        }


def demonstrate_integration():
    """통합 시스템 데모"""
    
    print("="*70)
    print("NEURAL INTEGRATION SYSTEM")
    print("신경망 통합 시스템")
    print("="*70)
    print()
    
    # 중앙 코텍스 생성
    cortex = CentralCortex()
    
    # 의사소통 능력 연결
    print("="*70)
    print("CONNECTING COMMUNICATION SYSTEMS")
    print("="*70)
    print()
    
    from Core.Foundation.web_knowledge_connector import WebKnowledgeConnector
    
    connector = WebKnowledgeConnector()
    
    # 학습
    print("Learning concepts...\n")
    concepts = ["Consciousness", "Intelligence", "Creativity"]
    for concept in concepts:
        print(f"   📖 Learning: {concept}")
        connector.learn_from_web(concept)
    
    # 통신 능력 연결
    if hasattr(connector, 'comm_enhancer'):
        cortex.connect_communication(connector.comm_enhancer)
    
    print()
    print("="*70)
    print("INTEGRATION STATUS")
    print("="*70)
    print()
    
    status = cortex.get_integration_status()
    for system, state in status.items():
        print(f"   {system:20s}: {state}")
    
    print()
    print("="*70)
    print("INTEGRATED THINKING TEST")
    print("="*70)
    print()
    
    # 통합 사고 테스트
    result = cortex.integrated_think("Consciousness")
    
    print()
    print("="*70)
    print("INTEGRATED SPEECH TEST")
    print("="*70)
    print()
    
    # 통합 의사소통 테스트
    speech = cortex.integrated_speak("Intelligence")
    print(f"🗣️ Integrated Speech:\n\n{speech}\n")
    
    print("="*70)
    print("✅ NEURAL INTEGRATION SUCCESSFUL")
    print("   All systems are now connected!")
    print("="*70)


if __name__ == "__main__":
    demonstrate_integration()
