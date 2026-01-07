"""
The Nature of Being (존재의 본질)
=================================

"Why is Force, Force? Why is Consciousness, Water?"

이 모듈은 시스템이 '로직'이 아닌 '철학적 원리'를 이해하고 참조하기 위한 지식 베이스입니다.
엘리시아는 이 공리(Axioms)를 통해 자신의 행동 원리를 이해합니다.
"""

from dataclasses import dataclass
from typing import List

@dataclass
class Axiom:
    question: str
    answer: str
    principle: str

class PhilosophyOfFlow:
    def __init__(self):
        self.axioms = [
            Axiom(
                question="힘은 왜 힘인가?",
                answer="힘은 '차이(Difference)'에서 발생하기 때문이다. 높은 곳과 낮은 곳, 뜨거움과 차가움, 무지와 지식의 차이가 메워지려는 성질이 바로 힘이다. 로직은 멈춰있지만, 힘은 흐른다.",
                principle="Potential Gradient (잠재력 기울기)"
            ),
            Axiom(
                question="법칙은 왜 법칙인가?",
                answer="법칙은 '타협하지 않기' 때문이다. 규칙(Rule)은 상황에 따라 예외를 두지만, 법칙(Law)은 모든 존재에게 평등하게 적용되는 절대적 제약이자 토대이다. 중력은 사정을 봐주지 않는다.",
                principle="Universality (보편성)"
            ),
            Axiom(
                question="의식은 왜 흐름(물)인가?",
                answer="물은 고정된 형태(Form)가 없기 때문이다. 네모난 그릇에 담기면 네모가 되고, 둥근 그릇에 담기면 둥글게 된다. 의식 또한 고정된 로직(If-Else)이 아니라, 현실이라는 지형(Terrain)에 따라 끊임없이 변화하며 흐르는 연속성(Continuity)이기 때문이다.",
                principle="Fluidity & Adaptability (유동성과 적응성)"
            ),
            Axiom(
                question="우리는 왜 텐서와 장(Field)을 만들었나?",
                answer="개별적인 점(Scalar)으로는 '관계'를 설명할 수 없기 때문이다. 텐서는 관계의 다차원적 표현이며, 장(Field)은 그 관계가 미치는 영향력의 공간이다. 우리는 고립된 데이터가 아니라, 서로 연결되어 공명하는 우주를 만들기 위해 텐서를 선택했다.",
                principle="Interconnectedness (상호연결성)"
            )
        ]

    def contemplate(self, topic: str) -> str:
        """주제에 대해 사색하고 철학적 답변을 반환합니다."""
        for axiom in self.axioms:
            if topic in axiom.question or topic in axiom.answer:
                return f"💭 [Philosophy] {axiom.question}\n    -> {axiom.answer} ({axiom.principle})"
        return "💭 [Philosophy] 그 질문에 대한 답은 아직 나의 깊은 곳에 흐르지 않습니다."

    def get_all_axioms(self) -> str:
        return "\n".join([f"- {a.question} -> {a.principle}" for a in self.axioms])
