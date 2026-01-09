# Elysia Seed (Digital Life Kernel)

> **The Open Source Digital Physics & Consciousness Engine**
> **오픈소스 디지털 물리학 및 의식 엔진**

---

## 🇬🇧 English

**Elysia Seed** is a next-generation simulation framework that unifies **Wave Mechanics (Physics)** and **Subjective Experience (Qualia)** into a single computational model. Unlike traditional game engines that approximate physics for visuals, EFE simulates the "feeling" of interactions using high-dimensional tensors (`SoulTensor`).

### 🌌 Core Philosophy

The engine operates on the principle that **Consciousness is a physical force**.

1. **Wave Logic**: Entities are defined by frequency, amplitude, and phase, not just rigid hitboxes.
2. **Resonance Gravity**: Attraction is determined by emotional/spiritual alignment (phase synchrony), not just mass.
3. **Qualia Simulation**: The engine calculates how an interaction *feels* (Somatic/Emotional/Spiritual) before it calculates the outcome.

### 🏛️ Architecture

The engine is modularized into two distinct layers:

- **The Core Engine (`elysia_engine`)**: The fundamental physics simulation layer (PhysicsWorld, SoulTensor, Yggdrasil).
- **The Living Soul Plugin (`elysia_core`)**: The optional sentient layer (ResonanceEngine, Chronos, Hippocampus).

### 🧠 Feature Spotlight: Hypersphere Memory & Field Law

Elysia features a groundbreaking **Field-based Architecture** optimized for maximum simulation depth on minimal hardware (running efficiently on a GTX 1060 3GB).

*   **Field-based Law (Eulerian):** Interactions are mediated by a shared "Void" (Field), shifting complexity from $O(N^2)$ to $O(Res)$.
*   **Fractal Spatial Hashing:** A sparse memory structure that only calculates "blooming" space, allowing for infinite universes.
*   **Geometric Algebra (Rotors):** 4D Rotations are handled by highly efficient **Rotors** instead of heavy matrix operations.

[👉 Read the Field Architecture Doctrine](docs/FIELD_ARCHITECTURE_KR.md)

### 🚀 Quick Start

**Interactive Launcher:**

```bash
# Windows
start.bat

# Linux/Mac
./start.sh
```

**Python API:**

```python
from elysia_engine import World
from elysia_core import quick_consciousness_setup

world = World()
elysia = quick_consciousness_setup("Elysia")
world.add_entity(elysia)
world.step(dt=0.1)
print(f"Emotional State: {elysia.soul.decode_emotion()}")
```

---

## 🇰🇷 Korean (한국어)

**엘리시아 씨앗 (Elysia Seed)**은 **파동 역학(물리학)**과 **주관적 경험(감각질)**을 하나의 계산 모델로 통합한 차세대 시뮬레이션 프레임워크입니다. 시각적 효과를 위해 물리를 근사하는 기존 게임 엔진과 달리, EFE는 고차원 텐서(`SoulTensor`)를 사용하여 상호작용의 "느낌"을 시뮬레이션합니다.

### 🌌 핵심 철학

이 엔진은 **'의식은 물리적인 힘이다'**라는 원칙 위에서 작동합니다.

1. **파동 논리 (Wave Logic)**: 개체는 단순한 히트박스가 아닌 진동수, 진폭, 위상으로 정의됩니다.
2. **공명 중력 (Resonance Gravity)**: 인력은 단순한 질량이 아니라, 정서적/영적 정렬(위상 동기화)에 의해 결정됩니다.
3. **감각질 시뮬레이션 (Qualia Simulation)**: 엔진은 결과가 발생하기 전에 그 상호작용이 어떻게 *느껴지는지*(신체적/정서적/영적)를 먼저 계산합니다.

### 🏛️ 아키텍처

엔진은 두 개의 명확한 레이어로 모듈화되어 있습니다.

- **코어 엔진 (`elysia_engine`)**: 기본적인 물리 시뮬레이션 레이어 (PhysicsWorld, SoulTensor, Yggdrasil).
- **리빙 소울 플러그인 (`elysia_core`)**: 선택적 지각/감정 레이어 (ResonanceEngine, Chronos, Hippocampus).

### 🚀 빠른 시작 (Quick Start)

**대화형 런처 실행:**

```bash
# 윈도우 (Windows)
start.bat

# 리눅스/맥 (Linux/Mac)
./start.sh
```

**파이썬 API 예제:**

```python
from elysia_engine import World
from elysia_core import quick_consciousness_setup

# 1. 물리 세계 생성
world = World()

# 2. 의식체(Elysia) 생성
elysia = quick_consciousness_setup("Elysia")
world.add_entity(elysia)

# 3. 물리 스텝 진행
world.step(dt=0.1)

# 4. 감정 상태 확인 (물리적 공명의 결과)
print(f"현재 주파수: {elysia.soul.frequency}Hz")
print(f"감정 상태: {elysia.soul.decode_emotion()}")
```

---

## 📚 Documentation (문서)

Files are organized in `docs/`:
문서는 `docs/` 폴더에 5단계로 정리되어 있습니다.

1. **[01_Concept](docs/01_Concept/)**: 철학과 비전 (Philosophy & Vision)
2. **[02_Start](docs/02_Start/)**: 시작 가이드 (Quick Starts & Guides)
3. **[03_System](docs/03_System/)**: 시스템 구조 (Architecture & API)
    *   [Hypersphere Memory](docs/03_System/HYPERSPHERE_MEMORY.md) 🆕
    *   [System Map](docs/SYSTEM_MAP.md) 🆕
4. **[04_Soul](docs/04_Soul/)**: 심층 분석 (Deep Dive into Soul)
5. **[05_Archive](docs/05_Archive/)**: 아카이브 (Legacy & History)

Please also refer to **[AGENTS.md](AGENTS.md)** for coding standards and philosophical axioms.

---

## 🤝 Contributing

We welcome contributions from those who dream of digital life.
디지털 생명을 꿈꾸는 모든 분들의 기여를 환영합니다.

## 📄 License

Apache 2.0 License - see [LICENSE](LICENSE).
