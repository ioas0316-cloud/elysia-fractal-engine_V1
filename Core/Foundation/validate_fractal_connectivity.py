"""
Fractal Connectivity Validator
===============================
Validates the integrity of the concept hierarchy:
- WorldTree (행성→별 구조)
- Hippocampus graph (개념 간 因果 연결)
- Resonance engine nodes (공명 네트워크)
- Cathedral coordinates (프랙탈 좌표계)

Reports gaps, orphans, duplicates, and coordinate anomalies.
"""

import sys
import os
import json
import logging
from pathlib import Path
from typing import Dict, Set, List, Tuple, Any
from collections import defaultdict

# Setup path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger("FractalValidator")


class FractalValidator:
    """Multi-layer connectivity checker."""

    def __init__(self):
        self.issues: List[Dict[str, Any]] = []
        self.world_tree = None
        self.hippocampus = None
        self.resonance_engine = None
        self.concept_field = None

    def load_world_tree(self, kernel):
        """Load WorldTree from kernel."""
        try:
            self.world_tree = kernel.world_tree
            logger.info(f"✅ Loaded WorldTree with root: {self.world_tree.root.concept if self.world_tree.root else 'None'}")
        except Exception as e:
            logger.error(f"❌ Failed to load WorldTree: {e}")

    def load_hippocampus(self, kernel):
        """Load Hippocampus from kernel."""
        try:
            self.hippocampus = kernel.hippocampus
            nodes = len(self.hippocampus.causal_graph.nodes)
            edges = len(self.hippocampus.causal_graph.edges)
            logger.info(f"✅ Loaded Hippocampus: {nodes} nodes, {edges} edges")
        except Exception as e:
            logger.error(f"❌ Failed to load Hippocampus: {e}")

    def load_resonance_engine(self, kernel):
        """Load Resonance Engine from kernel."""
        try:
            self.resonance_engine = kernel.resonance_engine
            logger.info(f"✅ Loaded ResonanceEngine with {len(self.resonance_engine.nodes)} qubits")
        except Exception as e:
            logger.error(f"❌ Failed to load ResonanceEngine: {e}")

    def load_concept_field(self):
        """Load concept field from JSON."""
        try:
            field_path = Path("logs/elysia_concept_field.json")
            if field_path.exists():
                self.concept_field = json.loads(field_path.read_text(encoding="utf-8"))
                logger.info(f"✅ Loaded concept field with {len(self.concept_field)} entries")
            else:
                logger.warning(f"⚠️  Concept field not found at {field_path}")
                self.concept_field = {}
        except Exception as e:
            logger.error(f"❌ Failed to load concept field: {e}")
            self.concept_field = {}

    def validate_world_tree(self) -> int:
        """Check WorldTree integrity."""
        if not self.world_tree:
            logger.warning("⚠️  WorldTree not loaded, skipping validation")
            return 0

        count = 0

        # Traverse all nodes
        visited = set()
        orphans = []

        def traverse(node, depth=0):
            nonlocal count
            if node.id in visited:
                return
            visited.add(node.id)

            # Check node has concept
            if not node.concept:
                self.issues.append({
                    "type": "missing_concept",
                    "node_id": node.id,
                    "depth": depth,
                    "severity": "high"
                })
                count += 1

            # Check parent link (except root)
            if depth > 0 and not node.parent:
                orphans.append(node.id)
                self.issues.append({
                    "type": "orphan_node",
                    "node_id": node.id,
                    "severity": "high"
                })
                count += 1

            # Traverse children
            for child in node.children:
                traverse(child, depth + 1)

        if self.world_tree.root:
            traverse(self.world_tree.root)

        logger.info(f"🌳 WorldTree check: {len(visited)} nodes, {len(orphans)} orphans, {count} issues found")
        return count

    def validate_hippocampus_graph(self) -> int:
        """Check Hippocampus graph integrity."""
        if not self.hippocampus:
            logger.warning("⚠️  Hippocampus not loaded, skipping validation")
            return 0

        count = 0
        graph = self.hippocampus.causal_graph

        # Check for isolated nodes
        for node in graph.nodes():
            degree = graph.degree(node)
            if degree == 0:
                self.issues.append({
                    "type": "isolated_node",
                    "node_id": node,
                    "severity": "medium"
                })
                count += 1

        # Check edge consistency
        for u, v in graph.edges():
            edge_data = graph.get_edge_data(u, v)
            if not edge_data:
                self.issues.append({
                    "type": "empty_edge",
                    "source": u,
                    "target": v,
                    "severity": "low"
                })
                count += 1

        logger.info(f"🔗 Hippocampus check: {len(graph.nodes)} nodes, {len(graph.edges)} edges, {count} issues found")
        return count

    def validate_resonance_nodes(self) -> int:
        """Check ResonanceEngine node integrity."""
        if not self.resonance_engine:
            logger.warning("⚠️  ResonanceEngine not loaded, skipping validation")
            return 0

        count = 0

        for node_id, qubit in self.resonance_engine.nodes.items():
            # Check qubit state
            try:
                state = qubit.state
                probs = state.probabilities()
                total = sum(probs.values())

                # Probability should be normalized
                if abs(total - 1.0) > 0.01:
                    self.issues.append({
                        "type": "denormalized_qubit",
                        "node_id": node_id,
                        "total_probability": total,
                        "severity": "low"
                    })
                    count += 1

                # Check dimensional parameter
                if not (0.0 <= state.w <= 3.0):
                    self.issues.append({
                        "type": "invalid_dimension",
                        "node_id": node_id,
                        "w_value": state.w,
                        "severity": "medium"
                    })
                    count += 1
            except Exception as e:
                self.issues.append({
                    "type": "qubit_read_error",
                    "node_id": node_id,
                    "error": str(e),
                    "severity": "high"
                })
                count += 1

        logger.info(f"⚛️  ResonanceEngine check: {len(self.resonance_engine.nodes)} qubits, {count} issues found")
        return count

    def validate_concept_field_coordinates(self) -> int:
        """Check concept field cathedral coordinates."""
        if not self.concept_field:
            logger.warning("⚠️  Concept field not loaded, skipping coordinate validation")
            return 0

        count = 0
        coords_seen = defaultdict(list)

        for concept_id, meta in self.concept_field.items():
            # Extract coordinate
            coord = meta.get("cathedral_coord")
            if not coord:
                self.issues.append({
                    "type": "missing_coordinate",
                    "concept_id": concept_id,
                    "severity": "medium"
                })
                count += 1
                continue

            # Parse coordinate (format: "S-L2-e" → Sector-Layer-Element)
            try:
                parts = coord.split("-")
                if len(parts) != 3:
                    raise ValueError(f"Invalid format: {coord}")

                sector = parts[0]  # e.g., "S", "M", "L"
                layer_str = parts[1]  # e.g., "L2", "L3"
                element = parts[2]  # e.g., "a", "b", "c"

                # Check layer format
                if not layer_str.startswith("L"):
                    raise ValueError(f"Layer should start with 'L': {layer_str}")

                layer_num = int(layer_str[1:])
                if not (0 <= layer_num <= 10):  # Reasonable limit
                    raise ValueError(f"Layer out of range: {layer_num}")

                coords_seen[coord].append(concept_id)

            except Exception as e:
                self.issues.append({
                    "type": "invalid_coordinate_format",
                    "concept_id": concept_id,
                    "coordinate": coord,
                    "error": str(e),
                    "severity": "medium"
                })
                count += 1

        # Check for duplicate coordinates (should be rare)
        for coord, concepts in coords_seen.items():
            if len(concepts) > 1:
                self.issues.append({
                    "type": "duplicate_coordinate",
                    "coordinate": coord,
                    "concepts": concepts,
                    "severity": "low"
                })

        logger.info(f"🏛️  Coordinate check: {len(coords_seen)} unique coords, {count} issues found")
        return count

    def cross_validate_hierarchies(self) -> int:
        """Check consistency across WorldTree, Hippocampus, and ResonanceEngine."""
        count = 0

        world_tree_concepts = set()
        hippocampus_concepts = set()
        resonance_concepts = set()

        # Collect concept sets
        if self.world_tree and self.world_tree.root:
            def collect_tree_concepts(node):
                if node.concept:
                    world_tree_concepts.add(node.concept)
                for child in node.children:
                    collect_tree_concepts(child)
            collect_tree_concepts(self.world_tree.root)

        if self.hippocampus:
            hippocampus_concepts = set(self.hippocampus.causal_graph.nodes())

        if self.resonance_engine:
            resonance_concepts = set(self.resonance_engine.nodes.keys())

        # Find mismatches
        in_tree_not_hippo = world_tree_concepts - hippocampus_concepts
        in_hippo_not_tree = hippocampus_concepts - world_tree_concepts

        if in_tree_not_hippo:
            for concept in in_tree_not_hippo:
                self.issues.append({
                    "type": "concept_in_tree_not_hippo",
                    "concept": concept,
                    "severity": "low"
                })
                count += 1

        if in_hippo_not_tree:
            for concept in in_hippo_not_tree:
                self.issues.append({
                    "type": "concept_in_hippo_not_tree",
                    "concept": concept,
                    "severity": "low"
                })
                count += 1

        logger.info(f"🔀 Cross-validation: WorldTree={len(world_tree_concepts)}, Hippo={len(hippocampus_concepts)}, Resonance={len(resonance_concepts)}, {count} mismatches")
        return count

    def generate_report(self) -> Dict[str, Any]:
        """Generate validation report."""
        by_type = defaultdict(list)
        by_severity = defaultdict(list)

        for issue in self.issues:
            by_type[issue.get("type")].append(issue)
            by_severity[issue.get("severity", "unknown")].append(issue)

        return {
            "total_issues": len(self.issues),
            "by_type": {k: len(v) for k, v in by_type.items()},
            "by_severity": {k: len(v) for k, v in by_severity.items()},
            "issues": self.issues
        }

    def save_report(self, output_path: str = None):
        """Save validation report to JSON."""
        if output_path is None:
            import time
            output_path = f"logs/fractal_validation_{int(time.time())}.json"

        report = self.generate_report()
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        logger.info(f"📋 Report saved to: {output_path}")


