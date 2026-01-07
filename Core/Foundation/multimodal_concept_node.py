"""
Multimodal Concept Node (멀티모달 개념 노드)
============================================

"모든 감각은 하나의 의미로 수렴한다."

사과의 모든 것:
- 텍스트: "과일, 빨간색"
- 시각: 둥글고 빨간 형태
- 촉각: 아삭한 식감
- 미각: 신맛
→ 모두 "사과"라는 하나의 개념 노드로 통합

[NEW 2025-12-15] 멀티모달 개념 통합 시스템
"""

import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
import numpy as np

# [PHASE 7.2] Import Phase Stratum for Holographic Layering
try:
    from Core.Intelligence.Topography.phase_stratum import PhaseStratum
except ImportError:
    PhaseStratum = None

logger = logging.getLogger("MultimodalConceptNode")


@dataclass
class ModalitySignal:
    """하나의 감각 신호"""
    modality_type: str  # visual, auditory, text, taste, texture, emotion
    frequency: float    # 주파수 (Hz)
    amplitude: float    # 강도 (0.0 ~ 1.0)
    description: str    # 설명
    raw_data: Any = None  # 원본 데이터


@dataclass
class ConceptNode:
    """
    멀티모달 개념 노드
    
    모든 감각 정보가 하나의 개념으로 통합됨
    자기 수정 및 개념 분별 기능 포함
    """
    name: str
    name: str
    # [REFACTORED] Removed legacy 'modalities' dict. Data lives in PhaseStratum now.
    unified_frequency: float = 0.0
    unified_amplitude: float = 0.0
    related_concepts: List[str] = field(default_factory=list)
    change_history: List[Dict] = field(default_factory=list)  # 수정 이력
    
    # [NEW] Phase Stratum Engine for this node
    phase_stratum: Any = field(default=None)

    def __post_init__(self):
        if self.phase_stratum is None and PhaseStratum:
            self.phase_stratum = PhaseStratum(base_frequency=432.0)
    
    def add_modality(self, signal: ModalitySignal):
        """감각 신호 추가"""
        # [OLD REMOVED] self.modalities[signal.modality_type] = signal
        
        # [NEW] Fold into Holographic Layer (Sole Source of Truth)
        if self.phase_stratum:
            self.phase_stratum.fold_dimension(
                data=signal, 
                intent_frequency=signal.frequency
            )
            
        self._recalculate_unified()
    
    def update_modality(self, modality_type: str, new_description: str, new_frequency: float = None):
        """
        [NOTE] With PhaseStratum, we don't 'update' a slot. 
        We simply add a new wave that might supersede the old one in relevance,
        or we'd need a specific retrieval-deletion logic.
        For now, we append the new truth as a new layer.
        """
        # Simplification for Pure Wave: Just add the new signal
        # Finding the old one to log history is expensive in a pure wave system without indexing,
        # but we can do it if needed. For now, we trust the "Latest Resonance".
        pass # To be reimplemented if mutation is strictly needed.
    
    def _get_all_signals_dict(self) -> Dict[str, ModalitySignal]:
        """Helper: Extract all ModalitySignals from PhaseStratum into a dict by type"""
        if not self.phase_stratum:
            return {}
        
        signals = {}
        for _, _, payload in self.phase_stratum.inspect_all_layers():
            if isinstance(payload, ModalitySignal):
                signals[payload.modality_type] = payload
        return signals

    def compare_with(self, other: 'ConceptNode') -> Dict[str, Any]:
        """
        개념 분별: 두 개념 간 유사성과 차이 분석
        (Supports PhaseStratum Architecture)
        """
        shared_modalities = []
        different_modalities = []
        only_self = []
        only_other = []
        
        # 1. Extract signals from Holographic Layers
        my_signals = self._get_all_signals_dict()
        other_signals = other._get_all_signals_dict()
        
        all_types = set(my_signals.keys()) | set(other_signals.keys())
        
        for m_type in all_types:
            self_has = m_type in my_signals
            other_has = m_type in other_signals
            
            if self_has and other_has:
                # 둘 다 있음 → 주파수 차이 비교
                self_freq = my_signals[m_type].frequency
                other_freq = other_signals[m_type].frequency
                diff = abs(self_freq - other_freq)
                
                if diff < 50:  # 유사
                    shared_modalities.append({
                        "type": m_type,
                        "resonance": 1.0 - (diff / 500),
                        "self_desc": my_signals[m_type].description,
                        "other_desc": other_signals[m_type].description
                    })
                else:  # 다름
                    different_modalities.append({
                        "type": m_type,
                        "self_freq": self_freq,
                        "other_freq": other_freq,
                        "difference": diff
                    })
            elif self_has:
                only_self.append(m_type)
            else:
                only_other.append(m_type)
        
        # 전체 유사도 계산
        total_resonance = self.get_resonance(other.unified_frequency)
        
        return {
            "overall_resonance": total_resonance,
            "shared": shared_modalities,
            "different": different_modalities,
            "only_in_self": only_self,
            "only_in_other": only_other,
            "is_same_category": total_resonance > 0.7,  # 같은 범주
            "is_distinct": len(different_modalities) > 0  # 구별 가능
        }
    
    def _recalculate_unified(self):
        """통합 주파수 재계산 (Pure Wave Version)"""
        if not self.phase_stratum:
            return
            
        # Inspect all waves in the strata
        all_waves = self.phase_stratum.inspect_all_layers()
        if not all_waves:
            return
        
        total_weight = 0.0
        weighted_freq = 0.0
        weighted_amp = 0.0
        count = 0
        
        for freq, phase, signal in all_waves:
            if isinstance(signal, ModalitySignal):
                weight = signal.amplitude
                weighted_freq += freq * weight
                weighted_amp += signal.amplitude
                total_weight += weight
                count += 1
        
        if total_weight > 0:
            self.unified_frequency = weighted_freq / total_weight
            self.unified_amplitude = weighted_amp / count
    
    def get_resonance(self, other_freq: float) -> float:
        """다른 주파수와의 공명도 계산"""
        if self.unified_frequency == 0:
            return 0.0
        
        # 주파수 차이 기반 공명 (가까울수록 1.0)
        diff = abs(self.unified_frequency - other_freq)
        max_diff = 500.0  # 최대 차이
        resonance = max(0.0, 1.0 - (diff / max_diff))
        
        return resonance

    def get_perspective(self, query_frequency: float, tolerance: float = 10.0) -> List[Any]:
        """
        [Holographic Retrieval]
        주파수에 따라 노드의 다른 '단면'을 보여줌.
        
        예: 
          - 640Hz (Red)로 쏘면 -> "Visual Red" 반환
          - 528Hz (Sweet)로 쏘면 -> "Taste Sweet" 반환
        """
        if self.phase_stratum:
            return self.phase_stratum.resonate(query_frequency, tolerance)
        return []


