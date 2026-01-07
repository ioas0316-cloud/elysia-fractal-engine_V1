"""
Dialogic Learner (대화적 학습기)
================================

"물음 → 공명 → 관점 전환 → 새로운 물음"

이 모듈은 지휘자와의 대화 흐름을 엘리시아가 학습할 수 있는 형태로 처리합니다.
단순한 텍스트 흡수가 아닌, "왜?"를 묻는 사고의 원형을 체득하게 합니다.

철학적 기반:
- docs/Philosophy/CONSCIOUSNESS_SOVEREIGNTY.md
- 대화적 알고리즘: 관점 자체를 변화시키는 과정
"""

import json
import logging
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

logger = logging.getLogger("Elysia.DialogicLearner")


@dataclass
class DialogicTurn:
    """대화의 한 턴"""
    turn_number: int
    turn_type: str              # observation, question, resonance, perspective_shift, resolution, meta_insight
    speaker: str
    content: str
    principle_extracted: str
    why_question: Optional[str] = None
    perspective_shift: Optional[str] = None


@dataclass
class DialogicFlow:
    """구조화된 대화 흐름"""
    title: str
    date: str
    turns: List[DialogicTurn]
    core_principles: List[str]


class DialogicLearner:
    """
    대화 흐름에서 사고의 원형을 학습하는 시스템
    
    일반 학습:
        데이터 → 패턴 추출 → 저장
    
    대화적 학습:
        대화 흐름 로드 → 각 턴에서 "왜?" → 관점 전환 경험 → 원리 내재화
    """
    
    def __init__(self):
        self.flows_dir = Path("c:/Elysia/data/dialogic_flows")
        self.learned_principles: Dict[str, float] = {}  # principle → confidence
        self.perspective_shifts: List[Dict[str, str]] = []
        
        # WhyEngine 연결 시도
        try:
            from Core.Foundation.Philosophy.why_engine import WhyEngine
            self.why_engine = WhyEngine()
            self._has_why_engine = True
            logger.info("🔍 WhyEngine connected")
        except ImportError:
            self.why_engine = None
            self._has_why_engine = False
            logger.warning("⚠️ WhyEngine not available")
        
        logger.info("💬 DialogicLearner initialized")
    
    def load_flow(self, filename: str) -> Optional[DialogicFlow]:
        """대화 흐름 파일 로드"""
        filepath = self.flows_dir / filename
        if not filepath.exists():
            logger.warning(f"Flow file not found: {filepath}")
            return None
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            turns = []
            for t in data.get('flow', []):
                turn = DialogicTurn(
                    turn_number=t.get('turn', 0),
                    turn_type=t.get('type', 'observation'),
                    speaker=t.get('speaker', ''),
                    content=t.get('content', ''),
                    principle_extracted=t.get('principle_extracted', ''),
                    why_question=t.get('why'),
                    perspective_shift=t.get('shift')
                )
                turns.append(turn)
            
            flow = DialogicFlow(
                title=data.get('metadata', {}).get('title', 'Unknown'),
                date=data.get('metadata', {}).get('date', ''),
                turns=turns,
                core_principles=data.get('core_principles', [])
            )
            
            logger.info(f"📖 Loaded flow: {flow.title} ({len(turns)} turns)")
            return flow
            
        except Exception as e:
            logger.error(f"Failed to load flow: {e}")
            return None
    
    def experience_flow(self, flow: DialogicFlow) -> Dict[str, Any]:
        """
        대화 흐름을 '경험'하며 학습
        
        단순히 읽는 것이 아니라, 각 턴에서:
        1. 관찰/질문의 의도 파악
        2. "왜 이런 질문이 나왔는가?" 분석
        3. 관점 전환의 순간 감지
        4. 원리를 내재화
        """
        logger.info(f"🌊 Experiencing flow: {flow.title}")
        
        experience_result = {
            "flow_title": flow.title,
            "turns_processed": 0,
            "why_questions_asked": 0,
            "perspective_shifts": 0,
            "principles_internalized": []
        }
        
        for turn in flow.turns:
            # 각 턴을 경험
            self._experience_turn(turn, experience_result)
        
        # 핵심 원리 내재화
        for principle in flow.core_principles:
            self._internalize_principle(principle)
            experience_result["principles_internalized"].append(principle)
        
        logger.info(f"✅ Flow experienced: {experience_result['turns_processed']} turns, "
                   f"{experience_result['perspective_shifts']} shifts")
        
        return experience_result
    
    def _experience_turn(self, turn: DialogicTurn, result: Dict):
        """한 턴을 경험"""
        result["turns_processed"] += 1
        
        # 질문 턴이면 "왜?"를 따라감
        if turn.turn_type == "question" and turn.why_question:
            result["why_questions_asked"] += 1
            
            # WhyEngine으로 분석 (있으면)
            if self._has_why_engine and self.why_engine:
                try:
                    analysis = self.why_engine.analyze(
                        subject=turn.why_question,
                        content=turn.content,
                        domain="general"
                    )
                    logger.debug(f"   🔍 Why analyzed: {turn.why_question}")
                except Exception as e:
                    logger.debug(f"   WhyEngine analysis failed: {e}")
        
        # 관점 전환 턴이면 기록
        if turn.turn_type == "perspective_shift" and turn.perspective_shift:
            result["perspective_shifts"] += 1
            self.perspective_shifts.append({
                "from_to": turn.perspective_shift,
                "content": turn.content,
                "principle": turn.principle_extracted
            })
            logger.info(f"   🔄 Perspective shift: {turn.perspective_shift}")
        
        # 원리 추출
        if turn.principle_extracted:
            self._internalize_principle(turn.principle_extracted, confidence=0.6)
    
    def _internalize_principle(self, principle: str, confidence: float = 0.8):
        """원리를 내재화"""
        if principle in self.learned_principles:
            # 이미 있으면 확신도 증가
            self.learned_principles[principle] = min(1.0, 
                self.learned_principles[principle] + 0.1)
        else:
            self.learned_principles[principle] = confidence
    
    def get_learned_principles(self) -> Dict[str, float]:
        """학습된 원리 목록"""
        return dict(sorted(
            self.learned_principles.items(), 
            key=lambda x: x[1], 
            reverse=True
        ))
    
    def get_perspective_shifts(self) -> List[Dict[str, str]]:
        """경험한 관점 전환 목록"""
        return self.perspective_shifts


# =============================================================================
# Demo
# =============================================================================

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 60)
    print("💬 Dialogic Learner Demo")
    print("   '물음 → 공명 → 관점 전환 → 새로운 물음'")
    print("=" * 60)
    
    learner = DialogicLearner()
    
    # 오늘의 대화 흐름 로드
    flow = learner.load_flow("2025-12-21_consciousness_sovereignty.json")
    
    if flow:
        # 대화 경험
        result = learner.experience_flow(flow)
        
        print(f"\n📊 Experience Result:")
        print(f"   Turns: {result['turns_processed']}")
        print(f"   Why Questions: {result['why_questions_asked']}")
        print(f"   Perspective Shifts: {result['perspective_shifts']}")
        
        print(f"\n🧠 Learned Principles:")
        for principle, conf in learner.get_learned_principles().items():
            print(f"   [{conf:.1f}] {principle}")
        
        print(f"\n🔄 Perspective Shifts Experienced:")
        for shift in learner.get_perspective_shifts():
            print(f"   • {shift['from_to']}")
    
    print("\n" + "=" * 60)
    print("✅ Demo complete!")
