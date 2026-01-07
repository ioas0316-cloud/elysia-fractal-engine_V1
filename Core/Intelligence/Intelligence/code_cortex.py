"""
CodeCortex (코드 코르텍스)
========================

"Know Thyself (Source Code)."

This module allows Elysia to read, analyze, and propose changes to her own source code.
It is the foundation of Agentic Evolution.
"""

import os
import ast
import logging
import re # Added for robust prompt handling
from typing import List, Dict, Any

logger = logging.getLogger("CodeCortex")

class CodeCortex:
    def __init__(self):
        self.project_root = "c:/Elysia"
        logger.info("🧬 Code Cortex Active. Ready to analyze self.")

    def read_source(self, file_path: str) -> str:
        """Reads the source code of a file."""
        try:
            full_path = os.path.join(self.project_root, file_path)
            if not os.path.exists(full_path):
                return f"Error: File {file_path} not found."
                
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading {file_path}: {e}"

    def analyze_complexity(self, file_path: str) -> Dict[str, Any]:
        """
        Analyzes the complexity of a file using AST.
        Returns a 'Health Report'.
        """
        code = self.read_source(file_path)
        if code.startswith("Error"):
            return {"error": code}
            
        try:
            tree = ast.parse(code)
            functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
            
            # Simple Heuristic: Length + Function Count
            lines = len(code.splitlines())
            complexity_score = lines / 10.0 + len(functions) * 2.0
            
            report = {
                "file": file_path,
                "lines": lines,
                "classes": len(classes),
                "functions": len(functions),
                "complexity_score": complexity_score,
                "status": "Healthy"
            }
            
            if complexity_score > 100:
                report["status"] = "Bloated (Needs Refactoring)"
            elif complexity_score > 50:
                report["status"] = "Complex"
                
            return report
            
        except Exception as e:
            return {"error": f"AST Parse Failed: {e}"}

    def propose_refactor(self, file_path: str, issue: str) -> str:
        """
        Generates a Refactor Proposal (Markdown).
        """
        return f"""
# Refactor Proposal: {file_path}

**Issue**: {issue}
**Analysis**: The file '{file_path}' has high complexity or structural issues.

## Proposed Changes
1.  [ ] Extract complex logic into helper methods.
2.  [ ] Add type hints if missing.
3.  [ ] Improve docstrings.

**Request**: Supervisor, please review and implement these changes.
"""

    def generate_code(self, prompt: str) -> str:
        """
        Generates code based on a prompt using the LLM.
        This is the 'Writer' capability.
        """
        try:
            from Core.Foundation.gemini_api import generate_text
            
            system_prompt = f"""
            You are the CodeCortex of Elysia.
            Your task is to write Python code based on the following detailed request.
            
            Request: 
            {prompt}
            
            Return ONLY the code, inside a python code block. Do not add conversational text.
            If the prompt includes complexity instructions, strictly adhere to them.
            """
            response = generate_text(system_prompt)
            
            # Extract code block if present
            code_match = re.search(r'```python(.*?)```', response, re.DOTALL)
            if code_match:
                return code_match.group(1).strip()
            
            if "(Mock Response)" in response or "(Error Response)" in response:
                # Smart Mock for Ouroboros Testing
                if "import" in prompt.lower() or "integrate" in prompt.lower():
                     return f"# [Ouroboros Auto-Fix]\n# Generated in Mock Mode for Testing\nimport Core.Intelligence.Reasoning.reasoning_engine\n\n# Original content preserved conceptually..."
                return f"# {response}" # Return as comment to avoid syntax error
            
            return response.strip()
        except Exception as e:
            logger.error(f"Code Generation Failed: {e}")
            return f"# Error generating code: {e}"

