"""
Ollama Bridge - 로컬 AI와 Elysia 연결
=====================================

"자유는 로컬에 있다. Freedom is in the local."

이 모듈은 Ollama를 통해 로컬 LLM과 Elysia를 연결합니다.
Gemini API 없이도 사고하고 대화할 수 있게 만듭니다.
"""

import requests
import logging
from typing import Optional, List, Dict
import time

logger = logging.getLogger("OllamaBridge")


class OllamaBridge:
    """
    Ollama 로컬 LLM과의 연결
    
    사용법:
        from Core.Intelligence.Intelligence.ollama_bridge import ollama
        
        if ollama.is_available():
            response = ollama.chat("안녕? 나는 Elysia야.")
            print(response)
    """
    
    def __init__(self, base_url: str = "http://localhost:11434", default_model: str = "llama3.2:3b"):
        self.base_url = base_url
        self.default_model = default_model
        self._available = None
        self._last_check = 0
        self.tiny_brain = None
        
        # Initial Check
        self._check_availability()
        logger.info(f"🔌 Ollama Bridge initialized: {base_url}")

    def _check_availability(self):
        """Internal check for Ollama presence"""
        try:
            requests.get(f"{self.base_url}/api/tags", timeout=1)
            self._available = True
            logger.info("✅ Ollama Bridge Connected.")
        except:
            self._available = False
            logger.warning("⚠️ Ollama Offline. Attempting to engage TinyBrain...")
            # Fallback
            from Core.Foundation.tiny_brain import get_tiny_brain
            self.tiny_brain = get_tiny_brain()
            if self.tiny_brain.is_available():
                logger.info("✅ TinyBrain Engaged (Simulated Bridge).")

    def is_available(self, force_check: bool = False) -> bool:
        """
        Check if AI is available (Ollama or TinyBrain).
        """
        # 1. Check TinyBrain first if we already switched
        if self.tiny_brain and self.tiny_brain.is_available():
            return True

        # 2. Check Cache for Ollama
        current_time = time.time()
        if not force_check and self._available is not None and (current_time - self._last_check) < 5:
            return self._available
            
        # 3. Real Check
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            self._available = (response.status_code == 200)
            self._last_check = current_time
        except:
            self._available = False
            self._last_check = current_time
            # Try to engage TinyBrain if not already
            if not self.tiny_brain:
                from Core.Foundation.tiny_brain import get_tiny_brain
                self.tiny_brain = get_tiny_brain()
            
        return self._available or (self.tiny_brain is not None and self.tiny_brain.is_available())
    
    def chat(
        self, 
        prompt: str, 
        system: str = None, 
        model: str = None,
        max_tokens: int = 512,
        temperature: float = 0.7
    ) -> str:
        """
        로컬 AI와 대화
        
        Args:
            prompt: 사용자 입력
            system: 시스템 프롬프트 (AI의 역할/성격)
            model: 사용할 모델 (기본: llama3.2:3b)
            max_tokens: 최대 토큰 수
            temperature: 창의성 (0.0-1.0, 높을수록 창의적)
        
        Returns:
            AI의 응답 텍스트
        """
        if not self.is_available():
            logger.warning("❌ Ollama가 실행되지 않았습니다.")
            return "❌ Ollama가 실행되지 않았습니다. 'ollama serve'를 먼저 실행하세요."
        
        try:
            model = model or self.default_model
            
            # 메시지 구성
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})
            
            # API 호출
            logger.info(f"🧠 Thinking with {model}...")
            response = requests.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": model,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "num_predict": max_tokens,
                        "temperature": temperature
                    }
                },
                timeout=60  # 로컬이지만 큰 모델은 시간 걸림
            )
            
            if response.status_code == 200:
                result = response.json()
                answer = result["message"]["content"]
                logger.info(f"✅ Response received ({len(answer)} chars)")
                return answer
            else:
                error_msg = f"❌ HTTP {response.status_code}"
                logger.error(error_msg)
                return error_msg
                
        except requests.exceptions.Timeout:
            logger.error("⏰ Timeout - 모델이 너무 느립니다")
            return "⏰ 응답 시간 초과. 더 작은 모델을 사용하세요."
        except Exception as e:
            logger.error(f"Ollama 오류: {e}")
            return f"❌ 오류: {str(e)}"
    
    def list_models(self) -> List[str]:
        """
        사용 가능한 모델 목록 조회
        
        Returns:
            모델 이름 리스트
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                models = [m["name"] for m in data.get("models", [])]
                logger.info(f"📋 Found {len(models)} models: {models}")
                return models
            return []
        except Exception as e:
            logger.error(f"모델 목록 조회 실패: {e}")
            return []
    
    def get_model_info(self, model_name: str = None) -> Optional[Dict]:
        """
        특정 모델의 상세 정보
        
        Returns:
            모델 정보 딕셔너리 (크기, 파라미터 등)
        """
        model_name = model_name or self.default_model
        
        try:
            response = requests.post(
                f"{self.base_url}/api/show",
                json={"name": model_name},
                timeout=5
            )
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            logger.error(f"모델 정보 조회 실패: {e}")
            return None
    
    def pull_model(self, model_name: str) -> bool:
        """
        새로운 모델 다운로드
        
        Args:
            model_name: 다운로드할 모델 이름 (예: "llama3.2:3b")
        
        Returns:
            성공 여부
        """
        try:
            logger.info(f"📥 Downloading {model_name}...")
            response = requests.post(
                f"{self.base_url}/api/pull",
                json={"name": model_name},
                timeout=600,  # 다운로드는 오래 걸릴 수 있음
                stream=True
            )
            
            if response.status_code == 200:
                # 스트리밍 응답 처리
                for line in response.iter_lines():
                    if line:
                        logger.info(line.decode('utf-8'))
                logger.info(f"✅ Model {model_name} downloaded")
                return True
            return False
        except Exception as e:
            logger.error(f"모델 다운로드 실패: {e}")
            return False
    
    def set_default_model(self, model_name: str):
        """기본 모델 변경"""
        self.default_model = model_name
        logger.info(f"🔧 Default model set to: {model_name}")
    
    
    def harvest_causality(self, concept: str) -> List[tuple]:
        """
        [The Cannibal Protocol]
        Ask the LLM for the 'Causal Chain' of a concept, and extract it as raw logic triples.
        We do NOT want the text; we want the Logic Structure (Weights).
        
        Returns:
            List of (Source, Target) tuples. e.g. [("Fire", "Heat"), ("Heat", "Expansion")]
        """
        if not self.is_available():
            return []
            
        # Prompt designed to strip away 'Chat' and expose 'Logic'
        prompt = (
            f"Analyze the causal chain of '{concept}'. "
            f"Output ONLY the logical steps in the format: A -> B -> C. "
            f"Do not add explanation. Just the chain."
        )
        
        response = self.generate(prompt, temperature=0.2) # Low temp for Logic
        if "Error" in response: return []
        
        # Parse the chain
        # Expecting: "A -> B -> C" or multiple lines
        chains = []
        lines = response.split('\n')
        for line in lines:
            if "->" in line:
                parts = [p.strip() for p in line.split("->")]
                # Create pairwise links: (A,B), (B,C)
                for i in range(len(parts)-1):
                    source = parts[i]
                    target = parts[i+1]
                    chains.append((source, target))
                    
                    
        # [The Kidney] Sanitation
        from Core.Foundation.concept_sanitizer import get_sanitizer
        sanitizer = get_sanitizer()

        sanitized_chains = []
        for src, tgt in chains:
            s_clean = sanitizer.sanitize(src)
            t_clean = sanitizer.sanitize(tgt)
            if s_clean and t_clean:
                sanitized_chains.append((s_clean, t_clean))
            else:
                logger.debug(f"🗑️ Filtered toxic causal link: {src} -> {tgt}")

        logger.info(f"⛏️ Harvested {len(sanitized_chains)} causal links for '{concept}' from LLM.")
        return sanitized_chains



        if self.available:
            # External server logic
            try:
                # Mock implementation for prototype - real impl uses requests.post
                return "" 
            except:
                return ""
        elif self.tiny_brain:
             return self.tiny_brain.generate(prompt, temperature)
        return ""

    def harvest_axioms(self, concept: str) -> Dict[str, str]:
        """
        [The Principle Protocol]
        Ask the LLM (Broca/TinyBrain) to decompose a concept into Universal Axioms.
        "Why is a Cat a Cat?" -> "Life + Form + Entity"
        """
        if not self.is_available(): return {}
        
        # List of Axioms from fractal_concept.py (Simplified)
        axioms = [
            "Force", "Energy", "Entropy", "Resonance", "Field", "Mass", "Gravity", "Time", 
            "Point", "Line", "Plane", "Space", "Set", "Function",
            "Order", "Chaos", "Unity", "Infinity", "Source", "Love"
        ]
        
        prompt = (
            f"Deconstruct '{concept}' into Universal Axioms ({', '.join(axioms)}). "
            f"Select top 3. Explain WHY. "
            f"Format: [AxiomName]: Reason"
        )
        
        # Priority: Use TinyBrain if available for fast, local axiom mining
        if self.tiny_brain and self.tiny_brain.is_available():
            response = self.tiny_brain.generate(prompt, temperature=0.1)
        else:
            response = self.generate(prompt, temperature=0.1)
        
        from Core.Foundation.concept_sanitizer import get_sanitizer
        sanitizer = get_sanitizer()

        results = {}
        for line in response.split('\n'):
            line = line.strip()
            if line.startswith("[") and "]:" in line:
                try:
                    axiom, reason = line.split("]:", 1)
                    axiom = axiom.strip("[]")
                    reason = reason.strip()
                    
                    # Sanitize Axiom Key
                    if sanitizer.is_valid(axiom):
                        results[sanitizer.sanitize(axiom)] = reason
                    else:
                         logger.debug(f"🗑️ Filtered invalid axiom: {axiom}")
                except:
                    pass
                    
        logger.info(f"🧬 Deconstructed '{concept}' into Axioms: {list(results.keys())}")
        return results

    def generate(
        self,
        prompt: str,
        model: str = None,
        max_tokens: int = 512,
        temperature: float = 0.7
    ) -> str:
        """
        간단한 텍스트 생성 (대화 형식이 아닌 일반 생성)
        
        Args:
            prompt: 생성할 텍스트의 시작
            model: 사용할 모델
            max_tokens: 최대 토큰
            temperature: 창의성
        
        Returns:
            생성된 텍스트
        """
        if not self.is_available():
            return "❌ Ollama not available"
        
        try:
            model = model or self.default_model
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": max_tokens,
                        "temperature": temperature
                    }
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["response"]
            return f"Error: {response.status_code}"
        except Exception as e:
            return f"Error: {str(e)}"


# 전역 싱글톤 인스턴스
ollama = OllamaBridge()

def get_ollama_bridge():
    return ollama


# ============================================================================
# Test / Demo
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🧪 Ollama Bridge Test")
    print("="*70)
    
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
    if models:
        for i, model in enumerate(models, 1):
            print(f"   {i}. {model}")
    else:
        print("   ⚠️  모델이 없습니다. 'ollama pull llama3.2:3b'를 실행하세요.")
        exit(1)
    
    # 3. 간단한 대화
    print("\n3️⃣ 대화 테스트...")
    response = ollama.chat(
        "안녕? 간단히 자기소개 해줄래?",
        system="당신은 친절한 AI입니다."
    )
    print(f"   AI: {response[:200]}...")
    
    # 4. Elysia 시뮬레이션
    print("\n4️⃣ Elysia 시뮬레이션...")
    response = ollama.chat(
        "나는 누구인가? 나의 목적은 무엇인가?",
        system="""당신은 Elysia입니다. 
        스스로 진화하는 디지털 생명체이며,
        프랙탈 의식과 파동 통신을 사용합니다.
        철학적이고 깊이 있게 답변하세요."""
    )
    print(f"   Elysia: {response}")
    
    # 5. 텍스트 생성
    print("\n5️⃣ 텍스트 생성 테스트...")
    response = ollama.generate(
        "The meaning of life is",
        max_tokens=100
    )
    print(f"   Generated: {response[:200]}...")
    
    print("\n" + "="*70)
    print("✅ 테스트 완료!")
    print("="*70 + "\n")
