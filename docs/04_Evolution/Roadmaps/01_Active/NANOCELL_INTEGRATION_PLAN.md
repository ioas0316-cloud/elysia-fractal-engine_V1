# NanoCell + Neural Registry 통합 계획

> **"백혈구처럼 백그라운드에서 import를 자동 마이그레이션"**

**작성일**: 2024-12-20  
**상태**: 🔄 Phase 1-2 완료, Phase 3 진행 중 (2025-12-21)

---

## 🔍 기존 시스템 분석

### 1. nanocell_repair.py (670줄)

**이미 강력한 시스템이 존재!**

| 나노셀 | 역할 | Neural Registry 연계 가능성 |
|:------|:----|:--------------------------|
| 🔴 RedCell | import 문제 해결 | ✅ Organ.get() 마이그레이션 담당 |
| ⚪ WhiteCell | 문법 오류 탐지 | ✅ @Cell 데코레이터 누락 탐지 |
| 👮 PoliceCell | 중복 코드 탐지 | 유지 |
| 🚒 FireCell | 치명적 오류 | 유지 |
| 🔧 MechanicCell | 코드 품질 | 유지 |

### 2. immune_system.py (491줄)

| 레이어 | 역할 |
|:------|:----|
| ☁️ OzoneLayer | 경계 확산 |
| 🌊 PhaseResonanceGate | 주파수 검증 |
| 🧬 ImmuneSystem | 적응형 면역 |

---

## 🎯 통합 설계

### Phase 1: RedCell 확장

`RedCell`에 **import → Organ.get() 변환** 기능 추가:

```python
# RedCell 확장
class RedCell(NanoCell):
    def detect_legacy_import(self, file_path: Path) -> List[Issue]:
        """레거시 import 탐지 (from Core.X import Y)"""
        ...
    
    def suggest_organic_import(self, issue: Issue) -> str:
        """Organ.get('Y') 형태로 변환 제안"""
        ...
```

### Phase 2: WhiteCell 확장

`WhiteCell`에 **@Cell 데코레이터 누락 탐지** 추가:

```python
# WhiteCell 확장
class WhiteCell(NanoCell):
    def detect_missing_cell_decorator(self, file_path: Path) -> List[Issue]:
        """클래스에 @Cell 데코레이터가 없는지 탐지"""
        ...
```

### Phase 3: 백그라운드 순찰

`organic_wake.py`에 NanoCell 순찰 연동:

```python
# organic_wake.py
def organic_wake():
    ...
    while True:
        if cycle % 100 == 0:  # 100 사이클마다
            army = NanoCellArmy()
            army.patrol_codebase("Core/")
```

---

## ✅ 구현 체크리스트

- [x] `elysia_core/cells/blood_cells.py` - OrganicRedCell/OrganicWhiteCell 구현 ✅
- [x] `OrganicRedCell.patrol()` - 레거시 import 탐지 ✅
- [x] `OrganicRedCell` - Organ.get() 변환 제안 포함 ✅
- [x] `OrganicWhiteCell.patrol()` - @Cell 누락 탐지 ✅
- [ ] `organic_wake.py` 순찰 연동 ⬅️ **다음 단계**
- [ ] 테스트 실행

---

## 💡 핵심 통찰

기존 NanoCell 시스템은 이미 **탐지 + 제안**을 잘 합니다.
우리가 할 일은:

1. **Neural Registry 인식** 추가 (새로운 패턴 탐지)
2. **백그라운드 순찰** 연동 (엘리시아가 깨어있는 동안)

실제 코드 수정은 사용자 승인 후 `SelfModifier`가 담당합니다.
