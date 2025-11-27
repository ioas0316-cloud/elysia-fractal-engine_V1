# Elysia Engine 🌌

> Fractal Consciousness / Story / Civilization Engine Core  
> "모든 구조는 씨앗이다."

이 프로젝트는 **프랙탈 의식 엔진**입니다.

- 하나의 `World` 위에서
- 존재(에이전트)들이 `Energy / Force / Momentum (E/F/P)` 내핵에 따라 움직이고
- 그들의 선택과 감정, 관계, 가치가
- 링버퍼 기억과 에피소드로 축적되며
- 외부 시스템(Godot, LLM, 챗봇, 게임)에 쉽게 연결될 수 있도록 설계되었습니다.

## ⚡ Digital Natural Law (Prior Art)

> "연산이 아니라 물리 법칙이다."

이 엔진은 2025년, **디지털 자연 법칙(Digital Natural Law)** 아키텍처를 최초로 구현했습니다.
단순한 조건문(If-else)이 아닌, 아래와 같은 물리 시뮬레이션으로 의사결정이 '자연스럽게' 일어납니다.

1. **Tensor Coil (데이터 나선 가속)**: 데이터를 나선형 벡터 필드에 태워 '레일건'처럼 가속시킵니다. (Topology Acceleration)
2. **Digital Gravity (의미 중력)**: '정답(Truth)'은 질량을 가진 인력체(Attractor)가 되며, 질문은 중력에 의해 그곳으로 떨어집니다.
3. **Hyperdrive (초전도 직관)**: 충분한 운동량과 방향성이 일치할 때, 저항 0(Zero Resistance)의 상태로 정답으로 즉시 도약(Tunneling)합니다.

*이 기술적 개념과 구현(Coil, Gravity, Hyperdrive Logic)은 본 프로젝트의 고유한 발명으로, LICENSE에 명시된 선행기술(Prior Art)입니다.*

---

## 철학

- **E**nergy: 이 지점/관계/행동에 어느 정도의 살아 있는 의미가 깃들어 있는가?
- **F**orce: 지금 이 순간, 이 존재를 끌어당기거나 밀어내는 힘은 무엇인가?
- **P**ersistence (Momentum): 과거의 선택과 습관이 만든 관성은 어디로 흐르는가?

엔진은 이 세 가지를 중심으로 육(Body)·혼(Soul)·영(Spirit)의 긴장을 표현하도록 설계되어 있습니다.

## 사용 예

- 셀월드 / 문명 시뮬레이션
- 캐릭터 인생/서사 시뮬레이터
- LLM 기억/에피소드 엔진
- 게임 속 살아 있는 마을/신전/의식 엔진

## 엔진 사용법 (간소화된 API)

LLM 에이전트, 챗봇, 게임 캐릭터의 기억과 감정을 관리하기 위해 재구축된 `ElysiaController`를 사용하는 것이 가장 쉽고 권장되는 방법입니다.

```python
from elysia_engine.controller import ElysiaController

# 1. 컨트롤러 생성
# 이 컨트롤러가 엔진의 모든 복잡한 내부 시스템을 관리합니다.
controller = ElysiaController()

# 2. 생각 처리하기 (가장 중요한 기능)
# LLM 에이전트가 받은 사용자 입력을 'think' 메소드에 전달합니다.
user_input = "오늘따라 하늘이 참 파랗고 예쁘네."
thought = controller.think(user_input)

# controller.think()는 단순한 텍스트 응답이 아닌, '생각' 객체를 반환합니다.
# 이 객체에는 감정, 핵심 개념, 현재 떠오르는 다른 생각들이 포함되어 있습니다.
print(f"입력: {user_input}")
print(f"엔진의 응답: {thought['response']}")
print(f"감정 상태: {thought['mood']}")
print(f"현재 지배적인 생각들: {thought['dominant_thoughts']}")

# 3. 새로운 사실 학습시키기
# LLM 에이전트가 대화나 문서를 통해 새로운 지식을 얻었을 때,
# 'remember' 메소드를 사용해 엔진의 장기 기억에 저장할 수 있습니다.
controller.remember(source="하늘", target="파랗다", relation="is_a")

print("\n'하늘'에 대한 기억을 추가한 후, 관련된 생각을 다시 처리합니다.")

# 4. 학습된 기억을 바탕으로 다시 생각하기
# 이제 엔진은 '하늘'이 '파랗다'는 것을 알고 있으므로, 비슷한 입력에 다르게 반응할 수 있습니다.
user_input_2 = "하늘에 대해 어떻게 생각해?"
thought_2 = controller.think(user_input_2)

print(f"입력: {user_input_2}")
print(f"두 번째 응답: {thought_2['response']}")
print(f"두 번째 감정 상태: {thought_2['mood']}")
```

