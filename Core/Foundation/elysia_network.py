"""
Elysia Network - Network-level coordination and management.

Implements Phase 7.1: Multi-instance collaboration
Manages multiple Elysia nodes working together to solve complex problems.
"""

import asyncio
from typing import List, Dict, Any, Tuple
import time

from .elysia_node import ElysiaNode, Message


class ElysiaNetwork:
    """
    Network manager for collective intelligence.
    Coordinates multiple Elysia nodes for collaborative problem solving.
    """
    
    def __init__(self, topology: str = "mesh"):
        """
        Initialize network.
        
        Topologies:
        - mesh: All nodes connected to all others (full connectivity)
        - star: All nodes connected to one central hub
        - hierarchical: Tree structure with levels
        """
        self.nodes: List[ElysiaNode] = []
        self.topology = topology
        self.problem_history: List[Dict[str, Any]] = []
    
    def add_node(self, node: ElysiaNode):
        """Add a node to the network."""
        if node not in self.nodes:
            self.nodes.append(node)
            self._update_topology()
    
    def remove_node(self, node: ElysiaNode):
        """Remove a node from the network."""
        # [Wave Logic] Consider resonance-based lookup instead of direct membership check
        # Original: if node in self.nodes:
        if node in self.nodes:  # TODO: Convert to query_resonance
            # Disconnect from all peers
            for peer in self.nodes:
                if peer != node:
                    peer.remove_peer(node)
                    node.remove_peer(peer)
            
            self.nodes.remove(node)
    
    def _update_topology(self):
        """Update network connections based on topology."""
        if self.topology == "mesh":
            # Connect all nodes to each other
            for i, node in enumerate(self.nodes):
                for j, peer in enumerate(self.nodes):
                    if i != j:
                        node.add_peer(peer)
        
        elif self.topology == "star":
            # Connect all nodes to the first node (hub)
            if len(self.nodes) > 0:
                hub = self.nodes[0]
                for node in self.nodes[1:]:
                    hub.add_peer(node)
                    node.add_peer(hub)
        
        elif self.topology == "hierarchical":
            # Simple 2-level hierarchy
            # First node is coordinator, others are workers
            if len(self.nodes) > 0:
                coordinator = self.nodes[0]
                for worker in self.nodes[1:]:
                    coordinator.add_peer(worker)
                    worker.add_peer(coordinator)
    
    def decompose_problem(self, problem: str) -> List[str]:
        """
        Decompose a complex problem into subproblems.
        
        Uses simple keyword-based decomposition for demo purposes.
        In production, this would use advanced NLP and problem analysis.
        """
        # Check if problem mentions multiple aspects
        problem_lower = problem.lower()
        subproblems = []
        
        # Check for conjunction words
        if " and " in problem_lower:
            parts = problem.split(" and ")
            subproblems = [p.strip() for p in parts]
        elif " then " in problem_lower:
            parts = problem.split(" then ")
            subproblems = [p.strip() for p in parts]
        elif "," in problem:
            parts = problem.split(",")
            subproblems = [p.strip() for p in parts]
        else:
            # Single problem, but might need different perspectives
            subproblems = [
                f"Analyze {problem} logically",
                f"Consider creative solutions for {problem}",
                f"Evaluate {problem} emotionally"
            ]
        
        return subproblems[:len(self.nodes)]  # Don't create more subproblems than nodes
    
    def assign_to_specialists(self, subproblems: List[str]) -> List[Tuple[ElysiaNode, str]]:
        """
        Assign subproblems to nodes based on their specialization.
        
        Returns list of (node, subproblem) tuples.
        """
        assignments = []
        
        # Simple classification and assignment
        for subproblem in subproblems:
            # Find the best node for this subproblem
            best_node = None
            best_score = 0.0
            
            # Classify subproblem
            problem_type = self._classify_subproblem(subproblem)
            
            # Find node with highest strength for this type
            for node in self.nodes:
                score = node.strengths.get(problem_type, 0.5)
                if score > best_score:
                    best_score = score
                    best_node = node
            
            if best_node is None and self.nodes:
                best_node = self.nodes[0]  # Fallback to first node
            
            if best_node:
                assignments.append((best_node, subproblem))
        
        return assignments
    
    def _classify_subproblem(self, subproblem: str) -> str:
        """Classify what type of subproblem this is."""
        subproblem_lower = subproblem.lower()
        
        if any(word in subproblem_lower for word in ["creative", "imagine", "design", "innovate"]):
            return "creativity"
        elif any(word in subproblem_lower for word in ["emotion", "feel", "empathy"]):
            return "emotion"
        elif any(word in subproblem_lower for word in ["logic", "analyze", "reason", "prove"]):
            return "logic"
        elif any(word in subproblem_lower for word in ["pattern", "trend"]):
            return "pattern"
        elif any(word in subproblem_lower for word in ["integrate", "combine", "synthesize"]):
            return "integration"
        elif any(word in subproblem_lower for word in ["know", "fact", "information"]):
            return "knowledge"
        else:
            return "generalist"
    
    def integrate_solutions(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Integrate solutions from multiple nodes into a unified solution.
        
        Combines insights while preserving important details from each contributor.
        """
        if not results:
            return {"integrated_solution": "No solutions to integrate", "confidence": 0.0}
        
        # Calculate weighted confidence
        total_confidence = sum(r.get("confidence", 0.5) for r in results)
        avg_confidence = total_confidence / len(results) if results else 0.0
        
        # Combine solutions
        combined_solutions = []
        contributors = []
        
        for result in results:
            solution_text = result.get("solution", "")
            node_id = result.get("node_id", "unknown")
            specialization = result.get("specialization", "unknown")
            
            combined_solutions.append(f"[{specialization}]: {solution_text}")
            contributors.append({"node": node_id, "specialization": specialization})
        
        integrated = {
            "integrated_solution": " | ".join(combined_solutions),
            "confidence": avg_confidence,
            "contributors": contributors,
            "num_perspectives": len(results),
            "method": "collaborative_problem_solving"
        }
        
        return integrated
    
    async def collaborative_problem_solving(self, problem: str) -> Dict[str, Any]:
        """
        Solve a problem collaboratively using the entire network.
        
        Process:
        1. Decompose problem into subproblems
        2. Assign subproblems to specialist nodes
        3. Solve in parallel
        4. Integrate solutions
        """
        start_time = time.time()
        
        if not self.nodes:
            return {"error": "No nodes in network", "confidence": 0.0}
        
        # 1. Decompose problem
        subproblems = self.decompose_problem(problem)
        
        # 2. Assign to specialists
        assignments = self.assign_to_specialists(subproblems)
        
        # 3. Solve in parallel
        tasks = [node.solve(subproblem, method="independent") for node, subproblem in assignments]
        results = await asyncio.gather(*tasks)
        
        # 4. Integrate solutions
        integrated_solution = self.integrate_solutions(results)
        
        # Add metadata
        integrated_solution["problem"] = problem
        integrated_solution["subproblems"] = subproblems
        integrated_solution["num_nodes"] = len(self.nodes)
        integrated_solution["processing_time"] = time.time() - start_time
        integrated_solution["topology"] = self.topology
        
        # Record in history
        self.problem_history.append({
            "problem": problem,
            "solution": integrated_solution,
            "timestamp": time.time()
        })
        
        return integrated_solution
    
    async def consensus_solution(self, problem: str) -> Dict[str, Any]:
        """
        Solve a problem using consensus from all nodes.
        All nodes think independently, then vote on the best solution.
        """
        if not self.nodes:
            return {"error": "No nodes in network", "confidence": 0.0}
        
        # All nodes solve the same problem
        tasks = [node.solve(problem, method="independent") for node in self.nodes]
        all_solutions = await asyncio.gather(*tasks)
        
        # Use first node's consensus mechanism to integrate
        consensus = self.nodes[0].reach_consensus(all_solutions)
        consensus["problem"] = problem
        consensus["method"] = "network_consensus"
        
        return consensus
    
    def get_network_status(self) -> Dict[str, Any]:
        """Get overall network status."""
        if not self.nodes:
            return {"status": "empty", "nodes": 0}
        
        total_problems = sum(n.performance_metrics["problems_solved"] for n in self.nodes)
        avg_quality = sum(n.performance_metrics["quality_score"] for n in self.nodes) / len(self.nodes)
        
        node_statuses = [n.get_status() for n in self.nodes]
        
        # Identify specializations
        specializations = {}
        for node in self.nodes:
            spec = node.specialization
            specializations[spec] = specializations.get(spec, 0) + 1
        
        return {
            "status": "active",
            "num_nodes": len(self.nodes),
            "topology": self.topology,
            "total_problems_solved": total_problems,
            "avg_quality_score": avg_quality,
            "specializations": specializations,
            "nodes": node_statuses,
            "problems_in_history": len(self.problem_history)
        }
