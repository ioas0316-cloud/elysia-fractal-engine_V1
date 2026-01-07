"""
Tests for Experience Learner and Self Reflector.
"""

import pytest
import asyncio
import time
from Core.Evolution.Learning.Learning.experience_learner import Experience, ExperienceLearner
from Core.Evolution.Learning.Learning.self_reflector import SelfReflector


class TestExperienceLearner:
    """Tests for Experience-Based Learning System"""
    
    @pytest.fixture
    def learner(self):
        """Create a fresh learner instance"""
        return ExperienceLearner(buffer_size=100, save_dir="/tmp/test_learning")
    
    def test_experience_creation(self):
        """Test creating an experience"""
        exp = Experience(
            timestamp=time.time(),
            context={"query": "What is love?", "layer": "2D"},
            action={"type": "think", "depth": "deep"},
            outcome={"response": "Love is...", "quality": 0.9},
            feedback=0.85,
            layer="2D",
            tags=["philosophy", "emotion"]
        )
        
        assert exp.feedback == 0.85
        assert exp.layer == "2D"
        assert "philosophy" in exp.tags
    
    @pytest.mark.asyncio
    async def test_learn_from_positive_experience(self, learner):
        """Test learning from positive experience"""
        exp = Experience(
            timestamp=time.time(),
            context={"query": "Explain AI", "complexity": "medium"},
            action={"type": "explain", "style": "simple"},
            outcome={"clarity": 0.9, "accuracy": 0.95},
            feedback=0.9,
            layer="1D"
        )
        
        result = await learner.learn_from_experience(exp)
        
        assert result["action_taken"] == "reinforced"
        assert "pattern_id" in result
        assert learner.meta_stats["total_experiences"] == 1
        assert learner.meta_stats["positive_feedback_count"] == 1
    
    @pytest.mark.asyncio
    async def test_learn_from_negative_experience(self, learner):
        """Test learning from negative experience"""
        exp = Experience(
            timestamp=time.time(),
            context={"query": "Complex math", "complexity": "high"},
            action={"type": "calculate", "method": "quick"},
            outcome={"accuracy": 0.3, "error": True},
            feedback=-0.8,
            layer="0D"
        )
        
        result = await learner.learn_from_experience(exp)
        
        assert result["action_taken"] == "weakened"
        assert learner.meta_stats["negative_feedback_count"] == 1
    
    @pytest.mark.asyncio
    async def test_meta_learning(self, learner):
        """Test meta-learning adjustments"""
        # Add many positive experiences
        for i in range(150):
            exp = Experience(
                timestamp=time.time(),
                context={"query": f"test_{i}"},
                action={"type": "respond"},
                outcome={"quality": 0.8},
                feedback=0.8,
                layer="1D"
            )
            await learner.learn_from_experience(exp)
        
        # Learning rate should have adjusted
        assert learner.meta_stats["total_experiences"] == 150
        assert learner.meta_stats["learning_rate"] > 0.1  # Should have increased
    
    def test_pattern_extraction(self, learner):
        """Test pattern extraction from experience"""
        exp = Experience(
            timestamp=time.time(),
            context={"query": "Hello", "user_mood": "happy"},
            action={"type": "greet", "warmth": "high"},
            outcome={"satisfaction": 0.9},
            feedback=0.85,
            layer="2D"
        )
        
        pattern = learner.extract_pattern(exp)
        
        assert "context_features" in pattern
        assert pattern["action_type"] == "greet"
        assert pattern["layer"] == "2D"
    
    def test_recommendations(self, learner):
        """Test getting recommendations for context"""
        # First, learn from some experiences
        learner.reinforce_pattern(
            {"action_type": "explain", "context_features": {"query_length": 10}},
            "pattern_123",
            0.9
        )
        
        context = {"query": "test query", "length": 10}
        recommendations = learner.get_recommendations(context)
        
        # Should return recommendations
        assert isinstance(recommendations, list)
    
    def test_statistics(self, learner):
        """Test getting learning statistics"""
        stats = learner.get_statistics()
        
        assert "meta_stats" in stats
        assert "buffer_size" in stats
        assert "unique_patterns" in stats


