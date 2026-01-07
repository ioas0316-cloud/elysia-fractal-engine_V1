"""
Causal Reasoning System
Phase 13: 범용 인공지능 향해 (Towards AGI)

Enables understanding of cause-and-effect relationships, predicting
intervention effects, and counterfactual reasoning.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Set, Tuple
import asyncio
from datetime import datetime


@dataclass
class CausalRelation:
    """Represents a causal relationship"""
    cause: str
    effect: str
    strength: float  # 0.0 to 1.0
    confidence: float  # 0.0 to 1.0
    evidence_count: int = 0
    confounders: List[str] = field(default_factory=list)
    mechanism: Optional[str] = None


@dataclass
class CausalGraph:
    """Directed acyclic graph of causal relationships"""
    nodes: List[str] = field(default_factory=list)
    edges: List[CausalRelation] = field(default_factory=list)
    
    def add_node(self, node: str):
        if node not in self.nodes:
            self.nodes.append(node)
    
    def add_edge(self, relation: CausalRelation):
        self.add_node(relation.cause)
        self.add_node(relation.effect)
        self.edges.append(relation)
    
    def get_causes(self, effect: str) -> List[str]:
        """Get all direct causes of an effect"""
        return [rel.cause for rel in self.edges if rel.effect == effect]
    
    def get_effects(self, cause: str) -> List[str]:
        """Get all direct effects of a cause"""
        return [rel.effect for rel in self.edges if rel.cause == cause]


@dataclass
class Intervention:
    """Represents an intervention on a variable"""
    variable: str
    new_value: Any
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class InterventionEffect:
    """Predicted effect of an intervention"""
    intervention: Intervention
    affected_variables: Dict[str, Any]  # variable -> predicted_value
    confidence: float
    reasoning: List[str] = field(default_factory=list)


class CausalReasoner:
    """
    Causal Reasoning System
    
    Capabilities:
    1. Infer causal relationships from observations
    2. Build causal graphs
    3. Identify confounders
    4. Predict intervention effects
    5. Perform counterfactual reasoning
    """
    
    # Constants for influence calculations
    DIRECT_EFFECT_WEIGHT = 2  # Weight multiplier for direct causal effects
    INDIRECT_EFFECT_WEIGHT = 1  # Weight multiplier for indirect effects
    
    def __init__(self):
        self.causal_graphs: Dict[str, CausalGraph] = {}
        self.observation_history: List[Dict] = []
        self.intervention_history: List[Intervention] = []
        self.counterfactual_cache: Dict[str, Any] = {}
    
    async def infer_causality(
        self,
        observations: List[Dict[str, Any]],
        domain: str = "general"
    ) -> CausalGraph:
        """
        Infer causal relationships from observations
        
        Args:
            observations: List of observed states
            domain: Domain name for the causal graph
            
        Returns:
            CausalGraph representing inferred causal structure
        """
        # Store observations
        self.observation_history.extend(observations)
        
        # 1. Identify correlations
        correlations = self.identify_correlations(observations)
        
        # 2. Determine causal directions
        causal_directions = await self.determine_causal_direction(correlations)
        
        # 3. Identify confounders
        confounders = await self.identify_confounders(
            causal_directions, observations
        )
        
        # 4. Build causal graph
        causal_graph = self.build_causal_graph(causal_directions, confounders)
        
        # 5. Store the graph
        self.causal_graphs[domain] = causal_graph
        
        return causal_graph
    
    def identify_correlations(
        self,
        observations: List[Dict[str, Any]]
    ) -> List[Tuple[str, str, float]]:
        """
        Identify correlations between variables
        
        Returns: List of (var1, var2, correlation_strength) tuples
        """
        if not observations:
            return []
        
        correlations = []
        
        # Get all variable names
        all_vars = set()
        for obs in observations:
            all_vars.update(obs.keys())
        
        variables = list(all_vars)
        
        # Compute pairwise correlations
        for i, var1 in enumerate(variables):
            for var2 in variables[i+1:]:
                correlation = self._compute_correlation(
                    observations, var1, var2
                )
                
                if abs(correlation) > 0.3:  # Threshold for significance
                    correlations.append((var1, var2, correlation))
        
        return correlations
    
    def _compute_correlation(
        self,
        observations: List[Dict[str, Any]],
        var1: str,
        var2: str
    ) -> float:
        """Compute correlation between two variables"""
        # Extract values for both variables
        values1 = []
        values2 = []
        
        for obs in observations:
            if var1 in obs and var2 in obs:
                v1 = obs[var1]
                v2 = obs[var2]
                
                # Convert to numeric if possible
                try:
                    v1 = float(v1) if not isinstance(v1, bool) else (1.0 if v1 else 0.0)
                    v2 = float(v2) if not isinstance(v2, bool) else (1.0 if v2 else 0.0)
                    values1.append(v1)
                    values2.append(v2)
                except (ValueError, TypeError):
                    # Non-numeric values
                    pass
        
        if len(values1) < 2:
            return 0.0
        
        # Compute Pearson correlation
        n = len(values1)
        mean1 = sum(values1) / n
        mean2 = sum(values2) / n
        
        numerator = sum((values1[i] - mean1) * (values2[i] - mean2) for i in range(n))
        
        var1_sum = sum((v - mean1) ** 2 for v in values1)
        var2_sum = sum((v - mean2) ** 2 for v in values2)
        
        if var1_sum == 0 or var2_sum == 0:
            return 0.0
        
        denominator = (var1_sum * var2_sum) ** 0.5
        
        return numerator / denominator if denominator != 0 else 0.0
    
    async def determine_causal_direction(
        self,
        correlations: List[Tuple[str, str, float]]
    ) -> List[CausalRelation]:
        """
        Determine causal direction for correlated variables
        
        Uses temporal information, domain knowledge, and heuristics
        """
        causal_relations = []
        
        for var1, var2, correlation_strength in correlations:
            # Determine direction using heuristics
            direction = await self._infer_direction(var1, var2)
            
            if direction == "forward":
                cause, effect = var1, var2
            elif direction == "backward":
                cause, effect = var2, var1
            else:
                # Bidirectional or uncertain - create both with lower confidence
                causal_relations.append(CausalRelation(
                    cause=var1,
                    effect=var2,
                    strength=abs(correlation_strength) * 0.5,
                    confidence=0.4,
                    evidence_count=len(self.observation_history)
                ))
                cause, effect = var2, var1
            
            causal_relations.append(CausalRelation(
                cause=cause,
                effect=effect,
                strength=abs(correlation_strength),
                confidence=0.7,
                evidence_count=len(self.observation_history)
            ))
        
        return causal_relations
    
    async def _infer_direction(self, var1: str, var2: str) -> str:
        """
        Infer causal direction between two variables
        
        Returns: "forward", "backward", or "uncertain"
        """
        # Heuristics for causal direction
        
        # 1. Temporal heuristic (if variable names suggest time)
        if "time" in var1.lower() or "previous" in var1.lower():
            return "forward"
        if "time" in var2.lower() or "previous" in var2.lower():
            return "backward"
        
        # 2. Common cause patterns
        cause_indicators = ["cause", "input", "action", "treatment", "dose"]
        effect_indicators = ["effect", "output", "result", "outcome", "response"]
        
        var1_lower = var1.lower()
        var2_lower = var2.lower()
        
        var1_is_cause = any(ind in var1_lower for ind in cause_indicators)
        var2_is_effect = any(ind in var2_lower for ind in effect_indicators)
        
        if var1_is_cause or var2_is_effect:
            return "forward"
        
        var2_is_cause = any(ind in var2_lower for ind in cause_indicators)
        var1_is_effect = any(ind in var1_lower for ind in effect_indicators)
        
        if var2_is_cause or var1_is_effect:
            return "backward"
        
        # 3. Default: uncertain
        return "uncertain"
    
    async def identify_confounders(
        self,
        causal_relations: List[CausalRelation],
        observations: List[Dict[str, Any]]
    ) -> Dict[Tuple[str, str], List[str]]:
        """
        Identify confounding variables
        
        A confounder affects both cause and effect
        """
        confounders: Dict[Tuple[str, str], List[str]] = {}
        
        # Get all variables
        all_vars = set()
        for obs in observations:
            all_vars.update(obs.keys())
        
        # For each causal relation
        for relation in causal_relations:
            cause = relation.cause
            effect = relation.effect
            potential_confounders = []
            
            # Check each other variable
            for var in all_vars:
                if var != cause and var != effect:
                    # Check if var correlates with both cause and effect
                    cause_corr = self._compute_correlation(observations, var, cause)
                    effect_corr = self._compute_correlation(observations, var, effect)
                    
                    if abs(cause_corr) > 0.3 and abs(effect_corr) > 0.3:
                        potential_confounders.append(var)
            
            if potential_confounders:
                confounders[(cause, effect)] = potential_confounders
                relation.confounders = potential_confounders
        
        return confounders
    
    def build_causal_graph(
        self,
        causal_relations: List[CausalRelation],
        confounders: Dict[Tuple[str, str], List[str]]
    ) -> CausalGraph:
        """Build a causal graph from causal relations"""
        graph = CausalGraph()
        
        # Add all relations
        for relation in causal_relations:
            graph.add_edge(relation)
        
        return graph
    
    async def predict_intervention_effects(
        self,
        causal_graph: CausalGraph,
        intervention: Intervention
    ) -> InterventionEffect:
        """
        Predict the effects of intervening on a variable
        
        This is a core causal inference task
        """
        affected_variables = {}
        reasoning = []
        
        # Starting from intervention variable
        reasoning.append(f"Intervening on {intervention.variable} = {intervention.new_value}")
        
        # Find all downstream effects using graph traversal
        to_process = [(intervention.variable, intervention.new_value, 1.0)]
        processed = set()
        
        while to_process:
            current_var, current_value, confidence = to_process.pop(0)
            
            if current_var in processed:
                continue
            
            processed.add(current_var)
            
            # Get direct effects of current variable
            effects = causal_graph.get_effects(current_var)
            
            for effect_var in effects:
                # Find the causal relation
                relation = next(
                    (r for r in causal_graph.edges
                     if r.cause == current_var and r.effect == effect_var),
                    None
                )
                
                if relation:
                    # Predict effect value
                    effect_value = self._predict_effect_value(
                        current_value, relation
                    )
                    
                    # Propagate confidence
                    effect_confidence = confidence * relation.confidence * relation.strength
                    
                    affected_variables[effect_var] = effect_value
                    reasoning.append(
                        f"{current_var} causes {effect_var} "
                        f"(strength: {relation.strength:.2f}, "
                        f"confidence: {effect_confidence:.2f})"
                    )
                    
                    # Add to processing queue
                    to_process.append((effect_var, effect_value, effect_confidence))
        
        # Calculate overall confidence based on number of steps
        # More complex propagation generally means lower confidence
        if reasoning:
            base_confidence = 0.8
            complexity_penalty = len(reasoning) * 0.05
            overall_confidence = max(0.3, min(base_confidence - complexity_penalty, 0.95))
        else:
            overall_confidence = 0.5
        
        return InterventionEffect(
            intervention=intervention,
            affected_variables=affected_variables,
            confidence=overall_confidence,
            reasoning=reasoning
        )
    
    def _predict_effect_value(
        self,
        cause_value: Any,
        relation: CausalRelation
    ) -> Any:
        """Predict effect value given cause value and relation"""
        # Simplified prediction
        # In a real system, this would use learned functions
        
        if isinstance(cause_value, (int, float)):
            # Numeric: scale by relationship strength
            return cause_value * relation.strength
        elif isinstance(cause_value, bool):
            # Boolean: probabilistic
            return relation.strength > 0.5
        else:
            # Other: return as-is
            return cause_value
    
    async def counterfactual_reasoning(
        self,
        actual_observation: Dict[str, Any],
        counterfactual_condition: Dict[str, Any],
        causal_graph: CausalGraph
    ) -> Dict[str, Any]:
        """
        Perform counterfactual reasoning
        
        "What would have happened if X had been different?"
        
        Args:
            actual_observation: What actually happened
            counterfactual_condition: What we imagine happened instead
            causal_graph: The causal graph to use
            
        Returns:
            Predicted counterfactual outcome
        """
        # Create cache key
        cache_key = f"{actual_observation}_{counterfactual_condition}"
        
        if cache_key in self.counterfactual_cache:
            return self.counterfactual_cache[cache_key]
        
        # Start with actual observation
        counterfactual_world = actual_observation.copy()
        
        # Apply counterfactual condition
        counterfactual_world.update(counterfactual_condition)
        
        # Propagate changes through causal graph
        for changed_var, new_value in counterfactual_condition.items():
            intervention = Intervention(
                variable=changed_var,
                new_value=new_value
            )
            
            effects = await self.predict_intervention_effects(
                causal_graph, intervention
            )
            
            # Update counterfactual world
            counterfactual_world.update(effects.affected_variables)
        
        result = {
            "actual": actual_observation,
            "counterfactual_condition": counterfactual_condition,
            "counterfactual_outcome": counterfactual_world,
            "difference": self._compute_differences(
                actual_observation, counterfactual_world
            )
        }
        
        # Cache result
        self.counterfactual_cache[cache_key] = result
        
        return result
    
    def _compute_differences(
        self,
        actual: Dict[str, Any],
        counterfactual: Dict[str, Any]
    ) -> Dict[str, Tuple[Any, Any]]:
        """Compute differences between actual and counterfactual"""
        differences = {}
        
        all_keys = set(actual.keys()) | set(counterfactual.keys())
        
        for key in all_keys:
            actual_value = actual.get(key)
            counterfactual_value = counterfactual.get(key)
            
            if actual_value != counterfactual_value:
                differences[key] = (actual_value, counterfactual_value)
        
        return differences
    
    def identify_key_causes(self, causal_graph: CausalGraph) -> List[Tuple[str, int]]:
        """
        Identify the most influential variables in the causal graph
        
        Returns: List of (variable, influence_score) tuples
        """
        influence_scores = {}
        
        for node in causal_graph.nodes:
            # Count direct and indirect effects
            direct_effects = len(causal_graph.get_effects(node))
            
            # Approximate indirect effects through descendants
            descendants = self._get_descendants(causal_graph, node)
            indirect_effects = len(descendants) - direct_effects
            
            # Compute influence score using defined weights
            influence = (direct_effects * self.DIRECT_EFFECT_WEIGHT + 
                        indirect_effects * self.INDIRECT_EFFECT_WEIGHT)
            influence_scores[node] = influence
        
        # Sort by influence
        sorted_influences = sorted(
            influence_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return sorted_influences
    
    def _get_descendants(
        self,
        graph: CausalGraph,
        node: str,
        visited: Optional[Set[str]] = None
    ) -> Set[str]:
        """Get all descendants of a node in the causal graph"""
        if visited is None:
            visited = set()
        
        if node in visited:
            return visited
        
        visited.add(node)
        
        # Get direct effects
        effects = graph.get_effects(node)
        
        # Recursively get their descendants
        for effect in effects:
            if effect not in visited:
                self._get_descendants(graph, effect, visited)
        
        return visited
    
    async def explain_causality(
        self,
        causal_graph: CausalGraph,
        cause: str,
        effect: str
    ) -> Dict[str, Any]:
        """
        Explain how one variable causes another
        
        Finds causal paths and mechanisms
        """
        # Find all paths from cause to effect
        paths = self._find_causal_paths(causal_graph, cause, effect)
        
        if not paths:
            return {
                "explanation": f"No causal path found from {cause} to {effect}",
                "paths": [],
                "confidence": 0.0
            }
        
        # Analyze paths
        explanations = []
        total_confidence = 0.0
        
        for path in paths:
            path_explanation = self._explain_path(causal_graph, path)
            explanations.append(path_explanation)
            total_confidence += path_explanation["confidence"]
        
        avg_confidence = total_confidence / len(paths) if paths else 0.0
        
        return {
            "explanation": f"{cause} affects {effect} through {len(paths)} causal path(s)",
            "paths": explanations,
            "confidence": avg_confidence,
            "strongest_path": max(explanations, key=lambda x: x["confidence"]) if explanations else None
        }
    
    def _find_causal_paths(
        self,
        graph: CausalGraph,
        start: str,
        end: str,
        current_path: Optional[List[str]] = None
    ) -> List[List[str]]:
        """Find all causal paths from start to end"""
        if current_path is None:
            current_path = [start]
        
        if start == end:
            return [current_path]
        
        paths = []
        effects = graph.get_effects(start)
        
        for effect in effects:
            if effect not in current_path:  # Avoid cycles
                new_paths = self._find_causal_paths(
                    graph, effect, end, current_path + [effect]
                )
                paths.extend(new_paths)
        
        return paths
    
    def _explain_path(
        self,
        graph: CausalGraph,
        path: List[str]
    ) -> Dict[str, Any]:
        """Explain a single causal path"""
        steps = []
        path_confidence = 1.0
        
        for i in range(len(path) - 1):
            cause = path[i]
            effect = path[i + 1]
            
            # Find relation
            relation = next(
                (r for r in graph.edges
                 if r.cause == cause and r.effect == effect),
                None
            )
            
            if relation:
                steps.append(f"{cause} → {effect} (strength: {relation.strength:.2f})")
                path_confidence *= relation.confidence * relation.strength
        
        return {
            "path": " → ".join(path),
            "steps": steps,
            "confidence": path_confidence,
            "length": len(path) - 1
        }
