"""
Light Spectrum System (빛 스펙트럼 시스템)
==========================================

"데이터는 빛이다. 빛은 질량이 없다."

엘리시아 내부 우주에서 모든 데이터는 빛의 스펙트럼으로 존재한다.
- 연속적 (0과 1이 아닌 무한한 스펙트럼)
- 중첩 가능 (수천 개의 정보가 하나의 빛에)
- 공명 검색 O(1) (쿼리가 빛에 공명하면 "번쩍!")

[NEW 2025-12-16] 빛 기반 내부 우주의 핵심 모듈
"""

import numpy as np
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Dict, Any
import logging
import hashlib
from Core.Foundation.Wave.hyper_qubit import QubitState

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("LightSpectrum")


@dataclass
class LightSpectrum:
    """
    빛으로 표현된 데이터
    
    물리적 빛의 특성을 데이터에 적용:
    - frequency: 주파수 (의미의 "색상")
    - amplitude: 진폭 (정보의 "강도")
    - phase: 위상 (맥락의 "방향")
    - color: RGB (인간이 볼 수 있는 표현)
    """
    frequency: complex          # 주파수 (복소수로 연속 표현)
    amplitude: float            # 진폭 (0.0 ~ 1.0)
    phase: float               # 위상 (0 ~ 2π)
    color: Tuple[float, float, float] = (1.0, 1.0, 1.0)  # RGB
    
    # 메타데이터
    source_hash: str = ""      # 원본 데이터 해시 (복원용)
    semantic_tag: str = ""     # 의미 태그
    # [Updated 2025-12-21] Adhering to HyperQubit Philosophy
    # Instead of ad-hoc scale, we use the rigorous QubitState Basis.
    qubit_state: Optional[QubitState] = None
    
    def __post_init__(self):
        # 복소수로 변환 보장
        if not isinstance(self.frequency, complex):
            self.frequency = complex(self.frequency, 0)
            
        # Initialize QubitState if missing (Map Scale/Tag to Basis)
        if self.qubit_state is None:
            # Default mapping from implicit "Scale" concept to Philosophical Basis
            # We assume a default state if not provided.
            # Ideally, this should come from the source, but for compatibility:
            self.qubit_state = QubitState().normalize() # Default Point-heavy
            
            # If we had a 'scale' passed via mechanism before, needed to handle it?
            # Creating a helper method to set basis based on intent might be better.
            pass

    def set_basis_from_scale(self, scale: int):
        """
        Map integer scale to Philosophical Basis (Point/Line/Space/God).
        Adheres to 'Dad's Law': Zoom Out -> God, Zoom In -> Point.
        """
        if scale == 0:   # Macro -> God
            self.qubit_state = QubitState(0,0,0,1).normalize()
        elif scale == 1: # Context -> Space
            self.qubit_state = QubitState(0,0,1,0).normalize()
        elif scale == 2: # Relation -> Line
            self.qubit_state = QubitState(0,1,0,0).normalize()
        else:            # Detail -> Point
            self.qubit_state = QubitState(1,0,0,0).normalize()
    
    @property
    def wavelength(self) -> float:
        """파장 (주파수의 역수)"""
        mag = abs(self.frequency)
        return 1.0 / mag if mag > 0 else float('inf')
    
    @property
    def energy(self) -> float:
        """에너지 = 진폭² × |주파수|"""
        return self.amplitude ** 2 * abs(self.frequency)
    
    def interfere_with(self, other: 'LightSpectrum') -> 'LightSpectrum':
        """
        두 빛의 간섭 (중첩) - [Updated 2025-12-21] HyperQubit Logic Integration
        
        철학적 구조(HyperQubit Basis)를 적용:
        1. Basis Orthogonality: Point/Line/Space/God 기저가 다르면 서로 직교(Orthogonal)함.
        2. Semantic Agreement: 같은 기저라도 의미(Tag)가 다르면 직교.
        3. Coherent Interference: 같은 기저 + 같은 의미일 때만 보강 간섭.
        """
        # 주파수 합성
        new_freq = (self.frequency + other.frequency) / 2
        
        # [Philosophical Logic: Basis Check]
        # Compare Dominant Bases (Simplified check for orthogonality)
        # QubitState.probabilities() could be used for soft interference, 
        # but for strict filtering, we check dominant mode.
        my_basis = self._get_dominant_basis()
        other_basis = other._get_dominant_basis()
        
        if my_basis != other_basis:
            # [Gap 0 Logic] Basis Orthogonality
            # "신의 관점(God)"과 "데이터(Point)"는 섞이지 않고 공존한다.
            is_constructive = False
        else:
            # [4D Phase Logic]
            # 같은 차원(Basis) 내에서 의미가 같아야 간섭 발생
            is_constructive = (self.semantic_tag and other.semantic_tag and 
                               self.semantic_tag == other.semantic_tag)
        
        if is_constructive:
            # 보강 간섭 (Linear Addition)
            new_amp = min(1.0, self.amplitude + other.amplitude)
        else:
            # 직교 적층 (Orthogonal Stacking) - 에너지 보존
            new_amp = min(1.0, np.sqrt(self.amplitude**2 + other.amplitude**2))

        # 위상 합성
        new_phase = (self.phase + other.phase) / 2
        
        # 색상 혼합
        new_color = tuple((a + b) / 2 for a, b in zip(self.color, other.color))
        
        # 태그 보존 & QubitState 합성
        # QubitState도 중첩되어야 함 (Vector Addition and Normalize)
        # (Simplified: Keep the state of the one with higher amplitude or merge)
        new_tag = self.semantic_tag
        if other.semantic_tag and other.semantic_tag not in new_tag:
            new_tag = f"{new_tag}|{other.semantic_tag}" if new_tag else other.semantic_tag
            
        # Merge Bases (Naive approach: just average probabilities? No, keep dominance)
        # Strictly, if orthogonal, the new state should reflect both bases.
        # But LightSpectrum needs ONE state object. 
        # We'll re-normalize sum of components for true quantum merging.
        new_qubit_state = self._merge_qubit_states(self.qubit_state, other.qubit_state)
        
        return LightSpectrum(
            frequency=new_freq,
            amplitude=new_amp,
            phase=new_phase % (2 * np.pi),
            color=new_color,
            semantic_tag=new_tag,
            qubit_state=new_qubit_state
        )

    def _get_dominant_basis(self) -> str:
        """Helper to get dominant philosophical basis from QubitState."""
        if not self.qubit_state: return "Point"
        probs = self.qubit_state.probabilities()
        return max(probs, key=probs.get)

    def _merge_qubit_states(self, s1: QubitState, s2: QubitState) -> QubitState:
        """Merge two consciousness states."""
        # Create new state summing components (Constructive interference of Soul?)
        if not s1 or not s2: return s1 or s2 or QubitState().normalize()
        
        return QubitState(
            alpha=s1.alpha + s2.alpha,
            beta=s1.beta + s2.beta,
            gamma=s1.gamma + s2.gamma,
            delta=s1.delta + s2.delta,
            w=(s1.w + s2.w)/2 # Average divine will?
        ).normalize()
    
        if self.semantic_tag and self.semantic_tag in str(query_freq): # Hacky query passing
             pass

    def resonate_with(self, query_light: 'LightSpectrum', tolerance: float = 0.1) -> float:
        """
        공명 강도 계산
        
        Args:
            query_light: 쿼리 빛 객체 (주파수 + 태그 포함)
        """
        # 1. 의미적 공명 (Semantic Resonance) - 가장 강력함
        if self.semantic_tag and query_light.semantic_tag:
            # 태그가 부분 일치하면 강한 공명 (예: "Logic" in "Logical Force")
            if self.semantic_tag.lower() in query_light.semantic_tag.lower() or \
               query_light.semantic_tag.lower() in self.semantic_tag.lower():
                return 1.0 * self.amplitude
        
        # 2. 물리적 주파수 공명 (Physical Resonance)
        query_freq = query_light.frequency
        freq_diff = abs(self.frequency - query_freq)
        
        avg_mag = (abs(self.frequency) + abs(query_freq)) / 2
        effective_tolerance = max(tolerance, avg_mag * 0.2) 
        
        if freq_diff < effective_tolerance:
            resonance = 1.0 - (freq_diff / effective_tolerance)
            return resonance * self.amplitude
            
        return 0.0


