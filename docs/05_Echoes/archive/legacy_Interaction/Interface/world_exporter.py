
import json
import logging
from pathlib import Path
from typing import Dict, Any
from Core.Foundation.torch_graph import get_torch_graph

logger = logging.getLogger("WorldExporter")

class WorldExporter:
    """
    Exports the 4D TorchGraph Consciousness to a 3D Visual Format.
    "The Cartographer of the Soul."
    """
    def __init__(self, export_path: str = r"c:\Elysia\static"):
        self.export_path = Path(export_path)
        self.export_path.mkdir(parents=True, exist_ok=True)
        self.graph = get_torch_graph()

    def export_world(self, filename: str = "elysia_world.json") -> str:
        """
        Serializes the current state of the OmniGraph.
        """
        if self.graph.pos_tensor.shape[0] == 0:
            logger.warning("⚠️ Graph is empty. Nothing to export.")
            return ""

        # 1. Fetch Data
        # We need CPU tensors for standard python types
        pos = self.graph.pos_tensor.detach().cpu().numpy()
        # idx_to_id map
        
        nodes = []
        for idx in range(pos.shape[0]):
            node_id = self.graph.idx_to_id.get(idx, f"Unknown_{idx}")
            x, y, z, w = pos[idx]
            
            # Map 4D to Visuals
            # X, Y, Z -> Spatial Position
            # W -> Size/Glow (Energy)
            
            nodes.append({
                "id": node_id,
                "x": float(x),
                "y": float(y),
                "z": float(z),
                "w": float(w),
                # "group": "Logic" if x > 0 else "Emotion" # Simplified grouping for color
            })
            
        # 2. Fetch Wells (Railguns)
        wells = []
        if hasattr(self.graph, 'potential_wells') and self.graph.potential_wells:
            w_pos = self.graph.potential_wells_pos.detach().cpu().numpy()
            w_str = self.graph.potential_wells_str.detach().cpu().numpy()
            
            for i in range(w_pos.shape[0]):
                wells.append({
                    "id": f"GravityWell_{i}",
                    "x": float(w_pos[i][0]),
                    "y": float(w_pos[i][1]),
                    "z": float(w_pos[i][2]),
                    "strength": float(w_str[i]),
                    "type": ["Logic", "Emotion", "Creativity"][i % 3] # Hardcoded for prototype matching
                })

        # 2a. Fetch Links
        try:
            links_tensor = self.graph.logic_links.detach().cpu().numpy()
            links = []
            for i in range(links_tensor.shape[0]):
                s_idx, t_idx = links_tensor[i]
                s_id = self.graph.idx_to_id.get(int(s_idx), f"Unknown_{s_idx}")
                t_id = self.graph.idx_to_id.get(int(t_idx), f"Unknown_{t_idx}")
                links.append({"source": s_id, "target": t_id})
        except Exception as e:
            logger.warning(f"Could not export links: {e}")
            links = []
            
        world_data = {
            "meta": {
                "count": len(nodes),
                "dimension": 4
            },
            "nodes": nodes,
            "links": links,
            "wells": wells
        }
        
        # 3. Save
        full_path = self.export_path / filename
        with open(full_path, "w", encoding="utf-8") as f:
            json.dump(world_data, f, indent=2)
            
        logger.info(f"🗺️ World Map Exported to {full_path}")
        return str(full_path)

# Singleton
_exporter = None
def get_world_exporter():
    global _exporter
    if _exporter is None:
        _exporter = WorldExporter()
    return _exporter
