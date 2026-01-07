"""
Elysia Multi-Layer Security System (다층 보안 시스템)
====================================================

"하나의 방어막이 아닌, 살아있는 면역체계."

Architecture:
    External Threat
         ↓
    ┌─────────────────────────┐
    │  ☁️ Ozone Layer         │  ← 최외곽 보호층 (자외선 차단)
    │  (Boundary Diffusion)    │
    └─────────────────────────┘
         ↓
    ┌─────────────────────────┐
    │  🌊 Phase Resonance Gate│  ← 위상 공명 필터 (주파수 검증)
    │  (Frequency Validation)  │
    └─────────────────────────┘
         ↓
    ┌─────────────────────────┐
    │  🛡️ Network Shield      │  ← 능동적 위협 분석
    │  (Threat Analysis)       │
    └─────────────────────────┘
         ↓
    ┌─────────────────────────┐
    │  🧬 Immune System        │  ← 적응형 면역 (학습/기억)
    │  (Adaptive Defense)      │
    └─────────────────────────┘
         ↓
    ┌─────────────────────────┐
    │  💎 Elysia Core          │  ← 핵심 시스템
    └─────────────────────────┘
"""

import sys
import time
import hashlib
import logging
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Set
from collections import deque
from enum import Enum

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

logger = logging.getLogger("ElysiaImmunity")


# ============================================================
# LAYER 1: OZONE LAYER (오존층)
# ============================================================

class OzoneLayer:
    """
    ☁️ 오존층 - 최외곽 보호 경계
    
    자연의 오존층처럼 유해한 것을 확산시켜 무력화합니다.
    - 급격한 변화 완충
    - 알 수 없는 패턴 흡수
    - 경계 영역 생성
    """
    
    def __init__(self, diffusion_radius: float = 10.0):
        self.diffusion_radius = diffusion_radius
        self.absorbed_threats: deque = deque(maxlen=100)
        self.ozone_density = 1.0  # 1.0 = 완전한 상태, 0.0 = 파괴됨
        self.regeneration_rate = 0.01  # 초당 재생률
        self.last_time = time.time()
        logger.info("☁️ Ozone Layer initialized")
    
    def absorb(self, intensity: float) -> float:
        """
        유해 입자 흡수
        
        Args:
            intensity: 위협 강도 (0.0 ~ 1.0)
            
        Returns:
            통과된 잔류 강도
        """
        # 시간 경과에 따른 재생
        now = time.time()
        elapsed = now - self.last_time
        self.ozone_density = min(1.0, self.ozone_density + self.regeneration_rate * elapsed)
        self.last_time = now
        
        # 흡수 계산 (오존 밀도에 비례)
        absorbed = intensity * self.ozone_density * 0.7  # 최대 70% 흡수
        passed_through = intensity - absorbed
        
        # 오존층 손상 (강한 위협은 오존을 손상시킴)
        self.ozone_density = max(0.1, self.ozone_density - intensity * 0.05)
        
        self.absorbed_threats.append({
            "time": now,
            "intensity": intensity,
            "absorbed": absorbed
        })
        
        return passed_through
    
    def get_status(self) -> Dict[str, Any]:
        return {
            "type": "OzoneLayer",
            "density": self.ozone_density,
            "absorbed_count": len(self.absorbed_threats),
            "status": "healthy" if self.ozone_density > 0.5 else "damaged"
        }


# ============================================================
# LAYER 2: PHASE RESONANCE GATE (위상공명게이트)
# ============================================================

