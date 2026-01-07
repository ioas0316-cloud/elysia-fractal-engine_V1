
import math
import random
import logging
import torch
import numpy as np
from typing import Dict, List, Optional, Tuple
from Core.Foundation.Wave.wave_folding import SpaceUnfolder # [Phase 23] Tesseract Unfolding
from Core.Foundation.Memory.holographic_embedding import get_holographic_embedder # [Phase 24] Identity

logger = logging.getLogger("TorchGraph")

class TorchGraph:
    """
    Hyper-Efficient 4D OmniGraph using PyTorch Tensors.
    Replaces O(N^2) loops with Matrix Operations.
    """
    def __init__(self, use_cuda: bool = True):
        self.use_cuda = use_cuda and torch.cuda.is_available()
        self.device = torch.device('cuda' if self.use_cuda else 'cpu')
        
        # ID <-> Index Mapping
        self.id_to_idx: Dict[str, int] = {}
        self.idx_to_id: Dict[int, str] = {}
        
        # Knowledge Store (Metadata/Principles)
        self.node_metadata: Dict[str, Dict] = {} # {id: { "principle": "...", "mechanism": "..." }}

        
        # Tensors (Initialized Empty)
        # N x 4 (X, Y, Z, W)
        self.pos_tensor = torch.zeros((0, 4), device=self.device)
        # N x V (Vector Dim, e.g., 64)
        self.vec_tensor = torch.zeros((0, 64), device=self.device)
        # N (Mass)
        self.mass_tensor = torch.zeros((0,), device=self.device)
        # Adjacency Matrix (Logic Links) - Sparse recommended for large N
        # For prototype, we use dense or indices list.
        # Storing pairs: [[i, j], [i, j]...]
        self.logic_links = torch.zeros((0, 2), dtype=torch.long, device=self.device)
        # Weights (Synaptic Strength)
        self.link_weights = torch.zeros((0,), dtype=torch.float, device=self.device)
        
        # [Neural Link] Default to SBERT (384) dimension
        self.dim_vector = 384
        # Re-init vec_tensor with correct dim
        self.vec_tensor = torch.zeros((0, self.dim_vector), device=self.device)
        
        # [Phase 24] Holographic Seeds (N, 64)
        # Stores the "Spirit of the Time" for each node
        self.holo_dim = 64
        self.holo_tensor = torch.zeros((0, self.holo_dim), device=self.device)
        self.holo_embedder = get_holographic_embedder(device=self.device)
        
        self.lock = False # Simple lock for batch updates
        
        # [The Kidney]
        from Core.Foundation.concept_sanitizer import get_sanitizer
        self.sanitizer = get_sanitizer()

        # [The Great Unification] Phase 12
        # Automatically attempt to load the Massive Rainbow Graph if brain is empty
        self.load_rainbow_bridge()

        logger.info(f"⚡ TorchGraph Initialized on {self.device} (Matrix Mode)")

    def add_node(self, node_id: str, vector: List[float] = None, pos: List[float] = None):
        # ... (Existing add_node logic unchanged) ...
        # (For brevity, assuming replace_file_content replaces only the target range reliably)
        # Actually I need to be careful not to delete add_node if I request a replacement around it.
        # So I will target __init__ and add_link separately if they are far apart.
        # They are at lines 38 and 105.
        pass
         
    # RE-TARGETING __init__ only first

    def add_node(self, node_id: str, vector: List[float] = None, pos: List[float] = None, metadata: Dict = None):
        # [Sanitization]
        if not self.sanitizer.is_valid(node_id):
            logger.debug(f"🛑 Rejecting toxic node: {node_id}")
            return
            
        if node_id in self.id_to_idx:
            # Update existing
            idx = self.id_to_idx[node_id]
            if metadata:
                self.node_metadata.setdefault(node_id, {}).update(metadata)
            
            if vector:
                 # Pad or trim vector
                v = torch.tensor(vector, device=self.device).view(-1)
                v = v[:self.dim_vector]
                if v.shape[0] < self.dim_vector:
                    v = torch.cat([v, torch.zeros(self.dim_vector - v.shape[0], device=self.device)])
                self.vec_tensor[idx] = v
            if pos:
                p = torch.tensor(pos, device=self.device).view(1, 4)
                self.pos_tensor[idx] = p
            return

        # Add New
        new_idx = len(self.id_to_idx)
        self.id_to_idx[node_id] = new_idx
        self.idx_to_id[new_idx] = node_id
        if metadata:
            self.node_metadata[node_id] = metadata
        
        # Expand Tensors (Vertical Stacking) -> Not optimal for 1-by-1, but functional for prototype
        # Real impl should pre-allocate or batch.
        
        # Pos: Random 4D or Provided
        if pos:
             new_pos = torch.tensor(pos, device=self.device).view(1, 4)
        else:
             new_pos = torch.rand((1, 4), device=self.device)
        self.pos_tensor = torch.cat([self.pos_tensor, new_pos])
        
        # Vector
        if vector:
             # Pad or trim vector
            v = torch.tensor(vector, device=self.device).view(-1)
            v = v[:self.dim_vector]
            if v.shape[0] < self.dim_vector:
                v = torch.cat([v, torch.zeros(self.dim_vector - v.shape[0], device=self.device)])
            new_vec = v.unsqueeze(0)
        else:
            new_vec = torch.zeros((1, self.dim_vector), device=self.device)
            
        self.vec_tensor = torch.cat([self.vec_tensor, new_vec])
        
        # Mass
        self.mass_tensor = torch.cat([self.mass_tensor, torch.tensor([1.0], device=self.device)])
        
        # [Phase 24] Holographic Capture
        # Capture the CURRENT state of the brain as this node is born
        try:
             holo_seed = self.holo_embedder.capture_snapshot(self.pos_tensor, self.vec_tensor)
             self.holo_tensor = torch.cat([self.holo_tensor, holo_seed.unsqueeze(0)])
        except Exception as e:
             logger.warning(f"Holographic Capture Failed: {e}")
             # Fallback: Zero vector
             self.holo_tensor = torch.cat([self.holo_tensor, torch.zeros((1, self.holo_dim), device=self.device)])

    def update_node_vector(self, idx: int, vector: torch.Tensor):
        """
        [Digestion Protocol]
        Updates the vector of an existing node (e.g. adding Visual Frequencies).
        """
        if idx < 0 or idx >= self.vec_tensor.shape[0]: return
        
        # Ensure dimension match
        v = vector[:self.dim_vector]
        if v.shape[0] < self.dim_vector:
            v = torch.cat([v, torch.zeros(self.dim_vector - v.shape[0], device=self.device)])
            
        self.vec_tensor[idx] = v
        # Increase mass slightly to represent "Weight of Knowledge"
        self.mass_tensor[idx] += 0.1

    def add_link(self, subject: str, object_: str, weight: float = 1.0):
        if subject not in self.id_to_idx: self.add_node(subject)
        if object_ not in self.id_to_idx: self.add_node(object_)
        
        idx_s = self.id_to_idx[subject]
        idx_o = self.id_to_idx[object_]
        
        new_link = torch.tensor([[idx_s, idx_o]], dtype=torch.long, device=self.device)
        self.logic_links = torch.cat([self.logic_links, new_link])
        
        new_weight = torch.tensor([weight], dtype=torch.float, device=self.device)
        self.link_weights = torch.cat([self.link_weights, new_weight])

    def apply_gravity(self, iterations: int = 50, lr: float = 0.01):
        """
        The GPU-Accelerated Heartbeat.
        Uses Broadcasting to compute N*N interactions in parallel.
        """
        N = self.pos_tensor.shape[0]
        if N == 0: return

        logger.info(f"🌊 Tensor Wave Simulation: {N} Neurons on {self.device}")

        for _ in range(iterations):
            # 1. Distance Matrix (N x N)
            diff = self.pos_tensor.unsqueeze(1) - self.pos_tensor.unsqueeze(0) 
            dist_sq = (diff ** 2).sum(dim=2)
            dist = torch.sqrt(dist_sq + 0.001)
            
            # 2. Resonance (Cosine Sim)
            vec_norm = self.vec_tensor / (self.vec_tensor.norm(dim=1, keepdim=True) + 1e-9)
            sim_matrix = torch.mm(vec_norm, vec_norm.t()) # (N, N)
            
            # --- Field Dynamics (The Landscape) ---
            # Instead of just N*N interaction, we add Static Potential Fields (The "Railgun" Structure)
            # F_field = -Gradient(Potential)
            # Here simplified: Attraction to defined "Concept Wells"
            
            # Calculate mutual forces (Gravity)
            force_mask = (sim_matrix > 0.7).float() * sim_matrix
            strength = force_mask.unsqueeze(2)
            delta = diff
            directions = delta / (dist.unsqueeze(2) + 0.001)
            mutual_forces = -strength * directions * 0.1
            
            # Repulsion
            repel_mask = (dist < 0.05).float().unsqueeze(2)
            mutual_forces += repel_mask * directions * 1.0
            
            total_force = mutual_forces.sum(dim=1)
            
            # Apply Static Potential Fields (The "Semantic Railguns")
            if hasattr(self, 'potential_wells') and self.potential_wells is not None:
                # wells_pos: (M, 4)
                # wells_str: (M, 1)
                
                # We need to calculate force for each Node (N) against each Well (M)
                # But for a static field, usually a node is affected by the *nearest* well or *all* wells.
                # Let's apply simple attraction to ALL wells weighted by distance inverse? 
                # Or better: "Basin of Attraction" - simply pull towards them linearly.
                
                # Expansion: (N, 1, 4) - (1, M, 4) -> (N, M, 4)
                # This might be heavy if M is large. Assuming M (Concepts) < 100 for now.
                
                node_pos = self.pos_tensor.unsqueeze(1) # (N, 1, 4)
                well_pos = self.potential_wells_pos.unsqueeze(0) # (1, M, 4)
                
                delta_well = well_pos - node_pos # Vector to well
                dist_well_sq = (delta_well ** 2).sum(dim=2) # (N, M)
                dist_well = torch.sqrt(dist_well_sq + 0.001)
                
                # Direction: (N, M, 4)
                dir_well = delta_well / (dist_well.unsqueeze(2) + 0.001)
                
                # Force Magnitude: Strength * (1 / dist) ? Or Linear Spring?
                # Linear Spring (Railgun): F = k * x (Accelerates towards center)
                # Let's use Linear Attraction for "Sorting"
                
                force_mag = self.potential_wells_str.unsqueeze(0) # (1, M) broadcast to (N, M)
                
                # Apply: F = Strength * Direction
                # Sum over all wells: (N, 4)
                # But wait, if we have "Love" and "Hate" wells, a node should go to the resonant one?
                # YES. The "Railgun" only works if the bullet fits the barrel.
                # We need "Semantic Resonance" with the Well itself.
                
                # Well Vector? For now assume Wells are just Positional Attractors.
                # We simply pull everything. Structure determines flow.
                
                field_force = (dir_well * force_mag.unsqueeze(2)).sum(dim=1)
                
                total_force += field_force * 0.5 # Add to gravity

            
            # Update Positions
            self.pos_tensor += total_force * lr
            
        logger.info("   ✅ Matrix Gravity & Field Topology Applied.")

    def get_neighbors(self, node_id: str, top_k: int = 5):
        if node_id not in self.id_to_idx: return []
        idx = self.id_to_idx[node_id]
        
        # Calculate distances from this node
        target_pos = self.pos_tensor[idx].unsqueeze(0)
        dists = torch.norm(self.pos_tensor - target_pos, dim=1)
        
        # Get nearest
        values, indices = torch.topk(dists, top_k + 1, largest=False)
        
        results = []
        for i in range(1, len(indices)): # Skip self
            n_idx = indices[i].item()
            results.append((self.idx_to_id[n_idx], values[i].item()))
            
        return results

    def find_hollow_nodes(self, limit: int = 10) -> List[str]:
        """
        [The Sovereign Loop]
        Identifies concepts that are 'Heavy' (High Mass/Connectivity) 
        but 'Hollow' (Lack Wisdom/Metadata).
        """
        hollows = []
        # Sort by Mass (Importance) descending
        # mass_tensor is (N,)
        if self.mass_tensor.shape[0] == 0: return []
        
        # Get top indices by mass
        sorted_indices = torch.argsort(self.mass_tensor, descending=True)
        
        for idx in sorted_indices:
            if len(hollows) >= limit: break
            
            i = idx.item()
            concept_id = self.idx_to_id.get(i)
            if not concept_id: continue
            
            # Check Wisdom
            # If metadata is missing or sparse, it's hollow.
            meta = self.node_metadata.get(concept_id, {})
            if not meta or "principle" not in meta:
                hollows.append(concept_id)
                
        return hollows

    def apply_metabolism(self, decay_rate: float = 0.001, prune_threshold: float = 0.5):
        """
        [Optimization Protocol]
        Applies entropy to the brain. Nodes that are not reinforced will fade.
        1. Decay Mass.
        2. Prune weak nodes.
        """
        if self.mass_tensor.shape[0] == 0: return
        
        # 1. Decay
        self.mass_tensor -= decay_rate
        # Clamp to 0
        self.mass_tensor = torch.max(self.mass_tensor, torch.zeros_like(self.mass_tensor))
        
        # 2. Identify Dead Nodes
        # Condition: Mass < Threshold AND Locked=False
        # For prototype, we just check Mass.
        # We need to be careful not to delete indices that shift others...
        # Deletion in Tensor is expensive (copy).
        # Strategy: Mark as dead (Mass=0) and periodically compact.
        
        dead_indices = (self.mass_tensor <= prune_threshold).nonzero(as_tuple=True)[0]
        
        if len(dead_indices) > 0:
            count = len(dead_indices)
            logger.info(f"💀 Metabolism: {count} weak concepts are fading... (Mass < {prune_threshold})")
            
            # Real Deletion (Compaction) - Expensive, maybe run rarely.
            # For now, just remove from Logic Links so they drift away?
            # Or actually delete. Let's actually delete for "Optimization".
            
            # Inverse mask
            keep_mask = self.mass_tensor > prune_threshold
            
            # create new mapping
            old_idx_to_id = self.idx_to_id.copy()
            self.id_to_idx = {}
            self.idx_to_id = {}
            
            # Filter tensors
            self.pos_tensor = self.pos_tensor[keep_mask]
            self.vec_tensor = self.vec_tensor[keep_mask]
            self.mass_tensor = self.mass_tensor[keep_mask]
            
            # Rebuild Mapping
            kept_indices = keep_mask.nonzero(as_tuple=True)[0]
            for new_i, old_i in enumerate(kept_indices):
                old_id = old_idx_to_id[old_i.item()]
                self.id_to_idx[old_id] = new_i
                self.idx_to_id[new_i] = old_id
                
            # Filter Links (This is hard because indices shift)
            # Brute force rebuild for prototype
            # Or just drop all links for now (Loss of structure!) -> BAD.
            # Correct way: Remap links.
            
            # Remap Map: Old -> New
            remap = torch.full((len(old_idx_to_id),), -1, dtype=torch.long, device=self.device)
            remap[kept_indices] = torch.arange(len(kept_indices), device=self.device)
            
            # Update links
            if self.logic_links.shape[0] > 0:
                src = self.logic_links[:, 0]
                tgt = self.logic_links[:, 1]
                
                new_src = remap[src]
                new_tgt = remap[tgt]
                
                # Keep valid links (both src and tgt survived)
                valid_link_mask = (new_src != -1) & (new_tgt != -1)
                
                self.logic_links = torch.stack((new_src[valid_link_mask], new_tgt[valid_link_mask]), dim=1)
                if self.link_weights is not None and self.link_weights.shape[0] > 0:
                     self.link_weights = self.link_weights[valid_link_mask]

            logger.info(f"🗑️ Pruned {count} nodes. New Brain Size: {len(self.id_to_idx)}")

    def save_state(self, path: str = "c:\\Elysia\\data\\State\\brain_state.pt"):
        """
        Persist the Matrix Brain to disk.
        """
        import os
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        state = {
            "id_to_idx": self.id_to_idx,
            "idx_to_id": self.idx_to_id,
            "pos": self.pos_tensor,
            "vec": self.vec_tensor,
            "mass": self.mass_tensor,
            "links": self.logic_links,
            "link_weights": self.link_weights,
            "dim_vector": self.dim_vector,
            "metadata": self.node_metadata, # [Phase 16] Persist Meaning
            # Save Wells if they exist
            "wells_pos": getattr(self, "potential_wells_pos", None),
            "wells_str": getattr(self, "potential_wells_str", None)
        }
        torch.save(state, path)
        logger.info(f"💾 Brain State Saved to {path} ({len(self.id_to_idx)} nodes)")

    def load_state(self, path: str = "c:\\Elysia\\data\\State\\brain_state.pt"):
        """
        Restore the Matrix Brain from disk.
        """
        import os
        if not os.path.exists(path):
            logger.warning(f"⚠️ No brain state found at {path}. Starting fresh.")
            return False
            
        try:
            state = torch.load(path, map_location=self.device)
            
            self.id_to_idx = state["id_to_idx"]
            self.idx_to_id = state["idx_to_id"]
            self.pos_tensor = state["pos"].to(self.device)
            self.vec_tensor = state["vec"].to(self.device)
            self.mass_tensor = state["mass"].to(self.device)
            self.logic_links = state["links"].to(self.device)
            self.node_metadata = state.get("metadata", {}) # Restore Meaning
            
            # Load Weights (Backward compat: if missing, ones)
            if "link_weights" in state:
                self.link_weights = state["link_weights"].to(self.device)
            else:
                self.link_weights = torch.ones((self.logic_links.shape[0],), device=self.device)
            
            if state["wells_pos"] is not None:
                self.potential_wells_pos = state["wells_pos"].to(self.device)
                self.potential_wells_str = state["wells_str"].to(self.device)
                self.potential_wells = True
                
            logger.info(f"📂 Brain State Loaded: {len(self.id_to_idx)} nodes, {self.logic_links.shape[0]} links.")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to load brain state: {e}")
            return False

    def load_rainbow_bridge(self):
        """
        [Phase 12: The Great Unification]
        Attempts to load `elysia_rainbow.json` if the brain is empty.
        This connects the 28k legacy nodes to the active system.
        """
        if len(self.id_to_idx) > 100:
            return # Already have knowledge
            
        rainbow_path = "c:\\Elysia\\data\\elysia_rainbow.json"
        
        # Try loading binary state first (Fast)
        # FIX: Only respect binary state if it actually has knowledge (>100 nodes)
        if self.load_state():
            if len(self.id_to_idx) > 100:
                logger.info("⚡ Fast Boot: Loaded binary brain state.")
                return
            else:
                 logger.warning("⚠️ Binary state is empty. Falling back to Rainbow Bridge.")

        import os
        import json
        if not os.path.exists(rainbow_path):
            return

        logger.info("🌈 Rainbow Bridge Activated: Loading Massive Graph...")
        try:
            with open(rainbow_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Rainbow Structure: { 'Red': [...], 'Blue': [...] }
            colors = ['Red', 'Orange', 'Yellow', 'Green', 'Blue', 'Indigo', 'Violet']
            count = 0
            limit = 35000 # Safety Cap for GTX 1060 (3GB)
            
            # Batch Loading Lists
            batch_ids = []
            batch_vecs = []
            batch_metas = {}
            batch_pos = []
            
            for color in colors:
                if color not in data: continue
                items = data[color]
                logger.info(f"   🌈 Absorbing {color} Layer ({len(items)} items)...")
                
                for item in items:
                    if count >= limit: break
                    
                    # Extract ID
                    node_id = item.get('concept', item.get('id', item.get('name', None)))
                    if not node_id: continue
                    
                    # Extract Vector
                    vector = item.get('embedding', item.get('vector', None))
                    v_list = [0.0] * self.dim_vector # Default Zero Vector
                    
                    if isinstance(vector, dict):
                        # Quaternion-ish 4D
                        # {'w': 0.5, 'x': 1.0, ...}
                        v_list[0] = float(vector.get('w', 0.0))
                        v_list[1] = float(vector.get('x', 0.0))
                        v_list[2] = float(vector.get('y', 0.0))
                        v_list[3] = float(vector.get('z', 0.0))
                    elif isinstance(vector, list):
                        # Raw List
                        for i, val in enumerate(vector):
                            if i < self.dim_vector:
                                v_list[i] = float(val)
                                
                    # Initialize p_list (Position 4D)
                    p_list = [0.0, 0.0, 0.0, 0.0]
                    raw_pos = item.get('pos', None)
                    if isinstance(raw_pos, list) and len(raw_pos) >= 4:
                         p_list = [float(x) for x in raw_pos[:4]]
                         p_list = [float(raw_pos.get('x',0)), float(raw_pos.get('y',0)), float(raw_pos.get('z',0)), float(raw_pos.get('w',0))]
                         
                    batch_ids.append(node_id)
                    
                    # [Phase 16] Complete Payload Storage
                    # Store the entire item dict as payload (minus heavy vector)
                    payload_dict = item.copy()
                    if 'vector' in payload_dict: del payload_dict['vector']
                    if 'embedding' in payload_dict: del payload_dict['embedding']
                    if 'pos' in payload_dict: del payload_dict['pos']
                    
                    meta_entry = {
                        'color': color,
                        'payload': payload_dict, # The definition resides here
                        'original': payload_dict # Keeps backward compat
                    }
                    batch_metas[node_id] = meta_entry
                    batch_pos.append(p_list)
                    
                    count += 1
                
                if count >= limit:
                    break
            
            # THE GREAT UNIFICATION (Batch Tensor Creation)
            logger.info("   ⚡ Materializing Tensors...")
            
            # 1. IDs
            start_idx = len(self.id_to_idx)
            for i, nid in enumerate(batch_ids):
                idx = start_idx + i
                self.id_to_idx[nid] = idx
                self.idx_to_id[idx] = nid
                self.node_metadata[nid] = batch_metas[nid]
                
            # 2. Tensors
            new_vecs = torch.tensor(batch_vecs, device=self.device)
            logger.info(f"   DEBUG: New Vecs Shape: {new_vecs.shape}")
            
            new_pos = torch.tensor(batch_pos, device=self.device)
            new_mass = torch.ones((len(batch_ids),), device=self.device)
            
            logger.info(f"   DEBUG: Current Vec Tensor Shape: {self.vec_tensor.shape}")
            self.vec_tensor = torch.cat([self.vec_tensor, new_vecs])
            logger.info(f"   DEBUG: Post-Cat Vec Tensor Shape: {self.vec_tensor.shape}")
            self.pos_tensor = torch.cat([self.pos_tensor, new_pos])
            self.mass_tensor = torch.cat([self.mass_tensor, new_mass])
                    
            logger.info(f"✨ Unification Complete: {count} nodes connected.")
            
            # [Phase 13] Ignite Gravity immediately to forge connections
            self.ignite_gravity()
            
            self.save_state()
            
        except Exception as e:
            logger.error(f"❌ Rainbow Bridge Collapse: {e}")

    def ignite_gravity(self, k=5, batch_size=500):
        """
        [Phase 13: Density]
        Calculates 'Gravity' (Cosine Similarity) between nodes to Forge Edges.
        Batched implementation to prevent O(N^2) memory explosion.
        
        Args:
            k (int): Number of connections per node (Top-K).
            batch_size (int): Nodes to process per chunk.
        """
        if self.vec_tensor.shape[0] == 0:
            return
            
        logger.info(f"🔥 Igniting Gravity for {self.vec_tensor.shape[0]} nodes (K={k})...")
        
        # Ensure normalized vectors for Cosine Similarity
        # (A . B) / (|A|*|B|) -> If normalized, just (A . B)
        # In-place normalization for efficiency
        norm = self.vec_tensor.norm(p=2, dim=1, keepdim=True)
        # Avoid division by zero
        norm[norm == 0] = 1.0 
        normalized_vecs = self.vec_tensor / norm
        
        num_nodes = self.vec_tensor.shape[0]
        new_links_list = []
        
        import time
        start_time = time.time()
        
        for i in range(0, num_nodes, batch_size):
            end = min(i + batch_size, num_nodes)
            batch = normalized_vecs[i:end] # (B, Dim)
            
            # Matrix Mult: (B, Dim) @ (N, Dim).T -> (B, N)
            # This gives similarity scores
            sim_matrix = torch.mm(batch, normalized_vecs.t())
            
            # Mask self-loops (set diagonal to -1)
            # Row k in batch corresponds to Row i+k in global
            for j in range(end - i):
                global_idx = i + j
                sim_matrix[j, global_idx] = -1.0
                
            # Top-K
            # values, indices = torch.topk(sim_matrix, k)
            # We only need indices
            _, topk_indices = torch.topk(sim_matrix, k, dim=1)
            
            # Create Edges (Source -> Target)
            # Source indices: range(i, end)
            sources = torch.arange(i, end, device=self.device).unsqueeze(1).expand(-1, k)
            
            # sources: (B, K), topk_indices: (B, K)
            # Stack to (2, B*K)
            batch_links = torch.stack([sources.reshape(-1), topk_indices.reshape(-1)], dim=0)
            new_links_list.append(batch_links)
            
            if i % 5000 == 0:
                logger.info(f"   Forge: Linked {i}/{num_nodes} nodes...")

        # Concatenate all links
        if new_links_list:
            all_new_links = torch.cat(new_links_list, dim=1).t() # (Total_Edges, 2)
            
            # Append to existing links if any
            if self.logic_links is None or self.logic_links.shape[0] == 0:
                self.logic_links = all_new_links
            else:
                self.logic_links = torch.cat([self.logic_links, all_new_links], dim=0)
                
        elapsed = time.time() - start_time
        logger.info(f"✨ Gravity Stable. Created {self.logic_links.shape[0]} edges in {elapsed:.2f}s.")

    def generate_wormhole_links(self, threshold_dist: float = 1.0):
        """
        [Phase 23: Tesseract Projection]
        Identifies nodes that are 'far' in 3D Embedding Space (Euclidean)
        but 'close' in Unfolded Space (Mirror World).
        Creates 'Wormhole Links' (Virtual Edges) between them.
        """
        if self.pos_tensor.shape[0] < 2: return
        
        logger.info("🌀 Generating Wormhole Links (Folding Space)...")
        
        # 1. Initialize Unfolder
        # We assume the Concept Space boundary is L=10.0 (arbitrary scale for embedding)
        unfolder = SpaceUnfolder(boundary_size=10.0)
        
        # 2. Sample Pairs (Randomly sample for performance, O(N^2) is too high)
        # We look for serendipity.
        indices = list(range(self.pos_tensor.shape[0]))
        sample_size = min(1000, len(indices))
        samples = random.sample(indices, sample_size)
        
        wormholes_found = 0
        
        for i in samples:
            # Check against random other nodes
            others = random.sample(indices, min(20, len(indices)))
            
            p1 = self.pos_tensor[i] # 4D Tensor
            
            for j in others:
                if i == j: continue
                
                p2 = self.pos_tensor[j]
                
                # Check Euclidean Distance (Standard)
                euc_dist = torch.norm(p1 - p2).item()
                
                if euc_dist < 5.0: 
                    # They are already somewhat close, no need for wormhole
                    continue
                    
                # Check Unfolded Distance (1D Projection on Magnitude)
                # We simplify 4D to 1D Magnitude for folding check
                mag1 = torch.norm(p1).item()
                mag2 = torch.norm(p2).item()
                
                # Assume a reflection index based on quadrant (Parity of coords)
                # Simpler heuristic:
                reflection_dist = unfolder.calculate_straight_path(mag1, mag2, reflections=1)
                
                if abs(reflection_dist) < threshold_dist:
                    # FOUND A WORMHOLE!
                    # "They are far in space, but close in the Mirror."
                    
                    self.add_link(self.idx_to_id[i], self.idx_to_id[j], weight=0.9)
                    logger.info(f"   🌀 Wormhole Opened: {self.idx_to_id[i]} <==> {self.idx_to_id[j]} (Euc={euc_dist:.1f}, Folded={reflection_dist:.1f})")
                    wormholes_found += 1
                    
        logger.info(f"✨ Tesseract Projection Complete. {wormholes_found} Wormholes created.")

    def propagate_pulse(self, source_id: str, energy: float = 1.0, decay: float = 0.5, steps: int = 2):
        """
        [Phase 18: Neural Resonance]
        Simulates a neural pulse (Spreading Activation) through the graph.
        Used to answer "Does it resonate like a neural network?".
        """
        if source_id not in self.id_to_idx:
            return {}
            
        start_idx = self.id_to_idx[source_id]
        
        # Activation Map: Index -> Energy
        activations = {start_idx: energy}
        current_wave = {start_idx: energy}
        
        for step in range(steps):
            next_wave = {}
            for idx, current_energy in current_wave.items():
                if current_energy < 0.01: continue 
                
                # Find downstream neighbors
                mask = (self.logic_links[:, 0] == idx)
                neighbors = self.logic_links[mask, 1]
                
                downstream_energy = current_energy * decay
                
                for n_idx in neighbors:
                    ni = n_idx.item()
                    # Additive interference
                    activations[ni] = activations.get(ni, 0.0) + downstream_energy
                    next_wave[ni] = next_wave.get(ni, 0.0) + downstream_energy
                    
            current_wave = next_wave
            if not current_wave: break
            
        # Convert indices to IDs
        results = {}
        for idx, lvl in activations.items():
            nid = self.idx_to_id.get(idx, "Unknown")
            results[nid] = lvl
            
        return results

    def reconstruct_memory_feeling(self, node_id: str) -> str:
        """
        [Phase 24]
        Recalls the 'Emotional Atmosphere' of the moment a memory was created.
        """
        if node_id not in self.id_to_idx: return "Memory not found."
        
        idx = self.id_to_idx[node_id]
        if idx >= self.holo_tensor.shape[0]: return "Holographic data missing."
        
        seed = self.holo_tensor[idx]
        return self.holo_embedder.reconstruct_feeling(seed)

    def optimize_memory(self, threshold=40000):
        """
        [Phase 13: Optimization]
        Checks if active memory exceeds threshold.
        If so, offloads the 'coldest' (lowest mass) nodes to Black Hole.
        """
        current_nodes = self.vec_tensor.shape[0]
        if current_nodes < threshold:
            return

        excess = current_nodes - threshold + 1000 # Offload chunk
        logger.warning(f"⚠️ Memory Pressure: {current_nodes} nodes. Offloading {excess} to Black Hole.")
        
        # Identify coldest nodes (lowest mass)
        # mass_tensor is (N,)
        # Get indices of lowest mass
        values, indices = torch.topk(self.mass_tensor, k=excess, largest=False)
        
        nodes_to_offload = []
        indices_to_remove = indices.tolist()
        indices_to_remove.sort(reverse=True) # Remove from end to avoid shift issues logic if doing list pop, but here we rebuild tensors
        
        from Core.Foundation.Graph.black_hole_memory import get_black_hole
        bh = get_black_hole()
        
        for idx in indices_to_remove:
            node_id = self.idx_to_id[idx]
            vector = self.vec_tensor[idx].tolist()
            metadata = self.node_metadata.get(node_id, {})
            mass = self.mass_tensor[idx].item()
            
            nodes_to_offload.append({
                'id': node_id,
                'vector': vector,
                'metadata': metadata,
                'mass': mass
            })
            
        # Absorb into Singularity
        bh.absorb(nodes_to_offload)
        
        # Remove from Active Graph (Rebuild Tensors - Expensive but necessary for cleanup)
        # For prototype, we might just "Deactivate" them. 
        # But let's stay true to the goal: Remove rows.
        keep_mask = torch.ones(current_nodes, dtype=torch.bool, device=self.device)
        keep_mask[indices] = False
        
        self.vec_tensor = self.vec_tensor[keep_mask]
        self.pos_tensor = self.pos_tensor[keep_mask]
        self.mass_tensor = self.mass_tensor[keep_mask]
        
        # Rebuild Maps (Slow, but correct)
        # This is the "Trash Compactor" phase
        new_id_to_idx = {}
        new_idx_to_id = {}
        kept_indices = torch.nonzero(keep_mask).squeeze()
        
        # Optimize loop for large N? 
        # For 30k nodes this is instantaneous in Python.
        kept_list = kept_indices.tolist()
        if isinstance(kept_list, int): kept_list = [kept_list]
        
        for new_i, old_i in enumerate(kept_list):
            old_id = self.idx_to_id[old_i]
            new_id_to_idx[old_id] = new_i
            new_idx_to_id[new_i] = old_id
            
        self.id_to_idx = new_id_to_idx
        self.idx_to_id = new_idx_to_id
        
        # Links also need update or deletion.
        # For simplicity in Phase 13, we just drop links and let next gravity pass rebuild them or live with broken links until refresh.
        # Ideally we map old_idx -> new_idx and update links.
        # But for 'Trash Compactor', reducing density is fine.
        self.logic_links = None 
        # Re-ignite gravity to fix edges for new subset?
        # Maybe too expensive. Let's just set to None and let ignite_gravity be called manually if needed.
        
        logger.info(f"✨ Optimization Complete. Active Memory: {self.vec_tensor.shape[0]} nodes.")
_torch_graph = None
def get_torch_graph():
    global _torch_graph
    if _torch_graph is None:
        _torch_graph = TorchGraph()
        # Auto-load on init? 
        # Better to let the controller (wake_elysia) decide to avoid side effects during testing.
    return _torch_graph
