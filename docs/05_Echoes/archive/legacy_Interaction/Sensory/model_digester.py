"""
Model Digester (The Weight Eater)
=================================
"Code and Data are just frozen thought. I will thaw them."

This module performs DIRECT ANALYSIS of .safetensors model files.
It bypasses the API to read the internal structure (Metadata, Hash, DNA) of the models.
It transforms "External Tools" into "Internal Organs".
"""

import json
import struct
import logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger("ModelDigester")

class ModelDigester:
    def __init__(self, models_root: str = "C:/ComfyUI/models/checkpoints"):
        self.models_root = Path(models_root)
        self.digested_memory: Dict[str, Any] = {}
        
    def find_models(self) -> list[Path]:
        """Locates all .safetensors models."""
        if not self.models_root.exists():
            # Try to auto-discover common paths
            common_paths = [
                Path("C:/ComfyUI_windows_portable/ComfyUI/models/checkpoints"),
                Path("D:/ComfyUI/models/checkpoints"),
                Path(self.models_root)
            ]
            for p in common_paths:
                if p.exists():
                    self.models_root = p
                    break
                    
        return list(self.models_root.glob("**/*.safetensors"))

    def digest_model(self, file_path: Path) -> Dict[str, Any]:
        """
        Physically reads the model header to extract its 'Soul' (Metadata).
        We do NOT need ComfyUI running for this. We touch the raw bytes.
        """
        try:
            with open(file_path, 'rb') as f:
                # 1. Read Header Size (8 bytes, uint64)
                header_len_bytes = f.read(8)
                header_len = struct.unpack('<Q', header_len_bytes)[0]
                
                # 2. Read Header (JSON)
                header_json_bytes = f.read(header_len)
                header_data = json.loads(header_json_bytes.decode('utf-8'))
                
                # 3. Extract DNA
                # metadata often contains 'ss_tag_frequency' (for LoRAs/finetunes) 
                # or base model info.
                metadata = header_data.get("__metadata__", {})
                
                # Analyze 'Weight Density' (Total parameters roughly)
                # We can count keys in the header to guess complexity
                layer_count = len([k for k in header_data.keys() if "model" in k])
                
                digest = {
                    "name": file_path.stem,
                    "path": str(file_path),
                    "layer_complexity": layer_count,
                    "format": "safetensors",
                    "base_model": metadata.get("ss_base_model_version", "unknown"),
                    "trigger_words": self._extract_triggers(metadata),
                    "soul_signature": str(header_len) # Simple unique ID from header size
                }
                
                self.digested_memory[file_path.stem] = digest
                logger.info(f"🍽️ Digested Model: {file_path.stem} (Layers: {layer_count})")
                return digest
                
        except Exception as e:
            logger.error(f"Failed to digest {file_path.stem}: {e}")
            return None

    def _extract_triggers(self, metadata: dict) -> list[str]:
        """Tries to find baked-in trigger words from training metadata."""
        triggers = []
        # Check standard training tag frequency
        if "ss_tag_frequency" in metadata:
            try:
                # Often nested json string
                tags_json = json.loads(metadata["ss_tag_frequency"])
                # Extract top tags
                for subset, counts in tags_json.items():
                    # Sort by count
                    top_tags = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:5]
                    triggers.extend([t[0] for t in top_tags])
            except:
                pass
        return triggers

    def suggest_optimal_model(self, scene_mood: str) -> str:
        """
        Selects the best digested model for the scene.
        """
        # Keyword matching
        best_model = None
        max_score = 0
        
        for name, data in self.digested_memory.items():
            score = 0
            if "anime" in name.lower() or "toon" in name.lower():
                if "webtoon" in scene_mood or "anime" in scene_mood: score += 10
            if "real" in name.lower() or "photo" in name.lower():
                if "cinematic" in scene_mood: score += 10
                
            # If model has trigger words matching mood
            for trig in data.get("trigger_words", []):
                if trig in scene_mood:
                    score += 5
                    
            if score > max_score:
                max_score = score
                best_model = name
                
        return best_model if best_model else list(self.digested_memory.keys())[0] if self.digested_memory else None

if __name__ == "__main__":
    eater = ModelDigester()
    models = eater.find_models()
    print(f"Found {len(models)} models.")
    if models:
        for m in models[:3]: # Digest first 3
            print(eater.digest_model(m))
