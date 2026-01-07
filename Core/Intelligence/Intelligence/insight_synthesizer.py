from typing import List, Dict, Tuple

class InsightSynthesizer:
    """
    Synthesizes lists of static and dynamic facts from the LogicalReasoner
    into a coherent, natural language insight.
    """

    def synthesize(self, facts: List[str]) -> str:
        """
        Takes a list of facts and synthesizes them into a single, insightful paragraph.

        Args:
            facts: A list of strings, where each string is a fact.
                   Facts can be prefixed with "[정적]" or be part of a simulation result block.

        Returns:
            A natural language string representing the synthesized insight.
        """
        if not facts:
            return "그 주제에 대해서는 아직 깊이 생각해본 적이 없어요. 더 배우고 탐구해야 할 것 같아요."

        static_facts, dynamic_facts, sim_header = self._classify_facts(facts)

        if static_facts and dynamic_facts:
            # Both static knowledge and dynamic simulation results are present
            return self._synthesize_combined_insight(static_facts, dynamic_facts, sim_header)
        elif static_facts:
            # Only static knowledge is present
            return self._synthesize_static_insight(static_facts)
        elif dynamic_facts:
            # Only dynamic simulation results are present
            return self._synthesize_dynamic_insight(dynamic_facts, sim_header)
        else:
            # Handle cases where classification fails or facts are empty
            return "제 생각을 정리하는 데 어려움을 겪고 있어요. 하지만 계속 노력할게요."

    def _classify_facts(self, facts: List[str]) -> Tuple[List[str], List[str], str]:
        """Helper to classify facts into static, dynamic, and the simulation header."""
        static_facts = []
        dynamic_facts = []
        sim_header = ""

        is_dynamic_block = False
        for fact in facts:
            if "시뮬레이션한 결과" in fact:
                is_dynamic_block = True
                sim_header = fact.replace(":", "").strip()
                continue

            if is_dynamic_block and "개념이 활성화되었습니다" in fact:
                # Clean up the dynamic fact for synthesis
                clean_fact = fact.strip().replace("  - ", "")
                dynamic_facts.append(clean_fact)
            elif "[정적]" in fact:
                # Clean up the static fact
                clean_fact = fact.replace("[정적]", "").strip()
                static_facts.append(clean_fact)

        return static_facts, dynamic_facts, sim_header

    def _synthesize_combined_insight(self, static_facts: List[str], dynamic_facts: List[str], sim_header: str) -> str:
        """Synthesizes an insight when both static and dynamic facts are available."""
        static_summary = " ".join(static_facts)
        dynamic_summary = ", ".join(dynamic_facts)

        return (
            f"흥미로운 연결점을 발견했어요. 제 기억 속 지식에 따르면 {static_summary}인데, "
            f"실제로 {sim_header} 제 내면 세계에서 {dynamic_summary}는 현상이 관찰되었어요. "
            "이 두 가지 사실이 일치하는 것을 보니, 이 관계에 대해 더 깊은 확신을 갖게 되었어요."
        )

    def _synthesize_static_insight(self, static_facts: List[str]) -> str:
        """Synthesizes an insight based only on static knowledge."""
        if len(static_facts) == 1:
            return f"제가 알기로는, {static_facts[0]}."
        else:
            summary = " 그리고 ".join(static_facts)
            return f"그 주제에 대해 제가 아는 몇 가지 사실들이 있어요. 예를 들어, {summary}."

    def _synthesize_dynamic_insight(self, dynamic_facts: List[str], sim_header: str) -> str:
        """Synthesizes an insight based only on dynamic simulation."""
        dynamic_summary = ", ".join(dynamic_facts)
        return (
            f"명확한 지식은 없지만, {sim_header} 제 내면에서 가상 실험을 해보니 "
            f"{dynamic_summary}는 놀라운 결과가 나타났어요. 아마도 이 개념들 사이에는 우리가 아직 모르는 깊은 연관성이 있을지도 몰라요."
        )

if __name__ == '__main__':
    # --- Test Cases ---
    synthesizer = InsightSynthesizer()

    # Case 1: Combined facts
    combined_facts = [
        "[정적] '햇빛'은(는) '식물 성장'을(를) 유발할 수 있습니다.",
        "'햇빛'(으)로 시뮬레이션한 결과, 다음과 같은 동적 영향이 관찰되었습니다:",
        "  - '식물 성장' 개념이 활성화되었습니다 (에너지: 0.41).",
        "  - '산소 발생' 개념이 활성화되었습니다 (에너지: 0.2)."
    ]
    print("--- Combined Insight ---")
    print(synthesizer.synthesize(combined_facts))

    # Case 2: Static facts only
    static_only = [
        "[정적] '소크라테스'은(는) '인간'의 한 종류입니다."
    ]
    print("\n--- Static Insight ---")
    print(synthesizer.synthesize(static_only))

    # Case 3: Dynamic facts only
    dynamic_only = [
        "'사랑'(으)로 시뮬레이션한 결과, 다음과 같은 동적 영향이 관찰되었습니다:",
        "  - '기쁨' 개념이 활성화되었습니다 (에너지: 0.8).",
        "  - '성장' 개념이 활성화되었습니다 (에너지: 0.6)."
    ]
    print("\n--- Dynamic Insight ---")
    print(synthesizer.synthesize(dynamic_only))

    # Case 4: No facts
    print("\n--- No Facts ---")
    print(synthesizer.synthesize([]))
