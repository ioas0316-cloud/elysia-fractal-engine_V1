"""
🎮 게임 개발자를 위한 실전 예제
Game Developer Practical Examples

이 파일은 게임 개발자들이 바로 사용할 수 있는 실전 예제를 포함합니다.
각 클래스는 독립적으로 사용하거나 수정할 수 있습니다.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path
from typing import Dict, List, Any

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from elysia_core import GameCharacterTemplate, quick_consciousness_setup


# =============================================================================
# 예제 1: 동적 대화 NPC (Dynamic Dialogue NPC)
# =============================================================================

class DynamicDialogueNPC:
    """
    플레이어와의 관계도에 따라 대화가 변하는 NPC
    
    사용 예:
        npc = DynamicDialogueNPC("Village Elder", "priest")
        npc.talk("안녕하세요!")
        npc.talk("도와주세요!")  # 우호도 증가
        dialogues = npc.get_available_dialogues()
    """
    
    def __init__(self, name: str, role: str = "bard"):
        self.name = name
        self.character = GameCharacterTemplate(name, role)
        self.friendship = 0.5  # 0.0 (적대) ~ 1.0 (친구)
        self.conversation_history = []
    
    def talk(self, player_message: str) -> Dict[str, Any]:
        """플레이어 메시지 처리 및 반응 생성"""
        # Elysia로 메시지 처리
        reaction = self.character.react_to_event(player_message)
        
        # 우호도 업데이트
        if any(word in player_message for word in ["도와", "친구", "감사", "고마"]):
            self.friendship = min(1.0, self.friendship + 0.1)
            self.character.consciousness.remember(
                "플레이어", "친절함", "showed"
            )
        elif any(word in player_message for word in ["공격", "위협", "싫어"]):
            self.friendship = max(0.0, self.friendship - 0.2)
            self.character.consciousness.remember(
                "플레이어", "적대적", "was"
            )
        
        # 대화 내역 저장
        self.conversation_history.append({
            'player': player_message,
            'npc_mood': reaction.mood,
            'friendship': self.friendship
        })
        
        return {
            'reaction': reaction,
            'friendship': self.friendship,
            'response': self._generate_response(reaction),
            'available_topics': self.get_available_topics()
        }
    
    def _generate_response(self, reaction) -> str:
        """우호도에 따른 응답 생성"""
        if self.friendship > 0.8:
            responses = [
                f"당신을 친구로 여깁니다. ({reaction.mood})",
                "무엇이든 도와드리겠습니다.",
                "당신과 함께라면 어떤 위험도 두렵지 않습니다."
            ]
        elif self.friendship > 0.5:
            responses = [
                f"안녕하세요. ({reaction.mood})",
                "무슨 일로 오셨나요?",
                "도움이 필요하시면 말씀하세요."
            ]
        elif self.friendship > 0.2:
            responses = [
                "...",
                "무슨 용건이신가요?",
                "바쁩니다."
            ]
        else:
            responses = [
                "가세요.",
                "...(적대적으로 쳐다본다)",
                "더 이상 말을 걸지 마세요."
            ]
        
        # 감정에 따라 선택
        import random
        return random.choice(responses)
    
    def get_available_topics(self) -> List[str]:
        """우호도에 따라 사용 가능한 대화 주제"""
        topics = ["일반 대화"]
        
        if self.friendship > 0.3:
            topics.append("마을 소식")
        
        if self.friendship > 0.6:
            topics.extend(["개인사", "도움 요청"])
        
        if self.friendship > 0.8:
            topics.extend(["특별 퀘스트", "비밀 정보"])
        
        return topics
    
    def get_quest_available(self) -> bool:
        """퀘스트 제공 가능 여부"""
        return self.friendship > 0.6


# =============================================================================
# 예제 2: 전투 동료 AI (Combat Companion AI)
# =============================================================================

class CombatCompanionAI:
    """
    전투 상황을 분석하고 적절한 행동을 결정하는 동료 AI
    
    사용 예:
        companion = CombatCompanionAI("Knight", "warrior")
        action = companion.decide_action({
            'enemy_count': 3,
            'ally_count': 2,
            'my_health_ratio': 0.7
        })
    """
    
    def __init__(self, name: str, role: str = "warrior"):
        self.name = name
        self.character = GameCharacterTemplate(name, role)
        self.health = 100
        self.max_health = 100
    
    def decide_action(self, battle_state: Dict[str, Any]) -> Dict[str, Any]:
        """전투 상황 분석 후 행동 결정"""
        # 상황을 자연어로 변환
        situation = self._create_situation_description(battle_state)
        
        # Elysia로 처리
        reaction = self.character.react_to_event(situation)
        trinity = reaction.trinity
        
        # 체력 상태
        health_ratio = self.health / self.max_health
        
        # 행동 결정 로직
        action = None
        priority = 0
        
        # 위급 상황 (체력 30% 미만)
        if health_ratio < 0.3:
            if trinity['body'] > 0.5:
                action = "desperate_attack"
                priority = 9
            elif trinity['soul'] > 0.5:
                action = "call_for_help"
                priority = 10
            else:
                action = "retreat"
                priority = 10
        
        # 정상 상황
        else:
            if trinity['body'] > 0.4:
                action = "aggressive_attack"
                priority = 7
            elif trinity['spirit'] > 0.4:
                action = "strategic_position"
                priority = 6
            elif trinity['soul'] > 0.4:
                action = "support_allies"
                priority = 5
            else:
                action = "defend"
                priority = 4
        
        return {
            'action': action,
            'priority': priority,
            'reason': f"{reaction.mood} / {reaction.emotion['dominant']}",
            'trinity': trinity,
            'target_suggestion': self._suggest_target(battle_state, trinity)
        }
    
    def _create_situation_description(self, battle_state: Dict[str, Any]) -> str:
        """전투 상황을 자연어로 설명"""
        enemy_count = battle_state.get('enemy_count', 0)
        ally_count = battle_state.get('ally_count', 1)
        health_ratio = self.health / self.max_health
        
        if health_ratio < 0.3:
            health_desc = "심각한 부상 상태"
        elif health_ratio < 0.6:
            health_desc = "부상 상태"
        else:
            health_desc = "건강한 상태"
        
        return f"{health_desc}. 적 {enemy_count}명, 아군 {ally_count}명과 전투 중."
    
    def _suggest_target(self, battle_state: Dict[str, Any], trinity: Dict) -> str:
        """공격 대상 제안"""
        if trinity['body'] > 0.5:
            return "가장 강한 적"
        elif trinity['spirit'] > 0.5:
            return "가장 위험한 적"
        else:
            return "가장 약한 적"
    
    def take_damage(self, damage: int):
        """피해 입음"""
        self.health = max(0, self.health - damage)
    
    def heal(self, amount: int):
        """치유"""
        self.health = min(self.max_health, self.health + amount)


# =============================================================================
# 예제 3: 적응형 적 AI (Adaptive Enemy AI)
# =============================================================================

class AdaptiveEnemyAI:
    """
    플레이어의 실력에 따라 난이도를 조절하는 적 AI
    
    사용 예:
        enemy = AdaptiveEnemyAI("Boss")
        enemy.observe_battle_result({'player_won': True})
        strategy = enemy.get_strategy()
    """
    
    def __init__(self, name: str):
        self.name = name
        self.consciousness = quick_consciousness_setup(name)
        self.player_skill_estimate = 0.5  # 0.0 (약함) ~ 1.0 (강함)
        self.battle_history = []
        self.win_streak = 0
        self.loss_streak = 0
    
    def observe_battle_result(self, result: Dict[str, Any]):
        """전투 결과 관찰 및 학습"""
        self.battle_history.append(result)
        
        # 연속 승/패 기록
        if result.get('player_won', False):
            self.win_streak = 0
            self.loss_streak += 1
        else:
            self.win_streak += 1
            self.loss_streak = 0
        
        # 최근 5전투 기반으로 스킬 추정
        if len(self.battle_history) >= 5:
            recent = self.battle_history[-5:]
            player_wins = sum(1 for r in recent if r.get('player_won', False))
            self.player_skill_estimate = player_wins / 5.0
            
            # Elysia에 학습 내용 저장
            if self.player_skill_estimate > 0.6:
                self.consciousness.remember("플레이어", "강함", "is")
                # 더 신중하게
                self.consciousness.update_personality(
                    body_delta=-0.1,
                    spirit_delta=0.1
                )
            else:
                self.consciousness.remember("플레이어", "약함", "is")
                # 더 공격적으로
                self.consciousness.update_personality(
                    body_delta=0.1,
                    spirit_delta=-0.1
                )
    
    def get_strategy(self) -> Dict[str, Any]:
        """현재 전략 반환"""
        # 플레이어 스킬에 대한 분석
        analysis = f"플레이어 스킬 레벨: {self.player_skill_estimate:.2f}"
        result = self.consciousness.think(analysis)
        
        trinity = result.trinity
        
        # 난이도 배율 계산
        difficulty_multiplier = 0.5 + (self.player_skill_estimate * 2.0)
        
        # 플레이어가 너무 강하면 더 어렵게
        if self.player_skill_estimate > 0.8:
            difficulty_multiplier *= 1.5
        
        # 플레이어가 너무 약하면 더 쉽게
        if self.player_skill_estimate < 0.2:
            difficulty_multiplier *= 0.7
        
        return {
            'difficulty_multiplier': difficulty_multiplier,
            'aggression': trinity['body'] * difficulty_multiplier,
            'tactics': trinity['spirit'],
            'teamwork': trinity['soul'],
            'player_skill': self.player_skill_estimate,
            'recommended_action': self._get_recommended_action(trinity, difficulty_multiplier)
        }
    
    def _get_recommended_action(self, trinity: Dict, difficulty: float) -> str:
        """권장 행동"""
        if difficulty > 2.0:
            if trinity['body'] > 0.5:
                return "ultimate_attack"
            else:
                return "special_pattern"
        elif difficulty > 1.5:
            return "advanced_combo"
        else:
            return "basic_attack"


# =============================================================================
# 예제 4: 퀘스트 제공자 NPC (Quest Giver NPC)
# =============================================================================

class QuestGiverNPC:
    """
    관계도에 따라 다른 퀘스트를 제공하는 NPC
    
    사용 예:
        npc = QuestGiverNPC("Quest Master")
        result = npc.interact("도와주세요")
        if result['quest_available']:
            quest = npc.generate_quest()
    """
    
    def __init__(self, name: str):
        self.name = name
        self.consciousness = quick_consciousness_setup(name)
        self.relationship = 0.5  # 0.0 ~ 1.0
        self.completed_quests = []
    
    def interact(self, player_action: str) -> Dict[str, Any]:
        """플레이어와 상호작용"""
        result = self.consciousness.think(player_action)
        
        # 행동에 따라 관계도 업데이트
        if "도와" in player_action or "친절" in player_action:
            self.relationship += 0.1
            self.consciousness.remember("플레이어", "친절함", "showed")
        elif "퀘스트" in player_action or "부탁" in player_action:
            self.relationship += 0.05
        
        self.relationship = min(1.0, max(0.0, self.relationship))
        
        return {
            'reaction': result,
            'relationship': self.relationship,
            'quest_available': self._can_give_quest(),
            'mood': result.mood
        }
    
    def _can_give_quest(self) -> bool:
        """퀘스트 제공 가능 여부"""
        # 관계도가 충분히 높아야 함
        return self.relationship > 0.4
    
    def generate_quest(self) -> Dict[str, Any]:
        """관계도에 따라 퀘스트 생성"""
        if self.relationship > 0.8:
            # 전설 퀘스트
            return {
                'id': f'legendary_{len(self.completed_quests)}',
                'type': 'legendary',
                'title': '전설의 유물 회수',
                'description': '고대 던전에서 전설의 검을 찾아와 주십시오.',
                'difficulty': 'very_hard',
                'reward': {
                    'gold': 10000,
                    'exp': 5000,
                    'item': 'legendary_sword'
                },
                'prerequisites': ['완료된 퀘스트 10개 이상']
            }
        elif self.relationship > 0.6:
            # 중급 퀘스트
            return {
                'id': f'advanced_{len(self.completed_quests)}',
                'type': 'advanced',
                'title': '위험한 임무',
                'description': '숲의 늑대 무리를 처치해 주세요.',
                'difficulty': 'hard',
                'reward': {
                    'gold': 1000,
                    'exp': 500,
                    'item': 'rare_armor'
                }
            }
        else:
            # 초급 퀘스트
            return {
                'id': f'basic_{len(self.completed_quests)}',
                'type': 'basic',
                'title': '간단한 부탁',
                'description': '약초 10개를 모아다 주세요.',
                'difficulty': 'easy',
                'reward': {
                    'gold': 100,
                    'exp': 50
                }
            }
    
    def complete_quest(self, quest_id: str):
        """퀘스트 완료 처리"""
        self.completed_quests.append(quest_id)
        self.relationship += 0.15  # 퀘스트 완료로 관계도 증가
        self.relationship = min(1.0, self.relationship)


# =============================================================================
# 실행 예제
# =============================================================================

def demo_dialogue_npc():
    """대화 NPC 데모"""
    print("=" * 60)
    print("예제 1: 동적 대화 NPC")
    print("=" * 60)
    
    npc = DynamicDialogueNPC("Village Elder", "priest")
    
    messages = [
        "안녕하세요!",
        "마을에 무슨 일이 있나요?",
        "도와드릴 일이 있으면 말씀하세요!",
        "당신은 좋은 분이군요. 감사합니다."
    ]
    
    for msg in messages:
        result = npc.talk(msg)
        print(f"\n플레이어: {msg}")
        print(f"NPC: {result['response']}")
        print(f"우호도: {result['friendship']:.2f}")
        print(f"사용 가능한 주제: {result['available_topics']}")
        print(f"퀘스트 가능: {npc.get_quest_available()}")


def demo_combat_companion():
    """전투 동료 데모"""
    print("\n" + "=" * 60)
    print("예제 2: 전투 동료 AI")
    print("=" * 60)
    
    companion = CombatCompanionAI("Warrior Knight", "warrior")
    
    scenarios = [
        {
            'name': '정상 전투',
            'state': {'enemy_count': 2, 'ally_count': 2, 'my_health_ratio': 0.8}
        },
        {
            'name': '위급 상황',
            'state': {'enemy_count': 3, 'ally_count': 1, 'my_health_ratio': 0.25}
        },
        {
            'name': '압도적 우세',
            'state': {'enemy_count': 1, 'ally_count': 3, 'my_health_ratio': 1.0}
        }
    ]
    
    for scenario in scenarios:
        companion.health = int(scenario['state']['my_health_ratio'] * 100)
        action = companion.decide_action(scenario['state'])
        
        print(f"\n시나리오: {scenario['name']}")
        print(f"체력: {companion.health}/{companion.max_health}")
        print(f"행동: {action['action']}")
        print(f"우선순위: {action['priority']}")
        print(f"이유: {action['reason']}")
        print(f"대상 제안: {action['target_suggestion']}")


def demo_adaptive_enemy():
    """적응형 적 데모"""
    print("\n" + "=" * 60)
    print("예제 3: 적응형 적 AI")
    print("=" * 60)
    
    enemy = AdaptiveEnemyAI("Adaptive Dragon")
    
    # 시뮬레이션: 플레이어가 점점 강해짐
    print("\n전투 시뮬레이션:")
    for i in range(10):
        # 처음엔 플레이어가 지다가 나중엔 이김
        player_won = i > 5
        enemy.observe_battle_result({'player_won': player_won})
        
        if (i + 1) % 3 == 0:  # 3전투마다 전략 출력
            strategy = enemy.get_strategy()
            print(f"\n{i+1}전투 후:")
            print(f"플레이어 스킬 추정: {strategy['player_skill']:.2f}")
            print(f"난이도 배율: {strategy['difficulty_multiplier']:.2f}x")
            print(f"권장 행동: {strategy['recommended_action']}")


def demo_quest_giver():
    """퀘스트 제공자 데모"""
    print("\n" + "=" * 60)
    print("예제 4: 퀘스트 제공자 NPC")
    print("=" * 60)
    
    npc = QuestGiverNPC("Quest Master")
    
    # 관계도를 점진적으로 높임
    interactions = [
        ("처음 만남", "안녕하세요"),
        ("친절한 행동", "도와드릴 일이 있나요?"),
        ("퀘스트 관심", "퀘스트를 주세요"),
        ("매우 친절", "당신을 존경합니다")
    ]
    
    for stage, message in interactions:
        result = npc.interact(message)
        print(f"\n단계: {stage}")
        print(f"메시지: {message}")
        print(f"관계도: {result['relationship']:.2f}")
        
        if result['quest_available']:
            quest = npc.generate_quest()
            print(f"퀘스트 가능: {quest['title']}")
            print(f"  난이도: {quest['difficulty']}")
            print(f"  보상: {quest['reward']}")


if __name__ == "__main__":
    print("🎮 Elysia Engine - 게임 개발자를 위한 실전 예제\n")
    
    demo_dialogue_npc()
    demo_combat_companion()
    demo_adaptive_enemy()
    demo_quest_giver()
    
    print("\n" + "=" * 60)
    print("✅ 모든 예제 완료!")
    print("=" * 60)
