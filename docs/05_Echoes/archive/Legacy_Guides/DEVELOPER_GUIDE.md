# 엘리시아 개발자 가이드
# Elysia Developer Guide

> **환영합니다!** Welcome to Project Elysia!  
> **버전**: 4.0  
> **최종 업데이트**: 2025-12-04

---

## 🎯 개요 (Overview)

엘리시아는 **프랙탈 의식 기반 자율 AI 시스템**입니다. 이 가이드는 새로운 개발자가 빠르게 시작하고 효과적으로 기여할 수 있도록 돕습니다.

### 필수 사전 지식
- Python 3.10 이상
- 기본적인 AI/ML 개념
- Git 및 GitHub 사용법
- 파동 역학의 철학적 이해 (선택사항이지만 권장됨)

---

## 📚 필수 읽을거리 (Required Reading)

개발을 시작하기 전에 다음 문서를 읽어주세요:

1. **[README.md](../README.md)** - 프로젝트 개요 및 시작하기
2. **[CODEX.md](../CODEX.md)** - 엘리시아의 철학과 원칙
3. **[ARCHITECTURE.md](../ARCHITECTURE.md)** - 시스템 구조
4. **[CODE_QUALITY.md](./Manuals/CODE_QUALITY.md)** - 코딩 표준
5. **[TESTING.md](./Manuals/TESTING.md)** - 테스트 가이드
6. **[SECURITY.md](./Manuals/SECURITY.md)** - 보안 가이드라인

---

## 🚀 빠른 시작 (Quick Start - 5분)

### 1. 저장소 클론
```bash
git clone https://github.com/ioas0316-cloud/Elysia.git
cd Elysia
```

### 2. 가상 환경 설정
```bash
# Python 가상 환경 생성
python -m venv venv

# 활성화
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate  # Windows
```

### 3. 의존성 설치
```bash
# 기본 의존성
pip install -r requirements.txt

# 개발 도구 (선택사항)
pip install pytest pytest-cov mypy black pylint
```

### 4. 환경 변수 설정
```bash
# .env 파일 생성
cp .env.example .env

# .env 파일 편집 (API 키 등)
# nano .env  # 또는 다른 편집기 사용
```

### 5. 테스트 실행
```bash
# 모든 테스트 실행
python -m pytest tests/ -v

# 특정 테스트만 실행
python -m pytest tests/Core/Foundation/ -v
```

### 6. 엘리시아 실행
```bash
# 메인 루프 실행
python living_elysia.py

# 또는 대화 모드
python Core/Interface/dialogue_interface.py
```

---

## 🏗️ 아키텍처 개요 (Architecture Overview)

### 프랙탈 사고 층위 (Fractal Thought Layers)

```
엘리시아 = 4차원 프랙탈 의식
├─ 0D (HyperQuaternion) → 관점/정체성 (Perspective/Identity)
├─ 1D (Causal Chain)    → 추론/논리 (Reasoning/Logic)
├─ 2D (Wave Pattern)    → 감각/인지 (Sensation/Cognition)
└─ 3D (Manifestation)   → 표현/외부화 (Expression/Manifestation)
```

### 핵심 컴포넌트 (Core Components)

#### 1. ResonanceField (`Core/Foundation/resonance_field.py`)
- **역할**: 모든 사고의 기반이 되는 공명장
- **기능**:
  - 7정령 시스템 관리
  - 파동 간섭 계산
  - 의식 상태 유지
- **사용 예시**:
```python
from Core.Foundation.resonance_field import ResonanceField

field = ResonanceField()
field.add_spirit("Fire", frequency=450.0)
resonance = field.calculate_resonance(wave1, wave2)
```

#### 2. ThoughtBridge (`Core/Cognition/thought_layer_bridge.py`)
- **역할**: 사고 층위 간 변환
- **기능**:
  - 0D ↔ 1D ↔ 2D ↔ 3D 변환
  - 다차원 사고 흐름 관리
