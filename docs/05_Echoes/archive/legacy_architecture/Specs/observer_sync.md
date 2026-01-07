## 고도 엔진 관측 동기화 안내 (엘리시아 + 월드)

### 목적
Godot 화면에서 다음 세 가지를 함께 보여줍니다:

- **엘리시아의 내면** (얼굴, 생각, 집중된 영역, 메타 관측)
- **월드 뷰** (셀/필터/오버레이)
- 이 둘의 **관계** (엘리시아가 어떤 세계 요소를 바라보는지, 렌즈가 어떻게 이동하는지, 시선이 어디에 머무는지)

### 핵심 개념

1. **정렬된 프레임**
   - 이미 브리지는 같은 틱에 `frame["elysia"]`와 `frame["world"]`를 함께 보냅니다.
   - 이 둘을 하나의 “관측 프레임”으로 보고, 화면을 나란히 두거나 연결선을 만들어 동시에 렌더링합니다.
   - `focus_area`, `thought_trail`, `meta_observation`을 그대로 써서 왜 그 지점을 보는지 설명합니다.

2. **Lens(렌즈) 인터페이스**
   - UI에 쿼터니언 축을 반영한 렌즈 패널을 추가합니다.
     * 셀이나 구역을 클릭하면 `{type:"input", input_type:"vision", description:"...", palette:[...], brightness:...}` 같은 vision 입력을 만들어 전송하고, 렌즈가 그쪽으로 미세하게 이동하게 합니다.
     * `anchor_strength`가 낮으면 전체 월드(배경/오버레이)를 부드럽게 강조하여 “아직 큰 우주의 일부”임을 느끼게 합니다.

3. **빛줄 연결**
   - 선택한 셀과 엘리시아 초상 사이에 시각적 연결(색 그라디언트, 빛줄기)을 그려 `focus_area`가 그 셀과 연관됨을 표시합니다.
   - `meta_observation`이 “신의 눈”이라면 WorldView에 bloom/광선 효과를, “작은 점 집중”이라면 초상에 미묘한 떨림/빛 효과를 줍니다.

### 구현 참고

1. **Godot UI 변경**
   - SplitContainer 또는 StackContainer로 “Inner Lens”/“Outer World” 패널을 동시에 보여줍니다.
   - “Lens Input”(vision/description)을 넣을 텍스트 필드와 버튼을 마련해 직접 descriptive vision을 보낼 수 있게 합니다.
   - `focus_area`/`meta_observation`이 업데이트될 때 주변 광원이나 오버레이 색을 애니메이션으로 바꿔 관측감을 강조합니다.
   - 웹소켓을 쓰지 않으려면 `Project_Elysia/high_engine/godot_integration.py`를 직접 호출하여 `next_frame()`/`process_input()`을 쓰면 됩니다.

2. **브리지/통합**
   - 현재 브리지는 vision/chat 입력을 전달하고, 동일 타임스탬프/무드로 묶인 프레임을 유지합니다.
   - 셀 클릭 시 `source_focus_cell` 같은 태그를 추가하면 UI에서 그 셀만 강조하기 수월합니다.

3. **로그/문서**
   - 이 문서는 Godot 디자이너나 UI 개발자가 “어떤 레이아웃을 만들어야 하는지” 참고할 수 있는 기준입니다.
   - `Core/CODEX.md`의 관측 프로토콜 또는 프랙탈 원칙 섹션에 이 흐름을 언급하여 문서와 UI가 일치하도록 합니다.

4. **실행 접근**
   - `scripts/godot_integration_run.py`를 실행하면 UI 없이 CLI에서도 동일한 흐름을 체험할 수 있으므로 “시각화 전 테스트”용으로 활용 가능합니다.

이 안내를 기반으로 Godot 씬을 구성하면, “엘리시아와 세계가 함께 관측되는” 하나의 통합 화면을 만들 수 있습니다.
