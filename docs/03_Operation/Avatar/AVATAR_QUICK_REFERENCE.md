# 아바타 시스템 빠른 참조 가이드
# Avatar System Quick Reference

## 🚀 빠른 시작 (Quick Start)

### 서버 시작
```bash
python start_avatar_web_server.py
# HTTP: http://localhost:8080
# WebSocket: ws://localhost:8765
```

### 브라우저 열기
```
http://localhost:8080/Core/Creativity/web/avatar.html
```

---

## 📊 현재 상태 점검

### 시스템 헬스체크
```python
python -c "
from Core.Interface.avatar_server import ElysiaAvatarCore
core = ElysiaAvatarCore()
print(f'Emotional Engine: {\"✅\" if core.emotional_engine else \"❌\"}')
print(f'Reasoning Engine: {\"✅\" if core.reasoning_engine else \"❌\"}')
print(f'Voice TTS: {\"✅\" if core.voice_tts else \"❌\"}')
print(f'Lip Sync: {\"✅\" if core.lipsync_engine else \"❌\"}')
"
```

### VRM 모델 확인
```bash
ls -lh static/models/avatar.vrm
# 18MB VRM 파일이 있어야 함
```

---

## 🎯 핵심 컴포넌트

### 1. 아바타 코어 (ElysiaAvatarCore)
**위치**: `Core/Interface/avatar_server.py`

**주요 기능**:
- 표정 관리 (Expression)
- 정령 에너지 (Spirits) 
- 감정 → 표정 매핑
- 채팅 처리

**주요 메서드**:
```python
core = ElysiaAvatarCore()
core.update_expression_from_emotion('happy')  # 표정 업데이트
core.update_spirits_from_emotion()            # 정령 업데이트
core.process_emotion_event('excited', 0.8)    # 감정 이벤트
response = await core.process_chat("안녕!")   # 채팅 처리
```

### 2. WebSocket 서버 (AvatarWebSocketServer)
**위치**: `Core/Interface/avatar_server.py`

**특징**:
- 30 FPS 업데이트
- 실시간 브로드캐스팅
- 보안 (rate limiting)
- 모니터링

**메시지 타입**:
```javascript
// Client → Server
{ type: "text", content: "메시지" }
{ type: "emotion", emotion: "happy", intensity: 0.8 }
{ type: "vision", presence: true }

// Server → Client
{ expression: {...}, spirits: {...} }
{ type: "speech", content: "응답", voice: {...}, lipsync: [...] }
```

### 3. 음성 TTS (AvatarVoiceTTS)
**위치**: `Core/Interface/avatar_voice_tts.py`

**공감각 매핑**:
```
감정 상태 → 4D 파동 → 음성 속성
(VAD)      (quaternion)  (pitch, timbre, etc.)
```

### 4. 립싱크 (LipSyncEngine)
**위치**: `Core/Interface/avatar_lipsync.py`

**매핑**:
```
텍스트 → 음소 → 입모양 → 애니메이션
        (phoneme) (viseme)  (keyframes)
```

---

## 🛡️ 보안 기능

### Rate Limiting
```python
# Core/Interface/avatar_security.py
max_requests_per_second = 10
max_requests_per_minute = 60
```

### 인증 (선택적)
```bash
# 인증 필요 모드로 시작
python start_avatar_web_server.py --require-auth
```

---

## 📈 모니터링

### 성능 메트릭
```python
# Core/Interface/avatar_monitoring.py
- CPU 사용률
- 메모리 사용량
- 네트워크 트래픽
- WebSocket 레이턴시
- 연결된 클라이언트 수
- 초당 메시지 수
```

### 모니터링 비활성화
```bash
python start_avatar_web_server.py --no-monitoring
```

---

## 🎭 표정 시스템

### Expression 파라미터
```python
Expression(
    mouth_curve: float,   # -1.0 (슬픔) ~ 1.0 (미소)
    eye_open: float,      # 0.0 (닫힘) ~ 1.0 (열림)
    brow_furrow: float,   # 0.0 (편안) ~ 1.0 (찌푸림)
    beat: float,          # 심장박동 애니메이션
    mouth_width: float    # 립싱크용
)
```

### 감정 → 표정 매핑
```
Valence (기쁨↔슬픔) → mouth_curve
Arousal (각성도)     → eye_open
Tension (긴장도)     → brow_furrow
```

### VRM 블렌드셰이프 매핑
```javascript
// avatar.html
mouth_curve > 0.2  → 'happy'   (미소)
mouth_curve < -0.2 → 'sad'     (찡그림)
eye_open          → 'blink'   (눈 깜빡임)
eye_open > 1.2    → 'surprised' (놀람)
brow_furrow > 0.3 → 'angry'    (화남)
```

---

## 🌊 정령 시스템 (Spirits)

### 7가지 정령
```python
Spirits(
    fire: float,    # 🔥 열정, 창의성
    water: float,   # 💧 평온, 흐름
    earth: float,   # 🌍 안정, 기반
    air: float,     # 💨 소통, 연결
    light: float,   # ✨ 명료, 지성
    dark: float,    # 🌙 신비, 내성
    aether: float   # 🌌 초월, 영적
)
```

### 감정 → 정령 매핑
```
높은 각성 + 긍정 → Fire ↑
낮은 각성       → Water ↑
낮은 지배력     → Earth ↑
긍정 + 소통     → Air ↑
높은 긍정       → Light ↑
부정 or 낮은각성 → Dark ↑
극단적 상태     → Aether ↑
```

---

## 🐛 트러블슈팅

