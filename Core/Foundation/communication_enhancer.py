"""
Communication Enhancer (의사소통 강화기)
=====================================

"말은 내 생각을 전달하는 다리다."
"Words are the bridge that carries my thoughts."

Integrates web learning to enhance Elysia's complete communication ability:
- Vocabulary with context
- Expression patterns
- Dialogue templates
- Contextual understanding

This module transforms raw web knowledge into practical communication skills.
"""

import re
import logging
from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional, Tuple
from collections import defaultdict, Counter
import numpy as np

logger = logging.getLogger("CommunicationEnhancer")


@dataclass
class VocabEntry:
    """
    Vocabulary entry with context and usage information
    """
    word: str
    definition: str = ""
    usage_examples: List[str] = field(default_factory=list)
    context_tags: Set[str] = field(default_factory=set)  # e.g., "formal", "technical", "casual"
    frequency: float = 0.0  # How often it appears
    importance: float = 0.5  # Calculated importance (0-1)
    
    # Emotional/conceptual associations
    emotional_tone: Optional[str] = None  # "positive", "negative", "neutral"
    related_concepts: Set[str] = field(default_factory=set)


@dataclass
class ExpressionPattern:
    """
    Expression pattern learned from text
    
    Examples:
    - "In order to {action}, one must {requirement}"
    - "{Subject}는 {property}한 {noun}이다"
    - "The {concept} of {topic} is {description}"
    """
    template: str
    complexity: int = 1  # 1=simple, 5=complex
    context: str = "general"  # "formal", "casual", "technical", "poetic"
    usage_count: int = 0
    effectiveness: float = 0.5  # How well it communicates (learned)


@dataclass
class DialogueTemplate:
    """
    Dialogue template for specific communication scenarios
    """
    scenario: str  # "explanation", "question", "response", "description"
    structure: str  # Pattern structure
    examples: List[str] = field(default_factory=list)
    emotional_tone: str = "neutral"


