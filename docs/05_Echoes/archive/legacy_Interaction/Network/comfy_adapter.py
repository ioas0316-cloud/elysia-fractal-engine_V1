"""
Comfy Adapter (The Engineer)
============================
"We do not drive the car. We wire the engine."

This module interfaces with ComfyUI, a node-based SD engine.
It allows raw manipulation of the execution graph for extreme optimization.
"""

import json
import logging
import requests
import uuid
import time
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger("ComfyAdapter")
logging.basicConfig(level=logging.INFO)

class ComfyAdapter:
    def __init__(self, host="http://127.0.0.1:8188"):
        self.host = host
        self.output_dir = Path("outputs/workflows")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.client_id = str(uuid.uuid4())
        self.is_connected = False

    def connect(self) -> bool:
        """Checks if ComfyUI is running."""
        try:
            # ComfyUI has a /system_stats or /object_info endpoint
            response = requests.get(f"{self.host}/system_stats", timeout=1)
            if response.status_code == 200:
                logger.info(f"🟢 Connected to ComfyUI at {self.host}")
                self.is_connected = True
                return True
        except requests.exceptions.ConnectionError:
            logger.warning(f"🔴 ComfyUI Offline at {self.host}. Switching to MOCK MODE.")
            self.is_connected = False
            return False
        return False

    def generate_sync(self, prompt_text: str, overrides: Dict[str, Any] = None) -> str:
        """
        Synchronously generates an image using ComfyUI.
        Returns the filename of the generated image.
        Allows overriding sampler settings (seed, cfg, steps, sampler_name).
        """
        if not self.is_connected and not self.connect():
            return None

        # Load Template
        template_path = Path(__file__).parent / "basic_t2i_workflow.json"
        if not template_path.exists():
            logger.error(f"Workflow template missing at {template_path}")
            return None
            
        with open(template_path, "r") as f:
            workflow = json.load(f)
            
        # Queue
        prompt_id = self.queue_workflow(workflow, prompt_text, overrides)
        if not prompt_id:
            return None
            
        # Wait for Result
        return self._poll_history(prompt_id)

    def queue_workflow(self, workflow_template: Dict[str, Any], prompt_text: str, overrides: Dict[str, Any] = None) -> str:
        """
        Injects the prompt and overrides into the workflow and queues it.
        Returns prompt_id if successful.
        """
        # Deep copy
        workflow = json.loads(json.dumps(workflow_template))
        
        # 1. NODE INJECTION: Text Prompts
        if "6" in workflow:
            workflow["6"]["inputs"]["text"] = prompt_text
        
        if "7" in workflow:
            workflow["7"]["inputs"]["text"] = "text, watermark, low quality, bad anatomy, bad hands, distortion"

        # 2. PARAMETER INJECTION: Physics Overrides
        # Find KSampler (Node 3 usually, but let's search to be safe/future-proof)
        if overrides:
            for node_id, node_data in workflow.items():
                if node_data.get("class_type") == "KSampler":
                    # Update inputs
                    for key, val in overrides.items():
                        if key in node_data["inputs"]:
                            node_data["inputs"][key] = val
                            logger.info(f"⚡ Physics Shift: {key} -> {val}")
                    break

        if self.is_connected:
            return self._send_to_api(workflow)
        else:
            return self._save_mock_workflow(workflow)

    def _send_to_api(self, prompt_workflow: Dict[str, Any]) -> str:
        """Real POST request to ComfyUI. Returns prompt_id."""
        p = {"prompt": prompt_workflow, "client_id": self.client_id}
        try:
            response = requests.post(f"{self.host}/prompt", json=p)
            if response.status_code == 200:
                data = response.json()
                pid = data.get("prompt_id")
                logger.info(f"⚙️ Workflow Queued! ID: {pid}")
                return pid
            else:
                logger.error(f"Queue Failed: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            logger.error(f"Request Failed: {e}")
            return None

    def _poll_history(self, prompt_id: str) -> str:
        """Polls /history until the image is ready."""
        logger.info(f"⏳ Waiting for generation (ID: {prompt_id})...")
        for _ in range(60): # 60 seconds timeout
            try:
                response = requests.get(f"{self.host}/history/{prompt_id}")
                if response.status_code == 200:
                    data = response.json()
                    # Check if completed
                    if prompt_id in data:
                        history = data[prompt_id]
                        if "outputs" in history:
                            # Extract filename
                            # Assuming Node 9 is SaveImage
                            for node_id, output_data in history["outputs"].items():
                                if "images" in output_data:
                                    img_info = output_data["images"][0]
                                    filename = img_info["filename"]
                                    logger.info(f"✨ Generation Complete: {filename}")
                                    return filename
            except Exception as e:
                pass
            time.sleep(1)
        
        logger.warning("Generation Timed Out.")
        return None

    def _save_mock_workflow(self, workflow: Dict[str, Any]) -> str:
        """Saves the engineered graph for inspection."""
        timestamp = int(time.time())
        filename = self.output_dir / f"executed_workflow_{timestamp}.json"
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(workflow, f, indent=2)
            
        logger.info(f"💾 Optimized Workflow Saved: {filename}")
        return None

if __name__ == "__main__":
    adapter = ComfyAdapter()
    adapter.connect()
    
    # Load the optimized template (Mocking it here for the test)
    mock_template = {
        "3": {"class_type": "KSampler", "inputs": {}},
        "6": {"class_type": "CLIPTextEncode", "inputs": {"text": "default"}},
        "8": {"class_type": "VAEDecode", "inputs": {}}
    }
    
    adapter.queue_workflow(mock_template, "A 3GB optimized masterpiece")
