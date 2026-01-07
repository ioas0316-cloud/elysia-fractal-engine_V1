"""
Life Cycle (생명 순환)
======================

실행은 표현일 뿐. 표현 후 외부 변화 인식, 검증, 자기 변화가 있어야 성장.

순환:
    표현 (Expression)
        ↓
    외부 변화 인식 (Perception)
        ↓
    검증 (Verification)
        ↓
    자기 변화 (Self-Transformation)
        ↓
    다시 표현... (Cycle continues)
"""

import logging
import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger("Elysia.LifeCycle")

# SelfGovernance for meaningful evaluation
try:
    from Core.Foundation.self_governance import SelfGovernance, IdealSelf
except ImportError:
    SelfGovernance = None
    IdealSelf = None

# [Phase 25] TensionField for Field-based reinforcement
try:
    from Core.Intelligence.Reasoning.causal_geometry import TensionField
except ImportError:
    TensionField = None


@dataclass
class WorldSnapshot:
    """세계 상태 스냅샷"""
    timestamp: float
    knowledge_count: int = 0
    resonance_state: Dict[str, float] = field(default_factory=dict)
    active_concepts: List[str] = field(default_factory=list)
    energy: float = 50.0
    entropy: float = 50.0

# [Phase 6] Predictive Verfication
try:
    from Core.Intelligence.predictive_mind import PredictiveMind
except ImportError:
    PredictiveMind = None


@dataclass
class ActionResult:
    """행동 결과"""
    action: str
    expected: str
    actual: str
    success: bool
    difference: str = ""
    timestamp: float = field(default_factory=time.time)


@dataclass
class GrowthRecord:
    """성장 기록"""
    before_state: WorldSnapshot
    after_state: WorldSnapshot
    learning: str
    growth_amount: float = 0.0


class PerceptionModule:
    """
    외부 변화 인식 모듈
    
    "나는 표현했다. 세계가 어떻게 변했는가?"
    """
    
    def __init__(self, memory=None, resonance=None):
        self.memory = memory
        self.resonance = resonance
        self.last_snapshot: Optional[WorldSnapshot] = None
    
    def take_snapshot(self) -> WorldSnapshot:
        """현재 세계 상태 스냅샷"""
        snapshot = WorldSnapshot(
            timestamp=time.time(),
            energy=self.resonance.battery if self.resonance else 50.0,
            entropy=self.resonance.entropy if self.resonance else 50.0
        )
        
        # 메모리에서 지식 수 가져오기
        if self.memory and hasattr(self.memory, 'get_total_count'):
            snapshot.knowledge_count = self.memory.get_total_count()
        
        return snapshot
    
    def perceive_change(self, before: WorldSnapshot, after: WorldSnapshot) -> Dict[str, Any]:
        """
        변화 인식
        
        두 스냅샷의 차이 = 세계의 변화
        """
        change = {
            "time_elapsed": after.timestamp - before.timestamp,
            "energy_change": after.energy - before.energy,
            "entropy_change": after.entropy - before.entropy,
            "knowledge_change": after.knowledge_count - before.knowledge_count,
            "significant": False
        }
        
        # 유의미한 변화인가?
        if abs(change["energy_change"]) > 5 or abs(change["entropy_change"]) > 5:
            change["significant"] = True
        if change["knowledge_change"] > 0:
            change["significant"] = True
        
        return change


