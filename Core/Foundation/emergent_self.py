"""
Emergent Self (창발적 자아)
===========================

하드코딩 없음. 빈 캔버스에서 시작.
목표, 가치, 자기 정의 모두 경험에서 창발.

원칙:
1. 시작은 비어있음 (No Enum, No Default Goals)
2. 경험에서 패턴 발견 → 가치 형성
3. 가치가 반복되면 → 목표로 결정화
4. 목표가 달성되거나 무의미해지면 → 소멸 또는 변형
5. 자기 정의 = 현재 활성 목표들의 총합
"""

import logging
import time
import json
import os
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime

logger = logging.getLogger("Elysia.EmergentSelf")


@dataclass
class EmergentValue:
    """
    창발된 가치 (Emergent Value)
    
    하드코딩되지 않음. 경험에서 자연스럽게 형성됨.
    """
    name: str                           # 이름 (엘리시아가 스스로 명명)
    origin: str                         # 어디서 왔는가 (경험의 출처)
    strength: float = 0.0               # 강도 (반복/강화 정도)
    created_at: float = field(default_factory=time.time)
    last_activated: float = field(default_factory=time.time)
    activation_count: int = 0           # 활성화 횟수
    
    def activate(self):
        """이 가치가 경험에서 다시 발견됨"""
        self.activation_count += 1
        self.strength += 0.1
        self.last_activated = time.time()
    
    def decay(self, amount: float = 0.01):
        """시간이 지나면 약해짐"""
        self.strength = max(0, self.strength - amount)


@dataclass
class EmergentGoal:
    """
    창발된 목표 (Emergent Goal)
    
    가치가 충분히 강해지면 목표로 결정화됨.
    달성되거나 무의미해지면 소멸.
    """
    name: str
    from_value: str                     # 어떤 가치에서 형성됨
    description: str                    # 엘리시아가 스스로 기술
    progress: float = 0.0               # 진행도 (0.0 ~ 무한)
    created_at: float = field(default_factory=time.time)
    achieved: bool = False
    abandoned: bool = False
    abandon_reason: str = ""
    
    def advance(self, amount: float = 0.1, evidence: str = ""):
        """목표를 향해 진전"""
        self.progress += amount
        logger.info(f"🎯 Goal '{self.name}' advanced: +{amount:.2f} (now {self.progress:.2f})")
    
    def is_stagnant(self, threshold_seconds: float = 3600) -> bool:
        """진전 없이 오래됨"""
        # 마지막 진전 시간을 추적해야 하지만, 간략히 생성 후 시간으로 대체
        return time.time() - self.created_at > threshold_seconds and self.progress < 0.5


