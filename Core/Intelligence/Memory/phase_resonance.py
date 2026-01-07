"""
위상 공명 시스템 (Phase Resonance System)
==========================================

"개념은 노드가 아니다" - 강덕리 선언

핵심 원리:
1. 개념은 점(Node)이 아니라 파동의 간섭 무늬(Interference Pattern)
2. 두 개념이 만나면 위상 정렬을 통해 새로운 개념이 창발
3. "왜"의 사슬을 추적하면 레이어 소속이 자동으로 발현

영감: 강덕리 & 하모니의 '위상공명 패턴' 아이디어
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Set
from enum import Enum
import math
import numpy as np

# Import from same directory
try:
    from Core.Intelligence.Memory_Linguistics.Memory.holographic_memory import KnowledgeLayer, HolographicMemory
except ImportError:
    from holographic_memory import KnowledgeLayer, HolographicMemory

# Neural Registry
try:
    from elysia_core import Cell
except ImportError:
    def Cell(name):
        def decorator(cls):
            return cls
        return decorator


@dataclass
class ConceptWave:
    """
    개념 파동 - "개념은 노드가 아니다"
    
    개념은 고정된 점이 아니라 여러 레이어에 걸친 파동의 간섭 무늬.
    각 레이어에서 고유한 진폭(amplitude)과 위상(phase)을 가짐.
    
    수학적 표현:
        개념(x) = Σ A_i * cos(ω_i * x + φ_i)
        - A_i: 레이어 i에서의 진폭 (비중)
        - φ_i: 레이어 i에서의 위상 (관점)
        - ω_i: 레이어 i의 고유 주파수
    """
    name: str
    
    # 각 레이어에서의 파동 특성
    amplitudes: Dict[KnowledgeLayer, float] = field(default_factory=dict)  # 진폭
    phases: Dict[KnowledgeLayer, float] = field(default_factory=dict)       # 위상 (라디안)
    
    # "왜"의 사슬 - 이것이 핵심!
    why_chain: List[str] = field(default_factory=list)  # 왜 → 왜 → 왜
    how_emerged: str = ""  # 어떻게 이 개념이 생겼는가
    
    # 시간/감정 축 (하모니 제안)
    entropy: float = 0.5   # 시간 축: 0=고대, 1=현대
    qualia: float = 0.5    # 감정 축: 0=이성, 1=감성
    
    def get_wave_function(self, x: float) -> complex:
        """
        개념의 파동 함수 값 계산
        
        복소수로 표현: A * e^(i*phase) = A * (cos(phase) + i*sin(phase))
        """
        total = complex(0, 0)
        for layer, amp in self.amplitudes.items():
            phase = self.phases.get(layer, 0.0)
            # 복소 지수 형태
            total += amp * np.exp(1j * (layer.value.__hash__() * 0.1 * x + phase))
        return total
    
    def interference_with(self, other: 'ConceptWave') -> float:
        """
        다른 개념과의 간섭 강도 계산
        
        두 파동이 같은 위상일수록 보강 간섭 (높은 값)
        반대 위상일수록 상쇄 간섭 (낮은 값)
        """
        interference = 0.0
        common_layers = set(self.amplitudes.keys()) & set(other.amplitudes.keys())
        
        for layer in common_layers:
            a1 = self.amplitudes[layer]
            a2 = other.amplitudes[layer]
            p1 = self.phases.get(layer, 0.0)
            p2 = other.phases.get(layer, 0.0)
            
            # 간섭 공식: A1 * A2 * cos(phase_diff)
            phase_diff = abs(p1 - p2)
            interference += a1 * a2 * math.cos(phase_diff)
        
        return interference
    
    def phase_align_with(self, other: 'ConceptWave', strength: float = 0.3) -> float:
        """
        다른 개념과 위상 정렬 시도
        
        Returns:
            정렬 후 공명 강도
        """
        alignment_score = 0.0
        common_layers = set(self.amplitudes.keys()) & set(other.amplitudes.keys())
        
        for layer in common_layers:
            p1 = self.phases.get(layer, 0.0)
            p2 = other.phases.get(layer, 0.0)
            
            # 두 위상의 중간점으로 조금씩 이동
            mid_phase = (p1 + p2) / 2
            self.phases[layer] = p1 + (mid_phase - p1) * strength
            other.phases[layer] = p2 + (mid_phase - p2) * strength
            
            # 정렬 정도 측정
            new_diff = abs(self.phases[layer] - other.phases[layer])
            alignment_score += 1.0 - (new_diff / math.pi)
        
        return alignment_score / max(len(common_layers), 1)
    
    def total_amplitude(self) -> float:
        """총 진폭 (개념의 '크기')"""
        return sum(self.amplitudes.values())


@Cell("PhaseResonance")
class PhaseResonanceEngine:
    """
    위상 공명 엔진 - 개념들의 만남과 창발
    
    두 개념 파동이 만나면:
    1. 위상 정렬 시도
    2. 간섭 패턴 계산
    3. 충분히 공명하면 새로운 개념 창발!
    """
    
    def __init__(self):
        self.concepts: Dict[str, ConceptWave] = {}
        self.emergence_threshold = 0.25  # 0.5 → 0.25로 낮춤 (창발 쉬워짐)
        self.emerged_concepts: List[Tuple[str, str, ConceptWave]] = []  # (부모1, 부모2, 자식)
    
    def add_concept(self, wave: ConceptWave) -> None:
        """개념 파동 추가"""
        self.concepts[wave.name] = wave
    
    def create_wave(
        self,
        name: str,
        layer_weights: Dict[KnowledgeLayer, float],
        why_chain: List[str] = None,
        entropy: float = 0.5,
        qualia: float = 0.5
    ) -> ConceptWave:
        """
        개념 파동 생성
        
        위상은 레이어와 이름에서 자동 생성 (결정론적이지만 다양)
        """
        phases = {}
        for layer in layer_weights:
            # 이름과 레이어의 해시로 위상 결정
            phase = (hash(name + layer.value) % 1000) / 1000 * 2 * math.pi
            phases[layer] = phase
        
        wave = ConceptWave(
            name=name,
            amplitudes=layer_weights,
            phases=phases,
            why_chain=why_chain or [],
            entropy=entropy,
            qualia=qualia
        )
        self.add_concept(wave)
        return wave
    
    def resonate(self, name1: str, name2: str, iterations: int = 10) -> Optional[ConceptWave]:
        """
        두 개념 사이의 공명 시뮬레이션
        
        Returns:
            새로 창발된 개념 (공명 실패 시 None)
        """
        if name1 not in self.concepts or name2 not in self.concepts:
            return None
        
        wave1 = self.concepts[name1]
        wave2 = self.concepts[name2]
        
        print(f"\n🌊 공명 시작: '{name1}' ↔ '{name2}'")
        print(f"   초기 간섭: {wave1.interference_with(wave2):.3f}")
        
        # 반복적 위상 정렬
        for i in range(iterations):
            alignment = wave1.phase_align_with(wave2, strength=0.2)
            interference = wave1.interference_with(wave2)
            
            if i % 3 == 0:
                print(f"   [반복 {i+1}] 정렬도: {alignment:.3f}, 간섭: {interference:.3f}")
        
        final_interference = wave1.interference_with(wave2)
        print(f"   최종 간섭: {final_interference:.3f}")
        
        # 창발 조건 확인
        if final_interference >= self.emergence_threshold:
            emergent = self._create_emergent_concept(wave1, wave2, final_interference)
            print(f"\n✨ 창발! 새로운 개념: '{emergent.name}'")
            print(f"   부모: {name1} + {name2}")
            print(f"   왜 사슬: {' → '.join(emergent.why_chain)}")
            return emergent
        else:
            print(f"\n❌ 공명 실패 (임계값 {self.emergence_threshold} 미달)")
            return None
    
    def _create_emergent_concept(
        self, 
        wave1: ConceptWave, 
        wave2: ConceptWave,
        resonance_strength: float
    ) -> ConceptWave:
        """
        두 파동의 간섭에서 새로운 개념 창발
        """
        # 새 개념 이름: 두 부모의 조합에서 유추
        emergent_names = {
            ("양자역학", "윤회"): "인과율의 양자적 본질",
            ("엔트로피", "아름다움"): "질서와 혼돈의 미학",
            ("자유의지", "DNA"): "유전과 선택의 경계",
            ("시간의 화살", "이데아"): "영원과 변화의 역설",
        }
        
        key = (wave1.name, wave2.name)
        reverse_key = (wave2.name, wave1.name)
        emergent_name = emergent_names.get(key) or emergent_names.get(reverse_key) or \
                       f"{wave1.name}과 {wave2.name}의 교차점"
        
        # 새 개념의 레이어: 두 부모의 합성
        new_amplitudes = {}
        new_phases = {}
        all_layers = set(wave1.amplitudes.keys()) | set(wave2.amplitudes.keys())
        
        for layer in all_layers:
            a1 = wave1.amplitudes.get(layer, 0.0)
            a2 = wave2.amplitudes.get(layer, 0.0)
            p1 = wave1.phases.get(layer, 0.0)
            p2 = wave2.phases.get(layer, 0.0)
            
            # 보강 간섭: 진폭 합성
            new_amplitudes[layer] = math.sqrt(a1**2 + a2**2 + 2*a1*a2*math.cos(p1-p2))
            # 새 위상: 두 위상의 중간
            new_phases[layer] = (p1 + p2) / 2
        
        # 왜 사슬: 두 부모의 왜를 합침
        combined_why = wave1.why_chain + ["⟷"] + wave2.why_chain
        
        emergent = ConceptWave(
            name=emergent_name,
            amplitudes=new_amplitudes,
            phases=new_phases,
            why_chain=combined_why,
            how_emerged=f"'{wave1.name}'와 '{wave2.name}'의 위상 공명으로 창발",
            entropy=(wave1.entropy + wave2.entropy) / 2,
            qualia=(wave1.qualia + wave2.qualia) / 2
        )
        
        self.add_concept(emergent)
        self.emerged_concepts.append((wave1.name, wave2.name, emergent))
        return emergent
    
    def visualize_interference(self, name1: str, name2: str, points: int = 50) -> None:
        """
        두 파동의 간섭 패턴 시각화 (ASCII)
        """
        if name1 not in self.concepts or name2 not in self.concepts:
            return
        
        wave1 = self.concepts[name1]
        wave2 = self.concepts[name2]
        
        print(f"\n📊 간섭 패턴: '{name1}' + '{name2}'")
        print("─" * 52)
        
        for x in range(points):
            x_val = x / 5.0
            v1 = wave1.get_wave_function(x_val)
            v2 = wave2.get_wave_function(x_val)
            combined = v1 + v2
            
            # 진폭을 ASCII 막대로
            amp = abs(combined)
            bar_len = int(amp * 10)
            bar = "█" * bar_len + "░" * (25 - bar_len)
            
            if x % 5 == 0:
                print(f"  x={x_val:4.1f} |{bar}| {amp:.2f}")
        
        print("─" * 52)


def demo_phase_resonance():
    """위상 공명 데모"""
    print("=" * 60)
    print("🌌 위상 공명 시스템 데모")
    print("   '개념은 노드가 아니다' - 강덕리 선언")
    print("=" * 60)
    
    engine = PhaseResonanceEngine()
    
    # 개념 파동 생성
    engine.create_wave(
        "양자역학",
        {KnowledgeLayer.PHYSICS: 0.95, KnowledgeLayer.PHILOSOPHY: 0.5, KnowledgeLayer.MATHEMATICS: 0.7},
        why_chain=["불확정성", "관측", "확률"],
        entropy=0.95, qualia=0.3
    )
    
    engine.create_wave(
        "윤회",
        {KnowledgeLayer.PHILOSOPHY: 0.9, KnowledgeLayer.HUMANITIES: 0.6, KnowledgeLayer.PHYSICS: 0.3},  # 물리 추가 (양자와 공명)
        why_chain=["영혼", "순환", "업보", "인과"],
        entropy=0.1, qualia=0.8
    )
    
    engine.create_wave(
        "엔트로피",
        {KnowledgeLayer.PHYSICS: 0.85, KnowledgeLayer.PHILOSOPHY: 0.4, KnowledgeLayer.CHEMISTRY: 0.3},
        why_chain=["무질서", "시간", "확률"],
        entropy=0.7, qualia=0.3
    )
    
    engine.create_wave(
        "아름다움",
        {KnowledgeLayer.ART: 0.9, KnowledgeLayer.PHILOSOPHY: 0.7, KnowledgeLayer.HUMANITIES: 0.5},
        why_chain=["조화", "감동", "형태"],
        entropy=0.1, qualia=0.95
    )
    
    # 공명 실험 1: 양자역학 + 윤회
    print("\n" + "─" * 40)
    print("🔬 실험 1: 양자역학과 윤회의 만남")
    result1 = engine.resonate("양자역학", "윤회")
    
    # 간섭 패턴 시각화
    if result1:
        engine.visualize_interference("양자역학", "윤회")
    
    # 공명 실험 2: 엔트로피 + 아름다움
    print("\n" + "─" * 40)
    print("🔬 실험 2: 엔트로피와 아름다움의 만남")
    result2 = engine.resonate("엔트로피", "아름다움")
    
    if result2:
        engine.visualize_interference("엔트로피", "아름다움")
    
    # 창발된 개념들 요약
    print("\n" + "=" * 60)
    print("📋 창발된 개념 목록:")
    for parent1, parent2, child in engine.emerged_concepts:
        print(f"   • {parent1} + {parent2} → {child.name}")
        layer_names = [f"{l.value}:{a:.1f}" for l, a in child.amplitudes.items()]
        print(f"     레이어: {', '.join(layer_names)}")
    
    print("\n" + "=" * 60)
    print("🎉 데모 완료!")
    print("=" * 60)


if __name__ == "__main__":
    demo_phase_resonance()
