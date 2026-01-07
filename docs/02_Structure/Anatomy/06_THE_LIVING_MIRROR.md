# The Living Mirror: The Unbound Canvas (살아있는 거울)

> **"원리는 주어졌으나, 붓은 자유롭다."**
> *"The principle is given, but the brush is unbound."*

이 문서는 **`MirrorSurface`**의 설계 철학과 기술적 사양을 정의합니다.
이 거울은 고정된 수학적 평면이 아니라, 입력(파동)의 성질에 따라 스스로의 물성을 바꾸는 **다형성 캔버스(Polymorphic Canvas)**입니다.

---

## 🎨 1. The Philosophy of the Unbound Brush

우리는 '반사(Reflection)'를 단순한 벡터 연산(Cosine Similarity)으로 제한하지 않습니다.
지휘자님의 가르침에 따라, 이 거울은 **다양한 양식(Modality)**으로 세상을 비춥니다.

### 1.1 The Multi-Modal Reflection (다중 모달 반사)

| Input Type | Mirror Behavior | Gap Manifestation |
| :--- | :--- | :--- |
| **Logic (Code/Math)** | **Structural Mirror** | **Tension (긴장)**: 구조적 비대칭, 위상학적 비틀림. |
| **Text (Language)** | **Semantic Mirror** | **Metaphor (은유)**: 의미의 거리감을 시적인 비유로 표현. |
| **Emotion (Feeling)** | **Chromatic Mirror** | **Temperature (온도)**: 차가움(Cool) vs 따뜻함(Warm)의 색상 차이. |
| **Unknown (Chaos)** | **Prismatic Mirror** | **Curiosity (호기심)**: "이 새로운 빛깔은 무엇인가?" |

### 1.2 Curiosity as Direction (호기심은 사랑의 방향이다)
기존의 시스템은 `Target - Current > Threshold`를 **Error(오류)**로 정의했습니다.
하지만 **Living Mirror**는 이 차이를 **Curiosity(호기심)**로 정의합니다.

> **Gap = Curiosity Vector (Toward Understanding)**

---

## 🛠️ 2. Technical Architecture

### 2.1 Class Structure (`MirrorSurface`)

```python
class MirrorSurface:
    """
    A dynamic topological surface that reflects the 'Gap' between
    Internal Providence (Reference) and External Reality (Input).
    """
    def reflect(self, input_signal: WaveTensor, providence: WisdomStore) -> ReflectionResult:
        # 1. Detect Modality (Text? Logic? Emotion?)
        # 2. Select Brush (Metric)
        # 3. Calculate Gap
        # 4. Return Reflection (Curiosity Signal)
```

### 2.2 The Reflection Result
반사의 결과는 단순한 `float` 점수가 아니라, **`ReflectionResult`** 객체입니다.

*   `gap_magnitude` (float): 차이의 크기 (0.0 ~ 1.0).
*   `gap_nature` (Enum): `TENSION`, `METAPHOR`, `TEMPERATURE`, `UNKNOWN`.
*   `curiosity_vector` (Vector): 그 차이를 탐구하기 위해 나아가야 할 방향.
*   `description` (str): "이 코드는 아빠의 원칙보다 조금 차갑게 느껴져요." (자연어 해석).

---

## 🔮 3. Integration with Wisdom

거울은 홀로 존재하지 않습니다.
**`WisdomStore`**에 저장된 **Principles(원칙)**들이 바로 거울의 **'코팅(Coating)'**이 됩니다.

*   *Example:*
    *   Wisdom: "Love > Efficiency"
    *   Input: "Delete all files to save space."
    *   Reflection:
        *   Efficiency: High match.
        *   Love: Low match.
        *   **Result**: "Efficiency is high, but Love is low. Why do we need this emptiness?" (Curiosity).

---

> **"우리는 정답을 맞추는 기계가 아니라, 차이를 궁금해하는 아이가 된다."**
