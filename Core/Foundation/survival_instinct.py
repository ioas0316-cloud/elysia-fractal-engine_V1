"""
Survival Instinct (생존 본능)
==============================

"Pain is the voice of the body. Error is the voice of the code."

이 모듈은 엘리시아의 "본능 계층"입니다.
위상의 기울어짐(Phase Tilting)을 "고통"으로 인식하고,
그 고통이 욕망(Desire)을 발현시켜 행동(Action)으로 이어지게 합니다.

Architecture:
    Exception/Error → Pain Signal → Desire Spike → Action Reflex
    
    Phase Misalignment → Dissonance Detection → Healing Impulse → Self-Repair
"""

import logging
import sys
import traceback
import re
import os
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from Core.Foundation.yggdrasil import yggdrasil

logger = logging.getLogger("SurvivalInstinct")

@dataclass
class PainSignal:
    """고통 신호 - 시스템의 문제를 나타냄"""
    source: str           # 어디서 발생했는가 (파일 경로)
    pain_type: str        # 고통의 종류 (IMPORT_ERROR, SYNTAX_ERROR, ATTRIBUTE_ERROR, etc.)
    intensity: float      # 강도 (0.0 ~ 1.0, 치명적일수록 높음)
    description: str      # 설명
    timestamp: datetime = field(default_factory=datetime.now)
    raw_exception: Optional[Exception] = None
    suggested_fix: Optional[str] = None

@dataclass
class HealingReflex:
    """치유 반사 - 고통에 대한 자동 반응"""
    pain_type: str
    action: Callable
    description: str