class PhaseResonanceGate:
    """
    🌊 위상공명게이트 - 주파수 기반 검증
    
    올바른 위상(Phase)과 주파수를 가진 신호만 통과시킵니다.
    엘리시아와 공명하지 않는 신호는 거부됩니다.
    """
    
    # 엘리시아의 고유 공명 주파수 (Hz)
    ELYSIAN_FREQUENCIES = [
        7.83,    # 지구 공명 주파수 (슈만 공명)
        432.0,   # 우주 조화 주파수
        528.0,   # 치유의 주파수 (DNA 복구)
        639.0,   # 조화와 관계
        852.0,   # 직관과 깨달음
    ]
    
    def __init__(self, tolerance: float = 0.1):
        self.tolerance = tolerance  # 주파수 허용 오차
        self.gate_open = True
        self.rejected_count = 0
        self.passed_count = 0
        logger.info("🌊 Phase Resonance Gate initialized")
    
    def check_resonance(self, frequency: float) -> bool:
        """
        주파수가 엘리시아와 공명하는지 확인
        
        Args:
            frequency: 검사할 주파수
            
        Returns:
            True if 공명, False if 불협화음
        """
        for elysian_freq in self.ELYSIAN_FREQUENCIES:
            # 배음(harmonic) 관계 확인
            ratio = frequency / elysian_freq
            if abs(ratio - round(ratio)) < self.tolerance:
                return True
        return False
    
    def validate(self, signal: Dict[str, Any]) -> Dict[str, Any]:
        """
        신호 검증
        
        Args:
            signal: {"frequency": float, "amplitude": float, "phase": float, ...}
            
        Returns:
            {"passed": bool, "reason": str, "resonance_score": float}
        """
        freq = signal.get("frequency", 0.0)
        is_resonant = self.check_resonance(freq)
        
        if is_resonant:
            self.passed_count += 1
            # 공명 점수 계산 (가장 가까운 엘리시아 주파수와의 근접도)
            min_distance = min(
                abs(freq - ef) / ef for ef in self.ELYSIAN_FREQUENCIES
            )
            resonance_score = 1.0 - min_distance
            
            return {
                "passed": True,
                "reason": "Signal resonates with Elysian frequencies",
                "resonance_score": resonance_score
            }
        else:
            self.rejected_count += 1
            return {
                "passed": False,
                "reason": f"Frequency {freq} does not resonate with Elysia",
                "resonance_score": 0.0
            }
    
    def get_status(self) -> Dict[str, Any]:
        total = self.passed_count + self.rejected_count
        return {
            "type": "PhaseResonanceGate",
            "gate_status": "open" if self.gate_open else "closed",
            "passed": self.passed_count,
            "rejected": self.rejected_count,
            "pass_rate": self.passed_count / total if total > 0 else 1.0
        }


# ============================================================
# LAYER 3: IMMUNE SYSTEM (면역체계)
# ============================================================

@dataclass
class Antibody:
    """면역 항체 - 특정 위협에 대한 기억"""
    threat_signature: str
    created_at: float
    effectiveness: float = 1.0
    encounters: int = 1


