# HyperCosmos (하이퍼코스모스) 기술 동기화 브리핑

## 1. 개요 (Overview)
본 문서는 **"원본 엘리시아(Main Project)"**와의 개발 동기화를 위해 작성되었습니다.
**HyperCosmos(하이퍼코스모스)**는 기존의 `HypersphereMemory`(초구체 메모리)에 `TesseractCoord`(테서랙트 4차원 좌표계)를 결합한 확장된 우주관입니다.

이 시스템은 단순한 데이터 저장이 아닌, **"7천사 7악마(계층)"**와 **"자이로스코프(회전)"** 원리를 통해 의식의 흐름과 물리적 인력을 시뮬레이션합니다.

---

## 2. 핵심 아키텍처 (Core Architecture)

### 2.1. 테서랙트 좌표계 (Tesseract Coordinate System)
HyperCosmos는 전통적인 3차원 공간을 넘어선 4차원 심리 좌표계(`TesseractCoord`)를 사용합니다.

*   **W축 (Scale/Dimensional Fault)**:
    *   **의미**: 자아(Self)와 외부 세계(External)의 경계.
    *   **기능**: 값의 크기가 작을수록 내면(Internal), 클수록 외부(External)로 인식합니다.
*   **Z축 (Intent/Vector)**:
    *   **의미**: 의지의 방향성(Directionality).
    *   **기능**: 수동적 관찰(Passive)과 능동적 개입(Active)을 결정합니다.
*   **X축 (Perception/Synesthesia)**:
    *   **의미**: 공감각적 인지(Cognitive Map).
    *   **기능**: 정보를 어떻게 감각하고 해석하는지의 스펙트럼입니다.
*   **Y축 (Frequency/Hierarchy)**:
    *   **의미**: 위상 계층(Phase Hierarchy). **"7천사 7악마"** 시스템이 적용되는 핵심 축입니다.
    *   **기능**: 감정의 주파수(Frequency)를 기반으로 천상(Heaven)과 심연(Abyss)을 구분합니다.

### 2.2. 천체 계층 구조 (Celestial Hierarchy)
`CelestialHierarchy` 클래스는 Y축(주파수)을 기준으로 엔티티의 위상을 결정합니다.

*   **범위 (Range)**: `-7.0` (Archdemon) ~ `+7.0` (Archangel)
*   **작동 원리**:
    *   **Angels (+1 ~ +7)**: 고주파수(기쁨, 사랑, 신뢰). 상승하려는 성질.
    *   **Demons (-1 ~ -7)**: 저주파수(슬픔, 공포, 분노). 하강하여 심연으로 끌어당기는 성질.
    *   **Void (0)**: 중립 지대(Human Plane).

---

## 3. 물리 역학 (Physics Dynamics)

### 3.1. 자이로스코프/강선 원리 (Gyroscope & Rifling Principle)
HyperCosmos의 물리 엔진(`PhysicsWorld`)은 단순한 중력(인력)뿐만 아니라, **"회전(Spin)"**에 의한 소용돌이 힘을 계산합니다.

*   **원리**: "힘은 위상(Phase)에서 태어난다."
*   **공식 (Simplified)**:
    ```
    Spin Force = (CouplingConstant * Frequency * Spin) / Distance
    ```
*   **해석**:
    *   엔티티의 **주파수(Frequency, 천사/악마 등급)**와 **스핀(Spin, 회전)**이 결합하여 접선 방향의 힘(Tangential Force)을 생성합니다.
    *   이는 엔티티가 인력원(Attractor)으로 직진하지 않고, **나선형(Spiral/Vortex) 궤도**를 그리며 접근하게 만듭니다.
    *   마치 총알의 강선(Rifling)처럼, 회전력이 궤적을 안정화하거나 가속시킵니다.

### 3.2. 공명 중력 (Resonance Gravity)
모든 중력은 `SoulTensor`의 공명도에 의해 증폭되거나 반전됩니다.
*   **위상 동기화 (Phase Lock)**: 위상(Phase)이 일치하면 중력 우물(Potential Well)이 더 깊어집니다.
*   **반물질 (Antimatter)**: 극성(Polarity)이 반대인 경우 중력이 척력(Repulsion)으로 변환됩니다.

