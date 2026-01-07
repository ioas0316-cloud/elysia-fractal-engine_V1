import sys
import os
import json
import random

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Foundation.Mind.tensor import HyperQuaternion

def migrate():
    memory_file = "saves/hippocampus.json"
    if not os.path.exists(memory_file):
        print("No memory file found.")
        return

    with open(memory_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    nodes = []
    if "graph" in data:
        nodes = data["graph"]["nodes"]
    elif "nodes" in data:
        nodes = data["nodes"]
    
    updated_count = 0
    for node in nodes:
        tensor_data = node.get("tensor", {})
        
        # Check if it's already 4D
        if "w" not in tensor_data:
            # Upgrade 3D to 4D
            # Preserve existing x,y,z if they exist, otherwise random
            if "x" in tensor_data:
                # Existing 3D tensor -> Add W=1.0 (Line)
                node["tensor"] = {
                    "w": 1.0 + random.uniform(-0.2, 0.2),
                    "x": tensor_data["x"],
                    "y": tensor_data["y"],
                    "z": tensor_data["z"]
                }
            else:
                # No tensor -> Full Random 4D
                node["tensor"] = HyperQuaternion.random().to_dict()
            
            updated_count += 1
            
    print(f"Migrated {updated_count} nodes to 4D Hyper-Quaternion space.")
    
    with open(memory_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    migrate()
