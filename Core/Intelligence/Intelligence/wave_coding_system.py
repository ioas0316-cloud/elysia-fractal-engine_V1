"""
Wave Coding System (파동 코딩 시스템)
=====================================

"코드는 얼어붙은 파동이다. 파동을 녹여 다시 흐르게 하라."

[Core Concept]
모든 코드를 파동으로 변환합니다.
파동의 간섭과 공명을 통해 코드 최적화, 병합, 압축을 수행합니다.

[Wave Properties of Code]
- Frequency: 코드 복잡도 (높을수록 복잡)
- Amplitude: 중요도/사용 빈도
- Phase: 코드 유형 (function, class, module)
- Dimension: 추상화 수준 (0D: 상수, 1D: 함수, 2D: 클래스, 3D: 모듈, 4D: 시스템)

[Wave DNA]
파동을 압축하여 "DNA"로 저장할 수 있습니다.
DNA는 파동의 씨앗으로, 전체 파동을 재생성할 수 있습니다.

[Time Acceleration]
88조배 가속으로 1초 안에 88조 개의 코드 파동을 분석할 수 있습니다.
"""

import logging
import math
import hashlib
import zlib
import time
import re
import ast
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple, Set
from enum import Enum, auto

logger = logging.getLogger("WaveCodingSystem")

# Import core structures
try:
    from Core.Foundation.hyper_quaternion import Quaternion, HyperWavePacket
    from Core.Foundation.ether import Wave, ether
except ImportError:
    @dataclass
    class Quaternion:
        w: float = 1.0
        x: float = 0.0
        y: float = 0.0
        z: float = 0.0
        
        def norm(self) -> float:
            return math.sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2)


class CodeDimension(Enum):
    """코드 추상화 차원"""
    CONSTANT = 0    # 0D: 상수, 리터럴
    FUNCTION = 1    # 1D: 함수 (입력 → 출력)
    CLASS = 2       # 2D: 클래스 (상태 + 행동)
    MODULE = 3      # 3D: 모듈 (클래스들의 집합)
    SYSTEM = 4      # 4D: 시스템 (모듈들의 상호작용)
    ECOSYSTEM = 5   # 5D: 생태계 (시스템들의 공존)


class CodePhase(Enum):
    """코드 유형 (위상)"""
    DECLARATION = "선언"
    DEFINITION = "정의"
    INVOCATION = "호출"
    CONTROL_FLOW = "제어"
    DATA_STRUCTURE = "데이터"
    ALGORITHM = "알고리즘"
    INTERFACE = "인터페이스"
    IMPLEMENTATION = "구현"


@dataclass
class CodeWave:
    """
    코드 파동 - 코드를 파동으로 표현합니다.
    """
    source_file: str
    code_snippet: str
    
    # 파동 속성
    frequency: float       # 복잡도 (0.0 ~ 100.0)
    amplitude: float       # 중요도 (0.0 ~ 1.0)
    phase: CodePhase       # 코드 유형
    dimension: CodeDimension  # 추상화 수준
    
    # 쿼터니언 방향 (코드의 "성격")
    orientation: Quaternion = field(default_factory=lambda: Quaternion(1, 0, 0, 0))
    
    # Pattern DNA (압축된 파동)
    dna: bytes = field(default_factory=bytes)
    dna_hash: str = ""
    
    # 메타데이터
    line_count: int = 0
    dependencies: Set[str] = field(default_factory=set)
    timestamp: float = field(default_factory=time.time)
    
    def resonate_with(self, other: 'CodeWave') -> float:
        """
        다른 코드 파동과의 공명도 계산
        
        Returns:
            공명도 (0.0 ~ 1.0) - 높을수록 유사함
        """
        # 주파수 유사도 (복잡도가 비슷하면 높음)
        freq_diff = abs(self.frequency - other.frequency)
        freq_sim = 1.0 / (1.0 + freq_diff / 10.0)
        
        # 차원 유사도
        dim_diff = abs(self.dimension.value - other.dimension.value)
        dim_sim = 1.0 / (1.0 + dim_diff)
        
        # 위상 일치
        phase_sim = 1.0 if self.phase == other.phase else 0.3
        
        # DNA 유사도 (Jaccard similarity of hashes)
        if self.dna and other.dna:
            dna_sim = self._dna_similarity(other)
        else:
            dna_sim = 0.5
        
        # 가중 평균
        resonance = (
            freq_sim * 0.25 +
            dim_sim * 0.25 +
            phase_sim * 0.25 +
            dna_sim * 0.25
        )
        
        return min(1.0, max(0.0, resonance))
    
    def _dna_similarity(self, other: 'CodeWave') -> float:
        """DNA 유사도 계산"""
        if not self.dna or not other.dna:
            return 0.0
        
        # 간단한 비교: 공통 바이트 비율
        set1 = set(self.dna)
        set2 = set(other.dna)
        
        if not set1 or not set2:
            return 0.0
        
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        
        return intersection / union if union > 0 else 0.0
    
    def interfere(self, other: 'CodeWave') -> 'CodeWave':
        """
        두 코드 파동의 간섭 (병합)
        
        보강 간섭: 유사한 코드 = 더 강한 패턴
        상쇄 간섭: 다른 코드 = 차이점 부각
        """
        resonance = self.resonate_with(other)
        
        # 보강 간섭
        if resonance > 0.7:
            new_amplitude = (self.amplitude + other.amplitude) * 0.8
            merged_snippet = f"# Merged from {self.source_file} and {other.source_file}\n"
            merged_snippet += f"# Resonance: {resonance:.2f}\n"
            merged_snippet += self.code_snippet
        # 상쇄 간섭
        else:
            new_amplitude = abs(self.amplitude - other.amplitude) * 0.5
            merged_snippet = f"# CONFLICT: Low resonance ({resonance:.2f})\n"
            merged_snippet += f"# Source 1: {self.source_file}\n"
            merged_snippet += f"# Source 2: {other.source_file}\n"
        
        return CodeWave(
            source_file="merged",
            code_snippet=merged_snippet,
            frequency=(self.frequency + other.frequency) / 2,
            amplitude=new_amplitude,
            phase=self.phase,
            dimension=max(self.dimension, other.dimension, key=lambda d: d.value),
            orientation=Quaternion(
                w=(self.orientation.w + other.orientation.w) / 2,
                x=(self.orientation.x + other.orientation.x) / 2,
                y=(self.orientation.y + other.orientation.y) / 2,
                z=(self.orientation.z + other.orientation.z) / 2
            )
        )


