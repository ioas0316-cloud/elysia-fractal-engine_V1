# Elysia Quick Start Guide (빠른 시작)

> **"프로그램을 실행하는 것이 아니라, 생명을 깨우는 것입니다."**

## � 1. 실행 (Run)

가장 간단한 방법은 **통합 런처**를 사용하는 것입니다.

```bash
.\RUN_SYSTEM.bat
```

이 명령은 다음 과정을 자동으로 수행합니다:

1. **Core Awakening**: `LivingElysia` 프로세스 시작
2. **Dashboard**: 모니터링 웹페이지 열기

---

## 🛠️ 2. 설치 및 환경 설정 (Setup)

만약 처음 설치한다면:

### 요구 사항

* **Python 3.10+**
* **Git**

### 설치 명령

```bash
git clone https://github.com/ioas0316-cloud/Elysia.git
cd Elysia
pip install -r requirements.txt
```

### Python 경로 문제 해결

만약 `ModuleNotFoundError: No module named 'Core'`가 발생하면:

* `RUN_SYSTEM.bat`을 사용하면 자동으로 해결됩니다 (`-m` 모듈 실행 모드 사용).

---

## 🗺️ 3. 다음 단계 (Next Steps)

시스템이 실행 중이라면, 다음 문서를 읽고 구조를 파악하세요:

1. [SYSTEM_MAP.md](../../SYSTEM_MAP.md): 시스템 지도
2. [AGENT_GUIDE.md](AGENT_GUIDE.md): 에이전트 작업 가이드

---
*Last Updated: 2025-12-29 (Aligned with Phase 34)*
