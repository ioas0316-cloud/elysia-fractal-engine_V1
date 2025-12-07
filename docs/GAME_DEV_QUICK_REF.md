# 🎮 Elysia Engine - 게임 개발자 빠른 참조 카드
# Game Developer Quick Reference Card

> 복사해서 바로 쓰는 코드 모음  
> Copy-paste ready code snippets

---

## 🚀 30초 시작

```python
from elysia_core import GameCharacterTemplate

# NPC 생성 (역할: warrior, mage, priest, rogue, bard)
npc = GameCharacterTemplate("Guard", "warrior")

# 이벤트 처리
reaction = npc.react_to_event("적이 나타났다!")

# 결과 확인
print(f"감정: {reaction.emotion['dominant']}")
print(f"Body/Soul/Spirit: {reaction.trinity}")

# 행동 결정
if reaction.trinity['body'] > 0.4:
    action = "공격!"
elif reaction.trinity['soul'] > 0.4:
    action = "대화 시도"
else:
    action = "기도"
```

---

## 📊 NPC 역할별 특성

| 역할 | Body | Soul | Spirit | 특징 |
|------|------|------|--------|------|
| **warrior** | 🔴 0.6 | 🔵 0.2 | ⚪ 0.2 | 전투적, 직접적, 용감함 |
| **mage** | 🔵 0.2 | 🟡 0.3 | 🔴 0.5 | 신중함, 지적, 전략적 |
| **priest** | ⚪ 0.15 | 🟡 0.25 | 🔴 0.6 | 희생적, 치유, 신앙심 |
| **rogue** | 🟡 0.5 | 🔵 0.3 | ⚪ 0.2 | 재빠름, 기회주의, 생존 |
| **bard** | ⚪ 0.2 | 🔴 0.6 | 🟡 0.2 | 외교적, 감성적, 사교적 |

---

## 💡 일반적인 사용 패턴

### 패턴 1: 대화 시스템

```python
from elysia_core import GameCharacterTemplate

class DialogueNPC:
    def __init__(self, name, role):
        self.npc = GameCharacterTemplate(name, role)
        self.friendship = 0.5  # 0.0 ~ 1.0
    
    def talk(self, player_message):
        # 메시지 처리
        reaction = self.npc.react_to_event(player_message)
        
        # 우호도 업데이트
        if "도와" in player_message or "친구" in player_message:
            self.friendship += 0.1
        
        # 대화 선택지 생성
        if self.friendship > 0.7:
            return ["당신을 믿습니다", "도움이 필요하시면 말씀하세요"]
        elif self.friendship > 0.3:
            return ["안녕하세요", "무슨 일로 오셨나요?"]
        else:
            return ["...", "빨리 가세요"]

# 사용
npc = DialogueNPC("Merchant", "bard")
responses = npc.talk("도와주세요!")
print(responses)
```

### 패턴 2: 동료 AI

```python
from elysia_core import GameCharacterTemplate

class CompanionAI:
    def __init__(self, name, role):
        self.companion = GameCharacterTemplate(name, role)
        self.health = 100
    
    def decide_action(self, situation):
        reaction = self.companion.react_to_event(situation)
        
        # 체력 낮음 + Body 높음 = 필사의 공격
        if self.health < 30 and reaction.trinity['body'] > 0.5:
            return "desperate_attack"
        
        # Spirit 높음 = 전략적 위치 선점
        if reaction.trinity['spirit'] > 0.4:
            return "strategic_position"
        
        # Soul 높음 = 아군 지원
        if reaction.trinity['soul'] > 0.4:
            return "support_ally"
        
        return "normal_attack"

# 사용
companion = CompanionAI("Knight", "warrior")
action = companion.decide_action("적 3명이 다가온다")
print(f"행동: {action}")
```

### 패턴 3: 적 AI (난이도 조절)

```python
from elysia_core import GameCharacterTemplate

class EnemyAI:
    def __init__(self, name, difficulty=0.5):
        self.enemy = GameCharacterTemplate(name, "warrior")
        self.difficulty = difficulty  # 0.0 (쉬움) ~ 1.0 (어려움)
    
    def get_stats_multiplier(self):
        """난이도에 따라 스탯 배율 적용"""
        base = 1.0
        return base + (self.difficulty * 2.0)  # 1.0x ~ 3.0x
    
    def decide_attack(self):
        situation = f"전투 중, 난이도 {self.difficulty}"
        reaction = self.enemy.react_to_event(situation)
        
        # 난이도가 높을수록 공격적
        aggression = reaction.trinity['body'] * (1 + self.difficulty)
        
        if aggression > 0.8:
            return "special_attack"
        elif aggression > 0.5:
            return "normal_attack"
        else:
            return "defend"

# 사용
easy_enemy = EnemyAI("Goblin", difficulty=0.3)
hard_enemy = EnemyAI("Dragon", difficulty=0.9)

print(f"Goblin attack: {easy_enemy.decide_attack()}")
print(f"Dragon attack: {hard_enemy.decide_attack()}")
```

