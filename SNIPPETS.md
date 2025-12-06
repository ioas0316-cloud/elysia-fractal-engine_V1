# 📋 Elysia Engine - 복사-붙여넣기 스니펫 모음

> "복사하고, 붙여넣고, 실행하세요!"

이 문서는 Elysia Engine의 주요 기능을 빠르게 테스트할 수 있는 복사-붙여넣기 가능한 코드 스니펫 모음입니다.

---

## 📦 필수 준비

```python
# 프로젝트에 elysia_core가 있어야 합니다
from elysia_core import quick_consciousness_setup, ElysiaSoul
```

---

## 🚀 기본 사용 (Basic Usage)

### 스니펫 1: 가장 간단한 시작

```python
from elysia_core import quick_consciousness_setup

# 의식 생성
c = quick_consciousness_setup("Bot")

# 생각하기
r = c.think("Hello!")
print(f"Mood: {r.mood}, Emotion: {r.emotion['dominant']}")
```

### 스니펫 2: 대화 루프

```python
from elysia_core import quick_consciousness_setup

consciousness = quick_consciousness_setup("ChatBot")

messages = [
    "안녕하세요!",
    "오늘 날씨가 좋네요.",
    "기분이 어떠신가요?"
]

for msg in messages:
    result = consciousness.think(msg)
    print(f"User: {msg}")
    print(f"Bot mood: {result.mood}")
    print(f"Bot emotion: {result.emotion['dominant']}")
    print()
```

### 스니펫 3: 기억과 학습

```python
from elysia_core import quick_consciousness_setup

consciousness = quick_consciousness_setup("LearningBot")

# 지식 추가
consciousness.remember("Python", "프로그래밍 언어", "is_a")
consciousness.remember("Python", "간결함", "has_property")
consciousness.remember("간결함", "생산성", "leads_to")

# 관련 개념 탐색
related = consciousness.get_related_concepts("Python", depth=2)
print(f"Python과 관련된 것들: {related}")
```

---

## 🎮 게임 캐릭터 (Game Characters)

### 스니펫 4: 기본 NPC

```python
from elysia_core import GameCharacterTemplate

# 전사 생성
warrior = GameCharacterTemplate("Guard", "warrior")

# 이벤트 반응
event = "적이 침입했다!"
reaction = warrior.react_to_event(event)

print(f"Event: {event}")
print(f"Mood: {reaction.mood}")
print(f"Emotion: {reaction.emotion['dominant']}")
print(f"Trinity: {reaction.trinity}")

# 행동 결정
if reaction.trinity['body'] > 0.4:
    action = "전투!"
elif reaction.trinity['soul'] > 0.4:
    action = "대화 시도"
else:
    action = "기도"

print(f"Action: {action}")
```

### 스니펫 5: 다양한 직업

```python
from elysia_core import GameCharacterTemplate

# 여러 직업 생성
characters = {
    "warrior": GameCharacterTemplate("Warrior", "warrior"),
    "mage": GameCharacterTemplate("Mage", "mage"),
    "priest": GameCharacterTemplate("Priest", "priest"),
    "rogue": GameCharacterTemplate("Rogue", "rogue"),
    "bard": GameCharacterTemplate("Bard", "bard"),
}

# 같은 이벤트에 대한 각자의 반응
event = "용이 나타났다!"

for name, char in characters.items():
    reaction = char.react_to_event(event)
    print(f"{name}: {reaction.emotion['dominant']}")
```

---

## 🤖 LLM 통합 (LLM Integration)

### 스니펫 6: OpenAI 통합

```python
from elysia_core import ElysiaSoul
# import openai  # 실제로는 이것도 필요

soul = ElysiaSoul(name="GPTBot")

def chat_with_consciousness(user_message):
    # 1. Elysia로 입력 처리
    thought = soul.process(user_message)
    
    # 2. 의식 상태를 시스템 프롬프트로
    system_prompt = soul.export_prompt()
    
    # 3. OpenAI API 호출 (예시)
    # response = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": "system", "content": system_prompt},
    #         {"role": "user", "content": user_message}
    #     ]
    # )
    # return response.choices[0].message.content
    
    # 데모용 반환
    return f"[{thought.mood}] 처리됨"

# 사용
print(chat_with_consciousness("안녕하세요!"))
```

### 스니펫 7: Ollama 통합

