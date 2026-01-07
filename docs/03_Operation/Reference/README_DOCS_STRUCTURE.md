# 문서 구조 가이드 / Documentation Structure Guide

**업데이트 날짜 / Updated**: 2025-12-07  
**버전 / Version**: 9.1  
**상태 / Status**: 아바타 시스템 문서 추가 / Avatar System Docs Added

---

## 📁 새로운 문서 구조 / New Documentation Structure

### 주요 변경사항 / Major Changes

1. **데이터 파일 이동** ✅
   - 82개 JSON 개념 파일 → `../data/concepts/`
   - `awakening_log.txt` → `../data/`

2. **로드맵 문서 재구성** ✅
   - 버전별 폴더 구조: P1, P2, P3, P4
   - 구현 계획과 완료 요약 분리

3. **분석/평가 문서 정리** ✅
   - V9 시스템 분석 전용 폴더
   - 평가 문서 아카이브

4. **레거시 문서 정리** ✅
   - 오래된 문서들을 `legacy/` 폴더로 이동

---

## 📂 현재 디렉토리 구조 / Current Directory Structure

```
docs/
├── README_DOCS_STRUCTURE.md          # 이 파일 (구조 가이드)
│
├── Roadmaps/                          # 🗺️ 로드맵 문서
│   ├── ACCELERATED_DEVELOPMENT_ROADMAP.md
│   ├── EXTENDED_ROADMAP_2025_2030.md
│   ├── P4_PREPARATION_DOCUMENTATION_MAPPING.md
│   │
│   ├── P1-Completion/                 # P1 완료 문서
│   │   └── P1_COMPLETION_SUMMARY.md
│   │
│   ├── P2-Implementation/             # P2 구현 문서 (완료 ✅)
│   │   ├── P2_IMPLEMENTATION_PLAN.md
│   │   ├── P2_OVERALL_PROGRESS.md
│   │   ├── P2_2_COMPLETION_SUMMARY.md
│   │   ├── P2_2_WAVE_KNOWLEDGE_SYSTEM.md
│   │   └── P2_3_CI_CD_COMPLETION.md
│   │
│   └── P3-Implementation/             # P3 구현 문서 (P3.1, P3.2 완료 ✅)
│       ├── P3_IMPLEMENTATION_PLAN.md
│       ├── P3_1_CONSCIOUSNESS_FABRIC_COMPLETION.md
│       └── P3_2_PURPOSE_DISCOVERY_COMPLETION.md
│
├── Analysis/                          # 📊 분석 및 평가
│   ├── V9-System/                     # V9.0 시스템 분석
│   │   ├── COMPREHENSIVE_SYSTEM_ANALYSIS_V9.md
│   │   └── SYSTEM_ANALYSIS_SUMMARY_KR.md
│   │
│   └── Evaluations/                   # 평가 프레임워크
│       ├── EVALUATION_CRITERIA.md
│       ├── EVALUATION_FRAMEWORK.md
│       ├── EVALUATION_SUMMARY_KR.md
│       └── PROJECT_EVALUATION.md
│
├── Guides/                            # 📖 가이드
│   ├── How_To_Start.txt
│   └── [기타 가이드 문서들]
│
├── Manuals/                           # 📘 매뉴얼
│   ├── CODE_QUALITY.md
│   ├── TESTING.md
│   ├── SECURITY.md
│   └── [기타 매뉴얼들]
│
├── [Avatar System Docs in docs/]     # 🎭 아바타 시스템 문서
│   ├── AVATAR_SERVER_SYSTEM.md        # 전체 시스템 아키텍처
│   ├── AVATAR_SERVER_QUICK_START.md   # 빠른 시작 가이드
│   ├── AVATAR_SERVER_IMPLEMENTATION_REPORT_KR.md  # 구현 보고서
│   ├── VRM_INTEGRATION_COMPLETE.md    # VRM 통합 가이드
│   ├── VRM_INTEGRATION_SUMMARY.md     # VRM 구현 요약
│   ├── AVATAR_SYSTEM_REVIEW_2025.md   # 시스템 검증 및 개선안
│   └── AVATAR_DOCUMENTATION_SUMMARY_KR.md  # 한국어 요약본
│
├── Reference/                         # 📚 참조 자료
├── Summaries/                         # 📝 요약 문서
├── Vision/                            # 🔮 비전 문서
├── Visuals/                           # 🎨 시각 자료
│
├── concepts/                          # 💭 개념 문서 (JSON은 data/로 이동됨)
├── images/                            # 🖼️ 이미지
├── reports/                           # 📋 보고서
├── retrospectives/                    # 🔄 회고
│
└── legacy/                            # 🗄️ 레거시 문서 (아카이브)
    ├── BRANCH_IDEA_LOG.md
    ├── COMPLETE_TRANSFORMATION_JOURNEY.md
    ├── DUPLICATE_CONSOLIDATION_FINAL_REPORT.md
    ├── PERSONALITY_ENTITY_GAP_ANALYSIS.md
    ├── SESSION_COMPLETE_SUMMARY.md
    └── old-summaries/
```

