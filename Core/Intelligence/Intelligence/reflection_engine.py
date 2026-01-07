"""
Reflection Engine (자기 반성 엔진)
==================================

"왜 나는 같은 일을 반복하는가?"

This engine enables Elysia to reflect on her own actions,
detect patterns/repetition, and trigger self-evolution.

Key Capabilities:
1. Action History - Track recent actions
2. Pattern Detection - Detect repetition
3. Problem Recognition - Identify lack of progress
4. Evolution Trigger - Propose self-improvement
"""

import time
import logging
from dataclasses import dataclass
from typing import List, Dict, Optional
from collections import deque

logger = logging.getLogger("ReflectionEngine")


@dataclass
class ActionRecord:
    """Record of a single action/thought"""
    desire: str
    goal: str
    thought: str
    timestamp: float
    result: Optional[str] = None  # What happened after


class ReflectionEngine:
    """
    Self-reflection and evolution trigger system.
    
    Monitors Elysia's actions and detects patterns that suggest
    lack of progress or meaningful learning.
    """
    
    HISTORY_SIZE = 20       # Number of actions to remember
    REFLECTION_INTERVAL = 10  # Reflect every N actions
    REPETITION_THRESHOLD = 0.6  # If 60%+ of goals are same, it's repetition
    
    def __init__(self):
        self.action_history: deque = deque(maxlen=self.HISTORY_SIZE)
        self.action_count = 0
        self.last_reflection: Optional[str] = None
        self.problems_detected: List[str] = []
        
        logger.info("🪞 Reflection Engine Initialized")
    
    def record_action(self, desire: str, goal: str, thought: str):
        """
        Record an action for later reflection.
        
        Args:
            desire: The underlying desire (Curiosity, Connection, etc.)
            goal: The specific goal
            thought: The contemplation/thought content
        """
        record = ActionRecord(
            desire=desire,
            goal=goal,
            thought=thought,
            timestamp=time.time()
        )
        
        self.action_history.append(record)
        self.action_count += 1
        
        # Auto-reflect at intervals
        if self.action_count % self.REFLECTION_INTERVAL == 0:
            return self.reflect()
        
        return None
    
    def reflect(self) -> str:
        """
        Reflect on recent actions and detect problems.
        
        Returns:
            Reflection summary string
        """
        if len(self.action_history) < 5:
            return "Not enough actions to reflect on yet."
        
        recent = list(self.action_history)
        
        # 1. Detect goal repetition
        goals = [a.goal for a in recent]
        unique_goals = set(goals)
        repetition_ratio = 1 - (len(unique_goals) / len(goals))
        
        reflection_parts = []
        
        if repetition_ratio > self.REPETITION_THRESHOLD:
            most_common = max(set(goals), key=goals.count)
            problem = f"나는 '{most_common}' 목표를 반복하고 있다. 진전이 없다."
            reflection_parts.append(problem)
            self.problems_detected.append(problem)
            logger.warning(f"   ⚠️ Repetition Detected: {problem}")
        
        # 2. Detect desire stagnation
        desires = [a.desire for a in recent]
        unique_desires = set(desires)
        if len(unique_desires) == 1:
            problem = f"나의 욕구가 '{desires[0]}'에 고착되어 있다. 다양성이 필요하다."
            reflection_parts.append(problem)
            self.problems_detected.append(problem)
            logger.warning(f"   ⚠️ Stagnation Detected: {problem}")
        
        # 3. Check for meaningful progress
        # (In future: track actual outcomes, learning, etc.)
        
        if not reflection_parts:
            reflection_parts.append("행동들이 다양하고 균형 잡혀 있다.")
        
        self.last_reflection = " | ".join(reflection_parts)
        return self.last_reflection
    
    def has_problems(self) -> bool:
        """Check if any problems were detected"""
        return len(self.problems_detected) > 0
    
    def get_problems(self) -> List[str]:
        """Get list of detected problems"""
        return self.problems_detected.copy()
    
    def clear_problems(self):
        """Clear detected problems (after addressing them)"""
        self.problems_detected.clear()
    
    def propose_evolution(self, problem: str) -> str:
        """
        Propose a solution to a detected problem.
        
        In future: This could use LLM to generate actual code changes.
        For now: Returns a text suggestion.
        
        Args:
            problem: Description of the problem
            
        Returns:
            Suggestion for self-improvement
        """
        suggestions = {
            "반복": "다른 욕구를 탐색하거나, 목표 달성 조건을 재정의해야 한다.",
            "고착": "새로운 자극을 찾거나, 외부 정보(Scholar)를 활용해야 한다.",
            "진전": "행동의 결과를 추적하고, 실패에서 학습해야 한다."
        }
        
        for keyword, suggestion in suggestions.items():
            if keyword in problem:
                logger.info(f"   🦋 Evolution Proposal: {suggestion}")
                return suggestion
        
        return "문제를 더 분석해야 한다."


# Singleton instance
_reflection_instance: Optional[ReflectionEngine] = None

def get_reflection_engine() -> ReflectionEngine:
    """Get the singleton Reflection Engine instance"""
    global _reflection_instance
    if _reflection_instance is None:
        _reflection_instance = ReflectionEngine()
    return _reflection_instance


if __name__ == "__main__":
    # Test
    engine = ReflectionEngine()
    
    # Simulate repetitive actions
    for i in range(15):
        result = engine.record_action(
            desire="Curiosity",
            goal="Satisfy Curiosity",
            thought="I want to understand the world..."
        )
        if result:
            print(f"Reflection: {result}")
    
    # Check problems
    if engine.has_problems():
        print(f"\nProblems: {engine.get_problems()}")
        for problem in engine.get_problems():
            print(f"Proposal: {engine.propose_evolution(problem)}")
