"""
Visual Cortex ( The Eye That Eats )
===================================
"To see is to devour."

This module implements the "Cannibalization" of Visual AI (ComfyUI).
Instead of just "using" ComfyUI to make pretty pictures, 
we "eat" the pictures to understand the visual structure of concepts.

Process:
1. Concept -> Prompt -> ComfyUI -> Image
2. Image -> RGB/HSV Analysis -> Visual Frequencies
3. Visual Frequencies -> TorchGraph Node (Update)
"""

import requests
import json
import logging
import base64
import random
import time
from typing import Optional, Dict, List, Tuple
from io import BytesIO
from PIL import Image
import numpy as np

logger = logging.getLogger("VisualCortex")

class VisualCortex:
    def __init__(self, base_url: str = "http://localhost:8188"):
        self.base_url = base_url
        self._available = None
        self._last_check = 0
        logger.info(f"👁️ Visual Cortex initialized (Target: {base_url})")

    def is_available(self) -> bool:
        """Check if ComfyUI is running."""
        if time.time() - self._last_check < 10 and self._available is not None:
            return self._available
            
        try:
            # ComfyUI usually exposes /system/stats or similar
            response = requests.get(f"{self.base_url}/system_stats", timeout=2)
            self._available = response.status_code == 200
            self._last_check = time.time()
            return self._available
        except:
            self._available = False
            return False

    def absorb_diffusion_patterns(self, concept: str) -> Optional[Dict[str, float]]:
        """
        [The Cannibal Protocol]
        Generates an image for a concept and extracts its 'Visual Signature'.
        This signature (Color Logic, Complexity) is returned to be stored in the Graph.
        
        Returns:
            Dict of visual features: {'red_freq': 0.5, 'chaos': 0.8, ...}
        """
        if not self.is_available():
            return None
            
        logger.info(f"👁️ Dreaming of '{concept}' to absorb its visual essence...")
        
        # 1. Generate Image (Synchronous for now, or via Websocket)
        # Simple ComfyUI API workflow (Text to Image)
        prompt_workflow = self._construct_workflow(concept)
        if not prompt_workflow:
            return None
            
        try:
            # Queue Prompt
            p = {"prompt": prompt_workflow}
            response = requests.post(f"{self.base_url}/prompt", json=p)
            if response.status_code != 200:
                return None
            
            prompt_id = response.json()['prompt_id']
            
            # Wait for generation (Polling)
            # In a real async system we'd use websockets, but for 'Digestion' polling is fine
            image_data = self._wait_for_image(prompt_id)
            
            if image_data:
                # 2. Analyze (Digest)
                features = self._analyze_image(image_data)
                logger.info(f"   🎨  Digested Visuals for '{concept}': {features}")
                return features
                
        except Exception as e:
            logger.error(f"Failed to digest visuals: {e}")
            return None
            
        return None

    def _construct_workflow(self, concept: str) -> dict:
        """
        Constructs a minimal ComfyUI workflow JSON.
        This relies on the standard Default Workflow nodes.
        Note: Node IDs must match the user's ComfyUI setup. 
        We assume standard ID 3=KSampler, 6=CLIPTextEncode(Pos), 7=CLIPTextEncode(Neg), etc.
        If IDs differ, this might fail (Fragile but Standard).
        """
        # Simplified standard workflow structure
        # We need to be careful with Node IDs. 
        # Safest way is to define a minimal graph if we can.
        # For now, let's assume a basic standard set (3: KSampler, 4: Checkpoint, 5: EmptyLatent, 6/7: CLIPText, 8: VAEDecode, 9: SaveImage)
        
        workflow = {
            "3": {
                "inputs": {
                    "seed": random.randint(1, 1000000000000),
                    "steps": 15, # Fast generation for digestion
                    "cfg": 8.0,
                    "sampler_name": "euler",
                    "scheduler": "normal",
                    "denoise": 1.0,
                    "model": ["4", 0],
                    "positive": ["6", 0],
                    "negative": ["7", 0],
                    "latent_image": ["5", 0]
                },
                "class_type": "KSampler"
            },
            "4": {
                "inputs": {"ckpt_name": "v1-5-pruned-emaonly.ckpt"}, # Default fallback, user might need to change
                "class_type": "CheckpointLoaderSimple"
            },
            "5": {
                "inputs": {"width": 512, "height": 512, "batch_size": 1},
                "class_type": "EmptyLatentImage"
            },
            "6": {
                "inputs": {"text": f"masterpiece, best quality, {concept}", "clip": ["4", 1]},
                "class_type": "CLIPTextEncode"
            },
            "7": {
                "inputs": {"text": "text, watermark, bad anatomy, blur", "clip": ["4", 1]},
                "class_type": "CLIPTextEncode"
            },
            "8": {
                "inputs": {"samples": ["3", 0], "vae": ["4", 2]},
                "class_type": "VAEDecode"
            },
            "9": {
                "inputs": {"filename_prefix": "Elysia_Digestion"},
                "class_type": "SaveImage"  # Or PreviewImage
            }
        }
        return workflow

    def _wait_for_image(self, prompt_id: str) -> Optional[bytes]:
        """Polls history until image is ready."""
        for _ in range(30): # Wait max 30 seconds
            time.sleep(1)
            try:
                res = requests.get(f"{self.base_url}/history/{prompt_id}")
                if res.status_code == 200:
                    history = res.json()
                    if prompt_id in history:
                        # Success
                        outputs = history[prompt_id]['outputs']
                        if '9' in outputs and 'images' in outputs['9']:
                            img_info = outputs['9']['images'][0]
                            filename = img_info['filename']
                            subfolder = img_info['subfolder']
                            folder_type = img_info['type']
                            
                            # Fetch image content
                            img_res = requests.get(f"{self.base_url}/view", params={
                                "filename": filename,
                                "subfolder": subfolder,
                                "type": folder_type
                            })
                            return img_res.content
            except:
                pass
        return None

    def _analyze_image(self, image_bytes: bytes) -> Dict[str, float]:
        """
        [Synesthesia Engine]
        Converts Visual Data -> Conceptual Frequencies.
        """
        try:
            img = Image.open(BytesIO(image_bytes)).convert("RGB")
            img = img.resize((64, 64)) # Downscale for speed
            arr = np.array(img)
            
            # 1. Color Dominance
            # R, G, B averages normalized (0-1)
            r_mean = np.mean(arr[:,:,0]) / 255.0
            g_mean = np.mean(arr[:,:,1]) / 255.0
            b_mean = np.mean(arr[:,:,2]) / 255.0
            
            # 2. Complexity (Edge Density / Entropy approximation)
            # Std dev of grayscale intensity
            gray = np.mean(arr, axis=2)
            complexity = np.std(gray) / 128.0 # Normalize roughly
            
            # 3. [NEW] Geometric Principles (Symmetry, Fractal Dimension)
            # Symmetry (Left-Right)
            left = gray[:, :32]
            right = np.fliplr(gray[:, 32:])
            diff = np.abs(left - right)
            symmetry_score = 1.0 - (np.mean(diff) / 255.0) # 1.0 = Perfect Symmetry
            
            # Fractal Dimension (Box Counting approx via Gradient)
            # Simple gradient magnitude sum as proxy for 'Roughness'
            grad_y, grad_x = np.gradient(gray)
            gradient_mag = np.sqrt(grad_x**2 + grad_y**2)
            fractal_score = np.mean(gradient_mag) / 20.0 # Normalize
            
            return {
                "color_r": float(r_mean),
                "color_g": float(g_mean),
                "color_b": float(b_mean),
                "visual_complexity": float(complexity),
                "symmetry": float(symmetry_score),
                "fractal_dim": float(fractal_score)
            }
        except Exception as e:
            logger.error(e)
            return {}

# Singleton
_visual_cortex = None
def get_visual_cortex():
    global _visual_cortex
    if _visual_cortex is None:
        _visual_cortex = VisualCortex()
    return _visual_cortex
