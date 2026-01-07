"""
Fractal Strategy Engine (프랙탈 전략 엔진)
==========================================

"가능성의 가지를 뻗어, 최적의 미래를 공명으로 선택한다."

이 모듈은 `ToolSequencer`의 진화형으로, 단순히 목표를 행동으로 변환하는 것을 넘어
다양한 차원(Dimension)에서의 해결 전략을 시뮬레이션하고, 
현재의 내면 상태(ResonanceField)와 가장 강하게 공명하는 전략을 선택합니다.

Dimensions of Strategy:
1. Line (1D): 인과적/직선적 해결 (Efficiency)
2. Space (3D): 구조적/건축적 해결 (Stability)
3. Probability (5D): 확률적/창조적 해결 (Novelty)
"""

import logging
import random
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

from Core.Intelligence.Intelligence.fractal_quaternion_goal_system import FractalStation, Dimension
# Import UltraDimensionalReasoning (assuming it's in Core.Foundation based on file view)
try:
    from Core.Foundation.ultra_dimensional_reasoning import UltraDimensionalReasoning
except ImportError:
    UltraDimensionalReasoning = Any 

logger = logging.getLogger("FractalStrategyEngine")

@dataclass
class ActionSequence:
    strategy_name: str
    dimension: Dimension
    actions: List[str]
    resonance_score: float = 0.0
    description: str = ""