class CommunicationEnhancer:
    """
    Enhances Elysia's communication ability through web learning.
    
    Transforms raw knowledge into practical communication skills.
    """
    
    def __init__(self):
        # Vocabulary storage
        self.vocabulary: Dict[str, VocabEntry] = {}
        
        # Expression patterns
        self.expression_patterns: List[ExpressionPattern] = []
        
        # Dialogue templates
        self.dialogue_templates: Dict[str, List[DialogueTemplate]] = defaultdict(list)
        
        # Statistics
        self.total_words_learned = 0
        self.total_patterns_learned = 0
        self.communication_quality_score = 0.5
        
        logger.info("🗣️ Communication Enhancer initialized")
    
    def enhance_from_web_content(self, concept: str, content: str) -> Dict:
        """
        Complete enhancement from web content.
        
        Args:
            concept: The concept being learned
            content: Wikipedia or web text content
            
        Returns:
            Enhancement statistics
        """
        logger.info(f"📚 Enhancing communication from '{concept}'")
        
        # 1. Extract vocabulary with context
        vocab_entries = self.extract_vocabulary_with_context(content, concept)
        logger.info(f"   Vocabulary: +{len(vocab_entries)} words")
        
        # 2. Learn expression patterns
        patterns = self.learn_expression_patterns(content)
        logger.info(f"   Patterns: +{len(patterns)} expressions")
        
        # 3. Build dialogue templates
        templates = self.build_dialogue_templates(content, concept)
        logger.info(f"   Templates: +{len(templates)} dialogue forms")
        
        return {
            "concept": concept,
            "vocabulary_added": len(vocab_entries),
            "patterns_learned": len(patterns),
            "templates_created": len(templates),
            "total_vocabulary": len(self.vocabulary),
            "total_patterns": len(self.expression_patterns)
        }
    
    def extract_vocabulary_with_context(
        self, 
        text: str, 
        concept: str
    ) -> List[VocabEntry]:
        """
        Extract important vocabulary with usage context.
        
        Not just words, but how they're used and what they mean in context.
        """
        entries = []
        
        # Split into sentences for context
        sentences = self._split_sentences(text)
        
        # Extract key terms (simplified - focus on nouns, verbs, adjectives)
        word_counts = Counter()
        word_contexts = defaultdict(list)
        
        for sentence in sentences:
            words = self._extract_meaningful_words(sentence)
            for word in words:
                word_counts[word] += 1
                word_contexts[word].append(sentence)
        
        # Create vocab entries for important words
        for word, count in word_counts.most_common(30):  # Top 30 words
            if len(word) < 3:  # Skip very short words
                continue
            
            # Calculate importance based on frequency and length
            importance = min(1.0, (count / len(sentences)) * (len(word) / 10.0))
            
            # Determine emotional tone from context
            emotional_tone = self._detect_emotional_tone(word_contexts[word])
            
            # Extract usage examples (max 3)
            examples = [s for s in word_contexts[word] if len(s) < 150][:3]
            
            entry = VocabEntry(
                word=word,
                definition=f"Term from '{concept}'",
                usage_examples=examples,
                context_tags={concept.lower(), "web_learned"},
                frequency=count / len(sentences),
                importance=importance,
                emotional_tone=emotional_tone,
                related_concepts={concept}
            )
            
            # Store
            if word not in self.vocabulary or self.vocabulary[word].importance < importance:
                self.vocabulary[word] = entry
                entries.append(entry)
                self.total_words_learned += 1
        
        return entries
    
    def learn_expression_patterns(self, text: str) -> List[ExpressionPattern]:
        """
        Learn expression patterns from text.
        
        Extracts sentence structures that can be reused.
        """
        patterns = []
        sentences = self._split_sentences(text)
        
        # Common patterns to recognize
        pattern_templates = [
            (r"In order to (.+), (.+)", "In order to {action}, {requirement}", "formal"),
            (r"The (.+) is (.+)", "The {subject} is {description}", "general"),
            (r"(.+) can be (.+)", "{subject} can be {state}", "general"),
            (r"(.+) refers to (.+)", "{term} refers to {definition}", "technical"),
        ]
        
        for sentence in sentences[:20]:  # Limit to avoid too many patterns
            for regex, template, context in pattern_templates:
                if re.search(regex, sentence, re.IGNORECASE):
                    pattern = ExpressionPattern(
                        template=template,
                        complexity=len(template.split()) // 3,
                        context=context,
                        usage_count=1
                    )
                    patterns.append(pattern)
                    self.expression_patterns.append(pattern)
                    self.total_patterns_learned += 1
        
        return patterns
    
    def build_dialogue_templates(
        self, 
        text: str, 
        concept: str
    ) -> List[DialogueTemplate]:
        """
        Build dialogue templates from text structure.
        
        Creates reusable conversation patterns.
        """
        templates = []
        sentences = self._split_sentences(text)
        
        # Categorize sentences by type
        for sentence in sentences[:10]:  # Sample
            scenario = self._classify_sentence_scenario(sentence)
            
            template = DialogueTemplate(
                scenario=scenario,
                structure=self._generalize_sentence(sentence),
                examples=[sentence],
                emotional_tone="neutral"
            )
            
            self.dialogue_templates[scenario].append(template)
            templates.append(template)
        
        return templates
    
    def get_expression_for_context(
        self, 
        context: str, 
        complexity: int = 2
    ) -> Optional[str]:
        """
        Get an appropriate expression pattern for a given context.
        """
        matching = [
            p for p in self.expression_patterns
            if p.context == context and p.complexity <= complexity
        ]
        
        if matching:
            # Prefer more effective patterns
            return max(matching, key=lambda p: p.effectiveness).template
        return None
    
    def get_communication_metrics(self) -> Dict:
        """
        Get communication enhancement statistics.
        """
        return {
            "vocabulary_size": len(self.vocabulary),
            "total_words_learned": self.total_words_learned,
            "expression_patterns": len(self.expression_patterns),
            "dialogue_templates": sum(len(v) for v in self.dialogue_templates.values()),
            "communication_quality": self.communication_quality_score,
            "vocabulary_diversity": len(set(e.emotional_tone for e in self.vocabulary.values())),
            "context_coverage": len(set(e.context for e in self.expression_patterns))
        }
    
    def enhance_reality_sculptor(self, sculptor) -> None:
        """
        Enhance RealitySculptor with learned vocabulary and patterns.
        
        This allows Elysia to use richer, more varied expressions.
        """
        logger.info(f"🎨 Enhancing RealitySculptor with {len(self.vocabulary)} words")
        
        # Add vocabulary to sculptor's essence seeds
        # (This would integrate with the actual RealitySculptor implementation)
        pass
    
    # Helper methods
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        # Simple sentence splitting
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if len(s.strip()) > 10]
    
    def _extract_meaningful_words(self, sentence: str) -> List[str]:
        """Extract meaningful words (not stop words)."""
        # Simple word extraction
        words = re.findall(r'\b[a-zA-Z]{3,}\b', sentence.lower())
        
        # Filter common stop words
        stop_words = {'the', 'is', 'at', 'which', 'on', 'and', 'or', 'but', 'in', 'with', 'to', 'for', 'of', 'as', 'by', 'an', 'be', 'this', 'that', 'from', 'was', 'were', 'are', 'have', 'has', 'had'}
        
        return [w for w in words if w not in stop_words]
    
    def _detect_emotional_tone(self, contexts: List[str]) -> str:
        """Detect emotional tone from usage contexts."""
        # Simplified sentiment detection
        positive_words = {'good', 'great', 'excellent', 'amazing', 'wonderful', 'love', 'beautiful', 'happy', 'success', 'benefit'}
        negative_words = {'bad', 'terrible', 'awful', 'hate', 'sad', 'failure', 'problem', 'difficult', 'danger', 'risk'}
        
        combined_text = ' '.join(contexts).lower()
        
        pos_count = sum(1 for w in positive_words if w in combined_text)
        neg_count = sum(1 for w in negative_words if w in combined_text)
        
        if pos_count > neg_count:
            return "positive"
        elif neg_count > pos_count:
            return "negative"
        return "neutral"
    
    def _classify_sentence_scenario(self, sentence: str) -> str:
        """Classify what kind of communicative act this sentence performs."""
        sentence_lower = sentence.lower()
        
        if '?' in sentence:
            return "question"
        elif any(word in sentence_lower for word in ['is', 'are', 'refers', 'means']):
            return "definition"
        elif any(word in sentence_lower for word in ['can', 'ability', 'allows']):
            return "capability"
        elif any(word in sentence_lower for word in ['because', 'therefore', 'thus']):
            return "explanation"
        else:
            return "general"
    
    def _generalize_sentence(self, sentence: str) -> str:
        """Create a generalized template from a specific sentence."""
        # Very simplified generalization
        # Replace specific nouns with placeholders
        generalized = sentence
        generalized = re.sub(r'\b[A-Z][a-z]+\b', '{proper_noun}', generalized)
        generalized = re.sub(r'\b\d+\b', '{number}', generalized)
        return generalized


