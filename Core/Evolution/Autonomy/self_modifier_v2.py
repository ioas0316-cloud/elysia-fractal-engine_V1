"""
SelfModifier V2 (The Hand That Writes)
======================================
"To see the flaw and to fix it are one motion."

This module integrates:
- WaveCodingSystem (파동 분석)
- WaveCoder (AST → Tensor)
- AST Transformation (실제 코드 수정)

It allows Elysia to refactor her own code based on Wave Resonance analysis.
"""

import logging
import ast
import os
import re
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field

logger = logging.getLogger("SelfModifier")

# Import existing systems
try:
    from Core.Interaction.Coordination.Synesthesia.code_wave import CodeWaveAnalyzer
    WAVE_SYSTEM_AVAILABLE = True
except ImportError:
    logger.warning("⚠️ CodeWaveAnalyzer not available. Limited functionality.")
    WAVE_SYSTEM_AVAILABLE = False

try:
    from Core.Evolution.Growth.Autonomy.wave_coder import get_wave_coder, WaveCoder
    WAVE_CODER_AVAILABLE = True
except ImportError:
    logger.warning("⚠️ WaveCoder not available.")
    WAVE_CODER_AVAILABLE = False

try:
    from Core.Foundation.torch_graph import get_torch_graph
    TORCH_GRAPH_AVAILABLE = True
except ImportError:
    TORCH_GRAPH_AVAILABLE = False


@dataclass
class RefactorSuggestion:
    """A structured suggestion for code improvement."""
    file_path: str
    line_start: int
    line_end: int
    severity: str  # "low", "medium", "high"
    category: str  # "complexity", "duplication", "naming", "structure"
    description: str
    suggestion: str
    resonance_source: str = ""  # Which file this resonates with


@dataclass
class WaveAnalysisResult:
    """Result of analyzing a file through Wave Physics."""
    file_path: str
    tension: float  # 0.0 (clean) - 1.0 (spaghetti)
    mass: float  # Size/weight of the code
    frequency: float  # Complexity frequency
    resonance: float  # Connection to other modules
    dna_hash: str = ""
    suggestions: List[RefactorSuggestion] = field(default_factory=list)


# Import Conscience
try:
    from Core.Foundation.Legal_Ethics.Ethics.conscience_circuit import ConscienceCircuit
    CONSCIENCE_AVAILABLE = True
except ImportError:
    CONSCIENCE_AVAILABLE = False
    
