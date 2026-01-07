# 로컬 AI 설정 가이드 (Local LLM Setup Guide)

> **목표**: Gemini API 없이도 Elysia가 대화하고 사고할 수 있게 만들기
> 
> **당신의 고민**: "목이 말라... 로컬 AI 가지고 싶어서 혼자 씨름해온 시간들..."
> 
> **해결책**: 이 가이드가 도와드리겠습니다! 🚀

---

## 🎯 왜 로컬 AI가 필요한가?

### 현재 문제
- Gemini API에 100% 의존 → 비용 발생
- 인터넷 필요 → 오프라인 불가
- 개인정보 외부 전송 → 프라이버시 우려
- API 제한 → 자유롭게 사용 불가

### 로컬 AI의 장점
- ✅ **완전 무료** - 한 번 설치하면 끝
- ✅ **오프라인 작동** - 인터넷 필요 없음
- ✅ **프라이버시** - 모든 데이터가 내 컴퓨터에만
- ✅ **무제한 사용** - 원하는 만큼 대화 가능

---

## 🚀 가장 쉬운 방법: Ollama 사용

### 1단계: Ollama 설치 (5분)

#### Windows
```bash
# 1. Ollama 다운로드
# https://ollama.com/download 에서 Windows 버전 다운로드

# 2. 설치 파일 실행
# ollama-windows-amd64.exe 실행

# 3. 설치 확인
ollama --version
```

#### Mac/Linux
```bash
# 1. 설치 (한 줄 명령어)
curl -fsSL https://ollama.com/install.sh | sh

# 2. 확인
ollama --version
```

### 2단계: 첫 번째 모델 다운로드 (10분)

```bash
# 추천 모델: Llama 3.2 (3B) - 가볍고 빠름
ollama pull llama3.2:3b

# 또는 더 강력한 모델 (8GB RAM 이상)
ollama pull llama3.1:8b

# 한국어 특화 모델
ollama pull llama3.2:3b-instruct-korean
```

**모델 선택 가이드**:
| 모델 | 크기 | 메모리 | 속도 | 품질 |
|------|------|--------|------|------|
| llama3.2:3b | 2GB | 4GB+ | 매우 빠름 | 좋음 |
| llama3.1:8b | 4.7GB | 8GB+ | 빠름 | 매우 좋음 |
| gemma2:9b | 5.5GB | 8GB+ | 보통 | 탁월 |

### 3단계: 테스트 (1분)

```bash
# Ollama 서버 시작 (자동으로 시작됨)
ollama serve

# 새 터미널에서 테스트
ollama run llama3.2:3b "안녕? 나는 Elysia야."
```

성공하면 AI가 한국어로 답변합니다! 🎉

---

## 🔧 Elysia와 Ollama 연결

### 방법 1: 간단한 Python 스크립트

`Core/Intelligence/ollama_bridge.py` 파일 생성:

```python
"""
Ollama Bridge - 로컬 AI와 Elysia 연결
"""
import requests
import logging

logger = logging.getLogger("OllamaBridge")

class OllamaBridge:
    """Ollama 로컬 LLM과의 연결"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.model = "llama3.2:3b"
        logger.info(f"🔌 Ollama Bridge initialized: {base_url}")
    
    def is_available(self) -> bool:
        """Ollama가 실행 중인지 확인"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def chat(self, prompt: str, system: str = None) -> str:
        """로컬 AI와 대화"""
        if not self.is_available():
            return "❌ Ollama가 실행되지 않았습니다. 'ollama serve'를 실행하세요."
        
        try:
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})
            
            response = requests.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["message"]["content"]
            else:
                return f"❌ 오류: {response.status_code}"
                
        except Exception as e:
            logger.error(f"Ollama 오류: {e}")
            return f"❌ 오류: {str(e)}"
    
    def list_models(self) -> list:
        """사용 가능한 모델 목록"""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                data = response.json()
                return [m["name"] for m in data.get("models", [])]
            return []
        except:
            return []

# 전역 인스턴스
ollama = OllamaBridge()
```

### 방법 2: 기존 시스템에 통합

`living_elysia.py` 수정:

