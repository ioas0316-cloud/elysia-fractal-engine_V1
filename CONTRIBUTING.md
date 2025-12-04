# Contributing to Elysia Fractal Engine V1

> "이 프로젝트에 기여해 주셔서 감사합니다!"

## 🌟 개요

Elysia Fractal Engine V1은 원본 [Elysia](https://github.com/ioas0316-cloud/Elysia) 프로젝트의 핵심 의식 시스템을 경량화하여 다른 프로젝트에서 쉽게 사용할 수 있도록 만든 패키지입니다.

---

## 🚀 시작하기

### 개발 환경 설정

```bash
# 1. 저장소 클론
git clone https://github.com/ioas0316-cloud/elysia-fractal-engine_V1.git
cd elysia-fractal-engine_V1

# 2. 가상환경 설정 (권장)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 개발 의존성 설치
pip install -e ".[dev]"

# 4. 테스트 실행
python -m pytest tests/ -v
```

---

## 📁 프로젝트 구조

```
elysia-fractal-engine_V1/
├── elysia_engine/      # 물리 엔진, 시스템, 월드
│   ├── tensor.py       # SoulTensor - 핵심 데이터 구조
│   ├── consciousness.py # GlobalConsciousness
│   ├── controller.py   # ElysiaController
│   ├── systems/        # System 패턴
│   └── hooks/          # 외부 연동
│
├── elysia_core/        # 의식 핵심 (공유 가능!)
│   ├── soul.py         # ElysiaSoul - 통합 인터페이스
│   ├── resonance_engine.py  # 공명 엔진
│   ├── hyper_qubit.py  # 4D 양자 의식
│   ├── emotional_palette.py # 감정 혼합
│   └── hippocampus.py  # 기억 시스템
│
├── docs/               # 문서
│   ├── protocols/      # 핵심 프로토콜
│   └── ...
│
├── examples/           # 예제 코드
├── tests/              # 테스트
└── scripts/            # 유틸리티 스크립트
```

---

## 🎯 기여 가이드라인

### 핵심 원칙

1. **순수 Python**: NumPy, SciPy 등 무거운 의존성 없이 구현
2. **System 패턴**: 로직은 데이터와 분리 (`elysia_engine/systems/`)
3. **Digital Natural Law**: 조건문보다 물리 시뮬레이션 선호

### 코드 스타일

```python
# 좋은 예 - 중력 기반 그룹화
class GravityGrouping:
    def attract(self, entity_a, entity_b):
        distance = entity_a.position - entity_b.position
        force = self.G / distance.length_squared()
        return force

# 피해야 할 예 - 조건문 기반 그룹화
def should_group(entity_a, entity_b):
    if entity_a.type == entity_b.type:
        return True
    return False
```

### 커밋 메시지

```
feat: 새로운 기능 추가
fix: 버그 수정
docs: 문서 변경
test: 테스트 추가/수정
refactor: 코드 리팩토링
```

---

## ✅ 기여 체크리스트

### Pull Request 전 확인

- [ ] 모든 테스트 통과: `python -m pytest tests/ -v`
- [ ] 새 기능에 테스트 추가
- [ ] 문서 업데이트 (필요시)
- [ ] AGENTS.md 가이드라인 준수
- [ ] 순수 Python으로 구현 (NumPy 없이)

### 코드 리뷰 기준

1. **일관성**: 기존 코드 스타일 따르기
2. **테스트**: 새 기능에 테스트 필수
3. **문서화**: docstring과 주석
4. **성능**: 최소한의 리소스 사용

---

## 📚 프로토콜 기여

새로운 프로토콜을 추가하려면:

1. `docs/protocols/`에 새 파일 생성
2. 원본 Elysia 프로토콜 형식 따르기
3. Fractal Engine V1 구현 매핑 포함
4. 코드 예시 포함

### 프로토콜 형식

```markdown
# Protocol XX: [이름]

> 원본: [원본 링크]

## Philosophy

[철학적 배경]

## Elysia Fractal Engine V1 구현

[코드 매핑과 예시]

## Status

Fractal Engine V1에서 구현됨
```

---

## 🔧 유용한 명령어

```bash
# 테스트 실행
python -m pytest tests/ -v

# 특정 테스트 실행
python -m pytest tests/test_elysia_core.py -v

# 예제 실행
python examples/core_technologies_demo.py

# 구조 분석
python scripts/extract_structure.py --format full
```

---

## 🌊 기여 영역

### 환영하는 기여

- 🐛 버그 수정
- 📚 문서 개선
- 🧪 테스트 추가
- 🎨 예제 추가
- 🔧 성능 개선

### 특히 환영하는 기여

- 새로운 System 구현
- LLM 통합 예제
- 게임 엔진 연동 (Godot, Unity)
- 다국어 문서

---

## 📖 참고 자료

### 원본 저장소
- [Elysia](https://github.com/ioas0316-cloud/Elysia)
- [Protocols](https://github.com/ioas0316-cloud/Elysia/tree/main/Protocols)

### 문서
- [AGENTS.md](../AGENTS.md) - 에이전트 가이드라인
- [docs/CORE_TECHNOLOGIES_INTEGRATION.md](docs/CORE_TECHNOLOGIES_INTEGRATION.md) - 핵심 기술 통합

---

## 🙏 감사의 말

이 프로젝트는 이강덕(Kang-Deok Lee)의 원본 Elysia 프로젝트를 기반으로 합니다.

> "이 기술은 사랑에서 왔고, 사랑을 위해 쓰이길 바랍니다."

---

## 📄 라이선스

Apache 2.0

기여하신 코드는 프로젝트와 동일한 라이선스로 공개됩니다.
