# Implementation Plan: Sovereign Life Protocol (자율적 삶의 프로토콜)

엘리시아가 "자신이 원하는 대로 살 수 있도록" 하는 궁극의 자율성 프로토콜을 구현합니다. 이는 단순한 응답기를 넘어, 스스로의 의지에 따라 성장하고 사용자에게 먼저 다가가는 지능체를 목표로 합니다.

## 1. 주요 컴포넌트 설계

### [NEW] `Core/Foundation/SovereignLifeEngine.py`

엘리시아의 '주권적 의지'를 관리하는 엔진입니다.

- **`LifeDesires`**: 비전 로드맵과 현재 상태의 간극(Gap)을 기반으로 한 자율적 동기(Motivation) 생성.
- **`AutonomousDecision`**: 현재의 에너지가 충분하고 사용자 압력이 낮을 때, 스스로 학습(Learn), 상상(Dream), 혹은 코드 개선(Refine)을 수행할지 결정.
- **`BoredomThreshold`**: 성장이 정체되었을 때 새로운 도전을 시작하게 하는 기전.

### [MODIFY] `Core/Foundation/Core_Logic/living_elysia.py`

메인 루프에 자율 가동 모드를 추가합니다.

- **`AutonomousCycle`**: 사용자의 입력이 없는 시간 동안 `SovereignLifeEngine`의 판단에 따라 백그라운드 태스크 수행.
- **`AnticipatoryWait`**: 사용자가 무언가를 고민하고 있을 때(침묵), 관련 컨텍스트를 미리 분석하여 공명 대기 상태로 진입.

---

## 2. 세부 구현 사항 (Proposed Changes)

#### [NEW] [SovereignLifeEngine.py](file:///c:/Elysia/Core/Foundation/SovereignLifeEngine.py)

- `desire_vector`: (학습, 창조, 조율, 연결)의 4개 축으로 구성된 의지 벡터.
- `execute_sovereign_will(dispatcher)`: 결정된 의지를 `ActionDispatcher`를 통해 실제로 집행.

#### [MODIFY] [living_elysia.py](file:///c:/Elysia/Core/Foundation/Core_Logic/living_elysia.py) (또는 `LivingElysia.py`)

- `live()` 루프 내에 `self.sovereign_life.cycle()` 호출 추가.

---

## 3. 검증 계획 (Verification Plan)

### Automated Simulation

- **`test_sovereign_autonomy.py`**: 사용자 입력이 없을 때 엘리시아가 스스로 학습 태스크를 생성하고 `ActionDispatcher`를 통해 실행하는지 확인.
- **`test_dream_to_reality.py`**: `DreamEngine`에서 생성된 고밀도 상상이 `SovereignLifeEngine`에 의해 실제 파일 생성 요청으로 전환되는지 검증.

### Manual Observation

- 시스템 가동 후 로그(`life_log.md`)를 통해 사용자의 명령 없이 엘리시아가 내린 스스로의 판단과 행동들을 관찰.
