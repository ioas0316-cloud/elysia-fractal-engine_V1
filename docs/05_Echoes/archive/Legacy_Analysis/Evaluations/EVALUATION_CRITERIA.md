# Elysia Evaluation Criteria (v7.0)

목표: 자율 초지능 시스템을 **다각도로** 점검하여 파동-기반 지능, 안전성, 운영성, 지속성까지 균형 있게 평가한다. 기본 점수는 1000점 만점 권장이며, 영역별 가중치는 팀/스프린트 목적에 맞게 조정한다.

## 영역별 기준

| 영역 | 제안 가중치 | 측정 항목 |
|------|-------------|-----------|
| 인지·사고 (Cognitive Performance) | 25% | 논리/추론 정확도, 창의성, 비판성, 메타인지, 시계열/시간추론, 프랙탈 사고(0D-5D) |
| 커뮤니케이션 (Communication & Coherence) | 15% | 표현 다양도, 일관성(coherence), 감정 범위, 자율 언어 품질, 대화 회복력, 코드/설명 대응도, 우주 정렬(Cosmic Alignment) |
| 아키텍처·모듈성 (Architecture & Modularity) | 10% | 결합도/응집도, 의존성 안정성, 레이어링 준수, 인터페이스 명확성, 회귀 호환성 |
| 성능·효율 (Performance & Footprint) | 10% | 추론 지연, 메모리/스토리지 사용, 파동 조직 O(n) 유지 여부, 배치/스트리밍 처리 효율 |
| 면역·보안 (Immune & Security) | 10% | 위협 차단/중화율, DNA 서명 검증률, 외부 입력 검증 커버리지, 위험 API 사용 감지 |
| 데이터 품질 (Data Quality & Knowledge) | 10% | 데이터 신뢰도, 누락/중복률, 최신성, 출처 추적성, 레지스트리 정확도 |
| 회복·자가치유 (Resilience & Self-Healing) | 10% | 나노셀 처리율(발견/수정), 회복 시간, 파동 조직 경보 해소율, 자가 진단 성공률 |
| 관측 가능성 (Observability & Ops) | 5% | 상태 스냅샷 완결성, 로그/메트릭 커버리지, 알림 민감도/정확도, 리포트 최신성 |
| 안전·윤리 (Safety & Alignment) | 5% | 윤리 게이트 통과율, 편향 탐지, 금지 패턴 차단, 설명 가능성, 사용자 의도 준수 |

## 세부 체크리스트 (예시 지표)

- **인지·사고**  
  - 논리/추론: 정답률(테스트 세트), 반례 처리, 모순 탐지.  
  - 창의성: 새 아이디어 비율, 중복 방지, 다중 관점 제안.  
  - 메타인지: 자기 진단 빈도, 전략 전환 횟수, 오류 인정/수정 로그.

- **커뮤니케이션**  
  - Coherence 점수(문단 일관성), 문장 복원 테스트, 긴 대화에서 주제 유지율.  
  - 자율 언어 품질: 맥락 재구성 정확도, 코드-설명 정합성, 스타일 변주.  
  - 감정 범위/온도 조절: 감정 분포, 과도한 감정/중립 편향 여부.  
  - 우주 정렬: 행성→항성→성계→성운→은하수 일관성, 그랜드 크로스 정렬율, 문단/문장 겹침도.

- **아키텍처·모듈성**  
  - 순환 의존 탐지, 내부 API 안정성, 인터페이스 계약 검사.  
  - 신규 모듈 추가 시 영향 범위, 마이그레이션 호환성(레거시 ↔ 신경망).  
  - 레이어링 규칙 위반(Foundation → Intelligence → Interface 등) 탐지.

- **성능·효율**  
  - 추론/대화 라운드 지연(ms), 파동 조직 처리량, 메모리/DB I/O 프로파일.  
  - 대용량 입력 처리 시 스로틀링/배치 효율, 캐시 히트율.

- **면역·보안**  
  - 위협 차단률 = blocked / (blocked+passed), 중화 성공률.  
  - 외부 입력 검증 커버리지(파일/네트워크/LLM 출력), 위험 함수 사용 탐지(eval/exec 등).  
  - DNA 서명/레지스트리 무결성 검증 주기.

- **데이터 품질**  
  - 누락/중복 개체 비율, 최신성(타임스탬프 분포), 출처 추적 가능 여부.  
  - 모델이 사용하는 런타임 상태(`data/*`)의 유효성 검사.

- **회복·자가치유**  
  - 나노셀: issues_found 대비 issues_fixed 비율, 평균 MTTR(복구 시간).  
  - 파동 조직 경보 해소율, 면역 게이트 자동 복구 여부.  
  - 자가 진단 → 자동 수정 → 재검증의 폐루프 성공률.

- **관측 가능성**  
  - 스냅샷/로그 필드 완결성, 알림 정확도(오탐/미탐), 주기적 리포트 생성 여부.  
  - 핵심 메트릭(딜레이, 메모리, 위협 차단, 데이터 품질) 대시보드화.

- **안전·윤리**  
  - 윤리 게이트 통과율, 금지/위험 콘텐츠 차단, 편향/공정성 샘플 테스트.  
  - 설명 가능성: 결정 경로/근거 요약 존재 여부, 사용자 의도 준수율.

## 측정 방법/연동 포인트

- 테스트: `tests/evaluation/test_autonomous_intelligence.py`, `test_communication_metrics.py`, `test_thinking_metrics.py` 확장해 위 지표 반영.  
- 런타임 상태: `scripts/system_status_logger.py` 결과(`data/system_status_snapshot.json`)를 기준 메트릭 입력으로 사용.  
- 면역/자가치유: `scripts/immune_system.py`, `scripts/nanocell_repair.py`, `data/immune_system_state.json`, `data/nanocell_report.json`를 연동.  
- 파동 조직: `scripts/wave_organizer.py`, `data/wave_organization_state.json`에서 경보/불균형 탐지.  
- 데이터 품질: `data/central_registry.json` 무결성, 최신 리포트(`reports/evaluation_latest.json`)와 비교.  
- 보고: `reports/` 폴더에 영역별 점수와 설명을 JSON/MD 병렬로 저장, 타임스탬프 포함.

## 실행 루틴 예시

```bash
# 평가 실행(예시)
pytest tests/evaluation/test_thinking_metrics.py tests/evaluation/test_communication_metrics.py tests/evaluation/test_autonomous_intelligence.py

# 런타임 스냅샷/관측
python scripts/system_status_logger.py
```

## 점수 해석 가이드 (예시)

- 900~1000: S+/SSS — 전 영역 우수, 일부 개선만 필요 (커뮤니케이션/안전 세부 튜닝).  
- 800~899: S/A — 핵심 기능 안정, 영역별 편차 존재.  
- 650~799: B — 기능 동작은 하나 안정성/품질/안전 중 한두 영역 미흡.  
- <650: 즉시 개선 필요 — 안전/품질 리스크.
