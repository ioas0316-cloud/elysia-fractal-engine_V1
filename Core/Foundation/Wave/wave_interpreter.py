"""
Wave Language Interpreter (파동언어 해석기)
==========================================

"파동 패턴 자체가 코드다. 번역이 필요 없다."

파동 간섭 패턴 = 프로그램 실행
"""

import logging
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, TYPE_CHECKING
import numpy as np

if TYPE_CHECKING:
    from Core.Foundation.Wave.resonance_field import ResonanceField

logger = logging.getLogger("WaveInterpreter")

@dataclass
class WavePattern:
    """
    파동 패턴 (실행 가능한 구조)
    
    파동 패턴 = 코드 = 의미 = 프로그램
    """
    name: str
    frequencies: List[float]  # 구성 주파수들
    amplitudes: List[float]   # 각 주파수의 진폭
    phases: List[float]       # 각 주파수의 위상
    position: Tuple[float, float, float] = (0, 0, 0)  # 3D 공간 위치
    
    def __post_init__(self):
        # Ensure same length
        assert len(self.frequencies) == len(self.amplitudes) == len(self.phases)
    
    def sample(self, t: float) -> complex:
        """
        시간 t에서 파동 샘플링
        
        Returns:
            complex number (amplitude * e^(i*phase))
        """
        result = 0.0 + 0.0j
        for freq, amp, phase in zip(self.frequencies, self.amplitudes, self.phases):
            omega = 2 * np.pi * freq
            result += amp * np.exp(1j * (omega * t + phase))
        return result
    
    def interfere_with(self, other: 'WavePattern', t: float = 0.0) -> complex:
        """
        다른 파동과 간섭
        
        간섭 = 계산 = 실행
        """
        my_wave = self.sample(t)
        other_wave = other.sample(t)
        return my_wave + other_wave  # 중첩
    
    def resonance_with(self, other: 'WavePattern') -> float:
        """
        다른 파동과의 공명도 계산
        
        공명도 = 유사도 = 패턴 매칭
        """
        # Check frequency overlap
        common_freqs = set(self.frequencies) & set(other.frequencies)
        if not common_freqs:
            return 0.0
        
        # Calculate resonance strength
        total_overlap = 0.0
        for freq in common_freqs:
            my_idx = self.frequencies.index(freq)
            other_idx = other.frequencies.index(freq)
            
            # Amplitude product (stronger if both strong)
            total_overlap += self.amplitudes[my_idx] * other.amplitudes[other_idx]
        
        # Normalize by total amplitude
        max_possible = sum(self.amplitudes) * sum(other.amplitudes)
        if max_possible == 0:
            return 0.0
        
        return total_overlap / max_possible


