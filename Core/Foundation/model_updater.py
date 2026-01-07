"""
Continuous Model Update System for Elysia.
Enables incremental and evolutionary model improvements.
"""

import time
import json
import copy
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import numpy as np
from collections import defaultdict


@dataclass
class ModelVersion:
    """모델 버전 정보 (Model Version Information)"""
    
    version_id: str
    timestamp: float
    performance_metrics: Dict[str, float]
    changes: List[str]
    parent_version: Optional[str] = None
    is_active: bool = False
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ModelVersion':
        """Create from dictionary"""
        return cls(**data)


class ContinuousUpdater:
    """
    지속적으로 모델을 업데이트하는 시스템 (Continuous Model Update System)
    
    Features:
    - Incremental model updates based on new experiences
    - Model version management with rollback capability
    - A/B testing for validation
    - Evolutionary updates with mutation
    - Performance monitoring and automatic improvement
    """
    
    def __init__(self, save_dir: str = "data/models", update_threshold: int = 100):
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(parents=True, exist_ok=True)
        
        self.update_threshold = update_threshold  # 경험 개수 임계값
        self.model_versions: List[ModelVersion] = []
        self.current_version: Optional[ModelVersion] = None
        
        # Update tracking
        self.pending_experiences = []
        self.update_history: List[Dict] = []
        
        # Performance tracking
        self.performance_buffer: Dict[str, List[float]] = defaultdict(list)
        
        # A/B testing
        self.ab_test_active = False
        self.test_version: Optional[ModelVersion] = None
        self.control_metrics: List[float] = []
        self.test_metrics: List[float] = []
        
        self._load_versions()
    
    async def incremental_update(self, new_experiences: List[Any]) -> Dict[str, Any]:
        """
        점진적 모델 업데이트 (Incremental Model Update)
        
        Args:
            new_experiences: List of new Experience objects
            
        Returns:
            Update result with metrics and status
        """
        # Add to pending queue
        self.pending_experiences.extend(new_experiences)
        
        # Check if we have enough experiences to trigger update
        if len(self.pending_experiences) < self.update_threshold:
            return {
                "status": "pending",
                "pending_count": len(self.pending_experiences),
                "threshold": self.update_threshold,
                "message": f"Waiting for more experiences ({len(self.pending_experiences)}/{self.update_threshold})"
            }
        
        # Perform update
        update_result = await self._perform_incremental_update()
        
        # Clear pending experiences
        self.pending_experiences = []
        
        return update_result
    
    async def _perform_incremental_update(self) -> Dict[str, Any]:
        """실제 업데이트 수행 (Perform Actual Update)"""
        
        # 1. Extract patterns from new experiences
        patterns = self._extract_patterns_from_experiences(self.pending_experiences)
        
        # 2. Calculate weight adjustments
        weight_adjustments = self._calculate_weight_adjustments(patterns)
        
        # 3. Create new model version
        new_version = self._create_updated_version(weight_adjustments)
        
        # 4. Test new version
        test_results = await self._test_version(new_version)
        
        # 5. Decide whether to apply or rollback
        if test_results["improved"]:
            self._apply_version(new_version)
            result = {
                "status": "success",
                "version_id": new_version.version_id,
                "improvement": test_results["improvement_percent"],
                "message": "Model updated successfully"
            }
        else:
            result = {
                "status": "rollback",
                "reason": "No improvement detected",
                "test_results": test_results,
                "message": "Update rolled back - no improvement"
            }
        
        # Record update history
        self.update_history.append({
            "timestamp": time.time(),
            "result": result,
            "experience_count": len(self.pending_experiences)
        })
        
        return result
    
    async def evolutionary_update(self, generations: int = 5, population_size: int = 10) -> Dict[str, Any]:
        """
        진화적 모델 업데이트 (Evolutionary Model Update)
        
        Uses evolutionary algorithms to find better model configurations.
        
        Args:
            generations: Number of evolution generations
            population_size: Size of population per generation
            
        Returns:
            Best model version and evolution results
        """
        if not self.current_version:
            return {
                "status": "error",
                "message": "No current model version to evolve from"
            }
        
        evolution_history = []
        best_version = self.current_version
        best_score = self._evaluate_version(best_version)
        
        for generation in range(generations):
            # 1. Generate population (mutations of current best)
            population = self._generate_population(best_version, population_size)
            
            # 2. Evaluate each variant
            scores = []
            for variant in population:
                score = self._evaluate_version(variant)
                scores.append(score)
            
            # 3. Select best variant
            best_idx = np.argmax(scores)
            gen_best_version = population[best_idx]
            gen_best_score = scores[best_idx]
            
            # 4. Update if improved
            if gen_best_score > best_score:
                best_version = gen_best_version
                best_score = gen_best_score
                improvement = ((best_score - self._evaluate_version(self.current_version)) / 
                              self._evaluate_version(self.current_version) * 100)
            else:
                improvement = 0.0
            
            evolution_history.append({
                "generation": generation,
                "best_score": gen_best_score,
                "avg_score": np.mean(scores),
                "improvement": improvement
            })
        
        # Apply best version if significantly better
        if best_score > self._evaluate_version(self.current_version) * 1.05:  # 5% improvement threshold
            self._apply_version(best_version)
            status = "success"
            message = f"Evolution successful - {((best_score / self._evaluate_version(self.current_version) - 1) * 100):.2f}% improvement"
        else:
            status = "no_improvement"
            message = "Evolution completed but no significant improvement"
        
        return {
            "status": status,
            "message": message,
            "best_version": best_version.version_id if status == "success" else None,
            "evolution_history": evolution_history,
            "final_score": best_score
        }
    
    async def start_ab_test(self, test_duration_seconds: int = 3600) -> Dict[str, Any]:
        """
        A/B 테스트 시작 (Start A/B Testing)
        
        Compares current model with a variant to validate improvements.
        
        Args:
            test_duration_seconds: Duration of A/B test in seconds
            
        Returns:
            A/B test configuration
        """
        if self.ab_test_active:
            return {
                "status": "error",
                "message": "A/B test already in progress"
            }
        
        # Generate test variant (small mutation)
        self.test_version = self._generate_population(self.current_version, 1)[0]
        
        self.ab_test_active = True
        self.control_metrics = []
        self.test_metrics = []
        
        return {
            "status": "started",
            "control_version": self.current_version.version_id,
            "test_version": self.test_version.version_id,
            "duration_seconds": test_duration_seconds,
            "message": "A/B test started"
        }
    
    async def record_ab_metric(self, version_type: str, metric_value: float):
        """Record metric for A/B test"""
        if not self.ab_test_active:
            return
        
        if version_type == "control":
            self.control_metrics.append(metric_value)
        elif version_type == "test":
            self.test_metrics.append(metric_value)
    
    async def finalize_ab_test(self) -> Dict[str, Any]:
        """
        A/B 테스트 종료 및 결과 분석 (Finalize A/B Test)
        
        Returns:
            Test results and decision
        """
        if not self.ab_test_active:
            return {
                "status": "error",
                "message": "No active A/B test"
            }
        
        # Calculate statistics
        control_mean = np.mean(self.control_metrics) if self.control_metrics else 0.0
        test_mean = np.mean(self.test_metrics) if self.test_metrics else 0.0
        
        improvement = ((test_mean - control_mean) / control_mean * 100) if control_mean > 0 else 0.0
        
        # Statistical significance (simple t-test approximation)
        if len(self.control_metrics) > 1 and len(self.test_metrics) > 1:
            control_std = np.std(self.control_metrics)
            test_std = np.std(self.test_metrics)
            pooled_std = np.sqrt((control_std**2 + test_std**2) / 2)
            effect_size = abs(test_mean - control_mean) / pooled_std if pooled_std > 0 else 0.0
            significant = effect_size > 0.5  # Medium effect size threshold
        else:
            significant = False
        
        # Decision
        if improvement > 2.0 and significant:  # 2% improvement threshold
            self._apply_version(self.test_version)
            decision = "adopt_test"
            message = f"Test version adopted - {improvement:.2f}% improvement"
        else:
            decision = "keep_control"
            message = f"Control version kept - insufficient improvement ({improvement:.2f}%)"
        
        # Reset A/B test state
        self.ab_test_active = False
        self.test_version = None
        self.control_metrics = []
        self.test_metrics = []
        
        return {
            "status": "completed",
            "decision": decision,
            "control_mean": control_mean,
            "test_mean": test_mean,
            "improvement_percent": improvement,
            "statistically_significant": significant,
            "message": message
        }
    
    def _extract_patterns_from_experiences(self, experiences: List[Any]) -> List[Dict]:
        """Extract learning patterns from experiences"""
        patterns = []
        
        # Group by feedback score
        positive_experiences = [e for e in experiences if hasattr(e, 'feedback') and e.feedback > 0.5]
        negative_experiences = [e for e in experiences if hasattr(e, 'feedback') and e.feedback < -0.5]
        
        # Extract patterns from positive experiences
        for exp in positive_experiences:
            patterns.append({
                "type": "success",
                "context_features": self._extract_features(exp.context if hasattr(exp, 'context') else {}),
                "action_type": exp.action.get("type") if hasattr(exp, 'action') and isinstance(exp.action, dict) else "unknown",
                "strength": abs(exp.feedback) if hasattr(exp, 'feedback') else 0.0
            })
        
        # Extract patterns from negative experiences
        for exp in negative_experiences:
            patterns.append({
                "type": "failure",
                "context_features": self._extract_features(exp.context if hasattr(exp, 'context') else {}),
                "action_type": exp.action.get("type") if hasattr(exp, 'action') and isinstance(exp.action, dict) else "unknown",
                "strength": abs(exp.feedback) if hasattr(exp, 'feedback') else 0.0
            })
        
        return patterns
    
    def _extract_features(self, context: Dict) -> List[str]:
        """Extract key features from context"""
        features = []
        for key, value in context.items():
            if isinstance(value, (str, int, float, bool)):
                features.append(f"{key}={value}")
        return features[:10]  # Limit to top 10 features
    
    def _calculate_weight_adjustments(self, patterns: List[Dict]) -> Dict[str, float]:
        """Calculate model weight adjustments based on patterns"""
        adjustments = {}
        
        # Simple weight adjustment based on pattern frequency and strength
        for pattern in patterns:
            pattern_key = f"{pattern['type']}_{pattern['action_type']}"
            adjustment = pattern['strength'] * (0.1 if pattern['type'] == 'success' else -0.1)
            
            if pattern_key in adjustments:
                adjustments[pattern_key] += adjustment
            else:
                adjustments[pattern_key] = adjustment
        
        return adjustments
    
    def _create_updated_version(self, weight_adjustments: Dict[str, float]) -> ModelVersion:
        """Create new model version with adjustments"""
        version_id = f"v{len(self.model_versions) + 1}_{int(time.time())}"
        
        # Calculate new performance (simulated)
        base_performance = self.current_version.performance_metrics.copy() if self.current_version else {
            "accuracy": 0.7,
            "efficiency": 0.75,
            "satisfaction": 0.8
        }
        
        # Apply small improvements based on adjustments
        for metric in base_performance:
            adjustment = sum(adj for adj in weight_adjustments.values()) / len(weight_adjustments) if weight_adjustments else 0.0
            base_performance[metric] = min(1.0, max(0.0, base_performance[metric] + adjustment * 0.01))
        
        new_version = ModelVersion(
            version_id=version_id,
            timestamp=time.time(),
            performance_metrics=base_performance,
            changes=[f"Applied {len(weight_adjustments)} weight adjustments"],
            parent_version=self.current_version.version_id if self.current_version else None,
            is_active=False
        )
        
        return new_version
    
    async def _test_version(self, version: ModelVersion) -> Dict[str, Any]:
        """Test a model version against validation data"""
        # Simulate testing
        current_score = self._evaluate_version(self.current_version) if self.current_version else 0.5
        new_score = self._evaluate_version(version)
        
        improved = new_score > current_score
        improvement_percent = ((new_score - current_score) / current_score * 100) if current_score > 0 else 0.0
        
        return {
            "improved": improved,
            "current_score": current_score,
            "new_score": new_score,
            "improvement_percent": improvement_percent
        }
    
    def _evaluate_version(self, version: ModelVersion) -> float:
        """Evaluate model version performance"""
        if not version:
            return 0.0
        
        # Aggregate performance metrics
        metrics = version.performance_metrics
        return sum(metrics.values()) / len(metrics) if metrics else 0.0
    
    def _apply_version(self, version: ModelVersion):
        """Apply a model version as current"""
        # Deactivate current version
        if self.current_version:
            self.current_version.is_active = False
        
        # Activate new version
        version.is_active = True
        self.model_versions.append(version)
        self.current_version = version
        
        # Save
        self._save_versions()
    
    def _generate_population(self, parent: ModelVersion, size: int) -> List[ModelVersion]:
        """Generate population of model variants through mutation"""
        population = []
        
        for i in range(size):
            # Create mutated version
            mutated_metrics = parent.performance_metrics.copy()
            
            # Apply random mutations
            for metric in mutated_metrics:
                mutation = np.random.normal(0, 0.02)  # Small random change
                mutated_metrics[metric] = min(1.0, max(0.0, mutated_metrics[metric] + mutation))
            
            variant = ModelVersion(
                version_id=f"{parent.version_id}_mut_{i}",
                timestamp=time.time(),
                performance_metrics=mutated_metrics,
                changes=[f"Mutation {i} of {parent.version_id}"],
                parent_version=parent.version_id,
                is_active=False
            )
            
            population.append(variant)
        
        return population
    
    def _load_versions(self):
        """Load model versions from disk"""
        versions_file = self.save_dir / "model_versions.json"
        if versions_file.exists():
            with open(versions_file, 'r') as f:
                data = json.load(f)
                self.model_versions = [ModelVersion.from_dict(v) for v in data["versions"]]
                
                # Find active version
                for version in self.model_versions:
                    if version.is_active:
                        self.current_version = version
                        break
    
    def _save_versions(self):
        """Save model versions to disk"""
        versions_file = self.save_dir / "model_versions.json"
        data = {
            "versions": [v.to_dict() for v in self.model_versions],
            "last_updated": time.time()
        }
        
        with open(versions_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_version_history(self) -> List[Dict]:
        """Get model version history"""
        return [v.to_dict() for v in self.model_versions]
    
    def rollback_to_version(self, version_id: str) -> Dict[str, Any]:
        """Rollback to a specific model version"""
        for version in self.model_versions:
            if version.version_id == version_id:
                self._apply_version(version)
                return {
                    "status": "success",
                    "version_id": version_id,
                    "message": f"Rolled back to version {version_id}"
                }
        
        return {
            "status": "error",
            "message": f"Version {version_id} not found"
        }
