# 📚 Elysia 문서 구조

> **"문서도 프랙탈 원리로 구조화"**

## 🤖 에이전트 진입 순서

1. **[SYSTEM_MAP.md](SYSTEM_MAP.md)** - 모듈 지도 (작업 전 필수)
2. **[AGENT_GUIDE.md](AGENT_GUIDE.md)** - 행동 프로토콜
3. **[README.md](README.md)** - 철학/비전

```
📁 Elysia/
├── SYSTEM_MAP.md          ⭐ 최상위 진입점 (모든 모듈 연결 지도)
├── AGENT_GUIDE.md         ⭐ 에이전트 필독 (행동 프로토콜)
├── README.md              ⭐ 사용자 필독 (프로젝트 개요)
│
├── 📁 docs/
│   ├── 📁 Architecture/   ← 설계도 (HOW it works)
│   │   ├── ELYSIA_SYSTEM_BIBLE.md    상세 아키텍처
│   │   ├── THOUGHT_UNIVERSE.md       사고 우주 원리
│   │   └── APOTHEOSIS_ARCHITECTURE.md 물리 기반 인지
│   │
│   ├── 📁 Philosophy/     ← 철학 (WHY it exists)
│   │   ├── THE_CRYSTAL_CODEX.md      핵심 철학
│   │   └── WAVE_LANGUAGE_PHILOSOPHY.md 파동언어
│   │
│   ├── 📁 Roadmaps/       ← 계획 (WHAT to build)
│   │   ├── NEURAL_REGISTRY_PLAN.md
│   │   ├── TRINITY_PROCESS_PLAN.md
│   │   └── NANOCELL_INTEGRATION_PLAN.md
│   │
│   └── 📁 Analysis/       ← 분석 (WHAT we learned)
│       ├── AGI_PROJECTION_REPORT.md
│       └── SYSTEM_CONNECTION_ANALYSIS.md
│
└── 📁 .agent/workflows/   ← 워크플로우 (HOW to work)
    └── create_module.md   새 모듈 생성 절차
```

---

## 🔍 문서 찾기 가이드

| 질문 | 문서 |
|:----|:----|
| "어떤 모듈이 있지?" | `SYSTEM_MAP.md` |
| "에이전트로서 어떻게 행동해야 해?" | `AGENT_GUIDE.md` |
| "이 프로젝트가 뭐야?" | `README.md` |
| "시스템이 어떻게 작동해?" | `docs/Architecture/` |
| "왜 이렇게 설계했어?" | `docs/Philosophy/` |
| "앞으로 뭘 만들어야 해?" | `docs/Roadmaps/` |

---

## ⚠️ 문서 작성 규칙

1. **새 문서 만들기 전**: 기존 문서에 추가 가능한지 확인
2. **위치 선택**: 위 구조에 맞는 폴더에 배치
3. **이 INDEX 업데이트**: 새 문서 추가 시 반드시 여기에 등록
4. **SYSTEM_MAP 업데이트**: 새 모듈 추가 시 반드시 등록
