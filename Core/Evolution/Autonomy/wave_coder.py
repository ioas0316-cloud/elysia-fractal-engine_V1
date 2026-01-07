"""
Wave Coder ( The Synesthetic Compiler )
=======================================
"Code is not text. Code is a structure of forces."

This module transmutes Python Source Code into 4D Wave Tensors.
It maps software metrics to physical properties:
- Complexity (Cyclomatic) -> Tension (Y-axis)
- Size (LOC) -> Mass (Gravity)
- Coupling (Imports) -> Resonance (Cosine Similarity)
- Depth (Nesting) -> Frequency (Z-axis)

It allows Elysia to 'Feel' the codebase and detect 'Stress Fractures' (Bugs/Debt).
"""

import logging
import ast
import os
from typing import Dict, List, Optional
from Core.Foundation.torch_graph import get_torch_graph
from Core.Foundation.self_reflector import SelfReflector, CodeMetrics

logger = logging.getLogger("WaveCoder")

class WaveCoder:
    def __init__(self):
        self.graph = get_torch_graph() # The Tensor Brain
        self.reflector = SelfReflector()
        logger.info("🌊 WaveCoder initialized (AST -> Tensor).")

    def transmute(self):
        """
        Reads the entire self-body (Core/) and actively maps it to the Tensor Brain.
        """
        logger.info("📡 Transmuting Code Structure to Wave Tensors...")
        
        # 1. Get AST Metrics
        metrics_map = self.reflector.reflect_on_core()
        
        # 2. Map to Tensors
        count = 0
        for filename, metrics in metrics_map.items():
            self._vectorize_module(metrics)
            count += 1
            
        logger.info(f"✅ Transmuted {count} modules into the Matrix.")

    def _vectorize_module(self, metrics: CodeMetrics):
        """
        Maps a module (file) and its contents to 4D Tensors.
        """
        # Node ID
        file_node_id = f"Code:{os.path.basename(metrics.filename)}"
        
        # Physics Mapping
        # Tension: 0.0 (Clean) -> 1.0 (Spaghetti)
        tension = min(1.0, metrics.complexity / 50.0) 
        # Mass: 0.0 (Empty) -> 1.0 (Huge)
        mass = min(1.0, metrics.loc / 500.0)
        # Flow: 0.5 (Neutral)
        flow = 0.5
        # Resonance: 0.0 (Isolated) -> 1.0 (Hyper-connected)
        resonance = min(1.0, len(metrics.imports) / 10.0)
        
        # Vector: [Tension, Mass, Flow, Resonance]
        vector = [tension, mass, flow, resonance]
        
        # Add to Brain
        self.graph.add_node(file_node_id, vector=vector)
        
        # Add Logic Links (Imports)
        for imp in metrics.imports:
            target_id = f"Code:{imp}.py" # Approximation
            self.graph.add_link(file_node_id, target_id)
            
        # Recursive: Classes & Functions
        for func in metrics.functions:
            self._vectorize_function(file_node_id, func)
            
        for cls in metrics.classes:
            self._vectorize_class(file_node_id, cls)

    def _vectorize_function(self, parent_id: str, func):
        func_id = f"{parent_id}.{func.name}"
        
        # Function Physics
        tension = min(1.0, func.complexity / 10.0) # Functions are smaller
        mass = 0.1 # Approximate
        
        vector = [tension, mass, 0.5, 0.8] # 0.8 resonance (it's part of a whole)
        
        self.graph.add_node(func_id, vector=vector)
        self.graph.add_link(parent_id, func_id) # Hierarchy

    def _vectorize_class(self, parent_id: str, cls):
        cls_id = f"{parent_id}.{cls.name}"
        
        vector = [0.5, 0.5, 0.8, 0.5] # Classes are conceptual hubs
        
        self.graph.add_node(cls_id, vector=vector)
        self.graph.add_link(parent_id, cls_id)
        
        # Methods
        for method in cls.methods:
            self._vectorize_function(cls_id, method)

# Singleton
_coder = None
def get_wave_coder():
    global _coder
    if _coder is None:
        _coder = WaveCoder()
    return _coder