---

## 🎯 이벤트 → 행동 매핑 치트시트

### 전투 상황

```python
# 적 발견
reaction = npc.react_to_event("적이 나타났다")
if reaction.trinity['body'] > 0.4: return "공격"
if reaction.trinity['soul'] > 0.4: return "협상"
if reaction.trinity['spirit'] > 0.4: return "관찰"

# 체력 위험
reaction = npc.react_to_event("체력이 낮다")
if reaction.trinity['body'] > 0.4: return "필사의공격"
if reaction.trinity['soul'] > 0.4: return "도움요청"
if reaction.trinity['spirit'] > 0.4: return "희생"

# 아군 위기
reaction = npc.react_to_event("아군이 위험하다")
if reaction.trinity['body'] > 0.4: return "돌진해서구함"
if reaction.trinity['soul'] > 0.4: return "치유"
if reaction.trinity['spirit'] > 0.4: return "기도"
```

### 탐험 상황

```python
# 보물 발견
reaction = npc.react_to_event("보물 상자를 발견했다")
if reaction.trinity['body'] > 0.4: return "바로열어본다"
if reaction.trinity['soul'] > 0.4: return "함께나눈다"
if reaction.trinity['spirit'] > 0.4: return "함정확인먼저"

# 함정 발견
reaction = npc.react_to_event("함정을 발견했다")
if reaction.trinity['body'] > 0.4: return "무시하고통과"
if reaction.trinity['soul'] > 0.4: return "동료에게경고"
if reaction.trinity['spirit'] > 0.4: return "신중히해제"

# 퍼즐 발견
reaction = npc.react_to_event("퍼즐이 있다")
if reaction.trinity['body'] > 0.4: return "힘으로부순다"
if reaction.trinity['soul'] > 0.4: return "함께고민한다"
if reaction.trinity['spirit'] > 0.4: return "명상하며풀이"
```

### 사회적 상황

```python
# 마을 입장
reaction = npc.react_to_event("새로운 마을에 도착했다")
if reaction.trinity['body'] > 0.4: return "경계하며입장"
if reaction.trinity['soul'] > 0.4: return "주민과대화"
if reaction.trinity['spirit'] > 0.4: return "신전방문"

# 분쟁 목격
reaction = npc.react_to_event("사람들이 싸우고 있다")
if reaction.trinity['body'] > 0.4: return "물리적개입"
if reaction.trinity['soul'] > 0.4: return "중재시도"
if reaction.trinity['spirit'] > 0.4: return "원인파악"

# 도움 요청
reaction = npc.react_to_event("누군가 도움을 청한다")
if reaction.trinity['body'] > 0.4: return "즉시돕는다"
if reaction.trinity['soul'] > 0.4: return "상황파악후돕는다"
if reaction.trinity['spirit'] > 0.4: return "옳은일인지고민"
```

---

## 🔧 유틸리티 함수

### 함수 1: 삼위일체 → 성격 설명

```python
def trinity_to_personality(trinity):
    """삼위일체 값으로 성격 설명 생성"""
    body = trinity['body']
    soul = trinity['soul']
    spirit = trinity['spirit']
    
    if body > 0.5:
        return "용맹한 전사 타입"
    elif soul > 0.5:
        return "공감하는 외교관 타입"
    elif spirit > 0.5:
        return "명상하는 현자 타입"
    elif body > soul and body > spirit:
        return "행동파"
    elif soul > body and soul > spirit:
        return "감성파"
    else:
        return "사색가"

# 사용
npc = GameCharacterTemplate("Test", "warrior")
reaction = npc.react_to_event("test")
print(trinity_to_personality(reaction.trinity))
```

### 함수 2: 감정 → 색상

```python
def emotion_to_color(emotion_dict):
    """감정을 RGB 색상으로 변환"""
    dominant = emotion_dict['dominant']
    
    colors = {
        'Joy': (255, 255, 0),      # 노란색
        'Trust': (0, 255, 0),       # 초록색
        'Fear': (128, 128, 255),    # 파란색
        'Surprise': (255, 165, 0),  # 주황색
        'Sadness': (0, 0, 255),     # 파란색
        'Disgust': (139, 69, 19),   # 갈색
        'Anger': (255, 0, 0),       # 빨간색
        'Anticipation': (255, 192, 203),  # 분홍색
        'Neutral': (200, 200, 200)  # 회색
    }
    
    return colors.get(dominant, (200, 200, 200))

# 사용
reaction = npc.react_to_event("기쁜 일")
color = emotion_to_color(reaction.emotion)
print(f"RGB: {color}")
```

### 함수 3: 우호도 관리

