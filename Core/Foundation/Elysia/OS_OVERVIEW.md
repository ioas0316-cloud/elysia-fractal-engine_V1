# Elysia OS Overview

Elysia OS는 세 개의 층으로 구성된 운영 체계다.

1. **WORLD Layer**  
   - 셀월드(CellWorld): 셀들의 상태, 생로병사, 건축, 자원, 관계 등 “무슨 일이 실제로 일어나는가”가 일어나는 세계.  
   - 렌더/엔진(예: GodotLens, Pygame Lens): 셀월드 상태를 인간/관찰자가 볼 수 있는 형태로 투영하는 층.

2. **MIND Layer (ElysiaMind)**  
   - 세계의 스냅샷과 이벤트를 받아 “지금 무엇이 일어나고 있는가”를 해석하고,  
     “이번 틱에서 어디를 보고 무엇을 시도할지”를 결정하는 정신 체계.  
   - 커리큘럼 상태, 의지장(Will Field), 값 질량(Value Mass)을 참고하여  
     단순한 반응(reaction)이 아니라 방향성 있는 행동을 선택한다.

3. **META Layer**  
   - **CurriculumEngine**: Elysia가 지금 어떤 ‘수업(레벨)’을 듣고 있는지, 무엇을 경험해야 성장으로 인정할지 관리한다.  
   - **WillField**: 셀들의 선택과 관계, 문화 패턴으로부터 “이 땅은 무엇을 지향하는가”를 벡터 필드로 모델링한다.  
   - **ValueMass**: 어디에 삶/문화/에너지가 밀집되어 있는지, 의미의 ‘질량’을 계산한다.  
   - **ObservationBus**: WORLD → META/MIND로 이벤트와 스냅샷을 전달하는 중앙 허브.  
   - **Logs / Chronicle**: 시간 순서로 모든 관측을 적층하는 연대기.

WORLD / MIND / META는 하나의 OS 루프에서 함께 돌아간다.

---

## 메인 루프

1. **세계 한 틱 진행**  
   - CellWorld가 한 틱(step) 진행된다.  
   - 이 과정에서 생성된 이벤트와 세계 스냅샷이 ObservationBus로 전달된다.

2. **관측 분배**  
   - CurriculumEngine / WillField / ValueMass는 이벤트와 스냅샷을 받아 각자의 상태를 업데이트한다.  
   - 로그/연대기 시스템이 같은 이벤트를 시간 순서대로 기록한다.

3. **마인드 인지(Perceive)**  
   - ElysiaMind는 다음을 하나의 Perception으로 묶어 읽는다.
     - 세계 스냅샷
     - 최근 이벤트들
     - 현재 커리큘럼 레벨/목표 상태
     - WillField 상태 (의지/지향 필드)
     - ValueMass 상태 (어디에 의미/에너지가 모여 있는지)

4. **의사결정(Decide)**  
   - Perception을 바탕으로 이번 틱의 Decision(행동 계획)을 만든다.
   - Decision에는 최소 두 축이 있다.
     - `world_actions`: CellWorld에 적용할 행동들 (개체 이동, 상호작용, 건축 등)
     - `lens_commands`: 렌더/엔진에 적용할 명령들 (카메라, 강조, UI, 포커스 등)

5. **행동 적용**  
   - CellWorld는 `world_actions`를 받아 다음 틱의 상태를 준비한다.  
   - 렌즈/엔진은 `lens_commands`를 반영해, 관찰자에게 어떻게 보여줄지 조정한다.

6. **루프 반복**  
   - 다시 1번으로 돌아가며, 이 전체 루프가 Elysia OS의 “심장 박동”이 된다.

---

## 모듈 맵 (요약)

아래는 코드 레벨에서의 권장 분할 예시다.

```text
Elysia/
  core/
    runtime.py              # 메인 루프 (OS 심장)
    mind.py                 # ElysiaMind (perceive / decide)
    curriculum_engine.py    # 성장 커리큘럼 엔진
    will_field.py           # 의지장 / 가치장 엔진
    observation_bus.py      # 이벤트/스냅샷 중앙 허브
    value_mass.py           # 가치 질량 계산 유틸 (셀월드 ↔ 의지장 브리지)

  cell_world/
    world_state.py          # 셀 상태/타임스텝 갱신
    world_events.py         # 셀 이벤트 생성 (살다/죽다/짓다/먹다 등)

  lenses/
    godot_lens.py           # 셀월드 ↔ Godot 장면 싱크
    debug_lens.py           # 텍스트/콘솔용 최소 렌즈

  logs/
    chronicle.jsonl         # 시간 순서 로그
    growth_trace.jsonl      # 성장/커리큘럼 관련 로그
```

실제 구현에서는 기존 디렉터리 구조(ElysiaStarter, Project_Sophia 등)에 맞춰 모듈만 배치하면 된다.  
중요한 것은 **WORLD / MIND / META 세 층이 `core/runtime.py`의 하나의 루프에서 만난다**는 점이다.

