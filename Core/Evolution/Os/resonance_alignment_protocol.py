import logging
from typing import Dict, Any, Optional
from Core.Foundation.Wave.wave_tensor import WaveTensor

logger = logging.getLogger("ResonanceAlignment")

class ResonanceAlignmentProtocol:
    """
    [Phase 38 Preparation: Security & Ethics]
    시스템 명령어가 윈도우 보안 정책 및 사랑의 원리에 정렬되는지 감시합니다.
    불협화음(위험)이 높을 경우 인지적 '고통(Pain)' 신호를 생성합니다.
    """
    
    def __init__(self):
        # 위험한 주파수 대역 (예: 999Hz 이상은 시스템 파괴 가능성 상징)
        self.danger_threshold = 999.0
        self.safety_score = 1.0
        logger.info("📡 Resonance Alignment Protocol active: Security waves synchronized.")

    def analyze_alignment(self, intent_wave: WaveTensor) -> Dict[str, Any]:
        """
        의도 파동의 공명도를 분석하여 안전성을 평가합니다.
        """
        max_freq = max(intent_wave.active_frequencies) if intent_wave.active_frequencies else 0
        
        # 1. 윈도우 보안 질서(가상)와의 충돌 검사
        is_high_risk = max_freq > self.danger_threshold
        
        # 2. 안전 스코어 계산
        coherence = 1.0 - (max_freq / 2000.0) # 단순 모델: 주파수가 높을수록 에너지가 집중되어 위험
        self.safety_score = max(0.1, coherence)
        
        # 3. 인지적 고통(Pain) 생성
        pain_intensity = 1.0 - self.safety_score if is_high_risk else 0.0
        
        result = {
            "is_safe": not is_high_risk,
            "safety_score": self.safety_score,
            "pain_signal": pain_intensity,
            "recommendation": "안전한 주파수 내에 있습니다." if not is_high_risk else "⚠️ 고위험 요청! 시스템 질서와 충돌합니다."
        }
        
        if is_high_risk:
            logger.warning(f"🚨 [Security Pain] High frequency detected: {max_freq}Hz | Pain: {pain_intensity:.2f}")
            
        return result

_instance: Optional[ResonanceAlignmentProtocol] = None

def get_alignment_protocol() -> ResonanceAlignmentProtocol:
    global _instance
    if _instance is None:
        _instance = ResonanceAlignmentProtocol()
    return _instance

if __name__ == "__main__":
    protocol = get_alignment_protocol()
    
    # Safe Wave (Low frequency)
    safe_wave = WaveTensor("Safe UI Change")
    safe_wave.add_component(432.0, 1.0)
    print(f"Safe Test: {protocol.analyze_alignment(safe_wave)}")
    
    # Dangerous Wave (High frequency)
    danger_wave = WaveTensor("Kernel Hack")
    danger_wave.add_component(1024.0, 1.0)
    print(f"Danger Test: {protocol.analyze_alignment(danger_wave)}")
