"""
Content Baptizer (Semantic Prism)
=================================
Renames Dark Matter nodes based on their CONTENT (Payload), ensuring UNIQUENESS.
Prevents "The Great Deletion" (Collisions).

Logic:
1. Read `node_metadata['payload']`.
2. Extract meaningful keywords (e.g., "formula", "constants").
3. Append a short Hash of the ID to guarantee uniqueness.
   e.g., Wikipedia_001 -> Concept_Formula_A1B2
"""

import logging
import hashlib
import re
import sys
import os

# Add project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Core.Foundation.Graph.torch_graph import get_torch_graph

logger = logging.getLogger("ContentBaptizer")

class ContentBaptizer:
    def __init__(self):
        self.graph = get_torch_graph()
        self.dark_pattern = re.compile(r"^(Wikipedia_\d+|Star-\d+|\d+)$")

    def _generate_unique_suffix(self, node_id):
        """Generates a short 8-char hash from the ID."""
        hash_obj = hashlib.md5(str(node_id).encode())
        return hash_obj.hexdigest()[:8].upper()

    def scan_dark_matter(self):
        """Returns list of Node IDs that need naming."""
        candidates = []
        for nid in self.graph.id_to_idx.keys():
            if self.dark_pattern.match(str(nid)):
                candidates.append(nid)
        return candidates

    def baptize(self, batch_size=50):
        """Renames a batch of nodes using Content + Hash."""
        candidates = self.scan_dark_matter()
        if not candidates:
            return 0

        logger.info(f"🌈 Baptizing {min(batch_size, len(candidates))} nodes using Semantic Prism...")
        
        count = 0
        renamed_map = {} # Old -> New

        for nid in candidates[:batch_size]:
            idx = self.graph.id_to_idx[nid]
            metadata = self.graph.node_metadata.get(nid, {})
            payload = str(metadata.get('payload', ''))
            
            # Base Name Derivation
            base_name = "Concept"
            
            if "formula" in payload:
                base_name = "Math_Formula"
            elif "constants" in payload:
                base_name = "Phy_Constant"
            elif "embryo" in payload:
                base_name = "Bio_Life"
            elif len(payload) > 5:
                # Text snippet? Use first word if clean
                clean_payload = re.sub(r'[^a-zA-Z0-9\s]', '', payload)
                words = clean_payload.split()
                if words:
                    base_name = f"Concept_{words[0]}"
                    
            # CRITICAL: Append Hash to ensure Uniqueness!
            # Using partial original ID or hash.
            # Original ID: Wikipedia_00019284 -> Suffix: 9284 (Too long?)
            # Let's use MD5 hash of the original ID.
            suffix = self._generate_unique_suffix(nid)
            
            new_name = f"{base_name}_{suffix}"
            
            # Rename
            renamed_map[nid] = new_name
            count += 1
            if count % 10 == 0:
                logger.info(f"   ✨ {nid} -> {new_name}")

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

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    baptist = ContentBaptizer()
    baptist.baptize(batch_size=20)