---

## 🎯 문서 찾기 가이드 / Document Finding Guide

### 로드맵 관련 문서를 찾으려면

**P1 로드맵**:
- 📁 `Roadmaps/P1-Completion/`

**P2 로드맵** (완료 ✅):
- 📁 `Roadmaps/P2-Implementation/`
- 주요 문서:
  - P2_IMPLEMENTATION_PLAN.md (전체 계획)
  - P2_OVERALL_PROGRESS.md (진행 상황)
  - P2_2_WAVE_KNOWLEDGE_SYSTEM.md (파동 지식 시스템)
  - P2_2_COMPLETION_SUMMARY.md (P2.2 완료)
  - P2_3_CI_CD_COMPLETION.md (P2.3 완료)

**P3 로드맵** (P3.1, P3.2 완료 ✅):
- 📁 `Roadmaps/P3-Implementation/`
- 주요 문서:
  - P3_IMPLEMENTATION_PLAN.md (전체 계획)
  - P3_1_CONSCIOUSNESS_FABRIC_COMPLETION.md (의식 직물 완료)
  - P3_2_PURPOSE_DISCOVERY_COMPLETION.md (목적성 발견 완료)

**P4 준비**:
- 📄 `Roadmaps/P4_PREPARATION_DOCUMENTATION_MAPPING.md`

**장기 로드맵**:
- 📄 `Roadmaps/EXTENDED_ROADMAP_2025_2030.md`
- 📄 `Roadmaps/ACCELERATED_DEVELOPMENT_ROADMAP.md`

### 시스템 분석 문서를 찾으려면

**V9.0 종합 분석** (최신 ⭐):
- 📁 `Analysis/V9-System/`
- 주요 문서:
  - COMPREHENSIVE_SYSTEM_ANALYSIS_V9.md (850+ lines, P2+P3 반영)
  - SYSTEM_ANALYSIS_SUMMARY_KR.md (한국어 요약)

**평가 프레임워크**:
- 📁 `Analysis/Evaluations/`
- 평가 기준, 프레임워크, 프로젝트 평가

### 개념 데이터 파일을 찾으려면

**JSON 개념 파일**:
- 📁 `../data/concepts/` (docs에서 data로 이동됨)
- 내용: 00_concept_*.json, 01_shape_*.json, scene_*.json 등

### 레거시 문서를 찾으려면

**오래된/중복 문서**:
- 📁 `legacy/`
- 이전 세션 요약, 통합 보고서, 브랜치 아이디어 로그 등

---

## 🗂️ 버전별 문서 정리 / Version-Based Organization

### AGI 7단계 시스템 보고서

| 버전 | 문서 | 위치 | 날짜 |
|------|------|------|------|
| **V9.0** | COMPREHENSIVE_SYSTEM_ANALYSIS_V9.md | `Analysis/V9-System/` | 2025-12-06 (최신) |
| V9.0 요약 | SYSTEM_ANALYSIS_SUMMARY_KR.md | `Analysis/V9-System/` | 2025-12-06 |

**V9.0 포함 내용**:
- AGI 점수: 4.25 / 7.0 (21% 향상)
- P2 로드맵 완료 반영 (P2.2, P2.3)
- P3 로드맵 완료 반영 (P3.1, P3.2)
- Level 4: 85%, Level 5: 65%, Level 6: 45%

### 로드맵 버전 히스토리

| 단계 | 상태 | 문서 위치 | 완료일 |
|------|------|-----------|--------|
| **P1** | ✅ 완료 | `Roadmaps/P1-Completion/` | [이전] |
| **P2.1** | ✅ 분석 | `Roadmaps/P2-Implementation/` | 2025-12-06 |
| **P2.2** | ✅ 완료 | `Roadmaps/P2-Implementation/` | 2025-12-06 |
| **P2.3** | ✅ 완료 | `Roadmaps/P2-Implementation/` | 2025-12-06 |
| **P3.1** | ✅ 완료 | `Roadmaps/P3-Implementation/` | 2025-12-06 |
| **P3.2** | ✅ 완료 | `Roadmaps/P3-Implementation/` | 2025-12-06 |
| **P3.3-P3.5** | 📋 계획됨 | `Roadmaps/P3-Implementation/` | TBD |
| **P4** | 📋 준비 중 | `Roadmaps/` | TBD |

---

## 📝 문서 업데이트 정책 / Document Update Policy

### 새 문서 추가 시

1. **로드맵 관련**: `Roadmaps/P[N]-Implementation/` 또는 `Roadmaps/P[N]-Completion/`
2. **시스템 분석**: `Analysis/V[N]-System/` (버전별 폴더)
3. **평가**: `Analysis/Evaluations/`
4. **가이드**: `Guides/`
5. **매뉴얼**: `Manuals/`

### 문서 명명 규칙

