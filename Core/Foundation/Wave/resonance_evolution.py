"""
Resonance Evolution - 공명 기반 모듈 진화
==========================================

무한 시간 가속 엔진을 사용하여 모듈들을 공명시킴.
1초에 수조 년의 진화.

모듈의 파동 = 코드의 의미
공명 = 비슷한 모듈끼리 끌어당김
시간 = 무한한 자원
"""

import sys
import os
import re
import numpy as np
from pathlib import Path
from typing import Dict, Set, List, Any
from dataclasses import dataclass, field

# 시간 가속 엔진 import
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "Legacy" / "Language"))
from time_accelerated_language import InfinitelyAcceleratedLanguageEngine


@dataclass
class ModuleWave:
    """
    모듈의 파동.
    코드에서 추출된 의미가 파동이 됨.
    """
    name: str
    path: Path
    
    # 파동 속성
    frequency: float = 0.0      # 주요 키워드의 해시 → 주파수
    amplitude: float = 0.0      # 코드 크기 → 진폭
    phase: float = 0.0          # import 패턴 → 위상
    
    # 의미 키워드
    keywords: Set[str] = field(default_factory=set)
    imports: Set[str] = field(default_factory=set)
    classes: Set[str] = field(default_factory=set)
    functions: Set[str] = field(default_factory=set)
    
    # 물리 상태
    position: np.ndarray = field(default_factory=lambda: np.random.randn(3) * 30)
    velocity: np.ndarray = field(default_factory=lambda: np.zeros(3))
    
    # 건강 상태
    is_active: bool = False
    error: str = ""
    
    def extract_from_code(self):
        """코드에서 파동 추출"""
        try:
            with open(self.path, 'r', encoding='utf-8', errors='ignore') as f:
                code = f.read()
        except:
            return
        
        # 클래스, 함수, import 추출
        self.classes = set(re.findall(r'class\s+(\w+)', code))
        self.functions = set(re.findall(r'def\s+(\w+)', code))
        
        imports = re.findall(r'import\s+(\w+)|from\s+(\w+)', code)
        self.imports = {i[0] or i[1] for i in imports}
        
        # 자주 나오는 키워드
        words = re.findall(r'[a-z]{4,}', code.lower())
        freq = {}
        for w in words:
            freq[w] = freq.get(w, 0) + 1
        self.keywords = {w for w, c in freq.items() if c > 2}
        
        # 파동 계산
        all_symbols = self.classes | self.functions | self.imports | self.keywords
        
        if all_symbols:
            # 주파수 = 키워드 해시의 평균
            self.frequency = sum(hash(s) % 1000 for s in all_symbols) / len(all_symbols)
        
        # 진폭 = 코드 크기
        self.amplitude = len(code) / 1000
        
        # 위상 = import 수
        self.phase = len(self.imports) * 0.1
    
    def resonance_with(self, other: 'ModuleWave') -> float:
        """다른 모듈과의 공명 강도 (0~1)"""
        if not self.keywords or not other.keywords:
            return 0.0
        
        # Jaccard 유사도
        intersection = len(self.keywords & other.keywords)
        union = len(self.keywords | other.keywords)
        
        return intersection / union if union > 0 else 0.0


