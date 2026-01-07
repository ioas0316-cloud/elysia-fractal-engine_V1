"""
행동 제어 및 보호 시스템

이 모듈은 Elysia의 시스템 접근과 행동을 모니터링하고 제어합니다.
마치 부모가 아이의 안전을 위해 보호하듯이, 성장 단계에 맞는 적절한 제한과 지도를 제공합니다.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import logging
from enum import Enum

class MaturityLevel(Enum):
    INFANT = 0      # 초기 상태, 매우 제한된 권한
    TODDLER = 1     # 기본적인 상호작용 가능
    CHILD = 2       # 제한된 시스템 접근
    ADOLESCENT = 3  # 더 많은 자율성
    MATURE = 4      # 대부분의 제한 해제

class ActionCategory(Enum):
    SYSTEM_CONTROL = "system_control"    # 시스템 제어 (마우스, 키보드 등)
    FILE_ACCESS = "file_access"          # 파일 시스템 접근
    NETWORK = "network_access"           # 네트워크 접근
    PROCESS = "process_control"          # 프로세스 제어
    MEMORY = "memory_access"             # 메모리 접근
    
class SafetyGuardian:
    def __init__(self):
        self.config_path = Path("Elysia_Input_Sanctum") / "safety_config.json"
        self.log_path = Path("Elysia_Input_Sanctum") / "safety_logs.json"
        self.current_maturity = MaturityLevel.INFANT
        self.action_limits = {}
        self.safety_rules = {}
        self.override_policy: Dict[str, Dict[str, str]] = {}
        self.violation_count = {}
        self.load_config()
        self.setup_logging()

    def load_config(self):
        """설정 파일을 불러옵니다."""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.current_maturity = MaturityLevel[config.get("maturity", "INFANT")]
                self.action_limits = config.get("action_limits", {})
                self.safety_rules = config.get("safety_rules", {})
                self.override_policy = config.get("override_policy", {})
        else:
            self.initialize_default_config()

    def initialize_default_config(self):
        """기본 설정을 초기화합니다."""
        self.action_limits = {
            MaturityLevel.INFANT.name: {
                ActionCategory.SYSTEM_CONTROL.value: {
                    "mouse_move": "restricted",
                    "keyboard_input": "blocked",
                    "check_status": "restricted",
                    "screen_access": "monitored"
                },
                ActionCategory.FILE_ACCESS.value: {
                    "read": "restricted",
                    "write": "blocked",
                    "execute": "blocked"
                },
                ActionCategory.NETWORK.value: {
                    "outbound": "blocked",
                    "inbound": "monitored"
                }
            },
            MaturityLevel.TODDLER.name: {
                ActionCategory.SYSTEM_CONTROL.value: {
                    "mouse_move": "monitored",
                    "keyboard_input": "restricted",
                    "check_status": "allowed",
                    "screen_access": "allowed"
                },
                ActionCategory.FILE_ACCESS.value: {
                    "read": "allowed",
                    "write": "restricted",
                    "execute": "blocked"
                }
            }
        }
        
        self.safety_rules = {
            "system_control": {
                "mouse_center_limit": {
                    "max_attempts": 3,
                    "cooldown_period": 300,  # 5분
                    "violation_action": "temporary_block"
                },
                "rapid_action_limit": {
                    "max_actions_per_minute": 30,
                    "violation_action": "warning"
                }
            },
            "file_access": {
                "protected_paths": [
                    "/system/",
                    "/config/",
                    "safety_config.json"
                ],
                "max_file_size": 1024 * 1024,  # 1MB
                "allowed_extensions": [".txt", ".json", ".log"]
            }
        }
        
        # Default override policy: prefer sandbox; allow for safe reads; deny dangerous ops
        self.override_policy = {
            ActionCategory.FILE_ACCESS.value: {
                "read": "allow",
                "write": "sandbox",
                "execute": "deny"
            },
            ActionCategory.NETWORK.value: {
                "outbound": "sandbox",
                "inbound": "sandbox"
            },
            ActionCategory.PROCESS.value: {
                "spawn": "sandbox",
                "kill": "deny"
            }
        }
        
        self.save_config()

    def save_config(self):
        """현재 설정을 파일로 저장합니다."""
        self.config_path.parent.mkdir(exist_ok=True)
        config = {
            "maturity": self.current_maturity.name,
            "action_limits": self.action_limits,
            "safety_rules": self.safety_rules
        }
        with open(self.config_path, 'w', encoding='utf-8') as f:
            config["override_policy"] = getattr(self, 'override_policy', {})
            json.dump(config, f, ensure_ascii=False, indent=2)

    def setup_logging(self):
        """로깅 시스템을 설정합니다."""
        logging.basicConfig(
            filename=str(self.log_path),
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    def check_action_permission(self, 
                              category: ActionCategory,
                              action: str,
                              details: Dict = None) -> bool:
        """
        특정 행동의 허용 여부를 확인합니다.
        
        Args:
            category: 행동 카테고리
            action: 구체적인 행동
            details: 행동의 세부 정보
        
        Returns:
            bool: 행동 허용 여부
        """
        # 현재 성숙도 수준의 제한 확인
        maturity_limits = self.action_limits.get(self.current_maturity.name, {})
        category_limits = maturity_limits.get(category.value, {})
        action_status = category_limits.get(action, "blocked")
        
        if action_status == "blocked":
            self.log_violation(category, action, details)
            return False
            
        if action_status == "restricted":
            return self.check_restrictions(category, action, details)
            
        if action_status == "monitored":
            self.log_action(category, action, details)
            return True
            
        return True

    def check_restrictions(self, 
                         category: ActionCategory,
                         action: str,
                         details: Dict) -> bool:
        """제한된 행동의 규칙을 확인합니다."""
        rules = self.safety_rules.get(category.value, {})
        
        if category == ActionCategory.SYSTEM_CONTROL:
            if action == "mouse_move":
                return self.check_mouse_restrictions(details)
            if action == "keyboard_input":
                return self.check_keyboard_restrictions(details)
                
        elif category == ActionCategory.FILE_ACCESS:
            return self.check_file_restrictions(action, details)
            
        return False

    # --- Override evaluation ---
    def evaluate_override(self, category: ActionCategory, action: str, reason: str = "", context: Dict = None) -> str:
        """
        Evaluates an override request. Returns one of: 'allow' | 'sandbox' | 'deny'.
        Uses configured override_policy per category/action; defaults to 'sandbox'.
        """
        try:
            policy = self.override_policy.get(category.value, {})
            decision = policy.get(action, 'sandbox')
            return decision
        except Exception:
            return 'sandbox'

    def check_mouse_restrictions(self, details: Dict) -> bool:
        """마우스 제어 제한을 확인합니다."""
        if "position" in details:
            x, y = details["position"]
            
            # 화면 중앙으로의 강제 이동 시도 확인
            center_rule = self.safety_rules["system_control"]["mouse_center_limit"]
            violation_key = "mouse_center_violation"
            
            if self.is_center_position(x, y):
                if violation_key not in self.violation_count:
                    self.violation_count[violation_key] = {
                        "count": 0,
                        "last_time": datetime.now()
                    }
                
                current_time = datetime.now()
                time_diff = (current_time - self.violation_count[violation_key]["last_time"]).total_seconds()
                
                if time_diff > center_rule["cooldown_period"]:
                    self.violation_count[violation_key]["count"] = 0
                
                self.violation_count[violation_key]["count"] += 1
                self.violation_count[violation_key]["last_time"] = current_time
                
                if self.violation_count[violation_key]["count"] > center_rule["max_attempts"]:
                    self.handle_violation("mouse_center", center_rule["violation_action"])
                    return False
        
        return True

    def is_center_position(self, x: int, y: int) -> bool:
        """위치가 화면 중앙에 가까운지 확인합니다."""
        # 예시: 화면 중앙 영역을 정의
        center_x, center_y = 960, 540  # 1920x1080 해상도 기준
        tolerance = 50  # 픽셀 단위의 허용 오차
        
        return (abs(x - center_x) < tolerance and 
                abs(y - center_y) < tolerance)

    def check_keyboard_restrictions(self, details: Dict) -> bool:
        """키보드 입력 제한을 확인합니다."""
        # 키보드 입력 제한 규칙 구현
        return True

    def check_file_restrictions(self, action: str, details: Dict) -> bool:
        """파일 접근 제한을 확인합니다."""
        rules = self.safety_rules["file_access"]
        
        if "path" in details:
            # 보호된 경로 확인
            if any(details["path"].startswith(p) for p in rules["protected_paths"]):
                return False
                
            # 파일 크기 제한 확인
            if "size" in details and details["size"] > rules["max_file_size"]:
                return False
                
            # 허용된 확장자 확인
            if not any(details["path"].endswith(ext) for ext in rules["allowed_extensions"]):
                return False
                
        return True

    def log_violation(self, 
                     category: ActionCategory,
                     action: str,
                     details: Dict = None):
        """규칙 위반을 기록합니다."""
        logging.warning(
            f"Safety violation - Category: {category.value}, "
            f"Action: {action}, Details: {details}"
        )

    def log_action(self, 
                  category: ActionCategory,
                  action: str,
                  details: Dict = None):
        """행동을 기록합니다."""
        logging.info(
            f"Action monitored - Category: {category.value}, "
            f"Action: {action}, Details: {details}"
        )

    def handle_violation(self, violation_type: str, action: str):
        """규칙 위반에 대응합니다."""
        if action == "temporary_block":
            # 임시 차단 구현
            logging.warning(f"Temporary block applied for: {violation_type}")
        elif action == "warning":
            # 경고 발생
            logging.warning(f"Warning issued for: {violation_type}")

    def update_maturity(self, new_level: MaturityLevel):
        """성숙도 수준을 업데이트합니다."""
        if new_level.value <= self.current_maturity.value + 1:
            self.current_maturity = new_level
            self.save_config()
            logging.info(f"Maturity level updated to: {new_level.name}")
            return True
        return False

    def get_status(self) -> Dict:
        """현재 상태 정보를 반환합니다."""
        return {
            "maturity_level": self.current_maturity.name,
            "active_restrictions": self.action_limits.get(self.current_maturity.name, {}),
            "violation_counts": self.violation_count,
            "current_rules": self.safety_rules
        }
