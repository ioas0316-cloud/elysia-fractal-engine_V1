"""
THE MIRROR OF CAUSALITY: VARIABLE MESH
======================================

"Life is not a line, but a mesh. Pull one thread, and the whole web trembles."

This module models the complex interdependence of daily life variables.
It replaces linear cause-and-effect with a state-graph system.
"""

import math
from dataclasses import dataclass, field
from typing import Dict, List, Any, Callable

@dataclass
class LifeVariable:
    name: str
    value: float # 0.0 to 1.0
    description: str
    is_hidden: bool = False
    decay_rate: float = 0.0 # Entropy per turn
    
    # Dependencies: List of dicts for complex logic
    # { "source": "Heat", "weight": 0.5, "type": "linear"|"sigmoid"|"threshold", "params": {} }
    dependencies: List[Dict[str, Any]] = field(default_factory=list)

class VariableMesh:
    def __init__(self):
        self.variables: Dict[str, LifeVariable] = {}
        self.chaos_factor: float = 0.0 # Global instability
        
    def add_variable(self, name: str, value: float, desc: str, hidden: bool = False, decay: float = 0.0):
        self.variables[name] = LifeVariable(name, value, desc, hidden, decay)
        
    def add_dependency(self, target: str, source: str, weight: float, type: str = "linear", params: Dict = None):
        if target in self.variables:
            dep = {
                "source": source, 
                "weight": weight, 
                "type": type, 
                "params": params or {}
            }
            self.variables[target].dependencies.append(dep)
            
    def update_state(self):
        """
        Recalculates State with High-Fidelity Physics.
        Includes: Non-linearity, Thresholds, Entropy.
        """
        snapshot = {k: v.value for k, v in self.variables.items()}
        
        for name, var in self.variables.items():
            # 1. Apply Natural Entropy first
            var.value = max(0.0, var.value - var.decay_rate)
            
            if not var.dependencies:
                continue
                
            total_change = 0.0
            
            for dep in var.dependencies:
                src_val = snapshot.get(dep["source"], 0.0)
                weight = dep["weight"]
                dtype = dep["type"]
                params = dep["params"]
                
                if dtype == "linear":
                    # Simple: Change += Source * Weight
                    # But we usually want Source to drive the Target towards a value, OR be a delta?
                    # Let's assume it's a contributor to the level.
                    # Simplified: Target moves towards weighted sum of inputs?
                    # Current logic: Delta application.
                    total_change += src_val * weight
                    
                elif dtype == "threshold":
                    # If Source > Threshold, apply massive impact
                    threshold = params.get("threshold", 0.8)
                    if src_val > threshold:
                        total_change += weight # Sudden jump/drop
                        
                elif dtype == "sigmoid":
                    # S-Curve: immense impact in middle, low at edges
                    # 1 / (1 + exp(-k*(x-x0)))
                    k = params.get("k", 10)
                    x0 = params.get("x0", 0.5)
                    sigmoid = 1 / (1 + math.exp(-k * (src_val - x0)))
                    total_change += (sigmoid - 0.5) * weight * 2 # Center at 0
            
            # Apply changes (clamped)
            # In a real mesh, we might want "Target = f(Inputs)", not "Target += Inputs"
            # But specific scenario choices apply Deltas directly.
            # Here, the Mesh Physics runs ON TOP of Choice Deltas.
            # So this represents "Environmental Feedback".
            
            var.value = max(0.0, min(1.0, var.value + total_change))

    def calculate_joy(self) -> float:
        """
        High-Fidelity Joy Metric.
        Joy = (Harmony of Visible) * (1 - Chaos)
        """
        if "Joy" in self.variables:
            return self.variables["Joy"].value
            
        total = 0
        count = 0
        for v in self.variables.values():
            if not v.is_hidden and v.name != "Money": # Money doesn't directly buy joy here
                total += v.value
                count += 1
        
        avg = total / max(1, count)
        return avg * (1.0 - self.chaos_factor)

    def get_state_summary(self) -> str:
        lines = []
        for name, var in self.variables.items():
            if not var.is_hidden:
                # ASCII Bar
                bar_len = int(var.value * 10)
                bar = "█" * bar_len + "░" * (10 - bar_len)
                lines.append(f"{name:<15}: {bar} ({var.value:.2f})")
        return "\n".join(lines)