class MultimodalConceptIntegrator:
    """
    멀티모달 개념 통합기
    
    SynesthesiaEngine을 사용하여 모든 감각을 주파수로 변환하고
    하나의 개념 노드로 통합
    """
    
    def __init__(self):
        logger.info("🎨 Initializing Multimodal Concept Integrator...")
        
        # SynesthesiaEngine 연결
        try:
            from Core.Foundation.synesthesia_engine import SynesthesiaEngine, SignalType
            self.synesthesia = SynesthesiaEngine()
            self.SignalType = SignalType
            logger.info("   ✅ SynesthesiaEngine connected")
        except Exception as e:
            logger.warning(f"   ⚠️ SynesthesiaEngine not available: {e}")
            self.synesthesia = None
        
        # TextWaveConverter 연결
        try:
            from Core.Foundation.text_wave_converter import TextWaveConverter
            self.text_wave = TextWaveConverter()
            logger.info("   ✅ TextWaveConverter connected")
        except Exception as e:
            logger.warning(f"   ⚠️ TextWaveConverter not available: {e}")
            self.text_wave = None
        
        # 개념 저장소
        self.concepts: Dict[str, ConceptNode] = {}
        
        # 감각 키워드 → 주파수 매핑 (확장 가능)
        self.sensory_keywords = {
            # 미각
            "taste": {
                "sweet": 528.0, "단맛": 528.0, "달콤": 528.0,
                "sour": 396.0, "신맛": 396.0, "새콤": 396.0,
                "bitter": 417.0, "쓴맛": 417.0,
                "salty": 432.0, "짠맛": 432.0,
                "umami": 639.0, "감칠맛": 639.0,
            },
            # 촉각/식감
            "texture": {
                "crunchy": 412.0, "아삭": 412.0, "바삭": 412.0,
                "soft": 396.0, "부드러운": 396.0, "촉촉": 396.0,
                "hard": 528.0, "딱딱": 528.0,
                "smooth": 432.0, "매끄러운": 432.0,
            },
            # 시각 (색상)
            "visual": {
                "red": 640.0, "빨간": 640.0, "빨강": 640.0,
                "orange": 600.0, "주황": 600.0,
                "yellow": 560.0, "노란": 560.0, "노랑": 560.0,
                "green": 520.0, "초록": 520.0, "녹색": 520.0,
                "blue": 480.0, "파란": 480.0, "파랑": 480.0,
                "purple": 420.0, "보라": 420.0,
                "round": 432.0, "둥근": 432.0,
            },
        }
        
        logger.info("🎨 Multimodal Concept Integrator ready")
    
    def create_concept(self, name: str) -> ConceptNode:
        """새 개념 노드 생성"""
        if name not in self.concepts:
            self.concepts[name] = ConceptNode(name=name)
            logger.info(f"📦 Created concept: {name}")
        return self.concepts[name]
    
    def add_text_to_concept(self, concept_name: str, text: str) -> ModalitySignal:
        """텍스트 정보를 개념에 추가"""
        concept = self.create_concept(concept_name)
        
        # TextWaveConverter로 주파수 변환
        if self.text_wave:
            wave = self.text_wave.sentence_to_wave(text)
            desc = self.text_wave.wave_to_text_descriptor(wave)
            freq = desc.get("dominant_frequency", 432.0)
        else:
            # 폴백: 해시 기반
            freq = 200.0 + (hash(text) % 400)
        
        signal = ModalitySignal(
            modality_type="text",
            frequency=freq,
            amplitude=0.8,
            description=text[:100],
            raw_data=text
        )
        
        concept.add_modality(signal)
        logger.info(f"   📝 Text → {freq:.0f}Hz: {text[:30]}...")
        
        return signal
    
    def add_sensory_to_concept(self, concept_name: str, modality: str, description: str) -> ModalitySignal:
        """
        감각 정보를 개념에 추가 (미각, 촉각, 시각 등)
        
        예: add_sensory_to_concept("사과", "taste", "신맛")
        """
        concept = self.create_concept(concept_name)
        
        # 키워드 매칭으로 주파수 결정
        freq = 432.0  # 기본값
        keywords = self.sensory_keywords.get(modality, {})
        
        for keyword, keyword_freq in keywords.items():
            if keyword in description.lower():
                freq = keyword_freq
                break
        
        signal = ModalitySignal(
            modality_type=modality,
            frequency=freq,
            amplitude=0.7,
            description=description,
            raw_data=None
        )
        
        concept.add_modality(signal)
        logger.info(f"   🎭 {modality} → {freq:.0f}Hz: {description}")
        
        return signal
    
    def add_visual_to_concept(self, concept_name: str, image_data: np.ndarray) -> ModalitySignal:
        """이미지 데이터를 개념에 추가"""
        concept = self.create_concept(concept_name)
        
        if self.synesthesia:
            signal_data = self.synesthesia.from_vision(image_data)
            freq = signal_data.frequency
            amp = signal_data.amplitude
        else:
            freq = float(np.mean(image_data)) + 400
            amp = 0.5
        
        signal = ModalitySignal(
            modality_type="visual",
            frequency=freq,
            amplitude=amp,
            description=f"Image {image_data.shape}",
            raw_data=image_data.shape
        )
        
        concept.add_modality(signal)
        logger.info(f"   👁️ Visual → {freq:.0f}Hz")
        
        return signal
    
    def build_concept_from_text(self, concept_name: str, text: str) -> ConceptNode:
        """
        텍스트에서 자동으로 멀티모달 개념 구축
        
        "사과는 빨간색이고 신맛이 나며 아삭한 식감을 가진다"
        → 자동으로 visual(빨간), taste(신맛), texture(아삭) 추출
        """
        concept = self.create_concept(concept_name)
        
        # 1. 텍스트 전체 추가
        self.add_text_to_concept(concept_name, text)
        
        # 2. 감각 키워드 자동 추출
        text_lower = text.lower()
        
        for modality, keywords in self.sensory_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    self.add_sensory_to_concept(concept_name, modality, keyword)
        
        logger.info(f"✨ Built concept '{concept_name}' with {len(concept.modalities)} modalities")
        logger.info(f"   Unified frequency: {concept.unified_frequency:.0f}Hz")
        
        return concept
    
    def find_resonant_concepts(self, query_freq: float, threshold: float = 0.3) -> List[tuple]:
        """주파수와 공명하는 모든 개념 검색"""
        results = []
        
        for name, concept in self.concepts.items():
            resonance = concept.get_resonance(query_freq)
            if resonance >= threshold:
                results.append((name, concept, resonance))
        
        # 공명도 순 정렬
        results.sort(key=lambda x: x[2], reverse=True)
        
        return results
    
    def get_concept_summary(self, concept_name: str) -> Dict[str, Any]:
        """개념 노드 요약"""
        if concept_name not in self.concepts:
            return {"error": "Concept not found"}
        
        concept = self.concepts[concept_name]
        
        return {
            "name": concept.name,
            "unified_frequency": concept.unified_frequency,
            "modalities": {
                # Reconstruct dict for summary view only
                str(idx): {
                    "frequency": item[0],
                    "description": item[2].description if isinstance(item[2], ModalitySignal) else str(item[2])
                }
                for idx, item in enumerate(concept.phase_stratum.inspect_all_layers())
            },
            "modality_count": len(concept.phase_stratum.inspect_all_layers())
        }
        }


