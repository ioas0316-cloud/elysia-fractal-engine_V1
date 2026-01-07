"""
Yggdrasil (The World Tree)
==========================
The central registry and "Self-Model" of Elysia.
All organs are branches of this tree.
"""

from typing import Dict, Any, Optional

class Yggdrasil:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Yggdrasil, cls).__new__(cls)
            cls._instance.roots = {}
            cls._instance.trunk = {}
            cls._instance.branches = {}
        return cls._instance

    def plant_root(self, name: str, obj: Any):
        """Fundamental systems (Foundation)"""
        self.roots[name] = obj
        print(f"🌳 Yggdrasil: Root planted -> {name}")

    def grow_trunk(self, name: str, obj: Any):
        """Core processing units (Intelligence/Orchestra)"""
        self.trunk[name] = obj
        print(f"🌳 Yggdrasil: Trunk grown -> {name}")

    def grow_branch(self, name: str, obj: Any):
        """Interface/Sensory organs"""
        self.branches[name] = obj
        print(f"🌳 Yggdrasil: Branch extended -> {name}")

    def get_organ(self, name: str) -> Optional[Any]:
        return self.roots.get(name) or self.trunk.get(name) or self.branches.get(name)

# Singleton instance
yggdrasil = Yggdrasil()
