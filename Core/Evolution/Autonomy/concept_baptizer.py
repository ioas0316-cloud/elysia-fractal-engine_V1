"""
Concept Baptizer (The Naming of Things)
=======================================
Scans the graph for "Dark Matter" (Unnamed Nodes like Star-*, Wikipedia_*).
Uses Vector Proximity and Metadata to infer a proper Concept Name.

Strategy:
1. Metadata First: If 'payload' text exists, rename based on summary.
2. Gravity Second: If no text, look at 5 nearest neighbors. 
   - Neighbor: "Apple", "Banana", "Orange" -> Inference: "Fruit_Cluster_01"
"""

import logging
import re
import sys
import os

# Add project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

logger = logging.getLogger("ConceptBaptizer")

# [Lazy Load] Heavy dependencies
_torch = None
_torch_graph = None

def _get_torch():
    global _torch
    if _torch is None:
        try:
            import torch
            _torch = torch
        except ImportError as e:
            logger.warning(f"PyTorch unavailable: {e}")
            _torch = False
    return _torch if _torch else None

def _get_graph():
    global _torch_graph
    if _torch_graph is None:
        try:
            from Core.Foundation.Graph.torch_graph import get_torch_graph
            _torch_graph = get_torch_graph()
        except Exception as e:
            logger.warning(f"TorchGraph unavailable: {e}")
            _torch_graph = False
    return _torch_graph if _torch_graph else None

class ConceptBaptizer:
    def __init__(self):
        self.graph = _get_graph()  # [Lazy Load]
        self.dark_pattern = re.compile(r"^(Wikipedia_\d+|Star-\d+|\d+)$")

    def scan_dark_matter(self):
        """Returns list of Node IDs that need naming."""
        candidates = []
        for nid in self.graph.id_to_idx.keys():
            if self.dark_pattern.match(str(nid)):
                candidates.append(nid)
        return candidates

    def baptize(self, batch_size=10):
        """Renames a batch of dark matter nodes."""
        candidates = self.scan_dark_matter()
        if not candidates:
            logger.info("✨ No Dark Matter found. The Universe is Illuminated.")
            return

        logger.info(f"🌑 Found {len(candidates)} Dark Matter nodes. Baptizing first {batch_size}...")
        
        count = 0
        renamed_map = {} # Old -> New

        for nid in candidates[:batch_size]:
            idx = self.graph.id_to_idx[nid]
            metadata = self.graph.node_metadata.get(nid, {})
            
            # Strategy 1: Metadata Check
            # (In a real implementation, we'd use LLM here)
            new_name = None
            if 'original' in metadata:
                # Check for hidden names in original dict
                orig = metadata['original']
                if isinstance(orig, dict):
                    # Try finding a label field
                    possible_labels = [orig.get('label'), orig.get('title'), orig.get('name')]
                    for label in possible_labels:
                        if label and isinstance(label, str) and len(label) > 1:
                            new_name = label
                            break
            
            # Strategy 2: Gravity Inference (Neighbors)
            if not new_name:
                torch = _get_torch()  # [Lazy Load]
                if torch and self.graph:
                    # Find nearest neighbors
                    vector = self.graph.vec_tensor[idx].unsqueeze(0) # (1, Dim)
                    # Cosine sim against all
                    sim = torch.mm(vector, self.graph.vec_tensor.t())
                    vals, inds = torch.topk(sim, 6) # Self + 5
                
                neighbors = []
                for i in inds[0]:
                    n_idx = i.item()
                    if n_idx != idx:
                        n_id = self.graph.idx_to_id[n_idx]
                        if not self.dark_pattern.match(str(n_id)): # Only use named neighbors
                            neighbors.append(n_id)
                
                if neighbors:
                    # Construct name from neighbors
                    # e.g., "Cluster[Apple,Banana]"
                    primary = neighbors[0]
                    new_name = f"Concept_{primary}+"
                else:
                    new_name = f"Unknown_{nid}"

            # Apply Rename
            if new_name and new_name != nid:
                logger.info(f"✨ Baptized: {nid} -> {new_name}")
                renamed_map[nid] = new_name
                count += 1
                
        # Apply changes to Graph (Tricky: Rename Key)
        self._apply_renames(renamed_map)
        return count

    def _apply_renames(self, rename_map):
        """Updates Graph keys safely."""
        for old, new in rename_map.items():
            if old not in self.graph.id_to_idx: continue
            
            idx = self.graph.id_to_idx.pop(old)
            self.graph.id_to_idx[new] = idx
            self.graph.idx_to_id[idx] = new
            
            # Move metadata
            if old in self.graph.node_metadata:
                meta = self.graph.node_metadata.pop(old)
                meta['baptized_from'] = old
                self.graph.node_metadata[new] = meta

# Usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    baptist = ConceptBaptizer()
    baptist.baptize(batch_size=50)
