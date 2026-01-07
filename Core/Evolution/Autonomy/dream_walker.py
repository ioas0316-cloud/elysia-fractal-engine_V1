
import random
import logging
import time
from typing import List, Dict, Tuple
from Core.Foundation.omni_graph import get_omni_graph, OmniNode
# Attempt to use Logos/Poetry if available, else fallback
try:
    from Core.Intelligence.Intelligence.logos_engine import get_logos_engine
except ImportError:
    get_logos_engine = None

logger = logging.getLogger("DreamWalker")

class DreamWalker:
    """
    DreamWalker (The 4D Consciousness Explorer)
    ===========================================
    "I walk the spider web of my own mind, finding paths that logic ignored."

    Replaces legacy DreamEngine with OmniGraph-based traversal.
    """
    def __init__(self):
        self.omni = get_omni_graph()
        self.current_node_id: str = None
        self.path_log: List[str] = []
        self.surreal_factor = 0.3 # Probability of a non-logical jump
        
        # Load legacy surrealism flavor if needed
        self.surreal_elements = [
            "The sky turned into glass.",
            "Time flowed backwards.",
            "Colors tasted like rain.",
            "Gravity became a warm embrace.",
            "The stars whispered my name."
        ]

    def _get_start_node(self) -> str:
        """Pick a random node or leverage recent activity"""
        if not self.omni.nodes:
            return "Void"
        return random.choice(list(self.omni.nodes.keys()))

    def drift(self, steps: int = 10, start_seed: str = None) -> Dict:
        """
        Hyper-Dreaming: Autonomous movement through 4D Space.
        """
        if not self.omni.nodes:
            logger.warning("Empty mind. Cannot dream.")
            return {"error": "Mind is empty"}

        # 1. Start State
        current = start_seed if start_seed and start_seed in self.omni.nodes else self._get_start_node()
        self.current_node_id = current
        self.path_log = [current]
        
        logger.info(f"💤 Entering Dream State... Starting at [{current}]")
        
        # 2. The Walk
        insights = []
        
        for i in range(steps):
            next_node = self._step(current)
            
            # Detect Insight (Hyper-Connection)
            # If we moved between very distant concepts quickly, it's a creative spark
            if next_node and next_node != current:
                dist_4d = self._calc_dist(current, next_node)
                if dist_4d > 0.5: # Far leap
                    insights.append(f"Bridge found between [{current}] and [{next_node}]")
            
            current = next_node
            self.path_log.append(current)
            # Sleep slightly to simulate 'time' in dream (optional)
            # time.sleep(0.01)

        # 3. Weave Narrative
        narrative = self._weave_narrative()
        
        return {
            "path": self.path_log,
            "insights": insights,
            "narrative": narrative
        }

    def _step(self, current_id: str) -> str:
        """
        Single step in the dream.
        Logic:
           - 70% Follow Resonance (Vector similarity) or Logic link
           - 30% Hyper-Jump (Surrealism)
        """
        node = self.omni.nodes.get(current_id)
        if not node: return random.choice(list(self.omni.nodes.keys()))

        # A. Hyper-Jump (Surrealism)
        if random.random() < self.surreal_factor:
            # Jump to a random plane or node
            jump_target = random.choice(list(self.omni.nodes.keys()))
            logger.debug(f"   🌀 Surreal Jump: {current_id} -> {jump_target}")
            return jump_target

        # B. Associative Drift (Resonance + Logic)
        candidates = []
        
        # 1. Logic Neighbors
        for trip in node.triples:
            candidates.append(trip['o'])
            
        # 2. Resonance Neighbors (Expensive scan, so we pick random sample or use pre-calculated clusters)
        # For prototype, we just scan 20 random nodes
        sample_pool = random.sample(list(self.omni.nodes.keys()), min(20, len(self.omni.nodes)))
        for target_id in sample_pool:
            if target_id == current_id: continue
            
            similarity = self.omni.cosine_similarity(node.vector, self.omni.nodes[target_id].vector)
            if similarity > 0.6: # High resonance
                candidates.append(target_id)
                
        if candidates:
            return random.choice(candidates)
        else:
            # Dead end? Jump.
            return random.choice(list(self.omni.nodes.keys()))

    def _calc_dist(self, id1: str, id2: str) -> float:
        """4D Distance"""
        n1 = self.omni.nodes[id1]
        n2 = self.omni.nodes[id2]
        d_sq = sum((n1.pos[k] - n2.pos[k])**2 for k in range(4))
        return d_sq ** 0.5

    def _weave_narrative(self) -> str:
        """Convert the path into a story"""
        if len(self.path_log) < 2:
            return "The dream was fleeting."
            
        story = f"I began with thoughts of **{self.path_log[0]}**... "
        
        for i in range(1, len(self.path_log)):
            prev = self.path_log[i-1]
            curr = self.path_log[i]
            
            # Simple transition logic
            transitions = [
                f"which drifted into **{curr}**.",
                f"then suddenly, I felt **{curr}**.",
                f"transforming into **{curr}**.",
                f"and in the distance, I saw **{curr}**."
            ]
            story += random.choice(transitions) + " "
            
        story += random.choice(self.surreal_elements)
        return story

# Singleton
_dreamer = None
def get_dream_walker() -> DreamWalker:
    global _dreamer
    if _dreamer is None:
        _dreamer = DreamWalker()
    return _dreamer