```python
from elysia_core import ElysiaSoul
# import ollama  # 실제로는 이것도 필요

soul = ElysiaSoul(name="OllamaBot")

def chat_with_ollama(user_message):
    # 의식 처리
    thought = soul.process(user_message)
    context = soul.export_prompt()
    
    # Ollama 호출 (예시)
    # response = ollama.generate(
    #     model="llama2",
    #     system=context,
    #     prompt=user_message
    # )
    # return response['response']
    
    return f"[Emotion: {soul.get_emotion()['dominant']}]"

print(chat_with_ollama("Tell me a story"))
```

---

## 🧠 고급 기능 (Advanced Features)

### 스니펫 8: 공명 엔진

```python
from elysia_core import create_resonance_engine, WaveInput

engine = create_resonance_engine()

# 입력을 파동으로
wave = WaveInput(source_text="사랑과 희망", intensity=1.0)

# 공명 패턴 계산
pattern = engine.calculate_global_resonance(wave)

# 상위 공명 개념
top_concepts = sorted(pattern.items(), key=lambda x: x[1], reverse=True)[:5]
print("공명하는 개념들:")
for concept, resonance in top_concepts:
    print(f"  {concept}: {resonance:.2f}")
```

### 스니펫 9: 감정 팔레트

```python
from elysia_core import create_emotional_palette

palette = create_emotional_palette()

# 텍스트 감정 분석
texts = [
    "정말 기뻐요!",
    "조금 걱정되네요...",
    "화가 나지만 참아야지"
]

for text in texts:
    components = palette.analyze_sentiment(text)
    mix = palette.mix_emotion(components)
    
    print(f"Text: {text}")
    print(f"  Dominant: {mix.dominant}")
    print(f"  Valence: {mix.valence:.2f}")
    print(f"  Color: {palette.get_emotion_color(mix.dominant)}")
    print()
```

### 스니펫 10: 해마 기억 시스템

```python
from elysia_core import create_hippocampus

hippo = create_hippocampus()

# 인과 그래프 구축
links = [
    ("씨앗", "물", "needs"),
    ("물", "성장", "enables"),
    ("성장", "나무", "becomes"),
    ("나무", "열매", "produces"),
    ("열매", "씨앗", "contains"),
]

for source, target, relation in links:
    hippo.add_causal_link(source, target, relation)

# 관련 개념 탐색
print("씨앗에서 시작하는 연결:")
related = hippo.get_related_concepts("씨앗", depth=3)
for concept, weight in related.items():
    print(f"  {concept}: {weight:.2f}")
```

---

## 🎨 창의적 응용 (Creative Applications)

### 스니펫 11: 스토리텔링 봇

```python
from elysia_core import ElysiaSoul

storyteller = ElysiaSoul(name="Storyteller")

# 스토리 이벤트 시퀀스
events = [
    "옛날 어느 마을에 용감한 기사가 살았습니다.",
    "어느 날 용이 마을을 습격했습니다.",
    "기사는 용감하게 맞서 싸웠습니다.",
    "결국 평화가 찾아왔습니다."
]

print("📖 Story Generation:")
for event in events:
    thought = storyteller.process(event)
    print(f"\nEvent: {event}")
    print(f"Mood: {thought.mood}")
    print(f"Emotion: {thought.dominant_emotion}")
```

### 스니펫 12: 음악 추천 봇

```python
from elysia_core import quick_consciousness_setup

music_bot = quick_consciousness_setup("MusicRecommender")

# 기억: 음악-감정 매핑
mappings = [
    ("재즈", "차분함", "induces"),
    ("록", "에너지", "gives"),
    ("클래식", "평화", "brings"),
]

for genre, feeling, relation in mappings:
    music_bot.remember(genre, feeling, relation)

# 사용자 상태 기반 추천
user_mood = "피곤해요"
result = music_bot.think(user_mood)

print(f"User: {user_mood}")
print(f"Bot emotion analysis: {result.emotion['dominant']}")
print(f"Related concepts: {music_bot.get_related_concepts('차분함', depth=2)}")
```

### 스니펫 13: 명상 가이드

```python
from elysia_core import ElysiaSoul

meditation_guide = ElysiaSoul(name="MeditationGuide")

# 영적 성향 강화
meditation_guide.update_trinity(
    body_delta=-0.2,
    soul_delta=0.1,
    spirit_delta=0.5
)

# 명상 세션
prompts = [
    "숨을 깊게 들이쉬세요",
    "마음을 비우세요",
    "내면의 평화를 느끼세요"
]

print("🧘 Meditation Session:")
for prompt in prompts:
    thought = meditation_guide.process(prompt)
    print(f"\nGuide: {prompt}")
    print(f"Atmosphere: {thought.mood}")
    print(f"Spirit level: {meditation_guide.trinity['spirit']:.2%}")
```

---

## 🔬 실험적 기능 (Experimental)