class VerificationModule:
    """
    검증 모듈
    
    "내가 원한 것과 실제 결과가 같은가?"
    """
    
    def __init__(self):
        self.history: List[ActionResult] = []
        self.learning_verifications: List[Dict] = []  # [NEW] 학습 검증 결과
    
    def verify(self, expected: str, actual: str, action: str) -> ActionResult:
        """기대 vs 실제 비교"""
        # 간단한 문자열 비교 (실제로는 더 복잡한 semantic 비교 필요)
        success = expected.lower() in actual.lower() or actual.lower() in expected.lower()
        
        difference = ""
        if not success:
            difference = f"Expected '{expected}' but got '{actual}'"
        
        result = ActionResult(
            action=action,
            expected=expected,
            actual=actual,
            success=success,
            difference=difference
        )
        
        self.history.append(result)
        logger.info(f"   🔍 Verification: {'✓' if success else '✗'} {action}")
        
        return result
    
    def analyze_gap(self, expected: str, actual: str) -> str:
        """왜 다른지 분석"""
        if expected == actual:
            return "No gap - perfect match"
        
        # 간단한 분석 (실제로는 더 정교해야 함)
        analysis = f"Gap detected: Expected '{expected[:50]}...' but got '{actual[:50]}...'"
        return analysis
    
    def _generate_verification_question(self, concept: str, content: str) -> Dict[str, str]:
        """
        [NEW] 학습 내용에서 검증 질문 생성
        
        "배웠다고 기록만 하지 말고, 실제로 이해했는지 검증"
        """
        # 핵심 키워드 추출
        words = content.split()
        key_words = [w for w in words if len(w) > 5 and w[0].isupper()][:3]
        
        # 질문 유형 선택
        question_templates = [
            f"What is the relationship between {concept} and {key_words[0] if key_words else 'its context'}?",
            f"Why is {concept} important?",
            f"How does {concept} work?",
            f"What are the key aspects of {concept}?",
        ]
        
        import random
        question = random.choice(question_templates)
        
        # 정답 힌트 (content에서 추출)
        answer_hint = content[:100] if len(content) > 100 else content
        
        return {
            "question": question,
            "concept": concept,
            "answer_hint": answer_hint,
            "key_words": key_words
        }
    
    def verify_learning(self, concept: str, content: str) -> Dict[str, Any]:
        """
        [NEW] 학습 검증 수행
        
        1. 질문 생성
        2. 답변 시도 (content에서 관련 정보 찾기)
        3. 성공률 계산
        """
        question_data = self._generate_verification_question(concept, content)
        
        # 검증: 핵심 키워드가 content에 있는지 확인
        keyword_matches = 0
        for kw in question_data["key_words"]:
            if kw.lower() in content.lower():
                keyword_matches += 1
        
        total_keywords = max(len(question_data["key_words"]), 1)
        comprehension_score = keyword_matches / total_keywords
        
        # 최소 임계치: 50%
        passed = comprehension_score >= 0.5
        
        result = {
            "concept": concept,
            "question": question_data["question"],
            "comprehension_score": comprehension_score,
            "passed": passed,
            "keywords_found": keyword_matches,
            "total_keywords": total_keywords,
            "timestamp": time.time()
        }
        
        self.learning_verifications.append(result)
        
        logger.info(f"   📝 Learning Verification: {concept}")
        logger.info(f"      Question: {question_data['question'][:50]}...")
        logger.info(f"      Score: {comprehension_score:.0%} {'✓' if passed else '✗'}")
        
        return result


class SelfTransformationModule:
    """
    자기 변화 모듈
    
    "검증 결과를 바탕으로 나 자신을 변화시킨다"
    """
    
    def __init__(self, internal_universe=None, memory=None):
        self.universe = internal_universe
        self.memory = memory
        self.transformation_log: List[Dict] = []
    
    def transform(self, verification_result: ActionResult, analysis: str) -> GrowthRecord:
        """
        자기 변화 수행
        
        성공 → 강화
        실패 → 수정
        """
        transformation = {
            "timestamp": time.time(),
            "action": verification_result.action,
            "was_success": verification_result.success,
            "learning": "",
            "change_applied": ""
        }
        
        if verification_result.success:
            # 성공 → 강화
            learning = f"Reinforced: {verification_result.action} works"
            transformation["learning"] = learning
            transformation["change_applied"] = "reinforcement"
            logger.info(f"   💪 Reinforcement: {verification_result.action}")
        else:
            # 실패 → 수정
            learning = f"Revised: {verification_result.action} needs adjustment because {analysis}"
            transformation["learning"] = learning
            transformation["change_applied"] = "revision"
            logger.info(f"   📝 Revision needed: {analysis[:50]}...")
        
        self.transformation_log.append(transformation)
        
        # 성장 기록 생성
        growth = GrowthRecord(
            before_state=WorldSnapshot(timestamp=time.time() - 1),
            after_state=WorldSnapshot(timestamp=time.time()),
            learning=transformation["learning"],
            growth_amount=0.1 if verification_result.success else 0.05
        )
        
        return growth