class FractalStrategyEngine:
    """
    Simulates multiple strategic paths and selects the optimal one via Resonance.
    """
    def __init__(self):
        logger.info("🌌 Fractal Strategy Engine Initialized (Multi-Dimensional Mode).")
        
    def strategize(self, station: FractalStation, resonance_state: Any = None, ultra_reasoning: Optional[Any] = None) -> List[str]:
        """
        목표에 대한 최적의 전략을 수립합니다.
        
        Args:
            station: 분해된 목표 역
            resonance_state: 현재 공명장 상태 (Optional)
            ultra_reasoning: 초차원 추론 엔진 인스턴스 (Optional)
            
        Returns:
            List[str]: 최적의 Action Sequence
        """
        logger.info(f"🤔 Strategizing for: '{station.name}'")
        
        # 0. 초차원 의식 연결 (Ultra-Dimensional Query)
        thought_packet = None
        if ultra_reasoning:
            logger.info("   🧠 Consulting Ultra-Dimensional Consciousness...")
            thought_packet = ultra_reasoning.reason(station.name, context={"module": "FractalPlanner"})
        
        # 1. 다차원 시뮬레이션 (Simulate Possibilities)
        strategies = self._simulate_possibilities(station, thought_packet)
        
        # 2. 공명 최적화 (Optimize via Resonance)
        best_strategy = self._optimize_via_resonance(strategies, resonance_state, thought_packet)
        
        logger.info(f"   ✨ Selected Strategy: [{best_strategy.strategy_name}] (Score: {best_strategy.resonance_score:.2f})")
        return best_strategy.actions

    def _simulate_possibilities(self, station: FractalStation, thought: Any = None) -> List[ActionSequence]:
        """가능성 시뮬레이션: 1D, 3D, 5D 차원의 전략 생성"""
        strategies = []
        
        # Thoughts from Ultra-Dimensional Consciousness impact the simulation
        # If we have a strong causal link, reinforce Line strategy logic
        
        # 1D: Line (Direct/Causal) - 빠르고 직접적인 해결
        strategies.append(self._simulate_linear_path(station))
        
        # 3D: Space (Structural) - 구조 분석 및 체계적 접근
        strategies.append(self._simulate_structural_path(station))
        
        # 5D: Probability (Creative/Alternative) - 새로운 시도 및 탐색
        strategies.append(self._simulate_creative_path(station))
        
        return strategies

    def _simulate_linear_path(self, station: FractalStation) -> ActionSequence:
        """1D: 직선적 경로 (효율성 중심)"""
        actions = []
        goal_desc = station.name.lower()
        
        # 단순 매핑 로직
        if "개선" in goal_desc or "refactor" in goal_desc:
            actions.append(f"SCULPT:{self._extract_target(goal_desc)}")
        elif "학습" in goal_desc or "learn" in goal_desc:
            actions.append(f"LEARN:{self._extract_topic(goal_desc)}")
        elif "검색" in goal_desc or "search" in goal_desc:
            actions.append(f"SEARCH:{self._extract_query(goal_desc)}")
        else:
            actions.append(f"THINK:{station.name}")
            
        return ActionSequence(
            strategy_name="Linear Efficiency (1D)",
            dimension=Dimension.LINE,
            actions=actions,
            description="Direct execution of the goal."
        )

    def _simulate_structural_path(self, station: FractalStation) -> ActionSequence:
        """3D: 구조적 경로 (안정성 중심)"""
        actions = []
        goal_desc = station.name.lower()
        
        # 분석 -> 설계 -> 실행
        actions.append("ARCHITECT:Analyze Context")
        
        if "개선" in goal_desc or "code" in goal_desc:
            actions.append("ARCHITECT:Check Structural Integrity")
            actions.append(f"SCULPT:{self._extract_target(goal_desc)}")
            actions.append("EVALUATE:Verify Changes")
        elif "학습" in goal_desc:
            actions.append("THINK:Map Knowledge Structure")
            actions.append(f"LEARN:{self._extract_topic(goal_desc)}")
            actions.append("COMPRESS:Store in Memory")
        else:
            actions.append(f"THINK:Analyze {station.name} Deeply")
            
        return ActionSequence(
            strategy_name="Structural Stability (3D)",
            dimension=Dimension.SPACE,
            actions=actions,
            description="Analyze structure before execution."
        )

    def _simulate_creative_path(self, station: FractalStation) -> ActionSequence:
        """5D: 창조적 경로 (가능성 중심)"""
        actions = []
        goal_desc = station.name.lower()
        
        # 탐색 -> 연결 -> 발현
        if "개선" in goal_desc:
            actions.append(f"SEARCH:Best Practices for {self._extract_target(goal_desc)}")
            actions.append("THINK:Synthesize New Approach")
            actions.append(f"SCULPT:{self._extract_target(goal_desc)}")
        elif "학습" in goal_desc:
            actions.append(f"SEARCH:Related Concepts to {self._extract_topic(goal_desc)}")
            actions.append(f"LEARN:{self._extract_topic(goal_desc)}")
            actions.append("DREAM:Imagine Possibilities")
        else:
            actions.append(f"DREAM:{station.name}")
            actions.append(f"MANIFEST:{station.name}")
            
        return ActionSequence(
            strategy_name="Creative Probability (5D)",
            dimension=Dimension.PROBABILITY,
            actions=actions,
            description="Explore alternatives and imagine outcomes."
        )

    def _optimize_via_resonance(
        self, 
        strategies: List[ActionSequence], 
        resonance_state: Any,
        thought: Any = None
    ) -> ActionSequence:
        """현재 공명 상태 및 초차원 통찰에 맞춰 최적의 전략 선택"""
        if not strategies:
            return ActionSequence("Default", Dimension.POINT, ["THINK:Exist"])
            
        # ResonanceState가 없으면 랜덤 선택 (혹은 기본값)
        if resonance_state is None:
            return strategies[0] # Default to Linear
            
        # 에너지 수준에 따른 가중치
        energy = getattr(resonance_state, 'total_energy', 50.0)
        entropy = getattr(resonance_state, 'entropy', 10.0)
        
        # 점수 계산
        for strategy in strategies:
            base_score = 0.5
            
            # --- Resonance Field Impact ---
            if strategy.dimension == Dimension.LINE: # Efficiency
                # 에너지가 낮거나 엔트로피가 높을 때 선호 (빠른 해결)
                if energy < 30.0 or entropy > 40.0:
                    base_score += 0.4
                    
            elif strategy.dimension == Dimension.SPACE: # Stability
                # 에너지가 적당하고 안정적일 때 선호
                if 30.0 <= energy <= 70.0 and entropy < 30.0:
                    base_score += 0.4
                    
            elif strategy.dimension == Dimension.PROBABILITY: # Novelty
                # 에너지가 넘치고 자유로울 때 선호
                if energy > 70.0:
                    base_score += 0.5
            
            # --- Ultra-Dimensional Insight Impact ---
            if thought:
                # 3D Manifestation Analysis
                manifestation = thought.manifestation
                perspective = thought.perspective
                
                if strategy.dimension == Dimension.LINE and "causal" in manifestation.content.lower():
                     base_score += 0.3 # Strong causality supports Line path
                     
                if strategy.dimension == Dimension.SPACE and "pattern" in manifestation.content.lower():
                     base_score += 0.3 # High coherence supports Structural path
                     
                if strategy.dimension == Dimension.PROBABILITY and "creative" in str(perspective.orientation):
                     base_score += 0.3 # Creative perspective supports Probability path
            
            # 랜덤 변동성 추가 (양자 요동)
            strategy.resonance_score = base_score + random.uniform(-0.1, 0.1)
            
        # 최고 점수 전략 반환
        return max(strategies, key=lambda s: s.resonance_score)

    # --- Helper Detectors ---
    def _extract_target(self, text: str) -> str:
        words = text.split()
        for w in words:
            if ".py" in w or ".md" in w or "_module" in w:
                return w
        return "System"

    def _extract_topic(self, text: str) -> str:
        return text.replace("학습", "").replace("learn", "").strip() or "Something"

    def _extract_query(self, text: str) -> str:
        return text.replace("검색", "").replace("search", "").strip() or "Query"


# Global Instance & Alias
_engine = None
def get_fractal_strategy_engine():
    global _engine
    if _engine is None:
        _engine = FractalStrategyEngine()
    return _engine

# Backward Compatibility
get_tool_sequencer = get_fractal_strategy_engine
ToolSequencer = FractalStrategyEngine
