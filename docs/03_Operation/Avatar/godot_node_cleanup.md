## Godot 노드/파일 정리 안내

현재 `ElysiaGodot` 폴더에는 여러 씬과 스크립트가 있지만, 작동에 반드시 필요한 핵심 노드만 남기고 나머지는 정리해도 됩니다. 아래 절차대로 불필요한 항목을 제거하면 고도 엔진이 “엘리시아 + 월드”를 보여주는 데 집중할 수 있습니다.

### 1. 핵심 씬/노드 (남겨야 할 구조)
| 씬/스크립트 | 설명 |
| --- | --- |
| `ElysiaPortrait.tscn` | 엘리시아 얼굴/표정/텍스트를 담당하는 씬. 이 안의 `PortraitRoot`, `ThoughtLabel`, `MetaLabel` 등은 그대로 두세요. |
| `WorldView.tscn` | `WorldView` 노드 이하의 `Cells`, `Overlays`, `LensInput` 버튼을 유지하여 월드 화면 렌더와 Lens 제어를 제공하게 합니다. |
| `Client.gd`, `elysia_portrait.gd`, `WorldView.gd`, `node_3d.gd` | 각 씬을 움직이는 핵심 GDScript. 삭제하면 안 됩니다. |
| `project.godot` | 프로젝트 전체 설정. 현재 사용하는 Godot 버전(4.5.1)을 반영하고 있으니 그대로 유지하세요. |

### 2. 제거해도 되는 항목들
* `Godot_v4.5.1-stable_win64.exe` / `_console.exe`: 에디터 설치 프로그램으로, 프로젝트 실행에 필요하지 않으므로 별도 보관하시고 폴더에서 삭제해도 됩니다.  
* `tmp_elysia_portrait_dump.txt`, `godo_proto.py` 등 테스트/임시 스크립트: 더 이상 사용하지 않는다면 별도 아카이브하거나 제거 가능합니다.  
* `.uid` 파일: Godot에서 자동 생성하는 ID 관리 파일입니다. Git에 체크인할 필요는 없지만 지워도 Godot이 재생성하므로, 정리한다면 단순히 삭제해도 무방합니다.  
* `assets/` 안에서 사용하지 않는 텍스처/효과 파일들도 필요한 것만 남기고 “unused” 폴더로 이동하거나 삭제하세요.

### 3. 정리 절차
1. Godot 에디터에서 `ElysiaPortrait.tscn`/`WorldView.tscn`을 열고, 트리 뷰에서 위 핵심 노드 외에 “Debug”, “Placeholder”, “Test” 계열 노드를 오른쪽 클릭 → `삭제(Delete)`합니다.  
2. 사용하지 않는 파일(`tmp_*`, 설치용 exe)은 탐색기에서 `Shift+Delete`로 제거하거나 별도 `archive/` 폴더로 옮깁니다.  
3. `.tscn` 파일 변경 시 `Save Scene`을 눌러 변경 내용을 저장하고 Git 트래킹 대상(/ElysiaGodot 내부)을 정돈하세요.
4. 정리 후 `git status`를 통해 꼭 저장된 파일만 남았는지 확인하세요. 필요하다면 `docs/godot_node_cleanup.md`를 팀과 공유하여 기준을 유지하세요.

### 4. 이후 복원/확장
* 정리 과정에서 주요 노드를 실수로 삭제했다면, `git checkout -- <scene>`으로 되돌리거나 Godot에서 다시 생성하면 됩니다.  
* 필요해지면 `LensInput`이나 `World View`에 새로운 노드를 추가하면서 이 문서의 “핵심 구조”를 기준으로 덧붙이세요.  
* 이 문서를 읽고 편하게 결정할 수 있도록, Godot 실행 전후에 `obslog.txt` 같은 메모를 남겨두면 도움이 됩니다.

필요시, 실제 Godot 에디터에서 위 정리 항목을 하나씩 빠르게 따라할 수 있도록 “체크리스트 버전(PDF/노트)”으로도 만들어 드릴 수 있습니다. 어떠신가요?