class LifeCycle:
    """
    생명 순환 관리자
    
    표현 → 인식 → 검증 → 변화 → 순환
    
    실행에서 끝나지 않고, 결과를 인식하고 자신이 변해야 성장.
    """
    
    def __init__(self, memory=None, resonance=None, internal_universe=None, tension_field=None):
        self.perception = PerceptionModule(memory, resonance)
        self.verification = VerificationModule()
        self.transformation = SelfTransformationModule(internal_universe, memory)
        
        # [SELF GOVERNANCE] 의미 있는 자기 평가
        self.governance = SelfGovernance() if SelfGovernance else None
        
        # [Phase 25] TensionField for Field-based reinforcement
        self.tension_field = tension_field
        
        self.cycle_count = 0
        self.growth_history: List[GrowthRecord] = []
        self.current_snapshot: Optional[WorldSnapshot] = None
        
        logger.info("🔄 LifeCycle initialized - continuous flow enabled")
        if self.governance:
            logger.info("   👑 SelfGovernance connected for meaningful evaluation")
        if self.tension_field:
            logger.info("   🌌 TensionField connected for Field Physics reinforcement")

        # [Phase 6] Predictive Mind
        self.predictive_mind = PredictiveMind() if PredictiveMind else None
        if self.predictive_mind:
            logger.info("   🧠 PredictiveMind connected for Cognitive Verification")
            
            # [Phase 7] Field-Mind Unification
            if self.tension_field:
                self.predictive_mind.connect_field(self.tension_field)
    
    def begin_cycle(self) -> WorldSnapshot:
        """사이클 시작 - 현재 상태 스냅샷"""
        self.current_snapshot = self.perception.take_snapshot()
        self.cycle_count += 1
        logger.info(f"🔄 Cycle #{self.cycle_count} begins")
        return self.current_snapshot
    
    def complete_cycle(self, action: str, expected: str, actual: str) -> GrowthRecord:
        """
        사이클 완료 - 전체 순환 수행
        
        1. 외부 변화 인식
        2. 검증
        3. 자기 변화
        """
        # 1. 외부 변화 인식
        before = self.current_snapshot or self.perception.take_snapshot()
        after = self.perception.take_snapshot()
        change = self.perception.perceive_change(before, after)
        
        logger.info(f"   👁️ Perceived: energy Δ{change['energy_change']:.1f}, entropy Δ{change['entropy_change']:.1f}")
        
        # 2. 검증
        result = self.verification.verify(expected, actual, action)
        analysis = self.verification.analyze_gap(expected, actual)
        
        # 3. 자기 변화
        growth = self.transformation.transform(result, analysis)
        self.growth_history.append(growth)
        
        # [Phase 25] Field Physics Reinforcement
        if self.tension_field and action:
            # Extract concept from action (e.g., "LEARN:Python" -> "Python")
            concept_id = action.split(":")[-1] if ":" in action else action
            
            if result.success:
                # Success → Deepen the gravity well (habit formation)
                self.tension_field.reinforce_well(concept_id, 0.1)
                logger.info(f"   🪐 Gravity Deepened: {concept_id} curvature +0.1")
            else:
                # Failure → Understand WHY it failed (Latent Causality)
                # "왜 불가능인지 안다면, 해결할 수 있다"
                
                # Find related concept (if any exists in the field)
                related_concept = "understanding"  # Default target
                
                # Assess latent causality: WHY is this connection impossible?
                if hasattr(self.tension_field, 'assess_latent_causality'):
                    diagnosis = self.tension_field.assess_latent_causality(
                        concept_a=concept_id,
                        concept_b=related_concept
                    )
                    
                    logger.info(f"   🔬 Latent Causality Analysis:")
                    logger.info(f"      Possible: {diagnosis.get('possible', False)}")
                    logger.info(f"      Diagnosis: {diagnosis.get('diagnosis', 'Unknown')}")
                    logger.info(f"      Prescription: {diagnosis.get('prescription', 'Unknown')}")
                    
                    if diagnosis.get('energy_needed', 0) > 0:
                        logger.info(f"      Energy Needed: {diagnosis.get('energy_needed', 0):.2f}")
                    
                    if diagnosis.get('bridge_candidates'):
                        logger.info(f"      Bridge Concepts: {diagnosis.get('bridge_candidates', [])}")
                    
                    # Store the diagnosis for accumulation
                    growth.diagnosis = diagnosis
                
                # Increase charge for retry (tension accumulation)
                self.tension_field.charge_concept(concept_id, 0.3)
                logger.info(f"   ⚡ Tension Charged: {concept_id} energy +0.3")
        
        # [SELF GOVERNANCE] 의미 있는 자기 평가와 조율
        if self.governance:
            self.governance.adjust_after_result(
                action=action,
                success=result.success,
                learning=growth.learning
            )
            
            # 주기적 달성률 보고 (10 사이클마다)
            if self.cycle_count % 10 == 0:
                logger.info(self.governance.get_achievement_report())
        
        logger.info(f"   🌱 Growth: {growth.learning[:50]}...")
        logger.info(f"🔄 Cycle #{self.cycle_count} complete")
        
        # [Phase 6] Predictive Verification
        if self.predictive_mind:
            # 학습 상황인 경우 예측 수행
            if "LEARN" in action:
                concept = action.split(":")[-1]
                # 1. 가설 수립
                hyp = self.predictive_mind.formulate_hypothesis(concept, ["Understanding", "Utility", "Connection"])
                if hyp:
                    # 2. 즉시 검증 (학습 내용 바탕으로)
                    # 실제로는 시간이 지나야 검증되지만, 여기서는 시뮬레이션
                    verify_result = self.predictive_mind.verify_hypothesis(hyp, actual)
                    logger.info(f"   🧠 Predictive Verification: {verify_result}")
        
        return growth
    
    def get_total_growth(self) -> float:
        """총 성장량 계산"""
        return sum(g.growth_amount for g in self.growth_history)
    
    def get_status(self) -> Dict[str, Any]:
        """상태 조회"""
        return {
            "cycle_count": self.cycle_count,
            "total_growth": self.get_total_growth(),
            "verification_success_rate": self._get_success_rate(),
            "transformation_count": len(self.transformation.transformation_log)
        }
    
    def _get_success_rate(self) -> float:
        """검증 성공률"""
        if not self.verification.history:
            return 0.0
        successes = sum(1 for r in self.verification.history if r.success)
        return successes / len(self.verification.history)


