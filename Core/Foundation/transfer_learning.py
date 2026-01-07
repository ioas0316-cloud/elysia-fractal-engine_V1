"""
Universal Transfer Learning System
Phase 13: 범용 인공지능 향해 (Towards AGI)

Enables rapid learning of new domains through transfer learning,
meta-learning, and few-shot learning capabilities.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Set
import asyncio
from datetime import datetime


@dataclass
class DomainKnowledge:
    """Knowledge representation for a domain"""
    domain: str
    concepts: List[str] = field(default_factory=list)
    patterns: Dict[str, Any] = field(default_factory=dict)
    examples: List[Dict] = field(default_factory=list)
    proficiency: float = 0.0  # 0.0 to 1.0
    learned_at: datetime = field(default_factory=datetime.now)
    
    
@dataclass
class TransferableKnowledge:
    """Knowledge that can be transferred across domains"""
    knowledge_type: str  # "pattern", "concept", "strategy", "heuristic"
    content: Dict[str, Any]
    source_domains: List[str]
    applicability_score: float  # How well it applies to new domain
    abstraction_level: str  # "low", "medium", "high"


class UniversalTransferLearner:
    """
    Advanced Transfer Learning System
    
    Enables rapid learning of new domains by:
    1. Identifying similar domains
    2. Extracting transferable knowledge
    3. Few-shot learning with minimal examples
    4. Meta-learning (learning how to learn)
    """
    
    def __init__(self):
        self.domain_knowledge: Dict[str, DomainKnowledge] = {}
        self.transfer_patterns: Dict[str, List[TransferableKnowledge]] = {}
        self.learning_strategies: Dict[str, Dict] = {}
        self.meta_learning_history: List[Dict] = []
        
        # Initialize with some base domains
        self._initialize_base_domains()
    
    def _initialize_base_domains(self):
        """Initialize with foundational knowledge domains"""
        base_domains = [
            "language", "mathematics", "logic", "pattern_recognition",
            "problem_solving", "creativity", "social_interaction"
        ]
        
        for domain in base_domains:
            self.domain_knowledge[domain] = DomainKnowledge(
                domain=domain,
                proficiency=0.5,  # Base proficiency
                concepts=self._get_base_concepts(domain)
            )
    
    def _get_base_concepts(self, domain: str) -> List[str]:
        """Get foundational concepts for a domain"""
        base_concepts = {
            "language": ["syntax", "semantics", "pragmatics", "grammar"],
            "mathematics": ["numbers", "operations", "equations", "functions"],
            "logic": ["reasoning", "inference", "deduction", "induction"],
            "pattern_recognition": ["similarity", "regularity", "anomaly"],
            "problem_solving": ["decomposition", "search", "optimization"],
            "creativity": ["novelty", "combination", "transformation"],
            "social_interaction": ["communication", "empathy", "cooperation"]
        }
        return base_concepts.get(domain, [])
    
    async def learn_new_domain(
        self,
        domain: str,
        examples: List[Dict],
        target_proficiency: float = 0.7
    ) -> DomainKnowledge:
        """
        Learn a new domain rapidly using transfer learning
        
        Args:
            domain: Name of the new domain
            examples: Few-shot examples for the domain
            target_proficiency: Target proficiency level (0.0 to 1.0)
            
        Returns:
            DomainKnowledge object with learned information
        """
        # 1. Identify similar domains
        similar_domains = await self.find_similar_domains(domain, examples)
        
        # 2. Extract transferable knowledge
        transferable_knowledge = await self.extract_transferable_knowledge(
            similar_domains, domain
        )
        
        # 3. Few-shot learning with examples
        domain_model = await self.few_shot_learn(
            domain, examples, transferable_knowledge
        )
        
        # 4. Iterative improvement until proficiency target
        iterations = 0
        max_iterations = 10
        
        while domain_model.proficiency < target_proficiency and iterations < max_iterations:
            # Self-generate more examples for practice
            synthetic_examples = await self.generate_synthetic_examples(
                domain, domain_model
            )
            
            # Continue learning
            await self.incremental_learn(domain_model, synthetic_examples)
            iterations += 1
        
        # 5. Store the learned domain
        self.domain_knowledge[domain] = domain_model
        
        # 6. Meta-learn from this experience
        await self.meta_learn_from_experience(domain, iterations, examples)
        
        return domain_model
    
    async def find_similar_domains(
        self,
        target_domain: str,
        examples: List[Dict]
    ) -> List[str]:
        """
        Find domains similar to the target domain
        
        Uses example characteristics to determine similarity
        """
        similarities = []
        
        # Extract features from examples
        target_features = self._extract_domain_features(examples)
        
        # Compare with existing domains
        for domain_name, domain_knowledge in self.domain_knowledge.items():
            if domain_knowledge.examples:
                domain_features = self._extract_domain_features(
                    domain_knowledge.examples
                )
                similarity = self._compute_feature_similarity(
                    target_features, domain_features
                )
                similarities.append((domain_name, similarity))
        
        # Sort by similarity and return top matches
        similarities.sort(key=lambda x: x[1], reverse=True)
        return [domain for domain, _ in similarities[:5] if _ > 0.3]
    
    def _extract_domain_features(self, examples: List[Dict]) -> Dict[str, Any]:
        """Extract key features from domain examples"""
        if not examples:
            return {}
        
        features = {
            "num_examples": len(examples),
            "complexity": self._estimate_complexity(examples),
            "data_types": self._identify_data_types(examples),
            "structure": self._analyze_structure(examples)
        }
        return features
    
    def _estimate_complexity(self, examples: List[Dict]) -> float:
        """Estimate complexity of examples (0.0 to 1.0)"""
        if not examples:
            return 0.0
        
        # Simple heuristic: based on nesting and size
        total_complexity = 0.0
        for example in examples:
            example_str = str(example)
            # Complexity factors
            length_factor = min(len(example_str) / 1000, 1.0)
            nesting_factor = example_str.count('{') / 10
            total_complexity += (length_factor + nesting_factor) / 2
        
        return min(total_complexity / len(examples), 1.0)
    
    def _identify_data_types(self, examples: List[Dict]) -> Set[str]:
        """Identify data types used in examples"""
        data_types = set()
        
        for example in examples:
            for value in example.values():
                data_types.add(type(value).__name__)
        
        return data_types
    
    def _analyze_structure(self, examples: List[Dict]) -> str:
        """Analyze structural pattern of examples"""
        if not examples:
            return "empty"
        
        # Check if examples have consistent keys
        key_sets = [set(ex.keys()) for ex in examples]
        if all(ks == key_sets[0] for ks in key_sets):
            return "structured"
        else:
            return "semi_structured"
    
    def _compute_feature_similarity(
        self,
        features1: Dict[str, Any],
        features2: Dict[str, Any]
    ) -> float:
        """Compute similarity between two feature sets"""
        if not features1 or not features2:
            return 0.0
        
        # Complexity similarity
        complexity_sim = 1.0 - abs(
            features1.get("complexity", 0) - features2.get("complexity", 0)
        )
        
        # Data type overlap
        types1 = features1.get("data_types", set())
        types2 = features2.get("data_types", set())
        if types1 and types2:
            type_sim = len(types1 & types2) / len(types1 | types2)
        else:
            type_sim = 0.0
        
        # Structure similarity
        struct1 = features1.get("structure", "")
        struct2 = features2.get("structure", "")
        struct_sim = 1.0 if struct1 == struct2 else 0.5
        
        # Weighted average
        return (complexity_sim * 0.3 + type_sim * 0.4 + struct_sim * 0.3)
    
    async def extract_transferable_knowledge(
        self,
        source_domains: List[str],
        target_domain: str
    ) -> List[TransferableKnowledge]:
        """
        Extract knowledge that can be transferred from source domains
        to target domain
        """
        transferable = []
        
        for source_domain in source_domains:
            if source_domain not in self.domain_knowledge:
                continue
            
            domain_knowledge = self.domain_knowledge[source_domain]
            
            # Extract patterns
            for pattern_name, pattern_data in domain_knowledge.patterns.items():
                # Determine if pattern is transferable
                applicability = await self._assess_transferability(
                    pattern_data, target_domain
                )
                
                if applicability > 0.5:
                    transferable.append(TransferableKnowledge(
                        knowledge_type="pattern",
                        content={"name": pattern_name, "data": pattern_data},
                        source_domains=[source_domain],
                        applicability_score=applicability,
                        abstraction_level=self._determine_abstraction_level(pattern_data)
                    ))
            
            # Extract concepts
            for concept in domain_knowledge.concepts:
                applicability = 0.6  # Concepts are generally transferable
                transferable.append(TransferableKnowledge(
                    knowledge_type="concept",
                    content={"concept": concept},
                    source_domains=[source_domain],
                    applicability_score=applicability,
                    abstraction_level="high"
                ))
        
        # Sort by applicability
        transferable.sort(key=lambda x: x.applicability_score, reverse=True)
        
        return transferable
    
    async def _assess_transferability(
        self,
        knowledge: Any,
        target_domain: str
    ) -> float:
        """Assess how transferable a piece of knowledge is"""
        # Simple heuristic: higher-level abstractions are more transferable
        # This would be more sophisticated in a real implementation
        return 0.7  # Default transferability score
    
    def _determine_abstraction_level(self, knowledge: Any) -> str:
        """Determine abstraction level of knowledge"""
        # Simple heuristic based on structure
        if isinstance(knowledge, dict):
            depth = self._get_dict_depth(knowledge)
            if depth > 3:
                return "high"
            elif depth > 1:
                return "medium"
        return "low"
    
    def _get_dict_depth(self, d: Dict, level: int = 0) -> int:
        """Get maximum nesting depth of a dictionary"""
        if not isinstance(d, dict):
            return level
        if not d:
            return level + 1
        return max(self._get_dict_depth(v, level + 1) for v in d.values())
    
    async def few_shot_learn(
        self,
        domain: str,
        examples: List[Dict],
        transferable_knowledge: List[TransferableKnowledge]
    ) -> DomainKnowledge:
        """
        Learn from few examples using transferred knowledge
        """
        # Extract patterns from examples
        patterns = self._extract_patterns_from_examples(examples)
        
        # Extract concepts
        concepts = self._extract_concepts_from_examples(examples)
        
        # Add transferred concepts
        for tk in transferable_knowledge:
            if tk.knowledge_type == "concept":
                concepts.append(tk.content["concept"])
            elif tk.knowledge_type == "pattern":
                patterns[tk.content["name"]] = tk.content["data"]
        
        # Estimate initial proficiency based on examples and transferred knowledge
        initial_proficiency = min(
            0.3 + (len(examples) * 0.05) + (len(transferable_knowledge) * 0.02),
            0.8
        )
        
        return DomainKnowledge(
            domain=domain,
            concepts=list(set(concepts)),
            patterns=patterns,
            examples=examples,
            proficiency=initial_proficiency
        )
    
    def _extract_patterns_from_examples(self, examples: List[Dict]) -> Dict[str, Any]:
        """Extract patterns from examples"""
        patterns = {}
        
        if not examples:
            return patterns
        
        # Common key pattern
        if len(examples) > 1:
            common_keys = set(examples[0].keys())
            for example in examples[1:]:
                common_keys &= set(example.keys())
            
            if common_keys:
                patterns["common_structure"] = {
                    "keys": list(common_keys),
                    "count": len(common_keys)
                }
        
        # Value type patterns
        type_patterns = {}
        for key in examples[0].keys():
            types = [type(ex.get(key)).__name__ for ex in examples if key in ex]
            if types:
                type_patterns[key] = max(set(types), key=types.count)
        
        if type_patterns:
            patterns["type_pattern"] = type_patterns
        
        return patterns
    
    def _extract_concepts_from_examples(self, examples: List[Dict]) -> List[str]:
        """Extract concepts from examples"""
        concepts = set()
        
        for example in examples:
            # Add keys as concepts
            concepts.update(example.keys())
            
            # Add string values as potential concepts
            for value in example.values():
                if isinstance(value, str) and len(value.split()) <= 3:
                    concepts.add(value.lower())
        
        return list(concepts)
    
    async def generate_synthetic_examples(
        self,
        domain: str,
        domain_model: DomainKnowledge
    ) -> List[Dict]:
        """Generate synthetic examples for continued learning"""
        synthetic = []
        
        # Generate examples based on patterns
        if "common_structure" in domain_model.patterns:
            structure = domain_model.patterns["common_structure"]
            keys = structure["keys"]
            
            # Generate 3-5 synthetic examples
            for i in range(3):
                example = {}
                for key in keys:
                    # Generate appropriate value based on type pattern
                    if "type_pattern" in domain_model.patterns:
                        value_type = domain_model.patterns["type_pattern"].get(key, "str")
                        example[key] = self._generate_value_of_type(value_type, i)
                    else:
                        example[key] = f"synthetic_value_{i}"
                
                synthetic.append(example)
        
        return synthetic
    
    def _generate_value_of_type(self, type_name: str, seed: int) -> Any:
        """Generate a value of specified type"""
        if type_name == "int":
            return seed * 10
        elif type_name == "float":
            return seed * 1.5
        elif type_name == "bool":
            return seed % 2 == 0
        elif type_name == "list":
            return [seed, seed + 1, seed + 2]
        else:  # str or other
            return f"generated_{seed}"
    
    async def incremental_learn(
        self,
        domain_model: DomainKnowledge,
        new_examples: List[Dict]
    ):
        """Incrementally improve domain knowledge with new examples"""
        # Add examples
        domain_model.examples.extend(new_examples)
        
        # Update patterns
        new_patterns = self._extract_patterns_from_examples(new_examples)
        domain_model.patterns.update(new_patterns)
        
        # Update concepts
        new_concepts = self._extract_concepts_from_examples(new_examples)
        domain_model.concepts = list(set(domain_model.concepts + new_concepts))
        
        # Improve proficiency
        proficiency_gain = len(new_examples) * 0.02
        domain_model.proficiency = min(domain_model.proficiency + proficiency_gain, 1.0)
    
    async def meta_transfer(self, source_task: str, target_task: str) -> Dict[str, Any]:
        """
        Meta-transfer: Transfer the learning strategy itself
        
        This transfers "how to learn" rather than just knowledge
        """
        if source_task not in self.learning_strategies:
            return {"strategy": "default", "confidence": 0.3}
        
        source_strategy = self.learning_strategies[source_task]
        
        # Adapt strategy for target task
        adapted_strategy = {
            "approach": source_strategy.get("approach", "few_shot"),
            "iterations": source_strategy.get("iterations", 5),
            "example_generation": source_strategy.get("example_generation", True),
            "confidence": 0.7
        }
        
        return adapted_strategy
    
    async def meta_learn_from_experience(
        self,
        domain: str,
        iterations: int,
        initial_examples: List[Dict]
    ):
        """Learn from the learning experience itself"""
        learning_record = {
            "domain": domain,
            "iterations_needed": iterations,
            "initial_examples": len(initial_examples),
            "final_proficiency": self.domain_knowledge[domain].proficiency,
            "timestamp": datetime.now().isoformat()
        }
        
        self.meta_learning_history.append(learning_record)
        
        # Update learning strategies
        self.learning_strategies[domain] = {
            "approach": "few_shot" if len(initial_examples) < 10 else "standard",
            "iterations": iterations,
            "example_generation": iterations > 3,
            "optimal_examples": len(initial_examples)
        }
    
    def get_domain_proficiency(self, domain: str) -> float:
        """Get proficiency level for a domain"""
        if not domain:
            return 0.0
        if domain in self.domain_knowledge:
            return self.domain_knowledge[domain].proficiency
        return 0.0
    
    def list_known_domains(self) -> List[str]:
        """List all known domains"""
        return list(self.domain_knowledge.keys())