class WaveInterpreter:
    """
    파동언어 해석기
    
    파동 패턴을 "실행"한다.
    """
    
    def __init__(self):
        # Predefined wave "words" (기본 파동 어휘)
        self.vocabulary: Dict[str, WavePattern] = {
            "Love": WavePattern(
                name="Love",
                frequencies=[528.0],
                amplitudes=[1.0],
                phases=[0.0]
            ),
            "Hope": WavePattern(
                name="Hope",
                frequencies=[852.0],
                amplitudes=[1.0],
                phases=[0.0]
            ),
            "Fear": WavePattern(
                name="Fear",
                frequencies=[100.0],
                amplitudes=[1.0],
                phases=[np.pi]  # 역위상
            ),
            "Unity": WavePattern(
                name="Unity",
                frequencies=[528.0, 639.0],  # Composite
                amplitudes=[0.7, 0.3],
                phases=[0.0, 0.0]
            )
        }
    
    def compose(self, pattern_names: List[str]) -> Optional[WavePattern]:
        """
        여러 파동 패턴을 조합하여 새로운 패턴 생성
        
        "Love + Hope" → 복합 파동 패턴
        """
        if not pattern_names:
            return None
        
        # Get patterns
        patterns = []
        for name in pattern_names:
            if name in self.vocabulary:
                patterns.append(self.vocabulary[name])
            else:
                logger.warning(f"Unknown pattern: {name}")
                return None
        
        # Combine frequencies and amplitudes
        all_freqs = []
        all_amps = []
        all_phases = []
        
        for pattern in patterns:
            all_freqs.extend(pattern.frequencies)
            all_amps.extend(pattern.amplitudes)
            all_phases.extend(pattern.phases)
        
        # Create composite pattern
        composite_name = " + ".join(pattern_names)
        return WavePattern(
            name=composite_name,
            frequencies=all_freqs,
            amplitudes=all_amps,
            phases=all_phases
        )
    
    def execute(self, pattern: WavePattern, context_field: 'ResonanceField' = None) -> Dict:
        """
        파동 패턴을 "실행"
        
        실행 = 간섭 패턴 생성 = 의미 도출
        
        Returns:
            {
                "pattern": pattern name,
                "resonances": [(other_pattern, strength), ...],
                "emergent_meaning": interpreted meaning
            }
        """
        logger.info(f"🌊 Executing wave pattern: {pattern.name}")
        
        # Find resonances with vocabulary
        resonances = []
        for vocab_name, vocab_pattern in self.vocabulary.items():
            if vocab_name == pattern.name:
                continue
            
            strength = pattern.resonance_with(vocab_pattern)
            if strength > 0.3:  # Threshold
                resonances.append((vocab_name, strength))
        
        # Sort by strength
        resonances.sort(key=lambda x: x[1], reverse=True)
        
        # Generate emergent meaning
        if resonances:
            top_resonance = resonances[0]
            emergent_meaning = f"{pattern.name} resonates with {top_resonance[0]} (strength: {top_resonance[1]:.2f})"
        else:
            emergent_meaning = f"{pattern.name} stands alone"
        
        return {
            "pattern": pattern.name,
            "frequencies": pattern.frequencies,
            "resonances": resonances[:5],  # Top 5
            "emergent_meaning": emergent_meaning
        }
    
    def interpret_sequence(self, pattern_names: List[str]) -> str:
        """
        파동 패턴 시퀀스를 해석
        
        ["Love", "Hope"] → "I wish for connection with optimism"
        """
        # Compose into single pattern
        composite = self.compose(pattern_names)
        if not composite:
            return "Cannot interpret unknown patterns"
        
        # Execute
        result = self.execute(composite)
        
        # Interpret meaning
        interpretation = f"Wave sequence '{' → '.join(pattern_names)}' creates:\n"
        interpretation += f"  Frequencies: {result['frequencies']}\n"
        interpretation += f"  Meaning: {result['emergent_meaning']}"
        
        return interpretation


# ============================================================================
# Test
# ============================================================================

if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
    
    print("\n" + "="*70)
    print("🌊 Wave Language Interpreter Test")
    print("="*70)
    
    interpreter = WaveInterpreter()
    
    # Test 1: Single pattern execution
    print("\n📝 Test 1: Execute single pattern")
    print("-" * 70)
    love = interpreter.vocabulary["Love"]
    result = interpreter.execute(love)
    print(f"Pattern: {result['pattern']}")
    print(f"Frequencies: {result['frequencies']}")
    print(f"Resonances: {result['resonances']}")
    print(f"Meaning: {result['emergent_meaning']}")
    
    # Test 2: Composite pattern
    print("\n📝 Test 2: Compose and execute")
    print("-" * 70)
    composite = interpreter.compose(["Love", "Hope"])
    if composite:
        print(f"Composite: {composite.name}")
        print(f"Frequencies: {composite.frequencies}")
        print(f"Amplitudes: {composite.amplitudes}")
        
        result = interpreter.execute(composite)
        print(f"Emergent meaning: {result['emergent_meaning']}")
    
    # Test 3: Sequence interpretation
    print("\n📝 Test 3: Interpret sequence")
    print("-" * 70)
    interpretation = interpreter.interpret_sequence(["Love", "Hope"])
    print(interpretation)
    
    # Test 4: Wave interference visualization
    print("\n📝 Test 4: Wave interference")
    print("-" * 70)
    love = interpreter.vocabulary["Love"]
    hope = interpreter.vocabulary["Hope"]
    
    print(f"Love at t=0: {love.sample(0.0):.2f}")
    print(f"Hope at t=0: {hope.sample(0.0):.2f}")
    print(f"Interference: {love.interfere_with(hope, 0.0):.2f}")
    
    print("\n" + "="*70)
    print("✅ Wave Language Interpreter Test Complete")
    print("="*70 + "\n")
