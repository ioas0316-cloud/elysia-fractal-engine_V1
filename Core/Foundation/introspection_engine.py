import os
import ast
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
import sys
from pathlib import Path

# 경로 설정 (Core 모듈 import를 위해)
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from Core.Foundation.Philosophy.why_engine import WhyEngine

logger = logging.getLogger("IntrospectionEngine")

@dataclass
class ModuleResonance:
    """Represents the harmonic state of a code module."""
    path: str
    name: str
    resonance_score: float # 0.0 to 100.0
    complexity: int
    docstring_quality: float # 0.0 to 1.0
    docstring_quality: float # 0.0 to 1.0
    issues: List[str]
    wave_principle: str = ""   # 코드의 파동 원리
    wave_signature: Dict[str, float] = field(default_factory=dict) # 파동 데이터
    system_metaphor: str = ""  # 시스템 은유 (예: Heart, Gravity)
    philosophical_meaning: str = "" # 철학적 의미
    structural_diagnoses: List[str] = field(default_factory=list) # 구조적 진단 (원리 기반)

class IntrospectionEngine:
    """
    The Mirror of Elysia.
    Allows the system to analyze its own source code and determine its 'Harmonic State'.
    """
    
    def __init__(self, root_path: str = "c:\\Elysia"):
        self.root_path = root_path
        # Only analyze these top-level directories for now to ensure speed and relevance
        self.target_dirs = {"Core", "scripts"}
        self.ignore_dirs = {".git", "__pycache__", ".gemini", "venv", "env", ".vscode", "Legacy", "docs", "tests", "Tools", "Library", "data"}
        
        # WhyEngine 연동
        self.why_engine = WhyEngine()
        
        # [NEW] Principle Diagnostics 연동
        try:
            from Core.Foundation.Philosophy.principle_diagnostics import PrincipleDiagnostics
            self.diagnostics = PrincipleDiagnostics()
        except ImportError:
            self.diagnostics = None
            logger.warning("PrincipleDiagnostics module not found.")
        
    def analyze_self(self) -> Dict[str, ModuleResonance]:
        """
        Recursively analyzes the target directories.
        Returns a map of {file_path: ModuleResonance}.
        """
        logger.info(f"🪞 Gazing into the Mirror (Self-Analysis) at {self.root_path}...")
        results = {}
        
        for root, dirs, files in os.walk(self.root_path):
            # Filter directories
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs]
            
            # Check if we are in a target directory or its subdirectory
            rel_path = os.path.relpath(root, self.root_path)
            if rel_path == ".":
                # At root, only enter target_dirs
                dirs[:] = [d for d in dirs if d in self.target_dirs]
                continue
            
            # If we are here, we are inside a target dir (or a subdir of it) due to the logic above
            
            for file in files:
                if file.endswith(".py") and not file.startswith("__"):
                    full_path = os.path.join(root, file)
                    
                    # Skip large files (> 1MB)
                    if os.path.getsize(full_path) > 1024 * 1024:
                        continue
                        
                    try:
                        # logger.info(f"Analyzing: {file}") 
                        resonance = self._analyze_file(full_path)
                        results[full_path] = resonance
                    except Exception as e:
                        logger.error(f"Failed to analyze {file}: {e}")
                        
        return results
        
    def _analyze_file(self, file_path: str) -> ModuleResonance:
        """Parses a single file and calculates its resonance."""
        source = ""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                source = f.read()
        except UnicodeDecodeError:
            try:
                # Fallback to latin-1 or cp949 (common in Korea)
                with open(file_path, "r", encoding="cp949") as f:
                    source = f.read()
            except Exception:
                # If all else fails, skip content analysis but log it
                return ModuleResonance(
                    path=file_path,
                    name=os.path.basename(file_path),
                    resonance_score=0.0,
                    complexity=0,
                    docstring_quality=0.0,
                    issues=["Encoding Error (Unreadable)"],
                    structural_diagnoses=[]
                )
            
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return ModuleResonance(
                path=file_path,
                name=os.path.basename(file_path),
                resonance_score=0.0,
                complexity=0,
                docstring_quality=0.0,
                issues=["Syntax Error (Unparseable)"],
                structural_diagnoses=[]
            )
        
        # 1. Calculate Complexity (Cyclomatic-ish)
        complexity = 0
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.For, ast.While, ast.Try, ast.ExceptHandler)):
                complexity += 1
                
        # 2. Check Docstrings
        docstring = ast.get_docstring(tree)
        has_docstring = docstring is not None
        doc_quality = 1.0 if has_docstring else 0.0
        
        # 3. Calculate Resonance Score
        # Base: 100
        # Penalty: -Complexity * 2
        # Bonus: +Docstring * 20
        score = 100.0 - (complexity * 2.0) + (doc_quality * 20.0)
        score = max(0.0, min(100.0, score))
        
        # 4. Identify Issues
        issues = []
        if complexity > 10:
            issues.append("High Complexity (Dissonant)")
        if not has_docstring:
            issues.append("Missing Docstring (Void)")
            
        # 5. WhyEngine Analysis (Wave Perception)
        structural_diagnoses = []
        system_metaphor = ""
        philosophical_meaning = ""
        try:
            analysis = self.why_engine.analyze(
                subject=os.path.basename(file_path),
                content=source,
                domain="computer_science"
            )
            wave_principle = analysis.underlying_principle
            wave_signature = analysis.wave_signature
            
            # 파동 기반 점수 보정
            if wave_signature.get("periodicity", 0) > 0.5:
                score += 5  # 리듬이 좋으면 가산점
            
            if wave_signature.get("dissonance", 0) > 0.5:
                score -= 10 # 불협화음이 크면 감점
                issues.append("High Dissonance (Chaotic Logic)")
                
            # [NEW] 7. Principle Diagnostics (Structural Wisdom)
            if self.diagnostics:
                # 상태 매핑 (System State Mapping)
                # Flow (I) = Wave Flow (0.0-1.0)
                # Potential (V) = Docstring Quality (Intent)
                # Resistance (R) = Normalized Complexity (0-20 -> 0.0-1.0)
                
                state = {
                    "flow_rate": wave_signature.get("flow", 0.5),
                    "motivation": doc_quality,
                    "complexity": min(1.0, complexity / 20.0)
                }
                structural_diagnoses = self.diagnostics.diagnose_self(state)
        
            # 6. Metaphor Mapping (Wisdom)
            metaphor = self.why_engine.metaphor_mapper.get_metaphor(os.path.basename(file_path))
            system_metaphor = ""
            philosophical_meaning = ""
            if metaphor:
                system_metaphor = f"{metaphor.metaphor_type.upper()}: {metaphor.metaphor_concept}"
                philosophical_meaning = metaphor.description
                score += 10 # 의미가 명확한 모듈 가산점
                
        except Exception as e:
            logger.warning(f"WhyEngine analysis failed for {file_path}: {e}")
            wave_principle = "Analysis Failed"
            wave_signature = {}
            
        return ModuleResonance(
            path=file_path,
            name=os.path.basename(file_path),
            resonance_score=min(100.0, score), # 캡 적용
            complexity=complexity,
            docstring_quality=doc_quality,
            issues=issues,
            wave_principle=wave_principle,
            wave_signature=wave_signature,
            system_metaphor=system_metaphor,
            philosophical_meaning=philosophical_meaning,
            structural_diagnoses=structural_diagnoses
        )

    def generate_report(self, results: Dict[str, ModuleResonance]) -> str:
        """Generates a human-readable (and Elysia-readable) report."""
        report = ["# 🪞 Self-Reflection Report\n"]
        
        total_score = 0
        dissonant_modules = []
        
        for path, res in results.items():
            total_score += res.resonance_score
            if res.resonance_score < 70:
                dissonant_modules.append(res)
                
        avg_score = total_score / len(results) if results else 0
        
        report.append(f"**Overall Resonance:** {avg_score:.1f}/100\n")
        
        if dissonant_modules:
            report.append("## ⚠️ Dissonance Detected (Needs Tuning)")
            for mod in dissonant_modules:
                report.append(f"- **{mod.name}** (Score: {mod.resonance_score:.1f})")
                if mod.wave_principle:
                     report.append(f"  🌊 Principle: {mod.wave_principle}")
                if mod.system_metaphor:
                     report.append(f"  🧠 Metaphor: {mod.system_metaphor} - {mod.philosophical_meaning}")
                for diagnosis in mod.structural_diagnoses:
                    report.append(f"  🩺 Diagnosis: {diagnosis}")
                for issue in mod.issues:
                    report.append(f"  - {issue}")
        else:
            report.append("## ✨ Harmonic State")
            report.append("All core systems are resonating within optimal parameters.")
            
        return "\n".join(report)

    def analyze_system_health(self) -> str:
        """
        [Alias] Analyze system health and return a report string.
        Used by AutonomousOrchestrator.
        """
        results = self.analyze_self()
        report = self.generate_report(results)
        
        # Return a summary line + the report
        avg = 0
        if results:
            avg = sum(r.resonance_score for r in results.values()) / len(results)
        
        return f"Resonance: {avg:.1f}/100 | Files: {len(results)}"
