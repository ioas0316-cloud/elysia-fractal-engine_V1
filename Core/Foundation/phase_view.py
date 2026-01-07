"""
Phase-tag inspection tool.
Lists nodes in Hippocampus with phase metadata and allows simple filtering.

Usage:
    python Tools/phase_view.py --min-mastery 0.2 --min-entropy 0.5
"""

import argparse
import logging
from Core.System.System.System.Kernel import kernel

logger = logging.getLogger("PhaseView")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-mastery", type=float, default=0.0, help="Minimum quaternion w component")
    parser.add_argument("--min-entropy", type=float, default=0.0, help="Minimum qubit entropy")
    parser.add_argument("--limit", type=int, default=20, help="Max nodes to display")
    args = parser.parse_args()

    matches = kernel.hippocampus.query_by_phase(
        min_mastery=args.min_mastery,
        min_entropy=args.min_entropy,
    )
    tags = kernel.hippocampus.get_phase_tags()
    tag_dict = {t["node"]: t["phase"] for t in tags}
    logger.info(f"Matched {len(matches)} nodes (phase-tagged total={len(tags)})")

    for node in matches[: args.limit]:
        phase = tag_dict.get(node, {})
        q = phase.get("quaternion", {})
        qubit = phase.get("qubit", {})
        logger.info(f"{node}: mastery={q.get('w', 0.0):.3f} entropy={_entropy(list(qubit.values())):.3f} phase={phase}")


def _entropy(probs):
    import math
    total = sum(probs)
    if total == 0:
        return 0.0
    norm = [p / total for p in probs if p > 0]
    return -sum(p * math.log(p, 2) for p in norm)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