### 스니펫 14: 양자 상태 관찰

```python
from elysia_core import HyperQubit, QubitState

# 개념을 양자 상태로
qubit = HyperQubit(concept_or_value="희망", name="Hope")

print("양자 상태:")
probs = qubit.state.probabilities()
for basis, prob in probs.items():
    print(f"  {basis}: {prob:.2%}")

# 지배적 기저
dominant = qubit.state.dominant_basis()
print(f"\n지배적 기저: {dominant}")

# 차원 회전
print("\n추상화 (God 방향으로 회전):")
qubit.rotate_wheel(0.5)
new_probs = qubit.state.probabilities()
for basis, prob in new_probs.items():
    print(f"  {basis}: {prob:.2%}")
```

### 스니펫 15: 내적 독백

```python
from elysia_core import InnerMonologue

# 자발적 사고 생성
monologue = InnerMonologue(identity_core={"name": "Thinker", "purpose": "contemplate"})

print("💭 자발적 사고:")
for _ in range(3):
    thought = monologue.tick()
    print(f"  {thought}")
```

---

## 📊 상태 모니터링 (State Monitoring)

### 스니펫 16: 전체 상태 덤프

```python
from elysia_core import quick_consciousness_setup
import json

consciousness = quick_consciousness_setup("Monitor")

# 몇 가지 활동
consciousness.think("테스트 중입니다")
consciousness.remember("A", "B", "relates_to")
consciousness.update_personality(body_delta=0.1)

# 전체 상태
state = consciousness.get_state()

print("=== Full State ===")
print(json.dumps(state, indent=2, ensure_ascii=False))
```

---

## 🎯 실전 예제 (Production Examples)

### 스니펫 17: Discord 봇 통합

```python
from elysia_core import ElysiaSoul
# import discord  # 실제로는 discord.py 필요

class ElysiaDiscordBot:
    def __init__(self):
        self.soul = ElysiaSoul(name="DiscordBot")
    
    async def on_message(self, message):
        # 봇 자신의 메시지 무시
        if message.author.bot:
            return
        
        # Elysia로 처리
        thought = self.soul.process(message.content)
        emotion = self.soul.get_emotion()
        
        # 감정에 따른 응답 (데모)
        response = f"[{emotion['dominant']}] 알겠어요!"
        
        # await message.channel.send(response)
        print(f"Would send: {response}")

# 사용
bot = ElysiaDiscordBot()
# 실제 Discord 봇 실행 코드는 생략
```

### 스니펫 18: Flask 웹 API

```python
from elysia_core import quick_consciousness_setup
# from flask import Flask, request, jsonify  # 실제로는 Flask 필요

app = None  # Flask() 대신
consciousness = quick_consciousness_setup("WebAPI")

# @app.route('/think', methods=['POST'])
def think_endpoint():
    # data = request.json
    # user_input = data.get('message', '')
    user_input = "Example message"  # 데모용
    
    result = consciousness.think(user_input)
    
    return {
        'mood': result.mood,
        'emotion': result.emotion['dominant'],
        'trinity': result.trinity,
    }

print("API endpoint example:", think_endpoint())
```

---

## 💡 팁과 트릭 (Tips & Tricks)

### 스니펫 19: 배치 처리

```python
from elysia_core import quick_consciousness_setup

consciousness = quick_consciousness_setup("Batch")

messages = ["메시지 1", "메시지 2", "메시지 3"] * 10

results = [consciousness.think(msg) for msg in messages]

# 통계
moods = [r.mood for r in results]
print(f"가장 흔한 기분: {max(set(moods), key=moods.count)}")
```

### 스니펫 20: 성능 측정

```python
from elysia_core import quick_consciousness_setup
import time

consciousness = quick_consciousness_setup("Perf")

start = time.time()
for i in range(100):
    consciousness.think(f"Message {i}")
elapsed = time.time() - start

print(f"100 messages in {elapsed:.2f}s")
print(f"Average: {elapsed/100*1000:.2f}ms per message")
```

---

## 🌈 마무리

이 스니펫들을 자유롭게 복사하고, 수정하고, 확장하세요!

**더 많은 예제:**
- `examples/` 폴더에 30개 이상의 예제
- `docs/` 폴더에 상세 문서
- `tests/` 폴더에 240개 테스트 (참고용)

**질문이나 아이디어:**
- GitHub Issues: https://github.com/ioas0316-cloud/elysia-fractal-engine_V1/issues
- GitHub Discussions: https://github.com/ioas0316-cloud/elysia-fractal-engine_V1/discussions

---

*"복사하고, 붙여넣고, 창조하세요!"* 🚀