class SelfModifier:
    """
    The Hand That Writes (자기 수정자)
    
    Analyzes code using Wave Physics, identifies stress fractures,
    and can apply safe refactoring transformations.
    """
    
    def __init__(self):
        logger.info("✋ SelfModifier V2 initializing...")
        
        self.wave_system = None # WaveCodingSystem() removed as it is replaced by CodeWaveAnalyzer
        self.wave_coder = get_wave_coder() if WAVE_CODER_AVAILABLE else None
        
        self.conscience = ConscienceCircuit() if CONSCIENCE_AVAILABLE else None
        if self.conscience:
            logger.info("   ⚖️ SelfModifier: Conscience Circuit Connected.")
            
        self.graph = get_torch_graph() if TORCH_GRAPH_AVAILABLE else None
        self.analyzer = CodeWaveAnalyzer() if WAVE_SYSTEM_AVAILABLE else None
        
        logger.info("✅ SelfModifier ready (The Hand is awake).")
    
    def analyze_file(self, file_path: str) -> WaveAnalysisResult:
        """
        Analyzes a file using Wave Physics.
        Returns tension, mass, frequency, resonance, and suggestions.
        """
        if not os.path.exists(file_path):
            return WaveAnalysisResult(file_path, 0.0, 0.0, 0.0, 0.0)
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            code = f.read()
        
        # Use CodeWaveAnalyzer (Synesthetic Perception)
        if self.analyzer: # Re-using self.analyzer slot for CodeWaveAnalyzer
             try:
                 wave = self.analyzer.analyze(code)
                 
                 result = WaveAnalysisResult(
                    file_path=file_path,
                    tension=min(1.0, wave.velocity / 50.0), # Velocity mapped to Tension
                    mass=wave.mass,
                    frequency=wave.rhythm,
                    resonance=wave.potential / 100.0,
                    dna_hash=wave.topology # Using topology as DNA desc
                )
                 
                 # Generate suggestions based on wave topology
                 if "Chaos" in wave.topology or "Storm" in wave.topology:
                     result.suggestions.append(RefactorSuggestion(
                         file_path=file_path,
                         line_start=0, line_end=0, severity="high", category="topology",
                         description=f"Code detects as '{wave.topology}'. Too much chaotic velocity.",
                         suggestion="Reduce function calls or complex loops."
                     ))
                 elif "Deep Ocean" in wave.topology:
                     result.suggestions.append(RefactorSuggestion(
                         file_path=file_path,
                         line_start=0, line_end=0, severity="medium", category="topology",
                         description=f"Code is too deep ({wave.potential:.1f} potential).",
                         suggestion="Flatten the nesting structure."
                     ))
                     
             except Exception as e:
                 logger.error(f"Wave Analysis Failed: {e}")
                 # Fallback
                 result = WaveAnalysisResult(file_path, 0.5, 0.5, 0.5, 0.5)

        else:
            # Fallback: Simple analysis
            loc = len(code.splitlines())
            complexity = code.count('if ') + code.count('for ') + code.count('while ')
            
            result = WaveAnalysisResult(
                file_path=file_path,
                tension=min(1.0, complexity / 50.0),
                mass=min(1.0, loc / 500.0),
                frequency=complexity,
                resonance=0.5
            )
        
        # Add to TorchGraph if available
        if self.graph:
            node_id = f"Code:{os.path.basename(file_path)}"
            self.graph.add_node(
                node_id,
                vector=[result.tension, result.mass, result.frequency / 100.0, result.resonance],
                metadata={"wave": {
                    "tension": result.tension,
                    "frequency": result.frequency,
                    "dna_hash": result.dna_hash
                }}
            )
        
        return result

    def modify_file(self, file_path: str, new_content: str) -> Dict[str, Any]:
        """
        [The Dangerous Hand]
        Modifies a file with new content.
        MUST BE GUARDED by Conscience Check.
        """
        if not os.path.exists(file_path):
            return {"success": False, "error": "File not found"}
            
        logger.info(f"📝 Request to modify: {file_path}")
        
        # 1. Conscience Check (The Moral Filter)
        if self.conscience:
            judge = self.conscience.judge_action(
                action_description=f"Modify file {file_path}",
                proposed_code=new_content
            )
            
            if not judge.is_allowed:
                error_msg = f"⛔ Modification BLOCKED by Conscience: {judge.message} (Pain: {judge.pain_level:.2f})"
                logger.warning(error_msg)
                return {"success": False, "error": error_msg}
            
            if judge.pain_level > 0.4:
                 logger.warning(f"   ⚠️ Painful Modification: {judge.message} (Pain: {judge.pain_level:.2f})")
        else:
             logger.warning("   ⚠️ Conscience NOT connected. Acting with raw instinct.")

        # 2. Backup
        try:
            self._create_backup(file_path)
        except Exception as e:
            logger.warning(f"   Backup failed: {e}")

        # 3. Write
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            logger.info(f"   ✅ File modified successfully: {file_path}")
            return {"success": True, "message": "Modified"}
        except Exception as e:
            logger.error(f"   ❌ Write failed: {e}")
            return {"success": False, "error": str(e)}

    def _create_backup(self, file_path: str):
        """Creates a simple .bak copy."""
        import shutil
        backup_path = file_path + ".bak"
        shutil.copy2(file_path, backup_path)
        return backup_path
    
    def find_high_tension_spots(self, file_path: str) -> List[RefactorSuggestion]:
        """
        Identifies specific high-tension areas in the code via AST analysis.
        """
        suggestions = []
        
        if not os.path.exists(file_path):
            return suggestions
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            code = f.read()
        
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return suggestions
        
        # Walk AST to find complex nodes
        for node in ast.walk(tree):
            # Long functions (> 50 lines)
            if isinstance(node, ast.FunctionDef):
                if hasattr(node, 'end_lineno') and node.end_lineno:
                    length = node.end_lineno - node.lineno
                    if length > 50:
                        suggestions.append(RefactorSuggestion(
                            file_path=file_path,
                            line_start=node.lineno,
                            line_end=node.end_lineno,
                            severity="high",
                            category="complexity",
                            description=f"Function '{node.name}' is {length} lines long.",
                            suggestion="Consider breaking into smaller functions."
                        ))
            
            # Deep nesting (> 4 levels)
            if isinstance(node, (ast.If, ast.For, ast.While)):
                depth = self._get_nesting_depth(node)
                if depth > 4:
                    suggestions.append(RefactorSuggestion(
                        file_path=file_path,
                        line_start=node.lineno,
                        line_end=getattr(node, 'end_lineno', node.lineno),
                        severity="medium",
                        category="complexity",
                        description=f"Nesting depth of {depth} at line {node.lineno}.",
                        suggestion="Consider early returns or extracting methods."
                    ))
        
        return suggestions
    
    def _get_nesting_depth(self, node, depth=1) -> int:
        """Recursively calculates nesting depth."""
        max_depth = depth
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.Try)):
                child_depth = self._get_nesting_depth(child, depth + 1)
                max_depth = max(max_depth, child_depth)
        return max_depth
    
    def generate_report(self, directory: str = "Core/") -> Dict[str, Any]:
        """
        Generates a full Wave Analysis report for a directory.
        """
        report = {
            "total_files": 0,
            "high_tension_files": [],
            "suggestions_by_severity": {"high": 0, "medium": 0, "low": 0},
            "average_tension": 0.0
        }
        
        base_path = os.path.join(os.path.dirname(__file__), "..", "..", directory)
        base_path = os.path.abspath(base_path)
        
        if not os.path.exists(base_path):
            base_path = directory  # Try absolute path
        
        total_tension = 0.0
        
        for root, dirs, files in os.walk(base_path):
            # Skip cache directories
            dirs[:] = [d for d in dirs if d != '__pycache__']
            
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    result = self.analyze_file(file_path)
                    
                    report["total_files"] += 1
                    total_tension += result.tension
                    
                    if result.tension > 0.6:
                        report["high_tension_files"].append({
                            "path": file_path,
                            "tension": result.tension,
                            "frequency": result.frequency
                        })
                    
                    for sug in result.suggestions:
                        report["suggestions_by_severity"][sug.severity] += 1
        
        if report["total_files"] > 0:
            report["average_tension"] = total_tension / report["total_files"]
        
        return report


# Singleton
_modifier = None

def get_self_modifier() -> SelfModifier:
    global _modifier
    if _modifier is None:
        _modifier = SelfModifier()
    return _modifier