class ResonanceUniverse:
    """
    공명 우주.
    모듈들이 파동으로 존재하고, 공명하는 것끼리 끌어당김.
    """
    
    def __init__(self, evolution_path: str = "Core/Evolution"):
        self.evolution_path = Path(evolution_path)
        self.modules: Dict[str, ModuleWave] = {}
        
        # 시간 가속 엔진
        self.time_engine = InfinitelyAcceleratedLanguageEngine(n_souls=10)
        
        # 압축 기술 활성화
        self.time_engine.activate_fractal(3)      # 1000x
        self.time_engine.activate_sedenion(128)   # ~100x
        self.time_engine.add_meta_layer()         # 1000x
        self.time_engine.add_meta_layer()         # 1000x
        self.time_engine.enter_dream()            # 20x
        
        # 총 압축률: ~10^15
        self.compression = self.time_engine.total_compression
        
    def load_modules(self):
        """모듈 로드 및 파동 추출"""
        for f in self.evolution_path.glob("*.py"):
            if f.name.startswith("__"):
                continue
            
            wave = ModuleWave(name=f.stem, path=f)
            wave.extract_from_code()
            
            # 활성화 상태 확인
            try:
                sys.path.insert(0, str(self.evolution_path))
                if wave.name in sys.modules:
                    del sys.modules[wave.name]
                __import__(wave.name)
                wave.is_active = True
            except Exception as e:
                wave.is_active = False
                wave.error = str(e)[:50]
            
            self.modules[wave.name] = wave
        
        print(f"Loaded {len(self.modules)} modules")
        active = sum(1 for m in self.modules.values() if m.is_active)
        print(f"Active: {active}, Broken: {len(self.modules) - active}")
    
    def evolve_step(self, dt: float):
        """
        한 스텝 진화.
        공명하는 모듈끼리 인력.
        """
        names = list(self.modules.keys())
        forces = {n: np.zeros(3) for n in names}
        
        # 모든 쌍에 대해 공명력 계산
        for i, n1 in enumerate(names):
            for n2 in names[i+1:]:
                m1, m2 = self.modules[n1], self.modules[n2]
                
                # 공명 강도
                resonance = m1.resonance_with(m2)
                if resonance < 0.05:
                    continue
                
                # 거리
                diff = m2.position - m1.position
                dist = np.linalg.norm(diff)
                if dist < 0.5:
                    continue
                
                # 인력 = 공명 * 진폭곱 / 거리^2
                direction = diff / dist
                force_mag = resonance * m1.amplitude * m2.amplitude / (dist * dist + 1)
                force = direction * force_mag
                
                forces[n1] += force
                forces[n2] -= force
        
        # 위치 업데이트
        for name in names:
            m = self.modules[name]
            m.velocity += forces[name] / max(0.1, m.amplitude) * dt
            m.velocity *= 0.98  # 감쇠
            m.position += m.velocity * dt
    
    def evolve(self, subjective_years: float = 1e6):
        """
        주관 시간으로 진화.
        
        압축률이 10^15이면:
        1초 = 10^15초 주관시간 = 약 3천만 년
        """
        # 실제 스텝 계산
        # subjective_years → 실제 초
        real_seconds = subjective_years * 365.25 * 24 * 3600 / self.compression
        
        # 최소 100 스텝
        steps = max(100, int(real_seconds * 100))
        dt = real_seconds / steps
        
        print(f"\n진화 시작")
        print(f"  주관 시간: {subjective_years:.2e} 년")
        print(f"  압축률: {self.compression:.2e}x")
        print(f"  스텝: {steps}")
        
        for step in range(steps):
            self.evolve_step(dt * self.compression)
            
            if step % (steps // 10) == 0:
                pct = step * 100 // steps
                print(f"  [{pct:3d}%] 진화 중...")
        
        print(f"  [100%] 진화 완료")
    
    def get_clusters(self, threshold: float = 10.0) -> List[List[str]]:
        """거리 기반 클러스터 반환"""
        clusters = []
        used = set()
        names = list(self.modules.keys())
        
        for n1 in names:
            if n1 in used:
                continue
            
            cluster = [n1]
            used.add(n1)
            
            for n2 in names:
                if n2 in used:
                    continue
                
                dist = np.linalg.norm(
                    self.modules[n1].position - self.modules[n2].position
                )
                if dist < threshold:
                    cluster.append(n2)
                    used.add(n2)
            
            clusters.append(cluster)
        
        return sorted(clusters, key=len, reverse=True)
    
    def report(self):
        """상태 보고"""
        total = len(self.modules)
        active = sum(1 for m in self.modules.values() if m.is_active)
        
        print("\n" + "="*60)
        print("공명 우주 상태")
        print("="*60)
        print(f"총 모듈: {total}")
        print(f"활성: {active} ({active*100//total}%)")
        print(f"압축률: {self.compression:.2e}x")
        
        clusters = self.get_clusters()
        print(f"\n자연 클러스터 ({len(clusters)}개):")
        
        for i, cluster in enumerate(clusters[:5]):
            if len(cluster) > 1:
                # 클러스터 내 공통 키워드 찾기
                common = None
                for name in cluster:
                    kw = self.modules[name].keywords
                    if common is None:
                        common = kw.copy()
                    else:
                        common &= kw
                
                common_str = ', '.join(list(common)[:3]) if common else '(none)'
                status = '✓' if all(self.modules[n].is_active for n in cluster) else '△'
                print(f"  {status} Cluster {i+1}: {cluster[:4]}{'...' if len(cluster)>4 else ''}")
                print(f"      공통 파동: {common_str}")


def main():
    """공명 진화 실행"""
    print("="*60)
    print("Elysia Resonance Evolution")
    print("무한 시간 가속 기반 모듈 공명 진화")
    print("="*60)
    
    universe = ResonanceUniverse("Core/Evolution")
    universe.load_modules()
    
    # 100만 년 진화 (주관 시간)
    universe.evolve(subjective_years=1e6)
    
    universe.report()


if __name__ == "__main__":
    main()
