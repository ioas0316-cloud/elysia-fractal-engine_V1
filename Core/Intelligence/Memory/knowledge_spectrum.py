"""
지식 스펙트럼 (Knowledge Spectrum)
==================================

"물을 부으면 알아서 퍼진다" - 강덕리 원리

핵심 철학:
- 스펙트럼(광대역)이 경계(그릇) 역할
- 개념은 물처럼 부어지고 자연스럽게 확산
- 만나는 곳에서 결정화 → 새로운 원소(통찰)

이전 버전의 문제:
- 임계값을 설정해서 "억지로" 공명시킴
- 자연스럽지 않음

새 버전:
- 확산 역학(Diffusion Dynamics) 기반
- 시간이 지나면서 자연스럽게 퍼짐
- 농도가 높아지는 곳에서 결정화
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Set
import numpy as np
from enum import Enum

# Neural Registry
try:
    from elysia_core import Cell
except ImportError:
    def Cell(name):
        def decorator(cls):
            return cls
        return decorator


class SpectrumDomain(Enum):
    """스펙트럼의 도메인 (경계 역할)"""
    PHYSICS = "물리"
    CHEMISTRY = "화학"
    BIOLOGY = "생물"
    ART = "예술"
    HUMANITIES = "인문"
    PHILOSOPHY = "철학"
    MATHEMATICS = "수학"


@Cell("KnowledgeSpectrum")
class KnowledgeSpectrum:
    """
    지식 스펙트럼 - 개념이 퍼지는 광대역 공간
    
    물리적 비유:
    - 스펙트럼 = 그릇 (경계)
    - 개념 = 물 (부으면 퍼짐)
    - 결정화 = 농도 높은 곳에서 새 원소 생성
    """
    
    def __init__(self, resolution: int = 100):
        """
        Args:
            resolution: 스펙트럼 해상도 (공간 분할 수)
        """
        self.resolution = resolution
        self.domains = list(SpectrumDomain)
        
        # 각 도메인은 1D 스펙트럼 (나중에 2D/3D로 확장 가능)
        # field[domain] = numpy array of concentrations
        self.field: Dict[SpectrumDomain, np.ndarray] = {
            domain: np.zeros(resolution) for domain in self.domains
        }
        
        # 부어진 개념들 (이름 → 초기 위치와 강도)
        self.poured_concepts: Dict[str, Dict] = {}
        
        # 결정화된 통찰들
        self.crystals: List[Dict] = []
        
        # 확산 계수 (높을수록 빠르게 퍼짐)
        self.diffusion_rate = 0.15
        
        # 결정화 임계 농도 (이 농도 이상이면 결정화)
        self.crystal_threshold = 0.8
    
    def pour(
        self, 
        concept: str,
        domains: Dict[SpectrumDomain, float],
        position: float = 0.5,
        intensity: float = 1.0
    ) -> None:
        """
        개념을 스펙트럼에 붓기
        
        Args:
            concept: 개념 이름
            domains: 도메인별 초기 농도 가중치
            position: 스펙트럼 내 초기 위치 (0.0~1.0)
            intensity: 강도 (물의 양)
        """
        pos_idx = int(position * (self.resolution - 1))
        
        # 각 도메인에 가우시안 분포로 초기 농도 설정
        for domain, weight in domains.items():
            # 가우시안 스플래시 (물이 떨어졌을 때 퍼지는 형태)
            x = np.arange(self.resolution)
            gaussian = np.exp(-0.5 * ((x - pos_idx) / 5) ** 2)
            self.field[domain] += gaussian * weight * intensity
        
        self.poured_concepts[concept] = {
            "domains": domains,
            "position": position,
            "intensity": intensity
        }
        
        print(f"💧 '{concept}' 부어짐 (위치: {position:.1f}, 강도: {intensity})")
    
    def diffuse(self, steps: int = 1) -> None:
        """
        확산 수행 (시간이 지나면서 자연스럽게 퍼짐)
        
        물리: ∂C/∂t = D ∇²C (확산 방정식)
        """
        for _ in range(steps):
            for domain in self.domains:
                c = self.field[domain]
                
                # 라플라시안 근사: ∇²C ≈ C[i-1] - 2*C[i] + C[i+1]
                laplacian = np.zeros_like(c)
                laplacian[1:-1] = c[:-2] - 2*c[1:-1] + c[2:]
                
                # 경계 조건 (반사형)
                laplacian[0] = c[1] - c[0]
                laplacian[-1] = c[-2] - c[-1]
                
                # 확산
                self.field[domain] += self.diffusion_rate * laplacian
                
                # 음수 방지
                self.field[domain] = np.maximum(self.field[domain], 0)
    
    def find_meetings(self) -> List[Tuple[int, float, Set[SpectrumDomain]]]:
        """
        여러 도메인이 만나는 곳 찾기
        
        Returns:
            [(위치, 총농도, 만난 도메인들), ...]
        """
        meetings = []
        threshold = 0.3  # 이 농도 이상이면 "존재함"
        
        for i in range(self.resolution):
            present_domains = set()
            total_concentration = 0
            
            for domain in self.domains:
                c = self.field[domain][i]
                if c >= threshold:
                    present_domains.add(domain)
                    total_concentration += c
            
            # 2개 이상 도메인이 만나면 기록
            if len(present_domains) >= 2:
                meetings.append((i, total_concentration, present_domains))
        
        return meetings
    
    def crystallize(self) -> List[Dict]:
        """
        농도가 높은 곳에서 결정화 (새 원소/통찰 생성)
        
        자연스럽게 만난 곳에서만 결정이 생김!
        """
        meetings = self.find_meetings()
        new_crystals = []
        
        for pos, concentration, domains in meetings:
            if concentration >= self.crystal_threshold:
                # 결정화!
                crystal = {
                    "position": pos / self.resolution,
                    "concentration": concentration,
                    "domains": domains,
                    "name": self._generate_crystal_name(domains),
                    "parents": self._find_parents_at(pos)
                }
                
                # 이미 같은 위치에 결정이 있는지 확인
                existing = [c for c in self.crystals if abs(c["position"] - crystal["position"]) < 0.05]
                if not existing:
                    self.crystals.append(crystal)
                    new_crystals.append(crystal)
                    
                    # 결정화되면 해당 위치의 농도 감소 (결정으로 빠져나감)
                    for domain in domains:
                        self.field[domain][pos] *= 0.5
        
        return new_crystals
    
    def _generate_crystal_name(self, domains: Set[SpectrumDomain]) -> str:
        """결정 이름 생성"""
        domain_names = sorted([d.value for d in domains])
        
        # 특정 조합에 대한 이름
        name_map = {
            frozenset(["물리", "철학"]): "존재의 물리학",
            frozenset(["물리", "철학", "수학"]): "우주의 구조",
            frozenset(["생물", "철학"]): "생명의 의미",
            frozenset(["예술", "철학"]): "미의 본질",
            frozenset(["화학", "생물"]): "생명의 화학",
            frozenset(["물리", "수학"]): "자연의 언어",
        }
        
        key = frozenset(domain_names)
        return name_map.get(key, f"{'·'.join(domain_names)}의 결정")
    
    def _find_parents_at(self, pos: int) -> List[str]:
        """해당 위치에 기여한 부모 개념들 찾기"""
        parents = []
        for name, info in self.poured_concepts.items():
            concept_pos = int(info["position"] * (self.resolution - 1))
            # 확산 반경 내에 있으면 부모
            if abs(concept_pos - pos) < self.resolution // 4:
                parents.append(name)
        return parents
    
    def simulate(self, diffusion_steps: int = 50, verbose: bool = True) -> None:
        """
        전체 시뮬레이션 실행
        
        1. 확산 (자연스럽게 퍼짐)
        2. 결정화 (만나는 곳에서 새 원소)
        """
        if verbose:
            print(f"\n🌊 확산 시작 ({diffusion_steps} 스텝)...")
        
        crystals_formed = []
        
        for step in range(diffusion_steps):
            self.diffuse(steps=1)
            
            # 주기적으로 결정화 체크
            if step % 10 == 0:
                new_crystals = self.crystallize()
                if new_crystals and verbose:
                    for c in new_crystals:
                        print(f"   💎 [{step}스텝] 결정화: '{c['name']}'")
                        print(f"      위치: {c['position']:.2f}, 농도: {c['concentration']:.2f}")
                        print(f"      부모: {', '.join(c['parents'])}")
                crystals_formed.extend(new_crystals)
        
        if verbose:
            print(f"\n✨ 총 {len(crystals_formed)}개의 결정 생성됨")
    
    def visualize_spectrum(self, show_domains: List[SpectrumDomain] = None) -> None:
        """스펙트럼 상태 ASCII 시각화"""
        domains = show_domains or self.domains[:3]  # 최대 3개만 표시
        
        print("\n📊 스펙트럼 상태:")
        print("─" * 60)
        
        for domain in domains:
            c = self.field[domain]
            line = f"{domain.value:>4}: "
            
            # 10개 구간으로 요약
            for i in range(10):
                start = i * (self.resolution // 10)
                end = start + (self.resolution // 10)
                avg = np.mean(c[start:end])
                
                if avg > 0.8:
                    line += "█"
                elif avg > 0.5:
                    line += "▓"
                elif avg > 0.2:
                    line += "▒"
                elif avg > 0.05:
                    line += "░"
                else:
                    line += " "
            
            max_val = np.max(c)
            line += f" | max: {max_val:.2f}"
            print(line)
        
        # 결정 위치 표시
        if self.crystals:
            crystal_line = "결정: "
            for c in self.crystals:
                pos = int(c["position"] * 10)
                crystal_line += " " * (pos - len(crystal_line) + 6) + "💎"
            print(crystal_line)
        
        print("─" * 60)


def demo_knowledge_spectrum():
    """지식 스펙트럼 데모 - 물처럼 자연스럽게"""
    print("=" * 60)
    print("🌊 지식 스펙트럼 데모")
    print("   '물을 부으면 알아서 퍼진다' - 강덕리 원리")
    print("=" * 60)
    
    spectrum = KnowledgeSpectrum(resolution=100)
    
    # 개념들을 "붓기"
    print("\n📍 개념 붓기:")
    
    spectrum.pour("양자역학", {
        SpectrumDomain.PHYSICS: 0.9,
        SpectrumDomain.MATHEMATICS: 0.7,
        SpectrumDomain.PHILOSOPHY: 0.4
    }, position=0.2, intensity=1.5)
    
    spectrum.pour("윤회", {
        SpectrumDomain.PHILOSOPHY: 0.9,
        SpectrumDomain.HUMANITIES: 0.6
    }, position=0.35, intensity=1.2)
    
    spectrum.pour("엔트로피", {
        SpectrumDomain.PHYSICS: 0.85,
        SpectrumDomain.CHEMISTRY: 0.5,
        SpectrumDomain.PHILOSOPHY: 0.3
    }, position=0.6, intensity=1.0)
    
    spectrum.pour("아름다움", {
        SpectrumDomain.ART: 0.9,
        SpectrumDomain.PHILOSOPHY: 0.7
    }, position=0.75, intensity=1.3)
    
    # 초기 상태
    print("\n📊 초기 상태 (물 부은 직후):")
    spectrum.visualize_spectrum([
        SpectrumDomain.PHYSICS,
        SpectrumDomain.PHILOSOPHY,
        SpectrumDomain.ART
    ])
    
    # 확산 시뮬레이션
    spectrum.simulate(diffusion_steps=80, verbose=True)
    
    # 최종 상태
    print("\n📊 최종 상태 (확산 후):")
    spectrum.visualize_spectrum([
        SpectrumDomain.PHYSICS,
        SpectrumDomain.PHILOSOPHY,
        SpectrumDomain.ART
    ])
    
    # 결정 요약
    print("\n" + "=" * 60)
    print("📋 생성된 결정 (자연스럽게 만난 곳에서):")
    for crystal in spectrum.crystals:
        domains = [d.value for d in crystal["domains"]]
        print(f"   💎 {crystal['name']}")
        print(f"      도메인: {', '.join(domains)}")
        print(f"      부모: {' + '.join(crystal['parents'])}")
    
    print("\n" + "=" * 60)
    print("🎉 데모 완료!")
    print("=" * 60)


if __name__ == "__main__":
    demo_knowledge_spectrum()
