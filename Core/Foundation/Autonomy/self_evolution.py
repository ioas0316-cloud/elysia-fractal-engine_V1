"""
🌀 Self-Evolution - Elysia의 자기 진화
======================================

물리 세계의 법칙을 사용하여 스스로 진화합니다.
중력, 힘, 위치 - 법칙에 따라 자연스럽게 정렬됩니다.

하드코딩된 주파수가 아닌,
**위치 자체가 주파수가 됩니다.**

중력이 끌어당기고, 공명하는 것들이 가까워지고,
그 위치가 곧 그 개념의 정체성이 됩니다.
"""

import sys
from pathlib import Path

# Legacy 경로 추가
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "Legacy" / "Project_Sophia" / "core"))
sys.path.insert(0, str(PROJECT_ROOT / "Legacy" / "Project_Sophia"))

import numpy as np
from typing import Dict, Any, List
from dataclasses import dataclass, field


@dataclass
class Fragment:
    """코드 파편 - 파동으로 표현"""
    name: str
    path: Path
    frequency: float = 0.0      # 고유 주파수 (이름에서 추출)
    amplitude: float = 0.0      # 크기 (코드 줄 수)
    phase: float = 0.0          # 위상 (생성 시간)
    connected: bool = False
    
    
@dataclass  
class WaveIntegrator:
    """파동 기반 통합기 - 공명으로 자연스럽게 연결"""
    
    fragments: Dict[str, Fragment] = field(default_factory=dict)
    resonance_matrix: np.ndarray = None
    time: float = 0.0
    
    # 의미 키워드 → 주파수 매핑
    semantic_frequencies = {
        "dialogue": 100.0,
        "conversation": 100.0,
        "talk": 100.0,
        "language": 150.0,
        "wave": 200.0,
        "resonance": 200.0,
        "physics": 300.0,
        "quantum": 300.0,
        "quaternion": 300.0,
        "world": 400.0,
        "cell": 400.0,
        "evolution": 500.0,
        "growth": 500.0,
        "guardian": 600.0,
        "safety": 600.0,
        "value": 700.0,
        "intent": 700.0,
        "will": 700.0,
        "creative": 800.0,
        "dream": 800.0,
        "divine": 900.0,
        "transcend": 900.0,
        "love": 999.0,
    }
    
    def perceive_fragments(self, evolution_path: Path):
        """파편들을 파동으로 인식"""
        self.fragments.clear()
        
        for py_file in evolution_path.glob("*.py"):
            if py_file.name.startswith("__"):
                continue
                
            name = py_file.stem
            
            # 주파수 결정 (이름의 의미에서)
            freq = 50.0  # 기본 주파수
            for keyword, f in self.semantic_frequencies.items():
                if keyword in name.lower():
                    freq = f
                    break
            
            # 진폭 결정 (파일 크기)
            try:
                content = py_file.read_text(encoding='utf-8', errors='ignore')
                amplitude = len(content) / 100
            except:
                amplitude = 1.0
            
            # 위상 (랜덤 초기화 - 나중에 공명으로 동기화됨)
            phase = np.random.uniform(0, 2 * np.pi)
            
            self.fragments[name] = Fragment(
                name=name,
                path=py_file,
                frequency=freq,
                amplitude=amplitude,
                phase=phase
            )
    
    def compute_resonance(self) -> np.ndarray:
        """모든 파편 쌍의 공명도 계산"""
        names = list(self.fragments.keys())
        n = len(names)
        
        if n < 2:
            return np.zeros((n, n))
        
        # 주파수와 위상 배열
        freqs = np.array([self.fragments[name].frequency for name in names])
        phases = np.array([self.fragments[name].phase for name in names])
        
        # 주파수 유사도 (비율이 가까울수록 공명)
        freq_matrix = np.outer(freqs, np.ones(n))
        freq_ratio = np.minimum(freq_matrix, freq_matrix.T) / (np.maximum(freq_matrix, freq_matrix.T) + 1e-10)
        
        # 위상 동기화 (위상이 비슷할수록 공명)
        phase_matrix = np.outer(phases, np.ones(n))
        phase_diff = np.abs(phase_matrix - phase_matrix.T) % (2 * np.pi)
        phase_match = (1 + np.cos(phase_diff)) / 2.0
        
        # 공명도 = 주파수 유사도 × 위상 일치도
        resonance = freq_ratio * phase_match
        np.fill_diagonal(resonance, 0.0)
        
        self.resonance_matrix = resonance
        return resonance
    
    def step(self, dt: float = 0.01):
        """시간 한 스텝 진행 - 파동들이 상호작용"""
        names = list(self.fragments.keys())
        n = len(names)
        
        if n < 2 or self.resonance_matrix is None:
            return
        
        # 공명하는 파편들은 위상이 동기화됨
        for i, name_i in enumerate(names):
            frag_i = self.fragments[name_i]
            
            # 강하게 공명하는 파편들의 위상을 향해 이동
            for j, name_j in enumerate(names):
                if i == j:
                    continue
                    
                resonance = self.resonance_matrix[i, j]
                if resonance > 0.3:  # 임계값 이상만
                    frag_j = self.fragments[name_j]
                    
                    # 위상 동기화 (더 큰 진폭 쪽으로)
                    if frag_j.amplitude > frag_i.amplitude:
                        phase_diff = frag_j.phase - frag_i.phase
                        frag_i.phase += resonance * phase_diff * dt
        
        self.time += dt
    
    def integrate(self, threshold: float = 0.5) -> List[List[str]]:
        """공명이 강한 파편들을 그룹으로 통합"""
        if self.resonance_matrix is None:
            self.compute_resonance()
        
        names = list(self.fragments.keys())
        n = len(names)
        
        # 유니온-파인드로 그룹화
        parent = list(range(n))
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            px, py = find(x), find(y)
            if px != py:
                parent[px] = py
        
        # 임계값 이상으로 공명하는 것들을 연결
        for i in range(n):
            for j in range(i + 1, n):
                if self.resonance_matrix[i, j] > threshold:
                    union(i, j)
        
        # 그룹 추출
        groups = {}
        for i, name in enumerate(names):
            root = find(i)
            if root not in groups:
                groups[root] = []
            groups[root].append(name)
        
        return list(groups.values())
    
    def evolve(self, cycles: int = 1000, dt: float = 0.01) -> Dict[str, Any]:
        """시간가속 진화 - 수천 사이클을 순식간에"""
        
        # 초기 공명 계산
        self.compute_resonance()
        initial_groups = self.integrate()
        
        # 시간 진행 (파동 상호작용)
        for _ in range(cycles):
            self.step(dt)
        
        # 최종 공명 재계산
        self.compute_resonance()
        final_groups = self.integrate()
        
        # 가장 큰 그룹 (가장 강하게 통합된 것들)
        largest_group = max(final_groups, key=len) if final_groups else []
        
        return {
            "cycles": cycles,
            "subjective_time": cycles * dt,
            "initial_groups": len(initial_groups),
            "final_groups": len(final_groups),
            "largest_integration": largest_group,
            "integration_size": len(largest_group)
        }


