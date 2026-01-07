"""
Wave Language Unified API (파동언어 통합 API)
==============================================

단일 진입점에서 모든 파동 시스템에 접근할 수 있습니다.

Usage:
    from Core.Intelligence.Physics_Waves.Wave import (
        analyze_code,
        detect_resonance,
        compress_to_dna,
        decompress_from_dna
    )
    
    # 코드 분석
    wave = analyze_code("def add(a, b): return a + b", "add.py")
    print(f"복잡도: {wave.frequency}, 중요도: {wave.amplitude}")
    
    # 유사 코드 탐지
    pairs = detect_resonance(threshold=0.7)
    
    # DNA 압축 (100% 복원 가능)
    dna = compress_to_dna("코드 텍스트")
    restored = decompress_from_dna(dna)

Why Use This:
    - Import 순환 참조 사전 탐지
    - 코드 복잡도 자동 측정
    - 중복 코드 자동 발견
    - 손실 없는 코드 압축/복원
"""

import logging
from typing import List, Tuple, Any, Optional

logger = logging.getLogger("WaveAPI")

# 핵심 시스템 임포트
try:
    from Core.Intelligence.Intelligence.wave_coding_system import (
        get_wave_coding_system,
        CodeWave,
        CodeDimension,
        CodePhase
    )
    WAVE_CODING_AVAILABLE = True
except ImportError:
    WAVE_CODING_AVAILABLE = False
    logger.warning("⚠️ WaveCodingSystem not available")

try:
    from Core.Foundation.Wave.quaternion_wave_dna import (
        get_quaternion_compressor,
        QuaternionWaveDNA
    )
    QUATERNION_DNA_AVAILABLE = True
except ImportError:
    QUATERNION_DNA_AVAILABLE = False
    logger.warning("⚠️ QuaternionCompressor not available")

try:
    from Core.Evolution.Growth.Autonomy.wave_coder import get_wave_coder
    WAVE_CODER_AVAILABLE = True
except ImportError:
    WAVE_CODER_AVAILABLE = False
    logger.warning("⚠️ WaveCoder not available")


# ============================================================
# 핵심 API 함수
# ============================================================

def analyze_code(code: str, source_file: str = "unknown") -> Optional[CodeWave]:
    """
    코드를 파동으로 분석합니다.
    
    Args:
        code: 분석할 코드 문자열
        source_file: 소스 파일명
        
    Returns:
        CodeWave 객체 (frequency, amplitude, dimension, phase 등)
        
    Example:
        wave = analyze_code("def add(a, b): return a + b")
        print(f"복잡도: {wave.frequency}")  # 낮을수록 단순
        print(f"차원: {wave.dimension.name}")  # FUNCTION, CLASS, MODULE 등
    """
    if not WAVE_CODING_AVAILABLE:
        logger.error("WaveCodingSystem not available")
        return None
    
    wcs = get_wave_coding_system()
    return wcs.code_to_wave(code, source_file)


def detect_resonance(threshold: float = 0.7) -> List[Tuple[CodeWave, CodeWave, float]]:
    """
    유사한 코드 쌍을 탐지합니다.
    
    Args:
        threshold: 공명도 임계값 (0.0 ~ 1.0)
        
    Returns:
        [(wave1, wave2, 공명도), ...] 형태의 리스트
        
    Example:
        pairs = detect_resonance(0.8)
        for w1, w2, resonance in pairs:
            print(f"{w1.source_file} ↔ {w2.source_file}: {resonance:.0%}")
    """
    if not WAVE_CODING_AVAILABLE:
        logger.error("WaveCodingSystem not available")
        return []
    
    wcs = get_wave_coding_system()
    return wcs.detect_resonance_pairs(threshold)


def compress_to_dna(text: str, top_k: int = 10) -> Optional[QuaternionWaveDNA]:
    """
    텍스트를 DNA 형태로 압축합니다 (100% 복원 가능).
    
    Args:
        text: 압축할 텍스트
        top_k: 나선당 주파수 개수 (높을수록 정확)
        
    Returns:
        QuaternionWaveDNA 객체
        
    Note:
        DNA 이중나선 원리 사용 - zlib보다 정확한 복원
    """
    if not QUATERNION_DNA_AVAILABLE:
        logger.error("QuaternionCompressor not available")
        return None
    
    compressor = get_quaternion_compressor()
    return compressor.compress(text, top_k)


