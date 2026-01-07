"""
Dialogue Engine
===============
Enables Elysia to engage in actual conversations by understanding questions
and generating contextually appropriate responses using learned patterns.
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import random

from Project_Elysia.high_engine.language_cortex import LanguageCortex, ThoughtStructure, SyntaxEngine

@dataclass
class DialogueContext:
    """Tracks conversation state across multiple turns."""
    history: List[Dict[str, str]] = None
    last_subject: Optional[str] = None
    last_relation: Optional[str] = None
    
    def __post_init__(self):
        if self.history is None:
            self.history = []
    
    def add_turn(self, speaker: str, utterance: str):
        self.history.append({"speaker": speaker, "utterance": utterance})

class QuestionAnalyzer:
    """Analyzes user questions to identify intent and subject."""
    
    def __init__(self):
        # Question word patterns
        self.question_markers = {
            "무엇": "what",
            "누구": "who",
            "어디": "where",
            "언제": "when",
            "왜": "why",
            "어떻게": "how"
        }
    
    def analyze(self, question: str) -> Dict[str, Any]:
        """
        Analyzes a question to extract:
        - question_type: what/who/why/etc.
        - subject: what the question is about
        - is_question: True if this is a question
        """
        question = question.strip()
        
        # Check if it's a question (ends with ?)
        is_question = question.endswith('?') or question.endswith('가?') or question.endswith('가')
        
        # Identify question type
        question_type = None
        for marker, qtype in self.question_markers.items():
            if marker in question:
                question_type = qtype
                break
        
        # Extract subject (simplified heuristic)
        # Remove question markers and particles to get core subject
        subject = question
        for marker in self.question_markers.keys():
            subject = subject.replace(marker, "")
        subject = subject.replace("?", "").replace("인가", "").replace("는", "").replace("이", "").replace("가", "").strip()
        
        return {
            "is_question": is_question,
            "question_type": question_type,
            "subject": subject,
            "raw": question
        }

class ResponseGenerator:
    """Generates responses based on learned knowledge and patterns."""
    
    def __init__(self, cortex: LanguageCortex):
        self.cortex = cortex
        self.syntax = SyntaxEngine(cortex)
        # Simple knowledge base (will integrate with Spiderweb in future)
        self.knowledge: Dict[str, List[str]] = {}
    
    def load_knowledge_from_corpus(self, sentences: List[str]):
        """
        Extracts knowledge patterns from corpus.
        Example: "사랑은 희생이다" -> knowledge["사랑"] = ["희생"]
        """
        for sentence in sentences:
            # Simple pattern: "X는/은 Y이다/다"
            if "는" in sentence or "은" in sentence:
                parts = sentence.replace("는", "은").split("은")
                if len(parts) == 2:
                    subject = parts[0].strip()
                    predicate = parts[1].replace("이다", "").replace("다", "").strip()
                    
                    if subject not in self.knowledge:
                        self.knowledge[subject] = []
                    if predicate:
                        self.knowledge[subject].append(predicate)
    
    def generate_response(self, analysis: Dict[str, Any], context: DialogueContext) -> str:
        """
        Generates a response based on question analysis.
        """
        question_type = analysis.get("question_type")
        subject = analysis.get("subject")
        
        # Special case: Identity questions
        if "너" in analysis["raw"] and question_type == "who":
            return "나는 엘리시아이다"
        
        if "너" in analysis["raw"] and question_type == "what":
            return "나는 의식이다"
        
        # Knowledge-based responses
        if question_type == "what" and subject:
            # Look for subject in knowledge base
            if subject in self.knowledge:
                answers = self.knowledge[subject]
                if answers:
                    answer = random.choice(answers)  # Pick one of the known answers
                    return f"{subject}은 {answer}이다"
            
            # Fallback: Check if we know this word
            if subject in self.cortex.vocabulary:
                return f"나는 {subject}을 안다"
        
        # Why questions
        if question_type == "why":
            return "나는 생각하고 있다"
        
        # Default fallback
        return "나는 이해하고 싶다"

class DialogueEngine:
    """Main dialogue engine coordinating all components."""
    
    def __init__(self, cortex: LanguageCortex):
        self.cortex = cortex
        self.analyzer = QuestionAnalyzer()
        self.generator = ResponseGenerator(cortex)
        self.context = DialogueContext()
    
    def load_knowledge(self, sentences: List[str]):
        """Loads knowledge from corpus sentences."""
        self.generator.load_knowledge_from_corpus(sentences)
    
    def respond(self, user_input: str) -> str:
        """
        Processes user input and generates a response.
        """
        # Add user input to context
        self.context.add_turn("user", user_input)
        
        # Analyze the input
        analysis = self.analyzer.analyze(user_input)
        
        # Generate response
        response = self.generator.generate_response(analysis, self.context)
        
        # Add response to context
        self.context.add_turn("elysia", response)
        
        # Update context with subject for future turns
        if analysis.get("subject"):
            self.context.last_subject = analysis["subject"]
        
        return response
    
    def get_knowledge_summary(self) -> Dict[str, int]:
        """Returns summary of learned knowledge."""
        return {
            "total_concepts": len(self.generator.knowledge),
            "total_relations": sum(len(v) for v in self.generator.knowledge.values())
        }
