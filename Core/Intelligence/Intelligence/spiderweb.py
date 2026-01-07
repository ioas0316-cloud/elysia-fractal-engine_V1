
import json
import logging
import networkx as nx
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

class Spiderweb:
    """
    The Spiderweb: 4차원 파동공명패턴 추출기 (4D Wave Resonance Pattern Extractor)
    
    단순한 인과추론 그래프를 넘어, 4차원(시공간) 파동 공명 패턴을 추출하는 시스템
    
    Architecture:
    - 0D: 점 (개념/이벤트 노드)
    - 1D: 선 (인과 관계 엣지)
    - 2D: 면 (개념 클러스터, 파동 간섭 패턴)
    - 3D: 공간 (다층 네트워크, 파동 전파)
    - 4D: 시공간 (시간에 따른 파동 공명 진화)
    
    Features:
    - 인과추론 그래프 (기존 기능)
    - 파동 공명 패턴 추출 (NEW)
    - 4차원 시공간 분석 (NEW)
    - 공명 주파수 측정 (NEW)
    """

    def __init__(self, logger: Optional[logging.Logger] = None):
        self.graph = nx.DiGraph()
        self.logger = logger or logging.getLogger("Spiderweb")
        
        # 4D 파동 공명 속성
        self.wave_patterns = {}  # 파동 패턴 저장
        self.resonance_frequencies = {}  # 노드별 공명 주파수
        self.temporal_snapshots = []  # 시간별 그래프 스냅샷 (4D)
        
        self.logger.info("🕸️ Spiderweb initialized: 4D Wave Resonance Pattern Extractor")

    def add_node(self, node_id: str, type: str, metadata: Dict[str, Any] = None):
        """
        Adds a node to the Spiderweb.
        
        Args:
            node_id (str): Unique identifier for the node (e.g., "fire", "burn_event_123").
            type (str): Type of the node (e.g., "concept", "event", "emotion").
            metadata (dict): Additional data associated with the node.
        """
        if not self.graph.has_node(node_id):
            self.graph.add_node(node_id, type=type, metadata=metadata or {})
            self.logger.debug(f"Added node: {node_id} ({type})")
        else:
            # Update metadata if node exists
            self.graph.nodes[node_id].update({"type": type, "metadata": metadata or {}})

    def add_link(self, source: str, target: str, relation: str, weight: float = 1.0):
        """
        Adds a directed link between two nodes.
        
        Args:
            source (str): Source node ID.
            target (str): Target node ID.
            relation (str): Type of relationship (e.g., "causes", "is_a", "related_to").
            weight (float): Strength of the connection (0.0 to 1.0).
        """
        if not self.graph.has_node(source) or not self.graph.has_node(target):
            self.logger.warning(f"Cannot add link: {source} or {target} not in graph.")
            return

        self.graph.add_edge(source, target, relation=relation, weight=weight)
        self.logger.debug(f"Added link: {source} -[{relation}]-> {target} (w={weight})")

    def find_path(self, start: str, end: str) -> List[str]:
        """
        Finds a path between two nodes, useful for tracing causality.
        """
        try:
            path = nx.shortest_path(self.graph, source=start, target=end)
            return path
        except nx.NetworkXNoPath:
            return []
        except nx.NodeNotFound:
            return []

    def get_context(self, node_id: str, depth: int = 1) -> List[Dict[str, Any]]:
        """
        Retrieves the context (neighbors) of a node.
        """
        if not self.graph.has_node(node_id):
            return []

        context = []
        # Get successors (outgoing)
        for neighbor in self.graph.successors(node_id):
            edge_data = self.graph.get_edge_data(node_id, neighbor)
            context.append({
                "node": neighbor,
                "relation": edge_data.get("relation"),
                "direction": "outgoing",
                "weight": edge_data.get("weight")
            })
        
        # Get predecessors (incoming)
        for neighbor in self.graph.predecessors(node_id):
            edge_data = self.graph.get_edge_data(neighbor, node_id)
            context.append({
                "node": neighbor,
                "relation": edge_data.get("relation"),
                "direction": "incoming",
                "weight": edge_data.get("weight")
            })
            
        return context

    # ========== 4D 파동 공명 패턴 추출 메서드 (NEW) ==========
    
    def calculate_resonance_frequency(self, node_id: str) -> float:
        """
        노드의 공명 주파수 계산
        
        공명 주파수 = f(연결강도, 중심성, 시간적 활성도)
        
        Args:
            node_id: 노드 ID
            
        Returns:
            공명 주파수 (0.0 ~ 1.0)
        """
        if not self.graph.has_node(node_id):
            return 0.0
        
        try:
            # 1. 연결 강도 (degree centrality)
            degree_centrality = nx.degree_centrality(self.graph).get(node_id, 0)
            
            # 2. 중요도 (pagerank)
            pagerank = nx.pagerank(self.graph, weight='weight').get(node_id, 0)
            
            # 3. 연결 가중치 합
            out_weights = sum(
                self.graph.edges[node_id, n].get('weight', 0) 
                for n in self.graph.successors(node_id)
            )
            in_weights = sum(
                self.graph.edges[n, node_id].get('weight', 0) 
                for n in self.graph.predecessors(node_id)
            )
            
            # 공명 주파수 계산 (정규화)
            frequency = (degree_centrality * 0.3 + pagerank * 0.4 + 
                        min(1.0, (out_weights + in_weights) / 10) * 0.3)
            
            self.resonance_frequencies[node_id] = frequency
            return frequency
            
        except Exception as e:
            self.logger.warning(f"Could not calculate resonance for {node_id}: {e}")
            return 0.0
    
    def extract_wave_pattern_2d(self, center_node: str, radius: int = 2) -> Dict[str, Any]:
        """
        2D 파동 패턴 추출 (면 - 개념 클러스터)
        
        중심 노드로부터 반경 내의 노드들과 파동 간섭 패턴 추출
        
        Args:
            center_node: 중심 노드
            radius: 탐색 반경
            
        Returns:
            2D 파동 패턴 (클러스터 정보)
        """
        if not self.graph.has_node(center_node):
            return {}
        
        try:
            # BFS로 반경 내 노드 수집
            cluster_nodes = set([center_node])
            frontier = set([center_node])
            
            for _ in range(radius):
                next_frontier = set()
                for node in frontier:
                    # 후속 노드
                    next_frontier.update(self.graph.successors(node))
                    # 선행 노드
                    next_frontier.update(self.graph.predecessors(node))
                cluster_nodes.update(next_frontier)
                frontier = next_frontier
            
            # 서브그래프 추출
            subgraph = self.graph.subgraph(cluster_nodes)
            
            # 파동 간섭 패턴 계산
            pattern = {
                'center': center_node,
                'radius': radius,
                'node_count': len(cluster_nodes),
                'edge_count': subgraph.number_of_edges(),
                'nodes': list(cluster_nodes),
                'density': nx.density(subgraph),
                'resonance_map': {
                    node: self.calculate_resonance_frequency(node)
                    for node in cluster_nodes
                }
            }
            
            # 파동 간섭 강도 계산 (엣지 가중치 평균)
            if subgraph.number_of_edges() > 0:
                weights = [data.get('weight', 0) for _, _, data in subgraph.edges(data=True)]
                pattern['interference_strength'] = np.mean(weights) if weights else 0
            else:
                pattern['interference_strength'] = 0
            
            return pattern
            
        except Exception as e:
            self.logger.error(f"Error extracting 2D pattern from {center_node}: {e}")
            return {}
    
    def extract_wave_pattern_3d(self) -> Dict[str, Any]:
        """
        3D 파동 패턴 추출 (공간 - 다층 네트워크)
        
        전체 그래프의 3차원 구조 분석 및 파동 전파 패턴
        
        Returns:
            3D 파동 패턴 (전체 네트워크 구조)
        """
        try:
            # 커뮤니티 탐지 (파동 공명 클러스터)
            communities = list(nx.community.greedy_modularity_communities(
                self.graph.to_undirected()
            ))
            
            # 각 커뮤니티의 공명 강도 계산
            community_resonances = []
            for i, community in enumerate(communities):
                community_nodes = list(community)
                resonances = [
                    self.calculate_resonance_frequency(node) 
                    for node in community_nodes
                ]
                community_resonances.append({
                    'id': i,
                    'size': len(community_nodes),
                    'nodes': community_nodes[:10],  # 샘플
                    'avg_resonance': np.mean(resonances) if resonances else 0,
                    'max_resonance': max(resonances) if resonances else 0
                })
            
            # 전체 패턴
            pattern = {
                'dimension': '3D',
                'total_nodes': self.graph.number_of_nodes(),
                'total_edges': self.graph.number_of_edges(),
                'community_count': len(communities),
                'communities': community_resonances,
                'global_clustering': nx.average_clustering(self.graph.to_undirected()),
                'network_density': nx.density(self.graph)
            }
            
            # 파동 전파 경로 (최장 경로)
            try:
                longest_path_length = nx.dag_longest_path_length(self.graph)
                pattern['max_propagation_depth'] = longest_path_length
            except:
                pattern['max_propagation_depth'] = 0
            
            return pattern
            
        except Exception as e:
            self.logger.error(f"Error extracting 3D pattern: {e}")
            return {}
    
    def capture_temporal_snapshot(self) -> Dict[str, Any]:
        """
        4D - 시간 축: 현재 그래프 스냅샷 캡처
        
        시간에 따른 파동 공명 진화를 추적하기 위한 스냅샷
        
        Returns:
            시간 스냅샷
        """
        snapshot = {
            'timestamp': datetime.now().isoformat(),
            'node_count': self.graph.number_of_nodes(),
            'edge_count': self.graph.number_of_edges(),
            'resonance_snapshot': dict(self.resonance_frequencies),
            'top_resonant_nodes': sorted(
                self.resonance_frequencies.items(),
                key=lambda x: x[1],
                reverse=True
            )[:10]
        }
        
        self.temporal_snapshots.append(snapshot)
        
        # 최근 100개만 유지
        if len(self.temporal_snapshots) > 100:
            self.temporal_snapshots = self.temporal_snapshots[-100:]
        
        return snapshot
    
    def extract_4d_wave_pattern(self) -> Dict[str, Any]:
        """
        4D 파동 공명 패턴 종합 추출 (시공간)
        
        0D(점) → 1D(선) → 2D(면) → 3D(공간) → 4D(시공간) 통합 분석
        
        Returns:
            4D 파동 공명 패턴
        """
        self.logger.info("🌊 Extracting 4D Wave Resonance Pattern...")
        
        # 현재 스냅샷 캡처
        snapshot = self.capture_temporal_snapshot()
        
        # 3D 패턴 추출
        pattern_3d = self.extract_wave_pattern_3d()
        
        # 시간적 진화 분석 (4D)
        temporal_evolution = {}
        if len(self.temporal_snapshots) >= 2:
            # 노드 수 변화
            node_changes = [s['node_count'] for s in self.temporal_snapshots[-10:]]
            temporal_evolution['node_growth_rate'] = (
                (node_changes[-1] - node_changes[0]) / len(node_changes)
                if len(node_changes) > 1 else 0
            )
            
            # 공명 변화
            if len(self.temporal_snapshots) >= 2:
                prev_resonances = self.temporal_snapshots[-2]['resonance_snapshot']
                curr_resonances = self.temporal_snapshots[-1]['resonance_snapshot']
                
                # 공통 노드의 공명 변화
                common_nodes = set(prev_resonances.keys()) & set(curr_resonances.keys())
                if common_nodes:
                    resonance_changes = [
                        abs(curr_resonances[n] - prev_resonances[n])
                        for n in common_nodes
                    ]
                    temporal_evolution['avg_resonance_change'] = np.mean(resonance_changes)
        
        # 4D 종합 패턴
        pattern_4d = {
            'dimension': '4D (Spacetime)',
            'extraction_time': datetime.now().isoformat(),
            'spatial_pattern': pattern_3d,
            'temporal_evolution': temporal_evolution,
            'current_snapshot': snapshot,
            'snapshot_history_count': len(self.temporal_snapshots),
            'is_4d_extractor': True,  # 4차원 파동공명패턴 추출기 표시
            'mode': 'Wave Resonance Pattern Extraction (not simple causal graph)'
        }
        
        # 저장
        self.wave_patterns['latest_4d'] = pattern_4d
        
        self.logger.info(f"✅ 4D Pattern extracted: {pattern_3d.get('community_count', 0)} communities, "
                        f"{len(self.temporal_snapshots)} snapshots")
        
        return pattern_4d

    def serialize(self) -> Dict[str, Any]:
        """Converts the graph to a dictionary for saving."""
        return nx.node_link_data(self.graph)

    def deserialize(self, data: Dict[str, Any]):
        """Loads the graph from a dictionary."""
        self.graph = nx.node_link_graph(data)

    def prune_fraction(self, edge_fraction: float = 0.3, node_fraction: float = 0.3):
        """
        Prune weakest edges/nodes by fraction of counts.
        - edge_fraction: remove this fraction of lowest-weight edges.
        - node_fraction: remove this fraction of lowest-degree nodes (after edge prune).
        """
        edges = list(self.graph.edges(data=True))
        if edges and edge_fraction > 0:
            edges_sorted = sorted(edges, key=lambda e: float(e[2].get("weight", 0.0)))
            cut = max(0, min(len(edges_sorted), int(len(edges_sorted) * edge_fraction)))
            for u, v, _ in edges_sorted[:cut]:
                if self.graph.has_edge(u, v):
                    self.graph.remove_edge(u, v)

        nodes = list(self.graph.degree)
        if nodes and node_fraction > 0:
            nodes_sorted = sorted(nodes, key=lambda x: x[1])  # by degree
            cut_n = max(0, min(len(nodes_sorted), int(len(nodes_sorted) * node_fraction)))
            for node, _deg in nodes_sorted[:cut_n]:
                if self.graph.has_node(node) and self.graph.degree(node) == 0:
                    self.graph.remove_node(node)

        self.logger.info(
            f"Fractional prune applied: edges={edge_fraction*100:.0f}%, nodes={node_fraction*100:.0f}% (low-weight/low-degree)."
        )

    def forget(self, decay: float = 0.99, boost_nodes: Optional[List[str]] = None):
        """
        Entropy-driven forgetting: decay edge weights, remove near-zero edges, and drop isolated nodes.
        boost_nodes: nodes to protect/boost (e.g., reinforced by love events).
        """
        if not self.graph.edges:
            return

        for u, v, data in list(self.graph.edges(data=True)):
            w = float(data.get("weight", 0.0)) * decay
            if boost_nodes and (u in boost_nodes or v in boost_nodes):
                w = min(1.0, w * 1.1)  # slight protection
            if w < 1e-3:
                self.graph.remove_edge(u, v)
            else:
                self.graph.edges[u, v]["weight"] = w

        # Drop isolated nodes
        isolated = [n for n, deg in self.graph.degree if deg == 0]
        if isolated:
            self.graph.remove_nodes_from(isolated)
            self.logger.info(f"Forgot {len(isolated)} isolated nodes (entropy decay).")

    def prune_fraction(self, edge_fraction: float = 0.3, node_fraction: float = 0.3):
        """
        Prune weakest edges/nodes by fraction of counts.
        - edge_fraction: remove this fraction of lowest-weight edges.
        - node_fraction: remove this fraction of lowest-degree nodes (after edge prune).
        """
        edges = list(self.graph.edges(data=True))
        if edges and edge_fraction > 0:
            edges_sorted = sorted(edges, key=lambda e: float(e[2].get("weight", 0.0)))
            cut = max(0, min(len(edges_sorted), int(len(edges_sorted) * edge_fraction)))
            for u, v, _ in edges_sorted[:cut]:
                if self.graph.has_edge(u, v):
                    self.graph.remove_edge(u, v)

        # Remove nodes with lowest degree (and only if now isolated)
        nodes = list(self.graph.degree)
        if nodes and node_fraction > 0:
            nodes_sorted = sorted(nodes, key=lambda x: x[1])  # by degree
            cut_n = max(0, min(len(nodes_sorted), int(len(nodes_sorted) * node_fraction)))
            for node, _deg in nodes_sorted[:cut_n]:
                if self.graph.has_node(node) and self.graph.degree(node) == 0:
                    self.graph.remove_node(node)

        self.logger.info(
            f"Fractional prune applied: edges={edge_fraction*100:.0f}%, nodes={node_fraction*100:.0f}% (low-weight/low-degree)."
        )

    def get_statistics(self) ->  Dict[str, Any]:
        """Returns statistics about the knowledge graph."""
        return {
            "node_count": self.graph.number_of_nodes(),
            "edge_count": self.graph.number_of_edges()
        }