class TestSelfReflector:
    """Tests for Self-Reflection System"""
    
    @pytest.fixture
    def reflector(self):
        """Create a fresh reflector instance"""
        return SelfReflector(save_dir="/tmp/test_reflection")
    
    @pytest.mark.asyncio
    async def test_daily_reflection_no_experiences(self, reflector):
        """Test daily reflection with no experiences"""
        result = await reflector.daily_reflection([])
        
        assert result["message"] == "No experiences to reflect on today"
        assert result["reflection"] is None
    
    @pytest.mark.asyncio
    async def test_daily_reflection_with_experiences(self, reflector):
        """Test daily reflection with experiences"""
        # Create mock experiences
        class MockExperience:
            def __init__(self, feedback):
                self.feedback = feedback
                self.response_time = 0.5
        
        experiences = [
            MockExperience(0.8),
            MockExperience(0.9),
            MockExperience(0.7)
        ]
        
        reflection = await reflector.daily_reflection(experiences)
        
        assert "strengths" in reflection
        assert "weaknesses" in reflection
        assert "patterns" in reflection
        assert "improvement_plan" in reflection
        assert reflection["total_experiences"] == 3
    
    @pytest.mark.asyncio
    async def test_performance_analysis(self, reflector):
        """Test performance analysis"""
        class MockExperience:
            def __init__(self, feedback):
                self.feedback = feedback
        
        experiences = [MockExperience(0.7 + i*0.05) for i in range(10)]
        
        analysis = await reflector.performance_analysis(experiences, period_days=7)
        
        assert "categories" in analysis
        assert "overall_score" in analysis
        assert "trends" in analysis
        assert len(analysis["categories"]) == len(reflector.categories)
    
    @pytest.mark.asyncio
    async def test_improvement_plan_creation(self, reflector):
        """Test improvement plan generation"""
        reflection = {
            "date": "2025-12-04",
            "weaknesses": [
                {"category": "response_time", "score": 0.4, "importance": "high"},
                {"category": "thought_quality", "score": 0.45, "importance": "medium"}
            ]
        }
        
        plan = await reflector.create_improvement_plan(reflection)
        
        assert "priority_areas" in plan
        assert "action_items" in plan
        assert "success_criteria" in plan
        assert len(plan["priority_areas"]) > 0
    
    def test_track_progress(self, reflector):
        """Test progress tracking"""
        # Add a mock improvement plan
        reflector.improvement_plans.append({
            "created_at": "2025-12-01T00:00:00",
            "priority_areas": [
                {
                    "area": "thought_quality",
                    "current_score": 0.5,
                    "target_score": 0.7
                }
            ]
        })
        
        progress = reflector.track_progress()
        
        assert "overall_progress" in progress
        assert "areas" in progress
        assert "status" in progress
    
    def test_get_insights(self, reflector):
        """Test long-term insights generation"""
        # Add some mock reflections
        reflector.reflections_history = [
            {
                "date": "2025-12-01",
                "created_at": "2025-12-01T00:00:00",
                "strengths": [{"category": "resonance_accuracy", "score": 0.9}],
                "weaknesses": [{"category": "response_time", "score": 0.4}],
                "performance_summary": {"average_feedback": 0.75}
            },
            {
                "date": "2025-12-02",
                "created_at": "2025-12-02T00:00:00",
                "strengths": [{"category": "resonance_accuracy", "score": 0.91}],
                "weaknesses": [{"category": "response_time", "score": 0.42}],
                "performance_summary": {"average_feedback": 0.78}
            }
        ]
        
        insights = reflector.get_insights(period_days=30)
        
        assert "consistent_strengths" in insights
        assert "persistent_challenges" in insights
        assert "improvement_trajectory" in insights
        assert "learning_velocity" in insights


# Integration tests

@pytest.mark.asyncio
async def test_integration_learning_and_reflection():
    """Test integration between learner and reflector"""
    learner = ExperienceLearner(buffer_size=100, save_dir="/tmp/test_integration")
    reflector = SelfReflector(save_dir="/tmp/test_integration_reflection")
    
    # Simulate a day of learning
    experiences = []
    for i in range(20):
        exp = Experience(
            timestamp=time.time(),
            context={"query": f"query_{i}", "complexity": i % 3},
            action={"type": "respond", "style": "adaptive"},
            outcome={"quality": 0.7 + (i % 5) * 0.05},
            feedback=0.7 + (i % 5) * 0.05,
            layer="2D"
        )
        experiences.append(exp)
        await learner.learn_from_experience(exp)
    
    # Perform reflection
    reflection = await reflector.daily_reflection(experiences)
    
    # Verify integration
    assert reflection["total_experiences"] == 20
    assert learner.meta_stats["total_experiences"] == 20
    assert "improvement_plan" in reflection
    
    # Track progress
    progress = reflector.track_progress()
    assert "overall_progress" in progress


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