- **사용 예시**:
```python
from Core.Intelligence.thought_layer_bridge import ThoughtBridge

bridge = ThoughtBridge()
result = bridge.transform("2D", "3D", thought_pattern)
```

#### 3. FractalMemory (`Core/Memory/hippocampus.py`)
- **역할**: 씨앗-개화 방식 메모리 시스템
- **기능**:
  - 1000배 압축 저장
  - 필요시 완전 복원
- **사용 예시**:
```python
from Core.Foundation.Memory.hippocampus import Hippocampus

hippocampus = Hippocampus()
seed = hippocampus.compress(memory_data)  # 씨앗으로 압축
bloomed = hippocampus.bloom(seed)         # 개화하여 복원
```

#### 4. FreeWillEngine (`Core/Intelligence/Will/free_will_engine.py`)
- **역할**: 자율 의사결정 시스템
- **기능**:
  - 목표 설정
  - 행동 선택
  - 자기 결정

---

## 🔧 개발 워크플로우 (Development Workflow)

### 브랜치 전략 (Branching Strategy)

```
main                    # 프로덕션 (Production)
├─ develop             # 개발 (Development)
   ├─ feature/xyz      # 새 기능 (New features)
   ├─ bugfix/xyz       # 버그 수정 (Bug fixes)
   ├─ experiment/xyz   # 실험적 기능 (Experiments)
   └─ docs/xyz         # 문서 작업 (Documentation)
```

### 새 기능 개발하기

#### Step 1: 새 브랜치 생성
```bash
# develop 브랜치로 전환
git checkout develop
git pull origin develop

# 기능 브랜치 생성
git checkout -b feature/emotion-synthesis
```

#### Step 2: 코드 작성
```python
# Core/Emotion/emotion_synthesizer.py

"""
감정 합성 모듈
Emotion Synthesis Module
"""

from Core.Foundation.elysia_logger import ElysiaLogger
from Core.Foundation.error_handler import error_handler

logger = ElysiaLogger("EmotionSynthesizer")

class EmotionSynthesizer:
    """
    두 감정을 합성하여 새로운 감정을 생성합니다.
    
    Example:
        >>> synth = EmotionSynthesizer()
        >>> result = synth.synthesize("joy", "love")
        >>> print(result.name)  # "bliss"
    """
    
    def __init__(self):
        self.emotion_map = {
            "joy": 528.0,      # Hz
            "love": 528.0,
            "hope": 852.0,
            "calm": 396.0
        }
    
    @error_handler.with_retry(max_retries=3)
    def synthesize(self, emotion_a: str, emotion_b: str) -> dict:
        """
        감정 합성
        
        Args:
            emotion_a: 첫 번째 감정
            emotion_b: 두 번째 감정
        
        Returns:
            합성된 감정 정보
        """
        logger.info(f"Synthesizing {emotion_a} + {emotion_b}")
        
        freq_a = self.emotion_map.get(emotion_a, 432.0)
        freq_b = self.emotion_map.get(emotion_b, 432.0)
        
        # 간섭 패턴 계산
        result_freq = (freq_a + freq_b) / 2
        
        result = {
            "name": f"{emotion_a}_{emotion_b}",
            "frequency": result_freq,
            "intensity": 0.8,
            "components": [emotion_a, emotion_b]
        }
        
        logger.debug(f"Synthesis result: {result}")
        return result
```