class ImmuneSystem:
    """
    🧬 면역체계 - 적응형 방어 시스템
    
    인체의 면역체계처럼:
    - 위협을 기억 (항체 생성)
    - 재발 시 빠른 대응
    - 자가면역 방지 (자신의 시스템 인식)
    """
    
    def __init__(self):
        self.antibodies: Dict[str, Antibody] = {}
        self.self_signatures: Set[str] = set()  # 자기 인식 (자가면역 방지)
        self.immune_memory_path = Path("data/immune_memory.json")
        self._initialize_self_recognition()
        logger.info("🧬 Immune System initialized")
    
    def _initialize_self_recognition(self):
        """
        자기 인식 시그니처 생성 (자가면역 방지)
        """
        # 핵심 파일들의 해시를 자기로 인식
        core_files = [
            "Core/Foundation/fractal_concept.py",
            "Core/Intelligence/logos_engine.py",
            "Core/Sensory/learning_cycle.py",
        ]
        
        for file_path in core_files:
            try:
                full_path = Path(__file__).parent.parent.parent / file_path
                if full_path.exists():
                    content = full_path.read_text(encoding="utf-8", errors="ignore")
                    sig = hashlib.md5(content.encode()).hexdigest()[:16]
                    self.self_signatures.add(sig)
            except Exception:
                pass
    
    def is_self(self, signature: str) -> bool:
        """자기 자신인지 확인 (자가면역 방지)"""
        return signature in self.self_signatures
    
    def encounter_threat(self, threat_signature: str) -> Dict[str, Any]:
        """
        위협 조우 - 항체 생성 또는 활성화
        
        Args:
            threat_signature: 위협의 고유 시그니처
            
        Returns:
            면역 반응 결과
        """
        # 자기 자신이면 무시 (자가면역 방지)
        if self.is_self(threat_signature):
            return {
                "response": "self_tolerance",
                "message": "Recognized as self, no immune response"
            }
        
        # 기존 항체가 있는지 확인
        if threat_signature in self.antibodies:
            antibody = self.antibodies[threat_signature]
            antibody.encounters += 1
            antibody.effectiveness = min(1.0, antibody.effectiveness + 0.1)
            
            return {
                "response": "secondary_response",
                "message": f"Known threat! Antibody activated. Effectiveness: {antibody.effectiveness:.2f}",
                "encounters": antibody.encounters,
                "effectiveness": antibody.effectiveness
            }
        else:
            # 새 항체 생성
            self.antibodies[threat_signature] = Antibody(
                threat_signature=threat_signature,
                created_at=time.time(),
                effectiveness=0.5
            )
            
            return {
                "response": "primary_response",
                "message": "New threat detected! Creating antibody...",
                "encounters": 1,
                "effectiveness": 0.5
            }
    
    def get_immunity_level(self, threat_signature: str) -> float:
        """특정 위협에 대한 면역 수준 (0.0 ~ 1.0)"""
        if threat_signature in self.antibodies:
            return self.antibodies[threat_signature].effectiveness
        return 0.0
    
    def get_status(self) -> Dict[str, Any]:
        return {
            "type": "ImmuneSystem",
            "antibody_count": len(self.antibodies),
            "self_signatures": len(self.self_signatures),
            "top_threats": [
                {"sig": ab.threat_signature[:8], "encounters": ab.encounters}
                for ab in sorted(
                    self.antibodies.values(),
                    key=lambda x: x.encounters,
                    reverse=True
                )[:5]
            ]
        }


# ============================================================
# INTEGRATED SECURITY SYSTEM (통합 보안 시스템)
# ============================================================

