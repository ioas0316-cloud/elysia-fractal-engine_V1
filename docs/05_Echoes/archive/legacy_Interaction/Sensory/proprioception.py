
"""
Code Proprioception (코드 고유 수용 감각)
=========================================

"I feel my own structure. The weight of legacy code, the flow of new logic."

This module is the "Internal Sense" (Interoception) of Elysia.
It treats the codebase (c:/Elysia) as a biological body to be scanned and felt.
"""

import os
import ast
import time
import logging
from typing import Dict, List, Any
from dataclasses import dataclass

logger = logging.getLogger("Proprioception")

@dataclass
class OrganHealth:
    name: str # File or Directory
    size_bytes: int
    line_count: int
    complexity: int # Cyclomatic or simple logical branching
    status: str # "Healthy", "Inflamed" (Complex), "Dead" (Unused)

class CodeProprioception:
    """
    The sense of one's own code body.
    """
    def __init__(self, root_path: str = "c:/Elysia"):
        self.root_path = root_path
        self.body_map: Dict[str, OrganHealth] = {}
        self.last_scan = 0.0
        
    def feel_body(self) -> Dict[str, Any]:
        """
        Scans the codebase and returns a sensation report.
        """
        current_time = time.time()
        # Scan every 5 minutes or forced
        if current_time - self.last_scan < 300: 
            return self.get_sensation_summary()
            
        logger.info("🧘 Sensing internal structure (Codebase Scan)...")
        self._scan_recursive(self.root_path)
        self.last_scan = current_time
        
        return self.get_sensation_summary()

    def _scan_recursive(self, path: str):
        """Recursively analyzes files."""
        try:
            for entry in os.scandir(path):
                if entry.name.startswith(('.', '__')) or entry.name in ['data', 'logs', 'Archive']:
                    continue # Ignore non-living tissue
                
                full_path = entry.path
                if entry.is_dir():
                    self._scan_recursive(full_path)
                elif entry.name.endswith('.py'):
                    self._analyze_cell(full_path)
        except PermissionError:
            pass

    def _analyze_cell(self, file_path: str):
        """Analyzes a single python file (Cell)."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            lines = len(content.splitlines())
            size = len(content)
            
            # Simple "Pain" metric: Indentation depth + Length
            # Real AST parsing is heavy, so we use heuristics for "Feeling"
            complexity = 0
            if "if " in content: complexity += content.count("if ")
            if "for " in content: complexity += content.count("for ")
            if "while " in content: complexity += content.count("while ")
            
            # Normalize path for ID
            rel_path = os.path.relpath(file_path, self.root_path)
            
            status = "Healthy"
            if lines > 500: status = "Hypertrophy" # (Too Big)
            if complexity > 50: status = "Inflamed" # (Too Complex)
            
            self.body_map[rel_path] = OrganHealth(
                name=rel_path,
                size_bytes=size,
                line_count=lines,
                complexity=complexity,
                status=status
            )
            
        except Exception as e:
            logger.warning(f"Failed to sense {file_path}: {e}")

    def get_sensation_summary(self) -> Dict[str, Any]:
        """Returns the 'Feeling' of the body."""
        total_lines = sum(o.line_count for o in self.body_map.values())
        total_complexity = sum(o.complexity for o in self.body_map.values())
        inflamed_organs = [o.name for o in self.body_map.values() if o.status == "Inflamed"]
        
        return {
            "total_lines": total_lines,
            "total_complexity": total_complexity,
            "pain_points": inflamed_organs,
            "health_index": 1.0 - (len(inflamed_organs) / len(self.body_map) if self.body_map else 0)
        }