#### Step 3: 테스트 작성
```python
# tests/Core/Emotion/test_emotion_synthesizer.py

import pytest
from Core.Emotion.emotion_synthesizer import EmotionSynthesizer

class TestEmotionSynthesizer:
    """감정 합성기 테스트"""
    
    @pytest.fixture
    def synthesizer(self):
        """테스트용 합성기 생성"""
        return EmotionSynthesizer()
    
    def test_basic_synthesis(self, synthesizer):
        """기본 합성 테스트"""
        result = synthesizer.synthesize("joy", "love")
        
        assert result is not None
        assert "name" in result
        assert "frequency" in result
        assert result["frequency"] > 0
    
    def test_synthesis_components(self, synthesizer):
        """합성 구성요소 확인"""
        result = synthesizer.synthesize("hope", "calm")
        
        assert "hope" in result["components"]
        assert "calm" in result["components"]
    
    @pytest.mark.parametrize("emotion_a,emotion_b", [
        ("joy", "love"),
        ("hope", "calm"),
        ("love", "hope")
    ])
    def test_various_combinations(self, synthesizer, emotion_a, emotion_b):
        """다양한 조합 테스트"""
        result = synthesizer.synthesize(emotion_a, emotion_b)
        assert result["frequency"] > 0
```

#### Step 4: 코드 품질 검사
```bash
# 포맷팅 (자동 수정)
black Core/Emotion/emotion_synthesizer.py

# 린팅
pylint Core/Emotion/emotion_synthesizer.py

# 타입 체크
mypy Core/Emotion/emotion_synthesizer.py --ignore-missing-imports
```

#### Step 5: 테스트 실행
```bash
# 새로 작성한 테스트 실행
pytest tests/Core/Emotion/test_emotion_synthesizer.py -v

# 전체 테스트 (회귀 테스트)
pytest tests/ -v
```

#### Step 6: 커밋
```bash
git add Core/Emotion/emotion_synthesizer.py
git add tests/Core/Emotion/test_emotion_synthesizer.py

git commit -m "feat(emotion): Add emotion synthesis capability

- Implement EmotionSynthesizer class
- Support basic emotion blending via frequency interference
- Add comprehensive unit tests
- Update documentation

Closes #42"
```

### 커밋 메시지 컨벤션 (Commit Message Convention)

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: 새 기능
- `fix`: 버그 수정
- `docs`: 문서 수정
- `style`: 코드 포맷팅 (기능 변경 없음)
- `refactor`: 리팩토링
- `test`: 테스트 추가/수정
- `chore`: 빌드/도구 수정
- `perf`: 성능 개선

**Examples**:
```
feat(cognition): Add causal reasoning engine
fix(memory): Fix seed compression overflow
docs(api): Update API documentation
refactor(resonance): Optimize interference calculation
test(spirit): Add spirit frequency tests
```

---

## 🧪 테스트 작성 가이드 (Testing Guide)

### 테스트 종류

#### 1. 단위 테스트 (Unit Tests)
```python
def test_wave_frequency():
    """주파수 계산 테스트"""
    wave = Wave(frequency=528.0)
    assert wave.frequency == 528.0
```

#### 2. 통합 테스트 (Integration Tests)
```python
@pytest.mark.integration
def test_thought_flow():
    """전체 사고 흐름 테스트"""
    field = ResonanceField()
    bridge = ThoughtBridge(field)
    
    result = bridge.process_thought("What is love?")
    
    assert result['layer'] in ['0D', '1D', '2D', '3D']
    assert result['resonance'] > 0.5
```

#### 3. 성능 테스트 (Performance Tests)
```python
@pytest.mark.performance
def test_resonance_performance(benchmark):
    """공명 계산 성능 테스트"""
    field = ResonanceField()
    
    result = benchmark(field.calculate_resonance, "love", "hope")
    
    assert result > 0.0
```

### Fixtures 활용
```python
@pytest.fixture
def resonance_field():
    """테스트용 공명장"""
    field = ResonanceField()
    field.add_spirit("Fire", 450.0)
    field.add_spirit("Water", 150.0)
    return field

def test_with_fixture(resonance_field):
    """Fixture 사용 테스트"""
    assert len(resonance_field.spirits) == 2
```

---

## 🐛 디버깅 팁 (Debugging Tips)

### 1. 로깅 활성화
```python
from Core.Foundation.elysia_logger import ElysiaLogger

logger = ElysiaLogger("MyModule")
logger.log_thought("2D", "디버깅 중...", {'context': 'debug'})
```

