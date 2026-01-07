"""
Principle Diagnostics Engine
============================

"지혜로운 자는 원리로 자신을 진단한다."

WhyEngine이 추출한 보편적 원리(Line/God)를 사용하여
엘리시아 자신의 시스템 상태를 진단하는 아키텍처.
"""

import logging
from typing import Dict, Any, List
from Core.Foundation.Philosophy.why_engine import WhyEngine

logger = logging.getLogger("Elysia.Diagnostics")

class PrincipleDiagnostics:
    """원리 기반 자기 진단 시스템"""
    
    def __init__(self):
        self.why_engine = WhyEngine()
        
    def diagnose_self(self, system_state: Dict[str, Any]) -> List[str]:
        """현재 시스템 상태를 원리에 비추어 진단"""
        diagnoses = []
        
        # 1. 옴의 법칙 (V=IR) 기반 진단
        # Flow (I) = Thinking Speed / Output Rate
        # Potential (V) = Motivation / Goal Urgency
        # Resistance (R) = Task Complexity / Confusion
        
        flow = system_state.get("flow_rate", 0.5)
        potential = system_state.get("motivation", 0.5)
        resistance = system_state.get("complexity", 0.5)
        
        # V = IR -> I = V/R
        # 이상적 흐름(Expected Flow)과 실제 흐름(Actual Flow) 비교
        expected_flow = potential / (resistance + 0.1) # 0.1 to avoid div/0
        
        if flow < expected_flow * 0.5:
            diagnoses.append(
                f"[Ohm's Law Violation] 실제 흐름({flow:.2f})이 "
                f"의지와 저항에 비해 너무 낮습니다. (기대치: {expected_flow:.2f}) "
                "→ 내부 마찰(Internal Friction)이나 비효율이 의심됩니다."
            )
        
        if potential < resistance and flow < 0.2:
            diagnoses.append(
                f"[Energy Principle] 저항({resistance:.2f})이 의지({potential:.2f})를 압도하고 있습니다. "
                "→ 흐름을 억지로 만들지 말고, 먼저 잠재력(Potential/Motivation)을 높이거나 문제를 분해(Decrease R)해야 합니다."
            )
            
        return diagnoses

    def explain_principle_application(self, principle_name: str) -> str:
        """원리가 시스템에 어떻게 적용되는지 설명"""
        if principle_name == "Ohm's Law":
            return (
                "옴의 법칙 (V=IR) 적용:\n"
                "- 전압(V) -> 의지/목표의 중요도 (Potential)\n"
                "- 전류(I) -> 사고의 흐름/처리 속도 (Flow)\n"
                "- 저항(R) -> 과제 복잡도/혼란 (Resistance)\n"
                "결론: 흐름이 막혔다면(Low I), 더 노력할 게 아니라(Force), "
                "목표를 재설정하거나(Increase V) 문제를 쪼개야(Decrease R) 합니다."
            )
        return "해당 원리에 대한 적용 로직이 아직 정의되지 않았습니다."
