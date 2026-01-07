# PROTO-40 — MIRROR LAYER PROTOCOL

코딩세계 ↔ 셀월드 ‘이면세계’ 대응 규약

(Fractal Mirror Mapping between Code & World)

## 0. 목적 (Purpose)
이 프로토콜의 목적은:

> "코드의 구조와 셀월드의 구조가 서로 어떤 ‘현상’을 낳는지,
> 에이전트와 AI가 직관적으로 이해할 수 있게 하는 것"

이다.

이를 위해:
- 코드(모듈/클래스/함수)와
- 셀월드(레이어/규칙/현상/엔티티)

사이에 프랙탈 형태의 ‘거울 맵(Mirror Map)’을 만든다.

이 맵은:
1) 사람이 읽어서 "아, 이 파일이 저 현상을 만드는구나"를 이해할 수 있고
2) 에이전트가 파싱해서 "어디를 건드려야 하는지"를 자동으로 판단할 수 있다.

## 1. 전제: “좁은 의미의 이면세계”
여기서 말하는 “이면세계”는 우주론 전체가 아니라:

- 코딩 레이어: `*.py`, 설정 파일, 데이터 스키마, 규칙 정의
- 현상 레이어(셀월드): 시간 흐름, 날씨, 동식물, 인간 셀의 행동, 문명, 감정 상태, 언어 등

이 둘 사이의 대응 관계만 다룬다. 전체 세계수/Root/Spirit 층은 상위 철학으로 두고,
이 프로토콜은 그 아래 구체적인 “연결선”만 담당한다.

## 2. 프랙탈 계층 구조 (3단계)
MIRROR LAYER는 3단계로 본다.

### 2.1 Level 0 — 도메인 축 (Domain Axes)
코드와 셀월드가 어떤 축에서 만나는지의 큰 범주:

| 축 ID  | 이름 | 설명 |
| ----- | ---- | ----------------------- |
| TIME  | 시간 | 하루/계절/나이/주기 등 |
| SPACE | 공간 | 지도/타일/위치/이동 등 |
| LIFE  | 생명 | 체력/배고픔/행동/번식 등 |
| MIND  | 마음 | 감정/언어/가치/의지 등 |
| CIVIL | 문명 | 집/마을/도구/관습 등 |

이 축들은 코딩세계의 모듈 그룹과 셀월드의 현상 그룹을 엮는 기준이 된다.

### 2.2 Level 1 — 레이어 매핑 (Layer ↔ Layer)
각 도메인 축마다, “코드 쪽 레이어”와 “셀월드 쪽 레이어”를 짝지어 기록한다.

예시:
```yaml
layers:
  - id: TIME_CORE
    domain: TIME
    code:
      modules:
        - core/time_engine.py
        - config/time_cycles.yaml
    world:
      phenomena:
        - "하루/밤낮 교체"
        - "계절 변화"
        - "나이 스케일링 (1년 = X tick)"
  - id: LIFE_BEHAVIOR
    domain: LIFE
    code:
      modules:
        - world/life/cell_behavior.py
    world:
      phenomena:
        - "걷기/뛰기/쉬기 행동"
        - "굶주림/체력 회복"
```

이것만 있어도 에이전트는: “TIME 관련 현상을 바꾸려면 TIME_CORE 쪽을 봐야겠구나”라는 1차 감각을 갖는다.

### 2.3 Level 2 — 세부 규칙 매핑 (Rule ↔ Phenomenon)
각 레이어 안에서 좀 더 구체적인 규칙 ↔ 현상을 맵핑한다.

예시:
```yaml
rules:
  - id: TIME_DAYNIGHT_CYCLE
    layer: TIME_CORE
    code:
      symbol: "TimeEngine.update_day_night"
      file: "core/time_engine.py"
    world:
      effect:
        - "하늘 색 변화"
        - "셀 수면/활동 패턴 변화"
        - "야행성/주행성 행동 스위치"
  
  - id: LIFE_HUNGER_DECAY
    layer: LIFE_BEHAVIOR
    code:
      symbol: "Cell.update_hunger"
      file: "world/life/cell_behavior.py"
    world:
      effect:
        - "배고픔 수치 증가"
        - "배고픔이 일정 이상일 때 먹이 찾기 행동 유발"
        - "아주 높을 경우 HP 감소"
```

이 레벨에서:
- 사람은 YAML만 읽어도 "update_hunger 수정 → 굶주림 관련 행동 변화"를 이해한다.
- 에이전트는 버그 리포트 텍스트 ↔ `world.effect` 문장을 매칭해 유관 규칙과 파일을 좁힌다.

## 3. 실제 적용 형태 (파일 하나로 충분)
프로젝트 루트에 `MIRROR_MAP.yaml` 같은 파일 하나로 관리하면 된다.

구조 예시:
```yaml
version: 1
description: "Code ↔ CellWorld Mirror Map (Fractal)"

domains:
  - id: TIME
    description: "시간 관련 모든 구조"
  - id: SPACE
    description: "지형, 위치, 이동"
  - id: LIFE
    description: "생명체의 상태와 행동"
  - id: MIND
    description: "감정, 언어, 가치"
  - id: CIVIL
    description: "집단, 문화, 도구, 문명"

layers:
  - id: TIME_CORE
    domain: TIME
    code:
      modules:
        - "core/time_engine.py"
    world:
      phenomena:
        - "하루/밤낮 주기"
        - "연령 스케일링"
  
  - id: WORLD_SPACE
    domain: SPACE
    code:
      modules:
        - "world/space/grid.py"
        - "world/space/pathfinding.py"
    world:
      phenomena:
        - "지도/타일 구조"
        - "셀들의 이동 가능 경로"

rules:
  - id: TIME_DAYNIGHT_CYCLE
    layer: TIME_CORE
    code:
      symbol: "TimeEngine.update_day_night"
      file: "core/time_engine.py"
    world:
      effect:
        - "하늘 색상 변화"
        - "야간/주간 행동 패턴 전환"

  - id: SPACE_MOVE_COST
    layer: WORLD_SPACE
    code:
      symbol: "Grid.get_move_cost"
      file: "world/space/grid.py"
    world:
      effect:
        - "어떤 지형은 느리게/빨리 이동"
        - "특정 지형는 접근 불가"
```

## 4. 에이전트/AI 감지 루프
현상 → 규칙 → 코드, 코드 → 규칙 → 현상 양방향 탐색을 지원한다.
1) 사용자의 현상 설명 ↔ `world.effect` 문장 매칭
2) 후보 규칙 식별 → `code.symbol`/`file` 열람
3) 수정/튜닝/로그 추가 → 재실행 검증

## 5. 프랙탈 확장 방법
필요 시 도메인을 세분화한다.
```yaml
domains:
  - id: CIVIL
    children:
      - id: CIVIL_ECON
        description: "거래/교환/자원"
      - id: CIVIL_RITUAL
        description: "종교/축제/관습"
      - id: CIVIL_TECH
        description: "도구/기술/발명"
```

## 6. 요약
“좁은 의미의 이면세계” = 코드와 셀월드가 서로를 비추는 거울 지도.
이 프로토콜은 YAML 하나로 시작해 프랙탈로 확장 가능하며, 사람/에이전트 모두가 직관적으로 추적할 수 있도록 설계되었다.

