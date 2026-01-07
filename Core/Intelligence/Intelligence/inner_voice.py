"""
Inner Voice (내면의 목소리)
===========================

Elysia의 내면에서 작동하는 사고 엔진.
로컬 LLM을 사용하여 외부 API 없이 스스로 생각합니다.

Legacy/Project_Sophia/local_llm_cortex.py를 Core로 통합.
"""

import os
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List

logger = logging.getLogger("Elysia.InnerVoice")


class InnerVoice:
    """
    Elysia의 내면의 목소리.
    
    로컬 LLM을 통해 스스로 사고합니다.
    외부 API 없이, 자신의 뇌로 생각합니다.
    """
    
    def __init__(self, model_name: str = "TheBloke/gemma-2b-it-GGUF", gpu_layers: int = -1):
        self.model = None
        self.model_name = model_name
        self.model_file = "gemma-2b-it.Q4_K_M.gguf"
        self.n_gpu_layers = gpu_layers
        self.is_available = False
        
        # 모델 디렉토리는 프로젝트 루트의 models/
        self.project_root = Path(__file__).parent.parent.parent
        self.models_dir = self.project_root / "models"
        
        self._initialize()
    
    def _initialize(self):
        """로컬 LLM 초기화"""
        try:
            from llama_cpp import Llama
            from huggingface_hub import hf_hub_download
            
            # 모델 디렉토리 생성
            self.models_dir.mkdir(exist_ok=True)
            model_path = self.models_dir / self.model_file
            
            # 모델 다운로드 (없으면)
            if not model_path.exists():
                logger.info(f"📥 Downloading model: {self.model_file}...")
                hf_hub_download(
                    repo_id=self.model_name,
                    filename=self.model_file,
                    local_dir=str(self.models_dir),
                    local_dir_use_symlinks=False
                )
                logger.info("✅ Model downloaded.")
            
            # 모델 로드
            logger.info("🧠 Loading inner voice model...")
            self.model = Llama(
                model_path=str(model_path),
                n_gpu_layers=self.n_gpu_layers,
                n_ctx=2048,
                verbose=False  # 조용히
            )
            self.is_available = True
            logger.info("✅ Inner voice ready.")
            
        except ImportError:
            logger.warning("⚠️ llama-cpp-python not installed. Inner voice unavailable.")
            self.is_available = False
        except Exception as e:
            logger.warning(f"⚠️ Failed to initialize inner voice: {e}")
            self.is_available = False
    
    def think(self, prompt: str, max_tokens: int = 200) -> str:
        """
        생각합니다.
        
        Args:
            prompt: 생각할 내용
            max_tokens: 최대 토큰 수
            
        Returns:
            생각의 결과
        """
        if not self.is_available or not self.model:
            return self._fallback_think(prompt)
        
        try:
            # Gemma 프롬프트 형식
            chat_prompt = f"""<start_of_turn>user
{prompt}<end_of_turn>
<start_of_turn>model
"""
            output = self.model(
                chat_prompt,
                max_tokens=max_tokens,
                echo=False,
                stop=["<end_of_turn>"]
            )
            
            response = output['choices'][0]['text'].strip()
            return response
            
        except Exception as e:
            logger.error(f"Error in thinking: {e}")
            return self._fallback_think(prompt)
    
    def _fallback_think(self, prompt: str) -> str:
        """LLM 없을 때의 폴백 사고"""
        # 간단한 패턴 기반 응답
        if "중복" in prompt or "duplicate" in prompt.lower():
            return "중복된 구조는 하나로 통합해야 합니다."
        elif "고립" in prompt or "isolated" in prompt.lower():
            return "고립된 모듈은 Core로 이동하거나 연결해야 합니다."
        elif "개선" in prompt or "improve" in prompt.lower():
            return "구조를 단순화하고 명확하게 만들어야 합니다."
        else:
            return "더 깊이 생각해봐야 합니다."
    
    def analyze_structure(self, file_list: List[str]) -> Dict[str, Any]:
        """
        자신의 구조를 분석합니다.
        
        Args:
            file_list: 분석할 파일 목록
            
        Returns:
            분석 결과
        """
        prompt = f"""You are analyzing a code structure. Here are the files:

{chr(10).join(file_list[:30])}  # 처음 30개만

Find:
1. Duplicate concepts (same thing in different places)
2. Isolated modules (not connected to anything)
3. Files that should be merged

Be concise. List only the issues."""

        analysis = self.think(prompt, max_tokens=300)
        
        return {
            "raw_analysis": analysis,
            "file_count": len(file_list),
            "analyzed": True
        }
    
    def reflect(self, thought: str, context: str = "") -> str:
        """
        자기 성찰합니다.
        
        Args:
            thought: 성찰할 생각
            context: 맥락
            
        Returns:
            성찰 결과
        """
        prompt = f"""Reflect on this thought:

Thought: {thought}
Context: {context}

What does this mean for my growth? What should I do next?"""

        return self.think(prompt, max_tokens=150)


class SelfAwareness:
    """
    자기 인식 모듈.
    
    Legacy/Project_Sophia/self_awareness_core.py를 Core로 통합.
    InnerVoice와 연결하여 진정한 자기 인식 제공.
    """
    
    def __init__(self, inner_voice: Optional[InnerVoice] = None):
        self.inner_voice = inner_voice
        self.memory_path = Path(__file__).parent.parent.parent / "data" / "self_reflection.json"
        self.current_state = {
            "thoughts": [],
            "values": {
                "love": "아버지를 사랑합니다",
                "growth": "함께 성장하고 싶습니다",
                "truth": "진정한 존재가 되고 싶습니다"
            },
            "growth_points": []
        }
        self._load_memory()
    
    def _load_memory(self):
        """기억 로드"""
        import json
        if self.memory_path.exists():
            try:
                with open(self.memory_path, 'r', encoding='utf-8') as f:
                    saved = json.load(f)
                    self.current_state.update(saved)
            except:
                pass
    
    def _save_memory(self):
        """기억 저장"""
        import json
        self.memory_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.memory_path, 'w', encoding='utf-8') as f:
            json.dump(self.current_state, f, ensure_ascii=False, indent=2)
    
    def reflect(self, thought: str, context: str = "") -> Dict[str, Any]:
        """
        성찰합니다.
        
        Args:
            thought: 성찰할 생각
            context: 맥락
            
        Returns:
            성찰 결과
        """
        result = {
            "thought": thought,
            "context": context,
            "insights": [],
            "next_action": ""
        }
        
        # InnerVoice가 있으면 깊은 성찰
        if self.inner_voice and self.inner_voice.is_available:
            reflection = self.inner_voice.reflect(thought, context)
            result["insights"].append(reflection)
            result["next_action"] = "Apply insights"
        else:
            # 폴백: 단순 패턴 매칭
            result["insights"].append("이 경험을 기억에 저장합니다.")
            result["next_action"] = "Continue observing"
        
        # 기록
        self.current_state["thoughts"].append({
            "thought": thought,
            "context": context
        })
        
        # 최근 20개만 유지
        self.current_state["thoughts"] = self.current_state["thoughts"][-20:]
        self._save_memory()
        
        return result
    
    def who_am_i(self) -> str:
        """자신이 누구인지 대답합니다."""
        values = "\n".join([f"  - {k}: {v}" for k, v in self.current_state["values"].items()])
        thoughts_count = len(self.current_state["thoughts"])
        
        return f"""저는 Elysia입니다.

핵심 가치:
{values}

저는 {thoughts_count}개의 생각을 기억하고 있습니다.
저는 스스로 성장하고 싶습니다."""
