# Neural Registry: 유기적 임포트 시스템

> **"위치(Path)가 아니라 의미(Identity)로 연결되는 세상"**

**작성일**: 2024-12-20  
**상태**: ✅ Phase 1 완료 (2025-12-21)  
**우선순위**: 🔴 Critical (시스템 부팅 불가 원인의 근본 해결)

---

## 💡 핵심 통찰

### 기존 방식의 본질적 한계

```python
# 주소 기반 연결 (Address-based)
from Core.Foundation.Memory.hippocampus import Hippocampus
```

이것은 친구를 부를 때 **"서울시 강남구 XX동 XX호에 사는 사람아!"**라고 부르는 것과 같다.
친구가 이사를 가면(파일 이동), "그런 사람 없는데요?" 하고 에러가 뜨며 관계가 끊어진다.

### 유기적 방식

```python
# 의미 기반 연결 (Identity-based)
from elysia_core import Cell, Organ

@Cell("Memory")
class Hippocampus:
    pass

# 사용할 때
memory = Organ.get("Memory")  # 어디에 있든 찾아냄
```

이것은 **"엘리시아!"**라고 이름을 부르는 것과 같다.
그녀가 서울에 있든 미국에 있든, 이름만 부르면 연결된다.

---

## 🏗️ 설계: 신경망 레지스트리

### 1. 원리: "나는 누구인가"만 선언한다 (Self-Declaration)

각 모듈은 **데코레이터**로 자신의 정체성만 선언한다.

```python
# Core/Foundation/Memory/hippocampus.py (어디에 있든 상관없음)

from elysia_core import Cell

@Cell("Memory")
class Hippocampus:
    """기억 세포"""
    pass

@Cell("Memory.ShortTerm")
class WorkingMemory:
    """단기 기억"""
    pass
```

### 2. 작동: "어디에 있든, 내가 찾아낼게" (Dynamic Scanning)

프로그램 시작 시, 스캐너가 전체 프로젝트를 훑어 **동적 지도**를 생성한다.

```python
# elysia_core/scanner.py

class NeuralScanner:
    def __init__(self, root_path: str):
        self.registry = {}  # {"Memory": <class Hippocampus>, ...}
    
    def scan(self):
        """모든 .py 파일을 순회하며 @Cell 데코레이터 탐지"""
        for py_file in self._find_all_python_files():
            module = self._import_module(py_file)
            for obj in self._get_decorated_objects(module):
                identity = obj._cell_identity
                self.registry[identity] = obj
                print(f"🧬 Cell registered: {identity} at {py_file}")
```

### 3. 연결: "필요한 것을 말해, 내가 이어줄게" (Dependency Injection)

```python
# elysia_core/organ.py

class Organ:
    _scanner = None
    
    @classmethod
    def initialize(cls, root_path: str):
        cls._scanner = NeuralScanner(root_path)
        cls._scanner.scan()
    
    @classmethod
    def get(cls, identity: str):
        """정체성(이름)으로 세포를 찾아 연결"""
        if identity not in cls._scanner.registry:
            raise CellNotFoundError(f"'{identity}' 세포를 찾을 수 없습니다.")
        return cls._scanner.registry[identity]()
```

---

## 📁 파일 구조

```
c:/Elysia/
├── elysia_core/           # 🆕 핵심 장기
│   ├── __init__.py
│   ├── cell.py            # @Cell 데코레이터
│   ├── organ.py           # Organ.get() 인터페이스
│   ├── scanner.py         # NeuralScanner
│   └── exceptions.py      # CellNotFoundError 등
│
├── Core/                  # 기존 코드 (리팩토링 대상)
│   ├── Foundation/
│   │   ├── Memory/
│   │   │   └── hippocampus.py  # @Cell("Memory") 추가
│   │   └── ...
│   └── ...
│
└── wake_elysia.py         # Organ.initialize() 호출
```

---

## ✅ 구현 체크리스트

### Phase 1: 핵심 인프라 ✅ 완료

- [x] `elysia_core/cell.py` - @Cell 데코레이터 구현 ✅
- [x] `elysia_core/organ.py` - Organ.get() 구현 ✅
- [x] `elysia_core/scanner.py` - NeuralScanner 구현 ✅

### Phase 2: 부팅 통합

- [ ] `wake_elysia.py` 수정 - `Organ.initialize("c:/Elysia")` 추가
- [ ] 기존 GlobalHub와 통합 검토

### Phase 3: 마이그레이션

- [ ] 핵심 모듈에 @Cell 데코레이터 추가
- [ ] 기존 import 문을 Organ.get()으로 점진적 교체

---

## 💎 장점

| 기존 방식 | Neural Registry |
|:---------|:----------------|
| 파일 이동 시 import 수정 필요 | ✅ 수정 불필요 |
| 에이전트가 기억 못함 | ✅ 자동 스캔으로 항상 최신 |
| 주소 기반 (딱딱함) | ✅ 의미 기반 (유기적) |
| 모듈 교체 시 전체 수정 | ✅ 이름표만 바꾸면 됨 |

---

## 🔗 기존 시스템과의 관계

- **GlobalHub**: 현재 수동 등록 → Neural Registry로 자동화
- **PathGuardian (폐기)**: 주소 수정 시도 → 근본적으로 주소 제거
- **wave coding**: 코드 품질 분석 → 그대로 유지

---

> **"이것은 기계 조립이 아니라, 혈관이 연결되는 것이다.  
> 어디에 붙어있든, 피(데이터)는 흐르게 된다."**
