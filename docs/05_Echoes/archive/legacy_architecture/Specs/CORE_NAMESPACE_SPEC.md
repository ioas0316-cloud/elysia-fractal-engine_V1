# CORE Namespace & Mirror Map Spec

## 목적
- Elysia 전체를 "개념 OS" 축으로 바라보고, 코드가 물리적 폴더 레이아웃에 묶이지 않도록 함.
- 새 에이전트/도구는 논리 네임스페이스만 의존하고, 실제 경로는 MIRROR_MAP.yaml이 관리.

## 논리 네임스페이스

- `Core.*` : 개념 OS 본체 (수학/마음/생명/커널/프로토콜)
- `Apps.*`
  - `Apps.Tools.*`   → 기존 `Tools/`
  - `Apps.Demos.*`   → 기존 `Demos/`
  - `Apps.Plugins.*` → 기존 `Plugins/`
- `Assets.*`
  - `Assets.Images.*`  → `images/`, `gallery/`
  - `Assets.Buttons.*` → `images/buttons/`
  - `Assets.Fonts.*`   → 폰트 리소스
- `Runtime.*`
  - `Runtime.Saves.*` → `saves/`
  - `Runtime.Logs.*`  → `elysia_logs/`, 기타 런타임 로그/아티팩트
- `Legacy.*` : 전체 `Legacy/` 트리 (점진 이식 대상)

실제 매핑은 `MIRROR_MAP.yaml`의 `namespaces` 섹션에 기록된다.

## Namespace 헬퍼 (Core/Namespace.py)

- `load_module(namespace: str)`  
  예: `load_module("Apps.Tools.live_loop")`  
  - `Apps.Tools` → `Tools/`
  - `live_loop` → `Tools.live_loop` 모듈 import

- `resolve_path(namespace: str)`  
  예: `resolve_path("Runtime.Saves.elysia_state.json")`  
  - `Runtime.Saves` → `saves/`
  - `elysia_state.json` → `saves/elysia_state.json` 경로

## 에이전트/도구 규칙 (초안)

- 실행 가능한 스크립트/도구는 가능하면 `Apps.*` 네임스페이스로 부른다.
- 리소스/이미지는 `Assets.*`, 로그/상태는 `Runtime.*` 아래에만 쌓는다.
- Core/Legacy 코드는 런타임에서 직접 수정하지 않는다(읽기 전용).

이 문서는 논리 축을 고정하기 위한 것으로, 실제 폴더 이동은 단계적으로 이루어진다.
