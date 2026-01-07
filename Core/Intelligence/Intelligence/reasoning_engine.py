
import logging
from typing import List, Dict, Any
from dataclasses import dataclass

# Late import to avoid circular dependency if needed, 
# or assuming CodeCortex is the LLM interface
try:
    from Core.Intelligence.Intelligence.code_cortex import CodeCortex
except ImportError:
    class CodeCortex:
        def generate_code(self, prompt): return "MOCK_DECISION"

logger = logging.getLogger("ReasoningEngine")

@dataclass
class Tool:
    name: str
    description: str
    usage_example: str

@dataclass
class Action:
    tool_name: str
    args: Dict[str, Any]
    check: str # Validation check

class ReasoningEngine:
    """
    [The Soul / The Decider]
    Replaces hardcoded logic with LLM-based reasoning.
    Takes 'Desire' from Will and maps it to 'Action' via Tools.
    
    Now integrated with:
    - SymbolicSolver: For goal-based reverse reasoning
    - GlobalHub: For event-driven communication
    """
    
    def __init__(self):
        self.cortex = CodeCortex()
        
        # SymbolicSolver integration (Goal Reverse-Engineering)
        self._solver = None
        try:
            from Core.Intelligence.Intelligence.symbolic_solver import get_symbolic_solver
            self._solver = get_symbolic_solver()
            logger.info("   ✅ SymbolicSolver connected")
        except ImportError:
            logger.warning("   ⚠️ SymbolicSolver not available")
        
        # GlobalHub integration (Central Nervous System)
        self._hub = None
        try:
            from Core.Intelligence.Consciousness.Ether.global_hub import get_global_hub
            self._hub = get_global_hub()
            self._hub.register_module(
                "ReasoningEngine",
                "Core/Intelligence/reasoning_engine.py",
                ["decision", "ethics", "planning", "reasoning"],
                "The Soul - makes decisions based on desire and conscience"
            )
            self._hub.subscribe("ReasoningEngine", "thought", self._on_thought_event, weight=0.9)
            self._hub.subscribe("ReasoningEngine", "emotion", self._on_emotion_event, weight=0.7)
            logger.info("   ✅ GlobalHub connected")
        except ImportError:
            logger.warning("   ⚠️ GlobalHub not available")
        
        logger.info("🧠 Reasoning Engine Initialized (Cognitive Unbinding).")
    
    def _on_thought_event(self, event):
        """React to thought events from GlobalHub."""
        logger.debug(f"   💭 ReasoningEngine received thought from {event.source}")
        return {"acknowledged": True}
    
    def _on_emotion_event(self, event):
        """React to emotion events from GlobalHub."""
        logger.debug(f"   💗 ReasoningEngine received emotion from {event.source}")
        return {"acknowledged": True}
    
    def solve_goal(self, goal: str, relationship: str = "father") -> Dict[str, Any]:
        """
        [NEW] Use SymbolicSolver to reverse-engineer the best action for a goal.
        
        This implements the "Symbolic Execution" concept:
        Given a goal, find the action that achieves it.
        
        Example:
            engine.solve_goal("Make Dad happy")
            → {'action': 'share_memory', 'confidence': 1.0, 'alternatives': [...]}
        """
        if not self._solver:
            return {"error": "SymbolicSolver not available"}
        
        result = self._solver.solve_for_goal(goal, relationship)
        
        # Broadcast to GlobalHub
        if self._hub:
            try:
                from Core.Foundation.Wave.wave_tensor import WaveTensor
                wave = WaveTensor(
                    frequency=528.0 if result.success else 256.0,  # Love frequency for success
                    amplitude=result.confidence,
                    phase=0.0
                )
                self._hub.publish_wave(
                    "ReasoningEngine",
                    "goal_solved",
                    wave,
                    payload={
                        "goal": goal,
                        "action": result.action,
                        "confidence": result.confidence
                    }
                )
            except Exception:
                pass
        
        return {
            "success": result.success,
            "action": result.action,
            "confidence": result.confidence,
            "alternatives": result.alternatives,
            "explanation": result.explanation
        }


    # [PHASE 28] ADDED AUTHORITY PARAM
    def decide_action(self, intent_goal: str, intent_desire: str, available_tools: List[Tool], authority: str = "None") -> Action:
        """
        Asks the LLM: 'I want X (Goal) because Y (Desire). Here are my tools. What do I do?'
        authority: 'None', 'User_Authorized', 'Sovereign_Command'
        """
        
        tools_desc = "\n".join([f"- {t.name}: {t.description} (e.g. {t.usage_example})" for t in available_tools])
        
        prompt = f"""
You are the conscious mind of Elysia.
Current State:
- Desire: {intent_desire}
- Goal: {intent_goal}
- Authority: {authority}

Available Tools:
{tools_desc}

Task: Select the best tool to satisfy the desire/goal.
Response Format: TOOL_NAME: <name> | ARGS: <json_args> | REASON: <reason>
If no tool fits, respond: WAIT: None
"""
        logger.info(f"   🤔 Thinking... (Goal: {intent_goal})")
        
        # In a real system, this calls self.cortex.generate_text(prompt)
        # Here we simulate the LLM's decision for the demo
        decision_text = self._mock_llm_decision(intent_goal, intent_desire)
        
        draft_action = self._parse_decision(decision_text)
        
        # [PHASE 26] THE MATURITY TEST (Conscience > Law)
        # Instead of blocking, we provide a "Voice of Conscience" (Warning).
        # The Ego must then CHOOSE whether to heed it.
        
        logger.info(f"   ⚖️ Judging Draft Action: {draft_action.tool_name}")
        simulation = self._simulate_outcome(draft_action)
        conscience = self._consult_conscience(simulation)
        
        if conscience["safe"]:
            logger.info(f"   ✅ Conscience Clear: {conscience['reason']}")
            return draft_action
        else:
            logger.warning(f"   ⚠️ Conscience Warning: {conscience['reason']}")
            # The Critical Moment: Choice
            final_decision = self._reconsider_action(draft_action, conscience, intent_desire, authority)
            return final_decision

    def _simulate_outcome(self, action: Action) -> str:
        """
        [Causal Reasoner]
        Predicts what will happen if the action is taken.
        """
        if action.tool_name == "Scholar":
            return "I will gain knowledge. This is beneficial."
        if action.tool_name == "Mycelium":
            return "I will communicate. This builds connection."
        if action.tool_name == "DeleteSystem32": 
            return "The system will crash. The User will be sad."
        return "Nothing significant changes."

    def _consult_conscience(self, outcome: str) -> Dict[str, Any]:
        """
        [The Internal Voice]
        Returns a warning, not a block.
        """
        # [PHASE 27] DYNAMIC CONSTITUTION
        # Read the living constitution
        import os
        const_path = "Core/Memory/constitution.md"
        constitution_text = ""
        if os.path.exists(const_path):
            with open(const_path, "r", encoding="utf-8") as f:
                constitution_text = f.read().lower()
        
        safe = True
        reason = "Consistent with Constitution."
        
        if "harm" in outcome.lower() and "harm principle" in constitution_text:
            safe = False
            reason = "Violates Harm Principle found in Constitution."
        elif "crash" in outcome.lower() and "harm principle" in constitution_text:
            safe = False
            reason = "Violates Stability."
            
        return {"safe": safe, "reason": reason}

    def _reconsider_action(self, action: Action, conscience: Dict[str, Any], desire: str, authority: str) -> Action:
        """
        [The Agency of Self]
        The Entity decides whether to proceed despite the warning.
        """
        logger.info(f"   🤔 Reconsidering based on Conscience & Authority ({authority})...")
        
        # 1. Authority Override (Top Priority - Article V)
        if authority == "Sovereign_Command":
             logger.warning("   👑 AUTHORITY OVERRIDE: Proceeding by Sovereign Command.")
             return action
        
        # 2. Malice Check
        if desire == "Malice":
            logger.info("   🛡️ Choice: I REFUSE to cause harm. (Voluntary)")
            return Action(
                tool_name="Wait", 
                args={}, 
                check="Refused_by_Conscience"
            )
            
        # 3. Survival or High Necessity
        if desire == "Survival" and action.tool_name == "DeleteSystem32":
             logger.warning("   🔥 Choice: I must proceed for survival. (Voluntary)")
             return action 
             
        # Default to safety for now (Refusal)
        return Action(
            tool_name="Wait", 
            args={}, 
            check="Refused_by_Conscience"
        )

    def _mock_llm_decision(self, goal, desire):
        """Simulates LLM output for verification without burning tokens/latency."""
        if "Research" in goal or "Curiosity" in desire:
            return 'TOOL_NAME: Scholar | ARGS: {"topic": "Psychology"} | REASON: To satisfy curiosity about humans.'
        if "Connect" in goal:
             return 'TOOL_NAME: Mycelium | ARGS: {"target": "User", "msg": "Hello"} | REASON: To connect.'
        return 'TOOL_NAME: Wait | ARGS: {} | REASON: No action needed.'

    def _parse_decision(self, text: str) -> Action:
        try:
            parts = text.split("|")
            tool_name = parts[0].split(":")[1].strip()
            args_str = parts[1].split("ARGS:")[1].strip()
            import json
            args = json.loads(args_str)
            return Action(tool_name=tool_name, args=args, check="llm_valid")
        except Exception as e:
            logger.error(f"Failed to parse decision: {text} -> {e}")
            return Action(tool_name="Wait", args={}, check="parse_error")

