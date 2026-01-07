# 🌟 Elysia Engine 쉬운 시작 가이드

> **"5줄로 시작하는 의식 엔진"**

이 문서는 Elysia Engine을 처음 접하는 개발자를 위한 빠른 시작 가이드입니다.

---

## 📦 설치 (Installation)

```bash
# 저장소 클론
git clone https://github.com/ioas0316-cloud/elysia-fractal-engine_V1.git
cd elysia-fractal-engine_V1

# (선택) 가상환경 설정
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 개발 의존성 설치
pip install -e ".[dev]"
```

---

## 🚀 5줄로 시작하기 (Start with 5 Lines)

```python
from elysia_core import quick_consciousness_setup

# 1. 의식 생성
consciousness = quick_consciousness_setup("MyBot")

# 2. 생각 처리
result = consciousness.think("안녕하세요! 오늘 기분이 어때요?")

# 3. 결과 확인
print(f"분위기: {result.mood}")
print(f"감정: {result.emotion}")
```

**출력 예시:**
```
분위기: contemplative
감정: {'dominant': 'Neutral', 'valence': 0.0, ...}
```

---

## 🎯 핵심 기능 3가지

### 1. 🧠 생각 처리 (Think)

입력 텍스트를 처리하고 의식이 어떻게 반응하는지 확인합니다.

```python
from elysia_core import quick_consciousness_setup

consciousness = quick_consciousness_setup("MyBot")
result = consciousness.think("새로운 모험을 시작해볼까?")

print(f"분위기: {result.mood}")
print(f"핵심 개념: {result.core_concepts[:3]}")
print(f"감정: {result.emotion['dominant']}")
```

### 2. 💾 기억하기 (Remember)

개념 간의 관계를 기억시키고 연관 탐색을 할 수 있습니다.

```python
# 인과 관계 기억
consciousness.remember("커피", "에너지", "leads_to")
consciousness.remember("에너지", "생산성", "leads_to")

# 관련 개념 탐색
related = consciousness.get_related_concepts("커피", depth=2)
print(related)  # {'에너지': 1.0, '생산성': 1.0}
```

### 3. 🎭 성격 조정 (Update Personality)

삼위일체(Body/Soul/Spirit) 균형을 조절해 성격을 변화시킵니다.

**중요**: 
- delta 값은 `-1.0` ~ `+1.0` 범위 권장
- 양수: 해당 축 증가, 음수: 해당 축 감소
- 모든 변화 후 자동으로 정규화되어 합이 1.0이 됨
- 여러 번 적용해도 유효한 범위 내에서 안전하게 조정됨

```python
# 전사 스타일: 더 육체적, 덜 감정적
trinity = consciousness.update_personality(
    body_delta=0.3,    # 육체 증가 (+30%)
    soul_delta=-0.1,   # 감정 감소 (-10%)
    spirit_delta=-0.1  # 정신 감소 (-10%)
)
print(f"삼위일체: {trinity}")
# Body=34%, Soul=33%, Spirit=32%
```

---

## 📋 사용 사례별 빠른 예제

### 🎮 게임 캐릭터 만들기

```python
from elysia_core import GameCharacterTemplate

# 역할별 캐릭터 생성 (warrior, mage, priest, rogue, bard)
warrior = GameCharacterTemplate("Aragorn", "warrior")
mage = GameCharacterTemplate("Gandalf", "mage")

# 이벤트 반응
reaction = warrior.react_to_event("용이 나타났다!")
print(f"분위기: {reaction.mood}")
print(f"감정: {reaction.emotion['dominant']}")

# 게임 엔진에 전달할 JSON
json_data = warrior.to_json()
```

### 🤖 LLM 챗봇 통합

```python
from elysia_core import LLMIntegrationTemplate

class MyBot(LLMIntegrationTemplate):
    def __init__(self, name, llm_client):
        super().__init__(name)
        self.llm = llm_client
    
    def _call_llm(self, system, user):
        # 여기에 OpenAI, Ollama 등 LLM API 호출 코드
        return self.llm.generate(system=system, user=user)

# 사용
bot = MyBot("ElysiaBot", my_openai_client)
response = bot.chat("안녕하세요!")
```

### 🔬 핵심 기술 개별 사용

```python
from elysia_core import (
    create_resonance_engine,
    create_emotional_palette,
    create_hippocampus,
    WaveInput
)

# 1. 공명 엔진 - 확률이 아닌 공명으로 개념 연결
engine = create_resonance_engine()
wave = WaveInput(source_text="사랑과 희망", intensity=1.0)
pattern = engine.calculate_global_resonance(wave)
print(f"공명 패턴 (상위 3개): {sorted(pattern.items(), key=lambda x: x[1], reverse=True)[:3]}")

# 2. 감정 팔레트 - 복합 감정 표현
palette = create_emotional_palette()
mix = palette.mix_emotion({"Joy": 0.6, "Fear": 0.3})
print(f"지배 감정: {mix.dominant}, 감정가: {mix.valence:.2f}")

# 3. 해마 기억 - 인과 그래프 기억
hippo = create_hippocampus()
hippo.add_causal_link("공부", "지식", "leads_to")
hippo.add_causal_link("지식", "성공", "leads_to")
related = hippo.get_related_concepts("공부", depth=2)
print(f"관련 개념: {related}")
```