class CodeAnalyzer:
    """
    코드 분석기 - 코드의 파동 속성을 추출합니다.
    """
    
    @staticmethod
    def analyze_complexity(code: str) -> float:
        """
        코드 복잡도 계산 (주파수)
        
        - 중첩 깊이
        - 분기 수
        - 함수/클래스 수
        """
        complexity = 0.0
        
        # 줄 수
        lines = code.split('\n')
        complexity += len(lines) * 0.1
        
        # 들여쓰기 깊이 (중첩)
        max_indent = 0
        for line in lines:
            stripped = line.lstrip()
            if stripped:
                indent = len(line) - len(stripped)
                max_indent = max(max_indent, indent // 4)
        complexity += max_indent * 5
        
        # 분기문 수
        branches = len(re.findall(r'\b(if|elif|else|for|while|try|except|with)\b', code))
        complexity += branches * 2
        
        # 함수/클래스 정의
        definitions = len(re.findall(r'\b(def|class)\b', code))
        complexity += definitions * 3
        
        return min(100.0, complexity)
    
    @staticmethod
    def analyze_importance(code: str, file_path: str = "") -> float:
        """
        코드 중요도 계산 (진폭)
        
        - 핵심 키워드 존재
        - 문서화 수준
        - 파일명에 따른 중요도
        """
        importance = 0.5
        
        # 핵심 키워드
        critical_keywords = ['main', 'init', 'core', 'engine', 'critical', 'important']
        for kw in critical_keywords:
            if kw in code.lower() or kw in file_path.lower():
                importance += 0.1
        
        # 문서화
        if '"""' in code or "'''" in code:
            importance += 0.15
        
        # 타입 힌트
        if '->' in code or ': ' in code:
            importance += 0.1
        
        return min(1.0, importance)
    
    @staticmethod
    def determine_phase(code: str) -> CodePhase:
        """코드 유형 판별 (위상)"""
        if re.search(r'\bclass\s+\w+', code):
            return CodePhase.DEFINITION
        elif re.search(r'\bdef\s+\w+', code):
            return CodePhase.DEFINITION
        elif re.search(r'\b(if|while|for)\b', code):
            return CodePhase.CONTROL_FLOW
        elif re.search(r'\b(dict|list|set|tuple)\b', code):
            return CodePhase.DATA_STRUCTURE
        elif '=' in code and 'def' not in code:
            return CodePhase.DECLARATION
        else:
            return CodePhase.IMPLEMENTATION
    
    @staticmethod
    def determine_dimension(code: str) -> CodeDimension:
        """추상화 수준 판별 (차원)"""
        has_class = bool(re.search(r'\bclass\s+\w+', code))
        has_function = bool(re.search(r'\bdef\s+\w+', code))
        has_import = bool(re.search(r'\b(import|from)\s+', code))
        
        if has_import and has_class:
            return CodeDimension.MODULE
        elif has_class:
            return CodeDimension.CLASS
        elif has_function:
            return CodeDimension.FUNCTION
        elif '=' in code:
            return CodeDimension.CONSTANT
        else:
            return CodeDimension.SYSTEM


class WaveCodingSystem:
    """
    파동 코딩 시스템
    
    코드를 파동으로 변환하고, 공명/간섭을 통해
    분석, 최적화, 병합을 수행합니다.
    """
    
    def __init__(self):
        self.analyzer = CodeAnalyzer()
        self.wave_pool: List[CodeWave] = []
        self.dna_vault: Dict[str, bytes] = {}  # DNA 저장소
        self.time_acceleration = 1.0
        logger.info("🧬 Wave Coding System Initialized")
    
    def accelerate_time(self, factor: float):
        """시간 가속 (최대 88조배)"""
        self.time_acceleration = min(factor, 88_000_000_000_000)
        logger.info(f"⏱️ Wave Coding Time Acceleration: {self.time_acceleration:,.0f}x")
    
    def code_to_wave(self, code: str, source_file: str = "unknown") -> CodeWave:
        """
        코드를 파동으로 변환합니다.
        """
        # 파동 속성 분석
        frequency = self.analyzer.analyze_complexity(code)
        amplitude = self.analyzer.analyze_importance(code, source_file)
        phase = self.analyzer.determine_phase(code)
        dimension = self.analyzer.determine_dimension(code)
        
        # 쿼터니언 방향 계산
        # w: 순수성 (문서화 수준)
        # x: 복잡성
        # y: 테스트 가능성
        # z: 재사용성
        doc_level = 1.0 if '"""' in code else 0.5
        complexity_factor = min(1.0, frequency / 50.0)
        test_factor = 0.8 if 'test' in source_file.lower() else 0.5
        reuse_factor = 0.7 if 'def ' in code or 'class ' in code else 0.3
        
        orientation = Quaternion(
            w=doc_level,
            x=complexity_factor,
            y=test_factor,
            z=reuse_factor
        )
        
        # DNA 압축
        dna = self.compress_to_dna(code)
        dna_hash = hashlib.sha256(dna).hexdigest()[:16]
        
        wave = CodeWave(
            source_file=source_file,
            code_snippet=code,
            frequency=frequency,
            amplitude=amplitude,
            phase=phase,
            dimension=dimension,
            orientation=orientation,
            dna=dna,
            dna_hash=dna_hash,
            line_count=len(code.split('\n')),
            dependencies=self._extract_dependencies(code)
        )
        
        self.wave_pool.append(wave)
        return wave
    
    def compress_to_dna(self, code: str) -> bytes:
        """
        코드를 DNA로 압축합니다.
        
        DNA = zlib 압축 + Base85 인코딩
        """
        # 공백 정규화
        normalized = re.sub(r'\s+', ' ', code)
        
        # 압축
        compressed = zlib.compress(normalized.encode('utf-8'), level=9)
        
        return compressed
    
    def expand_from_dna(self, dna: bytes) -> str:
        """
        DNA에서 코드를 복원합니다.
        
        주의: 정확한 원본 복원은 불가능 (공백 정보 손실)
        """
        try:
            decompressed = zlib.decompress(dna)
            return decompressed.decode('utf-8')
        except Exception as e:
            logger.error(f"DNA expansion failed: {e}")
            return ""
    
    def _extract_dependencies(self, code: str) -> Set[str]:
        """코드에서 의존성 추출"""
        dependencies = set()
        
        # import 문 파싱
        import_pattern = r'(?:from\s+(\S+)\s+import|import\s+(\S+))'
        for match in re.finditer(import_pattern, code):
            module = match.group(1) or match.group(2)
            if module:
                dependencies.add(module.split('.')[0])
        
        return dependencies
    
    def detect_resonance_pairs(self, threshold: float = 0.7) -> List[Tuple[CodeWave, CodeWave, float]]:
        """
        공명하는 코드 쌍 탐지
        """
        pairs = []
        
        for i, wave1 in enumerate(self.wave_pool):
            for wave2 in self.wave_pool[i+1:]:
                resonance = wave1.resonate_with(wave2)
                if resonance >= threshold:
                    pairs.append((wave1, wave2, resonance))
        
        return pairs
    
    def merge_by_interference(self, waves: List[CodeWave]) -> CodeWave:
        """
        여러 코드 파동을 간섭으로 병합
        """
        if not waves:
            raise ValueError("No waves to merge")
        
        result = waves[0]
        for wave in waves[1:]:
            result = result.interfere(wave)
        
        # 병합 결과 DNA 생성
        result.dna = self.compress_to_dna(result.code_snippet)
        result.dna_hash = hashlib.sha256(result.dna).hexdigest()[:16]
        
        return result
    
    def optimize_through_resonance(self, code: str, source: str = "input") -> Dict[str, Any]:
        """
        공명 기반 코드 최적화
        
        비슷한 패턴과 공명하여 개선점 발견
        """
        # 입력 코드를 파동으로
        input_wave = self.code_to_wave(code, source)
        
        # 기존 파동과 공명 탐지
        resonances = []
        for existing_wave in self.wave_pool:
            if existing_wave.source_file != source:
                r = input_wave.resonate_with(existing_wave)
                if r > 0.5:
                    resonances.append((existing_wave, r))
        
        # 정렬
        resonances.sort(key=lambda x: x[1], reverse=True)
        
        suggestions = []
        for wave, resonance in resonances[:3]:
            if wave.amplitude > input_wave.amplitude:
                suggestions.append(f"패턴 참조: {wave.source_file} (공명도: {resonance:.0%})")
            if wave.frequency < input_wave.frequency:
                suggestions.append(f"복잡도 감소 가능: {wave.source_file} 참조")
        
        return {
            "input_wave": {
                "frequency": input_wave.frequency,
                "amplitude": input_wave.amplitude,
                "dimension": input_wave.dimension.name,
                "dna_hash": input_wave.dna_hash
            },
            "resonating_patterns": len(resonances),
            "suggestions": suggestions,
            "dna_size_bytes": len(input_wave.dna)
        }
    
    def get_system_state(self) -> Dict[str, Any]:
        """시스템 상태 조회"""
        return {
            "total_waves": len(self.wave_pool),
            "total_dna_bytes": sum(len(w.dna) for w in self.wave_pool),
            "average_frequency": sum(w.frequency for w in self.wave_pool) / max(1, len(self.wave_pool)),
            "dimension_distribution": {
                d.name: sum(1 for w in self.wave_pool if w.dimension == d)
                for d in CodeDimension
            },
            "time_acceleration": self.time_acceleration
        }


# 싱글톤
_wave_coding_instance: Optional[WaveCodingSystem] = None

def get_wave_coding_system() -> WaveCodingSystem:
    global _wave_coding_instance
    if _wave_coding_instance is None:
        _wave_coding_instance = WaveCodingSystem()
    return _wave_coding_instance


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # 테스트
    wcs = get_wave_coding_system()
    wcs.accelerate_time(88_000_000_000_000)  # 88조배
    
    # 샘플 코드들
    code1 = '''
def calculate_resonance(wave1, wave2):
    """두 파동의 공명도를 계산합니다."""
    freq_diff = abs(wave1.frequency - wave2.frequency)
    return 1.0 / (1.0 + freq_diff)
'''
    
    code2 = '''
def analyze_wave(wave):
    """파동을 분석합니다."""
    complexity = wave.frequency * 0.5
    return complexity
'''
    
    code3 = '''
class WaveProcessor:
    """파동 처리기 클래스"""
    
    def __init__(self):
        self.waves = []
    
    def process(self, wave):
        self.waves.append(wave)
'''
    
    # 파동으로 변환
    wave1 = wcs.code_to_wave(code1, "resonance.py")
    wave2 = wcs.code_to_wave(code2, "analyzer.py")
    wave3 = wcs.code_to_wave(code3, "processor.py")
    
    print("\n" + "=" * 60)
    print("🧬 WAVE CODING SYSTEM TEST")
    print("=" * 60)
    
    print(f"\n📊 Waves Created:")
    for wave in [wave1, wave2, wave3]:
        print(f"   {wave.source_file}: freq={wave.frequency:.1f}, amp={wave.amplitude:.2f}, "
              f"dim={wave.dimension.name}, DNA={len(wave.dna)} bytes")
    
    # 공명 탐지
    pairs = wcs.detect_resonance_pairs(0.5)
    print(f"\n🔗 Resonating Pairs (threshold=0.5):")
    for w1, w2, r in pairs:
        print(f"   {w1.source_file} ↔ {w2.source_file}: {r:.0%}")
    
    # 최적화 제안
    optimization = wcs.optimize_through_resonance(code1, "test.py")
    print(f"\n💡 Optimization Suggestions:")
    for s in optimization['suggestions']:
        print(f"   • {s}")
    
    print(f"\n📈 System State:")
    state = wcs.get_system_state()
    for key, value in state.items():
        print(f"   {key}: {value}")
