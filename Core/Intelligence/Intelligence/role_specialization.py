"""
Role Specialization - Dynamic role assignment and load balancing.

Implements Phase 7.3: Role Specialization
Manages role assignment and rebalancing across the network.
"""

from typing import List, Dict, Any, Optional
from enum import Enum


class Role(Enum):
    """Roles that nodes can be assigned in the network."""
    KNOWLEDGE_KEEPER = "knowledge_keeper"  # Knowledge storage and retrieval
    PATTERN_RECOGNIZER = "pattern_recognizer"  # Pattern recognition specialist
    CREATIVE_GENERATOR = "creative_generator"  # Creative idea generation
    LOGIC_VALIDATOR = "logic_validator"  # Logical reasoning and validation
    EMOTION_PROCESSOR = "emotion_processor"  # Emotional processing
    INTEGRATION_SYNTHESIZER = "integration_synthesizer"  # Integration and synthesis


class SpecializationManager:
    """
    Manages role specialization and load balancing in the network.
    Dynamically assigns and rebalances roles based on node performance.
    """
    
    ROLE_DESCRIPTIONS = {
        Role.KNOWLEDGE_KEEPER: "Stores and retrieves knowledge efficiently",
        Role.PATTERN_RECOGNIZER: "Identifies patterns and trends in data",
        Role.CREATIVE_GENERATOR: "Generates creative and innovative solutions",
        Role.LOGIC_VALIDATOR: "Validates logical consistency and correctness",
        Role.EMOTION_PROCESSOR: "Processes emotional content and generates empathic responses",
        Role.INTEGRATION_SYNTHESIZER: "Integrates multiple perspectives into cohesive solutions"
    }
    
    # Mapping from specializations to roles
    SPECIALIZATION_TO_ROLE = {
        "knowledge": Role.KNOWLEDGE_KEEPER,
        "pattern": Role.PATTERN_RECOGNIZER,
        "creativity": Role.CREATIVE_GENERATOR,
        "logic": Role.LOGIC_VALIDATOR,
        "emotion": Role.EMOTION_PROCESSOR,
        "integration": Role.INTEGRATION_SYNTHESIZER
    }
    
    def __init__(self):
        self.role_assignments: Dict[str, Role] = {}  # node_id -> Role
        self.role_loads: Dict[Role, int] = {role: 0 for role in Role}
        self.load_threshold = 10  # Tasks per role before rebalancing
    
    def analyze_node_strengths(self, node: Any) -> Dict[Role, float]:
        """
        Analyze a node's strengths for different roles.
        
        Returns dict mapping Role to strength score (0.0-1.0)
        """
        strengths = {}
        
        # Get node's capability strengths
        node_strengths = getattr(node, 'strengths', {})
        
        # Map each role to corresponding strength
        for specialization, role in self.SPECIALIZATION_TO_ROLE.items():
            strength = node_strengths.get(specialization, 0.5)
            strengths[role] = strength
        
        return strengths
    
    def assign_role(self, node: Any, role: Role):
        """Assign a specific role to a node."""
        node_id = getattr(node, 'node_id', str(id(node)))
        
        # Remove old assignment if exists
        if node_id in self.role_assignments:
            old_role = self.role_assignments[node_id]
            self.role_loads[old_role] = max(0, self.role_loads[old_role] - 1)
        
        # Assign new role
        self.role_assignments[node_id] = role
        self.role_loads[role] = self.role_loads.get(role, 0) + 1
        
        # Update node's metadata if possible
        if hasattr(node, 'assigned_role'):
            node.assigned_role = role
    
    def assign_roles(self, nodes: List[Any]):
        """
        Assign optimal roles to all nodes based on their strengths.
        
        Process:
        1. Analyze each node's strengths
        2. Find best role match for each node
        3. Assign roles, balancing load
        """
        # Clear existing assignments
        self.role_assignments.clear()
        self.role_loads = {role: 0 for role in Role}
        
        # Create list of (node, role, strength) tuples
        assignments_candidates = []
        
        for node in nodes:
            strengths = self.analyze_node_strengths(node)
            
            # Get top 3 roles for this node
            sorted_roles = sorted(strengths.items(), key=lambda x: x[1], reverse=True)
            
            for role, strength in sorted_roles[:3]:  # Top 3 candidates
                node_id = getattr(node, 'node_id', str(id(node)))
                assignments_candidates.append((node, node_id, role, strength))
        
        # Sort by strength (descending)
        assignments_candidates.sort(key=lambda x: x[3], reverse=True)
        
        # Assign roles, preferring high-strength matches
        assigned_nodes = set()
        
        for node, node_id, role, strength in assignments_candidates:
            if node_id not in assigned_nodes:
                self.assign_role(node, role)
                assigned_nodes.add(node_id)
    
    def identify_overloaded_roles(self) -> List[Role]:
        """
        Identify roles that are overloaded.
        A role is overloaded if it has more than the threshold number of tasks.
        """
        overloaded = []
        
        for role, load in self.role_loads.items():
            if load > self.load_threshold:
                overloaded.append(role)
        
        return overloaded
    
    async def redistribute_roles(self, overloaded_roles: List[Role], nodes: List[Any]):
        """
        Redistribute roles to balance load.
        
        Process:
        1. Identify nodes with overloaded roles
        2. Find capable nodes with lighter loads
        3. Reassign some nodes to different roles
        """
        for overloaded_role in overloaded_roles:
            # Find nodes with this role
            nodes_with_role = []
            for node in nodes:
                node_id = getattr(node, 'node_id', str(id(node)))
                if self.role_assignments.get(node_id) == overloaded_role:
                    nodes_with_role.append(node)
            
            # If multiple nodes have this role, reassign some to secondary capabilities
            if len(nodes_with_role) > 1:
                # Reassign the weakest node to its second-best role
                weakest_node = None
                weakest_strength = 1.0
                
                for node in nodes_with_role:
                    strengths = self.analyze_node_strengths(node)
                    role_strength = strengths.get(overloaded_role, 0.5)
                    
                    if role_strength < weakest_strength:
                        weakest_strength = role_strength
                        weakest_node = node
                
                if weakest_node:
                    # Find alternative role for weakest node
                    strengths = self.analyze_node_strengths(weakest_node)
                    
                    # Find best alternative (not the current overloaded role)
                    alternatives = [(r, s) for r, s in strengths.items() if r != overloaded_role]
                    if alternatives:
                        best_alternative = max(alternatives, key=lambda x: x[1])
                        self.assign_role(weakest_node, best_alternative[0])
    
    async def dynamic_rebalancing(self, nodes: List[Any]):
        """
        Perform dynamic role rebalancing based on current load.
        
        This should be called periodically to maintain balanced load.
        """
        # Identify overloaded roles
        overloaded_roles = self.identify_overloaded_roles()
        
        if overloaded_roles:
            # Redistribute to balance load
            await self.redistribute_roles(overloaded_roles, nodes)
    
    def get_role_distribution(self) -> Dict[str, int]:
        """Get current distribution of roles across nodes."""
        distribution = {}
        for role in Role:
            distribution[role.value] = self.role_loads.get(role, 0)
        return distribution
    
    def get_node_role(self, node: Any) -> Optional[Role]:
        """Get the role assigned to a specific node."""
        node_id = getattr(node, 'node_id', str(id(node)))
        return self.role_assignments.get(node_id)
    
    def is_balanced(self) -> bool:
        """Check if roles are reasonably balanced."""
        loads = list(self.role_loads.values())
        if not loads:
            return True
        
        max_load = max(loads)
        min_load = min(loads)
        
        # Balanced if difference is less than threshold
        return (max_load - min_load) <= 3
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about role assignments."""
        return {
            "total_assignments": len(self.role_assignments),
            "role_distribution": self.get_role_distribution(),
            "is_balanced": self.is_balanced(),
            "load_threshold": self.load_threshold,
            "overloaded_roles": [r.value for r in self.identify_overloaded_roles()]
        }

