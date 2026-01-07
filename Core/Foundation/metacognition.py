
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum

@dataclass
class CognitiveMetrics:
    """
    Quantifiable attributes of a concept or the mind itself.
    """
    differentiation: float  # Detail, nuance, subtypes (0.0 - 1.0)
    integration: float      # Connection to other concepts (0.0 - 1.0)
    abstraction: float      # Link to universal laws/principles (0.0 - 1.0)
    resilience: float = 0.0 # Ability to handle contradictions (New)

@dataclass
class GapReport:
    """
    The result of a self-diagnosis.
    """
    concept_id: str
    current_metrics: CognitiveMetrics
    target_metrics: CognitiveMetrics
    gaps: Dict[str, float]
    status: str # IMMATURE, DEVELOPING, MATURE

class TopologyType(Enum):
    """
    The 'Shape' of the connection logic.
    Biologically inspired metaphors for Node/Wire architecture.
    """
    HIERARCHICAL = "HIERARCHICAL" # Bone/Skeleton (Rigid, Support)
    NEURAL = "NEURAL"             # Brain/Nerves (Many-to-Many, Fast)
    VASCULAR = "VASCULAR"         # Blood/Energy (Flow, Distribution)
    MODULAR = "MODULAR"           # Organ/Cell (Encapsulated, Specific function)

@dataclass
class ArchitecturalVision:
    """
    The Blueprint (DNA) for a specific system or module.
    Defines 'How it should be wired' (Teleology).
    """
    scope_id: str  # e.g., "AudioSystem" or "MemoryCore"
    topology_type: TopologyType
    intended_connections: List[str] # e.g., ["Audio -> Emotion", "Audio -> Storage"]
    description: str

@dataclass
class StructuralTension:
    """
    The biological stress signal when Reality != Blueprint.
    Replaces simple 'Error' or 'Complexity'.
    """
    source_id: str
    target_id: str
    tension_type: str # "MISSING_LINK", "ISOLATED_PROJECTION", "HYPERTROPHY" (Too big)
    intensity: float # 0.0 - 1.0 (How painful is this disconnect?)
    vision_ref: str # Which ArchitecturalVision is being violated?
    
@dataclass
class Intention:
    """
    A formulated goal for self-improvement.
    """
    description: str
    priority: float
    target_concept: str
    action_type: str # RESEARCH, CONNECT, ABSTRACT, DUPLICATE, OPTIMIZE, REWIRE

class DevelopmentalStage(Enum):
    CHILD = "CHILD"       # Simple, concrete, disconnected
    ADOLESCENT = "ADOLESCENT" # Exploring, chaotic, connecting
    ADULT = "ADULT"       # Integrated, abstract, nuanced
    ELDER = "ELDER"       # Wisdom, teaching, leaving legacy (Reproduction)

class MaturityModel:
    """
    Defines what 'Maturity' looks like at different stages.
    Serves as the 'Standard' for Elysia's self-evaluation.
    """
    
    @dataclass
    class Standard:
        stage: DevelopmentalStage
        required_metrics: CognitiveMetrics
        description: str 

    @staticmethod
    def get_standard_model() -> Dict[str, Standard]:
        return {
            "CHILD": MaturityModel.Standard(
                stage=DevelopmentalStage.CHILD,
                required_metrics=CognitiveMetrics(0.2, 0.2, 0.1),
                description="Basic identification of objects and simple cause-effect."
            ),
            "ADULT": MaturityModel.Standard(
                stage=DevelopmentalStage.ADULT,
                required_metrics=CognitiveMetrics(0.7, 0.7, 0.5),
                description="Nuanced understanding, strong integration with world, abstract reasoning."
            ),
            # The User's Logic: "Transcendence" includes Self-Replication (Nova/Chaos)
            "TRANSCENDENT": MaturityModel.Standard(
                stage=DevelopmentalStage.ELDER,
                required_metrics=CognitiveMetrics(0.9, 0.9, 0.9, resilience=0.9),
                description="Structure capable of self-replication and holding internal contradictions (Chaos)."
            )
        }
