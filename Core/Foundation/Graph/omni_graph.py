
import json
import math
import random
import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger("OmniGraph")

@dataclass
class OmniNode:
    """
    Unified Knowledge Node (The Spider Web Point) - 4D HyperQubit Ready
    Merges: Logic, Vector, Space (4D)
    """
    id: str
    vector: Optional[List[float]] = None
    triples: List[Dict] = field(default_factory=list)
    # X, Y, Z, W (W = Dimension/Plane/Time/Consciousness)
    pos: List[float] = field(default_factory=lambda: [random.random(), random.random(), random.random(), random.random()])
    mass: float = 1.0
    
    # Metabolic Stats
    usage: float = 1.0       # Energy/Activity level (Decays over time)
    tension: float = 0.0     # Internal stress (Triggers mitosis)

    def to_dict(self):
        return {
            "id": self.id,
            "vector": self.vector[:5] if self.vector else None,
            "triples_count": len(self.triples),
            "pos": [round(p, 3) for p in self.pos],
            "dimension": "4D",
            "usage": self.usage
        }

@dataclass
class HyperPlane:
    id: str
    normal_vector: List[float] # (x, y, z, w) - Defines the plane orientation
    bias: float # Distance from origin

class OmniGraph:
    """
    The Fusion Engine: Hyper-Dimensional Space (4D)
    """
    def __init__(self):
        self.nodes: Dict[str, OmniNode] = {}
        self.planes: Dict[str, HyperPlane] = {}
        
    def add_logic(self, subject: str, predicate: str, object_: str):
        if subject not in self.nodes:
            self.nodes[subject] = OmniNode(id=subject)
        if object_ not in self.nodes:
            self.nodes[object_] = OmniNode(id=object_)
            
        self.nodes[subject].triples.append({"p": predicate, "o": object_})
        self.nodes[subject].usage += 0.1 # Interaction increases energy
        self.nodes[object_].usage += 0.1
        
    def add_vector(self, subject: str, vector: List[float]):
        if subject not in self.nodes:
            self.nodes[subject] = OmniNode(id=subject)
        self.nodes[subject].vector = vector
        
        # Tension is the first component of vector (usually complexity)
        if vector:
             self.nodes[subject].tension = vector[0]

    def cosine_similarity(self, v1: List[float], v2: List[float]) -> float:
        if not v1 or not v2: return 0.0
        dot = sum(a*b for a, b in zip(v1, v2))
        norm_a = math.sqrt(sum(a*a for a in v1))
        norm_b = math.sqrt(sum(b*b for b in v2))
        return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0

    def apply_gravity(self, iterations: int = 50, learning_rate: float = 0.1):
        """
        4D Physics Simulation
        Calculates forces across X, Y, Z, and W dimensions.
        """
        logger.info(f"🕸️ Hyper-Folding Space... ({len(self.nodes)} nodes, 4D)")
        
        nodes_list = list(self.nodes.values())
        
        for _ in range(iterations):
            forces = {n.id: [0.0, 0.0, 0.0, 0.0] for n in nodes_list}
            
            for i, n1 in enumerate(nodes_list):
                for n2 in nodes_list[i+1:]:
                    resonance = self.cosine_similarity(n1.vector, n2.vector)
                    linked = any(t['o'] == n2.id for t in n1.triples) or \
                             any(t['o'] == n1.id for t in n2.triples)
                    
                    strength = 0.0
                    if resonance > 0.7: strength += resonance * 0.5
                    if linked: strength += 1.0
                    
                    if strength > 0:
                        # 4D Vector Math
                        d = [n2.pos[k] - n1.pos[k] for k in range(4)]
                        dist = math.sqrt(sum(x*x for x in d)) + 0.001
                        
                        f_mag = strength * (dist - 0.1)
                        f_vec = [(x/dist) * f_mag for x in d]
                        
                        for k in range(4):
                            forces[n1.id][k] += f_vec[k]
                            forces[n2.id][k] -= f_vec[k]

            for n in nodes_list:
                for k in range(4):
                    n.pos[k] += forces[n.id][k] * learning_rate

    def apply_metabolism(self):
        """
        Structural Metabolism (Synaptic Evoltion).
        1. Fusion: Merge highly resonant nodes.
        2. Pruning: Remove low energy nodes.
        3. Mitosis: Split high tension nodes.
        """
        logger.info("🧬 Applying Synaptic Metabolism...")
        nodes_to_remove = []
        nodes_to_add = []
        
        # Copy list to iterate safely
        all_nodes = list(self.nodes.values())
        
        # 1. Decay & Pruning
        for node in all_nodes:
            node.usage *= 0.95 # Decay
            if node.usage < 0.1:
                logger.info(f"   💀 Pruning dead neuron: {node.id}")
                nodes_to_remove.append(node.id)
                
        # 2. Fusion & Mitosis
        # Note: Proper implementation requires care not to invalidate references.
        # For prototype, we do a simple pass.
        
        processed = set()
        
        for i, n1 in enumerate(all_nodes):
            if n1.id in nodes_to_remove or n1.id in processed: continue
            
            # A. Mitosis Check
            if n1.tension > 0.9:
                logger.info(f"   ✨ Mitosis Triggered: {n1.id} (Tension {n1.tension:.2f})")
                child_a = OmniNode(id=f"{n1.id}_Alpha", vector=n1.vector, pos=n1.pos)
                child_b = OmniNode(id=f"{n1.id}_Beta", vector=n1.vector, pos=n1.pos)
                nodes_to_add.append(child_a)
                nodes_to_add.append(child_b)
                # Original remains as parent, or could be replaced.
                # Here we keep parent as abstract container (Strategy choice)
                n1.tension = 0.0 # Relieve tension
                continue

            # B. Fusion Check
            for n2 in all_nodes[i+1:]:
                if n2.id in nodes_to_remove or n2.id in processed: continue
                
                sim = self.cosine_similarity(n1.vector, n2.vector)
                
                # Check 4D Proximity (Must be physically close too)
                d_sq = sum((n1.pos[k] - n2.pos[k])**2 for k in range(4))
                dist = math.sqrt(d_sq)
                
                if sim > 0.98 and dist < 0.1:
                    # FUSION
                    new_id = f"Concept:{n1.id}+{n2.id}"
                    logger.info(f"   ⚛️ Fusion Event: {n1.id} + {n2.id} -> {new_id}")
                    
                    # Merge Vector (Average)
                    new_vec = [(a+b)/2 for a, b in zip(n1.vector, n2.vector)] if n1.vector else None
                    new_node = OmniNode(id=new_id, vector=new_vec, pos=n1.pos)
                    
                    # Merge Logic
                    new_node.triples.extend(n1.triples)
                    new_node.triples.extend(n2.triples)
                    
                    nodes_to_add.append(new_node)
                    nodes_to_remove.append(n1.id)
                    nodes_to_remove.append(n2.id)
                    processed.add(n1.id)
                    processed.add(n2.id)
                    break 

        # Apply Changes
        for nid in nodes_to_remove:
            if nid in self.nodes: del self.nodes[nid]
            
        for new_node in nodes_to_add:
            self.nodes[new_node.id] = new_node

        logger.info(f"   🧬 Metabolism Complete. +{len(nodes_to_add)} / -{len(nodes_to_remove)}")

    def visualize_cluster(self, center_id: str, radius: float = 0.5):
        if center_id not in self.nodes: return "Node not found."
        
        center = self.nodes[center_id]
        cluster = []
        
        for n in self.nodes.values():
            # 4D Distance
            d_sq = sum((n.pos[k] - center.pos[k])**2 for k in range(4))
            dist = math.sqrt(d_sq)
            
            if dist < radius:
                # W-coordinate explicitly shown (Dimensions)
                w_coord = f"W={n.pos[3]:.2f}"
                cluster.append((dist, f"{n.id}[{w_coord}]"))
                
        cluster.sort()
        return f"HyperCluster around [{center_id}]: " + ", ".join([item[1] for item in cluster])


# Singleton
_omni = None
def get_omni_graph() -> OmniGraph:
    global _omni
    if _omni is None:
        _omni = OmniGraph()
    return _omni