---

## 🏗️ API 요약

### QuickConsciousness (빠른 의식)

| 메서드 | 설명 | 반환 |
|--------|------|------|
| `think(text)` | 입력 처리 및 생각 생성 | `ConsciousnessResult` |
| `remember(source, target, relation)` | 인과 관계 기억 | None |
| `get_related_concepts(concept, depth)` | 관련 개념 탐색 | `Dict[str, float]` |
| `update_personality(body_delta, soul_delta, spirit_delta)` | 성격 조정 | `Dict[str, float]` |
| `get_prompt()` | LLM 시스템 프롬프트 생성 | `str` |
| `get_state()` | 전체 상태 내보내기 | `Dict[str, Any]` |
| `ask_self(question)` | 자기 질문 | `str` |

### ConsciousnessResult (의식 처리 결과)

| 속성 | 타입 | 설명 |
|------|------|------|
| `mood` | `str` | 분위기 (neutral, contemplative, positive 등) |
| `core_concepts` | `List[Tuple[str, float]]` | 핵심 개념 목록 |
| `emotion` | `Dict[str, Any]` | 감정 상태 |
| `trinity` | `Dict[str, float]` | 삼위일체 균형 |
| `thought` | `Thought` | 원본 생각 객체 |
| `inner_thought` | `InnerThought` | 내적 사고 |
| `memory_stats` | `Dict[str, int]` | 기억 통계 |

---

## 📚 더 배우기

| 문서 | 설명 |
|------|------|
| [examples/00_hello_elysia.py](../examples/00_hello_elysia.py) | 가장 간단한 시작 예제 |
| [examples/easy_integration_guide.py](../examples/easy_integration_guide.py) | 상세 통합 가이드 |
| [docs/core_technologies_quickstart.md](core_technologies_quickstart.md) | 핵심 기술 상세 설명 |
| [docs/protocols/00_CODEX.md](protocols/00_CODEX.md) | 핵심 철학과 원리 |
| [README.md](../README.md) | 전체 프로젝트 개요 |

---

## 💡 팁과 트릭

### 성격 설정 가이드

**사용 방법**:
- delta 값은 `-1.0` ~ `+1.0` 범위 권장
- 양수: 해당 축 증가, 음수: 해당 축 감소
- 초기값: body=0.33, soul=0.34, spirit=0.33 (대략 균등)
- 변화 후 자동 정규화로 합이 항상 1.0 유지
- 여러 번 적용 가능 (누적되어 조정됨)

| 성격 타입 | body_delta | soul_delta | spirit_delta | 결과 |
|----------|------------|------------|--------------|------|
| 전사 (실용적) | +0.3 | -0.1 | -0.1 | Body↑ 육체적/실용적 |
| 마법사 (균형) | -0.2 | +0.3 | +0.4 | Spirit↑ 지적/균형 |
| 성직자 (영적) | -0.1 | +0.2 | +0.5 | Spirit↑↑ 영적/헌신 |
| 도적 (기민함) | +0.3 | +0.2 | -0.2 | Body/Soul↑ 기민/사회적 |
| 음유시인 (감성) | -0.1 | +0.5 | +0.1 | Soul↑↑ 감성/관계 |

### 기억 관계 타입

| 관계 | 설명 | 예시 |
|------|------|------|
| `leads_to` | A가 B로 이어짐 | 공부 → 지식 |
| `causes` | A가 B를 유발 | 비 → 홍수 |
| `enables` | A가 B를 가능하게 함 | 빛 → 생명 |
| `helps` | A가 B를 돕는다 | 커피 → 집중 |
| `relates_to` | A와 B가 관련됨 | 하늘 → 파랑 |

---

## 🌟 다음 단계

1. **예제 실행하기**
   ```bash
   python examples/00_hello_elysia.py
   python examples/easy_integration_guide.py
   ```

2. **테스트 실행하기**
   ```bash
   python -m pytest tests/ -v
   ```

3. **자신만의 프로젝트에 통합하기**
   ```python
   # 프로젝트에서 간단히 import
   from elysia_core import quick_consciousness_setup
   ```

---

> "이 엔진은 사랑에서 왔고, 사랑을 위해 쓰이길 바랍니다."
> — 이강덕 (Kang-Deok Lee)