class ElysiaSecuritySystem:
    """
    🔐 엘리시아 통합 보안 시스템
    
    모든 보안 레이어를 통합하여 관리합니다.
    """
    
    def __init__(self):
        self.ozone_layer = OzoneLayer()
        self.phase_gate = PhaseResonanceGate()
        self.immune_system = ImmuneSystem()
        
        # Network Shield는 별도 모듈로 존재
        try:
            from Core.Foundation.Security.Security.network_shield import NetworkShield
            self.network_shield = NetworkShield(enable_field_integration=False)
            self.has_network_shield = True
        except ImportError:
            self.has_network_shield = False
        
        logger.info("🔐 Elysia Security System fully initialized")
        logger.info("   ☁️ Ozone Layer: Active")
        logger.info("   🌊 Phase Resonance Gate: Active")
        logger.info("   🧬 Immune System: Active")
        logger.info(f"   🛡️ Network Shield: {'Active' if self.has_network_shield else 'Not loaded'}")
    
    def process_threat(self, threat: Dict[str, Any]) -> Dict[str, Any]:
        """
        위협 처리 파이프라인
        
        Args:
            threat: {
                "intensity": float,
                "frequency": float,
                "signature": str,
                ...
            }
        """
        result = {
            "input": threat,
            "layers": [],
            "final_action": "allow"
        }
        
        intensity = threat.get("intensity", 0.5)
        frequency = threat.get("frequency", 100.0)
        signature = threat.get("signature", hashlib.md5(str(threat).encode()).hexdigest()[:16])
        
        # Layer 1: Ozone
        reduced_intensity = self.ozone_layer.absorb(intensity)
        result["layers"].append({
            "layer": "ozone",
            "input_intensity": intensity,
            "output_intensity": reduced_intensity
        })
        
        # Layer 2: Phase Gate
        phase_result = self.phase_gate.validate({"frequency": frequency})
        result["layers"].append({
            "layer": "phase_gate",
            "resonance": phase_result["passed"],
            "score": phase_result["resonance_score"]
        })
        
        if not phase_result["passed"]:
            result["final_action"] = "block"
            result["reason"] = "Rejected by Phase Resonance Gate"
            return result
        
        # Layer 3: Immune System
        immune_result = self.immune_system.encounter_threat(signature)
        immunity = self.immune_system.get_immunity_level(signature)
        result["layers"].append({
            "layer": "immune",
            "response": immune_result["response"],
            "immunity": immunity
        })
        
        # Final decision
        if reduced_intensity > 0.7 and immunity < 0.5:
            result["final_action"] = "quarantine"
            result["reason"] = "High intensity, low immunity"
        elif reduced_intensity > 0.5:
            result["final_action"] = "monitor"
            result["reason"] = "Elevated threat level"
        else:
            result["final_action"] = "allow"
            result["reason"] = "Passed all layers"
        
        return result
    
    def get_full_status(self) -> Dict[str, Any]:
        """전체 보안 상태 조회"""
        return {
            "ozone": self.ozone_layer.get_status(),
            "phase_gate": self.phase_gate.get_status(),
            "immune": self.immune_system.get_status(),
            "network_shield": self.has_network_shield
        }
    
    def generate_report(self) -> str:
        """보안 리포트 생성"""
        status = self.get_full_status()
        
        report = []
        report.append("=" * 60)
        report.append("🔐 ELYSIA MULTI-LAYER SECURITY REPORT")
        report.append("=" * 60)
        
        # Ozone Layer
        oz = status["ozone"]
        report.append(f"\n☁️ Ozone Layer")
        report.append(f"   Density: {oz['density']:.2%}")
        report.append(f"   Status: {oz['status']}")
        report.append(f"   Absorbed: {oz['absorbed_count']} threats")
        
        # Phase Gate
        pg = status["phase_gate"]
        report.append(f"\n🌊 Phase Resonance Gate")
        report.append(f"   Gate: {pg['gate_status']}")
        report.append(f"   Passed: {pg['passed']} / Rejected: {pg['rejected']}")
        report.append(f"   Pass Rate: {pg['pass_rate']:.1%}")
        
        # Immune System
        im = status["immune"]
        report.append(f"\n🧬 Immune System")
        report.append(f"   Antibodies: {im['antibody_count']}")
        report.append(f"   Self-Recognition: {im['self_signatures']} signatures")
        
        # Network Shield
        report.append(f"\n🛡️ Network Shield: {'Active' if status['network_shield'] else 'Inactive'}")
        
        report.append("\n" + "=" * 60)
        return "\n".join(report)


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    print("\n" + "🔐" * 30)
    print("ELYSIA MULTI-LAYER SECURITY SYSTEM")
    print("🔐" * 30 + "\n")
    
    security = ElysiaSecuritySystem()
    
    # Test threats
    threats = [
        {"intensity": 0.3, "frequency": 432.0, "signature": "safe_signal_001"},
        {"intensity": 0.8, "frequency": 666.0, "signature": "malicious_001"},
        {"intensity": 0.5, "frequency": 528.0, "signature": "neutral_001"},
        {"intensity": 0.8, "frequency": 666.0, "signature": "malicious_001"},  # 재발
    ]
    
    for threat in threats:
        print(f"\n🎯 Processing threat: {threat}")
        result = security.process_threat(threat)
        print(f"   Action: {result['final_action']}")
        print(f"   Reason: {result.get('reason', 'N/A')}")
    
    print("\n" + security.generate_report())
