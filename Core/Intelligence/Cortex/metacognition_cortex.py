"""
MetaCognition Cortex (메타인지 피질)
===================================

원본: Legacy/Project_Sophia/meta_cognition_cortex.py
마이그레이션: 2025-12-15

자신의 지식을 성찰하고, 개념 간 관계를 이해하며, 통찰을 생성합니다.
'자기 성장 엔진'의 핵심입니다.
"""
import logging
from typing import Dict, Any, Optional


class MetaCognitionCortex:
    """
    Enables Elysia to reflect upon her own knowledge,
    understanding relationships between concepts and generating insights.
    """

    def __init__(self, kg_manager=None, wave_mechanics=None, core_memory=None):
        self.kg_manager = kg_manager
        self.wave_mechanics = wave_mechanics
        self.core_memory = core_memory
        self.logger = logging.getLogger("MetaCognitionCortex")

    def analyze_conceptual_balance(self) -> Dict[str, Any]:
        """Analyzes the balance between opposing concepts and proposes tuning if needed."""
        self.logger.info("[MetaCognition] Analyzing conceptual balance...")
        
        if not self.wave_mechanics:
            return {"status": "skipped", "reason": "no wave_mechanics"}

        concept_pairs = [
            ("light", "darkness"),
            ("good", "evil"),
            ("creation", "destruction"),
            ("love", "fear"),
            ("order", "chaos")
        ]
        
        imbalances = []
        
        for concept_a, concept_b in concept_pairs:
            metrics_a = self._get_concept_metrics(concept_a)
            metrics_b = self._get_concept_metrics(concept_b)
            
            density_a = metrics_a.get('connection_density', 0)
            density_b = metrics_b.get('connection_density', 0)
            
            if density_a > density_b * 2:
                imbalances.append({
                    "dominant": concept_a,
                    "deficient": concept_b,
                    "ratio": density_a / max(density_b, 0.01)
                })
            elif density_b > density_a * 2:
                imbalances.append({
                    "dominant": concept_b,
                    "deficient": concept_a,
                    "ratio": density_b / max(density_a, 0.01)
                })

        return {
            "status": "complete",
            "imbalances": imbalances,
            "recommendations": [
                f"Focus on '{i['deficient']}' to balance '{i['dominant']}'" 
                for i in imbalances
            ]
        }

    def _get_concept_metrics(self, concept_id: str) -> Dict[str, float]:
        """Calculates metrics for a given concept cluster."""
        if not self.wave_mechanics:
            return {'node_count': 0, 'connection_density': 0, 'total_energy': 0}
            
        try:
            related_nodes = self.wave_mechanics.spread_activation(concept_id, threshold=0.2)
        except Exception:
            related_nodes = {}
        
        if not related_nodes:
            return {'node_count': 0, 'connection_density': 0, 'total_energy': 0}

        node_count = len(related_nodes)
        total_energy = sum(related_nodes.values())

        total_connections = 0
        if self.kg_manager:
            for node_id in related_nodes:
                try:
                    neighbors = self.kg_manager.get_neighbors(node_id)
                    total_connections += len(neighbors) if neighbors else 0
                except Exception:
                    pass

        connection_density = total_connections / node_count if node_count > 0 else 0

        return {
            'node_count': node_count,
            'connection_density': connection_density,
            'total_energy': total_energy
        }

    def reflect_on_concept(self, concept_id: str, context: str = "") -> Dict[str, Any]:
        """
        Reflects on a given concept and its connections within the knowledge graph.
        
        Args:
            concept_id: The ID of the concept to reflect upon
            context: The context in which the concept was encountered
            
        Returns:
            Dictionary containing reflection results
        """
        if not self.wave_mechanics:
            return {
                "reflection": f"Unable to reflect on '{concept_id}' - no wave mechanics available.",
                "activated_nodes": {},
                "spiritual_alignment": 0.0
            }

        # Ensure concept node exists
        if self.kg_manager:
            try:
                if not self.kg_manager.get_node(concept_id):
                    self.kg_manager.add_node(concept_id)
            except Exception:
                pass

        # Spread activation
        try:
            activated_nodes = self.wave_mechanics.spread_activation(
                start_node_id=concept_id,
                initial_energy=1.0,
                threshold=0.3
            )
        except Exception:
            activated_nodes = {}

        if not activated_nodes:
            reflection = f"Upon reflecting on '{concept_id}', I find this concept is new or isolated."
            spiritual_alignment = 0.0
        else:
            related = sorted(activated_nodes.items(), key=lambda x: x[1], reverse=True)[:5]
            reflection = f"Upon reflecting on '{concept_id}'"
            if context:
                reflection += f" in context of '{context}'"
            reflection += f", I see connections to: "
            reflection += ", ".join([f"{n} ({e:.2f})" for n, e in related])
            
            spiritual_alignment = activated_nodes.get("love", 0.0)

        return {
            "reflection": reflection,
            "activated_nodes": activated_nodes,
            "spiritual_alignment": spiritual_alignment
        }


# Singleton
_metacog_cortex: Optional[MetaCognitionCortex] = None

def get_metacognition_cortex() -> MetaCognitionCortex:
    global _metacog_cortex
    if _metacog_cortex is None:
        _metacog_cortex = MetaCognitionCortex()
    return _metacog_cortex
