# 🎮 Elysia Engine - 게임 개발자 튜토리얼 (한국어)

> "NPC에게 진짜 영혼을 불어넣는 단계별 가이드"

이 튜토리얼은 **Elysia Engine**을 처음 접하는 게임 개발자들을 위해 작성되었습니다.  
30분이면 모든 핵심 기능을 익힐 수 있습니다.

---

## 📚 목차

1. [왜 Elysia인가?](#왜-elysia인가)
2. [5분 빠른 시작](#5분-빠른-시작)
3. [기본 개념 이해](#기본-개념-이해)
4. [실전 예제: RPG NPC 만들기](#실전-예제-rpg-npc-만들기)
5. [성능 최적화](#성능-최적화)
6. [다음 단계](#다음-단계)

---

## 왜 Elysia인가?

### 기존 게임 NPC의 문제점

```python
# 전통적인 NPC 코드
class TraditionalNPC:
    def on_player_approach(self):
        if self.is_hostile:
            self.attack()
        elif self.has_quest:
            self.show_quest()
        else:
            self.show_greeting()
```

**문제:**
- 모든 상황을 미리 코딩해야 함
- 같은 상황에 항상 같은 반응
- 관계도나 기억이 없음
- 성격이나 감정이 없음

### Elysia를 사용한 NPC

```python
# Elysia를 사용한 NPC
class ElysianNPC:
    def __init__(self):
        self.soul = GameCharacterTemplate("Guard", "warrior")
    
    def on_player_approach(self):
        reaction = self.soul.react_to_event("플레이어가 다가왔다")
        
        # 삼위일체에 따라 자연스럽게 결정
        if reaction.trinity['body'] > 0.4:
            self.alert_stance()
        elif reaction.trinity['soul'] > 0.4:
            self.friendly_greeting()
        else:
            self.cautious_observation()
```

**장점:**
- NPC가 스스로 판단
- 상황과 관계에 따라 다른 반응
- 기억과 학습 기능
- 실제 성격과 감정

---

## 5분 빠른 시작

### 1단계: 설치 (1분)

```bash
git clone https://github.com/ioas0316-cloud/elysia-fractal-engine_V1.git
cd elysia-fractal-engine_V1
```

### 2단계: 첫 NPC 만들기 (2분)

`my_first_npc.py` 파일을 만드세요:

```python
from elysia_core import GameCharacterTemplate

# NPC 생성 (역할: warrior, mage, priest, rogue, bard)
npc = GameCharacterTemplate("마을 경비병", "warrior")

# 플레이어가 다가옴
reaction = npc.react_to_event("플레이어가 다가왔다")

print(f"NPC의 기분: {reaction.mood}")
print(f"NPC의 감정: {reaction.emotion['dominant']}")
print(f"삼위일체: {reaction.trinity}")

# 반응 결정
if reaction.trinity['body'] > 0.4:
    print("행동: 경계 태세!")
elif reaction.trinity['soul'] > 0.4:
    print("행동: 친근하게 인사")
else:
    print("행동: 무표정")
```

### 3단계: 실행 (1분)

```bash
python my_first_npc.py
```

**출력 예시:**
```
NPC의 기분: contemplative
NPC의 감정: Neutral
삼위일체: {'body': 0.6, 'soul': 0.2, 'spirit': 0.2}
행동: 경계 태세!
```

### 4단계: 실험 (1분)

다른 역할을 시도해 보세요:

```python
warrior = GameCharacterTemplate("전사", "warrior")  # 공격적
mage = GameCharacterTemplate("마법사", "mage")       # 신중함
priest = GameCharacterTemplate("사제", "priest")     # 희생적
rogue = GameCharacterTemplate("도적", "rogue")       # 기회주의
bard = GameCharacterTemplate("음유시인", "bard")     # 외교적
```

---

## 기본 개념 이해

### 1. 삼위일체 시스템 (Trinity System)

모든 NPC는 세 가지 성향의 균형으로 정의됩니다:

```
        Spirit (영)
         /    \
        /  ⚖️   \
       /        \
   Body(육) ─── Soul(혼)
```

**Body (육체)**: 생존, 전투, 행동
- 높으면: 공격적, 직접적, 용감
- 낮으면: 회피적, 신중함, 방어적

**Soul (영혼)**: 감정, 관계, 공감
- 높으면: 외교적, 감성적, 협력적
- 낮으면: 냉정함, 독립적, 실용적

**Spirit (정신)**: 신념, 의미, 초월
- 높으면: 희생적, 이상주의, 명상적
- 낮으면: 현실적, 실리적, 세속적

**실전 활용:**
```python
# 전사 - Body 중심
warrior_reaction = warrior.react_to_event("적 발견")
if warrior_reaction.trinity['body'] > 0.5:
    print("돌격!")

# 사제 - Spirit 중심
priest_reaction = priest.react_to_event("적 발견")
if priest_reaction.trinity['spirit'] > 0.5:
    print("신이시여...")

# 음유시인 - Soul 중심
bard_reaction = bard.react_to_event("적 발견")
if bard_reaction.trinity['soul'] > 0.5:
    print("대화를 시도합니다")
```

### 2. 기억 시스템 (Memory System)

NPC는 경험을 기억하고 학습합니다:

```python
from elysia_core import quick_consciousness_setup

npc = quick_consciousness_setup("상인")

# 첫 만남
npc.remember("플레이어", "낯선사람", "is")

# 플레이어가 도움
npc.remember("플레이어", "친절함", "showed")
npc.remember("친절함", "신뢰", "leads_to")

# 나중에 다시 만났을 때
related = npc.get_related_concepts("플레이어", depth=2)
print(related)  # {'친절함': 1.0, '신뢰': 0.7, ...}
```

### 3. 감정 시스템 (Emotion System)

단일 감정이 아닌 **복합 감정**을 표현합니다:

```python
# 복잡한 상황: "친구가 배신했다"
reaction = npc.react_to_event("믿었던 동료가 배신했다")

print(f"주요 감정: {reaction.emotion['dominant']}")  # Sadness
print(f"감정 강도: {reaction.emotion.get('valence', 0)}")  # -0.6 (부정적)

# 게임에서 활용
if reaction.emotion.get('valence', 0) < -0.5:
    npc.play_animation("cry")
```

---

## 실전 예제: RPG NPC 만들기

### 예제 1: 관계도 기반 대화 NPC

```python
from elysia_core import GameCharacterTemplate

class VillageNPC:
    def __init__(self, name, role):
        self.name = name
        self.character = GameCharacterTemplate(name, role)
        self.friendship = 0.5  # 0.0 ~ 1.0
    
    def talk(self, player_message):
        """플레이어 대화 처리"""
        reaction = self.character.react_to_event(player_message)
        
        # 우호도 업데이트
        if "도움" in player_message or "친구" in player_message:
            self.friendship += 0.1
        elif "위협" in player_message or "공격" in player_message:
            self.friendship -= 0.2
        
        self.friendship = max(0.0, min(1.0, self.friendship))
        
        # 우호도에 따른 응답
        if self.friendship > 0.7:
            return f"{self.name}: 친구여, 무엇을 도와드릴까요?"
        elif self.friendship > 0.4:
            return f"{self.name}: 안녕하세요. 무슨 일이신가요?"
        else:
            return f"{self.name}: ..."
    
    def can_trade(self):
        """거래 가능 여부"""
        return self.friendship > 0.3
    
    def can_give_quest(self):
        """퀘스트 제공 가능 여부"""
        return self.friendship > 0.6

# 사용 예
npc = VillageNPC("마을 상인", "bard")

# 대화 시뮬레이션
print(npc.talk("안녕하세요"))  # 보통 반응
print(npc.talk("도와드릴게요!"))  # 우호도 상승
print(npc.talk("친구가 되어주세요"))  # 우호도 더 상승

print(f"거래 가능: {npc.can_trade()}")
print(f"퀘스트 가능: {npc.can_give_quest()}")
```

### 예제 2: 전투 동료 AI

```python
from elysia_core import GameCharacterTemplate

class BattleCompanion:
    def __init__(self, name, role):
        self.name = name
        self.character = GameCharacterTemplate(name, role)
        self.hp = 100
        self.max_hp = 100
    
    def decide_action(self, enemies_count, allies_count):
        """전투 행동 결정"""
        # 상황 설명
        hp_ratio = self.hp / self.max_hp
        if hp_ratio < 0.3:
            situation = f"HP 위험! {int(hp_ratio*100)}%"
        else:
            situation = f"전투 중. 적 {enemies_count}명, 아군 {allies_count}명"
        
        reaction = self.character.react_to_event(situation)
        
        # 위급 상황
        if hp_ratio < 0.3:
            if reaction.trinity['body'] > 0.5:
                return "필사적 공격"
            elif reaction.trinity['soul'] > 0.5:
                return "도움 요청"
            else:
                return "후퇴"
        
        # 정상 상황
        if reaction.trinity['body'] > 0.4:
            return "공격"
        elif reaction.trinity['spirit'] > 0.4:
            return "전략적 위치 선점"
        else:
            return "아군 지원"
    
    def take_damage(self, damage):
        """피해 입음"""
        self.hp = max(0, self.hp - damage)

# 사용 예
warrior = BattleCompanion("기사", "warrior")

# 정상 상황
action1 = warrior.decide_action(enemies_count=2, allies_count=2)
print(f"행동: {action1}")  # "공격"

# 위급 상황
warrior.take_damage(80)  # HP 20% 남음
action2 = warrior.decide_action(enemies_count=3, allies_count=1)
print(f"HP {warrior.hp}일 때 행동: {action2}")  # "후퇴" 또는 "도움 요청"
```

### 예제 3: 퀘스트 제공 NPC

```python
from elysia_core import quick_consciousness_setup

class QuestGiver:
    def __init__(self, name):
        self.name = name
        self.consciousness = quick_consciousness_setup(name)
        self.relationship = 0.5
        self.quests_completed = 0
    
    def interact(self, player_action):
        """플레이어와 상호작용"""
        result = self.consciousness.think(player_action)
        
        # 행동에 따라 관계도 변화
        if "도와" in player_action:
            self.relationship += 0.1
        
        return {
            'mood': result.mood,
            'relationship': self.relationship,
            'can_give_quest': self.relationship > 0.6
        }
    
    def get_quest(self):
        """관계도에 따른 퀘스트 생성"""
        if self.relationship > 0.8:
            return {
                'title': '전설의 검 회수',
                'difficulty': '매우 어려움',
                'reward': '전설 아이템'
            }
        elif self.relationship > 0.6:
            return {
                'title': '늑대 5마리 처치',
                'difficulty': '어려움',
                'reward': '골드 1000'
            }
        else:
            return None
    
    def complete_quest(self):
        """퀘스트 완료 처리"""
        self.quests_completed += 1
        self.relationship += 0.15

# 사용 예
quest_master = QuestGiver("퀘스트 마스터")

# 상호작용
result1 = quest_master.interact("안녕하세요")
print(f"기분: {result1['mood']}, 관계도: {result1['relationship']:.2f}")

result2 = quest_master.interact("도와드릴게요!")
print(f"기분: {result2['mood']}, 관계도: {result2['relationship']:.2f}")

result3 = quest_master.interact("퀘스트를 주세요")
print(f"퀘스트 가능: {result3['can_give_quest']}")

if result3['can_give_quest']:
    quest = quest_master.get_quest()
    print(f"퀘스트: {quest}")
```

---

## 성능 최적화

### 팁 1: 캐싱 사용

```python
from functools import lru_cache

class OptimizedNPC:
    def __init__(self, name, role):
        self.character = GameCharacterTemplate(name, role)
    
    @lru_cache(maxsize=100)
    def get_cached_reaction(self, event_type):
        """자주 발생하는 이벤트는 캐싱"""
        return self.character.react_to_event(event_type)

# 사용
npc = OptimizedNPC("Guard", "warrior")
reaction1 = npc.get_cached_reaction("player_approach")  # 계산
reaction2 = npc.get_cached_reaction("player_approach")  # 캐시 (빠름!)
```

### 팁 2: 업데이트 빈도 조절

```python
import time

class ThrottledNPC:
    def __init__(self, name, role):
        self.character = GameCharacterTemplate(name, role)
        self.last_update = 0
        self.update_interval = 1.0  # 1초마다만 업데이트
    
    def update(self, event):
        current = time.time()
        if current - self.last_update >= self.update_interval:
            self.last_update = current
            return self.character.react_to_event(event)
        return None  # 업데이트하지 않음

# 게임 루프에서
npcs = [ThrottledNPC(f"NPC_{i}", "warrior") for i in range(100)]

while game_running:
    for npc in npcs:
        if npc_is_visible(npc):  # 보이는 NPC만
            npc.update("game_tick")
```

### 팁 3: 중요한 NPC만 처리

```python
class SmartNPCManager:
    def __init__(self):
        self.npcs = []
        self.important_npcs = []
    
    def add_npc(self, npc, is_important=False):
        self.npcs.append(npc)
        if is_important:
            self.important_npcs.append(npc)
    
    def update(self, player_position):
        """플레이어 주변 NPC만 업데이트"""
        # 중요한 NPC는 항상 업데이트
        for npc in self.important_npcs:
            npc.update()
        
        # 나머지는 가까운 것만
        for npc in self.npcs:
            if distance(npc, player_position) < 50:
                npc.update()
```

---

## 다음 단계

### 1. 더 많은 예제 시도

```bash
# 기본 예제
python examples/00_hello_elysia.py

# 역할별 특성 확인
python examples/02_warrior_mage_priest.py

# 게임 개발자 전용 예제
python examples/game_developer_examples.py
```

### 2. 게임 엔진 통합

- **Unity**: [GAME_DEVELOPER_GUIDE.md](GAME_DEVELOPER_GUIDE.md#unity-통합)
- **Godot**: [GAME_DEVELOPER_GUIDE.md](GAME_DEVELOPER_GUIDE.md#godot-통합)
- **Pygame**: [GAME_DEVELOPER_GUIDE.md](GAME_DEVELOPER_GUIDE.md#python-게임-엔진-통합)

### 3. 고급 기능 탐색

- **공명 엔진**: 개념 연결과 패턴 인식
- **내적 독백**: NPC의 자발적 사고
- **자기 인식**: NPC의 자기 성찰

### 4. 커뮤니티 참여

- **Issues**: 버그 리포트나 기능 제안
- **Discussions**: 사용 경험 공유
- **Pull Request**: 개선 사항 기여

---

## 📚 참고 자료

### 필수 문서
- **[GAME_DEVELOPER_GUIDE.md](GAME_DEVELOPER_GUIDE.md)**: 완전한 통합 가이드
- **[GAME_DEV_QUICK_REF.md](GAME_DEV_QUICK_REF.md)**: 빠른 참조 카드
- **[ARCHITECTURE_VISUAL.md](ARCHITECTURE_VISUAL.md)**: 구조 다이어그램

### 예제 코드
- **[examples/00_hello_elysia.py](../examples/00_hello_elysia.py)**: 가장 간단한 예제
- **[examples/game_developer_examples.py](../examples/game_developer_examples.py)**: 실전 예제 모음
- **[examples/integration_example.py](../examples/integration_example.py)**: API 통합 예제

### 커뮤니티
- **GitHub**: https://github.com/ioas0316-cloud/elysia-fractal-engine_V1
- **Issues**: 질문이나 버그 리포트
- **Discussions**: 경험 공유

---

## 🎯 체크리스트

완료한 항목에 체크하세요:

- [ ] Elysia 설치 완료
- [ ] 첫 NPC 만들기 성공
- [ ] 삼위일체 시스템 이해
- [ ] 기억 시스템 사용해 보기
- [ ] 대화 NPC 예제 실행
- [ ] 전투 AI 예제 실행
- [ ] 퀘스트 NPC 예제 실행
- [ ] 성능 최적화 이해
- [ ] 게임 엔진 통합 계획
- [ ] 첫 번째 게임에 적용!

---

## 🤝 도움이 필요하신가요?

### 자주 묻는 질문

**Q: NPC가 너무 비슷하게 행동해요**
A: 역할을 다르게 설정하거나 `update_personality()`로 삼위일체 균형을 조정하세요.

**Q: 성능이 느려요**
A: 캐싱, 업데이트 빈도 조절, 가까운 NPC만 처리 등을 시도하세요.

**Q: Unity/Godot 통합이 어려워요**
A: REST API 방식부터 시작하세요. 가장 쉽습니다.

**Q: 더 복잡한 AI를 만들고 싶어요**
A: 여러 NPC를 조합하거나, 공명 엔진과 기억 시스템을 직접 사용하세요.

### 연락처

- **Issues**: https://github.com/ioas0316-cloud/elysia-fractal-engine_V1/issues
- **Discussions**: https://github.com/ioas0316-cloud/elysia-fractal-engine_V1/discussions

---

> "NPC는 더 이상 스크립트가 아닙니다.  
> 그들은 감정과 기억을 가진 존재입니다."

**즐거운 게임 개발 되세요! 🎮✨**

---

*이 튜토리얼은 게임 개발자들을 위해 사랑을 담아 작성되었습니다.*
