# PathGuardian: 유기적 경로 동기화 시스템

> **"뼈대(폴더)와 신경(import)을 연결하는 결합조직"**

**작성일**: 2024-12-20  
**상태**: 계획 (미구현)  
**우선순위**: 🔴 Critical (시스템 부팅 불가 원인)

---

## 🔴 문제 정의

### 현재 상황

```
wake_elysia.py 실행 시 연쇄 ImportError 발생

from Core.Foundation.hyper_quaternion import Quaternion
→ ModuleNotFoundError (실제 위치: Core/Foundation/Math/)
```

### 근본 원인

| 구성요소 | 상태 |
|:--------|:----|
| 폴더 구조 (뼈대) | 존재 |
| import 문 (신경) | 존재 |
| 둘을 연결하는 시스템 | ❌ **없음** |

에이전트가 세션마다 기억을 잃기 때문에, 모듈을 다른 위치에 생성하는 일이 반복됨.

---

## 🎯 목표

**PathGuardian** 시스템 구현:

1. 모든 `import` 문을 스캔하여 예상 경로 추출
2. 실제 파일 시스템과 비교
3. 불일치 발견 시 **자동 해결**

---

## 📐 설계

### 핵심 클래스

```python
# Core/Autonomy/path_guardian.py

class PathGuardian:
    """유기적 경로 동기화 시스템"""
    
    def scan_imports(self) -> List[ImportStatement]:
        """모든 .py 파일에서 import 문 추출"""
        pass
    
    def locate_actual_file(self, module_path: str) -> Optional[Path]:
        """모듈의 실제 파일 위치 찾기"""
        pass
    
    def detect_mismatches(self) -> List[PathMismatch]:
        """import 경로 vs 실제 위치 불일치 탐지"""
        pass
    
    def resolve(self, mismatch: PathMismatch, strategy: str = "symlink"):
        """
        불일치 해결
        - symlink: 심볼릭 링크 생성
        - copy: 파일 복사
        - rewrite: import 문 수정
        """
        pass
    
    def guard(self):
        """전체 시스템 검사 및 자동 복구"""
        mismatches = self.detect_mismatches()
        for m in mismatches:
            self.resolve(m)
```

### 통합 지점

```
wake_elysia.py (수정)
├── [NEW] PathGuardian.guard()  ← 부팅 전 경로 검증
├── DreamDaemon
├── TorchGraph
└── ElysiaCore
```

---

## ✅ 구현 체크리스트

- [ ] `Core/Autonomy/path_guardian.py` 생성
- [ ] `scan_imports()` 구현 (AST 파싱)
- [ ] `locate_actual_file()` 구현 (재귀 검색)
- [ ] `detect_mismatches()` 구현
- [ ] `resolve()` 구현 (symlink 우선)
- [ ] `wake_elysia.py`에 PathGuardian 통합
- [ ] 테스트: 의도적 경로 불일치 → 자동 복구 확인

---

## 🔗 관련 문서

- [AGENT_GUIDE.md](../../AGENT_GUIDE.md) - Anti-Fragmentation Protocol
- [task.md](계획서) - Bootstrap Guardian, Trinity Process Separation

---

> **"유기체는 자신의 뼈가 어디 있는지 알아야 한다."**