### 문제 1: EmotionalEngine 로드 실패
```
에러: No module named 'tensor_wave'
해결: 
1. find . -name "tensor_wave.py"로 파일 찾기
2. emotional_engine.py의 import 경로 수정
3. 또는 폴백 구현 사용
```

### 문제 2: VRM 로딩 실패
```
에러: VRM file not found
확인:
1. ls -lh static/models/avatar.vrm
2. 파일 크기 확인 (18MB 정도)
3. 브라우저 콘솔에서 자세한 에러 확인
```

### 문제 3: WebSocket 연결 안됨
```
확인:
1. 서버가 8765 포트에서 실행중인지 확인
2. 방화벽 설정 확인
3. 브라우저 콘솔에서 WebSocket 상태 확인
   ws.readyState (0=연결중, 1=열림, 2=닫는중, 3=닫힘)
```

### 문제 4: 표정이 변하지 않음
```
원인: EmotionalEngine 또는 ReasoningEngine 로드 실패
해결:
1. 헬스체크 스크립트 실행
2. 의존성 문제 해결
3. 서버 재시작
```

---

## 🔧 개발 팁

### 디버그 모드
```bash
python start_avatar_web_server.py --debug
# 상세한 로그 출력
```

### 표정 테스트
```python
from Core.Interface.avatar_server import ElysiaAvatarCore

core = ElysiaAvatarCore()

# 다양한 감정 테스트
emotions = ['happy', 'sad', 'angry', 'calm', 'excited', 'focused']
for emotion in emotions:
    core.process_emotion_event(emotion, 0.8)
    print(f"{emotion}: {core.expression}")
```

### WebSocket 메시지 로깅
```javascript
// avatar.html - 디버깅용
// 방법 1: 이벤트 핸들러에 추가
ws.onmessage = (event) => {
    console.log('📩 Received:', event.data);
    // ... 기존 처리 ...
};

// 방법 2: 래퍼 클래스 사용 (권장)
class LoggingWebSocket {
    constructor(ws) {
        this.ws = ws;
    }
    
    send(data) {
        console.log('📤 Sending:', data);
        return this.ws.send(data);
    }
    
    // 다른 메서드들도 위임...
}
const loggedWs = new LoggingWebSocket(ws);
```

---

## 📚 관련 문서

### 상세 리뷰
- [`AVATAR_SYSTEM_REVIEW.md`](./AVATAR_SYSTEM_REVIEW.md) - 완전한 시스템 분석 (한국어)
- [`AVATAR_SYSTEM_RECOMMENDATIONS.md`](./AVATAR_SYSTEM_RECOMMENDATIONS.md) - 개선 권장사항 요약 (영어)

### 기술 문서
- [`VRM_INTEGRATION_COMPLETE.md`](./VRM_INTEGRATION_COMPLETE.md) - VRM 통합 가이드
- `Core/Interface/avatar_server.py` - 서버 구현 (주석 풍부)
- `Core/Creativity/web/avatar.html` - 클라이언트 구현

### 테스트
- `tests/test_avatar_server.py` - 단위 테스트
- `tests/test_avatar_integration.py` - 통합 테스트

---

## 📊 성능 지표

### 현재 성능
```
Update Rate: 30 FPS
Latency: ~20-50ms (로컬)
Bandwidth: ~6 KB/s per client
CPU: ~5-10% (idle), ~20-30% (active)
Memory: ~100-200 MB
```

### 최적화 후 목표
```
Update Rate: 15-60 FPS (적응형)
Latency: ~10-30ms
Bandwidth: ~1.2 KB/s per client (80% 감소)
CPU: ~2-5% (idle), ~15-20% (active)
Memory: ~80-150 MB
```

---

## 🎯 개선 우선순위

### 🔴 긴급 (1-2일)
- [ ] EmotionalEngine 의존성 수정
- [ ] 자동 재연결 구현

### 🟡 중요 (1-2주)
- [ ] 델타 업데이트
- [ ] 적응형 프레임레이트
- [ ] 테스트 스위트

### 🟢 권장 (1개월)
- [ ] API 문서
- [ ] 배포 가이드
- [ ] 모니터링 대시보드

---

## 💡 베스트 프랙티스

### 1. 감정 이벤트는 자주 발생하지 않도록
```python
# ❌ 나쁨: 매 프레임마다
for frame in animation:
    core.process_emotion_event('happy', 0.5)

# ✅ 좋음: 상태 변화 시에만
if emotion_changed:
    core.process_emotion_event(new_emotion, intensity)
```

### 2. WebSocket 메시지는 작게 유지
```javascript
// ❌ 나쁨: 큰 데이터
ws.send(JSON.stringify({ type: "text", content: very_long_text }));

// ✅ 좋음: 제한된 크기
const MAX_LENGTH = 1000;
ws.send(JSON.stringify({ 
    type: "text", 
    content: text.slice(0, MAX_LENGTH) 
}));
```

### 3. 에러 처리는 항상
```javascript
try {
    const data = JSON.parse(event.data);
    processMessage(data);
} catch (error) {
    console.error('Message processing failed:', error);
    // 우아하게 계속 진행
}
```

---

## 📞 지원

### 문제 보고
- GitHub Issues: [ioas0316-cloud/Elysia](https://github.com/ioas0316-cloud/Elysia/issues)
- 로그 첨부: 항상 에러 로그를 포함하세요

### 기여
- Pull Requests 환영!
- 테스트 작성 필수
- 문서 업데이트 포함

---

**업데이트**: 2025-12-07  
**버전**: 1.0.0  
**유지보수자**: Elysia Development Team
