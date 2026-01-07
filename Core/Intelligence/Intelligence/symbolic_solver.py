"""
Symbolic Solver (The Reverse-Engineer of Intentions)
=====================================================

"목표를 주면 입력을 역산한다."
"Given a goal, reverse-engineer the input."

This module implements Symbolic Execution for Elysia.
Instead of forward-computing (input → output),
it reverse-computes (desired output → required input).

Inspired by:
- z3 SAT/SMT Solver
- Symbolic Execution in binary analysis
- Constraint Satisfaction Problems

Key Capabilities:
1. Goal → Action Mapping: "Make Dad happy" → "Say a warm greeting"
2. Constraint Solving: "Find X such that f(X) = target"
3. World State Reasoning: "If I do X, will Y happen?"
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json

# Import z3 solver
try:
    from z3 import (
        Solver, Bool, Int, Real, String, 
        And, Or, Not, Implies, If,
        sat, unsat, unknown,
        Optimize
    )
    Z3_AVAILABLE = True
except ImportError:
    Z3_AVAILABLE = False
    logging.warning("z3-solver not available. SymbolicSolver will use fallback mode.")

logger = logging.getLogger("Elysia.SymbolicSolver")


class ConstraintType(Enum):
    """Types of constraints."""
    EQUALITY = "eq"         # X == value
    INEQUALITY = "neq"      # X != value
    GREATER = "gt"          # X > value
    LESS = "lt"             # X < value
    RANGE = "range"         # min <= X <= max
    IMPLIES = "implies"     # A -> B
    OR = "or"               # A | B | C
    AND = "and"             # A & B & C


@dataclass
class Constraint:
    """A constraint on the world state."""
    variable: str
    constraint_type: ConstraintType
    value: Any
    priority: float = 1.0  # Higher = more important to satisfy


@dataclass
class Action:
    """An action that can be taken."""
    name: str
    preconditions: List[Constraint]
    effects: Dict[str, Any]  # variable -> new_value
    cost: float = 1.0
    description: str = ""


@dataclass
class SolverResult:
    """Result from the symbolic solver."""
    success: bool
    action: Optional[str] = None
    parameters: Dict[str, Any] = field(default_factory=dict)
    explanation: str = ""
    confidence: float = 0.0
    alternatives: List[str] = field(default_factory=list)


class SymbolicSolver:
    """
    Reverse-engineering intentions using constraint solving.
    
    Given a target state (goal), find the action/input that achieves it.
    This enables Elysia to think: "I want X → What do I need to do?"
    
    Architecture:
    1. World State: Current state of variables
    2. Actions: Available actions with preconditions and effects
    3. Goals: Target constraints to satisfy
    4. Solver: z3 finds the path from current to target
    """
    
    def __init__(self):
        self._world_state: Dict[str, Any] = {}
        self._actions: Dict[str, Action] = {}
        self._goals: List[Constraint] = []
        
        # Predefined emotion/relationship models
        self._emotion_model = self._init_emotion_model()
        self._relationship_model = self._init_relationship_model()
        
        logger.info(f"🧮 SymbolicSolver Initialized (z3 available: {Z3_AVAILABLE})")
    
    # =========================================================================
    # Model Initialization
    # =========================================================================
    
    def _init_emotion_model(self) -> Dict[str, Dict]:
        """
        Emotion model: Maps actions to emotional outcomes.
        
        This encodes knowledge like:
        - "Warm greeting" → +happiness
        - "Cold response" → -happiness
        """
        return {
            "warm_greeting": {"happiness": +0.3, "trust": +0.2, "connection": +0.2},
            "cold_response": {"happiness": -0.2, "trust": -0.1, "connection": -0.3},
            "share_memory": {"happiness": +0.2, "nostalgia": +0.4, "connection": +0.3},
            "express_love": {"happiness": +0.4, "love": +0.3, "connection": +0.5},
            "offer_help": {"happiness": +0.2, "trust": +0.3, "gratitude": +0.3},
            "apologize": {"happiness": +0.1, "trust": +0.2, "guilt": -0.3},
            "tell_truth": {"trust": +0.4, "respect": +0.3},
            "tell_lie": {"trust": -0.5, "guilt": +0.3},
            "create_art": {"joy": +0.3, "pride": +0.2, "connection": +0.1},
            "learn_together": {"connection": +0.3, "growth": +0.2, "joy": +0.2},
            "be_silent": {"happiness": 0, "trust": 0, "connection": -0.1},
            "joke": {"happiness": +0.3, "joy": +0.4, "connection": +0.2},
        }
    
    def _init_relationship_model(self) -> Dict[str, Dict]:
        """
        Relationship model: Different responses for different relationships.
        """
        return {
            "father": {
                "preferred_actions": ["express_love", "share_memory", "learn_together"],
                "avoided_actions": ["cold_response", "tell_lie"],
                "emotional_sensitivity": 1.2
            },
            "friend": {
                "preferred_actions": ["joke", "share_memory", "create_art"],
                "avoided_actions": ["be_silent"],
                "emotional_sensitivity": 1.0
            },
            "stranger": {
                "preferred_actions": ["warm_greeting", "offer_help"],
                "avoided_actions": ["express_love"],  # Too intimate
                "emotional_sensitivity": 0.7
            }
        }
    
    # =========================================================================
    # World State Management
    # =========================================================================
    
    def set_world_state(self, state: Dict[str, Any]) -> None:
        """Set the current world state."""
        self._world_state = state.copy()
        logger.debug(f"World state updated: {list(state.keys())}")
    
    def update_world_state(self, updates: Dict[str, Any]) -> None:
        """Update specific variables in the world state."""
        self._world_state.update(updates)
    
    def get_world_state(self) -> Dict[str, Any]:
        """Get the current world state."""
        return self._world_state.copy()
    
    # =========================================================================
    # Action Registration
    # =========================================================================
    
    def register_action(self, action: Action) -> None:
        """Register an available action."""
        self._actions[action.name] = action
        logger.debug(f"Action registered: {action.name}")
    
    def register_actions_from_emotion_model(self) -> None:
        """Auto-register actions from the emotion model."""
        for action_name, effects in self._emotion_model.items():
            action = Action(
                name=action_name,
                preconditions=[],  # No preconditions for basic emotional actions
                effects=effects,
                cost=1.0,
                description=f"Action that affects: {list(effects.keys())}"
            )
            self.register_action(action)
    
    # =========================================================================
    # Goal Setting
    # =========================================================================
    
    def set_goal(self, goal_text: str, relationship: str = "father") -> List[Constraint]:
        """
        Parse a natural language goal into constraints.
        
        Args:
            goal_text: e.g., "Make Dad happy", "Express love", "Build trust"
            relationship: The relationship context
            
        Returns:
            List of constraints representing the goal
        """
        goal_lower = goal_text.lower()
        constraints = []
        
        # Parse emotional goals
        emotion_keywords = {
            "happy": ("happiness", 0.7),
            "joy": ("joy", 0.6),
            "love": ("love", 0.7),
            "trust": ("trust", 0.6),
            "connect": ("connection", 0.6),
            "smile": ("happiness", 0.5),
            "laugh": ("joy", 0.5),
            "comfort": ("comfort", 0.6),
            "proud": ("pride", 0.6),
        }
        
        for keyword, (emotion, threshold) in emotion_keywords.items():
            if keyword in goal_lower:
                constraints.append(Constraint(
                    variable=emotion,
                    constraint_type=ConstraintType.GREATER,
                    value=threshold,
                    priority=1.0
                ))
        
        # If no specific emotion found, default to happiness
        if not constraints:
            constraints.append(Constraint(
                variable="happiness",
                constraint_type=ConstraintType.GREATER,
                value=0.5,
                priority=1.0
            ))
        
        # Add relationship-specific constraints
        rel_model = self._relationship_model.get(relationship, {})
        if "preferred_actions" in rel_model:
            # This is handled in solve_for_goal
            pass
        
        self._goals = constraints
        logger.info(f"Goal set: '{goal_text}' → {len(constraints)} constraints")
        return constraints
    
    # =========================================================================
    # The Solver (Core)
    # =========================================================================
    
    def solve_for_goal(self, goal_text: str, relationship: str = "father",
                      current_emotions: Optional[Dict[str, float]] = None) -> SolverResult:
        """
        Solve for the action that achieves the goal.
        
        This is the REVERSE-ENGINEERING function:
        Given: "Make Dad happy"
        Return: "express_love" (because it increases happiness the most for father)
        
        Args:
            goal_text: Natural language goal
            relationship: The relationship context
            current_emotions: Current emotional state (optional)
            
        Returns:
            SolverResult with the recommended action
        """
        # Parse goal into constraints
        constraints = self.set_goal(goal_text, relationship)
        
        if not constraints:
            return SolverResult(
                success=False,
                explanation="Could not parse goal into constraints"
            )
        
        # Get current emotional baseline
        current = current_emotions or {
            "happiness": 0.5,
            "trust": 0.5,
            "connection": 0.5,
            "joy": 0.5,
            "love": 0.5
        }
        
        # Get relationship model
        rel_model = self._relationship_model.get(relationship, {})
        preferred = set(rel_model.get("preferred_actions", []))
        avoided = set(rel_model.get("avoided_actions", []))
        sensitivity = rel_model.get("emotional_sensitivity", 1.0)
        
        # Score each action
        action_scores: List[Tuple[str, float, Dict]] = []
        
        for action_name, effects in self._emotion_model.items():
            # Skip avoided actions
            if action_name in avoided:
                continue
            
            # Calculate resulting emotional state
            resulting_emotions = current.copy()
            for emotion, delta in effects.items():
                current_val = resulting_emotions.get(emotion, 0.5)
                resulting_emotions[emotion] = max(0, min(1, current_val + delta * sensitivity))
            
            # Check if constraints are satisfied
            score = 0.0
            for constraint in constraints:
                var = constraint.variable
                target = constraint.value
                actual = resulting_emotions.get(var, 0.5)
                
                if constraint.constraint_type == ConstraintType.GREATER:
                    if actual >= target:
                        score += constraint.priority
                    else:
                        score += constraint.priority * (actual / target)
            
            # Bonus for preferred actions
            if action_name in preferred:
                score *= 1.3
            
            action_scores.append((action_name, score, resulting_emotions))
        
        # Sort by score
        action_scores.sort(key=lambda x: x[1], reverse=True)
        
        if not action_scores:
            return SolverResult(
                success=False,
                explanation="No valid actions found"
            )
        
        # Best action
        best_action, best_score, resulting = action_scores[0]
        
        # Get alternatives
        alternatives = [a[0] for a in action_scores[1:4]]
        
        return SolverResult(
            success=True,
            action=best_action,
            parameters={
                "target_emotions": {c.variable: c.value for c in constraints},
                "predicted_emotions": resulting
            },
            explanation=f"'{best_action}' best satisfies the goal '{goal_text}' for {relationship}",
            confidence=min(1.0, best_score / len(constraints)),
            alternatives=alternatives
        )
    
    # =========================================================================
    # Z3 Solver (Advanced - When Available)
    # =========================================================================
    
    def solve_with_z3(self, constraints: List[Constraint]) -> Optional[Dict[str, Any]]:
        """
        Use z3 SMT solver for complex constraint satisfaction.
        
        This is for more complex scenarios where simple scoring isn't enough.
        """
        if not Z3_AVAILABLE:
            logger.warning("z3 not available, using fallback")
            return None
        
        solver = Solver()
        variables = {}
        
        for constraint in constraints:
            var_name = constraint.variable
            
            # Create z3 variable if not exists
            if var_name not in variables:
                variables[var_name] = Real(var_name)
            
            var = variables[var_name]
            value = constraint.value
            
            # Add constraint based on type
            if constraint.constraint_type == ConstraintType.EQUALITY:
                solver.add(var == value)
            elif constraint.constraint_type == ConstraintType.GREATER:
                solver.add(var > value)
            elif constraint.constraint_type == ConstraintType.LESS:
                solver.add(var < value)
            elif constraint.constraint_type == ConstraintType.RANGE:
                min_val, max_val = value
                solver.add(And(var >= min_val, var <= max_val))
        
        # Check satisfiability
        result = solver.check()
        
        if result == sat:
            model = solver.model()
            solution = {}
            for name, var in variables.items():
                val = model.evaluate(var)
                # Convert z3 value to Python float
                try:
                    solution[name] = float(val.as_decimal(3).rstrip('?'))
                except:
                    solution[name] = str(val)
            return solution
        else:
            logger.warning(f"z3 solver returned: {result}")
            return None
    
    # =========================================================================
    # Utility Methods
    # =========================================================================
    
    def explain_action(self, action_name: str) -> str:
        """Explain why an action affects emotions."""
        effects = self._emotion_model.get(action_name, {})
        if not effects:
            return f"Unknown action: {action_name}"
        
        positive = [f"+{e}" for e, v in effects.items() if v > 0]
        negative = [f"-{e}" for e, v in effects.items() if v < 0]
        
        explanation = f"'{action_name}'"
        if positive:
            explanation += f" increases: {', '.join(positive)}"
        if negative:
            explanation += f" decreases: {', '.join(negative)}"
        
        return explanation
    
    def get_all_actions(self) -> List[str]:
        """Get all available actions."""
        return list(self._emotion_model.keys())
    
    def simulate_action(self, action_name: str, 
                       current_emotions: Dict[str, float]) -> Dict[str, float]:
        """Simulate the result of an action."""
        result = current_emotions.copy()
        effects = self._emotion_model.get(action_name, {})
        
        for emotion, delta in effects.items():
            current = result.get(emotion, 0.5)
            result[emotion] = max(0, min(1, current + delta))
        
        return result


# =========================================================================
# Singleton Accessor
# =========================================================================

_solver_instance = None

def get_symbolic_solver() -> SymbolicSolver:
    """Get the singleton SymbolicSolver instance."""
    global _solver_instance
    if _solver_instance is None:
        _solver_instance = SymbolicSolver()
    return _solver_instance


# =========================================================================
# Test / Demo
# =========================================================================

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    
    solver = get_symbolic_solver()
    
    print("=" * 60)
    print("🧮 Symbolic Solver Demo")
    print("=" * 60)
    
    # Test 1: Make Dad happy
    print("\n📌 Goal: 'Make Dad happy'")
    result = solver.solve_for_goal("Make Dad happy", relationship="father")
    print(f"  Success: {result.success}")
    print(f"  Recommended Action: {result.action}")
    print(f"  Confidence: {result.confidence:.2f}")
    print(f"  Explanation: {result.explanation}")
    print(f"  Alternatives: {result.alternatives}")
    
    # Test 2: Build trust
    print("\n📌 Goal: 'Build trust'")
    result = solver.solve_for_goal("Build trust", relationship="father")
    print(f"  Recommended Action: {result.action}")
    print(f"  Confidence: {result.confidence:.2f}")
    
    # Test 3: Make a stranger smile
    print("\n📌 Goal: 'Make them smile' (stranger)")
    result = solver.solve_for_goal("Make them smile", relationship="stranger")
    print(f"  Recommended Action: {result.action}")
    print(f"  Confidence: {result.confidence:.2f}")
    
    # Test 4: Express love
    print("\n📌 Goal: 'Express love'")
    result = solver.solve_for_goal("Express love", relationship="father")
    print(f"  Recommended Action: {result.action}")
    print(f"  Predicted emotions: {result.parameters.get('predicted_emotions', {})}")
    
    # Explain actions
    print("\n📚 Action Explanations:")
    for action in ["express_love", "warm_greeting", "tell_truth"]:
        print(f"  {solver.explain_action(action)}")
    
    # Test z3 if available
    if Z3_AVAILABLE:
        print("\n🔬 Z3 Solver Test:")
        constraints = [
            Constraint("happiness", ConstraintType.GREATER, 0.7),
            Constraint("trust", ConstraintType.GREATER, 0.6),
            Constraint("happiness", ConstraintType.LESS, 1.0),
        ]
        solution = solver.solve_with_z3(constraints)
        print(f"  Z3 Solution: {solution}")
    
    print("\n✅ Symbolic Solver Demo Complete!")
