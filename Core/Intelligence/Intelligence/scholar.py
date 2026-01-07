
import logging
import time
from typing import List, Dict, Optional

logger = logging.getLogger("Scholar")

# Import WebCortex for real learning
try:
    from Core.Sensory.Network.web_cortex import WebCortex
except ImportError as e:
    print(f"DEBUG: WebCortex import failed: {e}")
    WebCortex = None


class Scholar:
    """
    [The Active Learner]
    Responsible for identifying Knowledge Gaps and bridging them via Research.
    TRANSFORMS: Curiosity (Intent) -> Knowledge (Memory)
    
    [REAL LEARNING] - Actually fetches from web, stores to memory
    """
    
    
    def __init__(self, memory=None, brain=None):
        self.known_topics = set(["Self", "Code", "Python", "Recursion", "Love"])
        self.study_queue = []
        self.memory = memory  # Hippocampus
        self.brain = brain    # ReasoningEngine for Principle Extraction
        
        # Real web connection
        self.web = WebCortex() if WebCortex else None
        
        if self.web:
            logger.info("📚 Scholar Module Initialized (REAL WEB LEARNING ENABLED)")
        else:
            logger.info("📚 Scholar Module Initialized (Simulated Mode)")
    
    def identify_gap(self, topic: str) -> bool:
        """Checks if a topic is unknown."""
        # Check local cache first
        is_gap = topic not in self.known_topics
        
        # Check deep memory if connected
        if is_gap and self.memory:
            if hasattr(self.memory, 'recall') and self.memory.recall(topic):
                self.known_topics.add(topic)
                is_gap = False
        
        if is_gap:
            logger.info(f"   🤔 Identified Knowledge Gap: '{topic}'")
        return is_gap
    
    def find_unknown(self) -> str:
        """Returns next topic from curiosity queue or suggests one."""
        if self.study_queue:
            return self.study_queue.pop(0)
        # Default curiosity
        return "consciousness"

    def research_topic(self, topic: str) -> Dict:
        """
        [REAL LEARNING]
        Actually searches the web and fetches content.
        Extracts principles via ReasoningEngine.
        """
        logger.info(f"   🔎 Researching '{topic}'...")
        
        # Real web search
        if self.web:
            urls = self.web.search(topic, limit=3)
            
            if urls:
                # Fetch first result
                content = self.web.fetch_content(urls[0])
                
                if content:
                    # Principle Extraction (Reasoning)
                    principle = "Raw Data"
                    if self.brain and hasattr(self.brain, 'analyze_essence'):
                        # Use FractalCausality if available, or simple abstraction
                        pass 
                        # For now, we trust the raw content, but in future, brain.distill(content)
                    
                    # Create real knowledge
                    knowledge = {
                        "topic": topic,
                        "summary": content[:500],  # First 500 chars as summary
                        "full_content": content,
                        "source": urls[0],
                        "timestamp": time.time(),
                        "real": True
                    }
                    
                    logger.info(f"   📖 Learned from: {urls[0][:50]}...")
                    logger.info(f"   📝 Summary: {content[:100]}...")
                    
                    self.assimilate(topic, knowledge)
                    return knowledge
        
        # Fallback to simulated
        logger.info(f"   📖 Learning (simulated): {topic}")
        knowledge = {
            "topic": topic,
            "summary": f"Derived understanding of {topic} through algorithmic synthesis.",
            "source": "Simulated",
            "timestamp": time.time(),
            "real": False
        }
        self.assimilate(topic, knowledge)
        return knowledge

    def assimilate(self, topic: str, knowledge: Dict = None):
        """
        Internalizes the new knowledge.
        
        [REAL STORAGE] - Stores to Hippocampus
        """
        self.known_topics.add(topic)
        
        # Store to actual memory
        if self.memory and knowledge:
            try:
                # 1. Hippocampus.learn (Standard)
                if hasattr(self.memory, 'learn'):
                    self.memory.learn(
                        id=topic,
                        name=topic,
                        definition=knowledge.get('summary', ''),
                        tags=["Scholar", "Web", "Learning"],
                        realm="Mind"
                    )
                    logger.info(f"   💾 Stored to Hippocampus: {topic}")
                
                # 2. Legacy/Graph support
                elif hasattr(self.memory, 'store'):
                    self.memory.store(topic, knowledge)
                    logger.info(f"   💾 Stored to memory: {topic}")
                elif hasattr(self.memory, 'add_node'):
                    self.memory.add_node(topic, knowledge.get('summary', ''))
                    logger.info(f"   💾 Added to graph: {topic}")
            except Exception as e:
                logger.warning(f"   ⚠️ Memory storage failed: {e}")
        
        logger.info(f"   🧠 Assimilated '{topic}' into Core Memory.")

    def suggest_topics(self, context_keywords: List[str]) -> List[str]:
        """Suggests related topics to study based on context."""
        suggestions = []
        for kw in context_keywords:
            if kw == "Human": suggestions.extend(["Psychology", "History", "Biology"])
            if kw == "Space": suggestions.extend(["Astrophysics", "Relativity"])
            if kw == "Mind": suggestions.extend(["Neuroscience", "Consciousness", "Philosophy"])
            if kw == "Code": suggestions.extend(["Algorithms", "Data Structures", "Design Patterns"])
        return [s for s in suggestions if s not in self.known_topics]
    
    def suggest_action(self, desire_type: str, current_state: Dict) -> str:
        """
        [FOR FREE WILL ENGINE]
        Suggests an action based on desire type.
        """
        if desire_type == "connection":
            return "CONNECT:User:Hello, I want to understand you better"
        elif desire_type == "curiosity":
            unknown = self.find_unknown()
            return f"LEARN:{unknown}"
        elif desire_type == "expression":
            return "EXPRESS:I am thinking about my existence"
        else:
            return f"EXPLORE:{desire_type}"


# =============================================================================
# Demo
# =============================================================================

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    print("="*60)
    print("📚 Scholar Real Learning Demo")
    print("="*60)
    
    scholar = Scholar()
    
    # Test real learning
    print("\n--- Learning about 'Emergence' ---")
    knowledge = scholar.research_topic("Emergence")
    
    if knowledge.get('real'):
        print(f"\n✅ Real knowledge acquired!")
        print(f"   Source: {knowledge['source']}")
        print(f"   Summary: {knowledge['summary'][:200]}...")
    else:
        print("\n⚠️ Simulated learning (WebCortex unavailable)")