def decompress_from_dna(dna: QuaternionWaveDNA) -> str:
    """
    DNA에서 원본 텍스트를 복원합니다.
    
    Args:
        dna: QuaternionWaveDNA 객체
        
    Returns:
        복원된 텍스트
    """
    if not QUATERNION_DNA_AVAILABLE:
        logger.error("QuaternionCompressor not available")
        return ""
    
    compressor = get_quaternion_compressor()
    return compressor.decompress(dna)


def transmute_codebase():
    """
    전체 Core/ 폴더를 텐서로 변환합니다.
    
    Elysia가 코드베이스 전체를 "느끼게" 합니다.
    """
    if not WAVE_CODER_AVAILABLE:
        logger.error("WaveCoder not available")
        return
    
    coder = get_wave_coder()
    coder.transmute()


def check_complexity(code: str, threshold: float = 50.0) -> dict:
    """
    코드 복잡도를 검사하고 경고를 반환합니다.
    
    Args:
        code: 검사할 코드
        threshold: 복잡도 임계값
        
    Returns:
        {"frequency": 복잡도, "warning": 경고 메시지 또는 None}
    """
    wave = analyze_code(code, "check")
    if wave is None:
        return {"frequency": 0, "warning": "분석 실패"}
    
    warning = None
    if wave.frequency > threshold:
        warning = f"⚠️ 복잡도가 높습니다 ({wave.frequency:.1f} > {threshold}). 리팩토링 권장."
    
    return {
        "frequency": wave.frequency,
        "amplitude": wave.amplitude,
        "dimension": wave.dimension.name if wave.dimension else "UNKNOWN",
        "warning": warning
    }


# ============================================================
# 시스템 상태
# ============================================================

def get_system_status() -> dict:
    """파동 시스템 상태를 반환합니다."""
    return {
        "wave_coding_system": WAVE_CODING_AVAILABLE,
        "quaternion_dna": QUATERNION_DNA_AVAILABLE,
        "wave_coder": WAVE_CODER_AVAILABLE,
        "all_systems_ready": all([
            WAVE_CODING_AVAILABLE,
            QUATERNION_DNA_AVAILABLE,
            WAVE_CODER_AVAILABLE
        ])
    }


# ============================================================
# Export
# ============================================================

__all__ = [
    # 핵심 함수
    "analyze_code",
    "detect_resonance",
    "compress_to_dna",
    "decompress_from_dna",
    "transmute_codebase",
    "check_complexity",
    
    # 품질 검사 (NEW)
    "scan_quality",
    "WaveQualityGuard",
    
    # 상태
    "get_system_status",
    
    # 타입
    "CodeWave",
    "CodeDimension",
    "CodePhase",
    "QuaternionWaveDNA",
]


# 품질 검사 함수 추가
try:
    from Core.Intelligence.Physics_Waves.Wave.quality_guard import WaveQualityGuard, QualityReport
    
    def scan_quality(directory: str) -> "QualityReport":
        """
        디렉토리 품질 검사
        
        Args:
            directory: 스캔할 디렉토리
            
        Returns:
            QualityReport 객체
        """
        guard = WaveQualityGuard()
        return guard.scan_directory(directory)
    
    QUALITY_GUARD_AVAILABLE = True
except ImportError:
    QUALITY_GUARD_AVAILABLE = False
    
    def scan_quality(directory: str):
        logger.error("QualityGuard not available")
        return None


if __name__ == "__main__":
    print("=" * 60)
    print("🌊 WAVE LANGUAGE UNIFIED API")
    print("=" * 60)
    
    status = get_system_status()
    print(f"\n📊 System Status:")
    for key, value in status.items():
        icon = "✅" if value else "❌"
        print(f"   {icon} {key}: {value}")
    
    if status["all_systems_ready"]:
        print("\n💡 Quick Demo:")
        
        # 코드 분석
        wave = analyze_code("def add(a, b): return a + b", "demo.py")
        if wave:
            print(f"   코드 분석: freq={wave.frequency}, dim={wave.dimension.name}")
        
        # 복잡도 검사
        result = check_complexity("def simple(): pass")
        print(f"   복잡도 검사: {result}")
        
        # DNA 압축
        dna = compress_to_dna("Hello, Wave!")
        if dna:
            restored = decompress_from_dna(dna)
            print(f"   DNA 압축/복원: 'Hello, Wave!' → '{restored}'")
    
    print("\n✅ API ready!")