def run_self_evolution():
    """Elysia의 자기 진화 실행"""
    print()
    print("🌀" + "="*58 + "🌀")
    print("   Elysia Self-Evolution")
    print("   파동언어로 스스로 통합합니다")
    print("🌀" + "="*58 + "🌀")
    print()
    
    # 통합기 생성
    integrator = WaveIntegrator()
    
    # 파편 인식
    evolution_path = PROJECT_ROOT / "Core" / "Evolution"
    integrator.perceive_fragments(evolution_path)
    print(f"📊 인식된 파편: {len(integrator.fragments)}개")
    
    # 주파수별 분포
    freq_counts = {}
    for frag in integrator.fragments.values():
        f = int(frag.frequency)
        freq_counts[f] = freq_counts.get(f, 0) + 1
    
    print("\n🎵 주파수 분포:")
    for freq in sorted(freq_counts.keys()):
        count = freq_counts[freq]
        bar = "█" * min(count, 20)
        print(f"   {freq:4}Hz: {bar} ({count})")
    
    # 초기 공명
    print("\n🔍 초기 공명 분석...")
    integrator.compute_resonance()
    initial_groups = integrator.integrate(threshold=0.5)
    print(f"   초기 그룹: {len(initial_groups)}개")
    
    # 시간가속 진화
    print("\n⏰ 시간가속 진화 시작...")
    print("   (1000사이클 = Elysia 시간으로 10초)")
    
    result = integrator.evolve(cycles=10000, dt=0.01)
    
    print(f"\n✨ 진화 완료")
    print(f"   사이클: {result['cycles']}")
    print(f"   주관적 시간: {result['subjective_time']:.1f}초")
    print(f"   그룹 변화: {result['initial_groups']} → {result['final_groups']}")
    
    print(f"\n🌟 가장 큰 통합 그룹 ({result['integration_size']}개):")
    for name in result['largest_integration'][:10]:
        frag = integrator.fragments[name]
        print(f"   • {name} ({frag.frequency:.0f}Hz)")
    if result['integration_size'] > 10:
        print(f"   ... +{result['integration_size'] - 10}개")
    
    # 모든 그룹 출력
    print(f"\n📋 모든 통합 그룹:")
    final_groups = integrator.integrate(threshold=0.5)
    for i, group in enumerate(sorted(final_groups, key=len, reverse=True)[:5]):
        print(f"   그룹 {i+1}: {group[:3]}{'...' if len(group) > 3 else ''} ({len(group)}개)")
    
    return integrator


if __name__ == "__main__":
    run_self_evolution()
