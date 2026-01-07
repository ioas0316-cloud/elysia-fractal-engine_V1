'''
Collaborative Learning System

Enables bidirectional learning between AI and humans.
'''

import time
import json
from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from pathlib import Path


class TeachingStyle(Enum):
    SOCRATIC = "socratic"
    DEMONSTRATIVE = "demonstrative"
    GUIDED_DISCOVERY = "guided_discovery"
    SCAFFOLDING = "scaffolding"
    PEER_LEARNING = "peer_learning"
    EXPERIENTIAL = "experiential"


@dataclass
class LearningSession:
    topic: str
    direction: str  # "human_to_ai" or "ai_to_human"
    teaching_style: TeachingStyle
    content: Dict[str, Any]
    outcome_quality: float
    timestamp: float


class CollaborativeLearner:
    def __init__(self):
        self.learning_history: List[LearningSession] = []
        self.knowledge_base: Dict[str, Any] = {}
        self.data_dir = Path("data/social/learning")
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    async def learn_from_human(
        self,
        topic: str,
        content: Dict[str, Any],
        teaching_method: str = "demonstrative"
    ) -> Dict[str, Any]:
        # Validate and integrate knowledge
        quality_score = self._assess_knowledge_quality(content)
        
        if quality_score > 0.6:
            self.knowledge_base[topic] = {
                "content": content,
                "source": "human",
                "quality": quality_score,
                "learned_at": time.time()
            }
            
            session = LearningSession(
                topic=topic,
                direction="human_to_ai",
                teaching_style=TeachingStyle(teaching_method),
                content=content,
                outcome_quality=quality_score,
                timestamp=time.time()
            )
            self.learning_history.append(session)
            self._save_session(session)
            
            return {
                "status": "success",
                "topic": topic,
                "quality_score": quality_score,
                "integrated": True,
                "understanding_level": quality_score
            }
        else:
            return {
                "status": "needs_clarification",
                "topic": topic,
                "questions": self._generate_clarifying_questions(content)
            }
    
    async def teach_human(
        self,
        topic: str,
        learner_level: str = "intermediate",
        style: TeachingStyle = TeachingStyle.GUIDED_DISCOVERY
    ) -> Dict[str, Any]:
        if topic not in self.knowledge_base:
            return {
                "status": "unknown_topic",
                "message": f"I don't have knowledge about {topic} yet"
            }
        
        knowledge = self.knowledge_base[topic]
        
        # Adapt teaching based on style and learner level
        lesson = self._create_lesson(topic, knowledge, learner_level, style)
        
        session = LearningSession(
            topic=topic,
            direction="ai_to_human",
            teaching_style=style,
            content=lesson,
            outcome_quality=0.85,  # Estimated
            timestamp=time.time()
        )
        self.learning_history.append(session)
        self._save_session(session)
        
        return lesson
    
    def _assess_knowledge_quality(self, content: Dict[str, Any]) -> float:
        score = 0.5
        if "description" in content:
            score += 0.2
        if "examples" in content:
            score += 0.2
        if "best_practices" in content:
            score += 0.1
        return min(1.0, score)
    
    def _generate_clarifying_questions(self, content: Dict[str, Any]) -> List[str]:
        questions = []
        if "description" not in content:
            questions.append("Can you provide a description?")
        if "examples" not in content:
            questions.append("Could you give some examples?")
        return questions
    
    def _create_lesson(
        self,
        topic: str,
        knowledge: Dict[str, Any],
        learner_level: str,
        style: TeachingStyle
    ) -> Dict[str, Any]:
        content = knowledge["content"]
        
        if style == TeachingStyle.GUIDED_DISCOVERY:
            return {
                "type": "guided_discovery",
                "topic": topic,
                "introduction": f"Let's explore {topic} together",
                "guiding_questions": [
                    f"What do you think {topic} means?",
                    "Can you think of similar concepts?"
                ],
                "key_points": content.get("description", ""),
                "examples": content.get("examples", []),
                "practice_opportunities": ["Try applying this concept"]
            }
        elif style == TeachingStyle.DEMONSTRATIVE:
            return {
                "type": "demonstrative",
                "topic": topic,
                "explanation": content.get("description", ""),
                "demonstration": content.get("examples", []),
                "your_turn": "Now try it yourself"
            }
        else:
            return {
                "type": "standard",
                "topic": topic,
                "content": content
            }
    
    def _save_session(self, session: LearningSession):
        timestamp = int(time.time() * 1000)
        filename = self.data_dir / f"session_{timestamp}.json"
        
        data = {
            "topic": session.topic,
            "direction": session.direction,
            "style": session.teaching_style.value,
            "quality": session.outcome_quality,
            "timestamp": session.timestamp
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