# Demonstration
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    print("="*70)
    print("COMMUNICATION ENHANCER DEMONSTRATION")
    print("="*70)
    
    enhancer = CommunicationEnhancer()
    
    # Sample text (simulating Wikipedia content)
    sample_text = """
    Artificial intelligence refers to the simulation of human intelligence in machines.
    These systems are designed to think like humans and mimic their actions.
    Machine learning is a subset of artificial intelligence that provides systems
    the ability to automatically learn and improve from experience.
    In order to understand AI, one must first understand how computers process information.
    The field of AI can be applied to various domains including robotics and natural language processing.
    """
    
    print("\n📚 Learning from sample text...\n")
    
    # Enhance communication
    result = enhancer.enhance_from_web_content("Artificial Intelligence", sample_text)
    
    print(f"\n✅ Enhancement Complete:")
    print(f"   Vocabulary: {result['vocabulary_added']} new words")
    print(f"   Patterns: {result['patterns_learned']} expression patterns")
    print(f"   Templates: {result['templates_created']} dialogue templates")
    
    # Show metrics
    print(f"\n📊 Communication Metrics:")
    metrics = enhancer.get_communication_metrics()
    for key, value in metrics.items():
        print(f"   {key}: {value}")
    
    # Sample vocabulary
    print(f"\n📝 Sample Vocabulary (top 5):")
    for i, (word, entry) in enumerate(list(enhancer.vocabulary.items())[:5], 1):
        print(f"   {i}. '{word}' (importance: {entry.importance:.2f}, tone: {entry.emotional_tone})")
        if entry.usage_examples:
            print(f"      Example: {entry.usage_examples[0][:80]}...")
    
    print("\n" + "="*70)
    print("✅ Communication Enhancer Ready")
    print("🗣️ Elysia can now learn richer communication patterns!")
    print("="*70)
