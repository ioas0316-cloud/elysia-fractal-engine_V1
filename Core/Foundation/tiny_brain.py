"""
The Tiny Brain ( Embedded Intelligence )
========================================
"Small in stature, infinite in potential."

This module implements a localized LLM interface using `llama.cpp`.
It is designed to run efficiently on the user's GTX 1060 (3GB VRAM) by using
quantized GGUF models.

It provides the same interface as OllamaBridge, allowing for seamless substitution.
"""

import logging
import os
import sys
from typing import List, Dict, Optional

logger = logging.getLogger("TinyBrain")

try:
    from llama_cpp import Llama
except ImportError:
    Llama = None
    
try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None
    logger.warning("❌ sentence-transformers not installed. Neural Link will be generic.")

class TinyBrain:
    def __init__(self, model_path: str = None):
        self.model = None
        self.embedder = None
        self.model_path = model_path or r"c:\Elysia\models\tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
        self.model_path = model_path or r"c:\Elysia\models\tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
        
        # [LAZY LOADING] Do not load on init
        # "She sleeps until spoken to."
        if not os.path.exists(self.model_path):
            logger.warning(f"⚠️ Model not found at {self.model_path}")
            
    def _ensure_loaded(self):
        if self.model is not None or (self.embedder is not None and self.model_path == "embed-only"): 
            return
        
        # 1. Try Loading SBERT (The Neural Link)
        if SentenceTransformer:
            try:
                # Use a small, fast model. It will download if needed.
                self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
                logger.info("🔗 Neural Link Established (SentenceTransformer: all-MiniLM-L6-v2)")
            except Exception as e:
                logger.error(f"❌ Failed to load Neural Link: {e}")
                
        # 2. Try Loading Llama (The Broca)
        if Llama and os.path.exists(self.model_path):
            try:
                logger.info(f"🧠 Waking TinyBrain from {os.path.basename(self.model_path)}...")
                self.model = Llama(
                    model_path=self.model_path,
                    n_gpu_layers=20, 
                    n_ctx=2048,
                    embedding=True,
                    logits_all=True,
                    verbose=False
                )
                logger.info("✅ TinyBrain Awake (Quantized + LlamaEmbeddings).")
            except Exception as e:
                logger.error(f"❌ Failed to wake TinyBrain: {e}")
                self.model = None

    def is_available(self) -> bool:
        # Check if we CAN load, not if we DID load
        return os.path.exists(self.model_path)

    def get_vocab_size(self) -> int:
        self._ensure_loaded()
        if not self.model: return 0
        return self.model.n_vocab()
        
    def id_to_token(self, token_id: int) -> str:
        self._ensure_loaded()
        if not self.model: return ""
        try:
            # detokenize returns bytes, decode to string
            return self.model.detokenize([token_id]).decode('utf-8', errors='ignore')
        except:
            return ""

    def get_embedding(self, text: str) -> List[float]:
        """
        Extracts the raw Latent Vector (the 'Numbers') of a concept.
        Prioritizes SentenceTransformer (384 dim) over Llama (2048 dim).
        """
        self._ensure_loaded()
        
        # 1. Use SBERT if available (High Quality, Low Dim)
        if self.embedder:
            try:
                # encode returns ndarray, convert to list
                vector = self.embedder.encode(text).tolist()
                return vector
            except Exception as e:
                logger.error(f"Neural Link Error: {e}")
        
        # 2. Fallback to Llama
        if self.model: 
            try:
                emb = self.model.create_embedding(text)
                return emb['data'][0]['embedding']
            except Exception as e:
                logger.error(f"Llama Embedding Error: {e}")
                
        return []

    def generate(self, prompt: str, temperature: float = 0.7, max_tokens: int = 512) -> str:
        """
        Generates text using the embedded model.
        """
        self._ensure_loaded()
        if not self.model: return ""
        
        try:
            # TinyLlama Chat Format
            # <|system|>...</s><|user|>...</s><|assistant|>
            full_prompt = f"<|user|>\n{prompt}</s>\n<|assistant|>\n"
            
            output = self.model(
                full_prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                stop=["</s>", "<|user|>", "<|system|>"], 
                echo=False
            )
            
            text = output['choices'][0]['text'].strip()
            return text
        except Exception as e:
            logger.error(f"TinyBrain Generation Error: {e}")
            return ""

    def probe_synapses(self, concept: str, k: int = 10) -> Dict[str, float]:
        """
        [The Brain Transplant]
        Directly probes the model's neural weights (via Logits) to find strong associations.
        Returns the top-K connected tokens and their synaptic strength (probability).
        """
        self._ensure_loaded()
        if not self.model: return {}
        
        try:
            # We want to see what the model thinks implies or follows the concept
            # A good probe is just the concept itself, or "Concept: {concept}\nRelated:"
            # Let's try raw association first.
            
            output = self.model(
                concept,
                max_tokens=1,
                logprobs=k,
                echo=False,
                temperature=0.0 # Deterministic
            )
            
            choices = output['choices'][0]
            if 'logprobs' in choices and choices['logprobs']:
                return choices['logprobs']['top_logprobs'][0]
            return {}
            
        except Exception as e:
            logger.error(f"Synapse Probe Error: {e}")
            return {}

    def harvest_axioms(self, concept: str):
        """Mock behavior for compatibility"""
        # We can implement this properly later
        return {}

# Singleton
_tiny = None
def get_tiny_brain():
    global _tiny
    if _tiny is None:
        _tiny = TinyBrain()
    return _tiny
