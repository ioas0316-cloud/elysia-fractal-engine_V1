"""
Self-Reflection System for Elysia.
Analyzes own performance and generates improvement plans.
"""

import time
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from collections import defaultdict
from pathlib import Path
import numpy as np


class SelfReflector:
    """
    자신의 행동과 성능을 반성하는 시스템 (Self-Reflection System)
    
    Features:
    - Daily performance reflection
    - Strength and weakness identification
    - Pattern discovery from experiences
    - Automatic improvement plan generation
    - Performance trend analysis
    """
    
    def __init__(self, save_dir: str = "data/reflection"):
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(parents=True, exist_ok=True)
        
        # Performance metrics
        self.daily_metrics: Dict[str, List[Dict]] = defaultdict(list)
        self.reflections_history: List[Dict] = []
        self.improvement_plans: List[Dict] = []
        
        # Analysis categories
        self.categories = [
            "thought_quality",
            "resonance_accuracy",
            "response_time",
            "user_satisfaction",
            "learning_efficiency",
            "error_handling"
        ]
        
        self._load_history()
    
    async def daily_reflection(self, experiences: List[Any] = None) -> Dict[str, Any]:
        """
        일일 반성 - 하루 동안의 경험 분석 (Daily Reflection)
        
        Args:
            experiences: List of Experience objects from today
        
        Returns:
            Comprehensive daily reflection with insights and improvement plan
        """
        today = datetime.now().strftime("%Y-%m-%d")
        
        # If no experiences provided, use collected metrics
        if experiences is None:
            experiences = self.daily_metrics.get(today, [])
        
        if not experiences:
            return {
                "date": today,
                "message": "No experiences to reflect on today",
                "reflection": None,
                "improvement_plan": None
            }
        
        # Analyze experiences
        reflection = {
            "date": today,
            "total_experiences": len(experiences),
            "strengths": self._identify_strengths(experiences),
            "weaknesses": self._identify_weaknesses(experiences),
            "patterns": self._discover_patterns(experiences),
            "improvements": self._suggest_improvements(experiences),
            "performance_summary": self._summarize_performance(experiences)
        }
        
        # Generate improvement plan
        improvement_plan = await self.create_improvement_plan(reflection)
        reflection["improvement_plan"] = improvement_plan
        
        # Save reflection
        self.reflections_history.append(reflection)
        self._save_reflection(reflection)
        
        return reflection
    
    async def performance_analysis(self, experiences: List[Any] = None, 
                                   period_days: int = 7) -> Dict[str, Any]:
        """
        성능 분석 - 어떤 영역이 강하고 약한지 (Performance Analysis)
        
        Args:
            experiences: List of experiences to analyze
            period_days: Number of days to include in analysis
        
        Returns:
            Detailed performance analysis across all categories
        """
        if experiences is None:
            # Gather experiences from recent days
            experiences = self._get_recent_experiences(period_days)
        
        analysis = {
            "period": f"Last {period_days} days",
            "total_experiences": len(experiences),
            "categories": {}
        }
        
        for category in self.categories:
            analysis["categories"][category] = self._analyze_category(
                category, experiences
            )
        
        # Overall performance score
        category_scores = [
            cat_data["score"] 
            for cat_data in analysis["categories"].values()
        ]
        analysis["overall_score"] = np.mean(category_scores) if category_scores else 0.0
        
        # Trends
        analysis["trends"] = self._analyze_trends(experiences, period_days)
        
        # Comparative analysis
        analysis["vs_previous_period"] = self._compare_with_previous_period(
            experiences, period_days
        )
        
        return analysis
    
    async def create_improvement_plan(self, reflection: Dict) -> Dict[str, Any]:
        """
        자기 개선 계획 생성 (Create Improvement Plan)
        
        Args:
            reflection: Daily reflection data
        
        Returns:
            Structured improvement plan with specific actions
        """
        plan = {
            "created_at": datetime.now().isoformat(),
            "based_on_reflection": reflection["date"],
            "priority_areas": [],
            "action_items": [],
            "success_criteria": [],
            "timeline": "1 week"
        }
        
        # Identify priority areas from weaknesses
        weaknesses = reflection.get("weaknesses", [])
        for weakness in weaknesses[:3]:  # Top 3 priorities
            plan["priority_areas"].append({
                "area": weakness["category"],
                "current_score": weakness["score"],
                "target_score": min(weakness["score"] + 0.2, 1.0),
                "importance": weakness.get("importance", "medium")
            })
        
        # Generate actionable items
        for weakness in weaknesses[:3]:
            actions = self._generate_actions_for_weakness(weakness)
            plan["action_items"].extend(actions)
        
        # Define success criteria
        plan["success_criteria"] = [
            {
                "metric": area["area"],
                "current": area["current_score"],
                "target": area["target_score"],
                "measurement": "daily_average"
            }
            for area in plan["priority_areas"]
        ]
        
        # Save plan
        self.improvement_plans.append(plan)
        self._save_improvement_plan(plan)
        
        return plan
    
    def track_progress(self, plan_id: Optional[int] = None) -> Dict[str, Any]:
        """
        개선 계획 진행 상황 추적 (Track Improvement Progress)
        
        Args:
            plan_id: ID of specific plan to track (default: latest)
        
        Returns:
            Progress report with completion status
        """
        if not self.improvement_plans:
            return {"message": "No improvement plans to track"}
        
        plan = self.improvement_plans[plan_id] if plan_id is not None else self.improvement_plans[-1]
        
        # Calculate progress for each priority area
        progress_report = {
            "plan_created": plan["created_at"],
            "areas": [],
            "overall_progress": 0.0,
            "status": "in_progress"
        }
        
        for area in plan["priority_areas"]:
            current_performance = self._get_current_performance(area["area"])
            progress = self._calculate_progress(
                area["current_score"],
                area["target_score"],
                current_performance
            )
            
            progress_report["areas"].append({
                "area": area["area"],
                "initial": area["current_score"],
                "target": area["target_score"],
                "current": current_performance,
                "progress": progress,
                "status": "completed" if progress >= 1.0 else "in_progress"
            })
        
        # Overall progress
        area_progress = [a["progress"] for a in progress_report["areas"]]
        progress_report["overall_progress"] = np.mean(area_progress) if area_progress else 0.0
        
        if progress_report["overall_progress"] >= 1.0:
            progress_report["status"] = "completed"
        elif progress_report["overall_progress"] >= 0.5:
            progress_report["status"] = "on_track"
        
        return progress_report
    
    def get_insights(self, period_days: int = 30) -> Dict[str, Any]:
        """
        장기적 인사이트 생성 (Generate Long-term Insights)
        
        Args:
            period_days: Number of days to analyze
        
        Returns:
            Long-term insights and recommendations
        """
        reflections = self._get_recent_reflections(period_days)
        
        if not reflections:
            return {"message": "Not enough data for insights"}
        
        insights = {
            "period": f"Last {period_days} days",
            "total_reflections": len(reflections),
            "consistent_strengths": self._find_consistent_patterns(
                reflections, "strengths"
            ),
            "persistent_challenges": self._find_consistent_patterns(
                reflections, "weaknesses"
            ),
            "improvement_trajectory": self._calculate_trajectory(reflections),
            "learning_velocity": self._calculate_learning_velocity(reflections),
            "recommendations": self._generate_recommendations(reflections)
        }
        
        return insights
    
    # Private helper methods
    
    def _identify_strengths(self, experiences: List[Any]) -> List[Dict]:
        """Identify areas of strong performance"""
        strengths = []
        
        # Analyze each category
        for category in self.categories:
            score = self._calculate_category_score(category, experiences)
            
            if score > 0.7:  # High performance threshold
                strengths.append({
                    "category": category,
                    "score": score,
                    "description": self._generate_strength_description(category, score)
                })
        
        # Sort by score
        strengths.sort(key=lambda x: x["score"], reverse=True)
        return strengths
    
    def _identify_weaknesses(self, experiences: List[Any]) -> List[Dict]:
        """Identify areas needing improvement"""
        weaknesses = []
        
        for category in self.categories:
            score = self._calculate_category_score(category, experiences)
            
            if score < 0.5:  # Below average threshold
                importance = "high" if score < 0.3 else "medium"
                weaknesses.append({
                    "category": category,
                    "score": score,
                    "importance": importance,
                    "description": self._generate_weakness_description(category, score)
                })
        
        # Sort by severity (lowest score first)
        weaknesses.sort(key=lambda x: x["score"])
        return weaknesses
    
    def _discover_patterns(self, experiences: List[Any]) -> List[Dict]:
        """Discover behavioral patterns from experiences"""
        patterns = []
        
        # Time-of-day patterns
        time_pattern = self._analyze_time_patterns(experiences)
        if time_pattern["confidence"] > 0.6:
            patterns.append(time_pattern)
        
        # Performance consistency
        consistency = self._analyze_consistency(experiences)
        if consistency["notable"]:
            patterns.append(consistency)
        
        # Success correlations
        correlations = self._find_success_correlations(experiences)
        patterns.extend(correlations)
        
        return patterns
    
    def _suggest_improvements(self, experiences: List[Any]) -> List[str]:
        """Generate improvement suggestions"""
        suggestions = []
        
        weaknesses = self._identify_weaknesses(experiences)
        
        for weakness in weaknesses[:3]:  # Top 3
            category = weakness["category"]
            
            if category == "response_time":
                suggestions.append("Optimize processing pipeline to reduce response time")
            elif category == "thought_quality":
                suggestions.append("Enhance thinking depth and multi-perspective analysis")
            elif category == "resonance_accuracy":
                suggestions.append("Refine resonance calculation algorithms")
            elif category == "user_satisfaction":
                suggestions.append("Improve empathy and user intent understanding")
            elif category == "learning_efficiency":
                suggestions.append("Increase pattern recognition and generalization")
            elif category == "error_handling":
                suggestions.append("Strengthen error recovery and graceful degradation")
        
        return suggestions
    
    def _summarize_performance(self, experiences: List[Any]) -> Dict:
        """Create performance summary"""
        if not experiences:
            return {}
        
        # Calculate statistics
        feedbacks = [getattr(exp, 'feedback', 0.5) for exp in experiences]
        
        return {
            "total_interactions": len(experiences),
            "average_feedback": np.mean(feedbacks),
            "feedback_std": np.std(feedbacks),
            "positive_rate": sum(1 for f in feedbacks if f > 0.5) / len(feedbacks),
            "excellence_rate": sum(1 for f in feedbacks if f > 0.8) / len(feedbacks)
        }
    
    def _analyze_category(self, category: str, experiences: List[Any]) -> Dict:
        """Analyze performance in specific category"""
        score = self._calculate_category_score(category, experiences)
        
        return {
            "category": category,
            "score": score,
            "grade": self._score_to_grade(score),
            "trend": self._calculate_category_trend(category),
            "recommendations": self._get_category_recommendations(category, score)
        }
    
    def _calculate_category_score(self, category: str, experiences: List[Any]) -> float:
        """Calculate score for a category"""
        if not experiences:
            return 0.5
        
        # Category-specific scoring logic
        if category == "thought_quality":
            scores = [getattr(exp, 'feedback', 0.5) for exp in experiences]
        elif category == "response_time":
            times = [getattr(exp, 'response_time', 1.0) for exp in experiences 
                    if hasattr(exp, 'response_time')]
            # Lower is better, normalize to 0-1
            if times:
                avg_time = np.mean(times)
                scores = [max(0, 1.0 - avg_time / 5.0)]  # 5s as reference
            else:
                return 0.5
        else:
            # Default: use feedback
            scores = [getattr(exp, 'feedback', 0.5) for exp in experiences]
        
        return np.mean(scores) if scores else 0.5
    
    def _analyze_trends(self, experiences: List[Any], period_days: int) -> Dict:
        """Analyze performance trends"""
        if len(experiences) < 2:
            return {"trend": "insufficient_data"}
        
        # Split into two halves
        mid = len(experiences) // 2
        first_half = experiences[:mid]
        second_half = experiences[mid:]
        
        first_avg = np.mean([getattr(exp, 'feedback', 0.5) for exp in first_half])
        second_avg = np.mean([getattr(exp, 'feedback', 0.5) for exp in second_half])
        
        change = second_avg - first_avg
        
        if change > 0.1:
            trend = "improving"
        elif change < -0.1:
            trend = "declining"
        else:
            trend = "stable"
        
        return {
            "trend": trend,
            "change": change,
            "first_period_avg": first_avg,
            "second_period_avg": second_avg
        }
    
    def _compare_with_previous_period(self, experiences: List[Any], 
                                     period_days: int) -> Dict:
        """Compare with previous period"""
        # This would require historical data
        # Simplified version
        return {
            "comparison": "baseline",
            "note": "Requires historical data for comparison"
        }
    
    def _generate_actions_for_weakness(self, weakness: Dict) -> List[Dict]:
        """Generate specific actions for a weakness"""
        category = weakness["category"]
        
        actions = []
        
        if category == "thought_quality":
            actions.append({
                "action": "Practice multi-perspective thinking",
                "frequency": "daily",
                "duration": "15 minutes"
            })
        elif category == "response_time":
            actions.append({
                "action": "Optimize processing algorithms",
                "frequency": "weekly",
                "duration": "2 hours"
            })
        
        return actions
    
    def _get_current_performance(self, area: str) -> float:
        """Get current performance for an area"""
        recent_experiences = self._get_recent_experiences(days=3)
        return self._calculate_category_score(area, recent_experiences)
    
    def _calculate_progress(self, initial: float, target: float, current: float) -> float:
        """Calculate progress toward target"""
        if target == initial:
            return 1.0
        
        progress = (current - initial) / (target - initial)
        return max(0.0, min(1.0, progress))
    
    def _get_recent_experiences(self, days: int) -> List[Any]:
        """Get experiences from recent days"""
        # This would integrate with experience buffer
        # Placeholder implementation
        return []
    
    def _get_recent_reflections(self, days: int) -> List[Dict]:
        """Get reflections from recent days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        return [
            r for r in self.reflections_history
            if datetime.fromisoformat(r.get("created_at", "2000-01-01")) > cutoff_date
        ]
    
    def _find_consistent_patterns(self, reflections: List[Dict], 
                                  key: str) -> List[Dict]:
        """Find patterns that appear consistently"""
        # Count occurrences of each pattern
        pattern_counts = defaultdict(int)
        
        for reflection in reflections:
            items = reflection.get(key, [])
            for item in items:
                category = item.get("category", "unknown")
                pattern_counts[category] += 1
        
        # Find consistent patterns (appear in >50% of reflections)
        threshold = len(reflections) * 0.5
        consistent = [
            {"pattern": category, "frequency": count / len(reflections)}
            for category, count in pattern_counts.items()
            if count > threshold
        ]
        
        return consistent
    
    def _calculate_trajectory(self, reflections: List[Dict]) -> Dict:
        """Calculate improvement trajectory"""
        if len(reflections) < 2:
            return {"trajectory": "insufficient_data"}
        
        # Extract overall scores from reflections
        scores = []
        for reflection in reflections:
            summary = reflection.get("performance_summary", {})
            avg_feedback = summary.get("average_feedback", 0.5)
            scores.append(avg_feedback)
        
        # Calculate trend
        if len(scores) >= 2:
            slope = (scores[-1] - scores[0]) / len(scores)
            
            if slope > 0.01:
                trajectory = "upward"
            elif slope < -0.01:
                trajectory = "downward"
            else:
                trajectory = "stable"
        else:
            trajectory = "stable"
        
        return {
            "trajectory": trajectory,
            "slope": slope if len(scores) >= 2 else 0,
            "recent_scores": scores[-5:]
        }
    
    def _calculate_learning_velocity(self, reflections: List[Dict]) -> float:
        """Calculate how fast the system is learning"""
        if len(reflections) < 2:
            return 0.0
        
        # Rate of improvement over time
        first_score = reflections[0].get("performance_summary", {}).get("average_feedback", 0.5)
        last_score = reflections[-1].get("performance_summary", {}).get("average_feedback", 0.5)
        
        days = len(reflections)
        velocity = (last_score - first_score) / days if days > 0 else 0.0
        
        return velocity
    
    def _generate_recommendations(self, reflections: List[Dict]) -> List[str]:
        """Generate long-term recommendations"""
        recommendations = []
        
        trajectory = self._calculate_trajectory(reflections)
        
        if trajectory["trajectory"] == "downward":
            recommendations.append("Performance declining - review recent changes")
        elif trajectory["trajectory"] == "stable":
            recommendations.append("Consider exploring new learning strategies")
        
        velocity = self._calculate_learning_velocity(reflections)
        if velocity < 0.001:
            recommendations.append("Learning velocity low - increase challenge level")
        
        return recommendations
    
    def _analyze_time_patterns(self, experiences: List[Any]) -> Dict:
        """Analyze time-of-day performance patterns"""
        return {
            "pattern": "time_of_day",
            "confidence": 0.5,
            "description": "Neutral time pattern"
        }
    
    def _analyze_consistency(self, experiences: List[Any]) -> Dict:
        """Analyze performance consistency"""
        if not experiences:
            return {"notable": False}
        
        feedbacks = [getattr(exp, 'feedback', 0.5) for exp in experiences]
        std = np.std(feedbacks)
        
        return {
            "pattern": "consistency",
            "std_deviation": std,
            "notable": std > 0.3,
            "description": f"Performance variability: {'high' if std > 0.3 else 'low'}"
        }
    
    def _find_success_correlations(self, experiences: List[Any]) -> List[Dict]:
        """Find what correlates with success"""
        return []
    
    def _generate_strength_description(self, category: str, score: float) -> str:
        """Generate description for strength"""
        return f"Strong performance in {category} (score: {score:.2f})"
    
    def _generate_weakness_description(self, category: str, score: float) -> str:
        """Generate description for weakness"""
        return f"Needs improvement in {category} (score: {score:.2f})"
    
    def _score_to_grade(self, score: float) -> str:
        """Convert score to letter grade"""
        if score >= 0.9:
            return "A+"
        elif score >= 0.8:
            return "A"
        elif score >= 0.7:
            return "B"
        elif score >= 0.6:
            return "C"
        else:
            return "D"
    
    def _calculate_category_trend(self, category: str) -> str:
        """Calculate trend for category"""
        return "stable"  # Simplified
    
    def _get_category_recommendations(self, category: str, score: float) -> List[str]:
        """Get recommendations for category"""
        if score < 0.5:
            return [f"Focus on improving {category}"]
        return []
    
    def _save_reflection(self, reflection: Dict):
        """Save reflection to disk"""
        date = reflection["date"]
        save_path = self.save_dir / f"reflection_{date}.json"
        # Convert numpy types to Python types for JSON serialization
        reflection_copy = self._make_json_serializable(reflection)
        with open(save_path, 'w') as f:
            json.dump(reflection_copy, f, indent=2)
    
    def _make_json_serializable(self, obj):
        """Convert numpy types to JSON-serializable types"""
        import numpy as np
        if isinstance(obj, dict):
            return {k: self._make_json_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._make_json_serializable(item) for item in obj]
        elif isinstance(obj, (np.integer, np.floating)):
            return float(obj)
        elif isinstance(obj, np.bool_):
            return bool(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return obj
    
    def _save_improvement_plan(self, plan: Dict):
        """Save improvement plan to disk"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = self.save_dir / f"improvement_plan_{timestamp}.json"
        with open(save_path, 'w') as f:
            json.dump(plan, f, indent=2)
    
    def _load_history(self):
        """Load historical reflections"""
        if not self.save_dir.exists():
            return
        
        for file_path in self.save_dir.glob("reflection_*.json"):
            try:
                with open(file_path, 'r') as f:
                    reflection = json.load(f)
                    self.reflections_history.append(reflection)
            except Exception as e:
                print(f"Warning: Could not load reflection {file_path}: {e}")