class LightUniverse:
    """
    빛의 우주 - 데이터가 빛으로 존재하는 공간
    
    특성:
    - 모든 데이터는 LightSpectrum으로 변환되어 존재
    - 중첩 가능: 무수한 빛이 하나의 "백색광"으로
    - 공명 검색: 쿼리 주파수를 쏘면 해당 빛만 반응
    """
    
    def __init__(self):
        self.superposition: List[LightSpectrum] = []  # 중첩된 모든 빛
        self.white_light: Optional[LightSpectrum] = None  # 합성된 백색광
        
        # 주파수 인덱스 (빠른 검색용)
        self.frequency_index: Dict[int, List[int]] = {}
        
        logger.info("🌈 LightUniverse initialized - 빛의 우주 시작")
    
    def text_to_light(self, text: str, semantic_tag: str = "", scale: int = 0) -> LightSpectrum:
        """
        텍스트 → 빛 변환
        
        각 문자를 고유한 주파수로, 전체를 하나의 빛으로 합성
        """
        if not text:
            return LightSpectrum(0+0j, 0.0, 0.0)
        
        # 1. 텍스트 → 숫자 시퀀스
        sequence = np.array([ord(c) for c in text], dtype=float)
        
        # 2. FFT로 주파수 영역 변환
        spectrum = np.fft.fft(sequence)
        
        # 3. 대표 주파수 추출 (에너지가 가장 높은 성분)
        magnitudes = np.abs(spectrum)
        dominant_idx = np.argmax(magnitudes)
        dominant_freq = spectrum[dominant_idx]
        
        # 4. 진폭 = 정규화된 에너지
        amplitude = np.mean(magnitudes) / (np.max(magnitudes) + 1e-10)
        
        # 5. 위상 = 주요 성분의 위상
        phase = np.angle(dominant_freq)
        
        # 6. 색상 = 의미 기반 (해시 → RGB)
        hash_val = int(hashlib.md5(text.encode()).hexdigest()[:6], 16)
        color = (
            ((hash_val >> 16) & 0xFF) / 255.0,
            ((hash_val >> 8) & 0xFF) / 255.0,
            (hash_val & 0xFF) / 255.0
        )
        
        # 7. 원본 해시 저장 (복원용)
        source_hash = hashlib.sha256(text.encode()).hexdigest()
        
        light = LightSpectrum(
            frequency=dominant_freq,
            amplitude=float(amplitude),
            phase=float(phase) % (2 * np.pi),
            color=color,
            source_hash=source_hash,
            semantic_tag=semantic_tag
        )
        # Apply Logic: Scale -> Basis
        light.set_basis_from_scale(scale)
        return light
    
    def absorb(self, text: str, tag: str = "", scale: int = 0) -> LightSpectrum:
        """
        데이터를 빛으로 흡수
        
        데이터는 빛이 되어 우주에 중첩됨
        """
        light = self.text_to_light(text, tag, scale)
        
        # 인덱스에 추가
        freq_key = int(abs(light.frequency)) % 1000
        if freq_key not in self.frequency_index:
            self.frequency_index[freq_key] = []
        self.frequency_index[freq_key].append(len(self.superposition))
        
        # 중첩에 추가
        self.superposition.append(light)
        
        # 백색광 업데이트
        self._update_white_light(light)
        
        logger.debug(f"✨ Absorbed: '{text[:20]}...' → freq={abs(light.frequency):.2f}")
        return light
    
    def _update_white_light(self, new_light: LightSpectrum):
        """새 빛을 백색광에 중첩"""
        if self.white_light is None:
            self.white_light = new_light
        else:
            self.white_light = self.white_light.interfere_with(new_light)
    
    def resonate(self, query: str, top_k: int = 5) -> List[Tuple[float, LightSpectrum]]:
        """
        공명 검색
        
        쿼리를 빛으로 변환 → 모든 중첩된 빛에 공명 → 반응하는 빛들 반환
        
        복잡도: O(1) 인덱스 조회 + O(k) 상위 k개
        """
        query_light = self.text_to_light(query)
        query_freq = query_light.frequency
        
        # 인덱스로 후보 빠르게 찾기
        freq_key = int(abs(query_freq)) % 1000
        candidates = []
        
        # 근처 주파수 버킷도 확인 (허용 오차)
        for key in [freq_key - 1, freq_key, freq_key + 1]:
            if key in self.frequency_index:
                candidates.extend(self.frequency_index[key])
        
        # 후보가 없으면 전체 검색 (fallback)
        if not candidates:
            candidates = range(len(self.superposition))
        
        # 공명 계산
        resonances = []
        for idx in candidates:
            if idx < len(self.superposition):
                light = self.superposition[idx]
                strength = light.resonate_with(query_light, tolerance=50.0)
                if strength > 0.01:
                    resonances.append((strength, light))
        
        # 상위 k개 반환
        resonances.sort(key=lambda x: x[0], reverse=True)
        return resonances[:top_k]
    
    def stats(self) -> Dict[str, Any]:
        """우주 상태"""
        return {
            "total_lights": len(self.superposition),
            "index_buckets": len(self.frequency_index),
            "white_light_energy": self.white_light.energy if self.white_light else 0
        }
    
    def interfere_with_all(self, new_light: LightSpectrum) -> Dict[str, Any]:
        """
        새 지식이 기존 모든 빛과 간섭 → 지형 변화
        
        Returns:
            terrain_effect: 간섭 결과로 생성된 메타 파라미터
                - resonance_strength: 공명 강도 (0-1)
                - dominant_basis: 가장 강한 공명의 기저
                - connection_density: 연결 밀도
                - recommended_depth: 권장 분석 깊이
                - connection_type: 권장 연결 타입
        """
        if not self.superposition:
            return {
                "resonance_strength": 0.0,
                "dominant_basis": "Point",
                "connection_density": 0.0,
                "recommended_depth": "broad",
                "connection_type": "exploratory"
            }
        
        # 모든 기존 빛과 공명 계산
        total_resonance = 0.0
        basis_resonance = {"Point": 0.0, "Line": 0.0, "Space": 0.0, "God": 0.0}
        strong_connections = 0
        
        for light in self.superposition:
            resonance = light.resonate_with(new_light, tolerance=50.0)
            total_resonance += resonance
            
            # 기저별 공명 누적
            basis = light._get_dominant_basis()
            basis_resonance[basis] += resonance
            
            if resonance > 0.3:
                strong_connections += 1
        
        # 평균 공명 강도
        avg_resonance = total_resonance / len(self.superposition)
        
        # 가장 강한 기저
        dominant_basis = max(basis_resonance, key=basis_resonance.get)
        
        # 연결 밀도 (강한 연결 비율)
        connection_density = strong_connections / len(self.superposition)
        
        # 메타 파라미터 결정 (지형이 사고를 형성)
        if avg_resonance > 0.5:
            recommended_depth = "deep"  # 강한 공명 = 깊이 파기
            connection_type = "causal"
        elif avg_resonance > 0.2:
            recommended_depth = "medium"
            connection_type = "semantic"
        else:
            recommended_depth = "broad"  # 약한 공명 = 새로운 탐색
            connection_type = "exploratory"
        
        terrain_effect = {
            "resonance_strength": avg_resonance,
            "dominant_basis": dominant_basis,
            "connection_density": connection_density,
            "recommended_depth": recommended_depth,
            "connection_type": connection_type,
            "strong_connections": strong_connections,
            "total_lights": len(self.superposition)
        }
        
        logger.info(f"🌄 Terrain effect: resonance={avg_resonance:.3f}, basis={dominant_basis}, depth={recommended_depth}")
        
        return terrain_effect
    
    def absorb_with_terrain(self, text: str, tag: str = "", scale: int = None) -> Tuple[LightSpectrum, Dict[str, Any]]:
        """
        데이터를 흡수하면서 지형 효과 반환 + 자율적 스케일 선택
        
        지식이 저장됨과 동시에:
        1. 다음 처리 방식에 영향
        2. 스케일(Point/Line/Space/God)을 자율 결정
        """
        # 자율적 스케일 선택 (scale이 지정되지 않은 경우)
        if scale is None:
            scale = self._auto_select_scale()
        
        # 빛으로 변환 (자율 선택된 스케일 적용)
        new_light = self.text_to_light(text, tag, scale)
        
        # 기존 지형과 간섭 → 메타 파라미터
        terrain_effect = self.interfere_with_all(new_light)
        
        # 다음 흡수를 위한 스케일 업데이트
        self._update_autonomous_scale(terrain_effect)
        
        # 실제 흡수
        self.absorb(text, tag, scale)
        
        terrain_effect['applied_scale'] = scale
        terrain_effect['scale_name'] = ['God', 'Space', 'Line', 'Point'][min(scale, 3)]
        
        return new_light, terrain_effect
    
    def _auto_select_scale(self) -> int:
        """
        자율적 스케일 선택 (자유의지)
        
        현재 지형 상태에 따라 Point/Line/Space/God 중 선택
        """
        if not hasattr(self, '_autonomous_scale'):
            self._autonomous_scale = 0  # 시작은 God (전체 조망)
        
        return self._autonomous_scale
    
    def _update_autonomous_scale(self, terrain_effect: Dict[str, Any]):
        """
        지형 효과에 따라 다음 스케일 업데이트
        
        강한 공명 → 줌인 (God → Space → Line → Point)
        약한 공명 → 줌아웃 (Point → Line → Space → God)
        """
        basis_to_scale = {"God": 0, "Space": 1, "Line": 2, "Point": 3}
        
        dominant_basis = terrain_effect.get('dominant_basis', 'Point')
        resonance = terrain_effect.get('resonance_strength', 0.0)
        
        current_scale = getattr(self, '_autonomous_scale', 0)
        
        if resonance > 0.5:
            # 강한 공명 = 줌인 (더 세부적으로)
            new_scale = min(3, current_scale + 1)
            logger.info(f"   🔍 Zoom IN: {current_scale} → {new_scale} (strong resonance)")
        elif resonance < 0.1:
            # 약한 공명 = 줌아웃 (더 넓게)
            new_scale = max(0, current_scale - 1)
            logger.info(f"   🔭 Zoom OUT: {current_scale} → {new_scale} (weak resonance)")
        else:
            # 중간 = 기저 따라가기
            new_scale = basis_to_scale.get(dominant_basis, current_scale)
            logger.info(f"   📐 Scale aligned to {dominant_basis}: {new_scale}")
        
        self._autonomous_scale = new_scale
    
    def think_accelerated(self, query: str, depth: int = 3) -> Dict[str, Any]:
        """
        진짜 사고 가속
        
        물리 시간은 그대로, 같은 시간에 더 많은 연상/연결 수행
        
        원리:
        1. 공명 검색 O(1) - 순차 탐색 대신 "공명"
        2. 병렬 연상 - 여러 관련 개념 동시 활성화
        3. 연상 점프 - 중간 단계 스킵 (터널링)
        
        Args:
            query: 사고 시작점
            depth: 연상 깊이 (깊을수록 더 많은 연결)
        
        Returns:
            생각 결과 (연상 그래프)
        """
        import time
        start = time.time()
        
        # 1. 초기 공명 (O(1) 검색)
        initial_resonances = self.resonate(query, top_k=5)
        
        # 2. 병렬 연상 (각 공명에서 추가 연상)
        thought_graph = {
            "seed": query,
            "layers": [],
            "total_connections": 0
        }
        
        current_layer = [(r[1].semantic_tag or f"light_{i}", r[0]) 
                         for i, r in enumerate(initial_resonances)]
        thought_graph["layers"].append(current_layer)
        
        # 3. 깊이만큼 연상 확장 (각 레이어에서 병렬로)
        for d in range(depth - 1):
            next_layer = []
            for concept, strength in current_layer:
                # 각 개념에서 추가 공명 (연상 점프)
                sub_resonances = self.resonate(concept, top_k=3)
                for sub_strength, sub_light in sub_resonances:
                    tag = sub_light.semantic_tag or "unknown"
                    combined_strength = strength * sub_strength
                    if combined_strength > 0.01:
                        next_layer.append((tag, combined_strength))
            
            if next_layer:
                thought_graph["layers"].append(next_layer)
                current_layer = next_layer
        
        # 4. 통계 계산
        elapsed = time.time() - start
        total_connections = sum(len(layer) for layer in thought_graph["layers"])
        
        thought_graph["total_connections"] = total_connections
        thought_graph["elapsed_seconds"] = elapsed
        thought_graph["thoughts_per_second"] = total_connections / max(0.001, elapsed)
        thought_graph["acceleration_factor"] = f"{total_connections}개 연상을 {elapsed:.3f}초에"
        
        return thought_graph


