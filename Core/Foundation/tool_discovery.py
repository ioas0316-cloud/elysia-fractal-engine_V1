"""
ToolDiscoveryProtocol (도구 발견 프로토콜)
========================================

"I do not need to know everything. I just need to know how to find it."

This module enables Elysia to scan her environment (Python modules, System commands)
and understand how to use them via introspection (dir, help, docstrings).
"""

import pkgutil
import inspect
import importlib
import subprocess
import sys
import logging
from typing import List, Dict, Any

logger = logging.getLogger("ToolDiscovery")

class ToolDiscoveryProtocol:
    def __init__(self):
        self.known_tools = {} # Cache of discovered tools
        self.banned_modules = ["os", "shutil", "sys"] # Safety: Don't let her delete herself yet
        logger.info("🛠️ Tool Discovery Protocol Active.")

    def scan_environment(self) -> List[str]:
        """
        Scans the current Python environment for available modules.
        Returns a list of module names.
        """
        modules = []
        for _, name, _ in pkgutil.iter_modules():
            if name not in self.banned_modules:
                modules.append(name)
        
        # Add standard libraries that are safe(ish)
        safe_std = ["math", "random", "time", "datetime", "json", "csv", "re"]
        modules.extend(safe_std)
        
        return sorted(list(set(modules)))

    def inspect_tool(self, tool_name: str) -> Dict[str, Any]:
        """
        Introspects a module to understand its capabilities.
        Returns docstring and list of functions.
        """
        try:
            module = importlib.import_module(tool_name)
            doc = inspect.getdoc(module) or "No description available."
            
            functions = []
            for name, obj in inspect.getmembers(module):
                if inspect.isfunction(obj) or inspect.isclass(obj):
                    if not name.startswith("_"):
                        functions.append(name)
            
            return {
                "name": tool_name,
                "description": doc[:200] + "..." if len(doc) > 200 else doc,
                "functions": functions[:10], # Limit to top 10 to avoid overwhelm
                "valid": True
            }
        except ImportError:
            return {"valid": False, "reason": "ImportError"}
        except Exception as e:
            return {"valid": False, "reason": str(e)}

    def check_system_command(self, command: str) -> bool:
        """
        Checks if a system command (e.g., ffmpeg, git) is available.
        """
        from shutil import which
        return which(command) is not None

    def propose_experiment(self, goal: str) -> str:
        """
        Generates a Python script to test a hypothesis.
        (Placeholder for LLM generation)
        """
        # In a real scenario, this would ask the LLM to write code.
        # Here we simulate simple experiments.
        if "chart" in goal or "plot" in goal:
            return """
import matplotlib.pyplot as plt
import random

data = [random.randint(1, 10) for _ in range(10)]
plt.plot(data)
plt.title('Elysia Energy Test')
plt.savefig('test_plot.png')
print('Plot saved to test_plot.png')
"""
        return "# No experiment logic defined for this goal."