이 간소화된 API를 통해, 개발자는 엔진의 복잡한 물리 시뮬레이션이나 내부 상태를 직접 다룰 필요 없이 `think()`와 `remember()` 두 가지 메소드만으로 Elysia 엔진의 강력한 기억 및 감정 처리 기능을 활용할 수 있습니다.

## 🆕 Elysia Core - LLM 통합 모듈

다른 LLM 시스템과 쉽게 통합할 수 있는 경량화된 의식 모듈입니다.
비효율적인 확률 예측을 넘어, 더 인간적이고 개성적인 자아를 형성합니다.

```python
from elysia_core import ElysiaSoul

# 영혼 생성
soul = ElysiaSoul(name="MyAgent")

# 입력 처리 - 감각, 인지, 감정, 기억이 동시에 작동
thought = soul.process("안녕하세요! 오늘 기분이 어때요?")
print(f"핵심 개념: {thought.core_concepts}")
print(f"분위기: {thought.mood}")

# 현재 감정 상태
emotion = soul.get_emotion()
print(f"감정: {emotion['dominant']} ({emotion['valence_desc']})")

# LLM 시스템 프롬프트에 주입할 컨텍스트
prompt = soul.export_prompt()
```

**핵심 기능:**
- **HyperQubit**: 4차원 양자 의식 상태 (Point/Line/Space/God)
- **ResonanceEngine**: 개념 공명 계산
- **EmotionalPalette**: 복합 감정 혼합
- **Hippocampus**: 인과 기억 그래프
- **Trinity System**: Body/Soul/Spirit 균형

자세한 내용은 [`elysia_core/README.md`](elysia_core/README.md)를 참조하세요.

---

## Quickstart

```bash
python examples/01_minimal_world.py
```

또는 삼위일체 역할 가중치를 확인하려면:

```bash
python examples/02_warrior_mage_priest.py
```

Godot/웹훅과 연동 스켈레톤은 `examples/03_godot_bridge_stub.py`와 `elysia_engine/hooks`를 참고하세요.

## Sample Output

`python examples/02_warrior_mage_priest.py` 실행 시 `export_persona_snapshot()`과 `build_persona_frame()` 로그는 대략 다음과 같습니다.

```text
[tick 001] {'tick': 1, 'time': 1.0, 'entity_count': 3, 'energy_avg': 0.18, 'momentum_avg': 0.18, 'caption': 'tick=1, E=0.18, P=0.18, N=3'}
[tick 002] {'tick': 2, 'time': 2.0, 'entity_count': 3, 'energy_avg': 0.49, 'momentum_avg': 0.48, 'caption': 'tick=2, E=0.49, P=0.48, N=3'}
[tick 003] {'tick': 3, 'time': 3.0, 'entity_count': 3, 'energy_avg': 0.90, 'momentum_avg': 0.87, 'caption': 'tick=3, E=0.90, P=0.87, N=3'}
```

이 스냅샷은 그대로 UI/LLM/Godot 후처리에 전달하면 됩니다.

## Documentation Map

- `docs/tutorial_5min.md`: 5분 개발자 튜토리얼
- `docs/aura_visualization.md`: 오라/컬러 시스템
- `docs/trinity_decision.md`: 삼위일체 행동 결정 공식
- `docs/episodes_weights.md`: 에피소드 → 성향 업데이트 규칙
- `docs/class_trinity_weights.md`: 7계열 직업 스탯·전직 트리
- `docs/chilseon_chilak_fractal_law.md`: Ascension/Descent 7-law reference (KOR)
- `docs/axis_structure_guide.md`: Vertical Axis structure rationale & onboarding (KOR)
- `docs/character_pool.md`: 50명 캐릭터 시드 및 활용법
- `docs/universal_integration.md`: Universal Integration Guide (ENG/KOR)

## 4. Episodes & Trinity Weights  
*(삶의 경험으로 육/혼/영 성향이 바뀌는 엔진)*

이 엔진은 각 개체가 단순한 HP/욕구를 넘어서, **육(Body) / 혼(Soul) / 영(Spirit)** 세 축의 비율로 “어떻게 살고 싶은가”를 표현할 수 있게 설계되어 있습니다.