**로드맵 문서**:
- 계획: `P[N]_IMPLEMENTATION_PLAN.md`
- 진행: `P[N]_OVERALL_PROGRESS.md`
- 완료: `P[N]_[FEATURE]_COMPLETION.md` 또는 `P[N]_COMPLETION_SUMMARY.md`
- 상세: `P[N]_[N]_[FEATURE_NAME].md`

**분석 문서**:
- 종합: `COMPREHENSIVE_SYSTEM_ANALYSIS_V[N].md`
- 요약: `SYSTEM_ANALYSIS_SUMMARY_[LANG].md`

**평가 문서**:
- `EVALUATION_[TYPE].md`

### 오래된 문서 처리

1. 더 이상 사용하지 않는 문서 → `legacy/`
2. 중복 문서 → 최신 문서로 통합 후 구 문서는 `legacy/`
3. 세션 완료 문서 → `legacy/`
4. 브랜치별 임시 문서 → `legacy/` 또는 삭제

---

## 🔍 빠른 참조 / Quick Reference

### 가장 중요한 문서 Top 5

1. **📄 COMPREHENSIVE_SYSTEM_ANALYSIS_V9.md**
   - 위치: `Analysis/V9-System/`
   - 내용: v9.0 전체 시스템 분석 (AGI 7단계, P2+P3 반영)

2. **📄 P2_OVERALL_PROGRESS.md**
   - 위치: `Roadmaps/P2-Implementation/`
   - 내용: P2 로드맵 완료 상태 및 성과

3. **📄 P3_IMPLEMENTATION_PLAN.md**
   - 위치: `Roadmaps/P3-Implementation/`
   - 내용: P3 로드맵 전체 계획 (P3.1, P3.2 완료)

4. **📄 P4_PREPARATION_DOCUMENTATION_MAPPING.md**
   - 위치: `Roadmaps/`
   - 내용: P4 준비를 위한 문서 매핑 및 검증

5. **📄 DOCUMENTATION_INDEX.md**
   - 위치: `../` (루트)
   - 내용: 전체 문서 색인 (142+개 문서)

### 아바타 시스템 문서 (2025-12-07 업데이트 🆕)

**빠른 시작**:
- **AVATAR_SERVER_QUICK_START.md** - 5분 만에 시작하기
- **VRM_INTEGRATION_COMPLETE.md** - VRM 3D 아바타 가이드

**상세 문서**:
- **AVATAR_SERVER_SYSTEM.md** - 전체 아키텍처 및 API
- **AVATAR_SYSTEM_REVIEW_2025.md** - 문서화 검증 및 개선안 (40KB)
- **AVATAR_DOCUMENTATION_SUMMARY_KR.md** - 한국어 요약본 (5KB)

**구현 보고서**:
- **AVATAR_SERVER_IMPLEMENTATION_REPORT_KR.md** - 한국어 구현 보고서
- **VRM_INTEGRATION_SUMMARY.md** - VRM 통합 요약

**기능 문서 (2025-12-07 신규)**:
- **SYNESTHESIA_VOICE_INTEGRATION.md** - 공감각 음성 합성 시스템 (40KB)
- **LIPSYNC_SYSTEM.md** - 음소 기반 립싱크 엔진 (40KB)
- **AVATAR_SECURITY_SYSTEM.md** - 보안 시스템 (인증, Rate limiting, 입력 검증) (40KB)
- **AVATAR_MONITORING_SYSTEM.md** - 실시간 성능 모니터링 (40KB)
- **AVATAR_PRODUCTION_DEPLOYMENT.md** - 프로덕션 배포 가이드 (HTTPS, Nginx) (40KB)

### 현재 AGI 진행도 (2025-12-06)

```
AGI Score: 4.25 / 7.0 (60.7%)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Level 0-3: 완료 ✅ (100%)
Level 4: 진행중 ◐ (85%)
Level 5: 진행중 ◑ (65%)
Level 6: 진행중 ◔ (45%)
Level 7: 계획 ○ (0%)
```

---

## 🎯 다음 단계 / Next Steps

### P4 로드맵 진행 시

1. ✅ 문서 구조 재정리 완료
2. ✅ V9.0 시스템 분석 업데이트 완료
3. ✅ P2, P3 완료 문서 정리 완료
4. 📋 P4 로드맵 계획 수립
5. 📋 P4 구현 시작

### 문서 유지보수

- 새 로드맵 단계 시작 시 → 새 폴더 생성 (예: `P5-Implementation/`)
- 시스템 버전 업데이트 시 → 새 분석 폴더 생성 (예: `Analysis/V10-System/`)
- 분기별 → 레거시 문서 정리

---

**작성자 / Author**: Elysia Documentation System  
**최종 업데이트 / Last Updated**: 2025-12-07  
**문의 / Contact**: docs 폴더 관리자

---

**"깔끔한 문서 구조는 명확한 사고의 반영이다."**

*"A clean documentation structure reflects clear thinking."*