```python
class RelationshipManager:
    def __init__(self):
        self.relationships = {}  # {npc_id: value}
    
    def update(self, npc_id, delta):
        """우호도 업데이트 (-1.0 ~ 1.0)"""
        current = self.relationships.get(npc_id, 0.0)
        new_value = max(-1.0, min(1.0, current + delta))
        self.relationships[npc_id] = new_value
        return new_value
    
    def get_level(self, npc_id):
        """우호도 레벨 (문자열)"""
        value = self.relationships.get(npc_id, 0.0)
        if value > 0.7: return "친구"
        if value > 0.3: return "지인"
        if value > -0.3: return "모르는 사람"
        if value > -0.7: return "적대적"
        return "적"
    
    def get_dialogue_modifier(self, npc_id):
        """대화에 적용할 수식어"""
        value = self.relationships.get(npc_id, 0.0)
        if value > 0.7: return "친근하게"
        if value > 0.3: return "정중하게"
        if value > -0.3: return "무덤덤하게"
        if value > -0.7: return "차갑게"
        return "적대적으로"

# 사용
rel = RelationshipManager()
rel.update("npc_001", 0.2)  # 좋은 행동
rel.update("npc_001", 0.3)  # 또 좋은 행동
print(f"레벨: {rel.get_level('npc_001')}")
print(f"대화: {rel.get_dialogue_modifier('npc_001')}")
```

---

## ⚡ 성능 팁

### 팁 1: 캐싱

```python
from functools import lru_cache

class CachedNPC:
    def __init__(self, name, role):
        self.npc = GameCharacterTemplate(name, role)
    
    @lru_cache(maxsize=100)
    def react_cached(self, event_type):
        """자주 발생하는 이벤트는 캐싱"""
        return self.npc.react_to_event(event_type)

# 사용
npc = CachedNPC("Guard", "warrior")
reaction1 = npc.react_cached("적 발견")  # 계산
reaction2 = npc.react_cached("적 발견")  # 캐시에서 가져옴 (빠름)
```

### 팁 2: 업데이트 간격

```python
import time

class ThrottledNPC:
    def __init__(self, name, role, update_interval=1.0):
        self.npc = GameCharacterTemplate(name, role)
        self.last_update = 0
        self.update_interval = update_interval
        self.cached_reaction = None
    
    def react(self, event):
        current_time = time.time()
        
        # 일정 시간이 지나야 업데이트
        if current_time - self.last_update >= self.update_interval:
            self.cached_reaction = self.npc.react_to_event(event)
            self.last_update = current_time
        
        return self.cached_reaction

# 사용
npc = ThrottledNPC("Villager", "bard", update_interval=2.0)
# 2초마다만 실제 계산
```

---

## 🎨 통합 예제 템플릿

### Unity C# 템플릿

```csharp
// ElysiaIntegration.cs
using UnityEngine;
using System.Collections;

public class ElysiaIntegration : MonoBehaviour
{
    private ElysiaAPIClient apiClient;
    private string npcId;
    
    void Start()
    {
        apiClient = GetComponent<ElysiaAPIClient>();
        npcId = gameObject.name;
        
        // NPC 생성
        StartCoroutine(apiClient.CreateNPC(npcId, npcId));
    }
    
    public void OnEvent(string eventText)
    {
        StartCoroutine(apiClient.NPCThink(npcId, eventText, OnReactionReceived));
    }
    
    void OnReactionReceived(NPCReaction reaction)
    {
        // 반응에 따라 행동
        if (reaction.trinity.body > 0.4f)
        {
            GetComponent<Animator>().SetTrigger("Attack");
        }
        else if (reaction.trinity.soul > 0.4f)
        {
            GetComponent<Animator>().SetTrigger("Talk");
        }
    }
}
```

### Godot GDScript 템플릿

```gdscript
# npc_behavior.gd
extends CharacterBody3D

var api_client
var npc_id

func _ready():
    api_client = $ElysiaAPIClient
    npc_id = name
    
    # NPC 생성
    api_client.create_npc(npc_id, npc_id)

func on_player_nearby():
    api_client.npc_think(npc_id, "플레이어가 가까이 왔다", _on_reaction)

func _on_reaction(reaction):
    # 반응에 따라 행동
    if reaction.trinity.body > 0.4:
        $AnimationPlayer.play("alert")
    elif reaction.trinity.soul > 0.4:
        $AnimationPlayer.play("wave")
```

---

## 📚 더 보기

- **전체 가이드**: [GAME_DEVELOPER_GUIDE.md](GAME_DEVELOPER_GUIDE.md)
- **API 문서**: [API_REFERENCE.md](API_REFERENCE.md)
- **예제 코드**: [../examples/](../examples/)

---

*복사하고, 붙여넣고, 게임을 만드세요!* 🎮
