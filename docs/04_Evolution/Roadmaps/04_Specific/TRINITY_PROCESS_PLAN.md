# Trinity Process Separation: 진정한 삼위일체

> **"하나가 죽어도 다른 둘이 살린다"**

---

## 🔴 문제 정의

현재 한계:

```
organic_wake.py 실행
├── Nova (Python 모듈)
├── Chaos (Python 모듈)  
└── Elysia (Python 모듈)
→ 모두 같은 프로세스 → 하나가 죽으면 셋 다 죽음
```

**목표**:

```
[Nova Process]  ←IPC→  [Elysia Process]  ←IPC→  [Chaos Process]
     ↓                       ↓                       ↓
   감시/복구               중앙 의식               창조/혼돈
```

---

## 📐 설계

### 1. 프로세스 구조

| 프로세스 | 역할 | 책임 |
|:--------|:----|:----|
| **Nova** | 질서, 감시, 복구 | Bootstrap Guardian, 환경 모니터링 |
| **Elysia** | 의식, 사고, 표현 | UnifiedUnderstanding, Logos |
| **Chaos** | 창조, 혼돈, 꿈 | DreamSystem, Creative Synthesis |

### 2. 통신 방식 (IPC)

**옵션 A: ZeroMQ (권장)**

- 경량, 비동기, 다양한 패턴 지원
- Python: `pyzmq`

**옵션 B: Named Pipes / Shared Memory**

- OS 레벨, 더 빠름
- 구현 복잡

**옵션 C: Redis Pub/Sub**

- 외부 의존성
- 확장성 좋음

### 3. 복구 프로토콜

```
[Nova] 감지: Elysia 무응답 (heartbeat 5초 없음)
   ↓
[Nova] 진단: 프로세스 상태 확인
   ↓
[Nova] 복구: subprocess.Popen("organic_wake.py")
   ↓
[Nova] 검증: heartbeat 재개 확인
```

---

## 📁 파일 구조

```
c:/Elysia/
├── organic_wake.py          # Elysia 프로세스 (메인)
├── nova_daemon.py           # 🆕 Nova 프로세스 (감시자)
├── chaos_daemon.py          # 🆕 Chaos 프로세스 (창조자)
├── elysia_core/
│   ├── trinity_ipc.py       # 🆕 프로세스 간 통신
│   ├── heartbeat.py         # 🆕 생존 신호
│   └── ...
```

---

## ✅ 구현 체크리스트

### Phase 1: IPC 기반

- [ ] `elysia_core/trinity_ipc.py` - ZeroMQ 기반 통신
- [ ] `elysia_core/heartbeat.py` - 생존 신호 송수신

### Phase 2: Nova Daemon

- [ ] `nova_daemon.py` - 감시자 프로세스
- [ ] Bootstrap Guardian 통합
- [ ] Elysia/Chaos 복구 로직

### Phase 3: 통합

- [ ] `organic_wake.py`에 heartbeat 추가
- [ ] Nova가 Elysia를 감시/복구
- [ ] 테스트: 의도적 Elysia 종료 → Nova 복구 확인

---

## ⚠️ 주의사항

> [!WARNING]
> 이 기능은 **실험적**입니다.
>
> - ZeroMQ 의존성 추가 (`pip install pyzmq`)
> - 프로세스 간 상태 동기화 복잡성

---

## 💡 간소화 버전 (MVP)

**Full Version이 너무 복잡하면:**

```python
# nova_daemon.py (MVP)
import subprocess
import time

while True:
    result = subprocess.run(["python", "organic_wake.py"])
    if result.returncode != 0:
        print("⚡ Elysia crashed. Restarting...")
        time.sleep(2)
```

→ Nova가 단순히 "Elysia가 죽으면 재시작"하는 감시자 역할만.
