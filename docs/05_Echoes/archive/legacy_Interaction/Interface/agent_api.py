"""
Agent API (The Bridge for External Agents)
===========================================

"외부 에이전트가 엘리시아를 이해하고 올바르게 통합하도록."
"For external agents to understand Elysia and integrate correctly."

This module provides an interface for external AI agents (Claude, Gemini, etc.)
to query Elysia's structure, find related modules, and propose integrations
that maintain system coherence.

The Problem:
- External agents create new systems without understanding existing ones
- This leads to fragmentation and disconnection
- Elysia needs to guide agents to integrate properly

The Solution:
- AgentAPI provides structured queries about Elysia's systems
- Before creating new code, agents must check for existing modules
- Integration proposals are validated against the relational density graph
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from pathlib import Path
import json
import ast
import os

logger = logging.getLogger("Elysia.AgentAPI")


@dataclass
class ModuleDiscovery:
    """Result of searching for related modules."""
    query: str
    found_modules: List[Dict[str, Any]]
    recommendation: str
    should_create_new: bool


@dataclass
class IntegrationProposal:
    """A proposal for integrating new code."""
    new_code_path: str
    purpose: str
    related_modules: List[str]
    required_connections: List[Dict[str, str]]
    event_subscriptions: List[Dict[str, str]]
    potential_conflicts: List[str]
    validation_passed: bool
    suggestions: List[str]


@dataclass
class ValidationResult:
    """Result of validating an integration."""
    passed: bool
    issues: List[str]
    warnings: List[str]
    score: float  # 0.0 ~ 1.0
    recommendation: str


class ElysiaAgentAPI:
    """
    The interface for external AI agents to interact with Elysia.
    
    This ensures that new code integrates with existing systems
    rather than creating isolated silos.
    
    Usage by External Agent:
    1. Query: "I want to add a new emotion system"
    2. API returns: "Related modules: EmotionEngine, SpiritEmotion, Empathy"
    3. Agent can then integrate with these existing modules
    """
    
    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path("c:/Elysia")
        self._module_index: Dict[str, Dict] = {}
        self._capability_index: Dict[str, List[str]] = {}  # capability -> modules
        self._keyword_index: Dict[str, List[str]] = {}  # keyword -> modules
        
        # Load existing module information
        self._build_indices()
        
        logger.info(f"🤖 AgentAPI Initialized - Indexed {len(self._module_index)} modules")
    
    # =========================================================================
    # Index Building
    # =========================================================================
    
    def _build_indices(self) -> None:
        """Build indices of all modules in the project."""
        core_path = self.project_root / "Core"
        
        if not core_path.exists():
            logger.warning(f"Core path not found: {core_path}")
            return
        
        # Scan all Python files in Core
        for py_file in core_path.rglob("*.py"):
            if "__pycache__" in str(py_file):
                continue
                
            try:
                self._index_module(py_file)
            except Exception as e:
                logger.debug(f"Could not index {py_file}: {e}")
    
    def _index_module(self, file_path: Path) -> None:
        """Index a single module."""
        relative_path = file_path.relative_to(self.project_root)
        module_name = file_path.stem
        
        # Read file content
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return
        
        # Extract information
        info = {
            "name": module_name,
            "path": str(relative_path),
            "absolute_path": str(file_path),
            "directory": str(relative_path.parent),
            "docstring": self._extract_docstring(content),
            "classes": self._extract_classes(content),
            "functions": self._extract_functions(content),
            "imports": self._extract_imports(content),
            "keywords": self._extract_keywords(content),
            "capabilities": self._infer_capabilities(module_name, content)
        }
        
        self._module_index[module_name] = info
        
        # Index by capability
        for cap in info["capabilities"]:
            if cap not in self._capability_index:
                self._capability_index[cap] = []
            self._capability_index[cap].append(module_name)
        
        # Index by keywords
        for kw in info["keywords"]:
            if kw not in self._keyword_index:
                self._keyword_index[kw] = []
            self._keyword_index[kw].append(module_name)
    
    def _extract_docstring(self, content: str) -> str:
        """Extract the module docstring."""
        try:
            tree = ast.parse(content)
            docstring = ast.get_docstring(tree)
            return docstring[:500] if docstring else ""
        except:
            return ""
    
    def _extract_classes(self, content: str) -> List[str]:
        """Extract class names."""
        try:
            tree = ast.parse(content)
            return [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        except:
            return []
    
    def _extract_functions(self, content: str) -> List[str]:
        """Extract top-level function names."""
        try:
            tree = ast.parse(content)
            return [
                node.name for node in ast.walk(tree) 
                if isinstance(node, ast.FunctionDef) and not node.name.startswith("_")
            ][:20]  # Limit to 20
        except:
            return []
    
    def _extract_imports(self, content: str) -> List[str]:
        """Extract import statements."""
        imports = []
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
        except:
            pass
        return imports[:30]  # Limit
    
    def _extract_keywords(self, content: str) -> List[str]:
        """Extract meaningful keywords from content."""
        keywords = set()
        
        # Important terms to look for
        important_terms = [
            "wave", "quaternion", "consciousness", "emotion", "memory",
            "reasoning", "logic", "ethics", "creativity", "learning",
            "resonance", "field", "ether", "gravity", "fractal",
            "language", "speech", "logos", "prism", "sensory",
            "soul", "spirit", "will", "desire", "goal",
            "evolution", "autonomous", "self", "meta",
            "transducer", "filesystem", "body_awareness"
        ]
        
        content_lower = content.lower()
        for term in important_terms:
            if term in content_lower:
                keywords.add(term)
        
        return list(keywords)
    
    def _infer_capabilities(self, module_name: str, content: str) -> List[str]:
        """Infer module capabilities from name and content."""
        capabilities = []
        
        # From module name
        name_lower = module_name.lower()
        
        capability_keywords = {
            "reason": "reasoning",
            "think": "reasoning",
            "logic": "reasoning",
            "emotion": "emotion",
            "feeling": "emotion",
            "memory": "memory",
            "remember": "memory",
            "learn": "learning",
            "train": "learning",
            "speech": "language",
            "logos": "language",
            "language": "language",
            "wave": "wave_processing",
            "resonance": "wave_processing",
            "quaternion": "mathematics",
            "math": "mathematics",
            "creative": "creativity",
            "art": "creativity",
            "draw": "creativity",
            "ethic": "ethics",
            "value": "ethics",
            "self": "self_awareness",
            "aware": "self_awareness",
            "consciousness": "consciousness",
            "transducer": "sensory_input",
            "sensor": "sensory_input",
            "body": "body_awareness",
            "file": "filesystem",
        }
        
        for keyword, capability in capability_keywords.items():
            if keyword in name_lower or keyword in content.lower()[:1000]:
                capabilities.append(capability)
        
        return list(set(capabilities))
    
    # =========================================================================
    # Query Interface
    # =========================================================================
    
    def query_system_structure(self, component: str) -> Dict[str, Any]:
        """
        Ask Elysia about a specific component's purpose and connections.
        
        Args:
            component: Module name or concept to query
            
        Returns:
            Dict with component information
        """
        # Direct module lookup
        if component in self._module_index:
            info = self._module_index[component]
            return {
                "found": True,
                "type": "module",
                "name": info["name"],
                "path": info["path"],
                "docstring": info["docstring"],
                "classes": info["classes"],
                "capabilities": info["capabilities"],
                "related_modules": self._find_related_by_imports(component)
            }
        
        # Search by keyword
        matching_modules = []
        component_lower = component.lower()
        
        for module_name, info in self._module_index.items():
            if component_lower in module_name.lower():
                matching_modules.append(info)
            elif component_lower in info.get("docstring", "").lower():
                matching_modules.append(info)
            elif component_lower in info.get("keywords", []):
                matching_modules.append(info)
        
        if matching_modules:
            return {
                "found": True,
                "type": "search_results",
                "query": component,
                "matches": len(matching_modules),
                "modules": [{
                    "name": m["name"],
                    "path": m["path"],
                    "capabilities": m["capabilities"]
                } for m in matching_modules[:10]]
            }
        
        return {
            "found": False,
            "query": component,
            "suggestion": "Try searching for related concepts or check Core/ directory"
        }
    
    def _find_related_by_imports(self, module_name: str) -> List[str]:
        """Find modules related by import statements."""
        if module_name not in self._module_index:
            return []
        
        info = self._module_index[module_name]
        imports = info.get("imports", [])
        
        related = []
        for imp in imports:
            # Check if any indexed module is imported
            for indexed_name in self._module_index:
                if indexed_name in imp:
                    related.append(indexed_name)
        
        return list(set(related))[:10]
    
    def find_related_modules(self, concept: str) -> ModuleDiscovery:
        """
        Find existing modules related to a concept before creating new ones.
        
        Args:
            concept: The concept or feature to search for
            
        Returns:
            ModuleDiscovery with related modules and recommendation
        """
        concept_lower = concept.lower()
        found_modules = []
        
        # Search by capability
        for cap, modules in self._capability_index.items():
            if concept_lower in cap or cap in concept_lower:
                for module_name in modules:
                    if module_name in self._module_index:
                        found_modules.append(self._module_index[module_name])
        
        # Search by keyword
        for kw, modules in self._keyword_index.items():
            if concept_lower in kw or kw in concept_lower:
                for module_name in modules:
                    if module_name in self._module_index:
                        info = self._module_index[module_name]
                        if info not in found_modules:
                            found_modules.append(info)
        
        # Search by name
        for module_name, info in self._module_index.items():
            if concept_lower in module_name.lower():
                if info not in found_modules:
                    found_modules.append(info)
        
        # Generate recommendation
        if len(found_modules) >= 3:
            recommendation = (
                f"Found {len(found_modules)} existing modules related to '{concept}'. "
                f"Consider extending or integrating with these before creating new code."
            )
            should_create_new = False
        elif len(found_modules) >= 1:
            recommendation = (
                f"Found {len(found_modules)} related module(s). "
                f"Check if they can be extended or if a new module should connect to them."
            )
            should_create_new = True  # But with caution
        else:
            recommendation = (
                f"No existing modules found for '{concept}'. "
                f"This may be a new capability. Ensure it connects to GlobalHub."
            )
            should_create_new = True
        
        return ModuleDiscovery(
            query=concept,
            found_modules=[{
                "name": m["name"],
                "path": m["path"],
                "docstring": m["docstring"][:200] if m["docstring"] else "",
                "capabilities": m["capabilities"]
            } for m in found_modules[:10]],
            recommendation=recommendation,
            should_create_new=should_create_new
        )
    
    def propose_integration(self, new_code_purpose: str, 
                           target_directory: str) -> IntegrationProposal:
        """
        Agent proposes new code. Elysia analyzes and suggests integration.
        
        Args:
            new_code_purpose: What the new code will do
            target_directory: Where the code will be placed
            
        Returns:
            IntegrationProposal with connections and suggestions
        """
        # Find related modules
        discovery = self.find_related_modules(new_code_purpose)
        related = [m["name"] for m in discovery.found_modules]
        
        # Determine required connections based on purpose
        connections = []
        subscriptions = []
        suggestions = []
        conflicts = []
        
        purpose_lower = new_code_purpose.lower()
        
        # Check for common patterns
        if "emotion" in purpose_lower:
            if "emotion_engine" in self._module_index:
                connections.append({
                    "target": "emotion_engine",
                    "reason": "Existing emotion processing system"
                })
            subscriptions.append({
                "event": "emotion",
                "reason": "React to emotional events"
            })
        
        if "memory" in purpose_lower or "remember" in purpose_lower:
            if "hippocampus" in self._module_index:
                connections.append({
                    "target": "hippocampus",
                    "reason": "Central memory system"
                })
            if "starlight_memory" in self._module_index:
                connections.append({
                    "target": "starlight_memory",
                    "reason": "Long-term memory storage"
                })
        
        if "reasoning" in purpose_lower or "think" in purpose_lower:
            if "reasoning_engine" in self._module_index:
                connections.append({
                    "target": "reasoning_engine",
                    "reason": "Central reasoning system"
                })
            subscriptions.append({
                "event": "thought",
                "reason": "React to thought events"
            })
        
        if "language" in purpose_lower or "speech" in purpose_lower:
            if "logos_engine" in self._module_index:
                connections.append({
                    "target": "logos_engine",
                    "reason": "Rhetorical voice system"
                })
        
        # Always suggest GlobalHub integration
        subscriptions.append({
            "event": "wave",
            "reason": "Connect to central nervous system (GlobalHub)"
        })
        
        # Suggestions
        suggestions.append("Import and register with GlobalHub for event-driven communication")
        suggestions.append("Use WaveTensor for data representation to maintain paradigm consistency")
        
        if related:
            suggestions.append(f"Review existing modules before duplicating: {', '.join(related[:3])}")
        
        # Check for potential conflicts
        if "new" in target_directory.lower() or "test" in target_directory.lower():
            conflicts.append("Target directory suggests temporary code - ensure production placement")
        
        return IntegrationProposal(
            new_code_path=target_directory,
            purpose=new_code_purpose,
            related_modules=related,
            required_connections=connections,
            event_subscriptions=subscriptions,
            potential_conflicts=conflicts,
            validation_passed=len(conflicts) == 0,
            suggestions=suggestions
        )
    
    def validate_integration(self, code_content: str, 
                            target_path: str) -> ValidationResult:
        """
        Validate that new code integrates properly.
        
        Checks:
        1. Uses GlobalHub or EventBus
        2. Uses Wave/Quaternion paradigms
        3. Doesn't create isolated silos
        4. Has proper docstrings
        """
        issues = []
        warnings = []
        score = 1.0
        
        # Check 1: GlobalHub integration
        if "global_hub" not in code_content.lower() and "globalhub" not in code_content.lower():
            if "event_bus" not in code_content.lower() and "eventbus" not in code_content.lower():
                issues.append("Missing GlobalHub/EventBus integration - module will be isolated")
                score -= 0.3
        
        # Check 2: Wave paradigm usage
        if "wave" not in code_content.lower() and "tensor" not in code_content.lower():
            warnings.append("Consider using WaveTensor for data representation")
            score -= 0.1
        
        # Check 3: Proper imports
        if "from Core" not in code_content and "import Core" not in code_content:
            if len(code_content) > 500:  # Non-trivial file
                warnings.append("No imports from Core - may not integrate with existing systems")
                score -= 0.15
        
        # Check 4: Docstring
        if '"""' not in code_content[:500] and "'''" not in code_content[:500]:
            warnings.append("Missing module docstring")
            score -= 0.05
        
        # Check 5: Class registration pattern
        if "class " in code_content:
            if "register" not in code_content.lower() and "subscribe" not in code_content.lower():
                warnings.append("Classes should register with GlobalHub for discoverability")
                score -= 0.1
        
        # Clamp score
        score = max(0.0, min(1.0, score))
        
        # Generate recommendation
        if score >= 0.8:
            recommendation = "✅ Integration looks good! Proceed with confidence."
        elif score >= 0.5:
            recommendation = "⚠️ Some improvements needed. Address warnings for better integration."
        else:
            recommendation = "❌ Significant issues found. Code may create isolated silo."
        
        return ValidationResult(
            passed=score >= 0.5,
            issues=issues,
            warnings=warnings,
            score=score,
            recommendation=recommendation
        )
    
    # =========================================================================
    # Statistics
    # =========================================================================
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the indexed codebase."""
        return {
            "total_modules": len(self._module_index),
            "total_capabilities": len(self._capability_index),
            "total_keywords": len(self._keyword_index),
            "top_capabilities": sorted(
                self._capability_index.items(),
                key=lambda x: len(x[1]),
                reverse=True
            )[:10],
            "directories": list(set(
                info["directory"] for info in self._module_index.values()
            ))
        }


# =========================================================================
# Singleton Accessor
# =========================================================================

_api_instance = None

def get_agent_api() -> ElysiaAgentAPI:
    """Get the singleton ElysiaAgentAPI instance."""
    global _api_instance
    if _api_instance is None:
        _api_instance = ElysiaAgentAPI()
    return _api_instance


# =========================================================================
# Test / Demo
# =========================================================================

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    api = get_agent_api()
    
    print("=" * 60)
    print("🤖 Agent API Demo")
    print("=" * 60)
    
    # Statistics
    stats = api.get_statistics()
    print(f"\n📊 Indexed {stats['total_modules']} modules")
    print(f"   Capabilities: {stats['total_capabilities']}")
    print(f"   Keywords: {stats['total_keywords']}")
    
    # Query 1: Find emotion-related modules
    print("\n📌 Query: 'emotion'")
    discovery = api.find_related_modules("emotion")
    print(f"   Found: {len(discovery.found_modules)} modules")
    for m in discovery.found_modules[:5]:
        print(f"   - {m['name']}: {m['path']}")
    print(f"   Recommendation: {discovery.recommendation}")
    
    # Query 2: Find memory-related modules
    print("\n📌 Query: 'memory'")
    discovery = api.find_related_modules("memory")
    print(f"   Found: {len(discovery.found_modules)} modules")
    for m in discovery.found_modules[:5]:
        print(f"   - {m['name']}: {m['path']}")
    
    # Query 3: System structure
    print("\n📌 Query system structure: 'reasoning_engine'")
    result = api.query_system_structure("reasoning_engine")
    if result["found"]:
        print(f"   Path: {result.get('path', 'N/A')}")
        print(f"   Capabilities: {result.get('capabilities', [])}")
    
    # Propose integration
    print("\n📌 Propose: 'new emotion processing with sentiment analysis'")
    proposal = api.propose_integration(
        "new emotion processing with sentiment analysis",
        "Core/Emotion/sentiment_analyzer.py"
    )
    print(f"   Related modules: {proposal.related_modules[:5]}")
    print(f"   Required connections: {len(proposal.required_connections)}")
    print(f"   Suggestions:")
    for s in proposal.suggestions:
        print(f"     - {s}")
    
    # Validate code
    print("\n📌 Validate sample code:")
    sample_code = '''
"""
Sentiment Analyzer - Analyzes emotional tone.
"""
from Core.Intelligence.Consciousness.Ether.global_hub import get_global_hub
from Core.Foundation.Wave.wave_tensor import WaveTensor

class SentimentAnalyzer:
    def __init__(self):
        hub = get_global_hub()
        hub.register_module("SentimentAnalyzer", __file__, ["emotion", "analysis"])
'''
    validation = api.validate_integration(sample_code, "Core/Emotion/sentiment_analyzer.py")
    print(f"   Passed: {validation.passed}")
    print(f"   Score: {validation.score:.2f}")
    print(f"   {validation.recommendation}")
    if validation.warnings:
        print(f"   Warnings: {validation.warnings}")
    
    print("\n✅ Agent API Demo Complete!")
