from typing import Dict, Any, List, Optional, Callable
from .intelligence_line import IntelligenceLine
from .universal_line import UniversalLine
import json
import os

class DynamicIntelligenceFactory:
    """
    Factory for creating Intelligence Lines dynamically.
    It reads 'Material' (Knowledge/Keywords) and 'Logic' (Processing Rules)
    to spawn new forms of intelligence on the fly.
    """

    def __init__(self, material_path: str = "Core/Intelligence/Weaving/materials"):
        self.material_path = material_path
        self._custom_logics: Dict[str, Callable] = {}

    def register_logic(self, name: str, logic_func: Callable):
        """
        Registers a custom logic function that can be used by generated lines.
        """
        self._custom_logics[name] = logic_func

    def create_line(self, name: str, material_file: Optional[str] = None,
                    keywords: Optional[List[str]] = None,
                    logic_type: str = "keyword_density") -> IntelligenceLine:
        """
        Creates a new IntelligenceLine.

        Args:
            name: The name of the intelligence (e.g., "Cooking").
            material_file: Filename in the materials directory (e.g., "cooking.json").
            keywords: Direct list of keywords if no file is used.
            logic_type: The type of logic to use ('keyword_density', 'pattern_match', etc).
        """

        # 1. Load Material (Knowledge)
        final_keywords = keywords or []
        loaded_patterns = {}

        if material_file:
            try:
                # In a real scenario, we'd handle path joining safely
                full_path = os.path.join(self.material_path, material_file)
                if os.path.exists(full_path):
                    with open(full_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        # Expecting structure: {"keywords": [...], "patterns": {...}}
                        final_keywords.extend(data.get("keywords", []))
                        loaded_patterns = data.get("patterns", {})
            except Exception as e:
                print(f"Error loading material {material_file}: {e}")

        # 2. Select Logic (Principle)
        # Default logic is simple keyword density
        # Future: We can attach more complex logic functions here

        return UniversalLine(
            name=name,
            keywords=final_keywords,
            patterns=loaded_patterns,
            logic_type=logic_type
        )

    def load_all_materials(self) -> List[IntelligenceLine]:
        """
        Scans the materials directory and creates a line for each file.
        """
        lines = []
        if not os.path.exists(self.material_path):
            return lines

        for filename in os.listdir(self.material_path):
            if filename.endswith(".json"):
                name = filename.replace(".json", "").capitalize()
                # e.g., "cooking_material.json" -> "Cooking_material" -> clean up name
                name = name.split("_")[0]
                lines.append(self.create_line(name, material_file=filename))
        return lines
