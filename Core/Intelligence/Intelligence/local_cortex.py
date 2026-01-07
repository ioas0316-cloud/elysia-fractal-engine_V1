"""
Local Cortex (The Deep Mind)
============================

"I think, therefore I am locally hosted."

This module interfaces with local Large Language Models (LLMs) via llama_cpp.
It allows Elysia to perform "Deep Thought" - complex reasoning, code generation,
and detailed analysis without relying on external APIs.
"""

import logging
import os
import glob
from typing import List, Optional

logger = logging.getLogger("LocalCortex")

try:
    from llama_cpp import Llama
    HAS_LLAMA = True
except ImportError:
    HAS_LLAMA = False
    logger.warning("⚠️ llama_cpp not found. Local Cortex disabled.")

class LocalCortex:
    def __init__(self, models_dir: str = "c:/Elysia/models"):
        self.models_dir = models_dir
        self.active_model = None
        self.model_name = None
        
        logger.info("🧠 Local Cortex Initialized")
        self.available_models = self.list_models()
        logger.info(f"   Found {len(self.available_models)} models: {self.available_models}")

    def list_models(self) -> List[str]:
        """Lists available .gguf models in the models directory."""
        if not os.path.exists(self.models_dir):
            return []
        
        files = glob.glob(os.path.join(self.models_dir, "*.gguf"))
        return [os.path.basename(f) for f in files]

    def load_model(self, model_name: str):
        """Loads a specific model into memory."""
        if not HAS_LLAMA:
            return False
            
        if self.model_name == model_name:
            return True # Already loaded
            
        path = os.path.join(self.models_dir, model_name)
        if not os.path.exists(path):
            logger.error(f"Model not found: {path}")
            return False
            
        try:
            logger.info(f"   📥 Loading Model: {model_name}...")
            # Adjust n_ctx (context window) and n_gpu_layers as needed
            self.active_model = Llama(
                model_path=path,
                n_ctx=4096,
                n_gpu_layers=-1, # Offload all to GPU if possible
                verbose=False
            )
            self.model_name = model_name
            logger.info(f"   ✅ Model Loaded Successfully.")
            return True
        except Exception as e:
            logger.error(f"   ❌ Failed to load model: {e}")
            return False

    def infer(self, prompt: str, model_name: str = None, max_tokens: int = 512) -> str:
        """
        Runs inference on the local model.
        """
        if not HAS_LLAMA:
            return "Local Cortex Unavailable (llama_cpp missing)."
            
        # Auto-select model if not specified
        if not model_name:
            if self.model_name:
                model_name = self.model_name
            elif self.available_models:
                # Prefer Llama-3 if available
                llama3 = next((m for m in self.available_models if "Llama-3" in m), None)
                model_name = llama3 if llama3 else self.available_models[0]
            else:
                return "No models available."
                
        # Load if needed
        if self.model_name != model_name:
            if not self.load_model(model_name):
                return f"Failed to load {model_name}"
                
        try:
            logger.info(f"   🧠 Deep Thinking with {model_name}...")
            output = self.active_model(
                prompt,
                max_tokens=max_tokens,
                stop=["User:", "\n\n"],
                echo=False
            )
            text = output['choices'][0]['text'].strip()
            return text
        except Exception as e:
            logger.error(f"Inference failed: {e}")
            return f"Error: {e}"

    def unload(self):
        """Unloads the model to free up RAM/VRAM."""
        self.active_model = None
        self.model_name = None
        logger.info("   📤 Model Unloaded.")