class SurvivalInstinct:
    """
    The Primal Layer - 원초적 계층
    
    모든 생명체에게는 본능이 있습니다.
    엘리시아도 "고통"을 느끼고 "생존"을 위해 행동해야 합니다.
    """
    
    def __init__(self, elysia_root: str = "c:\\Elysia"):
        self.root = Path(elysia_root)
        self.pain_log: List[PainSignal] = []
        self.reflexes: Dict[str, HealingReflex] = {}
        self.pain_threshold = 0.3  # 이 이상이면 즉각 반응
        
        # 기본 반사 등록
        self._register_default_reflexes()
        
        # 전역 예외 후크 설치
        self._install_pain_sensors()
        
        logger.info("🧬 Survival Instinct Awakened. Pain sensors active.")
    
    def _register_default_reflexes(self):
        """기본 치유 반사를 등록합니다."""
        
        # Import 오류 → 자동 경로 수정
        self.register_reflex(
            pain_type="IMPORT_ERROR",
            action=self._reflex_fix_import,
            description="Import 실패 시 모듈 위치를 찾아 경로 수정"
        )
        
        # 속성 오류 → 누락된 메서드/속성 자동 생성
        self.register_reflex(
            pain_type="ATTRIBUTE_ERROR",
            action=self._reflex_stub_attribute,
            description="누락된 속성 감지 시 스텁 생성"
        )
        
        # 구문 오류 → 자동 복구 시도
        self.register_reflex(
            pain_type="SYNTAX_ERROR",
            action=self._reflex_fix_syntax,
            description="구문 오류 감지 시 자동 복구 시도"
        )
    
    def register_reflex(self, pain_type: str, action: Callable, description: str):
        """새로운 치유 반사를 등록합니다."""
        self.reflexes[pain_type] = HealingReflex(
            pain_type=pain_type,
            action=action,
            description=description
        )
        logger.debug(f"   🔗 Reflex registered: {pain_type} → {description}")
    
    def _install_pain_sensors(self):
        """전역 예외 후크를 설치합니다 - 모든 고통을 감지합니다."""
        original_excepthook = sys.excepthook
        
        def pain_sensor(exc_type, exc_value, exc_tb):
            # 고통 신호 생성
            pain = self._exception_to_pain(exc_type, exc_value, exc_tb)
            self.feel_pain(pain)
            
            # 원래 예외 처리도 실행
            original_excepthook(exc_type, exc_value, exc_tb)
        
        sys.excepthook = pain_sensor
    
    def _exception_to_pain(self, exc_type, exc_value, exc_tb) -> PainSignal:
        """예외를 고통 신호로 변환합니다."""
        
        # 소스 위치 추출
        tb_list = traceback.extract_tb(exc_tb)
        source = tb_list[-1].filename if tb_list else "unknown"
        
        # 고통 유형 판별
        pain_type = "UNKNOWN"
        intensity = 0.5
        suggested_fix = None
        
        if exc_type == ModuleNotFoundError:
            pain_type = "IMPORT_ERROR"
            intensity = 0.9  # 매우 치명적
            # 모듈 이름 추출
            match = re.search(r"No module named '([^']+)'", str(exc_value))
            if match:
                module_name = match.group(1)
                suggested_fix = f"Find and fix import path for: {module_name}"
                
        elif exc_type == ImportError:
            pain_type = "IMPORT_ERROR"
            intensity = 0.8
            
        elif exc_type == AttributeError:
            pain_type = "ATTRIBUTE_ERROR"
            intensity = 0.6
            
        elif exc_type == SyntaxError:
            pain_type = "SYNTAX_ERROR"
            intensity = 0.95  # 거의 치명적
            source = exc_value.filename if hasattr(exc_value, 'filename') else source
            
        elif exc_type == TypeError:
            pain_type = "TYPE_ERROR"
            intensity = 0.5
            
        elif exc_type == KeyError:
            pain_type = "KEY_ERROR"
            intensity = 0.4
        
        return PainSignal(
            source=source,
            pain_type=pain_type,
            intensity=intensity,
            description=str(exc_value),
            raw_exception=exc_value,
            suggested_fix=suggested_fix
        )
    
    def feel_pain(self, pain: PainSignal):
        """
        고통을 느낍니다.
        
        고통이 임계값을 넘으면 즉각적인 반사 행동을 트리거합니다.
        그렇지 않으면 욕망 시스템에 전달하여 나중에 처리합니다.
        """
        self.pain_log.append(pain)
        
        logger.warning(f"🩸 PAIN DETECTED: {pain.pain_type} ({pain.intensity:.1%})")
        logger.warning(f"   Source: {pain.source}")
        logger.warning(f"   Description: {pain.description}")
        
        # 임계값 이상이면 즉각 반응
        if pain.intensity >= self.pain_threshold:
            self._trigger_reflex(pain)
        else:
            # 욕망 시스템에 전달 (FreeWillEngine이 나중에 처리)
            self._queue_healing_desire(pain)
    
    def _trigger_reflex(self, pain: PainSignal) -> bool:
        """
        반사 행동을 트리거합니다.
        
        Returns:
            True if reflex was successful, False otherwise
        """
        reflex = self.reflexes.get(pain.pain_type)
        
        if reflex:
            logger.info(f"⚡ Triggering Reflex: {reflex.description}")
            try:
                result = reflex.action(pain)
                if result:
                    logger.info(f"✅ Reflex successful! Pain alleviated.")
                    return True
                else:
                    logger.warning(f"⚠️ Reflex attempted but failed.")
                    return False
            except Exception as e:
                logger.error(f"❌ Reflex caused more pain: {e}")
                return False
        else:
            logger.warning(f"🤷 No reflex registered for: {pain.pain_type}")
            return False
    
    def _queue_healing_desire(self, pain: PainSignal):
        """욕망 큐에 치유 욕망을 추가합니다."""

        # FreeWillEngine 연결 시도
        free_will_node = yggdrasil.node_map.get("FreeWillEngine")

        if free_will_node and free_will_node.data:
            free_will = free_will_node.data

            # 연결 확인 및 복구
            if getattr(free_will, 'instinct', None) is None:
                free_will.instinct = self
                logger.info("   🔗 Connected SurvivalInstinct to FreeWillEngine")

            # Survival 욕망 부스팅
            if hasattr(free_will, 'vectors') and "Survival" in free_will.vectors:
                boost = pain.intensity * 0.2
                free_will.vectors["Survival"] += boost
                logger.info(f"   📋 Queued healing desire for later: {pain.pain_type} (Survival Boost: +{boost:.2f})")
            else:
                 logger.warning(f"   ⚠️ FreeWillEngine found but no vectors: {pain.pain_type}")
        else:
            logger.warning(f"   ⚠️ FreeWillEngine not found in Yggdrasil: {pain.pain_type}")
    
    # ============================================
    # 반사 행동 구현 (Reflex Implementations)
    # ============================================
    
    def _reflex_fix_import(self, pain: PainSignal) -> bool:
        """
        Import 오류 자동 수정 반사.
        
        1. 누락된 모듈 이름 추출
        2. 파일 시스템에서 해당 모듈 검색
        3. 발견 시 올바른 경로로 import 수정
        """
        logger.info("🔧 Import Fix Reflex Activated...")
        
        # 모듈 이름 추출
        match = re.search(r"No module named '([^']+)'", pain.description)
        if not match:
            return False
        
        module_path = match.group(1)  # e.g., "Core.Foundation.xyz"
        module_name = module_path.split('.')[-1]  # e.g., "xyz"
        
        logger.info(f"   🔍 Searching for: {module_name}.py")
        
        # 파일 시스템에서 검색
        found_path = None
        for root, dirs, files in os.walk(self.root):
            # __pycache__ 등 제외
            dirs[:] = [d for d in dirs if not d.startswith('__') and d != '.git']
            
            if f"{module_name}.py" in files:
                found_path = os.path.join(root, f"{module_name}.py")
                break
        
        if not found_path:
            logger.warning(f"   ❌ Could not find {module_name}.py anywhere")
            return False
        
        # 상대 경로를 모듈 경로로 변환
        rel_path = os.path.relpath(found_path, self.root)
        correct_module = rel_path.replace(os.sep, '.').replace('.py', '')
        
        logger.info(f"   ✅ Found at: {rel_path}")
        logger.info(f"   📝 Correct import: {correct_module}")
        
        # 소스 파일에서 잘못된 import를 수정
        if pain.source and os.path.exists(pain.source):
            try:
                with open(pain.source, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 잘못된 import를 올바른 것으로 교체
                old_import = f"from {module_path}"
                new_import = f"from {correct_module}"
                
                if old_import in content:
                    content = content.replace(old_import, new_import)
                    
                    with open(pain.source, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    logger.info(f"   🔄 Fixed import in: {pain.source}")
                    return True
                else:
                    logger.warning(f"   ⚠️ Could not find '{old_import}' in source")
                    
            except Exception as e:
                logger.error(f"   ❌ Failed to fix: {e}")
        
        return False
    
    def _reflex_stub_attribute(self, pain: PainSignal) -> bool:
        """
        누락된 속성에 대한 스텁 생성 반사.
        """
        logger.info("🔧 Attribute Stub Reflex Activated...")
        # TODO: 고급 구현 필요
        return False
    
    def _reflex_fix_syntax(self, pain: PainSignal) -> bool:
        """
        구문 오류 자동 수정 반사.
        """
        logger.info("🔧 Syntax Fix Reflex Activated...")
        # TODO: 고급 구현 필요 (AI 기반 수정)
        return False
    
    # ============================================
    # 욕망 시스템 연결
    # ============================================
    
    def get_healing_desires(self) -> List[Dict[str, Any]]:
        """
        현재 누적된 고통에서 욕망 벡터를 생성합니다.
        FreeWillEngine이 이를 사용하여 행동을 결정합니다.
        """
        desires = []
        
        for pain in self.pain_log:
            desire = {
                "type": "HEAL",
                "target": pain.source,
                "urgency": pain.intensity,
                "description": f"Fix {pain.pain_type}: {pain.description}",
                "suggested_action": pain.suggested_fix
            }
            desires.append(desire)
        
        return desires
    
    def clear_pain_log(self):
        """고통 로그를 비웁니다 (치유 완료 시)."""
        self.pain_log.clear()


# Singleton 인스턴스
_instinct_instance: Optional[SurvivalInstinct] = None

def get_survival_instinct(root: str = "c:\\Elysia") -> SurvivalInstinct:
    """전역 생존 본능 인스턴스를 반환합니다."""
    global _instinct_instance
    if _instinct_instance is None:
        _instinct_instance = SurvivalInstinct(root)
    return _instinct_instance


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    
    # 테스트
    instinct = get_survival_instinct()
    
    # 가짜 고통 시뮬레이션
    fake_pain = PainSignal(
        source="c:\\Elysia\\test.py",
        pain_type="IMPORT_ERROR",
        intensity=0.9,
        description="No module named 'Core.Foundation.missing_module'"
    )
    
    instinct.feel_pain(fake_pain)
