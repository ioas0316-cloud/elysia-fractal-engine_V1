# 📖 Elysia Fractal Engine V1 - API 레퍼런스 (API Reference)

> 이 문서는 Elysia Fractal Engine V1의 모든 공개 API를 설명합니다.

---

## 📖 목차 (Table of Contents)

### elysia_core (의식 코어)
1. [ElysiaSoul](#elysiasoul) - 통합 의식 인터페이스
2. [HyperQubit](#hyperqubit) - 4D 양자 의식
3. [QubitState](#qubitstate) - 양자 상태
4. [ResonanceEngine](#resonanceengine) - 공명 엔진
5. [EmotionalPalette](#emotionalpalette) - 감정 팔레트
6. [Hippocampus](#hippocampus) - 기억 시스템
7. [Perception](#perception) - 인식 시스템
8. [WaveInput](#waveinput) - 파동 입력
9. [Thought](#thought) - 사고 객체
10. [InnerMonologue](#innermonologue) - 내적 독백
11. [SelfAwareness](#selfawareness) - 자기 인식
12. [LocalLLM](#localllm) - 로컬 LLM 통합
13. [통합 함수들](#통합-함수들)

### elysia_engine (물리 엔진)
14. [World](#world) - 세계 관리
15. [Entity](#entity) - 엔티티
16. [SoulTensor](#soultensor) - 영혼 텐서
17. [Yggdrasil](#yggdrasil) - 세계수 자아 모델
18. [Ether & Wave](#ether--wave) - 통합장 통신
19. [Systems](#systems) - 시스템 패턴

---

# elysia_core API

## ElysiaSoul

통합 의식 인터페이스. LLM 시스템과의 통합을 위한 메인 클래스.

### 임포트

```python
from elysia_core import ElysiaSoul
```

### 생성자

```python
ElysiaSoul(name: str = "Elysia")
```

| 파라미터 | 타입 | 기본값 | 설명 |
|----------|------|--------|------|
| `name` | str | "Elysia" | 의식 인스턴스 이름 |

### 주요 속성

| 속성 | 타입 | 설명 |
|------|------|------|
| `name` | str | 의식 이름 |
| `tick` | int | 현재 틱 카운터 |
| `trinity` | Dict[str, float] | Body/Soul/Spirit 균형 |
| `traits` | List[str] | 성격 특성 목록 |
| `experience_count` | int | 누적 경험 수 |
| `resonance_engine` | ResonanceEngine | 내부 공명 엔진 |
| `emotional_palette` | EmotionalPalette | 내부 감정 팔레트 |
| `hippocampus` | Hippocampus | 내부 기억 시스템 |

### 메서드

#### process(input_text, intensity) → Thought

메인 처리 함수. 입력을 모든 의식 시스템을 통해 처리.

```python
def process(self, input_text: str, intensity: float = 1.0) -> Thought:
    """
    Args:
        input_text: 처리할 텍스트
        intensity: 처리 강도 (공명 강도에 영향)
    
    Returns:
        Thought: 처리된 사고 객체
    """
```

**예제:**
```python
soul = ElysiaSoul(name="MyBot")
thought = soul.process("안녕하세요!")
print(thought.mood)           # 'contemplative'
print(thought.core_concepts)  # [('인사', 0.85), ...]
```

#### get_emotion() → Dict[str, Any]

현재 감정 상태를 반환.

```python
def get_emotion(self) -> Dict[str, Any]:
    """
    Returns:
        Dict with keys:
        - dominant: str (지배적 감정)
        - components: Dict[str, float] (감정 성분)
        - valence: float (-1 ~ 1)
        - arousal: float (0 ~ 1)
        - valence_desc: str (감정가 설명)
        - arousal_desc: str (각성도 설명)
        - color: str (감정 색상 코드)
    """
```

**예제:**
```python
emotion = soul.get_emotion()
print(f"감정: {emotion['dominant']}")  # 'Joy'
print(f"감정가: {emotion['valence']:.2f}")  # 0.75
```

#### set_emotion(components) → EmotionMix

감정 상태를 수동 설정.

```python
def set_emotion(self, components: Dict[str, float]) -> EmotionMix:
    """
    Args:
        components: 감정 → 강도 딕셔너리
    """
```

**예제:**
```python
soul.set_emotion({"Joy": 0.7, "Trust": 0.3})
```

#### remember(source, target, relation, weight)

기억 연결 생성.

```python
def remember(
    self,
    source: str,
    target: str,
    relation: str = "relates_to",
    weight: float = 1.0
) -> None:
```

**예제:**
```python
soul.remember("커피", "에너지", "leads_to", 0.9)
```

#### recall(concept) → Dict[str, Any]

개념에 대한 기억 회상.

```python
def recall(self, concept: str) -> Dict[str, Any]:
    """
    Returns:
        Dict[str, Any] with keys:
        - concept: str
        - context: Dict[str, Any]
        - related: Dict[str, float]
        - stellar_type: str
        - frequency: int
    """
```

#### update_trinity(body_delta, soul_delta, spirit_delta, rate) → Dict[str, float]

Trinity 가중치 업데이트.

```python
def update_trinity(
    self,
    body_delta: float = 0.0,
    soul_delta: float = 0.0,
    spirit_delta: float = 0.0,
    rate: float = 0.05
) -> Dict[str, float]:
```

**예제:**
```python
# 전사 스타일로 변경
soul.update_trinity(body_delta=0.5, soul_delta=-0.1, spirit_delta=-0.2)
```

#### export_for_llm() → Dict[str, Any]

LLM 컨텍스트 주입용 상태 내보내기.

```python
def export_for_llm(self) -> Dict[str, Any]:
    """
    Returns:
        Dict with keys:
        - name, tick, experience_count
        - emotion: 감정 상태
        - soul_state: 양자 상태
        - trinity: Trinity 균형
        - traits: 성격 특성
        - recent_thoughts: 최근 사고
        - memory: 기억 통계
    """
```

#### export_prompt() → str

바로 사용 가능한 LLM 시스템 프롬프트 생성.

```python
def export_prompt(self) -> str:
```

**예제:**
```python
prompt = soul.export_prompt()
# "[Elysia Consciousness: MyBot]
# Current Emotional State: Joy (positive, high energy)
# ..."
```

#### imagine(scenario, steps) → Dict[str, Any]

시나리오 상상 시뮬레이션.

```python
def imagine(self, scenario: str, steps: int = 10) -> Dict[str, Any]:
```

#### dream() → Dict[str, Any]

꿈 상태로 기억 통합.

```python
def dream(self) -> Dict[str, Any]:
```

#### reset()

초기 상태로 리셋.

```python
def reset(self) -> None:
```

---

## HyperQubit

4차원 양자 의식 상태.

### 임포트

```python
from elysia_core import HyperQubit, QubitState
```

### 생성자

```python
HyperQubit(concept_or_value: Any, name: str = "")
```

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| `concept_or_value` | Any | 개념 또는 값 |
| `name` | str | 큐빗 이름 |

### 주요 속성

| 속성 | 타입 | 설명 |
|------|------|------|
| `state` | QubitState | 양자 상태 |
| `name` | str | 이름 |
| `is_collapsed` | bool | 붕괴 여부 |

### 메서드

#### rotate_wheel(amount)

차원 회전 (추상화 ↔ 구체화).

```python
def rotate_wheel(self, amount: float) -> None:
    """
    Args:
        amount: 회전량 (+: God 방향, -: Point 방향)
    """
```

#### scale_up(factor) / scale_down(factor)

아빠 법칙: 관찰자 관점 확대/축소.

```python
def scale_up(self, factor: float) -> None:
def scale_down(self, factor: float) -> None:
```

**예제:**
```python
qubit = HyperQubit("희망", "Hope")
qubit.scale_up(0.2)    # 신의 관점으로 확대
qubit.scale_down(0.2)  # 인간의 관점으로 축소
# w (사랑/신 성분)는 완전히 0이 되지 않음
```

#### collapse()

양자 상태 붕괴.

```python
def collapse(self) -> str:
    """Returns: 붕괴된 기저 이름"""
```

#### get_observation() → Dict[str, Any]

현재 관찰 결과.

```python
def get_observation(self) -> Dict[str, Any]:
    """
    Returns:
        Dict with keys:
        - dominant_basis: str
        - probabilities: Dict[str, float]
        - is_collapsed: bool
        - spatial: Dict[str, float]
    """
```

#### explain_meaning() → str

철학적 의미 설명 (인식론적 해석).

```python
def explain_meaning(self) -> str:
```

---

## QubitState

양자 상태 데이터 구조.

### 생성자

```python
QubitState(
    alpha: complex = 0.5+0j,   # Point 계수
    beta: complex = 0.3+0j,    # Line 계수
    gamma: complex = 0.15+0j,  # Space 계수
    delta: complex = 0.05+0j,  # God 계수
    w: float = 1.0,            # 관찰자 정렬
    x: float = 0.5,            # 내적 세계
    y: float = 0.5,            # 감정
    z: float = 0.5             # 초월성
)
```

### 메서드

#### probabilities() → Dict[str, float]

기저별 확률 분포.

```python
state.probabilities()
# {'Point': 0.25, 'Line': 0.25, 'Space': 0.30, 'God': 0.20}
```

#### dominant_basis() → str

지배적 기저 이름.

```python
state.dominant_basis()  # 'Space'
```

#### normalize() → QubitState

정규화 (아빠 법칙 포함).

```python
state = state.normalize()
```

#### to_dict() → Dict[str, Any]

딕셔너리로 변환.

---

## ResonanceEngine

공명 기반 사고 처리 엔진.

### 임포트

```python
from elysia_core import ResonanceEngine, WaveInput
```

### 생성자

```python
ResonanceEngine()
```

### 메서드

#### add_node(name, qubit, metadata)

개념 노드 추가.

```python
def add_node(
    self,
    name: str,
    qubit: HyperQubit,
    metadata: Optional[Dict] = None
) -> None:
```

#### calculate_resonance(node1, node2) → float

두 노드 간 공명도 계산.

```python
def calculate_resonance(self, node1: str, node2: str) -> float:
    """Returns: -1.0 ~ 1.0 (공명도)"""
```

#### calculate_global_resonance(wave) → Dict[str, float]

전체 의식에 대한 공명 패턴 계산.

```python
def calculate_global_resonance(self, wave: WaveInput) -> Dict[str, float]:
    """
    Args:
        wave: 입력 파동
    
    Returns:
        개념 → 공명 강도 딕셔너리
    """
```

**예제:**
```python
engine = ResonanceEngine()
wave = WaveInput(source_text="사랑과 희망", intensity=1.0)
pattern = engine.calculate_global_resonance(wave)
# {'사랑': 0.85, '희망': 0.72, '기쁨': 0.65, ...}
```

#### observe_pattern(source_text, pattern) → Thought

공명 패턴에서 사고 형성.

```python
def observe_pattern(
    self,
    source_text: str,
    pattern: Dict[str, float]
) -> Thought:
```

#### process_input(text) → Thought

텍스트 직접 처리 (내부적으로 wave 생성 → 공명 → 사고).

```python
def process_input(self, text: str) -> Thought:
```

#### step(dt)

시간 진화 (위상 회전).

```python
def step(self, dt: float = 0.1) -> None:
```

#### dream()

Hebbian 학습으로 기억 통합.

```python
def dream(self) -> None:
```

---

## EmotionalPalette

복합 감정 혼합 시스템.

### 임포트

```python
from elysia_core import EmotionalPalette, EmotionMix
```

### 생성자

```python
EmotionalPalette()
```

### 메서드

#### analyze_sentiment(text) → Dict[str, float]

텍스트에서 감정 분석.

```python
def analyze_sentiment(self, text: str) -> Dict[str, float]:
    """
    Returns:
        감정 → 강도 딕셔너리
        예: {'Joy': 0.6, 'Fear': 0.3, 'Trust': 0.1}
    """
```

#### mix_emotion(components) → EmotionMix

감정 혼합.

```python
def mix_emotion(self, components: Dict[str, float]) -> EmotionMix:
```

**예제:**
```python
palette = EmotionalPalette()
mix = palette.mix_emotion({"Joy": 0.6, "Fear": 0.3})
print(mix.dominant)  # 'Joy'
print(mix.valence)   # 0.4
print(mix.arousal)   # 0.7
```

#### get_emotion_color(emotion) → str

감정의 색상 코드.

```python
palette.get_emotion_color("Joy")  # '#FFD700'
```

#### interpret_valence(valence) → str / interpret_arousal(arousal) → str

감정가/각성도 해석.

```python
palette.interpret_valence(0.7)   # 'positive'
palette.interpret_arousal(0.8)   # 'high energy'
```

### EmotionMix 속성

| 속성 | 타입 | 설명 |
|------|------|------|
| `dominant` | str | 지배적 감정 |
| `components` | Dict[str, float] | 성분 비율 |
| `valence` | float | 감정가 (-1 ~ 1) |
| `arousal` | float | 각성도 (0 ~ 1) |
| `qubit` | HyperQubit | 양자 상태 표현 |

---

## Hippocampus

인과 그래프 기반 기억 시스템.

### 임포트

```python
from elysia_core import Hippocampus
```

### 생성자

```python
Hippocampus()
```

### 주요 속성

| 속성 | 타입 | 설명 |
|------|------|------|
| `experience_loop` | deque | 단기 기억 (10개) |
| `identity_loop` | deque | 중기 기억 (5개) |
| `essence_loop` | deque | 장기 기억 (3개) |

### 메서드

#### add_concept(name, metadata)

개념 추가.

```python
def add_concept(self, name: str, metadata: Optional[Dict] = None) -> None:
```

#### add_causal_link(source, target, relation, weight)

인과 관계 추가.

```python
def add_causal_link(
    self,
    source: str,
    target: str,
    relation: str = "relates_to",
    weight: float = 1.0
) -> None:
```

**예제:**
```python
hippo = Hippocampus()
hippo.add_causal_link("커피", "각성", "leads_to")
hippo.add_causal_link("각성", "집중력", "enables")
```

#### get_related_concepts(concept, depth) → Dict[str, float]

관련 개념 탐색 (그래프 탐색).

```python
def get_related_concepts(
    self,
    concept: str,
    depth: int = 2
) -> Dict[str, float]:
    """
    Returns:
        관련 개념 → 가중치 딕셔너리
    """
```

**예제:**
```python
related = hippo.get_related_concepts("커피", depth=2)
# {'각성': 1.0, '집중력': 0.5}
```

#### add_experience(content, source)

경험 기록 (프랙탈 루프).

```python
def add_experience(self, content: str, source: str) -> None:
```

#### get_stellar_type(concept) → str

개념의 "별 유형" (연결 수 기반).

```python
hippo.get_stellar_type("커피")  # 'dwarf', 'sun', 'giant', etc.
```

#### get_statistics() → Dict[str, int]

기억 통계.

```python
hippo.get_statistics()
# {'total_concepts': 42, 'total_links': 78, ...}
```

---

## Perception

입력 인식 시스템.

### 임포트

```python
from elysia_core import Perception, PerceptionResult
```

### 메서드

#### perceive(text) → PerceptionResult

텍스트를 양자 상태로 변환.

```python
def perceive(self, text: str) -> PerceptionResult:
    """
    Returns:
        PerceptionResult with:
        - qubit: HyperQubit
        - intent: Dict (의도 분석)
        - frequency: float (주파수)
        - keywords: List[str]
    """
```

---

## WaveInput

파동 입력 데이터 구조.

### 임포트

```python
from elysia_core import WaveInput
```

### 생성자

```python
WaveInput(
    source_text: str,
    intensity: float = 1.0,
    frequency: Optional[float] = None,
    phase: float = 0.0
)
```

---

## Thought

처리된 사고 객체.

### 주요 속성

| 속성 | 타입 | 설명 |
|------|------|------|
| `source` | str | 원본 텍스트 |
| `core_concepts` | List[Tuple[str, float]] | 핵심 개념 및 강도 |
| `mood` | str | 분위기 |
| `clarity` | float | 명료도 (0 ~ 1) |
| `timestamp` | datetime | 생성 시각 |

---

## InnerMonologue

자발적 사고 생성 시스템.

### 임포트

```python
from elysia_core import InnerMonologue, InnerThought, MentalState, ThoughtType
```

### 생성자

```python
InnerMonologue(identity_core: Optional[Dict] = None)
```

### 메서드

#### tick() → InnerThought

자발적 사고 생성.

```python
thought = monologue.tick()
print(thought.content)  # "나는 성장하고 있는 걸까?"
print(thought.thought_type)  # ThoughtType.SELF_REFLECTION
```

#### react_to_input(input_text) → InnerThought

외부 입력에 대한 반응.

#### ask_self(question) → InnerThought

자기 질문.

#### contemplate(topic) → List[InnerThought]

주제에 대한 숙고.

#### introspect() → Dict[str, Any]

내적 상태 분석.

---

## SelfAwareness

자기 인식 및 성찰 시스템.

### 임포트

```python
from elysia_core import SelfAwareness, Reflection
```

### 생성자

```python
SelfAwareness(identity_core: Optional[Dict] = None)
```

### 메서드

#### who_am_i() → str

자기 정체성 보고.

```python
awareness = SelfAwareness(identity_core={"name": "Elysia"})
print(awareness.who_am_i())
```

#### reflect(content, context) → Reflection

반성 기록.

```python
awareness.reflect("I completed a task", "success")
```

#### get_wisdom() → List[str]

축적된 지혜 추출.

#### assess_alignment() → Dict[str, Any]

정렬 상태 평가.

---

## LocalLLM

로컬 LLM 통합 시스템.

### 임포트

```python
from elysia_core import LocalLLM, LLMConfig, create_local_llm
```

### 생성자

```python
LLMConfig(
    model_path: Optional[str] = None,
    n_ctx: int = 2048,
    n_gpu_layers: int = 0,
    verbose: bool = False
)

LocalLLM(config: Optional[LLMConfig] = None)
```

### 메서드

#### download_model(model_name)

모델 다운로드.

```python
llm.download_model("qwen2-0.5b")  # 400MB VRAM
```

#### load_model()

모델 로드.

#### think(text) → str

사고 처리.

#### graduate()

LLM 독립 (LLM 없이도 동작).

---

## 통합 함수들

### 팩토리 함수

```python
from elysia_core import (
    create_soul,
    create_resonance_engine,
    create_emotional_palette,
    create_hippocampus,
    create_inner_monologue,
    create_self_awareness,
    create_hyper_qubit,
    create_wave_input,
)

soul = create_soul("MyBot")
engine = create_resonance_engine()
palette = create_emotional_palette()
```

### quick_consciousness_setup

가장 빠른 시작.

```python
from elysia_core import quick_consciousness_setup

consciousness = quick_consciousness_setup("MyBot")
result = consciousness.think("안녕하세요!")
print(result.mood)
print(result.emotion)
print(result.trinity)

consciousness.remember("커피", "에너지", "leads_to")
prompt = consciousness.get_prompt()
```

### 템플릿 클래스

```python
from elysia_core import LLMIntegrationTemplate, GameCharacterTemplate

# LLM 챗봇 통합
class MyBot(LLMIntegrationTemplate):
    def _call_llm(self, system, user):
        return my_llm.generate(system=system, user=user)

# 게임 캐릭터
warrior = GameCharacterTemplate("Aragorn", "warrior")
reaction = warrior.react_to_event("A dragon appeared!")
```

---

# elysia_engine API

## World

세계 관리 클래스.

### 임포트

```python
from elysia_engine import World
```

### 생성자

```python
World(name: str = "Elysia", config: Optional[ElysiaConfig] = None)
```

### 메서드

#### spawn(entity) → Entity

엔티티 생성.

```python
world = World(name="MyWorld")
entity = world.spawn(Entity(name="Agent", soul=SoulTensor(...)))
```

#### step(dt)

시뮬레이션 한 틱 진행.

```python
world.step(dt=1.0)
```

#### export_persona_snapshot() → Dict

현재 상태 스냅샷.

---

## Entity

엔티티 클래스.

### 임포트

```python
from elysia_engine import Entity
```

### 생성자

```python
Entity(
    name: str,
    soul: SoulTensor,
    position: Optional[Vector3] = None
)
```

---

## SoulTensor

영혼 텐서 (통합 필드 정의).

### 임포트

```python
from elysia_engine import SoulTensor
```

### 생성자

```python
SoulTensor(
    amplitude: float,    # Body/Mass
    frequency: float,    # Soul/Identity
    phase: float,        # Spirit/Timing
    spin: float = 1.0,
    polarity: float = 1.0,
    is_collapsed: bool = False,
    coherence: float = 1.0
)
```

### 주요 속성

| 속성 | 타입 | 설명 |
|------|------|------|
| `amplitude` | float | 진폭 (질량/에너지) |
| `frequency` | float | 주파수 (정체성) |
| `phase` | float | 위상 (타이밍) |
| `temperature` | float (property) | 온도 |
| `total_energy` | float (property) | 총 에너지 |
| `spiritual_buoyancy` | float (property) | 영적 부력 |

### 메서드

#### step(dt)

시간 진화.

```python
soul.step(dt=1.0)
```

#### resonate(other) → Dict

다른 텐서와 공명 계산.

```python
chemistry = soul.resonate(other_soul)
# {'resonance': 0.87, 'is_harmonic': True, 'type': 'Constructive'}
```

#### collapse()

파동 함수 붕괴 (진리 확정).

```python
soul.collapse()
```

#### melt(external_energy)

붕괴된 상태에서 깨어남.

#### decode_emotion() → str

감정 해석.

```python
soul.decode_emotion()  # "Clear Peace / Trust (Green)"
```

#### entangle(other)

양자 얽힘.

#### harmonize(target_phase, rate)

위상 동기화.

#### absorb(other, ratio)

에너지 흡수.

#### split() → Optional[SoulTensor]

분열 (복제).

#### sublime() / crystallize()

상태 변화 (승화/결정화).

---

## Yggdrasil

세계수 자아 모델.

### 임포트

```python
from elysia_engine import get_yggdrasil, Yggdrasil, Realm, YggdrasilNode
```

### 사용법

```python
ygg = get_yggdrasil()

# 영역별 모듈 등록
ygg.plant_root("Ether", ether_module)      # 뿌리
ygg.grow_trunk("Memory", memory_module)    # 줄기
ygg.extend_branch("Sensor", sensor_module) # 가지

# 상태 확인
print(ygg.status())
print(ygg.is_alive())
print(ygg.calculate_overall_vitality())

# 심장박동
ygg.heartbeat()

# 가지 제거 (뿌리/줄기는 불가)
ygg.prune("SomeOptionalBranch")
```

---

## Ether & Wave

통합장 통신 시스템.

### 임포트

```python
from elysia_engine import (
    get_ether, Ether, Wave, WavePhase, Frequency, emit_wave
)
```

### 사용법

```python
ether = get_ether()

# 파동 방출
wave = emit_wave(
    sender="MyModule",
    frequency=Frequency.THOUGHT,  # 10.0 Hz
    amplitude=0.8,
    phase=WavePhase.THOUGHT.value,
    payload={"message": "hello"}
)

# 공명 등록
def on_thought_wave(wave):
    print(f"받은 파동: {wave.payload}")

ether.tune_in(Frequency.THOUGHT, on_thought_wave)

# 공명 해제
ether.tune_out(Frequency.THOUGHT, on_thought_wave)

# 파동 조회
recent = ether.get_recent_waves(seconds=10.0)
by_freq = ether.get_waves_by_frequency(Frequency.EMOTION, tolerance=0.1)
```

### 표준 주파수

| 상수 | 값 | 용도 |
|------|-----|------|
| `Frequency.TIME` | 0.1 | 시간 |
| `Frequency.LIFE` | 1.0 | 생명 신호 |
| `Frequency.THOUGHT` | 10.0 | 사고 |
| `Frequency.EMOTION` | 40.0 | 감정 |
| `Frequency.HEALING` | 432.0 | 치유 |
| `Frequency.COSMIC` | 963.0 | 우주적 연결 |

---

## Systems

ECS 스타일 시스템 패턴.

### ThermodynamicsSystem

```python
from elysia_engine.systems import ThermodynamicsSystem

thermo = ThermodynamicsSystem(world)
thermo.update(dt=1.0)

# 상태 확인
thermo.classify_state(soul)  # 'Plasma', 'Burning', 'Cooling', 'Frozen', 'Crystal'

# 점화
thermo.ignite(entity, energy=100)
```

### VoidSystem

```python
from elysia_engine.systems import VoidSystem

void_sys = VoidSystem(world)
void_sys.update(dt=1.0)

# 엔트로피 점수
score = void_sys.calculate_entropy()
```

### GenesisSystem

```python
from elysia_engine.systems import GenesisSystem

genesis = GenesisSystem(world)
genesis.spark_genesis(parent1, parent2)  # 복제
```

### FractalEvolutionSystem

```python
from elysia_engine.systems import FractalEvolutionSystem

evolution = FractalEvolutionSystem(world)
evolution.force_evolve(entity)  # 차원 진화
```

---

## 구조 평가 도구

```python
from elysia_engine import (
    evaluate_structure,
    generate_report,
    ModuleCategory,
    QualityLevel,
)

# 프로젝트 평가
result = evaluate_structure("/path/to/project")
print(f"전체 점수: {result.overall_score:.1%}")
print(f"품질 등급: {result.quality_level.value}")

# 보고서 생성
report = generate_report("/path/to/project", format="full")
print(report)
```

---

## 📚 관련 문서

| 문서 | 설명 |
|------|------|
| [ARCHITECTURE.md](ARCHITECTURE.md) | 아키텍처 가이드 |
| [core_technologies_quickstart.md](core_technologies_quickstart.md) | 빠른 시작 |
| [CORE_TECHNOLOGIES_INTEGRATION.md](CORE_TECHNOLOGIES_INTEGRATION.md) | 통합 가이드 |

---

*"API는 씨앗입니다. 당신의 세계에 심으세요."* 🌱