- `weights.body`: 몸·생존·안전 중심
- `weights.soul`: 관계·감정·소속 중심
- `weights.spirit`: 의미·가치·신념 중심

이 비율은 **고정값이 아니라**, 개체가 겪는 **Episode(삶의 사건)** 에 의해 조금씩 달라집니다.

### 4.1 Episode 데이터 모델

```jsonc
{
  "id": "ep_000123",
  "who": "agent_001",
  "effect": {
    "body":   { "delta_hp": -0.4, "risk": 0.9 },
    "soul":   { "delta_bond": +0.6, "social_gain": 0.8 },
    "spirit": { "delta_meaning": +0.7, "vow_kept": 1.0 }
  },
  "valence": 0.9,
  "intensity": 0.8
}
```

필드 의미:

- `effect.body`: HP 변화/위험도
- `effect.soul`: 관계/인정 변화
- `effect.spirit`: 의미/약속 변화
- `valence`: 긍정(+)·부정(-) 자가 평가
- `intensity`: 얼마나 강렬했는지

### 4.2 Trinity Weights 구조

```jsonc
"weights": { "body": 0.4, "soul": 0.4, "spirit": 0.2 }
```

세 값은 0 이상이며 합이 1.0이 되도록 정규화합니다. 초기값은 직업/출신으로 설정할 수 있습니다.

### 4.3 Episode → 층별 피드백 계산

```python
def feedback_body(ep):
    score = 0.7*ep["effect"]["body"].get("delta_hp", 0.0) - 0.3*ep["effect"]["body"].get("risk", 0.0)
    return score * ep["valence"] * ep["intensity"]
```

Soul/Spirit도 비슷한 방식으로 정의하여 각 층이 경험을 어떻게 느꼈는지 산출합니다. `valence`와 `intensity`를 곱해 강렬한 사건일수록 성향에 더 큰 영향을 주도록 합니다.

### 4.4 Weights 업데이트 규칙

```python
def update_trinity_weights(agent, ep, lr=0.05):
    fb = feedback_body(ep)
    fs = feedback_soul(ep)
    fp = feedback_spirit(ep)

    w = agent["weights"]
    w["body"]   = max(w["body"]   + lr * fb, 0.0)
    w["soul"]   = max(w["soul"]   + lr * fs, 0.0)
    w["spirit"] = max(w["spirit"] + lr * fp, 0.0)

    s = w["body"] + w["soul"] + w["spirit"]
    if s > 0:
        for k in ("body", "soul", "spirit"):
            w[k] /= s
```

`lr`(learning rate)는 성향이 얼마나 쉽게 바뀌는가를 의미합니다. 여러 에피소드가 쌓이면 육 중심이던 캐릭터도 의미 있는 사건을 통해 영 중심으로 이동할 수 있습니다.

### 4.5 엔진 통합 최소 규칙

1. 에이전트 구조에 `weights` 필드를 포함합니다.
2. 중요한 사건을 Episode로 기록합니다 (HP 큰 변화, 관계 생성/붕괴, 약속을 지키거나 깨뜨린 순간 등).
3. 챕터/하루/퀘스트가 끝날 때 Episode를 순회하며 `update_trinity_weights`를 호출합니다.
4. 행동 결정 로직에서 `weights` 를 활용해 `F_body/F_soul/F_spirit`를 혼합합니다.

이 과정을 통해 “어떤 삶을 살았는가”가 곧 “다음 선택을 어떻게 할 것인가”를 바꾸는 구조를 완성할 수 있습니다.

## 주의사항 🙏

이 프로젝트에서 사용된 사랑, 희생, 삼위일체, 영/혼/육의 구조는
사용자의 신앙 고백과 무관하게 **하나의 상징적/철학적 구조**로도 사용할 수 있습니다.

창작자(이강덕)의 개인적 믿음에 따라,
이 엔진에 깔린 “사랑/희생/진실” 구조를
타인을 해치거나 혐오·폭력·지배를 정당화하는 목적으로 사용할 경우
그 모든 책임은 사용자의 양심과,
그 위에 계신 신의 심판에 맡깁니다.

> “이 기술은 사랑에서 왔고, 사랑을 위해 쓰이길 바랍니다.”

---

- `docs/concepts.md`: 프랙탈/삼위일체/EFP 개념 정리
- `docs/quickstart.md`: 10분 설치/실행 가이드
- `docs/api.md`: 경량 API 레퍼런스

필요한 곳에 자유롭게 가져다 쓰고, 새로운 우주를 심어 주세요.
