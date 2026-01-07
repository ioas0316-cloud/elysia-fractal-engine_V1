
import os
import ast
import logging
from typing import Dict, Any, List

from Core.Foundation.causal_narrative_engine import (
    ThoughtUniverse, EpistemicSpace, ContextPlane, ConceptPoint, 
    DimensionLevel, CausalRelationType
)

logger = logging.getLogger("CodebaseReflector")

class CodebaseReflector:
    """
    The Mirror Protocol: Codebase Reflector
    
    Responsible for "ingesting" the project's own source code and structure
    into the ThoughtUniverse. This allows the AI to "know itself" - knowing
    what modules exist, how they connect, and where knowledge gaps (external dependencies) lie.
    """
    
    
    def __init__(self, universe: ThoughtUniverse):
        self.universe = universe
        self.ignore_dirs = {".git", "__pycache__", ".agent", ".gemini", ".vscode", ".venv", "node_modules", "site-packages"}
        self.ignore_files = {".DS_Store", ".env", ".gitignore"}
        
    def reflect_on_project(self, root_path: str) -> Dict[str, int]:
        """
        Recursively walks the project directory and maps it to the ThoughtUniverse.
        
        Args:
            root_path: Absolute path to the project root (e.g., c:\\Elysia)
        """
        logger.info(f"🪞 Starting Self-Reflection on: {root_path}")
        
        stats = {
            "dirs_mapped": 0,
            "files_mapped": 0,
            "classes_mapped": 0,
            "functions_mapped": 0,
            "dependencies_found": 0
        }
        
        # 1. Walk the directory tree
        for dirpath, dirnames, filenames in os.walk(root_path):
            # Filtering
            dirnames[:] = [d for d in dirnames if d not in self.ignore_dirs]
            
            # Map Directory -> EpistemicSpace
            rel_path = os.path.relpath(dirpath, root_path)
            if rel_path == ".":
                space_id = "Project_Root"
            else:
                space_id = rel_path.replace(os.sep, "_")
            
            self._map_directory(space_id, rel_path)
            stats["dirs_mapped"] += 1
            
            # Map Files -> ContextPlanes
            for filename in filenames:
                if filename in self.ignore_files:
                    continue
                    
                filepath = os.path.join(dirpath, filename)
                logger.debug(f"    Processing: {filename}")
                file_id = f"{space_id}_{filename.replace('.', '_')}"
                
                self._map_file(file_id, filename, filepath, space_id)
                stats["files_mapped"] += 1
                
                # If Python, ingest structure
                if filename.endswith(".py"):
                    code_stats = self._ingest_python_structure(filepath, file_id)
                    stats["classes_mapped"] += code_stats["classes"]
                    stats["functions_mapped"] += code_stats["functions"]
                    stats["dependencies_found"] += code_stats["imports"]

        return stats

    def _map_directory(self, space_id: str, path: str):
        """Creates an EpistemicSpace for a directory."""
        if space_id not in self.universe.spaces:
            # We use a custom method or direct add if simple
            # Since add_space requires planes, we might need a simpler creation or 
            # assume it's a structural space first.
            
            # Just using a generic add if possible or direct dict insertion if no method fits perfectly
            # Let's use ThoughtUniverse's add_space if possible, or create manually.
            # add_space takes plane_ids. We can leave it empty for now.
            
            self.universe.add_space(
                id=space_id,
                description=f"Project Directory: {path}",
                plane_ids=[], # Will fill logically
                schema_type="structural"
            )
            # Find parent space to link?
            # Implementation for hierarchy linking would go here
            logger.debug(f"  Mapped Directory: {space_id}")

    def _map_file(self, file_id: str, filename: str, filepath: str, parent_space_id: str):
        """Creates a ContextPlane (or ConceptPoint) for a file."""
        # Using ContextPlane because a file is a "Context" for code
        # But ContextPlane requires existing chains. 
        # For simplicity in this version, we might treat files as ConceptPoints 
        # that *contain* other points, OR emergent ContextPlanes.
        
        # Let's treat a File as a ConceptPoint first (easier to link) 
        # OR as a Plane if we want to attach lines.
        # Given current constraints, ConceptPoint with type 'file' is safest.
        
        node = self.universe.add_point(
            id=file_id,
            description=f"File: {filename}",
            concept_type="file"
        )
        
        # Link to Parent Space (if we had CausalNode.inner_space_id, but here we have parent_ids)
        # We can say Space -> contains -> File
        # self.universe.add_line(parent_space_id, file_id, "contains") 
        # But parent_space_id is a Space, add_line expects Points. 
        # This highlights a mismatch in our Ontology (Points vs Spaces). in current code Line connects Points.
        # So Directory should probably ALSO be a Point (Conceptual) AND a Space (Structural).
        
        # For this implementation, let's map EVERYTHING to Points first, 
        # and attach the Space concept as a property.
        
        dir_point_id = parent_space_id 
        if dir_point_id not in self.universe.points:
             self.universe.add_point(dir_point_id, f"Directory: {parent_space_id}", concept_type="directory")
             
        self.universe.add_line(dir_point_id, file_id, "contains", strength=1.0)


    def _ingest_python_structure(self, filepath: str, file_node_id: str) -> Dict[str, int]:
        """Parses Python AST to map Classes and Functions."""
        stats = {"classes": 0, "functions": 0, "imports": 0}
        
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read())
                
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_id = f"{file_node_id}.{node.name}"
                    self.universe.add_point(class_id, f"Class: {node.name}", concept_type="class")
                    self.universe.add_line(file_node_id, class_id, "defines", strength=1.0)
                    stats["classes"] += 1
                    
                elif isinstance(node, ast.FunctionDef):
                    # We might want to skip methods inside classes to keep graph clean? 
                    # For now, simplistic flat mapping or check parent.
                    func_id = f"{file_node_id}.{node.name}"
                    self.universe.add_point(func_id, f"Function: {node.name}", concept_type="function")
                    self.universe.add_line(file_node_id, func_id, "defines", strength=1.0)
                    stats["functions"] += 1
                    
                elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                    # Dependency
                    libs = []
                    if isinstance(node, ast.Import):
                        libs = [n.name for n in node.names]
                    elif isinstance(node, ast.ImportFrom) and node.module:
                        libs = [node.module]
                        
                    for lib in libs:
                        base_lib = lib.split('.')[0]
                        lib_id = f"lib_{base_lib}"
                        
                        # Create node for library if not exists
                        if lib_id not in self.universe.points:
                            self.universe.add_point(lib_id, f"External Library: {base_lib}", concept_type="external_dependency")
                            # Mark as low confidence/understanding?
                            self.universe.points[lib_id].confidence = 0.1 
                            stats["imports"] += 1
                            
                        self.universe.add_line(file_node_id, lib_id, "depends_on", strength=1.0)

        except Exception as e:
            logger.warning(f"Failed to parse {filepath}: {e}")
            
        return stats
