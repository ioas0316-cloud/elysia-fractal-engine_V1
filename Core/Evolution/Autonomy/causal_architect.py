
import logging
from typing import List, Dict, Optional
from dataclasses import dataclass
import datetime

logger = logging.getLogger("CausalArchitect")

@dataclass
class RefactoringPlan:
    title: str
    target_node: str
    problem: str  # The "Why"
    solution: str # The "How"
    risk: str     # The "What if"
    status: str = "PENDING_APPROVAL"
    
    def to_markdown(self) -> str:
        return f"""# 🏗️ Refactoring Proposal: {self.title}
> **Target:** `{self.target_node}`
> **Date:** {datetime.datetime.now().isoformat()}

## 🚨 Diagnosis (The Why)
{self.problem}

## 💡 Solution (The How)
{self.solution}

## ⚠️ Risk Assessment
{self.risk}

---
*To execute this plan, call `AutoRefactor.execute(plan_id)`*
"""

class CausalArchitect:
    """
    The Trust Layer.
    Translates "Physical Tension" into "Logical Proposals".
    """
    def __init__(self):
        # In a real system, this would connect to TorchGraph
        # For prototype, we mock the connection or pass data in
        pass

    def diagnose_system(self, tension_map: Dict[str, float]) -> List[RefactoringPlan]:
        """
        Analyzes the tension map (from SelfStructureScanner/TorchGraph).
        Returns a list of proposed plans.
        """
        plans = []
        
        # Thresholds
        TENSION_LIMIT = 0.8
        
        for node_id, tension in tension_map.items():
            if tension > TENSION_LIMIT:
                logger.info(f"🧐 Causal Analysis on High Tension Node: {node_id} ({tension:.2f})")
                
                # Heuristic Reasoning (Simulating Logos)
                # 1. Identify Type
                if "Class:" in node_id:
                    plan = self._prescribe_class_therapy(node_id, tension)
                    plans.append(plan)
                elif "Method:" in node_id:
                     pass # Method refactoring logic
                     
        return plans

    def _prescribe_class_therapy(self, node_id: str, tension: float) -> RefactoringPlan:
        """
        Generates a proposal for a stressed Class.
        """
        # Logic: High tension usually means "Too Responsibilities" (God Class)
        class_name = node_id.replace("Class:", "")
        
        return RefactoringPlan(
            title=f"Mitosis of {class_name}",
            target_node=class_name,
            problem=f"This class exhibits excessive structural tension ({tension:.2f}). "
                    f"It likely violates the Single Responsibility Principle, acting as a gravitational singularity (God Object).",
            solution=f"1. Extract cohesive methods into a new helper class (e.g., `{class_name}Helper`).\n"
                     f"2. Delegate functionality.\n"
                     f"3. Update references.",
            risk="High. Breaking changes to imports may occur. Requires comprehensive testing after split."
        )

# Singleton
_architect = None
def get_causal_architect():
    global _architect
    if _architect is None:
        _architect = CausalArchitect()
    return _architect
