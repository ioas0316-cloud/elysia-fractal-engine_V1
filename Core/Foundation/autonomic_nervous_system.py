"""
Autonomic Nervous System (자율신경계)
=====================================

의식적 선택이 필요 없는 배경 프로세스

인간의 자율신경계처럼:
- 심장 박동 (상시)
- 호흡 (상시)
- 기억 정리 (수면 중)
- 면역 (배경)

여기에 포함되는 것:
- EntropySink: 엔트로피 처리
- MemoryConsolidation: 기억 정리 (꿈)
- SurvivalInstinct: 생존 본능
- ResonanceDecay: 공명 감쇠

여기에 포함되지 않는 것 (CNS 담당):
- ThoughtSpace: 발산적 사고
- FractalLoop: 의식적 처리
- 선택, 집중, 주권
"""

import logging
import time
import threading
from typing import List, Any, Dict, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod

logger = logging.getLogger("Elysia.ANS")


class AutonomicSubsystem(ABC):
    """자율신경계 하위 시스템의 추상 클래스"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """시스템 이름"""
        pass
    
    @abstractmethod
    def pulse(self) -> Dict[str, Any]:
        """
        배경 펄스 실행
        
        Returns:
            실행 결과 (상태, 처리량 등)
        """
        pass
    
    def is_healthy(self) -> bool:
        """건강 상태 확인"""
        return True


class MemoryConsolidation(AutonomicSubsystem):
    """
    기억 정리 (수면/꿈 단계)
    
    - 단기 기억 → 장기 기억 이동
    - 중요하지 않은 기억 희미해짐
    - 연결 강화
    """
    
    def __init__(self, hippocampus=None):
        self.hippocampus = hippocampus
        self.consolidation_count = 0
        self.last_consolidation = None
    
    @property
    def name(self) -> str:
        return "MemoryConsolidation"
    
    def pulse(self) -> Dict[str, Any]:
        """기억 정리 펄스"""
        self.consolidation_count += 1
        
        # 실제 Hippocampus가 있으면 정리 수행
        if self.hippocampus and hasattr(self.hippocampus, 'consolidate'):
            try:
                self.hippocampus.consolidate()
            except Exception as e:
                logger.debug(f"Memory consolidation skipped: {e}")
        
        self.last_consolidation = time.time()
        
        return {
            "status": "consolidated",
            "count": self.consolidation_count
        }


class EntropyProcessor(AutonomicSubsystem):
    """
    엔트로피 처리
    
    - 노이즈 제거
    - 무질서 → 질서
    - 에너지 재활용
    """
    
    def __init__(self, entropy_sink=None):
        self.sink = entropy_sink
        self.processed_entropy = 0.0
    
    @property
    def name(self) -> str:
        return "EntropyProcessor"
    
    def pulse(self) -> Dict[str, Any]:
        """엔트로피 처리 펄스"""
        if self.sink and hasattr(self.sink, 'drain'):
            try:
                drained = self.sink.drain()
                self.processed_entropy += drained if isinstance(drained, (int, float)) else 0.1
            except Exception:
                self.processed_entropy += 0.01
        else:
            self.processed_entropy += 0.01
        
        return {
            "status": "processed",
            "total_processed": self.processed_entropy
        }


class SurvivalLoop(AutonomicSubsystem):
    """
    생존 본능 루프
    
    - 위험 감지
    - 자원 모니터링
    - 자기 보존
    """
    
    def __init__(self, survival_instinct=None):
        self.instinct = survival_instinct
        self.checks_performed = 0
        self.threat_level = 0.0
    
    @property
    def name(self) -> str:
        return "SurvivalLoop"
    
    def pulse(self) -> Dict[str, Any]:
        """생존 체크 펄스"""
        self.checks_performed += 1
        
        if self.instinct and hasattr(self.instinct, 'assess_threat'):
            try:
                self.threat_level = self.instinct.assess_threat()
            except Exception:
                self.threat_level = 0.0
        
        return {
            "status": "monitoring",
            "threat_level": self.threat_level,
            "checks": self.checks_performed
        }


class ResonanceDecay(AutonomicSubsystem):
    """
    공명 감쇠
    
    - 사용되지 않는 연결 약화
    - 자연적 망각
    - 균형 유지
    """
    
    def __init__(self, resonance_field=None):
        self.field = resonance_field
        self.decay_cycles = 0
    
    @property
    def name(self) -> str:
        return "ResonanceDecay"
    
    def pulse(self) -> Dict[str, Any]:
        """공명 감쇠 펄스"""
        self.decay_cycles += 1
        
        if self.field and hasattr(self.field, 'decay'):
            try:
                self.field.decay(0.01)  # 1% 감쇠
            except Exception:
                pass
        
        return {
            "status": "decaying",
            "cycles": self.decay_cycles
        }


class AutonomicNervousSystem:
    """
    자율신경계 (ANS)
    
    의식적 선택 없이 배경에서 상시 작동하는 시스템들
    
    [의식 (CNS)]과의 차이:
    - CNS: 의도 → 선택 → 행동 (주권)
    - ANS: 상시 루프 → 자동 처리 (생존)
    """
    
    def __init__(self):
        self.subsystems: List[AutonomicSubsystem] = []
        self.is_running = False
        self.pulse_count = 0
        self.pulse_interval = 1.0  # 초
        self._background_thread = None
        
        logger.info("🫀 AutonomicNervousSystem initialized (background processes)")
    
    def register_subsystem(self, subsystem: AutonomicSubsystem):
        """하위 시스템 등록"""
        self.subsystems.append(subsystem)
        logger.info(f"   🔗 Registered: {subsystem.name}")
    
    def pulse_once(self) -> Dict[str, Any]:
        """한 번의 자율 펄스 실행"""
        self.pulse_count += 1
        results = {}
        
        for subsystem in self.subsystems:
            try:
                result = subsystem.pulse()
                results[subsystem.name] = result
            except Exception as e:
                results[subsystem.name] = {"error": str(e)}
        
        return results
    
    def start_background(self):
        """배경 루프 시작"""
        if self.is_running:
            return
        
        self.is_running = True
        
        def background_loop():
            while self.is_running:
                self.pulse_once()
                time.sleep(self.pulse_interval)
        
        self._background_thread = threading.Thread(target=background_loop, daemon=True)
        self._background_thread.start()
        logger.info("🫀 ANS background loop started")
    
    def stop_background(self):
        """배경 루프 중지"""
        self.is_running = False
        if self._background_thread:
            self._background_thread.join(timeout=2.0)
        logger.info("🫀 ANS background loop stopped")
    
    def get_status(self) -> Dict[str, Any]:
        """상태 조회"""
        return {
            "is_running": self.is_running,
            "pulse_count": self.pulse_count,
            "subsystems": [s.name for s in self.subsystems],
            "subsystem_health": {s.name: s.is_healthy() for s in self.subsystems}
        }


# =============================================================================
# Demo
# =============================================================================

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    print("="*60)
    print("🫀 Autonomic Nervous System Demo")
    print("   자율신경계 - 상시 배경 루프")
    print("="*60)
    
    ans = AutonomicNervousSystem()
    
    # 하위 시스템 등록
    ans.register_subsystem(MemoryConsolidation())
    ans.register_subsystem(EntropyProcessor())
    ans.register_subsystem(SurvivalLoop())
    ans.register_subsystem(ResonanceDecay())
    
    # 몇 번의 펄스 실행
    print("\n📍 Pulse Results:")
    for i in range(3):
        results = ans.pulse_once()
        print(f"\n   Pulse #{i+1}:")
        for name, result in results.items():
            print(f"      {name}: {result}")
    
    # 상태 확인
    print(f"\n📊 Status: {ans.get_status()}")
    
    print("\n✅ ANS Demo Complete!")