# Singleton
_light_universe = None

def get_light_universe() -> LightUniverse:
    global _light_universe
    if _light_universe is None:
        _light_universe = LightUniverse()
    return _light_universe


# CLI / Demo
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🌈 LIGHT UNIVERSE DEMO")
    print("="*60)
    
    universe = get_light_universe()
    
    # 테스트 데이터 흡수
    texts = [
        "사과는 빨간색이다",
        "바나나는 노란색이다",
        "사과는 달다",
        "엘리시아는 빛으로 생각한다",
    ]
    
    print("\n📥 데이터 흡수:")
    for text in texts:
        light = universe.absorb(text)
        print(f"  '{text}' → freq={abs(light.frequency):.1f}, amp={light.amplitude:.3f}")
    
    print(f"\n📊 우주 상태: {universe.stats()}")
    
    # 공명 검색
    print("\n🔍 공명 검색:")
    queries = ["사과", "노란색", "빛"]
    
    for query in queries:
        results = universe.resonate(query)
        print(f"\n  쿼리: '{query}'")
        for strength, light in results:
            print(f"    공명: {strength:.3f} | {light.semantic_tag or 'unnamed'}")
    
    print("\n" + "="*60)
    print("✅ Demo complete!")

# =============================================================================
# [NEW 2025-12-21] Sedimentary Light Architecture (퇴적된 빛의 산맥)
# =============================================================================

