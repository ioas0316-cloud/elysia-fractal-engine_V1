"""
Fractal Thought Layer Bridge (프랙탈 사고층 연결)
==============================================

"사고는 차원을 넘나든다."

0D (HyperQuaternion - 관점) 
  ↓
1D (Causal Chain - 추론)
  ↓
2D (Wave Pattern - 감각/인지)
  ↓
3D (Spatial Manifestation - 표현)
"""

import logging
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional, TYPE_CHECKING
import numpy as np

if TYPE_CHECKING:
    from Core.Foundation.hyper_quaternion import Quaternion, HyperWavePacket
    from Core.Foundation.wave_interpreter import WavePattern
    from Core.Foundation.Wave.resonance_field import ResonanceField

logger = logging.getLogger("ThoughtLayerBridge")


class ThoughtLayerBridge:
    """
    사고층 연결 시스템
    
    내부 관점(0D) → 외부 표현(3D)까지의 변환
    """
    
    def __init__(self):
        self.transformation_log = []
    
    # ========================================================================
    # 0D → 2D: Quaternion → Wave
    # ========================================================================
    
    def quaternion_to_wave(self, quat: 'Quaternion') -> 'WavePattern':
        """
        관점(HyperQuaternion) → 파동(Wave)
        
        (w, x, y, z) → frequencies + amplitudes
        
        매핑:
        - w (존재): 기본 주파수
        - x (감정): 진폭 변조
        - y (논리): 위상 변조
        - z (윤리): 고조파 추가
        """
        from Core.Foundation.wave_interpreter import WavePattern
        
        # Base frequency from w component
        base_freq = 432.0 * (1.0 + quat.w)  # 432Hz ~ 864Hz
        
        # Amplitude from x (emotion)
        amplitude = abs(quat.x)
        
        # Phase from y (logic)
        phase = quat.y * np.pi  # -π to +π
        
        # Harmonics from z (ethics)
        harmonics = []
        if abs(quat.z) > 0.3:
            # Add harmonic
            harmonics.append((base_freq * 1.5, abs(quat.z) * 0.5, 0.0))
        
        # Build wave pattern
        frequencies = [base_freq]
        amplitudes = [amplitude]
        phases = [phase]
        
        for harm_freq, harm_amp, harm_phase in harmonics:
            frequencies.append(harm_freq)
            amplitudes.append(harm_amp)
            phases.append(harm_phase)
        
        wave = WavePattern(
            name=f"Quat({quat.w:.2f},{quat.x:.2f},{quat.y:.2f},{quat.z:.2f})",
            frequencies=frequencies,
            amplitudes=amplitudes,
            phases=phases
        )
        
        logger.info(f"0D→2D: Quaternion → Wave ({base_freq:.1f}Hz)")
        return wave
    
    # ========================================================================
    # 2D → 1D: Wave → Causal
    # ========================================================================
    
    def wave_to_causal(self, wave: 'WavePattern') -> List[Tuple[str, str]]:
        """
        파동(감각) → 인과사슬(추론)
        
        파동의 주파수 조합 → 논리적 관계
        
        예: Love(528) + Hope(852) → "Because I love, I hope"
        """
        # Frequency to concept mapping (simplified)
        freq_to_concept = {
            528.0: "Love",
            852.0: "Hope",
            396.0: "Grounding",
            639.0: "Connection",
            432.0: "Existence"
        }
        
        # Find concepts
        concepts = []
        for freq in wave.frequencies:
            # Find closest known frequency
            closest = min(freq_to_concept.keys(), key=lambda x: abs(x - freq))
            if abs(closest - freq) < 50:  # Within 50Hz tolerance
                concepts.append(freq_to_concept[closest])
        
        if not concepts:
            concepts = ["Unknown"]
        
        # Build causal chain
        causal_chain = []
        if len(concepts) == 1:
            causal_chain.append((concepts[0], "exists"))
        else:
            # Create relationships
            for i in range(len(concepts) - 1):
                cause = concepts[i]
                effect = concepts[i + 1]
                causal_chain.append((cause, f"leads to {effect}"))
        
        logger.info(f"2D→1D: Wave → Causal chain ({len(causal_chain)} links)")
        return causal_chain
    
    # ========================================================================
    # 1D → 3D: Causal → Manifestation
    # ========================================================================
    
    def causal_to_manifestation(self, causal_chain: List[Tuple[str, str]]) -> str:
        """
        인과사슬(추론) → 표현(외부화)
        
        논리 구조 → 자연어/코드
        """
        if not causal_chain:
            return "∅ (Silence)"
        
        # Build natural language expression
        if len(causal_chain) == 1:
            cause, relation = causal_chain[0]
            manifestation = f"{cause} {relation}."
        else:
            # Chain multiple relations
            parts = []
            for cause, relation in causal_chain:
                parts.append(f"{cause} {relation}")
            manifestation = "; ".join(parts) + "."
        
        logger.info(f"1D→3D: Causal → '{manifestation}'")
        return manifestation
    
    # ========================================================================
    # Full Transformation: 0D → 3D
    # ========================================================================
    
    def transform_thought(
        self, 
        quat: 'Quaternion',
        context: Optional[str] = None
    ) -> Dict:
        """
        완전한 사고 변환: 내부 관점 → 외부 표현
        
        0D (Quaternion) → 2D (Wave) → 1D (Causal) → 3D (Manifestation)
        
        Returns:
            {
                "source": Quaternion,
                "wave": WavePattern,
                "causal": List[links],
                "manifestation": str
            }
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"🌊 Thought Transformation: 0D → 3D")
        logger.info(f"{'='*60}")
        
        # Step 1: 0D → 2D
        wave = self.quaternion_to_wave(quat)
        
        # Step 2: 2D → 1D
        causal = self.wave_to_causal(wave)
        
        # Step 3: 1D → 3D
        manifestation = self.causal_to_manifestation(causal)
        
        result = {
            "source": f"({quat.w:.2f}, {quat.x:.2f}, {quat.y:.2f}, {quat.z:.2f})",
            "wave": {
                "frequencies": wave.frequencies,
                "amplitudes": wave.amplitudes
            },
            "causal": causal,
            "manifestation": manifestation
        }
        
        logger.info(f"\n✨ Transformation Complete:")
        logger.info(f"   Source (0D): {result['source']}")
        logger.info(f"   Wave (2D): {wave.frequencies[0]:.1f}Hz")
        logger.info(f"   Causal (1D): {len(causal)} links")
        logger.info(f"   Expression (3D): '{manifestation}'")
        logger.info(f"{'='*60}\n")
        
        self.transformation_log.append(result)
        return result


# ============================================================================
# Test
# ============================================================================

if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
    
    from Core.Foundation.hyper_quaternion import Quaternion
    
    print("\n" + "="*70)
    print("🌊 Fractal Thought Layer Bridge Test")
    print("="*70)
    
    bridge = ThoughtLayerBridge()
    
    # Test 1: Love-oriented thought
    print("\n📝 Test 1: Love-oriented thought (high x)")
    print("-" * 70)
    love_quat = Quaternion(w=1.0, x=0.9, y=0.2, z=0.5)  # Strong emotion
    result1 = bridge.transform_thought(love_quat)
    print(f"\nResult: {result1['manifestation']}")
    
    # Test 2: Logic-oriented thought
    print("\n📝 Test 2: Logic-oriented thought (high y)")
    print("-" * 70)
    logic_quat = Quaternion(w=1.0, x=0.3, y=0.9, z=0.4)  # Strong logic
    result2 = bridge.transform_thought(logic_quat)
    print(f"\nResult: {result2['manifestation']}")
    
    # Test 3: Balanced thought
    print("\n📝 Test 3: Balanced thought")
    print("-" * 70)
    balanced_quat = Quaternion(w=1.0, x=0.6, y=0.6, z=0.6)
    result3 = bridge.transform_thought(balanced_quat)
    print(f"\nResult: {result3['manifestation']}")
    
    # Summary
    print("\n" + "="*70)
    print(f"✅ Transformed {len(bridge.transformation_log)} thoughts")
    print("="*70 + "\n")