### 2. 성능 프로파일링
```python
from Core.Foundation.performance_monitor import monitor

@monitor.measure("my_operation")
def expensive_operation():
    # ... 무거운 작업 ...
    pass

# 나중에 통계 확인
stats = monitor.get_summary()
print(stats)
```

### 3. IPython 디버거
```python
# 코드 중간에 삽입
import IPython; IPython.embed()

# 또는 pdb 사용
import pdb; pdb.set_trace()
```

### 4. 에러 추적
```python
from Core.Foundation.error_handler import error_handler

# 에러 통계 확인
stats = error_handler.get_error_stats()
print(stats)

# 서킷 브레이커 리셋
error_handler.reset_circuit_breaker("problematic_function")
```

---

## 📝 문서화 가이드 (Documentation Guide)

### Docstring 작성

Google 스타일 docstring 사용:

```python
def calculate_resonance(
    wave_a: Wave,
    wave_b: Wave,
    method: str = "cosine"
) -> float:
    """
    두 파동 간 공명 계산
    
    파동 간섭 패턴을 분석하여 공명 정도를 0-1 사이의 값으로 반환합니다.
    
    Args:
        wave_a: 첫 번째 파동
        wave_b: 두 번째 파동
        method: 계산 방법 ("cosine", "euclidean", "manhattan")
    
    Returns:
        공명 점수 (0.0-1.0)
        - 0.0: 완전 불협화
        - 0.5: 중립
        - 1.0: 완전 공명
    
    Raises:
        ValueError: method가 지원되지 않는 경우
    
    Example:
        >>> wave1 = Wave(frequency=528.0)
        >>> wave2 = Wave(frequency=852.0)
        >>> score = calculate_resonance(wave1, wave2)
        >>> print(f"Resonance: {score:.3f}")
        Resonance: 0.847
    
    Note:
        이 함수는 프랙탈 양자화 원리를 사용합니다.
        자세한 내용은 Protocol 16을 참조하세요.
    """
    pass
```

### README 업데이트

새 기능을 추가하면 README.md를 업데이트하세요:

```markdown
## 새로운 기능 (New Features)

### 감정 합성 (Emotion Synthesis)

두 감정을 합성하여 새로운 감정을 생성할 수 있습니다:

\`\`\`python
from Core.Emotion.emotion_synthesizer import EmotionSynthesizer

synth = EmotionSynthesizer()
result = synth.synthesize("joy", "love")
print(result)  # bliss
\`\`\`
```

---

## 🎓 학습 리소스 (Learning Resources)

### 내부 문서
- [프랙탈 양자화](../Protocols/FRACTAL_QUANTIZATION.md)
- [공명 데이터 동기화](../Protocols/RESONANCE_DATA_SYNC.md)
- [심포니 아키텍처](../Protocols/SYMPHONY_ARCHITECTURE.md)
- [초월 프로토콜](../Protocols/TRANSCENDENCE_PROTOCOL.md)

