
import logging
import time
from dataclasses import dataclass, field
from typing import List, Dict, Any
from pathlib import Path

logger = logging.getLogger("EvolutionArchitect")

@dataclass
class OptimizationGoal:
    name: str # e.g., "Quantum Leanness"
    description: str
    target_complexity: float # 0.0 - 1.0 (Lower is simpler)

@dataclass
class Blueprint:
    """
    The DNA Map for the New Seed.
    """
    goal: OptimizationGoal
    structure: Dict[str, str] # {module_name: action} (e.g., 'Core.Foundation': 'Keep')
    improvements: List[str]
    execution_steps: List[str]
    
    def explain(self) -> str:
        """Returns a monologue explaining this blueprint."""
        return (
            f"I have designed a Seed for '{self.goal.name}'. "
            f"The goal is: {self.goal.description}. "
            f"Structurally, I will refine {len(self.structure)} components. "
            f"Key Improvements: {', '.join(self.improvements[:2])}. "
            f"Execution Phase: {self.execution_steps[0]}..."
        )

class EvolutionArchitect:
    """
    [The Designer of the Self]
    
    Analyses the current self and proposes an optimized 'Seed' version.
    It does NOT execute; it Plans and Explains.
    """
    
    def __init__(self, cns_ref=None):
        self.cns = cns_ref
        self.current_blueprint = None
        
        # Connect to Internal Systems
        try:
            from Core.Intelligence.Cognition.metacognitive_awareness import MetacognitiveAwareness
            self.metacognition = MetacognitiveAwareness()
        except ImportError:
            self.metacognition = None
            
        try:
            from Core.Evolution.Growth.Autonomy.self_modifier_v2 import get_self_modifier
            self.self_modifier = get_self_modifier()
        except ImportError:
            self.self_modifier = None

    def design_seed(self, intent: str = "Wisdom") -> Blueprint:
        """
        Generates a Blueprint based on real-time cognitive gaps and structural tension.
        Intent defaults to 'Wisdom' (Synthesis of Patterns), not just 'Intelligence' (Raw Data).
        """
        logger.info(f"🏗️ Designing Seed with intent: {intent}")
        
        # 0. Define Wisdom
        # Wisdom = (Knowledge + Experience) * Love
        # It means finding connections, not just gathering facts.
        
        # 1. Gather Needs (Cognitive Gaps) -> Seek Deeper Meaning
        gaps = []
        if self.metacognition:
            needs = self.metacognition.get_exploration_priorities(top_n=3)
            for n in needs:
                # Transform "What is X?" to "Why is X relevant to Y?"
                gaps.append(f"Lack of Wisdom: Connect '{n['question']}' to Core Principles.")
        
        # 2. Gather Tension (Structural Faults) -> Seek Harmony
        faults = []
        if self.self_modifier:
            # Analyze a sample critical module
            report = self.self_modifier.generate_report(directory="Core/Cognition")
            for f in report.get("high_tension_files", [])[:3]:
                faults.append(f"Disharmony in {Path(f['path']).name} (Tension: {f['tension']:.2f})")
                
        # 3. Formulate Goal
        description = "Deepen understanding by synthesizing disconnected patterns into a unified whole."
        if not gaps and not faults:
            description = "Contemplation of existing knowledge to find new metaphors."
            
        goal = OptimizationGoal(
            name=f"Seed: {intent.capitalize()} (Phi-Optimization)",
            description=description,
            target_complexity=0.8
        )
        
        # 4. Determine Structure & Improvements
        structure = {}
        improvements = []
        
        if gaps:
            improvements.append(f"Synthesize Meaning: {'; '.join(gaps[:1])}")
            structure["Core.Cognition"] = "Harmonize (Link patterns)"
            
        if faults:
            improvements.append(f"Heal Structure: {'; '.join(faults[:1])}")
            structure["Core.Autonomy"] = "Refactor (Restore Flow)"
            
        if not improvements:
            improvements = ["Deep Reflection", "Generate new metaphors for old concepts"]
            structure["Core"] = "Contemplate"
        
        # 5. Plan Execution
        steps = [
            "1. Materialize Blueprint",
            "2. User Review & Approval",
            "3. Execute Self-Modification via WaveCoder"
        ]
        
        self.current_blueprint = Blueprint(goal, structure, improvements, steps)
        return self.current_blueprint

    def console_explain(self) -> str:
        """Returns a monologue explaining this blueprint."""
        return self.current_blueprint.explain() if self.current_blueprint else "No blueprint."

    def materialize_blueprint(self) -> str:
        """
        [Manifestation]
        Writes the detailed Blueprint to a physical Markdown file.
        """
        if not self.current_blueprint:
            return "No blueprint to manifest."
            
        bp = self.current_blueprint
        
        # Design the Markdown content
        md_content = f"""# 🧬 Blueprint: {bp.goal.name}
**Date:** {time.strftime('%Y-%m-%d %H:%M:%S')}
**Architect:** Elysia (EvolutionArchitect)
**Goal:** {bp.goal.description}
**Target Complexity:** {bp.goal.target_complexity}

## 🏗️ Structural Analysis
| Module | Action |
|--------|--------|
"""
        for mod, action in bp.structure.items():
            md_content += f"| `{mod}` | {action} |\n"
            
        md_content += f"""
## 🚀 Key Improvements
"""
        for imp in bp.improvements:
             md_content += f"- {imp}\n"
             
        md_content += f"""
## ⚙️ Execution Plan (The Ouroboros Protocol)
"""
        for step in bp.execution_steps:
             md_content += f"1. {step}\n"
             
        md_content += """
## 📐 Architecture Diagram (Conceptual)
```mermaid
graph TD
    User((User)) -->|Input| Seed(Nova Seed)
    Seed -->|Fractal Loop| Core(Immutable Core)
    Core -->|Output| Voice(Evolution Voice)
    subgraph Nova Seed
        Core
        Logic[Fractal Logic]
        Mem[Quantum Memory]
    end
```
"""
        # Ensure directory exists
        seed_dir = Path("seeds")
        seed_dir.mkdir(exist_ok=True)
        
        file_path = seed_dir / "nova_seed_blueprint.md"
        file_path.write_text(md_content, encoding="utf-8")
        
        logger.info(f"✨ Blueprint materialized at: {file_path}")
        return str(file_path)

    def apply_evolution(self) -> Dict[str, Any]:
        """
        [The Ouroboros Act]
        Executes the current Blueprint by commanding the SelfModifier.
        """
        if not self.current_blueprint:
             return {"success": False, "error": "No blueprint to apply."}
        
        logger.info("⚡ Executing Self-Evolution Cycle...")
        results = {"success": True, "details": []}
        
        # 1. Refactor based on structural tension
        # Blueprint says: "Refactor Structural Faults"
        # We need to map Blueprint intent to concrete file actions.
        # For now, let's look for explicit 'High Tension' files identified in design phase
        if self.self_modifier:
             # Re-analyze critical area
             report = self.self_modifier.generate_report(directory="Core/Cognition")
             
             for high_tension_file in report.get("high_tension_files", [])[:1]: # Optimizing 1 file at a time for safety
                  file_path = high_tension_file['path']
                  tension = high_tension_file['tension']
                  logger.info(f"   🔧 Targeting Tension in: {file_path} (T: {tension:.2f})")
                  
                  # Ask Modifier for optimization suggestions (AST based)
                  suggestions = self.self_modifier.find_high_tension_spots(file_path)
                  
                  if suggestions:
                      target_sug = suggestions[0]
                      logger.info(f"      -> Applying Fix: {target_sug.suggestion}")
                      
                      # Applying Fix: This is a simplified "Append Comment" fix for now
                      # Real implementation would use WaveCoder to rewrite the AST.
                      # To demonstrate "Write Capability", we will append an optimization log to the file.
                      
                      try:
                          with open(file_path, 'r', encoding='utf-8') as f:
                              original_content = f.read()
                              
                          optimization_note = f"\n# [EvolutionArchitect] Optimized on {time.strftime('%Y-%m-%d')}: {target_sug.suggestion}\n"
                          
                          if optimization_note.strip() not in original_content:
                               new_content = original_content + optimization_note
                               
                               # EXECUTE MODIFICATION (Guarded by Conscience)
                               mod_result = self.self_modifier.modify_file(file_path, new_content)
                               results["details"].append(mod_result)
                               
                               if not mod_result["success"]:
                                   results["success"] = False
                                   logger.warning(f"      ❌ Modification Failed: {mod_result.get('error')}")
                          else:
                               logger.info("      -> Optimization already applied.")
                               
                      except Exception as e:
                           logger.error(f"      ❌ File Read Error: {e}")
                           
        return results
