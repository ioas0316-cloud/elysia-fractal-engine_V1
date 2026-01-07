
import logging
import uuid
from typing import Dict, Any, List, Optional

class TreeNode:
    def __init__(self, data: Any, parent: Optional['TreeNode'] = None):
        self.id = str(uuid.uuid4())
        self.data = data
        self.parent = parent
        self.children: List['TreeNode'] = []
        self.meta: Dict[str, Any] = {}

    def add_child(self, child_node: 'TreeNode'):
        self.children.append(child_node)
        child_node.parent = self

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "data": self.data,
            "children": [child.to_dict() for child in self.children],
            "meta": self.meta
        }

class WorldTree:
    """
    The WorldTree represents knowledge as a fractal, hierarchical structure.
    It allows for infinite expansion of concepts into sub-concepts (branches).
    """

    def __init__(self, logger: Optional[logging.Logger] = None):
        self.root = TreeNode("ROOT")
        self.logger = logger or logging.getLogger("WorldTree")
        self.logger.info("WorldTree initialized.")

    def add_seed(self, concept: str, parent_id: Optional[str] = None) -> str:
        """
        Adds a new concept seed to the tree.
        If parent_id is provided, adds as a child of that node.
        Otherwise, adds as a child of the root.
        """
        new_node = TreeNode(concept)
        
        if parent_id:
            parent = self._find_node(self.root, parent_id)
            if parent:
                parent.add_child(new_node)
                self.logger.debug(f"Added seed '{concept}' to parent {parent_id}")
            else:
                self.logger.warning(f"Parent {parent_id} not found. Adding to root.")
                self.root.add_child(new_node)
        else:
            self.root.add_child(new_node)
            self.logger.debug(f"Added seed '{concept}' to root")
            
        return new_node.id

    def grow(self, branch_id: str, data: Any):
        """
        Expands a branch with new data (adds a child node).
        """
        return self.add_seed(data, parent_id=branch_id)

    def prune(self, branch_id: str):
        """
        Removes a branch and its children.
        """
        node_to_remove = self._find_node(self.root, branch_id)
        if node_to_remove and node_to_remove.parent:
            node_to_remove.parent.children.remove(node_to_remove)
            self.logger.info(f"Pruned branch {branch_id}")

    def _find_node(self, current_node: TreeNode, target_id: str) -> Optional[TreeNode]:
        if current_node.id == target_id:
            return current_node
        
        for child in current_node.children:
            found = self._find_node(child, target_id)
            if found:
                return found
        return None

    def visualize(self) -> Dict[str, Any]:
        """
        Returns the tree structure as a dictionary.
        """
        return self.root.to_dict()
