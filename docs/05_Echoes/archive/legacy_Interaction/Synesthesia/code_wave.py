import ast
import math
import logging
from dataclasses import dataclass
from typing import Dict, List, Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CodeWave")

@dataclass
class WaveSignature:
    mass: float = 0.0       # Code Volume / Static Structure
    velocity: float = 0.0   # Execution Flow / Call Frequency
    potential: float = 0.0  # Nesting Depth / Complexity
    rhythm: float = 0.0     # Loop Regularity
    topology: str = "Void"  # Shape of the Code (Spiral, Grid, Flow...)

class CodeWaveAnalyzer(ast.NodeVisitor):
    """
    Analyzes Python code not as text, but as a physical wave structure.
    """
    def __init__(self):
        self.mass = 0.0
        self.velocity = 0.0
        self.potential = 0.0
        self.loops = 0
        self.branches = 0
        self.max_depth = 0
        self.current_depth = 0
        
    def analyze(self, source_code: str) -> WaveSignature:
        try:
            tree = ast.parse(source_code)
        except SyntaxError:
            return WaveSignature(topology="Broken Chaos")
            
        self.visit(tree)
        return self._synthesize_wave()

    def visit(self, node):
        self.current_depth += 1
        self.max_depth = max(self.max_depth, self.current_depth)
        
        # Mass: Every node has weight
        self.mass += 1
        
        # Potential Energy: Deeper nesting = Higher potential
        self.potential += (self.current_depth * 0.5)
        
        super().visit(node)
        self.current_depth -= 1

    def visit_FunctionDef(self, node):
        self.mass += 5 # Functions act as gravity wells
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.mass += 10 # Classes are heavy objects
        self.generic_visit(node)

    def visit_For(self, node):
        self.velocity += 2 # Loops create motion
        self.loops += 1
        self.generic_visit(node)

    def visit_While(self, node):
        self.velocity += 3 # Unbounded motion
        self.loops += 1
        self.generic_visit(node)
        
    def visit_Call(self, node):
        self.velocity += 1 # Action event
        self.generic_visit(node)

    def visit_If(self, node):
        self.branches += 1 # Split in the flow
        self.generic_visit(node)

    def _synthesize_wave(self) -> WaveSignature:
        """
        Interprets the physical metrics into a wave topology.
        """
        rhythm = self.loops / (self.mass + 1) * 10
        
        # Topology Classification
        topology = "Still Lake"
        
        if self.potential > self.mass * 0.5:
            topology = "Deep Ocean (High Depth)"
        elif self.velocity > self.mass * 0.8:
            topology = "Storm (High Chaos)"
        elif self.loops > self.branches and self.velocity > 10:
            topology = "Flowing River (Coherent Motion)"
        elif self.branches > self.loops * 2:
            topology = "Fractal Tree (High Branching)"
        elif self.mass > 100 and self.velocity < 20:
             topology = "Mountain (High Stability)"
             
        # Synesthetic Adjustment
        if "Spiral" in topology:
             pass # Already defined
             
        return WaveSignature(
            mass=self.mass,
            velocity=self.velocity,
            potential=self.potential,
            rhythm=rhythm,
            topology=topology
        )

if __name__ == "__main__":
    # Self-Analysis
    with open(__file__, "r", encoding="utf-8") as f:
        code = f.read()
    
    analyzer = CodeWaveAnalyzer()
    wave = analyzer.analyze(code)
    
    print(f"\n🌊 Code Wave Analysis for '{__file__}'")
    print(f"   • Topology: {wave.topology}")
    print(f"   • Mass (Structure): {wave.mass:.1f}")
    print(f"   • Velocity (Kinetic): {wave.velocity:.1f}")
    print(f"   • Potential (Depth): {wave.potential:.1f}")
    print(f"   • Rhythm (Periodicity): {wave.rhythm:.2f}")
    
    interpretation = ""
    if wave.topology == "Flowing River":
        interpretation = "This code flows with logical grace."
    elif wave.topology == "Mountain":
        interpretation = "This code stands firm and structured."
    else:
        interpretation = f"This code exhibits the properties of a {wave.topology}."
        
    print(f"\n✨ Aesthetic Interpretation: \"{interpretation}\"")