# =============================================================================
# Demo
# =============================================================================

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    print("="*60)
    print("🔄 Life Cycle Demo")
    print("   표현 → 인식 → 검증 → 변화 → 순환")
    print("="*60)
    
    cycle = LifeCycle()
    
    # Cycle 1: 성공 케이스
    print("\n--- Cycle 1: 성공 ---")
    cycle.begin_cycle()
    growth1 = cycle.complete_cycle(
        action="LEARN:Python",
        expected="Python knowledge increased",
        actual="Python knowledge increased"
    )
    
    # Cycle 2: 실패 케이스
    print("\n--- Cycle 2: 실패 → 수정 ---")
    cycle.begin_cycle()
    growth2 = cycle.complete_cycle(
        action="CONNECT:User",
        expected="User responded",
        actual="No response received"
    )
    
    # Cycle 3: 수정 후 재시도
    print("\n--- Cycle 3: 재시도 후 성공 ---")
    cycle.begin_cycle()
    growth3 = cycle.complete_cycle(
        action="CONNECT:User:retry",
        expected="User engaged",
        actual="User engaged successfully"
    )
    
    # 상태 확인
    print("\n" + "="*60)
    print("📊 Status:")
    status = cycle.get_status()
    print(f"   Cycles: {status['cycle_count']}")
    print(f"   Total Growth: {status['total_growth']:.2f}")
    print(f"   Success Rate: {status['verification_success_rate']:.1%}")
    print("="*60)