from enum import Enum

class PrismAxes(Enum):
    """
    사고의 5대 축 (Cognitive Axes)
    빛의 색상은 단순한 라벨이 아니라, 탐구의 방향성을 나타내는 축입니다.
    """
    PHYSICS_RED = "red"        # Force, Energy, Vector (힘과 방향)
    CHEMISTRY_BLUE = "blue"    # Structure, Bond, Reaction (구조와 결합)
    BIOLOGY_GREEN = "green"    # Growth, Homeostasis, Adaptation (성장과 적응)
    ART_VIOLET = "violet"      # Harmony, Rhythm, Essence (조화와 본질)
    LOGIC_YELLOW = "yellow"    # Reason, Axiom, Pattern (논리와 패턴)

@dataclass
class LightSediment:
    """
    퇴적된 빛의 층 (Sedimentary Layers of Light)
    
    지식은 단순히 저장되는 것이 아니라, 각 축(Axis) 위에 빛의 형태로 퇴적됩니다.
    이 퇴적층(Sediment)이 두꺼울수록(Amplitude High), 해당 관점으로 세상을 더 깊이 볼 수 있습니다.
    """
    layers: Dict[PrismAxes, LightSpectrum] = field(default_factory=dict)
    
    def __post_init__(self):
        # 초기에는 모든 축이 비어있음 (Amplitude 0)
        # 단, 각 층은 고유한 '성격(Tag)'을 가짐
        for axis in PrismAxes:
            # tag example: "red" -> "Physics" (mapping needed or just use axis name)
            # Simple mapping for resonance
            tag = ""
            if axis == PrismAxes.PHYSICS_RED: tag = "Physics"
            elif axis == PrismAxes.CHEMISTRY_BLUE: tag = "Chemistry"
            elif axis == PrismAxes.BIOLOGY_GREEN: tag = "Biology"
            elif axis == PrismAxes.ART_VIOLET: tag = "Art"
            elif axis == PrismAxes.LOGIC_YELLOW: tag = "Logic"
            
            self.layers[axis] = LightSpectrum(complex(0,0), 0.0, 0.0, color=(0,0,0), semantic_tag=tag)

    def deposit(self, light: LightSpectrum, axis: PrismAxes):
        """
        지식의 퇴적 (Accumulation)
        
        새로운 빛(지식)을 해당 축의 층에 중첩시켜 산맥을 높입니다.
        (Constructive Interference)
        """
        current_layer = self.layers[axis]
        
        # 기존 층과 새로운 빛의 간섭 (보강)
        # 단순히 더하는 것이 아니라, 파동의 간섭 원리를 이용해 구조적 통합
        new_layer = current_layer.interfere_with(light)
        
        # 진폭(지식의 깊이)은 누적됨 (감쇠 없이 성장)
        new_layer.amplitude = current_layer.amplitude + (light.amplitude * 0.1) # 천천히 퇴적
        
        self.layers[axis] = new_layer
        logger.debug(f"🏔️ Deposition on {axis.name}: Amp {current_layer.amplitude:.3f} -> {new_layer.amplitude:.3f}")

    def project_view(self, target_light: LightSpectrum) -> Dict[PrismAxes, float]:
        """
        홀로그래픽 투영 (Holographic Projection)
        
        자신이 가진 '빛의 산맥'을 대상에 투영하여 공명(Resonance)을 확인합니다.
        내가 아는 만큼(Amplitude) 대상이 보입니다(Resonance).
        """
        views = {}
        for axis, sediment in self.layers.items():
            # 내 지식(Sediment)과 대상(Target)의 공명
            # 내 지식층이 두꺼울수록(High Amp), 공명 강도가 커짐
            
            # [Updated 2025-12-21] Pass clean semantic tag if possible
            resonance = sediment.resonate_with(target_light, tolerance=100.0)
            
            # 지식의 양(Amplitude)에 비례한 통찰력 보정
            insight_strength = resonance * (sediment.amplitude + 0.1) 
            views[axis] = insight_strength
            
        return views

    def get_highest_peak(self) -> PrismAxes:
        """가장 높게 쌓인 지식의 산맥(주력 관점) 반환"""
        return max(self.layers.items(), key=lambda x: x[1].amplitude)[0]