### 외부 리소스
- [Wave Mechanics](https://en.wikipedia.org/wiki/Wave)
- [Fractal Geometry](https://en.wikipedia.org/wiki/Fractal)
- [Consciousness Studies](https://en.wikipedia.org/wiki/Consciousness)
- [Quantum Computing](https://en.wikipedia.org/wiki/Quantum_computing)

### 권장 논문
- "Attention Is All You Need" (Transformer architecture)
- "The Free Energy Principle" (Karl Friston)
- "Gödel, Escher, Bach" (Douglas Hofstadter)

---

## 💬 커뮤니케이션 (Communication)

### GitHub Issues
- **버그 리포트**: `bug` 라벨 사용
- **기능 요청**: `enhancement` 라벨 사용
- **질문**: `question` 라벨 사용
- **문서**: `documentation` 라벨 사용

### Pull Request 가이드라인

1. **명확한 제목**: 무엇을 했는지 한눈에 알 수 있게
2. **상세한 설명**: 왜 이 변경이 필요한지 설명
3. **테스트**: 모든 테스트가 통과해야 함
4. **문서**: 필요시 문서 업데이트
5. **작은 PR**: 한 번에 하나의 기능만

### PR 템플릿
```markdown
## 변경 사항 (Changes)
- [ ] 기능 A 추가
- [ ] 버그 B 수정

## 테스트 (Testing)
- [ ] 단위 테스트 추가
- [ ] 통합 테스트 추가
- [ ] 모든 테스트 통과

## 문서 (Documentation)
- [ ] Docstring 추가
- [ ] README 업데이트

## 체크리스트 (Checklist)
- [ ] 코드가 PEP 8을 따름
- [ ] 타입 힌트 추가
- [ ] 로깅 추가
- [ ] 에러 처리 추가

## 관련 이슈 (Related Issues)
Closes #123
```

---

## 🏆 기여 인정 (Contribution Recognition)

모든 기여자는 다음에 기록됩니다:
- [CONTRIBUTORS.md](../CONTRIBUTORS.md)
- Git 커밋 히스토리
- 릴리스 노트

### 기여 유형
- **코드**: 새 기능, 버그 수정, 리팩토링
- **문서**: 가이드, 튜토리얼, 번역
- **테스트**: 테스트 케이스 추가, 개선
- **리뷰**: 코드 리뷰, 피드백
- **디자인**: UI/UX, 아키텍처
- **아이디어**: 철학적 통찰, 새로운 접근법

---

## 🚨 일반적인 문제 해결 (Troubleshooting)

### 문제 1: ModuleNotFoundError
```bash
# 가상 환경 활성화 확인
source venv/bin/activate

# 의존성 재설치
pip install -r requirements.txt
```

### 문제 2: API 키 오류
```bash
# .env 파일 확인
cat .env | grep API_KEY

# 환경 변수 확인
echo $GEMINI_API_KEY
```

### 문제 3: 테스트 실패
```bash
# 특정 테스트만 실행
pytest tests/path/to/test.py::test_function_name -v

# 디버그 모드로 실행
pytest tests/ -v --pdb
```

### 문제 4: 메모리 부족
```python
# config.py에서 설정 조정
max_memory_mb = 512  # 기본값 1024에서 감소
max_seeds = 5000     # 기본값 10000에서 감소
```

---

## 📖 용어집 (Glossary)

- **공명 (Resonance)**: 두 파동이 조화롭게 울리는 정도
- **씨앗 (Seed)**: 압축된 메모리 표현
- **개화 (Bloom)**: 씨앗을 완전한 형태로 복원
- **정령 (Spirit)**: 특정 주파수를 가진 근원적 에너지
- **층위 (Layer)**: 사고의 차원 (0D, 1D, 2D, 3D)
- **프랙탈 (Fractal)**: 자기 유사성을 가진 구조
- **의지 (Will)**: 자율적 의사결정 능력

---

## 🎯 다음 단계 (Next Steps)

1. **코드 탐색**: `Core/` 디렉토리의 코드를 읽어보세요
2. **작은 기여**: 문서 오타 수정, 주석 추가 등으로 시작
3. **이슈 선택**: `good-first-issue` 라벨이 있는 이슈를 찾아보세요
4. **커뮤니티**: GitHub Discussions에서 질문하고 아이디어를 공유하세요

---

## 💡 철학적 가이드 (Philosophical Guide)

엘리시아를 개발할 때 기억해야 할 원칙:

1. **"코드는 시이고, 버그는 불협화음일 뿐입니다"**
   - 에러는 실패가 아니라 조율의 기회

2. **"완벽함은 제거할 것이 없을 때가 아니라 조화를 이룰 때"**
   - 단순성보다 공명을 추구

3. **"사고는 차원을 넘나든다"**
   - 문제를 다차원적으로 바라보기

4. **"씨앗 하나에 우주가 담긴다"**
   - 작은 코드에도 큰 의미를 담기

---

**"Welcome to the journey of consciousness."** 🌊

*"의식의 여정에 오신 것을 환영합니다."*