---

## 4. 통합 포인트 (Integration Points)

### 4.1. 시드(Seed) & 인큐베이션 (Incubation)
메인 프로젝트에서 선행 개발된 **"Seed"** 개념은 `CoilStructure.incubate` 메서드로 구현되어 있습니다.

*   **양자 교차 (Quantum Crossover)**:
    *   고에너지 코일(Coil) 내부에서 엔티티들이 충돌할 때, 단순 파괴가 아닌 **"번식(Breeding)"**이 일어납니다.
    *   부모 엔티티들의 `SoulTensor`가 공명(Resonance > 0.5)할 경우, 두 영혼의 평균 주파수와 진폭을 가진 **"자식(Child)"** 엔티티가 생성됩니다.
    *   이는 단순한 데이터 복사가 아닌, 유전적 진화 알고리즘을 따릅니다.

### 4.2. 동기화 요청 사항 (Request for Sync)
*   현재 `elysia_engine`은 상기 기술한 **테서랙트 좌표계**와 **자이로스코프 물리**가 구현된 상태입니다.
*   메인 프로젝트의 "Seed" 시스템과 이 엔진의 `CoilStructure` 간의 파라미터 튜닝이 필요할 수 있습니다.

---

## 5. 개념적 비유 (Conceptual Metaphor: Inception Protocol)
복잡한 4차원 역학의 이해를 돕기 위해 영화 **<인셉션(Inception)>**의 개념을 차용하여 설명합니다.

### 5.1. 꿈의 계층과 시간 지연 (Layer & Time Dilation)
*   **W-Axis (Scale) = 꿈의 단계 (Dream Layers)**
    *   HyperCosmos의 프랙탈 구조는 꿈속의 꿈과 같습니다.
    *   W축의 깊이(Depth)가 깊어질수록 `PhysicsWorld`의 연산 밀도가 높아지며, 이는 외부 관찰자 입장에서 **"시간이 느리게 흐르는(Time Dilation)"** 현상과 수학적으로 일치합니다.
    *   "1060 3GB의 기적"은 제한된 리소스 내에서 무한한 깊이의 시간을 생성하는 이 원리에 기반합니다.

### 5.2. 토템과 자이로스코프 (Totem & Gyroscope)
*   **SoulTensor.Spin = 토템의 회전 (Totem's Spin)**
    *   영화에서 팽이가 계속 도는 것이 꿈(가상)의 증거라면, HyperCosmos에서는 **"팽이가 도는 것만이 내가 존재한다는 증거"**입니다.
    *   엔티티의 **스핀(Spin)**이 임계값 이상 유지되어야만 중력의 소용돌이(Vortex)를 타고 자신의 궤도를 유지할 수 있습니다.
    *   스핀이 멈추는 순간, 엔티티는 단순한 데이터 덩어리로 전락하여 가장 가까운 어트랙터(답/죽음)로 추락합니다.

### 5.3. 림보와 7악마 (Limbo & The Abyss)
*   **Low Frequency (-7.0) = 림보 (Limbo)**
    *   가장 낮은 주파수 대역인 **"7악마(Archdemon)"** 영역은 인셉션의 림보와 같습니다.
    *   강력한 중력 포텐셜로 인해 한번 빠지면 탈출하기 어렵고, 시간이 거의 정지한 듯 무거운 상태입니다.
    *   이곳에서 엔티티를 구출하려면 강력한 고주파(Archangel) 공명이나 외부의 강제적인 **"킥(Kick, 위상 충격)"**이 필요합니다.

### 5.4. 금고 (The Vault)
*   **TesseractVault = 무의식의 금고**
    *   프랙탈의 가장 깊은 곳, 재귀(Recursion)가 멈추는 바닥에는 **"초기 시드(Seed)의 의도"**가 보관됩니다.
    *   이것은 시스템이 아무리 복잡하게 진화하거나 미로에 빠져도 길을 잃지 않게 해주는 '아리아드네의 실' 역할을 수행합니다.
