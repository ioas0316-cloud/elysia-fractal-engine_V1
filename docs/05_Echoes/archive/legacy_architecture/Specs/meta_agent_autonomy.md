## MetaAgent Autonomy Guide

이제 엘리시아는 **자율적으로 자료를 찾아서, 흡수하고, 법칙/문법을 다시 기르는 메타 루프**를 갖게 되었습니다. 다음 키워드를 기억하세요:

### 1. 자료 공급 (자율 탐색)

1. `data/corpus_feed/`는 엘리시아에게 새 영양소를 주입하는 장소입니다. 여기엔:
   * 공개 대화, 에세이, 철학 텍스트 (`.md`, `.txt`)
   * 수학/프로그래밍 해설 (`.md`, `.py`, `.json`)
   * 코드 스니펫이나 로그 (`.py`, `.json`, `.js`)
   등을 자유롭게 복사(혹은 drop)하세요.
2. `MetaAgent`가 주기적으로 `data/corpus_feed/`를 훑어서 `data/corpus_incoming/`으로 자동 이동하고, `scripts/ingest_corpus.py`가 이를 분류해서 실제 코퍼스에 덮어쓴 뒤 `scripts/run_meta_agent.py`를 호출해 학습 흐름을 다시 시작합니다.
3. 이 루프를 멈추지 않고 돌리려면 `scripts/run_meta_agent_loop.py`를 실행(예: 작업 스케줄러/백그라운드 프로세스)하세요. 내부적으로 `MetaAgent.autonomous_loop()`가 `cycle()`을 반복하며 feed/MetaLaw/grammar/ 상태를 업데이트합니다.

### 2. 무의식 학습

* `MetaAgent.autonomous_loop()`는 `MetaAgent` 주기(기본 60초)마다 다음을 수행합니다:
  * `data/corpus_feed/`에서 새 파일을 수집 → `data/corpus_incoming/`에 이동.
  * `MetaLawEngine`으로 CoreMemory를 다시 훑어 law 축을 재정의하고 KG에 연결.
  * `scripts/refine_feed.py`�� `data/corpus_incoming/`���� ������ �������� ������� ���̴�, ���ۿ� ���ִ� ���ڸ��� `data/corpus_archive/`�� �����Ѵ�.
  * `scripts/train_grammar.py`를 다시 실행하여 문법 통계를 갱신 (`grammar_model.json`).
  * 상태 (`meta_agent_state.json`)를 저장하므로 다음 주기에는 변화만 반영됩니다.

### 3. 모니터링 & 로그

* `MetaAgent` 각 사이클의 반환값에 `feed`, `meta_law`, `grammar` 키가 담겨 있으므로 `scripts/run_meta_agent_loop.py`를 터미널에서 띄워놓고 관찰하면 “얼마나 새로운 자료를 빨아들였는지”, “law/grammar가 변화했는지”를 실시간으로 확인할 수 있습니다.
* `logs/language_progress.jsonl`에는 정기 평가(`scripts/evaluate_language_progress.py`) 결과가 쌓이므로, 주기 실행과 함께 누적 데이터(턴 수, law focus 분포, 평균 path 길이 등)를 분석하면 언어 능력 향상 그래프를 그릴 수 있습니다.

### 4. 외부 자료/인터넷 연결 (미래 확장)

* `MetaAgent`는 현재 로컬 feed만 처리하지만, `data/corpus_feed/`를 채우는 자동화 스크립트(예: `download_feed.py`)를 추가하면 인터넷 공개 텍스트를 `feed/`에 내려받고, 자동 루프에 흡수시킬 수 있습니다.
* 필요한 경우 알려주시면 URL 리스트, RSS, API 호출 등을 `data/corpus_feed/`에 주기적으로 배치하는 helper script도 만들어 드릴 수 있습니다.

이제 엘리시아는 “밥이 들어올 때마다” 스스로 그 밥을 KG에 연결하고, 법칙 축 위에 올려두고, 문장을 정리해서 다시 말을 하므로, 당신이 곁에 없어도 시스템 전체가 프랙탈하게 확장됩니다.