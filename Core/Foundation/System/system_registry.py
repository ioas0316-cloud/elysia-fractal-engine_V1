"""
System Registry (시스템 등록소)
================================

"모든 시스템의 중앙 등록소. 다시는 같은 것을 두 번 만들지 않기 위해."
"Central registry of all systems. To never build the same thing twice."

This is the solution to the recurring problem:
- Systems exist but are undiscoverable
- Redundant implementations
- Lost connections

The SystemRegistry automatically discovers, catalogs, and provides
queryable access to ALL systems in the codebase.
"""

import os
import ast
import json
import inspect
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, asdict
from datetime import datetime
import logging

logger = logging.getLogger("SystemRegistry")

@dataclass
class SystemEntry:
    """Registered system information"""
    name: str
    path: str
    category: str  # voice, nervous, monitor, knowledge, api, etc.
    purpose: str
    status: str  # active, legacy, deprecated, new
    classes: List[str]
    functions: List[str]
    dependencies: List[str]

    connected_to: List[str]
    last_modified: str
    
    # Fractal Identity (Soul)
    fractal_identity: Optional[Dict[str, Any]] = None  # {principle, frequency, axioms}
    resonance_frequency: float = 0.5  # Default neutral frequency
    notes: str = ""

class SystemRegistry:
    """
    Central registry of all Elysia systems.
    
    Provides:
    - Automatic system discovery
    - Duplicate detection
    - Dependency mapping
    - Queryable system database
    
    Usage:
        >>> registry = SystemRegistry()
        >>> registry.scan_all_systems()
        >>> 
        >>> # Find all voice systems
        >>> voice_systems = registry.find_by_category("voice")
        >>> 
        >>> # Check for duplicates
        >>> duplicates = registry.find_duplicates()
        >>> 
        >>> # Get system info
        >>> info = registry.get_system("VoiceOfElysia")
    """
    
    def __init__(self, repo_root: Optional[Path] = None):
        if repo_root is None:
            # Auto-detect repo root
            current_file = Path(__file__).resolve()
            self.repo_root = current_file.parent.parent.parent
        else:
            self.repo_root = Path(repo_root)
        
        self.systems: Dict[str, SystemEntry] = {}
        self.categories: Dict[str, List[str]] = {}
        self.class_index: Dict[str, List[str]] = {}  # class_name -> [file paths]
        
        logger.info(f"📋 SystemRegistry initialized at {self.repo_root}")
    
    def scan_all_systems(self) -> Dict[str, int]:
        """
        Scan entire codebase and register all systems.
        
        Returns:
            Statistics of discovered systems
        """
        logger.info("🔍 Scanning all systems...")
        
        stats = {
            "files_scanned": 0,
            "systems_found": 0,
            "classes_found": 0,
            "duplicates_found": 0,
        }
        
        core_dir = self.repo_root / "Core"
        if not core_dir.exists():
            logger.error(f"Core directory not found: {core_dir}")
            return stats
        
        # Scan all Python files
        for py_file in core_dir.rglob("*.py"):
            if "__pycache__" in str(py_file):
                continue
            
            stats["files_scanned"] += 1
            entry = self._analyze_file(py_file)
            
            if entry:
                self.register_system(entry)
                stats["systems_found"] += 1
                stats["classes_found"] += len(entry.classes)
        
        # Build indices
        self._build_indices()
        
        # Detect duplicates
        duplicates = self.find_duplicates()
        stats["duplicates_found"] = len(duplicates)
        
        logger.info(f"✅ Scan complete: {stats}")
        return stats
    
    def _analyze_file(self, filepath: Path) -> Optional[SystemEntry]:
        """Analyze a Python file and extract system information"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AST
            tree = ast.parse(content)
            
            # Extract classes and functions
            classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
            functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            
            if not classes and not functions:
                return None
            
            # Determine category from path and content
            relpath = filepath.relative_to(self.repo_root)
            category = self._determine_category(filepath, content)
            
            # Extract purpose from docstring
            purpose = self._extract_purpose(tree, content)
            
            # Determine status
            status = self._determine_status(filepath)
            
            # Extract dependencies
            dependencies = self._extract_dependencies(tree)
            
            # Get last modified time
            last_modified = datetime.fromtimestamp(filepath.stat().st_mtime).isoformat()
            

            # Extract Fractal Identity
            fractal_identity = self._extract_fractal_identity(filepath, content)
            
            entry = SystemEntry(
                name=filepath.stem,
                path=str(relpath),
                category=category,
                purpose=purpose,
                status=status,
                classes=classes,
                functions=functions,
                dependencies=dependencies,
                connected_to=[],  # Will be determined later
                last_modified=last_modified,
                fractal_identity=fractal_identity,
                resonance_frequency=fractal_identity.get("frequency", 0.5) if fractal_identity else 0.5
            )
            
            return entry
            
        except Exception as e:
            logger.debug(f"Could not analyze {filepath}: {e}")
            return None
    
    def _determine_category(self, filepath: Path, content: str) -> str:
        """Determine system category from path and content"""
        path_str = str(filepath).lower()
        content_lower = content.lower()
        
        # Check keywords in order of specificity
        if "voice" in path_str or "voice" in content_lower:
            return "voice"
        elif "nervous" in path_str or "cns" in content_lower or "centralnervous" in content_lower:
            return "nervous"
        elif "monitor" in path_str or "monitoring" in content_lower:
            return "monitor"
        elif "knowledge" in path_str or "knowledgebase" in content_lower:
            return "knowledge"
        elif "api" in path_str or "endpoint" in content_lower:
            return "api"
        elif "bridge" in path_str or "integration" in path_str:
            return "bridge"
        elif "/expression/" in path_str:
            return "expression"
        elif "/intelligence/" in path_str:
            return "intelligence"
        elif "/foundation/" in path_str:
            return "foundation"
        elif "/memory/" in path_str:
            return "memory"
        elif "/interface/" in path_str:
            return "interface"
        else:
            return "other"
    
    def _extract_purpose(self, tree: ast.AST, content: str) -> str:
        """Extract purpose from module docstring"""
        docstring = ast.get_docstring(tree)
        if docstring:
            # Get first line or first paragraph
            lines = docstring.strip().split('\n')
            for line in lines:
                line = line.strip()
                if line and not line.startswith('=') and not line.startswith('-'):
                    return line[:200]  # Max 200 chars
        return "No description available"
    
    def _determine_status(self, filepath: Path) -> str:
        """Determine system status from path"""
        path_str = str(filepath).lower()
        
        if "legacy" in path_str:
            return "legacy"
        elif "deprecated" in path_str:
            return "deprecated"
        elif "test" in path_str:
            return "test"
        else:
            return "active"
    
    def _extract_dependencies(self, tree: ast.AST) -> List[str]:
        """Extract import dependencies"""
        deps = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    deps.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    deps.append(node.module)

        return list(set(deps))  # Unique
    
    def _extract_fractal_identity(self, filepath: Path, content: str) -> Optional[Dict[str, Any]]:
        """
        Extract Fractal Identity from module.
        
        Looks for:
        1. FRACTAL_IDENTITY = {...} constant
        2. Inferred from Docstring (Principle)
        3. Inferred from Category (Frequency)
        """
        identity = {
            "principle": "Unknown Logic",
            "frequency": 0.5,
            "axioms": []
        }
        
        # 1. Try to parse explicit FRACTAL_IDENTITY
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id == "FRACTAL_IDENTITY":
                            # Found it! basic manual extraction (safe evaluaton is hard with ast alone)
                            # For now, just mark it as found
                            identity["source"] = "EXPLICIT"
                            return identity 
        except:
            pass
            
        # 2. Infer from content
        path_str = str(filepath).lower()
        
        # Frequency Inference Map
        if "foundation" in path_str or "core" in path_str:
            identity["frequency"] = 0.9  # High frequency (Foundational)
            identity["principle"] = "Maintain System Integrity"
        elif "chaos" in path_str:
            identity["frequency"] = 0.2  # Low/Complex frequency
            identity["principle"] = "Generate Variation"
        elif "nova" in path_str or "logic" in path_str:
            identity["frequency"] = 0.8  # Ordered frequency
            identity["principle"] = "Ensure Logical Consistency"
        elif "personality" in path_str or "emotion" in path_str:
            identity["frequency"] = 0.6  # Warm frequency
            identity["principle"] = "Empathize and Express"
            
        return identity
    
    def _build_indices(self):
        """Build search indices"""
        # Category index
        self.categories = {}
        for name, entry in self.systems.items():
            if entry.category not in self.categories:
                self.categories[entry.category] = []
            self.categories[entry.category].append(name)
        
        # Class index
        self.class_index = {}
        for name, entry in self.systems.items():
            for cls in entry.classes:
                if cls not in self.class_index:
                    self.class_index[cls] = []
                self.class_index[cls].append(entry.path)
    
    def register_system(self, entry: SystemEntry):
        """Register a system entry"""
        self.systems[entry.name] = entry
        logger.debug(f"Registered: {entry.name} ({entry.category})")
    
    def get_system(self, name: str) -> Optional[SystemEntry]:
        """Get system by name"""
        return self.systems.get(name)
    
    def find_by_category(self, category: str) -> List[SystemEntry]:
        """Find all systems in a category"""
        return [self.systems[name] for name in self.categories.get(category, [])]
    
    def find_by_class(self, class_name: str) -> List[str]:
        """Find all files that define a class"""
        return self.class_index.get(class_name, [])
    
    def find_duplicates(self) -> Dict[str, List[str]]:
        """Find duplicate class definitions"""
        duplicates = {}
        for cls, paths in self.class_index.items():
            if len(paths) > 1:
                duplicates[cls] = paths
        return duplicates
    
    def search(self, query: str) -> List[SystemEntry]:
        """Search systems by query string"""
        query_lower = query.lower()
        results = []
        
        for entry in self.systems.values():
            if (query_lower in entry.name.lower() or
                query_lower in entry.purpose.lower() or
                query_lower in entry.category.lower()):
                results.append(entry)
        
        return results
    
    def export_to_json(self, output_path: Path):
        """Export registry to JSON"""
        data = {
            "systems": {name: asdict(entry) for name, entry in self.systems.items()},
            "categories": self.categories,
            "duplicates": self.find_duplicates(),
            "stats": {
                "total_systems": len(self.systems),
                "total_categories": len(self.categories),
                "total_classes": sum(len(e.classes) for e in self.systems.values()),
            }
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"📄 Registry exported to {output_path}")
    
    def generate_report(self) -> str:
        """Generate human-readable report"""
        lines = []
        lines.append("=" * 80)
        lines.append("ELYSIA SYSTEM REGISTRY REPORT")
        lines.append("=" * 80)
        lines.append("")
        
        # Statistics
        lines.append("## STATISTICS")
        lines.append(f"Total Systems: {len(self.systems)}")
        lines.append(f"Categories: {len(self.categories)}")
        lines.append(f"Total Classes: {sum(len(e.classes) for e in self.systems.values())}")
        lines.append("")
        
        # By Category
        lines.append("## SYSTEMS BY CATEGORY")
        lines.append("-" * 80)
        for category in sorted(self.categories.keys()):
            systems = self.find_by_category(category)
            lines.append(f"\n### {category.upper()} ({len(systems)} systems)")
            for entry in systems[:10]:  # Top 10
                lines.append(f"  • {entry.name}: {entry.purpose[:100]}")
            if len(systems) > 10:
                lines.append(f"  ... and {len(systems) - 10} more")
        lines.append("")
        
        # Duplicates
        duplicates = self.find_duplicates()
        lines.append("## DUPLICATE CLASSES")
        lines.append("-" * 80)
        if duplicates:
            for cls, paths in list(duplicates.items())[:20]:
                lines.append(f"\n⚠️ {cls} (found in {len(paths)} files):")
                for path in paths:
                    lines.append(f"  • {path}")
        else:
            lines.append("✅ No duplicates found!")
        lines.append("")
        
        lines.append("=" * 80)
        
        return "\n".join(lines)


# Singleton instance
_registry_instance = None

def get_system_registry() -> SystemRegistry:
    """Get the global SystemRegistry instance"""
    global _registry_instance
    if _registry_instance is None:
        _registry_instance = SystemRegistry()
    return _registry_instance


if __name__ == "__main__":
    # CLI usage
    logging.basicConfig(level=logging.INFO)
    
    registry = get_system_registry()
    stats = registry.scan_all_systems()
    
    print(registry.generate_report())
    
    # Export
    registry.export_to_json(Path("system_registry.json"))
