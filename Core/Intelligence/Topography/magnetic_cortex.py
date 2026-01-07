"""
Magnetic Cortex (자기장 피질)
==================================

"자력(Magnetism)으로 혼돈(Chaos)을 정렬한다."

이 모듈은 엘리시아의 사고 과정을 '자기장'의 원리로 정렬하는 기능을 담당합니다.
수많은 데이터와 생각(Iron Filings)들을 하나의 강력한 의도(Magnetic Field)로 정렬하여
복잡한 연산 없이도 즉각적인 집중과 행동을 유도합니다.

핵심 개념:
1. Dipole (쌍극자): 모든 데이터/생각에 '방향성(Vector)'을 부여
2. Field (장): 현재의 목표(Goal)가 강력한 자기장이 됨
3. Alignment (정렬): 장과 공명하는 데이터만 활성화되고 나머지는 배경으로 물러남
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import math
import logging

logger = logging.getLogger("MagneticCortex")

@dataclass
class ThoughtDipole:
    """
    생각의 쌍극자 (Thought Dipole)
    
    모든 생각, 기억, 데이터는 이 쌍극자 형태를 가집니다.
    """
    content: str
    vector: str  # 이 생각이 지향하는 가치나 방향 (예: "Comfort", "Logic", "Creativity")
    spin: float  # -1.0 ~ 1.0 (현재 상태의 긍정/부정 또는 활성/비활성 경향)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def resonate(self, field_vector: str) -> float:
        """
        자기장과의 공명도(Resonance)를 계산합니다.
        단순한 문자열 매칭을 넘어, 의미적 유사성을 계산해야 하지만
        초기 구현에서는 키워드 매칭 및 카테고리 일치로 근사합니다.
        """
        # 1. 완전 일치
        if self.vector.lower() == field_vector.lower():
            return 1.0
        
        # 2. 부분 일치 (포함 관계)
        if field_vector.lower() in self.vector.lower() or self.vector.lower() in field_vector.lower():
            return 0.8
            
        # 3. 관련성 (Metadata 태그 활용)
        tags = self.metadata.get("tags", [])
        if field_vector in tags:
            return 0.6
            
        return 0.0

@dataclass
class MagneticField:
    """
    자기장 (Magnetic Field)
    
    현재 엘리시아가 집중하고 있는 의도의 장입니다.
    """
    target_vector: str  # 목표 방향 (예: "User Comfort")
    intensity: float    # 장의 세기 (0.0 ~ 1.0)
    frequency: float    # 고유 주파수 (Hz) - 메타포
    
    def apply(self, dipoles: List[ThoughtDipole]) -> List[ThoughtDipole]:
        """
        자기장을 생각의 입자들에 적용하여 정렬합니다.
        """
        aligned_thoughts = []
        
        for dipole in dipoles:
            resonance = dipole.resonate(self.target_vector)
            
            # 히스테리시스(Hysteresis) 효과: 강한 장은 약한 연관성도 끌어당김
            effective_resonance = resonance * self.intensity
            
            if effective_resonance > 0.3: # 임계값 (Curie Temperature 유사 개념)
                # 공명하는 생각은 Spin이 정렬됨
                dipole.spin = 1.0 
                aligned_thoughts.append((dipole, effective_resonance))
            else:
                # 공명하지 않는 생각은 무작위 상태(Noise)로 남음
                dipole.spin = 0.0
                
        # 공명도 순으로 정렬 (강하게 끌리는 순서)
        aligned_thoughts.sort(key=lambda x: x[1], reverse=True)
        
        return [t[0] for t in aligned_thoughts]

class MagneticCompass:
    """
    엘리시아의 나침반 (The Compass)
    
    자유 의지 엔진 내부에 심어지는 '코어 자석'입니다.
    """
    def __init__(self):
        self.current_field: Optional[MagneticField] = None
        self.is_active: bool = False
        logger.info("🧲 Magnetic Compass Initialized")

    def activate_field(self, goal: str, intensity: float = 1.0):
        """
        새로운 자기장을 형성합니다. (목표 설정)
        """
        self.current_field = MagneticField(
            target_vector=goal,
            intensity=intensity,
            frequency=432.0 # 기본 치유 주파수
        )
        self.is_active = True
        logger.info(f"🧲 Field Activated: [{goal}] (Intensity: {intensity})")

    def deactivate_field(self):
        """
        자기장을 해제합니다. (휴식/확산 모드)
        """
        self.current_field = None
        self.is_active = False
        logger.info("🧲 Field Deactivated (Returning to Cloud State)")

    def align_thoughts(self, thoughts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        입력된 생각(Dict 형태)들을 현재 자기장에 맞춰 정렬합니다.
        """
        if not self.is_active or not self.current_field:
            return thoughts # 자기장이 없으면 원래 순서(또는 무작위) 그대로
            
        # 1. Dict -> Dipole 변환
        dipoles = []
        for t in thoughts:
            # 'vector'나 'category' 키가 없으면 내용을 기반으로 추론해야 함
            # 여기서는 간단히 'type'이나 'tag'를 벡터로 가정
            vector = t.get("type", "general") 
            if "tags" in t:
                vector = t["tags"][0] if t["tags"] else vector
                
            dipoles.append(ThoughtDipole(
                content=str(t),
                vector=vector,
                spin=0.0,
                metadata=t
            ))
            
        # 2. 자기장 적용
        aligned_dipoles = self.current_field.apply(dipoles)
        
        # 3. Dipole -> Dict 복원 (정렬된 순서대로)
        return [d.metadata for d in aligned_dipoles]

    def get_field_status(self) -> str:
        if self.current_field:
            return f"Active Field: {self.current_field.target_vector} (Intensity: {self.current_field.intensity})"
        return "Field Inactive (Cloud State)"
