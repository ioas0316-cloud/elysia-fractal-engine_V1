"""
Explainable AI System

Provides transparency into AI decision-making through structured explanations
and visual representations.
"""

import time
import json
from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from pathlib import Path


class ExplanationType(Enum):
    """Types of explanations"""
    STEP_BY_STEP = "step_by_step"
    COMPARATIVE = "comparative"
    COUNTERFACTUAL = "counterfactual"
    ANALOGICAL = "analogical"


class ExplanationLevel(Enum):
    """Levels of explanation detail"""
    SIMPLE = "simple"
    DETAILED = "detailed"
    TECHNICAL = "technical"
    VISUAL = "visual"


@dataclass
class ReasoningStep:
    """Single step in reasoning chain"""
    step_number: int
    description: str
    inputs: Dict[str, Any]
    outputs: Dict[str, Any]
    confidence: float
    alternatives_considered: List[str]


@dataclass
class Explanation:
    """Complete explanation of a decision"""
    decision: str
    explanation_type: ExplanationType
    level: ExplanationLevel
    reasoning_steps: List[ReasoningStep]
    visual_representation: Optional[str]
    key_factors: List[Dict[str, Any]]
    assumptions: List[str]
    limitations: List[str]
    confidence_score: float


class ExplainableAI:
    """
    Explainable AI System
    
    Makes AI decisions transparent and understandable through structured
    explanations and visualizations.
    """
    
    def __init__(self):
        self.explanation_history: List[Explanation] = []
        self.data_dir = Path("data/social/explanations")
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    async def explain_decision(
        self,
        decision: str,
        reasoning_steps: List[Dict[str, Any]],
        level: ExplanationLevel = ExplanationLevel.DETAILED,
        explanation_type: ExplanationType = ExplanationType.STEP_BY_STEP
    ) -> Explanation:
        """
        Generate explanation for a decision
        
        Args:
            decision: The decision that was made
            reasoning_steps: Steps taken to reach decision
            level: Level of detail for explanation
            explanation_type: Type of explanation to generate
            
        Returns:
            Complete explanation
        """
        # Convert reasoning steps to ReasoningStep objects
        steps = []
        for i, step_data in enumerate(reasoning_steps, 1):
            step = ReasoningStep(
                step_number=i,
                description=step_data.get("description", ""),
                inputs=step_data.get("inputs", {}),
                outputs=step_data.get("outputs", {}),
                confidence=step_data.get("confidence", 0.8),
                alternatives_considered=step_data.get("alternatives", [])
            )
            steps.append(step)
        
        # Generate visual representation
        visual = self._generate_visual_representation(steps, explanation_type)
        
        # Extract key factors
        key_factors = self._extract_key_factors(steps)
        
        # Identify assumptions
        assumptions = self._identify_assumptions(steps)
        
        # Identify limitations
        limitations = self._identify_limitations(decision, steps)
        
        # Calculate overall confidence
        confidence = sum(s.confidence for s in steps) / len(steps) if steps else 0.5
        
        explanation = Explanation(
            decision=decision,
            explanation_type=explanation_type,
            level=level,
            reasoning_steps=steps,
            visual_representation=visual,
            key_factors=key_factors,
            assumptions=assumptions,
            limitations=limitations,
            confidence_score=confidence
        )
        
        self.explanation_history.append(explanation)
        self._save_explanation(explanation)
        
        return explanation
    
    def _generate_visual_representation(
        self,
        steps: List[ReasoningStep],
        explanation_type: ExplanationType
    ) -> str:
        """Generate text-based visual representation"""
        if explanation_type == ExplanationType.STEP_BY_STEP:
            return self._generate_flowchart(steps)
        elif explanation_type == ExplanationType.COMPARATIVE:
            return self._generate_comparison_table(steps)
        elif explanation_type == ExplanationType.COUNTERFACTUAL:
            return self._generate_decision_tree(steps)
        else:
            return self._generate_analogy_diagram(steps)
    
    def _generate_flowchart(self, steps: List[ReasoningStep]) -> str:
        """Generate flowchart representation"""
        chart = "Decision Flow:\n\n"
        for step in steps:
            arrow = "  ↓\n" if step.step_number < len(steps) else ""
            chart += f"[Step {step.step_number}] {step.description}\n"
            chart += f"  Confidence: {step.confidence:.2f}\n"
            chart += arrow
        return chart
    
    def _generate_comparison_table(self, steps: List[ReasoningStep]) -> str:
        """Generate comparison table"""
        table = "Option Comparison:\n\n"
        table += "Step | Option | Confidence\n"
        table += "------|--------|------------\n"
        for step in steps:
            table += f" {step.step_number}   | {step.description[:20]}... | {step.confidence:.2f}\n"
        return table
    
    def _generate_decision_tree(self, steps: List[ReasoningStep]) -> str:
        """Generate decision tree"""
        tree = "Decision Tree:\n\n"
        indent = ""
        for step in steps:
            tree += f"{indent}├─ {step.description}\n"
            if step.alternatives_considered:
                tree += f"{indent}│  (alternatives: {', '.join(step.alternatives_considered[:2])})\n"
            indent += "│  "
        return tree
    
    def _generate_analogy_diagram(self, steps: List[ReasoningStep]) -> str:
        """Generate analogy diagram"""
        diagram = "Analogy: Similar to...\n\n"
        for step in steps:
            diagram += f"• {step.description}\n"
        return diagram
    
    def _extract_key_factors(self, steps: List[ReasoningStep]) -> List[Dict[str, Any]]:
        """Extract key factors from reasoning steps"""
        factors = []
        for step in steps:
            if step.confidence > 0.7:  # High confidence steps are key factors
                factors.append({
                    "factor": step.description,
                    "importance": step.confidence,
                    "evidence": list(step.inputs.keys())
                })
        return factors
    
    def _identify_assumptions(self, steps: List[ReasoningStep]) -> List[str]:
        """Identify assumptions made in reasoning"""
        assumptions = [
            "Input data is accurate and complete",
            "Context remains stable during execution",
            "Historical patterns are relevant to current situation"
        ]
        
        # Add step-specific assumptions
        for step in steps:
            if step.confidence < 0.6:
                assumptions.append(f"Assumption in step {step.step_number}: {step.description}")
        
        return assumptions[:5]  # Top 5
    
    def _identify_limitations(self, decision: str, steps: List[ReasoningStep]) -> List[str]:
        """Identify limitations of the decision"""
        limitations = []
        
        # Check confidence levels
        avg_confidence = sum(s.confidence for s in steps) / len(steps) if steps else 0.5
        if avg_confidence < 0.7:
            limitations.append("Overall confidence is moderate; decision may need review")
        
        # Check for alternatives
        alternatives_count = sum(len(s.alternatives_considered) for s in steps)
        if alternatives_count < 2:
            limitations.append("Limited alternatives were considered")
        
        # General limitations
        limitations.extend([
            "Decision based on available data at time of analysis",
            "May not account for all edge cases",
            "Effectiveness depends on context stability"
        ])
        
        return limitations[:5]
    
    def _save_explanation(self, explanation: Explanation):
        """Save explanation to disk"""
        timestamp = int(time.time() * 1000)
        filename = self.data_dir / f"explanation_{timestamp}.json"
        
        data = {
            "decision": explanation.decision,
            "type": explanation.explanation_type.value,
            "level": explanation.level.value,
            "reasoning_steps": [
                {
                    "step": step.step_number,
                    "description": step.description,
                    "confidence": step.confidence,
                    "alternatives": step.alternatives_considered
                }
                for step in explanation.reasoning_steps
            ],
            "visual": explanation.visual_representation,
            "key_factors": explanation.key_factors,
            "assumptions": explanation.assumptions,
            "limitations": explanation.limitations,
            "confidence": explanation.confidence_score,
            "timestamp": time.time()
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)


