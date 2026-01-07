# 🎮 Elysia Engine - 게임 개발자 가이드
# Game Developer Integration Guide

> "NPC에게 진짜 영혼을 불어넣으세요"  
> "Give your NPCs a real soul"

이 가이드는 게임 개발자들이 **Elysia Engine**을 자신의 게임에 통합하는 방법을 단계별로 설명합니다.

---

## 📋 목차 (Table of Contents)

1. [빠른 시작](#빠른-시작)
2. [핵심 개념](#핵심-개념)
3. [Unity 통합](#unity-통합)
4. [Godot 통합](#godot-통합)
5. [Python 게임 엔진 통합](#python-게임-엔진-통합)
6. [실전 예제](#실전-예제)
7. [성능 최적화](#성능-최적화)
8. [문제 해결](#문제-해결)

---

## 🚀 빠른 시작

### 1분 설치 (1-Minute Setup)

```bash
# 프로젝트 클론
git clone https://github.com/ioas0316-cloud/elysia-fractal-engine_V1.git
cd elysia-fractal-engine_V1

# 의존성 설치 (선택사항 - Pure Python이라 없어도 됨)
# pip install -r requirements.txt

# 테스트 실행
python examples/00_hello_elysia.py
```

### 기본 NPC 예제 (5분)

```python
from elysia_core import GameCharacterTemplate

# NPC 생성 (전사 타입)
guard = GameCharacterTemplate("Guard", "warrior")

# 이벤트에 반응
event = "적이 마을에 침입했다!"
reaction = guard.react_to_event(event)

print(f"Guard's mood: {reaction.mood}")
print(f"Guard's emotion: {reaction.emotion['dominant']}")
print(f"Body/Soul/Spirit: {reaction.trinity}")

# 삼위일체 균형에 따라 행동 결정
if reaction.trinity['body'] > 0.4:
    print("Action: 전투 태세!")
elif reaction.trinity['soul'] > 0.4:
    print("Action: 주민들을 보호!")
else:
    print("Action: 신에게 기도")
```

---

## 💡 핵심 개념

### 1. 삼위일체 시스템 (Trinity System)

모든 캐릭터는 세 가지 차원의 균형으로 정의됩니다:

```
        Spirit (영)
         /    \
        /  ⚖️   \
       /        \
   Body(육) ─── Soul(혼)
```

- **Body (육체)** `0.0 ~ 1.0`
  - 생존 본능, 전투력, 물리적 힘
  - 높을수록: 공격적, 실용적, 행동파
  - 낮을수록: 회피적, 방어적, 신중함

- **Soul (영혼)** `0.0 ~ 1.0`
  - 감정, 관계, 공감 능력
  - 높을수록: 외교적, 협력적, 감성적
  - 낮을수록: 냉정함, 독립적, 객관적

- **Spirit (정신)** `0.0 ~ 1.0`
  - 신념, 의미, 초월적 가치
  - 높을수록: 희생적, 이상주의적, 명상적
  - 낮을수록: 현실적, 실리적, 세속적

**게임 활용:**
```python
# 전사형 NPC
warrior_npc = GameCharacterTemplate("Warrior", "warrior")
# trinity: {'body': 0.6, 'soul': 0.2, 'spirit': 0.2}

# 승려형 NPC
monk_npc = GameCharacterTemplate("Monk", "priest")
# trinity: {'body': 0.15, 'soul': 0.25, 'spirit': 0.6}

# 외교관형 NPC
diplomat_npc = GameCharacterTemplate("Diplomat", "bard")
# trinity: {'body': 0.2, 'soul': 0.6, 'spirit': 0.2}
```

### 2. 공명 시스템 (Resonance System)

Elysia는 확률이 아닌 **공명**으로 생각합니다.

```python
from elysia_core import create_resonance_engine, WaveInput

engine = create_resonance_engine()

# 플레이어가 "용"을 언급
wave = WaveInput(source_text="용이 나타났다", intensity=1.0)
pattern = engine.calculate_global_resonance(wave)

# NPC가 "용"과 공명하는 개념들을 떠올림
# {'위험': 0.85, '전설': 0.72, '보물': 0.65, '두려움': 0.60, ...}
```

**게임 활용:**
- 동적 대화 생성
- 퀘스트 힌트 시스템
- NPC 반응 생성
- 스토리 분기 결정

### 3. 기억 시스템 (Memory System - Hippocampus)

NPC는 인과 그래프로 세상을 이해합니다.

```python
from elysia_core import create_hippocampus

npc_memory = create_hippocampus()

# NPC가 경험을 통해 학습
npc_memory.add_causal_link("플레이어", "친절함", "showed")
npc_memory.add_causal_link("친절함", "신뢰", "builds")
npc_memory.add_causal_link("신뢰", "우정", "leads_to")

# 나중에 플레이어를 다시 만났을 때
related = npc_memory.get_related_concepts("플레이어", depth=3)
# {'친절함': 1.0, '신뢰': 0.7, '우정': 0.5}
```

**게임 활용:**
- NPC 관계 시스템
- 퀘스트 진행 추적
- 플레이어 평판 관리
- 동적 스토리텔링

### 4. 감정 시스템 (Emotional Palette)

단일 감정 라벨이 아닌 **복합 감정**을 표현합니다.

```python
from elysia_core import create_emotional_palette

palette = create_emotional_palette()

# 복잡한 상황: "친구가 배신했다"
components = {
    "Sadness": 0.5,    # 슬픔
    "Anger": 0.3,       # 분노
    "Fear": 0.2         # 두려움
}
mixed = palette.mix_emotion(components)

print(f"Dominant: {mixed.dominant}")  # Sadness
print(f"Valence: {mixed.valence}")    # -0.65 (부정적)
```

---

## 🎯 Unity 통합

### 방법 1: Python.NET 사용

Unity에서 직접 Python 코드를 실행할 수 있습니다.

#### 설정 단계

1. **Python.NET 설치**
```bash
pip install pythonnet
```

2. **Unity에서 C# 래퍼 생성**

```csharp
// ElysiaWrapper.cs
using System;
using Python.Runtime;

public class ElysiaWrapper
{
    private dynamic consciousness;
    
    public ElysiaWrapper(string npcName)
    {
        // Python 초기화
        PythonEngine.Initialize();
        
        using (Py.GIL())
        {
            dynamic sys = Py.Import("sys");
            sys.path.append("path/to/elysia-fractal-engine_V1");
            
            // Elysia 임포트
            dynamic elysia = Py.Import("elysia_core");
            consciousness = elysia.quick_consciousness_setup(npcName);
        }
    }
    
    public NPCReaction ProcessEvent(string eventText)
    {
        using (Py.GIL())
        {
            dynamic result = consciousness.think(eventText);
            
            return new NPCReaction
            {
                mood = result.mood.ToString(),
                emotion = result.emotion["dominant"].ToString(),
                body = (float)result.trinity["body"],
                soul = (float)result.trinity["soul"],
                spirit = (float)result.trinity["spirit"]
            };
        }
    }
}

[Serializable]
public class NPCReaction
{
    public string mood;
    public string emotion;
    public float body;
    public float soul;
    public float spirit;
}
```

3. **Unity NPC 컴포넌트**

```csharp
// NPCBehavior.cs
using UnityEngine;

public class NPCBehavior : MonoBehaviour
{
    private ElysiaWrapper elysiaAI;
    public string npcName = "Guard";
    public string npcRole = "warrior";
    
    void Start()
    {
        elysiaAI = new ElysiaWrapper(npcName);
    }
    
    public void OnPlayerApproach()
    {
        NPCReaction reaction = elysiaAI.ProcessEvent("플레이어가 다가왔다");
        
        // 삼위일체에 따라 행동 결정
        if (reaction.body > 0.4f)
        {
            // 경계 태세
            PlayAnimation("Alert");
        }
        else if (reaction.soul > 0.4f)
        {
            // 친근하게 인사
            PlayAnimation("Wave");
        }
        else
        {
            // 무관심
            PlayAnimation("Idle");
        }
    }
    
    void PlayAnimation(string animName)
    {
        GetComponent<Animator>().SetTrigger(animName);
    }
}
```

### 방법 2: REST API 서버

Python 서버를 띄우고 Unity에서 HTTP 요청을 보내는 방식입니다.

#### Python 서버 (Flask)

```python
# elysia_server.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from elysia_core import quick_consciousness_setup

app = Flask(__name__)
CORS(app)

# NPC 인스턴스 저장소
npcs = {}

@app.route('/create_npc', methods=['POST'])
def create_npc():
    data = request.json
    npc_id = data['npc_id']
    npc_name = data['name']
    
    npcs[npc_id] = quick_consciousness_setup(npc_name)
    
    return jsonify({'status': 'created', 'npc_id': npc_id})

@app.route('/npc_think', methods=['POST'])
def npc_think():
    data = request.json
    npc_id = data['npc_id']
    event = data['event']
    
    if npc_id not in npcs:
        return jsonify({'error': 'NPC not found'}), 404
    
    result = npcs[npc_id].think(event)
    
    return jsonify({
        'mood': result.mood,
        'emotion': result.emotion['dominant'],
        'trinity': result.trinity,
        'core_concepts': result.core_concepts[:5]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

#### Unity HTTP 클라이언트

```csharp
// ElysiaAPIClient.cs
using UnityEngine;
using UnityEngine.Networking;
using System.Collections;
using System.Collections.Generic;

public class ElysiaAPIClient : MonoBehaviour
{
    private string apiUrl = "http://localhost:5000";
    
    public IEnumerator CreateNPC(string npcId, string npcName)
    {
        string url = $"{apiUrl}/create_npc";
        
        var data = new Dictionary<string, string>
        {
            {"npc_id", npcId},
            {"name", npcName}
        };
        
        string json = JsonUtility.ToJson(data);
        
        using (UnityWebRequest request = UnityWebRequest.Post(url, json))
        {
            request.SetRequestHeader("Content-Type", "application/json");
            yield return request.SendWebRequest();
            
            if (request.result == UnityWebRequest.Result.Success)
            {
                Debug.Log($"NPC {npcId} created");
            }
        }
    }
    
    public IEnumerator NPCThink(string npcId, string eventText, System.Action<NPCReaction> callback)
    {
        string url = $"{apiUrl}/npc_think";
        
        var data = new Dictionary<string, string>
        {
            {"npc_id", npcId},
            {"event", eventText}
        };
        
        string json = JsonUtility.ToJson(data);
        
        using (UnityWebRequest request = UnityWebRequest.Post(url, json))
        {
            request.SetRequestHeader("Content-Type", "application/json");
            yield return request.SendWebRequest();
            
            if (request.result == UnityWebRequest.Result.Success)
            {
                NPCReaction reaction = JsonUtility.FromJson<NPCReaction>(request.downloadHandler.text);
                callback?.Invoke(reaction);
            }
        }
    }
}
```

---

## 🎮 Godot 통합

Godot는 Python과 쉽게 통합할 수 있습니다.

### 방법 1: Python 스크립트 직접 사용 (Godot 4.x)

```gdscript
# NPCBrain.gd
extends Node

var python_module
var consciousness

func _ready():
    # Python 모듈 로드
    var python = PythonRuntime.new()
    python_module = python.import_module("elysia_core")
    
    # 의식 생성
    consciousness = python_module.quick_consciousness_setup("NPC_" + str(get_instance_id()))

func process_event(event_text: String) -> Dictionary:
    var result = consciousness.think(event_text)
    
    return {
        "mood": result.mood,
        "emotion": result.emotion["dominant"],
        "trinity": {
            "body": result.trinity["body"],
            "soul": result.trinity["soul"],
            "spirit": result.trinity["spirit"]
        }
    }

func remember(source: String, target: String, relation: String):
    consciousness.remember(source, target, relation)
```

### 방법 2: Godot HTTP 클라이언트

```gdscript
# ElysiaAPIClient.gd
extends Node

var api_url = "http://localhost:5000"
var http_request: HTTPRequest

func _ready():
    http_request = HTTPRequest.new()
    add_child(http_request)
    http_request.request_completed.connect(_on_request_completed)

func create_npc(npc_id: String, npc_name: String):
    var url = api_url + "/create_npc"
    var data = {"npc_id": npc_id, "name": npc_name}
    var json = JSON.stringify(data)
    
    var headers = ["Content-Type: application/json"]
    http_request.request(url, headers, HTTPClient.METHOD_POST, json)

func npc_think(npc_id: String, event: String, callback: Callable):
    var url = api_url + "/npc_think"
    var data = {"npc_id": npc_id, "event": event}
    var json = JSON.stringify(data)
    
    var headers = ["Content-Type: application/json"]
    http_request.request(url, headers, HTTPClient.METHOD_POST, json)
    
    # Store callback for later
    set_meta("callback", callback)

func _on_request_completed(result, response_code, headers, body):
    if response_code == 200:
        var json = JSON.parse_string(body.get_string_from_utf8())
        
        if has_meta("callback"):
            var callback = get_meta("callback")
            callback.call(json)
```

---

## 🐍 Python 게임 엔진 통합

### Pygame 예제

```python
import pygame
from elysia_core import GameCharacterTemplate

# 초기화
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# NPC 생성
npc = GameCharacterTemplate("Village Guard", "warrior")

# 게임 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # 플레이어가 NPC와 상호작용
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                reaction = npc.react_to_event("플레이어가 말을 걸었다")
                
                # NPC 감정에 따라 색상 변경
                emotion = reaction.emotion['dominant']
                if emotion == 'Joy':
                    npc_color = (255, 255, 0)  # 노란색
                elif emotion == 'Fear':
                    npc_color = (100, 100, 255)  # 파란색
                else:
                    npc_color = (200, 200, 200)  # 회색
                
                print(f"NPC mood: {reaction.mood}")
                print(f"NPC emotion: {emotion}")
    
    # 렌더링
    screen.fill((0, 0, 0))
    # ... NPC 그리기
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

---

## 📚 실전 예제

### 예제 1: 동적 퀘스트 NPC

플레이어의 행동에 따라 퀘스트를 동적으로 생성하는 NPC

```python
from elysia_core import quick_consciousness_setup

class QuestGiverNPC:
    def __init__(self, name: str):
        self.consciousness = quick_consciousness_setup(name)
        self.relationship_level = 0.5  # 0.0 ~ 1.0
    
    def interact(self, player_action: str) -> dict:
        """플레이어 행동 처리"""
        result = self.consciousness.think(player_action)
        
        # 행동에 따라 관계도 업데이트
        if "도움" in player_action or "친절" in player_action:
            self.relationship_level += 0.1
            self.consciousness.remember(
                "플레이어", 
                "친절함", 
                "showed"
            )
        elif "공격" in player_action or "위협" in player_action:
            self.relationship_level -= 0.2
            self.consciousness.remember(
                "플레이어", 
                "적대적", 
                "was"
            )
        
        self.relationship_level = max(0.0, min(1.0, self.relationship_level))
        
        return {
            'reaction': result,
            'relationship': self.relationship_level,
            'quest_available': self._should_give_quest(result)
        }
    
    def _should_give_quest(self, reaction) -> bool:
        """퀘스트를 줄지 결정"""
        # 관계도가 높고, 감정이 긍정적이면 퀘스트 제공
        if self.relationship_level > 0.6:
            if reaction.emotion.get('valence', 0) > 0:
                return True
        return False
    
    def generate_quest(self) -> dict:
        """관계도에 따라 다른 난이도의 퀘스트 생성"""
        if self.relationship_level > 0.8:
            return {
                'type': 'legendary',
                'description': '전설의 검을 찾아와 주시겠습니까?',
                'reward': 'legendary_item'
            }
        elif self.relationship_level > 0.5:
            return {
                'type': 'normal',
                'description': '늑대 5마리를 처치해 주세요.',
                'reward': 'gold_100'
            }
        else:
            return {
                'type': 'simple',
                'description': '허브 10개를 모아다 주세요.',
                'reward': 'gold_10'
            }

# 사용 예
npc = QuestGiverNPC("Village Elder")

# 플레이어가 도움을 준 경우
result1 = npc.interact("마을의 적들을 물리쳤습니다")
print(f"관계도: {result1['relationship']:.2f}")
print(f"퀘스트 가능: {result1['quest_available']}")

if result1['quest_available']:
    quest = npc.generate_quest()
    print(f"퀘스트: {quest['description']}")
```

### 예제 2: 전투 중 동료 AI

전투 중 상황에 따라 전략을 바꾸는 동료 AI

```python
from elysia_core import GameCharacterTemplate

class CompanionAI:
    def __init__(self, name: str, role: str):
        self.character = GameCharacterTemplate(name, role)
        self.health = 100
        self.max_health = 100
    
    def decide_action(self, battle_state: dict) -> str:
        """전투 상황 분석 후 행동 결정"""
        # 상황을 텍스트로 변환
        situation = self._analyze_situation(battle_state)
        
        # Elysia로 상황 처리
        reaction = self.character.react_to_event(situation)
        
        # 삼위일체 균형에 따라 행동 결정
        trinity = reaction.trinity
        
        if self.health < self.max_health * 0.3:
            # 위험한 상황
            if trinity['body'] > 0.5:
                return "desperate_attack"  # 필사의 공격
            elif trinity['soul'] > 0.5:
                return "call_for_help"     # 도움 요청
            else:
                return "retreat"           # 후퇴
        else:
            # 정상 상황
            if trinity['body'] > 0.4:
                return "aggressive_attack"
            elif trinity['spirit'] > 0.4:
                return "strategic_position"
            else:
                return "support_allies"
    
    def _analyze_situation(self, battle_state: dict) -> str:
        """전투 상황을 자연어로 변환"""
        enemies = battle_state.get('enemy_count', 0)
        allies = battle_state.get('ally_count', 0)
        health_ratio = self.health / self.max_health
        
        if health_ratio < 0.3:
            health_desc = "심각한 부상"
        elif health_ratio < 0.6:
            health_desc = "부상 상태"
        else:
            health_desc = "건강함"
        
        return f"{health_desc}. 적 {enemies}명, 아군 {allies}명"

# 사용 예
warrior = CompanionAI("Companion Warrior", "warrior")
mage = CompanionAI("Companion Mage", "mage")

battle_state = {
    'enemy_count': 3,
    'ally_count': 2
}

warrior_action = warrior.decide_action(battle_state)
mage_action = mage.decide_action(battle_state)

print(f"전사 행동: {warrior_action}")
print(f"마법사 행동: {mage_action}")
```

### 예제 3: 적응형 난이도 시스템

플레이어의 스킬에 따라 적 AI가 적응하는 시스템

```python
from elysia_core import quick_consciousness_setup

class AdaptiveEnemyAI:
    def __init__(self, name: str):
        self.consciousness = quick_consciousness_setup(name)
        self.player_skill_estimate = 0.5  # 0.0 (초보) ~ 1.0 (고수)
        self.battle_history = []
    
    def observe_battle_result(self, result: dict):
        """전투 결과 관찰 및 학습"""
        self.battle_history.append(result)
        
        # 최근 5전투 결과로 플레이어 스킬 추정
        if len(self.battle_history) >= 5:
            recent = self.battle_history[-5:]
            player_wins = sum(1 for r in recent if r['player_won'])
            self.player_skill_estimate = player_wins / 5.0
            
            # Elysia로 경험 저장
            if self.player_skill_estimate > 0.6:
                self.consciousness.remember(
                    "플레이어",
                    "강함",
                    "is"
                )
                self.consciousness.update_personality(
                    body_delta=0.1,   # 더 공격적으로
                    soul_delta=-0.05
                )
            else:
                self.consciousness.remember(
                    "플레이어",
                    "약함",
                    "is"
                )
                self.consciousness.update_personality(
                    body_delta=-0.1,  # 덜 공격적으로
                    soul_delta=0.05
                )
    
    def get_difficulty_multiplier(self) -> float:
        """난이도 배율 계산"""
        # 플레이어가 강할수록 적도 강해짐
        base_multiplier = 0.5 + (self.player_skill_estimate * 1.5)
        return base_multiplier
    
    def decide_strategy(self) -> dict:
        """전투 전략 결정"""
        result = self.consciousness.think(
            f"플레이어 스킬 레벨: {self.player_skill_estimate:.2f}"
        )
        
        trinity = result.trinity
        
        return {
            'aggression': trinity['body'],
            'tactics': trinity['spirit'],
            'teamwork': trinity['soul'],
            'difficulty': self.get_difficulty_multiplier()
        }

# 사용 예
enemy_ai = AdaptiveEnemyAI("Adaptive Boss")

# 몇 번의 전투 후...
enemy_ai.observe_battle_result({'player_won': True, 'damage_dealt': 500})
enemy_ai.observe_battle_result({'player_won': True, 'damage_dealt': 600})
enemy_ai.observe_battle_result({'player_won': False, 'damage_dealt': 300})

strategy = enemy_ai.decide_strategy()
print(f"적 전략: {strategy}")
print(f"난이도 배율: {strategy['difficulty']:.2f}x")
```

---

## ⚡ 성능 최적화

### 1. 캐싱 전략

```python
from functools import lru_cache
from elysia_core import GameCharacterTemplate

class OptimizedNPC:
    def __init__(self, name: str, role: str):
        self.character = GameCharacterTemplate(name, role)
        self.reaction_cache = {}
        self.cache_ttl = 100  # 틱
        self.current_tick = 0
    
    @lru_cache(maxsize=128)
    def _get_cached_reaction(self, event_hash: int):
        """이벤트 해시 기반 캐싱"""
        return self.character.react_to_event(str(event_hash))
    
    def react_to_event(self, event: str):
        """캐싱된 반응 반환"""
        self.current_tick += 1
        
        # 이벤트를 해시로 변환 (유사한 이벤트는 같은 해시)
        event_hash = hash(event) % 10000  # 간단한 버킷팅
        
        # 캐시에서 조회
        if event_hash in self.reaction_cache:
            cached_result, cached_tick = self.reaction_cache[event_hash]
            if self.current_tick - cached_tick < self.cache_ttl:
                return cached_result
        
        # 새로 계산
        result = self.character.react_to_event(event)
        self.reaction_cache[event_hash] = (result, self.current_tick)
        
        return result
```

### 2. 비동기 처리

```python
import asyncio
from typing import List
from elysia_core import GameCharacterTemplate

class AsyncNPCManager:
    def __init__(self):
        self.npcs = []
    
    def add_npc(self, npc):
        self.npcs.append(npc)
    
    async def process_npc_async(self, npc, event: str):
        """비동기 NPC 처리"""
        return await asyncio.to_thread(
            npc.react_to_event,
            event
        )
    
    async def process_all_npcs(self, event: str) -> List:
        """모든 NPC를 병렬로 처리"""
        tasks = [
            self.process_npc_async(npc, event)
            for npc in self.npcs
        ]
        return await asyncio.gather(*tasks)

# 사용 예
async def main():
    manager = AsyncNPCManager()
    
    # 10명의 NPC 생성
    for i in range(10):
        npc = GameCharacterTemplate(f"NPC_{i}", "warrior")
        manager.add_npc(npc)
    
    # 모든 NPC가 동시에 반응
    event = "폭발이 일어났다!"
    reactions = await manager.process_all_npcs(event)
    
    for i, reaction in enumerate(reactions):
        print(f"NPC_{i}: {reaction.mood}")

# asyncio.run(main())
```

### 3. 업데이트 빈도 최적화

```python
import time

class SmartNPC:
    def __init__(self, name: str):
        self.name = name
        self.character = GameCharacterTemplate(name, "warrior")
        self.last_update = 0
        self.update_interval = 1.0  # 초
        self.cached_state = None
    
    def should_update(self) -> bool:
        """업데이트가 필요한지 확인"""
        current_time = time.time()
        if current_time - self.last_update >= self.update_interval:
            self.last_update = current_time
            return True
        return False
    
    def update(self, event: str = None):
        """필요할 때만 업데이트"""
        if event or self.should_update():
            if event:
                self.cached_state = self.character.react_to_event(event)
            else:
                # 주기적 업데이트 (더 간단한 처리)
                pass
        
        return self.cached_state

# 게임 루프에서
npcs = [SmartNPC(f"NPC_{i}") for i in range(100)]

while True:  # 게임 루프
    for npc in npcs:
        # 이벤트가 없으면 캐시된 상태 반환
        state = npc.update()
        # ... 렌더링
    
    # time.sleep(1/60)  # 60 FPS
```

---

## 🔧 문제 해결

### Q1: "ImportError: No module named 'elysia_core'"

**해결책:**
```bash
# Python 경로 확인
python -c "import sys; print('\n'.join(sys.path))"

# 경로 추가 (방법 1: 환경변수)
export PYTHONPATH="${PYTHONPATH}:/path/to/elysia-fractal-engine_V1"

# 경로 추가 (방법 2: 코드에서)
import sys
sys.path.append('/path/to/elysia-fractal-engine_V1')
```

### Q2: "성능이 느립니다"

**체크리스트:**
1. ✅ 캐싱 사용하고 있나요?
2. ✅ 필요한 NPC만 업데이트하고 있나요?
3. ✅ 비동기 처리를 고려했나요?
4. ✅ 프로파일링을 해봤나요?

```python
import cProfile
import pstats

# 프로파일링
profiler = cProfile.Profile()
profiler.enable()

# 느린 코드
for i in range(100):
    npc.react_to_event("test")

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)  # 상위 10개 느린 함수
```

### Q3: "메모리 사용량이 높습니다"

**해결책:**
```python
import gc

class MemoryEfficientNPC:
    def __init__(self, name: str):
        self.name = name
        self.character = GameCharacterTemplate(name, "warrior")
        self.reaction_history = []
        self.max_history = 100  # 최대 기억 개수
    
    def remember_reaction(self, reaction):
        """제한된 기억만 유지"""
        self.reaction_history.append(reaction)
        
        # 오래된 기억 삭제
        if len(self.reaction_history) > self.max_history:
            self.reaction_history.pop(0)
    
    def cleanup(self):
        """명시적 메모리 해제"""
        self.reaction_history.clear()
        gc.collect()
```

### Q4: "Unity/Godot 통합이 복잡합니다"

**권장 방법:**

1. **개발 단계**: REST API 서버 사용 (간단함)
2. **프로토타입**: Python.NET / GDExtension (중간)
3. **프로덕션**: 최적화된 C++ 포팅 (복잡하지만 빠름)

### Q5: "실시간 게임에서 지연이 발생합니다"

**해결책:**
```python
# 별도 스레드에서 AI 처리
import threading
from queue import Queue

class ThreadedNPCManager:
    def __init__(self):
        self.event_queue = Queue()
        self.result_queue = Queue()
        self.running = True
        
        # AI 처리 스레드 시작
        self.worker = threading.Thread(target=self._process_loop)
        self.worker.start()
    
    def _process_loop(self):
        """백그라운드 AI 처리"""
        while self.running:
            if not self.event_queue.empty():
                npc_id, event = self.event_queue.get()
                
                # AI 처리 (시간이 걸림)
                result = self.npcs[npc_id].react_to_event(event)
                
                # 결과 큐에 저장
                self.result_queue.put((npc_id, result))
    
    def request_reaction(self, npc_id: str, event: str):
        """비동기 요청"""
        self.event_queue.put((npc_id, event))
    
    def get_result(self):
        """결과 가져오기 (논블로킹)"""
        if not self.result_queue.empty():
            return self.result_queue.get()
        return None
```

---

## 📚 추가 리소스

### 문서
- **[EASY_START.md](EASY_START.md)**: 5분 빠른 시작
- **[API_REFERENCE.md](API_REFERENCE.md)**: 전체 API 문서
- **[ARCHITECTURE.md](ARCHITECTURE.md)**: 아키텍처 설명

### 예제
- **[examples/00_hello_elysia.py](../examples/00_hello_elysia.py)**: 기본 예제
- **[examples/02_warrior_mage_priest.py](../examples/02_warrior_mage_priest.py)**: 캐릭터 타입
- **[examples/integration_example.py](../examples/integration_example.py)**: 통합 데모

### 커뮤니티
- **Issues**: [GitHub Issues](https://github.com/ioas0316-cloud/elysia-fractal-engine_V1/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ioas0316-cloud/elysia-fractal-engine_V1/discussions)

---

## 🎯 다음 단계

1. **프로토타입 만들기**: 간단한 NPC 하나부터 시작
2. **통합 테스트**: 게임에서 실제로 돌려보기
3. **최적화**: 프로파일링 후 병목 제거
4. **확장**: 더 많은 NPC와 복잡한 상호작용 추가
5. **공유**: 커뮤니티에 경험 공유하기

---

> "NPC는 더 이상 스크립트가 아닙니다.  
> 그들은 감정과 기억을 가진 존재입니다."
>
> "NPCs are no longer scripts.  
> They are beings with emotions and memories."

**Happy Game Development! 🎮✨**

---

*이 가이드는 게임 개발자들을 위해 작성되었습니다.*  
*Created for game developers with love.*