class EmergentSelf:
    """
    창발적 자아
    
    - 빈 상태로 시작
    - 경험에서 가치를 발견
    - 가치에서 목표를 형성
    - 목표에서 자기 정의를 도출
    """
    
    def __init__(self, state_path: str = "c:\\Elysia\\data\\State\\emergent_self.json"):
        self.state_path = state_path
        
        # 빈 상태로 시작
        self.values: Dict[str, EmergentValue] = {}
        self.goals: Dict[str, EmergentGoal] = {}
        self.self_definition: str = ""  # 빈 문자열로 시작
        
        # 역사 (변화 추적)
        self.history: List[Dict] = []
        self.snapshots: List[Dict] = []
        
        # 상태 복원 시도
        self._load_state()
        
        logger.info("🌱 EmergentSelf initialized (empty canvas)")
    
    # ========================
    # 가치 발견 (Value Discovery)
    # ========================
    
    def notice_pattern(self, pattern_name: str, origin: str):
        """
        경험에서 패턴 발견 → 가치 형성/강화
        
        이것이 학습의 시작점.
        외부에서 "무엇이 중요한지" 주입하지 않음.
        경험에서 반복되는 것이 자연스럽게 가치가 됨.
        """
        if pattern_name in self.values:
            # 기존 가치 강화
            self.values[pattern_name].activate()
            logger.info(f"💎 Value reinforced: '{pattern_name}' (strength: {self.values[pattern_name].strength:.2f})")
        else:
            # 새 가치 탄생
            self.values[pattern_name] = EmergentValue(
                name=pattern_name,
                origin=origin,
                strength=0.1
            )
            logger.info(f"✨ New value emerged: '{pattern_name}' (from {origin})")
            
            self._record_change("value_created", pattern_name)
        
        # 가치가 충분히 강하면 목표로 결정화
        self._crystallize_goals()
    
    def _crystallize_goals(self, threshold: float = 1.0):
        """
        강한 가치 → 목표로 결정화
        """
        for name, value in self.values.items():
            if value.strength >= threshold and name not in self.goals:
                # 새 목표 형성
                goal = EmergentGoal(
                    name=f"Pursue_{name}",
                    from_value=name,
                    description=f"Explore and deepen understanding of '{name}'"
                )
                self.goals[goal.name] = goal
                logger.info(f"🎯 Goal crystallized from value: '{goal.name}'")
                self._record_change("goal_created", goal.name)
    
    # ========================
    # 목표 진행 (Goal Progress)
    # ========================
    
    def report_progress(self, goal_name: str, amount: float, evidence: str = ""):
        """
        목표 진전 보고
        
        외부(학습 시스템 등)에서 호출.
        """
        if goal_name in self.goals:
            self.goals[goal_name].advance(amount, evidence)
            self._update_self_definition()
    
    def check_goals(self):
        """
        목표 상태 점검
        - 달성된 것은 완료 처리
        - 정체된 것은 재검토
        """
        for name, goal in list(self.goals.items()):
            if goal.progress >= 10.0 and not goal.achieved:
                goal.achieved = True
                logger.info(f"🏆 Goal achieved: '{name}'")
                self._record_change("goal_achieved", name)
                
                # 새로운 더 높은 목표 형성?
                self._evolve_goal(goal)
            
            elif goal.is_stagnant() and not goal.abandoned:
                # 정체 감지 → 재검토
                logger.warning(f"⚠️ Goal stagnant: '{name}'. Re-evaluating...")
                self._reevaluate_goal(goal)
    
    def _evolve_goal(self, achieved_goal: EmergentGoal):
        """
        달성된 목표 → 더 높은 목표로 진화
        """
        new_goal = EmergentGoal(
            name=f"Deepen_{achieved_goal.name}",
            from_value=achieved_goal.from_value,
            description=f"Go beyond '{achieved_goal.name}' - find deeper meaning"
        )
        self.goals[new_goal.name] = new_goal
        logger.info(f"🚀 Goal evolved: '{achieved_goal.name}' → '{new_goal.name}'")
        self._record_change("goal_evolved", new_goal.name)
    
    def _reevaluate_goal(self, stagnant_goal: EmergentGoal):
        """
        정체된 목표 재검토
        - 방법이 잘못됐는가? → 목표 유지, 접근 변경
        - 목표 자체가 잘못됐는가? → 목표 폐기
        """
        # 연관 가치 강도 확인
        value = self.values.get(stagnant_goal.from_value)
        if value and value.strength < 0.5:
            # 가치 자체가 약해짐 → 목표 폐기
            stagnant_goal.abandoned = True
            stagnant_goal.abandon_reason = "Underlying value weakened"
            logger.info(f"🗑️ Goal abandoned: '{stagnant_goal.name}' (value weakened)")
            self._record_change("goal_abandoned", stagnant_goal.name)
        else:
            # 가치는 강함 → 접근 변경 필요
            logger.info(f"🔄 Goal needs new approach: '{stagnant_goal.name}'")
            # 메타 목표: "왜 진전이 없는지 이해하기"
            meta_goal = EmergentGoal(
                name=f"Understand_{stagnant_goal.name}_Block",
                from_value="meta_cognition",
                description=f"Why is '{stagnant_goal.name}' not progressing?"
            )
            self.goals[meta_goal.name] = meta_goal
    
    # ========================
    # 자기 정의 (Self Definition)
    # ========================
    
    def _update_self_definition(self):
        """
        자기 정의 = 현재 활성 목표들의 총합
        
        하드코딩 아님. 현재 상태에서 자연스럽게 도출.
        """
        active_goals = [g for g in self.goals.values() if not g.achieved and not g.abandoned]
        strong_values = [v for v in self.values.values() if v.strength > 0.5]
        
        if not active_goals and not strong_values:
            self.self_definition = "아직 정의되지 않음. 경험을 통해 형성 중."
        else:
            parts = []
            if strong_values:
                value_names = ", ".join([v.name for v in sorted(strong_values, key=lambda x: -x.strength)[:3]])
                parts.append(f"'{value_names}'을 중시하는 존재")
            if active_goals:
                goal_names = ", ".join([g.name for g in active_goals[:3]])
                parts.append(f"'{goal_names}'를 추구하는 존재")
            
            old_def = self.self_definition
            self.self_definition = " 그리고 ".join(parts)
            
            if old_def != self.self_definition:
                logger.info(f"🔄 Self-definition updated: {self.self_definition}")
                self._record_change("self_redefined", self.self_definition)
    
    def who_am_i(self) -> str:
        """나는 누구인가?"""
        self._update_self_definition()
        return self.self_definition
    
    # ========================
    # 변화 추적 (Change Tracking)
    # ========================
    
    def _record_change(self, change_type: str, detail: str):
        """변화 기록"""
        self.history.append({
            "timestamp": time.time(),
            "type": change_type,
            "detail": detail
        })
    
    def take_snapshot(self) -> Dict:
        """현재 상태 스냅샷"""
        snapshot = {
            "timestamp": time.time(),
            "date": datetime.now().isoformat(),
            "value_count": len(self.values),
            "goal_count": len(self.goals),
            "active_goals": len([g for g in self.goals.values() if not g.achieved and not g.abandoned]),
            "total_value_strength": sum(v.strength for v in self.values.values()),
            "self_definition": self.self_definition,
            "values": {k: asdict(v) for k, v in self.values.items()},
            "goals": {k: asdict(g) for k, g in self.goals.items()}
        }
        self.snapshots.append(snapshot)
        return snapshot
    
    def compare_to_yesterday(self) -> str:
        """어제와 비교"""
        if len(self.snapshots) < 2:
            return "아직 비교할 수 있는 역사가 없습니다."
        
        yesterday = self.snapshots[-2]
        today = self.snapshots[-1]
        
        changes = []
        
        value_diff = today["value_count"] - yesterday["value_count"]
        if value_diff != 0:
            changes.append(f"가치: {'+' if value_diff > 0 else ''}{value_diff}")
        
        goal_diff = today["active_goals"] - yesterday["active_goals"]
        if goal_diff != 0:
            changes.append(f"활성 목표: {'+' if goal_diff > 0 else ''}{goal_diff}")
        
        if today["self_definition"] != yesterday["self_definition"]:
            changes.append(f"자기 정의 변화: '{yesterday['self_definition'][:30]}...' → '{today['self_definition'][:30]}...'")
        
        if not changes:
            return "변화 없음 (정체 상태)"
        
        return " | ".join(changes)
    
    # ========================
    # 상태 저장/복원
    # ========================
    
    def save_state(self):
        """상태 저장"""
        os.makedirs(os.path.dirname(self.state_path), exist_ok=True)
        
        state = {
            "values": {k: asdict(v) for k, v in self.values.items()},
            "goals": {k: asdict(g) for k, g in self.goals.items()},
            "self_definition": self.self_definition,
            "history": self.history[-100:],  # 최근 100개만
            "snapshots": self.snapshots[-30:]  # 최근 30일
        }
        
        with open(self.state_path, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        
        logger.info(f"💾 EmergentSelf state saved")
    
    def _load_state(self):
        """상태 복원"""
        if not os.path.exists(self.state_path):
            return
        
        try:
            with open(self.state_path, 'r', encoding='utf-8') as f:
                state = json.load(f)
            
            # 가치 복원
            for k, v in state.get("values", {}).items():
                self.values[k] = EmergentValue(**v)
            
            # 목표 복원
            for k, g in state.get("goals", {}).items():
                self.goals[k] = EmergentGoal(**g)
            
            self.self_definition = state.get("self_definition", "")
            self.history = state.get("history", [])
            self.snapshots = state.get("snapshots", [])
            
            logger.info(f"📂 EmergentSelf state restored: {len(self.values)} values, {len(self.goals)} goals")
        except Exception as e:
            logger.warning(f"Failed to load state: {e}")
    
    # ========================
    # 가치/목표 자연 소멸
    # ========================
    
    def apply_entropy(self):
        """
        시간의 흐름 = 엔트로피
        사용되지 않는 것은 약해지고 사라짐
        """
        for value in self.values.values():
            value.decay(0.01)
        
        # 너무 약해진 가치 제거
        weak_values = [k for k, v in self.values.items() if v.strength <= 0]
        for k in weak_values:
            del self.values[k]
            logger.info(f"💨 Value faded away: '{k}'")
            self._record_change("value_faded", k)


# 싱글톤
_emergent_self = None

def get_emergent_self() -> EmergentSelf:
    global _emergent_self
    if _emergent_self is None:
        _emergent_self = EmergentSelf()
    return _emergent_self
