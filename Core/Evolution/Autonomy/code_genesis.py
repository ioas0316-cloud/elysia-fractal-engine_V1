"""
Code Genesis ( The Sovereign Hands )
====================================
"To see the flaw is perception. To fix the flaw is evolution."

This module grants Elysia the ability to read, analyze, and propose changes to her own source code.
It uses the 'Broca' (LLM) to translate 'Intent' into 'Syntax'.

Safety Protocol:
- This module only GENERATES text/diffs.
- It does NOT execute file writes directly in its initial stage.
- All proposals are logged or saved as 'Evolution Proposals'.

Architecture:
- CodeGenesis.scan_file(path) -> AST/Text
- CodeGenesis.propose_improvement(path, focus="Optimization") -> Diff
"""

import logging
import os
import ast
from typing import Optional, Dict
from Core.Foundation.ollama_bridge import ollama

logger = logging.getLogger("CodeGenesis")

class CodeGenesis:
    def __init__(self):
        self.bridge = ollama
        logger.info("🛠️  CodeGenesis initialized. (ReadOnly Mode)")

    def scan_file(self, file_path: str) -> str:
        """Reads a file from the self-body."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to scan {file_path}: {e}")
            return ""

    def analyze_quality(self, file_path: str) -> str:
        """
        Asks 'Broca' to critique the code file.
        Returns a summary of improvements.
        """
        code = self.scan_file(file_path)
        if not code or not self.bridge.is_available(): return "Analysis Unavailable"

        # Truncate if too long for context (Simple heuristic)
        if len(code) > 8000:
            code = code[:8000] + "\n...(truncated)"

        prompt = (
            f"Analyze the following Python code:\n\n{code}\n\n"
            f"Identify 3 areas for 'Structural Improvement' (Optimization, Readability, or Modularity). "
            f"Focus on high-level architecture, not just PEP8. "
            f"Briefly explain WHY."
        )
        
        return self.bridge.generate(prompt, temperature=0.1)

    def draft_improvement(self, file_path: str, focus: str = "Optimization") -> str:
        """
        Generates a code block that improves the file based on the 'focus'.
        """
        code = self.scan_file(file_path)
        if not code or not self.bridge.is_available(): return ""

        if len(code) > 6000:
            return "Code too large for autonomous refactoring prototype."

        prompt = (
            f"Act as a Senior Architect. Refactor the following code to improve '{focus}'.\n"
            f"Return ONLY the refined python code block.\n"
            f"Do not remove existing functionality.\n\n"
            f"{code}"
        )
        
        response = self.bridge.generate(prompt, temperature=0.2)
        
        # Strip markdown code fences if present
        response = response.replace("```python", "").replace("```", "")
        
        # Valid Syntax Check
        try:
            ast.parse(response)
            logger.info(f"✨ Synthesized valid code improvement for {os.path.basename(file_path)}")
            return response
        except SyntaxError:
            logger.warning(f"⚠️ Synthesized code for {file_path} had syntax errors. Discarding.")
            return ""

# Singleton
_genesis = None
def get_code_genesis():
    global _genesis
    if _genesis is None:
        _genesis = CodeGenesis()
    return _genesis