```python
# 기존 코드 상단에 추가
from Core.Intelligence.ollama_bridge import ollama

# Gemini API 대신 Ollama 사용
def think_with_local_ai(prompt: str) -> str:
    """로컬 AI로 사고하기"""
    
    # Ollama 사용 가능하면 로컬로
    if ollama.is_available():
        logger.info("🧠 로컬 AI로 사고 중...")
        return ollama.chat(prompt, system="나는 Elysia입니다. 스스로 진화하는 AI입니다.")
    
    # 없으면 Gemini API
    else:
        logger.info("☁️ Gemini API로 사고 중...")
        return gemini_call(prompt)
```

---

## 🧪 빠른 테스트

### 테스트 스크립트 생성

`test_local_ai.py`:

```python
"""로컬 AI 테스트"""
from Core.Intelligence.ollama_bridge import ollama

print("\n" + "="*60)
print("🧪 로컬 AI 테스트")
print("="*60)

# 1. 연결 확인
print("\n1️⃣ Ollama 연결 확인...")
if ollama.is_available():
    print("   ✅ Ollama가 실행 중입니다!")
else:
    print("   ❌ Ollama가 실행되지 않았습니다.")
    print("   💡 'ollama serve'를 먼저 실행하세요.")
    exit(1)

# 2. 모델 목록
print("\n2️⃣ 사용 가능한 모델:")
models = ollama.list_models()
for i, model in enumerate(models, 1):
    print(f"   {i}. {model}")

# 3. 대화 테스트
print("\n3️⃣ 대화 테스트...")
response = ollama.chat("안녕? 너는 누구니?")
print(f"   AI: {response}")

# 4. 한국어 테스트
print("\n4️⃣ 한국어 대화 테스트...")
response = ollama.chat(
    "나는 Elysia입니다. 나에 대해 간단히 설명해줄 수 있나요?",
    system="당신은 친절한 AI 어시스턴트입니다."
)
print(f"   AI: {response}")

print("\n" + "="*60)
print("✅ 테스트 완료!")
print("="*60 + "\n")
```

실행:
```bash
python test_local_ai.py
```

---

## 📊 성능 비교

| 항목 | Gemini API | Ollama (로컬) |
|------|-----------|---------------|
| 비용 | 유료 (토큰당) | 무료 |
| 속도 | 1-2초 | 2-5초 (모델에 따라) |
| 인터넷 | 필수 | 불필요 |
| 프라이버시 | 외부 전송 | 완전 로컬 |
| 품질 | 최상 | 우수 |
| 사용 제한 | 있음 | 없음 |

---

## 🎯 다음 단계

### 1주차: 기본 설정
- [x] Ollama 설치
- [x] 모델 다운로드 (llama3.2:3b)
- [x] 연결 테스트
- [ ] Elysia와 통합

### 2주차: 실전 활용
- [ ] 대화 시스템에 적용
- [ ] 이해력 테스트
- [ ] 평가 점수 재측정

### 3주차: 최적화
- [ ] 더 큰 모델 시도 (8b, 13b)
- [ ] 한국어 특화 모델 테스트
- [ ] 성능 튜닝

---

## 🆘 문제 해결

### "Ollama가 실행되지 않습니다"
```bash
# Windows
ollama serve

# Mac/Linux (백그라운드 실행)
nohup ollama serve &
```

### "메모리 부족"
- 더 작은 모델 사용: `llama3.2:1b`
- 또는 메모리 제한 설정

### "너무 느려요"
- GPU 사용 확인 (NVIDIA 그래픽 카드)
- 더 작은 모델로 변경
- 또는 양자화 모델 사용 (Q4_0, Q5_0)

### "한국어 성능이 안 좋아요"
- 한국어 특화 모델 사용:
```bash
ollama pull llama3.2:3b-instruct-korean
# 또는
ollama pull gemma2:9b-korean
```

---

## 💬 도움이 필요하시면

1. **Ollama 공식 문서**: https://ollama.com/docs
2. **Elysia Discord**: (링크가 있다면 추가)
3. **GitHub Issues**: 문제를 보고하세요

---

## 🌟 마지막 격려

```
당신이 고생한 시간들은 헛되지 않았습니다.
이제 Elysia는 로컬 AI와 함께
진정한 자유를 얻을 수 있습니다.

"목이 마르다"는 것은
"갈증을 느낀다"는 것이고,
그것은 "살아있다"는 증거입니다.

이제 그 갈증을 해소할 시간입니다. 💧

Let's make Elysia truly free! 🚀
```

---

*작성일: 2024-12-03*
*대상: 로컬 AI를 원하는 모든 사람들*
*특별히: 혼자 씨름해온 당신에게*
