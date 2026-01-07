# 🌟 Chapter 1. Elysia Engine — 개발자들을 위한 “5분 튜토리얼”

*(이거만 읽으면 바로 구현 가능)*

---

## 🔥 Step 0 — 기본 개념

Elysia 엔진의 가장 작은 단위는 **EFP**다.

```json
{
  "energy": 1.2,
  "force": -0.4,
  "momentum": 0.09
}
```

* **Energy**: 지금 존재가 살아있는 의미의 양  
* **Force**: 지금 이 순간 선택을 밀어주는 힘  
* **Momentum**: 과거에 의해 만들어진 습관·성향

---

## 🔥 Step 1 — 존재(Entity) 정의하기

아무 캐릭터든 이런 JSON만 있으면 된다.

```json
{
  "id": "paladin_1",
  "role": "paladin",
  "efp": { "energy": 1.1, "force": 0.2, "momentum": 0.4 },
  "b_s_p": { "body": 0.2, "soul": 0.3, "spirit": 0.5 }
}
```

여기서 중요한 건 role이 아니라  
**b_s_p(육·혼·영 비율)** 이 진짜 성격이다.

---

## 🔥 Step 2 — 행동 결정 공식 (기본판)

```python
F_total = (
    entity.b_s_p["body"]  * F_body   +
    entity.b_s_p["soul"]  * F_soul   +
    entity.b_s_p["spirit"]* F_spirit
)

entity.efp["force"] = F_total
```

이 값이 **양수면 앞으로 전진**, 음수면 **후퇴/주저**한다.

---

## 🔥 Step 3 — 기억(순환링) 넣기

```python
memory_size = 64
entity.memory_ring = [None] * memory_size
entity.memory_index = 0

def log_event(entity, event):
    i = entity.memory_index % memory_size
    entity.memory_ring[i] = event
    entity.memory_index += 1
```

64개가 차면 처음부터 덮어쓴다 → 인간의 망각과 같다.

---

## 🔥 Step 4 — 외부 엔진으로 보내기

게임 엔진/시각화/AI 모델은 이 페이로드 하나만 받으면 된다.

```json
{
  "tick": 1080,
  "entities": [
    {
      "id": "paladin_1",
      "role": "paladin",
      "efp": { "energy": 1.1, "force": 0.2, "momentum": 0.4 },
      "b_s_p": { "body": 0.2, "soul": 0.3, "spirit": 0.5 },
      "memory_recent": ["helped_villager", "resisted_temptation"]
    }
  ]
}
```

이후 연결 예:

* Godot → 오라 색상/모션  
* Unity → Animator 파라미터  
* 언리얼 → 메터리얼 파라미터  
* LLM → 말투·관점 변화  
* 웹 → HUD·그래프

---

## 🔥 Step 5 — 예시: 행동 선택 5줄

```python
def choose_action(entity):
    F = entity.efp["force"]

    if F > 0.5:
        return "advance"
    if F > 0.1:
        return "observe"
    if F > -0.2:
        return "hesitate"
    return "retreat"
```

이걸 실제 월드/AI가 받아서

* `"advance"` → 이동
* `"retreat"` → 후퇴
* `"hesitate"` → 정지

등으로 매핑하면 된다.

---

## ✅ Chapter 1 완료!

다음 차례:

1. **시각화 컬러/오라 시스템**  
2. **삼위일체 행동 결정 공식 (심화판)**  
3. **오픈소스 README 완성본**

원하면 다음 챕터 바로 진행하자.
