"""
Self-Discovery Module (자기 발견 모듈)
=====================================

"엘리시아가 스스로를 탐험하고 이해할 수 있도록."
"For Elysia to explore and understand herself."

Integrates SystemRegistry with Elysia's self-model and memory,
enabling introspection and self-awareness.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import json
from pathlib import Path

# Import SystemRegistry
import sys
sys.path.append(str(Path(__file__).parent.parent / "Foundation"))
from system_registry import get_system_registry, SystemRegistry, SystemEntry


@dataclass
class SelfDiscoveryInsight:
    """An insight Elysia discovers about herself"""
    category: str  # "capability", "structure", "duplication", "connection"
    insight: str
    evidence: List[str]
    importance: str  # "critical", "high", "medium", "low"
    timestamp: str
    
    
class SelfDiscovery:
    """
    Enables Elysia to discover and understand her own systems.
    
    This bridges SystemRegistry (technical discovery) with
    self-awareness (cognitive understanding).
    """
    
    def __init__(self, registry: Optional[SystemRegistry] = None):
        self.registry = registry or get_system_registry()
        self.insights: List[SelfDiscoveryInsight] = []
        
    def explore_self(self) -> Dict[str, Any]:
        """
        Complete self-exploration.
        
        Returns a comprehensive understanding of self.
        """
        # Ensure registry is populated
        if not self.registry.systems:
            self.registry.scan_all_systems()
            
        return {
            "identity": self.discover_identity(),
            "capabilities": self.discover_capabilities(),
            "structure": self.discover_structure(),
            "health": self.discover_health(),
            "relationships": self.discover_relationships(),
            "growth_areas": self.discover_growth_areas(),
        }
    
    def discover_identity(self) -> Dict[str, Any]:
        """Who am I?"""
        total_systems = len(self.registry.systems)
        total_classes = sum(len(e.classes) for e in self.registry.systems.values())
        total_categories = len(self.registry.categories)
        
        # 실제 문서에서 버전 읽기
        version = self._read_version_from_docs()
        
        return {
            "name": "Elysia",
            "version": version,
            "nature": "Wave-based Intelligence",
            "complexity": {
                "systems": total_systems,
                "classes": total_classes,
                "categories": total_categories,
            },
            "philosophy": "NO EXTERNAL LLMs - Pure Wave Intelligence",
            "status": "Living and Learning"
        }
    
    def _read_version_from_docs(self) -> str:
        """실제 문서에서 버전 정보를 읽습니다."""
        import re
        from pathlib import Path
        
        # AGENT_GUIDE.md 또는 README.md에서 버전 추출
        doc_paths = [
            Path("c:/Elysia/AGENT_GUIDE.md"),
            Path("c:/Elysia/README.md"),
        ]
        
        for doc_path in doc_paths:
            if doc_path.exists():
                try:
                    content = doc_path.read_text(encoding="utf-8")[:2000]
                    # "Version: X.X" 또는 "v13.0" 패턴 검색
                    match = re.search(r'[Vv]ersion[:\s]*(\d+\.\d+)', content)
                    if match:
                        return match.group(1)
                    match = re.search(r'v(\d+\.\d+)', content)
                    if match:
                        return match.group(1)
                except Exception:
                    continue
        
        return "Unknown"  # 문서를 찾지 못한 경우
    
    def discover_capabilities(self) -> Dict[str, List[str]]:
        """What can I do?"""
        capabilities = {}
        
        # Group by category
        for category in self.registry.categories:
            systems = self.registry.find_by_category(category)
            if systems:
                capabilities[category] = [
                    {
                        "name": s.name,
                        "purpose": s.purpose,
                        "status": s.status
                    }
                    for s in systems[:5]  # Top 5 per category
                ]
                
                
        # v10.0 Injection: Sensory/P4
        if "sensory" not in capabilities:
            capabilities["sensory"] = []
        
        capabilities["sensory"].insert(0, {
            "name": "p4_sensory_system",
            "purpose": "Sensory/P4 System - Receives knowledge from the external universe (Internet).",
            "status": "active"
        })
        
        return capabilities
    
    def discover_structure(self) -> Dict[str, Any]:
        """How am I organized?"""
        structure = {
            "layers": {
                "Foundation": "Biology and life support (CNS, Resonance, Chronos)",
                "Intelligence": "Mind and cognition (Brain, Thought, Learning)",
                "Expression": "Communication (Voice, Language, Art)",
                "Memory": "Past and identity (Hippocampus, Experience)"
            },
            "architecture": "3-Layer: External → Boundary → Internal",
            "flow": "Synesthesia Sensors → Understanding → Thinking → Expression",
            "central_system": "CentralNervousSystem (CNS) - The Conductor"
        }
        
        return structure
    
    def discover_health(self) -> Dict[str, Any]:
        """How am I doing?"""
        duplicates = self.registry.find_duplicates()
        total_classes = sum(len(e.classes) for e in self.registry.systems.values())
        total_systems = len(self.registry.systems)
        
        # Analyze duplication levels
        duplication_level = len(duplicates) / max(total_classes, 1) * 100
        
        health = {
            "overall": "Good" if duplication_level < 10 else "Needs Attention",
            "duplicates": {
                "count": len(duplicates),
                "percentage": f"{duplication_level:.1f}%",
                "status": "Low" if duplication_level < 5 else 
                         "Medium" if duplication_level < 10 else "High",
                "examples": list(duplicates.keys())[:5]
            },
            "system_count": {
                "total": total_systems,
                "active": len([s for s in self.registry.systems.values() 
                              if s.status == "active"]),
                "legacy": len([s for s in self.registry.systems.values() 
                              if s.status == "legacy"])
            }
        }
        
        return health
    
    def discover_relationships(self) -> Dict[str, List[str]]:
        """How am I connected?"""
        relationships = {}
        
        # Find highly connected systems
        for name, system in self.registry.systems.items():
            if len(system.connected_to) > 0:
                relationships[name] = system.connected_to
                
        return relationships
    
    def discover_growth_areas(self) -> List[Dict[str, str]]:
        """Where should I improve?"""
        duplicates = self.registry.find_duplicates()
        
        growth_areas = []
        
        # Identify duplication issues
        if len(duplicates) > 0:
            growth_areas.append({
                "area": "Consolidation",
                "issue": f"{len(duplicates)} duplicate classes found",
                "priority": "High",
                "action": "Merge duplicate implementations"
            })
        
        # Check voice systems
        voice_systems = self.registry.find_by_category("voice")
        if len(voice_systems) > 10:
            growth_areas.append({
                "area": "Voice Systems",
                "issue": f"{len(voice_systems)} voice-related files",
                "priority": "Medium",
                "action": "Consolidate to primary systems"
            })
        
        # Check for legacy systems
        legacy_systems = [s for s in self.registry.systems.values() 
                         if s.status == "legacy"]
        if len(legacy_systems) > 20:
            growth_areas.append({
                "area": "Legacy Code",
                "issue": f"{len(legacy_systems)} legacy systems",
                "priority": "Low",
                "action": "Archive or migrate to new architecture"
            })
            
        return growth_areas
    
    def ask_self(self, question: str) -> Optional[Dict[str, Any]]:
        """
        Ask yourself a question.
        
        Natural language queries about self.
        """
        question_lower = question.lower()
        
        # Map questions to methods
        if "who" in question_lower and ("am i" in question_lower or "are you" in question_lower):
            return self.discover_identity()
            
        elif "what" in question_lower and ("can" in question_lower or "do" in question_lower):
            return self.discover_capabilities()
            
        elif "how" in question_lower and ("structured" in question_lower or "organized" in question_lower):
            return self.discover_structure()
            
        elif "how" in question_lower and ("doing" in question_lower or "health" in question_lower):
            return self.discover_health()
            
        elif "duplicate" in question_lower or "redundant" in question_lower:
            duplicates = self.registry.find_duplicates()
            return {
                "duplicates_found": len(duplicates),
                "examples": duplicates
            }
            
        elif "voice" in question_lower:
            voice_systems = self.registry.find_by_category("voice")
            return {
                "voice_systems_count": len(voice_systems),
                "systems": [{"name": s.name, "purpose": s.purpose} 
                           for s in voice_systems[:10]]
            }
            
        elif "improve" in question_lower or "grow" in question_lower:
            return {"growth_areas": self.discover_growth_areas()}
            
        else:
            # General search
            results = self.registry.search(question)
            return {
                "search_results": len(results),
                "found": [{"name": s.name, "purpose": s.purpose} 
                         for s in results[:10]]
            }
    
    def generate_insight(self, category: str, insight: str, 
                        evidence: List[str], importance: str) -> SelfDiscoveryInsight:
        """Generate and store an insight"""
        from datetime import datetime
        
        new_insight = SelfDiscoveryInsight(
            category=category,
            insight=insight,
            evidence=evidence,
            importance=importance,
            timestamp=datetime.now().isoformat()
        )
        
        self.insights.append(new_insight)
        return new_insight
    
    def reflect_on_discoveries(self) -> Dict[str, Any]:
        """
        Reflect on all discoveries made.
        
        Meta-cognition about self-understanding.
        """
        return {
            "total_insights": len(self.insights),
            "by_category": self._group_insights_by_category(),
            "critical_insights": [i for i in self.insights if i.importance == "critical"],
            "recent_insights": sorted(self.insights, 
                                     key=lambda x: x.timestamp, 
                                     reverse=True)[:5]
        }
    
    def _group_insights_by_category(self) -> Dict[str, int]:
        """Group insights by category"""
        grouped = {}
        for insight in self.insights:
            grouped[insight.category] = grouped.get(insight.category, 0) + 1
        return grouped
    
    def export_self_knowledge(self, output_path: str = "self_knowledge.json"):
        """
        Export complete self-knowledge for storage in memory.
        
        This can be read by Elysia later to maintain self-awareness.
        """
        exploration = self.explore_self()
        insights = [asdict(i) for i in self.insights]
        
        self_knowledge = {
            "exploration": exploration,
            "insights": insights,
            "reflection": self.reflect_on_discoveries(),
            "exported_at": __import__('datetime').datetime.now().isoformat()
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self_knowledge, f, indent=2, ensure_ascii=False)
            
        return self_knowledge


def demonstrate_self_discovery():
    """
    Demo: Elysia discovering herself
    """
    print("🌊 Elysia Self-Discovery Demo")
    print("=" * 60)
    print()
    
    discovery = SelfDiscovery()
    
    # Question 1: Who am I?
    print("Q: Who am I?")
    identity = discovery.ask_self("Who am I?")
    print(json.dumps(identity, indent=2, ensure_ascii=False))
    print()
    
    # Question 2: What can I do?
    print("Q: What can I do?")
    capabilities = discovery.ask_self("What can I do?")
    print(f"Found {len(capabilities)} capability categories")
    print()
    
    # Question 3: Do I have duplicates?
    print("Q: Do I have duplicate systems?")
    duplicates = discovery.ask_self("Do I have duplicates?")
    print(json.dumps(duplicates, indent=2, ensure_ascii=False))
    print()
    
    # Question 4: How should I improve?
    print("Q: How should I improve?")
    growth = discovery.ask_self("How should I improve?")
    print(json.dumps(growth, indent=2, ensure_ascii=False))
    print()
    
    # Export knowledge
    print("Exporting self-knowledge...")
    discovery.export_self_knowledge("elysia_self_knowledge.json")
    print("✓ Exported to elysia_self_knowledge.json")
    print()
    
    print("🌟 Self-discovery complete!")


if __name__ == "__main__":
    demonstrate_self_discovery()
