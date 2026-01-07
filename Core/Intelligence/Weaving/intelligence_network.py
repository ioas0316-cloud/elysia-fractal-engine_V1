from typing import List, Dict, Tuple
from .intelligence_line import IntelligenceLine
from .universal_line import UniversalLine

class IntelligenceNetwork:
    """
    Manages the web of Intelligence Lines.
    It treats each Intelligence Line as a 'Node' and calculates
    the 'Resonance' (Connections) between them based on shared principles (keywords).
    """

    def __init__(self, lines: List[IntelligenceLine]):
        self.nodes: Dict[str, IntelligenceLine] = {line.name: line for line in lines}
        self.edges: Dict[str, List[Tuple[str, float]]] = {} # Adjacency list with weight

        self._build_network()

    def _build_network(self):
        """
        Calculates resonance between all pairs of nodes to build the graph.
        """
        node_names = list(self.nodes.keys())
        for i in range(len(node_names)):
            for j in range(i + 1, len(node_names)):
                name_a = node_names[i]
                name_b = node_names[j]

                line_a = self.nodes[name_a]
                line_b = self.nodes[name_b]

                # Calculate Resonance
                resonance = self._calculate_resonance(line_a, line_b)

                if resonance > 0:
                    self._add_edge(name_a, name_b, resonance)

    def _calculate_resonance(self, line_a: IntelligenceLine, line_b: IntelligenceLine) -> float:
        """
        Determines how much two intelligences overlap.
        For UniversalLines, we compare keywords.
        """
        if not isinstance(line_a, UniversalLine) or not isinstance(line_b, UniversalLine):
            return 0.0

        set_a = set(line_a.keywords)
        set_b = set(line_b.keywords)

        intersection = set_a.intersection(set_b)
        union = set_a.union(set_b)

        if not union:
            return 0.0

        # Jaccard Similarity variant
        return len(intersection) / len(union)

    def _add_edge(self, u: str, v: str, weight: float):
        if u not in self.edges: self.edges[u] = []
        if v not in self.edges: self.edges[v] = []

        self.edges[u].append((v, weight))
        self.edges[v].append((u, weight))

    def get_related_intelligences(self, name: str) -> List[Tuple[str, float]]:
        """
        Returns a list of intelligences related to the given one.
        """
        return sorted(self.edges.get(name, []), key=lambda x: x[1], reverse=True)

    def visualize_connections(self):
        """
        Prints the network structure.
        """
        print("\n[Intelligence Network Topology]")
        for node, neighbors in self.edges.items():
            connected = ", ".join([f"{n}({w:.2f})" for n, w in neighbors])
            print(f"  * {node} <--> {connected}")
