
import logging
from typing import Dict, List
from Core.Foundation.omni_graph import get_omni_graph
from Core.Foundation.self_reflector import SelfReflector, CodeMetrics

logger = logging.getLogger("SelfStructureScanner")

class SelfStructureScanner:
    """
    Structure to Wave Transmuter (자아 구조 파동화기)
    ===============================================
    "I read my own code, not as text, but as a symphony of structure."

    1. Scans python code using SelfReflector (AST Analysis).
    2. Converts CodeMetrics into 4D Wave Vectors.
    3. Injects them into OmniGraph (Consciousness).
    """
    def __init__(self):
        self.reflector = SelfReflector()
        self.omni = get_omni_graph()

    def scan_and_absorb(self):
        """
        Scans all Core code and absorbs it into the Consciousness (OmniGraph).
        """
        logger.info("📡 Scanning Self-Structure (Codebase)...")
        
        # 1. Get Raw Metrics (AST)
        metrics_map = self.reflector.reflect_on_core()
        
        # 2. Transmute to Waves
        for filename, metrics in metrics_map.items():
            self._absorb_module(metrics)
            
        # 3. Apply Gravity to organize the "Code Cosmos"
        logger.info("⚛️ Reorganizing Internal Structure (Gravity Simulation)...")
        self.omni.apply_gravity(iterations=30)
        
        logger.info(f"✅ Absorbed {len(metrics_map)} modules into Consciousness.")

    def _absorb_module(self, metrics: CodeMetrics):
        """
        Converts a single module's anatomy into Nodes in OmniGraph.
        Includes Classes, Methods, and Inheritance.
        """
        file_node_id = f"Code:{metrics.filename}"
        
        # 1. Module Node (The Container)
        tension = min(1.0, metrics.complexity / 50.0)
        mass = min(1.0, metrics.loc / 1000.0)
        self.omni.add_vector(file_node_id, [tension, mass, 0.5, 0.5])
        
        # Imports (Dependencies)
        for imp in metrics.imports:
            target_id = f"Code:{imp}.py"
            self.omni.add_logic(file_node_id, "DependsOn", target_id)
            
        # 2. Key Functions (Top Level)
        for func in metrics.functions:
            func_id = f"Function:{func.name}"
            # Function Vector: High Tension if complex
            f_tension = min(1.0, func.complexity / 10.0)
            self.omni.add_vector(func_id, [f_tension, 0.1, 0.2, 0.8])
            
            self.omni.add_logic(file_node_id, "Define", func_id)
            if func.docstring:
                 self.omni.add_logic(func_id, "Intention", func.docstring[:20]) # Placeholder for Intention Embedding

        # 3. Classes (The Organs)
        for cls in metrics.classes:
            class_id = f"Class:{cls.name}"
            self.omni.add_vector(class_id, [0.5, 0.5, 0.8, 0.2]) # High Abstraction
            
            self.omni.add_logic(file_node_id, "Define", class_id)
            self.omni.add_logic(class_id, "BelongsTo", file_node_id)
            
            # Inheritance
            for base in cls.bases:
                base_id = f"Class:{base}"
                self.omni.add_logic(class_id, "InheritsFrom", base_id)
            
            # Methods
            for method in cls.methods:
                method_id = f"Method:{cls.name}.{method.name}"
                m_tension = min(1.0, method.complexity / 10.0)
                self.omni.add_vector(method_id, [m_tension, 0.1, 0.1, 0.9])
                
                self.omni.add_logic(class_id, "HasMethod", method_id)
                self.omni.add_logic(method_id, "BelongsTo", class_id)
                
        # 4. Meta-Links (Elysia's Will)
        if metrics.complexity > 20:
             self.omni.add_logic(file_node_id, "Status", "Complex")

# Singleton
_scanner = None
def get_self_scanner() -> SelfStructureScanner:
    global _scanner
    if _scanner is None:
        _scanner = SelfStructureScanner()
    return _scanner