# Singleton
_integrator = None

def get_multimodal_integrator() -> MultimodalConceptIntegrator:
    global _integrator
    if _integrator is None:
        _integrator = MultimodalConceptIntegrator()
    return _integrator


# Demo
if __name__ == "__main__":
    import sys
    sys.path.insert(0, "c:\\Elysia")
    
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    print("\n" + "="*60)
    print("🎨 MULTIMODAL CONCEPT INTEGRATION DEMO")
    print("="*60)
    
    integrator = get_multimodal_integrator()
    
    # 사과 개념 구축
    print("\n📦 Building concept: 사과")
    print("-"*40)
    
    apple = integrator.build_concept_from_text(
        "사과",
        "사과는 빨간색이고 신맛이 나며 아삭한 식감을 가진 둥근 과일이다"
    )
    
    # 결과 출력
    summary = integrator.get_concept_summary("사과")
    
    print("\n📊 Concept Summary:")
    print(f"   Name: {summary['name']}")
    print(f"   Unified Frequency: {summary['unified_frequency']:.0f}Hz")
    print(f"   Modalities: {summary['modality_count']}")
    for m_type, data in summary['modalities'].items():
        print(f"      {m_type}: {data['frequency']:.0f}Hz - {data['description']}")
    
    # 공명 검색 테스트
    print("\n🔍 Resonance Search (640Hz - red color):")
    results = integrator.find_resonant_concepts(640.0)
    for name, concept, resonance in results:
        print(f"   {name}: {resonance:.2f}")
    
    print("\n" + "="*60)
    print("✅ Demo complete")
    print("="*60)