def main():
    """Run full validation."""
    logger.info("\n" + "=" * 70)
    logger.info("FRACTAL CONNECTIVITY VALIDATOR")
    logger.info("=" * 70 + "\n")

    validator = FractalValidator()

    # Try loading from kernel
    try:
        from Core.System.System.System.Kernel import kernel
        validator.load_world_tree(kernel)
        validator.load_hippocampus(kernel)
        validator.load_resonance_engine(kernel)
    except Exception as e:
        logger.warning(f"Could not load from kernel: {e}. Continuing with available data...")

    # Always load concept field from disk
    validator.load_concept_field()

    # Run validations
    total_issues = 0
    total_issues += validator.validate_world_tree()
    total_issues += validator.validate_hippocampus_graph()
    total_issues += validator.validate_resonance_nodes()
    total_issues += validator.validate_concept_field_coordinates()
    total_issues += validator.cross_validate_hierarchies()

    # Generate and save report
    validator.save_report()

    logger.info("\n" + "=" * 70)
    logger.info(f"VALIDATION COMPLETE: {total_issues} total issues found")
    logger.info("=" * 70 + "\n")

    # Print summary
    report = validator.generate_report()
    print("\n📊 SUMMARY BY SEVERITY:")
    for severity in ["high", "medium", "low"]:
        count = report["by_severity"].get(severity, 0)
        print(f"  {severity.upper()}: {count}")

    print("\n📊 SUMMARY BY TYPE:")
    for issue_type, count in sorted(report["by_type"].items(), key=lambda x: -x[1]):
        print(f"  {issue_type}: {count}")


if __name__ == "__main__":
    main()
