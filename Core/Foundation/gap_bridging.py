
import logging
import uuid
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from .causal_narrative_engine import (
    ThoughtUniverse, EpistemicSpace, ContextPlane, ConceptPoint, 
    DimensionLevel, CausalRelationType
)
from .metacognition import MaturityModel, CognitiveMetrics, GapReport, Intention

logger = logging.getLogger("GapBridging")

@dataclass
class Hypothesis:
    id: str
    description: str
    target_concept_id: str
    test_code: str  # Code to verify the hypothesis

@dataclass
class LabResult:
    hypothesis_id: str
    success: bool
    observations: List[str]
    learned_concepts: List[Dict[str, Any]] # Concepts to be promoted

class GapBridgingDrive:
    """
    Phase 16: The Gap-Bridging Drive (Active Learning)
    
    Transforms passive gap identification into active learning using an 'Epistemic Sandbox'.
    """
    
    def __init__(self, universe: ThoughtUniverse):
        self.universe = universe
        self.active_labs: Dict[str, str] = {} # lab_id -> target_concept_id
        
    def bridge_gap(self, gap_report: GapReport) -> Optional[LabResult]:
        """
        Orchestrates the full bridging process:
        1. Create Lab
        2. Formulate Hypothesis
        3. Run Experiment
        4. Consolidate Learning
        """
        target_id = gap_report.concept_id
        logger.info(f"🌉 Initiating Gap Bridging for: {target_id}")
        
        # 1. Create Lab Space (The Sandbox)
        lab_id = self._create_lab_space(target_id)
        
        # 2. Formulate Hypothesis (Simulated for now, would use LLM in full version)
        # For this phase, we simulate learning 'lib_ast' if that's the target
        hypothesis = self._formulate_hypothesis(target_id)
        
        if not hypothesis:
            logger.warning("   Could not formulate hypothesis.")
            return None
            
        # 3. Run Experiment in Lab
        result = self._run_experiment(lab_id, hypothesis)
        
        # 4. Consolidate (Promote to Truth)
        if result.success:
            self._consolidate_learning(target_id, result)
            logger.info(f"✅ Gap Bridged: {target_id} enhanced with {len(result.learned_concepts)} new concepts.")
        else:
            logger.info(f"❌ Experiment Failed: {result.observations}")
            
        # Cleanup
        self._destroy_lab_space(lab_id)
        
        return result

    def _create_lab_space(self, target_id: str) -> str:
        """Spawns a temporary EpistemicSpace for experimentation."""
        lab_id = f"Lab_{target_id}_{str(uuid.uuid4())[:8]}"
        
        # Create a contained space
        self.universe.add_space(
            id=lab_id,
            description=f"Experimental Sandbox for {target_id}",
            plane_ids=[], 
            schema_type="laboratory"
        )
        
        self.active_labs[lab_id] = target_id
        logger.info(f"   🧪 Created Lab: {lab_id}")
        return lab_id

    def _formulate_hypothesis(self, target_id: str) -> Optional[Hypothesis]:
        """Generates a testable hypothesis."""
        # Hardcoded simulation for 'lib_ast' as per Phase 16 plan
        if "lib_ast" in target_id or "ast" in target_id:
            return Hypothesis(
                id=f"Hyp_{str(uuid.uuid4())[:8]}",
                description="AST module can parse string code into tree objects.",
                target_concept_id=target_id,
                test_code="import ast; tree = ast.parse('x = 1')"
            )
        return None

    def _run_experiment(self, lab_id: str, hypothesis: Hypothesis) -> LabResult:
        """Executes the hypothesis in the safety of the Lab."""
        logger.info(f"   🔬 Running Experiment: {hypothesis.description}")
        
        try:
            # ACTUALLY RUN THE CODE (Safety warning: Sandbox needed in real deploy)
            # For this internal system, we trust the hypothesis generator (Self).
            exec_globals = {}
            exec(hypothesis.test_code, exec_globals)
            
            # If no exception, it worked.
            # Simulate "Observing" the result
            learned = []
            if "ast" in hypothesis.target_concept_id:
                learned.append({
                    "id": f"{hypothesis.target_concept_id}.parse",
                    "type": "function",
                    "description": "Parses source code into an AST node."
                })
                learned.append({
                    "id": f"{hypothesis.target_concept_id}.AST",
                    "type": "class",
                    "description": "Base class for AST nodes."
                })
            
            return LabResult(
                hypothesis_id=hypothesis.id,
                success=True,
                observations=["Code executed successfully", "Objects created"],
                learned_concepts=learned
            )
            
        except Exception as e:
            return LabResult(
                hypothesis_id=hypothesis.id,
                success=False,
                observations=[f"Error: {e}"],
                learned_concepts=[]
            )

    def _consolidate_learning(self, target_id: str, result: LabResult):
        """Promotes Lab concepts to the main ThoughtUniverse."""
        
        # 1. Update the Target Node (Confidence boost)
        if target_id in self.universe.points:
            self.universe.points[target_id].confidence = min(1.0, self.universe.points[target_id].confidence + 0.3)
            
        # 2. Add New Concepts
        for concept in result.learned_concepts:
            c_id = concept["id"]
            if c_id not in self.universe.points:
                self.universe.add_point(
                    id=c_id,
                    description=concept["description"],
                    concept_type=concept["type"]
                )
                # Link to Target
                self.universe.add_line(target_id, c_id, "provides_capability", strength=1.0)
                logger.info(f"      ✨ Promoted Concept: {c_id}")

    def _destroy_lab_space(self, lab_id: str):
        """Cleans up the sandbox."""
        if lab_id in self.universe.spaces:
            del self.universe.spaces[lab_id]
        if lab_id in self.active_labs:
            del self.active_labs[lab_id]
        logger.info(f"   🧹 Destroyed Lab: {lab_id}")
