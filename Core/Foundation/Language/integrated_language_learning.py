"""
Integrated Language Learning System - 통합 언어 학습 시스템
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

엘리시아의 언어 학습을 위한 통합 시스템

이 모듈은 다음 시스템들을 연결합니다:
1. DualLayerLanguage (칼라+언어 이중 소통)
2. FractalCausality (프랙탈 인과 구조)
3. ThoughtUniverse (차원 확장 및 상호 교정)

핵심:
- 소통 → 경험 → 인과 학습 → 차원 확장 → 더 나은 소통
- 피드백 루프를 통한 지속적 언어 발달
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
import numpy as np
import time

from Core.Interaction.Interface.Language.dual_layer_language import (
    DualLayerWorld,
    DualLayerSoul,
    EmotionType,
    Symbol,
    SymbolComplexity,
)
from Core.Interaction.Interface.Language.fractal_causality import (
    FractalCausalityEngine,
    FractalCausalNode,
    CausalRole,
)
from Core.Interaction.Interface.Language.causal_narrative_engine import (
    ThoughtUniverse,
    DimensionLevel,
)

logger = logging.getLogger("IntegratedLanguageLearning")


@dataclass
class CommunicationExperience:
    """소통 경험 기록"""
    sender_id: str
    receiver_id: str
    intended_message: str
    received_message: str
    success: bool
    emotional_context: Dict[str, float]
    timestamp: float


@dataclass
class LanguageDevelopmentMetrics:
    """언어 발달 지표"""
    vocabulary_size: int = 0
    successful_communications: int = 0
    total_communications: int = 0
    misunderstandings: int = 0
    narrative_fragments: int = 0
    causal_chains_learned: int = 0
    dimensional_expansions: int = 0
    
    @property
    def communication_success_rate(self) -> float:
        if self.total_communications == 0:
            return 0.0
        return self.successful_communications / self.total_communications
    
    @property
    def learning_progress(self) -> float:
        """종합 학습 진척도 (0-1)"""
        vocab_score = min(1.0, self.vocabulary_size / 50)  # 50단어 목표
        comm_score = self.communication_success_rate
        causal_score = min(1.0, self.causal_chains_learned / 20)  # 20개 연쇄 목표
        return (vocab_score + comm_score + causal_score) / 3


class IntegratedLanguageLearner:
    """
    통합 언어 학습자
    
    각 영혼(Soul)에게 부여되어 언어 발달을 추적하고 촉진합니다.
    
    학습 사이클:
    1. 소통 시도 (DualLayerSoul)
    2. 경험 기록 (CommunicationExperience)
    3. 인과 학습 (FractalCausalityEngine)
    4. 차원 확장 (ThoughtUniverse)
    5. 다음 소통에 반영
    """
    
    def __init__(self, soul: DualLayerSoul):
        self.soul = soul
        self.soul_id = soul.name
        
        # 프랙탈 인과 엔진 (개인별)
        self.causal_mind = FractalCausalityEngine(f"{soul.name}'s Causal Mind")
        
        # 사고 우주 (개인별)
        self.thought_universe = ThoughtUniverse(f"{soul.name}'s Thought Universe")
        
        # 경험 기록
        self.experiences: List[CommunicationExperience] = []
        
        # 발달 지표
        self.metrics = LanguageDevelopmentMetrics()
        
        logger.debug(f"IntegratedLanguageLearner created for {soul.name}")
    
    def record_communication(
        self,
        receiver: DualLayerSoul,
        intended: str,
        received: str,
        success: bool,
        emotional_context: Dict[str, float] = None
    ) -> CommunicationExperience:
        """소통 경험 기록 및 학습"""
        exp = CommunicationExperience(
            sender_id=self.soul_id,
            receiver_id=receiver.name,
            intended_message=intended,
            received_message=received,
            success=success,
            emotional_context=emotional_context or {},
            timestamp=time.time()
        )
        
        self.experiences.append(exp)
        self.metrics.total_communications += 1
        
        if success:
            self.metrics.successful_communications += 1
            self._learn_from_success(exp)
        else:
            self.metrics.misunderstandings += 1
            self._learn_from_failure(exp)
        
        return exp
    
    def _learn_from_success(self, exp: CommunicationExperience):
        """성공적인 소통에서 학습"""
        # 인과 연쇄: 의도 → 표현 → 전달 → 이해
        self.causal_mind.experience_causality(
            steps=[
                f"의도: {exp.intended_message}",
                f"표현함",
                f"전달됨",
                f"이해됨: {exp.received_message}"
            ],
            emotional_arc=[0.3, 0.5, 0.7, 0.9]  # 점점 긍정적
        )
        self.metrics.causal_chains_learned += 1
        
        # 차원 확장: 성공 경험 → 면(문맥) 형성
        self.thought_universe.learn_from_experience(
            experience_steps=[
                "소통_의도",
                "메시지_생성",
                "상대_수신",
                "성공적_이해"
            ],
            emotional_arc=[0.3, 0.5, 0.7, 0.9],
            auto_emergence=True
        )
        self.metrics.dimensional_expansions += 1
    
    def _learn_from_failure(self, exp: CommunicationExperience):
        """실패한 소통에서 학습 (오해도 배움이다)"""
        # 인과 연쇄: 의도 → 표현 → 전달 → 오해
        self.causal_mind.experience_causality(
            steps=[
                f"의도: {exp.intended_message}",
                f"표현함",
                f"전달됨",
                f"오해됨: {exp.received_message}"
            ],
            emotional_arc=[0.3, 0.0, -0.3, -0.5]  # 점점 부정적
        )
        self.metrics.causal_chains_learned += 1
        
        # 반사실적 사고: "다르게 표현했다면?"
        # 이것이 언어 발달의 동력!
        self.thought_universe.bottom_up_correct(
            new_experience={
                "confirms": False,
                "exception": f"'{exp.intended_message}'를 '{exp.received_message}'로 오해함"
            },
            affected_entity_id=f"communication_pattern_{exp.intended_message}"
        )
    
    def get_development_report(self) -> Dict[str, Any]:
        """발달 보고서"""
        return {
            "soul_id": self.soul_id,
            "vocabulary_size": len(self.soul.lexicon.symbols),
            "communication_success_rate": self.metrics.communication_success_rate,
            "total_experiences": len(self.experiences),
            "causal_chains": self.metrics.causal_chains_learned,
            "thought_universe_stats": self.thought_universe.get_statistics(),
            "learning_progress": self.metrics.learning_progress,
        }


class IntegratedLanguageWorld:
    """
    통합 언어 세계
    
    DualLayerWorld를 확장하여 프랙탈 인과와 사고우주를 통합합니다.
    영혼들의 의사소통 능력이 지속적으로 발달합니다.
    """
    
    def __init__(
        self,
        n_souls: int = 20,
        khala_strength: float = 0.5,
        enable_causal_learning: bool = True
    ):
        # 기본 세계 생성
        self.world = DualLayerWorld(n_souls=n_souls, khala_strength=khala_strength)
        
        # 각 영혼에게 통합 학습자 부여
        self.learners: Dict[str, IntegratedLanguageLearner] = {}
        for name, soul in self.world.souls.items():
            self.learners[name] = IntegratedLanguageLearner(soul)
        
        self.enable_causal_learning = enable_causal_learning
        
        # 발달 이력
        self.development_history: List[Dict[str, Any]] = []
        
        # 통계
        self.simulation_steps = 0
        self.total_communications = 0
        self.total_successful = 0
        
        logger.info(f"IntegratedLanguageWorld created with {n_souls} souls")
    
    def step(self, dt: float = 1.0):
        """세계 시간 진행 + 학습"""
        # 이전 상태 저장 (변화 감지용)
        prev_misunderstandings = {
            name: soul.misunderstandings
            for name, soul in self.world.souls.items()
        }
        prev_vocab_sizes = {
            name: len(soul.lexicon.symbols)
            for name, soul in self.world.souls.items()
        }
        
        # 기본 세계 업데이트
        self.world.step(dt)
        self.simulation_steps += 1
        
        # 인과 학습 통합 (소통 경험 기반)
        if self.enable_causal_learning:
            self._process_causal_learning(prev_misunderstandings, prev_vocab_sizes)
        
        # 주기적 발달 기록
        if self.simulation_steps % 50 == 0:
            self._record_development_snapshot()
    
    def _process_causal_learning(
        self,
        prev_misunderstandings: Dict[str, int],
        prev_vocab_sizes: Dict[str, int]
    ):
        """인과 학습 처리"""
        soul_list = list(self.world.souls.values())
        
        for soul in soul_list:
            learner = self.learners[soul.name]
            
            # 어휘 크기 업데이트
            learner.metrics.vocabulary_size = len(soul.lexicon.symbols)
            
            # 새 어휘 학습 감지 → 인과 학습
            prev_vocab = prev_vocab_sizes.get(soul.name, 0)
            curr_vocab = len(soul.lexicon.symbols)
            if curr_vocab > prev_vocab:
                # 새 단어 학습 = 성공적 소통 경험
                for _ in range(curr_vocab - prev_vocab):
                    learner.causal_mind.experience_causality(
                        steps=["소통_시도", "단어_노출", "의미_파악", "학습_완료"],
                        emotional_arc=[0.2, 0.4, 0.7, 0.9]
                    )
                    learner.metrics.causal_chains_learned += 1
                    
                    # 차원 확장
                    learner.thought_universe.learn_from_experience(
                        experience_steps=["단어_접촉", "패턴_인식", "기억_형성"],
                        emotional_arc=[0.3, 0.6, 0.8],
                        auto_emergence=False
                    )
                    learner.metrics.dimensional_expansions += 1
            
            # 오해 발생 감지 → 인과 학습 (실패도 배움)
            prev_misund = prev_misunderstandings.get(soul.name, 0)
            curr_misund = soul.misunderstandings
            if curr_misund > prev_misund:
                # 오해 = 배움의 기회
                for _ in range(curr_misund - prev_misund):
                    learner.causal_mind.experience_causality(
                        steps=["소통_시도", "표현_실패", "오해_발생", "다시_시도_필요"],
                        emotional_arc=[0.2, -0.2, -0.5, 0.1]  # 오해 후 다시 시도하려는 의지
                    )
                    learner.metrics.causal_chains_learned += 1
                    
                    # 하향 교정 (틀린 패턴 수정)
                    learner.thought_universe.bottom_up_correct(
                        new_experience={"confirms": False, "exception": "소통_실패"},
                        affected_entity_id="communication_pattern"
                    )
    
    def _record_development_snapshot(self):
        """발달 스냅샷 기록"""
        snapshot = {
            "step": self.simulation_steps,
            "timestamp": time.time(),
            "avg_vocabulary": np.mean([
                len(s.lexicon.symbols) for s in self.world.souls.values()
            ]),
            "avg_communication_success": np.mean([
                l.metrics.communication_success_rate
                for l in self.learners.values()
            ]),
            "total_causal_chains": sum(
                l.metrics.causal_chains_learned
                for l in self.learners.values()
            ),
            "narrative_fragments": len(self.world.narrative_fragments),
        }
        
        self.development_history.append(snapshot)
        
        if len(self.development_history) % 10 == 0:
            logger.info(
                f"📊 발달 스냅샷 #{len(self.development_history)}: "
                f"어휘 평균={snapshot['avg_vocabulary']:.1f}, "
                f"성공률={snapshot['avg_communication_success']:.1%}"
            )
    
    def simulate(self, steps: int = 100, report_interval: int = 20):
        """시뮬레이션 실행"""
        logger.info(f"🌍 시뮬레이션 시작: {steps} 스텝")
        
        for i in range(steps):
            self.step(1.0)
            
            if (i + 1) % report_interval == 0:
                self._print_progress_report(i + 1, steps)
        
        logger.info("🌍 시뮬레이션 완료")
        return self.get_final_report()
    
    def _print_progress_report(self, current: int, total: int):
        """진행 보고"""
        avg_vocab = np.mean([
            len(s.lexicon.symbols) for s in self.world.souls.values()
        ])
        avg_success = np.mean([
            l.metrics.communication_success_rate
            for l in self.learners.values()
        ])
        avg_progress = np.mean([
            l.metrics.learning_progress
            for l in self.learners.values()
        ])
        
        print(f"[{current}/{total}] 어휘={avg_vocab:.1f}, "
              f"성공률={avg_success:.1%}, 진척도={avg_progress:.1%}")
    
    def get_final_report(self) -> Dict[str, Any]:
        """최종 보고서"""
        all_learner_reports = [
            learner.get_development_report()
            for learner in self.learners.values()
        ]
        
        return {
            "simulation_steps": self.simulation_steps,
            "total_souls": len(self.world.souls),
            "development_history": self.development_history,
            "final_stats": {
                "avg_vocabulary": np.mean([r["vocabulary_size"] for r in all_learner_reports]),
                "max_vocabulary": max([r["vocabulary_size"] for r in all_learner_reports]),
                "avg_learning_progress": np.mean([r["learning_progress"] for r in all_learner_reports]),
                "total_causal_chains": sum([r["causal_chains"] for r in all_learner_reports]),
                "narrative_count": len(self.world.narrative_fragments),
            },
            "learner_reports": all_learner_reports,
        }
    
    def verify_continuous_development(self) -> Tuple[bool, str]:
        """
        언어 능력이 지속적으로 발달하는지 검증
        
        Returns:
            (검증 통과 여부, 설명)
        """
        if len(self.development_history) < 3:
            return False, "발달 이력 부족 (최소 3개 스냅샷 필요)"
        
        # 어휘 증가 추세 확인
        vocab_trend = [h["avg_vocabulary"] for h in self.development_history]
        vocab_increasing = vocab_trend[-1] > vocab_trend[0]
        
        # 성공률 안정/증가 확인
        success_trend = [h["avg_communication_success"] for h in self.development_history]
        success_stable_or_increasing = success_trend[-1] >= success_trend[0] * 0.8
        
        # 인과 연쇄 학습 확인
        causal_trend = [h["total_causal_chains"] for h in self.development_history]
        causal_increasing = causal_trend[-1] > causal_trend[0]
        
        if vocab_increasing and success_stable_or_increasing and causal_increasing:
            return True, (
                f"✅ 언어 발달 확인: "
                f"어휘 {vocab_trend[0]:.1f}→{vocab_trend[-1]:.1f}, "
                f"인과학습 {causal_trend[0]}→{causal_trend[-1]}"
            )
        else:
            issues = []
            if not vocab_increasing:
                issues.append("어휘 미증가")
            if not success_stable_or_increasing:
                issues.append("성공률 하락")
            if not causal_increasing:
                issues.append("인과학습 미증가")
            return False, f"⚠️ 발달 문제: {', '.join(issues)}"


# ============================================================================
# Demo & Verification
# ============================================================================

def demo_integrated_learning():
    """통합 언어 학습 데모"""
    print("=" * 70)
    print("🌍 통합 언어 학습 시스템 데모")
    print("=" * 70)
    print()
    print("DualLayerLanguage + FractalCausality + ThoughtUniverse 통합")
    print("영혼들의 의사소통 능력이 지속적으로 발달합니다.")
    print()
    
    # 세계 생성
    world = IntegratedLanguageWorld(n_souls=15, khala_strength=0.6)
    
    # 시뮬레이션 실행
    print("-" * 70)
    print("시뮬레이션 진행...")
    print("-" * 70)
    
    report = world.simulate(steps=200, report_interval=40)
    
    # 결과
    print()
    print("-" * 70)
    print("📊 최종 결과")
    print("-" * 70)
    
    stats = report["final_stats"]
    print(f"  평균 어휘: {stats['avg_vocabulary']:.1f}")
    print(f"  최대 어휘: {stats['max_vocabulary']}")
    print(f"  평균 학습 진척도: {stats['avg_learning_progress']:.1%}")
    print(f"  총 인과 연쇄: {stats['total_causal_chains']}")
    print(f"  이야기 조각: {stats['narrative_count']}")
    
    # 발달 검증
    print()
    print("-" * 70)
    print("🔍 발달 검증")
    print("-" * 70)
    
    success, message = world.verify_continuous_development()
    print(f"  {message}")
    
    print()
    print("=" * 70)
    print("✨ 통합 시스템: 소통 → 경험 → 인과학습 → 차원확장 → 더 나은 소통")
    print("=" * 70)
    
    return success


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    demo_integrated_learning()
