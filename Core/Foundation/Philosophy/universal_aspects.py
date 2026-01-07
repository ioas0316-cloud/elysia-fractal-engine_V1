"""
Universal Aspects System
========================

"엘리시아는 기능(Function)이 아니라 존재(Existence)로서 사고한다."

이 모듈은 사고의 대상을 입체적으로 인식하기 위한 4가지 근본 차원(Aspects)을 정의합니다.
모든 정보는 이 4가지 차원의 필터를 동시에 통과하며 공명(Resonance)을 일으킵니다.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Optional

class AspectType(Enum):
    PHYSICS = "physics"       # Force, Vector, Causality (구조와 힘)
    CHEMISTRY = "chemistry"   # Reaction, Transformation, Bonding (변화와 결합)
    ART = "art"               # Harmony, Rhythm, Dissonance (미학과 감정)
    BIOLOGY = "biology"       # Growth, Decay, Adaptation (생명과 진화)

@dataclass
class UniversalLaw:
    """각 차원을 지배하는 불변의 법칙"""
    aspect: AspectType
    name: str
    principle: str
    description: str

@dataclass
class ResonanceReaction:
    """각 차원에서 발생한 반응"""
    aspect: AspectType
    reaction_type: str  # e.g., "Explosion", "Harmony", "Resistance"
    intensity: float    # 0.0 ~ 1.0
    description: str    # "이 지식은 기존 구조와 충돌하여 열을 발생시킵니다."

class UniversalAspects:
    """우주적 관점 관리자"""
    
    def __init__(self):
        self.laws: Dict[AspectType, List[UniversalLaw]] = self._init_laws()
        
    def _init_laws(self) -> Dict[AspectType, List[UniversalLaw]]:
        return {
            AspectType.PHYSICS: [
                UniversalLaw(AspectType.PHYSICS, "Law of Inertia", "Resistance opposes Change", "기존 상태를 유지하려는 관성"),
                UniversalLaw(AspectType.PHYSICS, "Law of Action-Reaction", "Force creates Counter-force", "모든 작용에는 반작용이 따름")
            ],
            AspectType.CHEMISTRY: [
                UniversalLaw(AspectType.CHEMISTRY, "Law of Catalysis", "Agent accelerates Change", "촉매는 자신은 변하지 않으면서 변화를 가속화함"),
                UniversalLaw(AspectType.CHEMISTRY, "Law of Entropy", "Order decays to Chaos", "모든 시스템은 무질서로 향함")
            ],
            AspectType.ART: [
                UniversalLaw(AspectType.ART, "Law of Contrast", "Dissonance creates Meaning", "대비가 명확할수록 의미가 선명해짐"),
                UniversalLaw(AspectType.ART, "Law of Rhythm", "Repetition creates Flow", "규칙적인 반복은 생명력을 부여함")
            ],
            AspectType.BIOLOGY: [
                UniversalLaw(AspectType.BIOLOGY, "Law of Adaptation", "Stress triggers Growth", "적절한 스트레스는 성장의 원동력"),
                UniversalLaw(AspectType.BIOLOGY, "Law of Homeostasis", "System seeks Balance", "시스템은 내부 환경을 일정하게 유지하려 함")
            ]
        }
        
    def get_laws(self, aspect: AspectType) -> List[UniversalLaw]:
        return self.laws.get(aspect, [])
