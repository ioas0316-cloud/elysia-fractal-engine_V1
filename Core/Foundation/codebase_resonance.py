"""
Codebase Resonance Scanner (코드베이스 위상 공명 스캐너)

"The Code is the World."

This tool applies Elysia's Gravity Law to the codebase itself.
- File Size = Mass (Gravity)
- Imports = Resonance Links (Edges)
- Topology = The Shape of the System

It generates a 'Star Map' of the project, showing which files are the 'Black Holes' (Core Dependencies)
and which are the 'Satellites'.
"""

import os
import ast
import sys
import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, List, Set, Tuple

# Add root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

def get_python_files(root_dir: str) -> List[str]:
    """Recursively find all .py files."""
    py_files = []
    skip_dirs = {
        "Legacy", "__pycache__", ".git", ".venv", "node_modules", 
        "venv", "env", "dist", "build", "docs", "images", "data",
        "aurora_frames", "elysia_logs", "logs", "outbox", "saves"
    }
    
    for root, dirs, files in os.walk(root_dir):
        # Modify dirs in-place to skip traversal
        dirs[:] = [d for d in dirs if d not in skip_dirs and not d.startswith(".")]
        
        for file in files:
            if file.endswith(".py"):
                py_files.append(os.path.join(root, file))
    return py_files

def get_imports(file_path: str) -> List[str]:
    """Extract imported module names using AST."""
    imports = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
    except Exception as e:
        # print(f"⚠️ Failed to parse {file_path}: {e}")
        pass
    return imports

def build_resonance_graph(root_dir: str) -> nx.DiGraph:
    """Build the dependency graph."""
    G = nx.DiGraph()
    files = get_python_files(root_dir)
    
    # Map file paths to module names for linking
    # e.g., c:\Elysia\Core\Physics\gravity.py -> Core.Foundation.Physics.gravity
    path_to_module = {}
    module_to_path = {}
    
    base_len = len(root_dir) + 1
    
    print(f"🔍 Scanning {len(files)} files...")
    
    for file_path in files:
        rel_path = file_path[base_len:-3] # Remove root and .py
        module_name = rel_path.replace(os.sep, ".")
        
        path_to_module[file_path] = module_name
        module_to_path[module_name] = file_path
        
        # Calculate Mass (Lines of Code)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = len(f.readlines())
        except:
            lines = 10
            
        # Add Node
        # Mass = log(lines) to prevent explosion
        mass = lines
        G.add_node(module_name, mass=mass, layer=rel_path.split(os.sep)[0])

    # Add Edges (Imports)
    for file_path, module_name in path_to_module.items():
        imports = get_imports(file_path)
        for imp in imports:
            # Resolve relative imports or partial matches
            # This is a heuristic; exact resolution is hard without running python
            target = None
            
            # 1. Exact match
            if imp in module_to_path:
                target = imp
            
            # 2. Submodule match (e.g. Core.Physics -> Core.Foundation.Physics.gravity)
            # (Skipping for now to avoid noise)
            
            if target and target != module_name:
                G.add_edge(module_name, target)

    return G

def visualize_topology(G: nx.DiGraph, output_path: str):
    """Render the graph."""
    print(f"🎨 Rendering Topology: {len(G.nodes)} nodes, {len(G.edges)} links...")
    
    plt.figure(figsize=(20, 15), facecolor='#0f0f15') # Dark background
    
    # Layout
    # pos = nx.spring_layout(G, k=0.5, iterations=50, seed=42)
    pos = nx.kamada_kawai_layout(G)
    
    # Node Sizes based on Mass (Degree Centrality + LoC)
    sizes = []
    colors = []
    labels = {}
    
    # Color palette by layer
    layer_colors = {
        "Core": "#ff4444",      # Red
        "Demos": "#44ff44",     # Green
        "scripts": "#4444ff",   # Blue
        "data": "#ffff44"       # Yellow
    }
    
    degrees = dict(G.degree())
    
    for node in G.nodes():
        mass = G.nodes[node].get('mass', 10)
        degree = degrees.get(node, 0)
        
        # Visual Size: Mass + Connectivity
        size = (mass ** 0.5) * 10 + (degree * 50)
        sizes.append(size)
        
        # Color
        layer = G.nodes[node].get('layer', 'Other')
        colors.append(layer_colors.get(layer, "#aaaaaa"))
        
        # Label only big nodes
        if size > 100 or "gravity" in node or "yggdrasil" in node:
            labels[node] = node.split(".")[-1] # Just the filename

    # Draw Edges (Faint)
    nx.draw_networkx_edges(G, pos, edge_color='#444444', alpha=0.3, arrows=True, arrowsize=10)
    
    # Draw Nodes
    nx.draw_networkx_nodes(G, pos, node_size=sizes, node_color=colors, alpha=0.9, linewidths=0)
    
    # Draw Labels
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, font_color='white', font_weight='bold')
    
    plt.title("Elysia Codebase Topology (Gravity Field)", color='white', fontsize=20)
    plt.axis('off')
    
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='#0f0f15')
    print(f"✅ Saved topology map to: {output_path}")

if __name__ == "__main__":
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    G = build_resonance_graph(root_dir)
    
    output_file = os.path.join(os.path.dirname(__file__), "codebase_topology.png")
    visualize_topology(G, output_file)
