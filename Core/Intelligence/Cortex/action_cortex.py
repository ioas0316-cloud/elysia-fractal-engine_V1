"""
Action Cortex (행동 피질)
========================

원본: Legacy/Project_Sophia/action_cortex.py
마이그레이션: 2025-12-15

이 모듈은 사용자 요청이나 내부 목표에 따라 어떤 도구를 사용할지 결정합니다.
Wave Principle을 사용하여 도구를 선택하고 LLM으로 파라미터를 추출합니다.
"""
import json
import re
from pathlib import Path
from typing import Dict, Any, Optional

# Updated imports for Core structure
try:
    from Core.Foundation.gemini_api import generate_text
except ImportError:
    generate_text = None

try:
    from tools.kg_manager import KGManager
except ImportError:
    KGManager = None


class ActionCortex:
    """
    The ActionCortex decides which action (tool) to take based on a given prompt
    or internal goal. It uses the Wave Principle on a dedicated tool KG and then
    uses an LLM to extract parameters.
    """

    def __init__(self, tools_kg_path: str = "data/Knowledge/tools_kg.json"):
        self.tools_kg_manager = None
        self.wave_mechanics = None
        
        if KGManager is not None:
            kg_path = Path(tools_kg_path)
            if kg_path.exists():
                self.tools_kg_manager = KGManager(filepath=kg_path)
                try:
                    from Core.Foundation.wave_mechanics import WaveMechanics
                    self.wave_mechanics = WaveMechanics(self.tools_kg_manager)
                except ImportError:
                    pass
        
        self.tool_schemas = self._load_tool_schemas()

    def _load_tool_schemas(self) -> Dict:
        """Loads the schemas for tools that define their parameters."""
        return {
            "read_file": {
                "description": "Reads the content of a specified file.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filepath": {
                            "type": "string",
                            "description": "The path to the file that needs to be read.",
                        }
                    },
                    "required": ["filepath"],
                },
            },
            "http_request": {
                "description": "Fetches a URL and returns a simple summary.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "url": {"type": "string", "description": "URL to fetch"}
                    },
                    "required": ["url"]
                }
            },
            "check_vital_signs": {
                "description": "Checks the system's status (CPU, Memory).",
                "parameters": {"type": "object", "properties": {}, "required": []}
            },
            "move_cursor": {
                "description": "Moves the mouse cursor to a specific position.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {"type": "string", "enum": ["move", "click", "right_click"], "default": "move"},
                        "x": {"type": "integer", "description": "X coordinate"},
                        "y": {"type": "integer", "description": "Y coordinate"},
                        "duration": {"type": "number", "default": 0.5}
                    },
                    "required": ["x", "y"]
                }
            },
            "type_text": {
                "description": "Types text using the keyboard.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "Text to type"}
                    },
                    "required": ["text"]
                }
            }
        }

    def _find_best_tool(self, prompt: str) -> Optional[str]:
        """Uses the Wave Principle to find the most relevant tool."""
        # Manual override for common patterns
        if "마우스" in prompt or "mouse" in prompt or "cursor" in prompt:
            return "move_cursor"
        if "키보드" in prompt or "type" in prompt or "keyboard" in prompt:
            return "type_text"
        if "상태" in prompt or "status" in prompt or "cpu" in prompt:
            return "check_vital_signs"
        if "읽" in prompt or "read" in prompt or "file" in prompt:
            return "read_file"
        if "url" in prompt.lower() or "http" in prompt.lower():
            return "http_request"

        # Wave-based selection if available
        if self.wave_mechanics and self.tools_kg_manager:
            prompt_tokens = set(re.findall(r'\w+', prompt.lower()))
            all_node_ids = {node['id'] for node in self.tools_kg_manager.kg.get('nodes', [])}
            stimulus_nodes = prompt_tokens.intersection(all_node_ids)
            
            if stimulus_nodes:
                final_echo = {}
                for start_node in stimulus_nodes:
                    echo = self.wave_mechanics.spread_activation(start_node)
                    for node, energy in echo.items():
                        final_echo[node] = final_echo.get(node, 0) + energy

                tool_ids = set(self.tool_schemas.keys())
                tool_echo = {n: e for n, e in final_echo.items() if n in tool_ids}
                if tool_echo:
                    return max(tool_echo, key=tool_echo.get)

        return None

    def _extract_parameters(self, prompt: str, tool_name: str) -> Dict[str, Any]:
        """Uses LLM to extract parameters for a given tool from the prompt."""
        schema = self.tool_schemas.get(tool_name)
        if not schema or generate_text is None:
            return {}

        extraction_prompt = f"""
Given the user's prompt and the tool schema, extract the required parameters.
Respond with a JSON object containing the parameters.

User Prompt: "{prompt}"
Tool: "{tool_name}"
Schema: {json.dumps(schema, indent=2, ensure_ascii=False)}

Extracted parameters (JSON only):
"""
        try:
            response_text = generate_text(extraction_prompt)
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
        except Exception as e:
            print(f"[ActionCortex] Error during parameter extraction: {e}")
        return {}

    def decide_action(self, prompt: str) -> Optional[Dict[str, Any]]:
        """
        Based on the prompt, decide which tool to use and what parameters to use.
        
        Returns:
            {"tool_name": str, "parameters": dict} or None
        """
        print(f"[ActionCortex] Deciding action for: {prompt}")
        
        best_tool = self._find_best_tool(prompt)
        if not best_tool:
            print("[ActionCortex] No relevant tool found.")
            return None

        print(f"[ActionCortex] Best tool: {best_tool}")
        parameters = self._extract_parameters(prompt, best_tool)

        return {
            "tool_name": best_tool,
            "parameters": parameters
        }


# Singleton
_action_cortex: Optional[ActionCortex] = None

def get_action_cortex() -> ActionCortex:
    global _action_cortex
    if _action_cortex is None:
        _action_cortex = ActionCortex()
    return _action_cortex
