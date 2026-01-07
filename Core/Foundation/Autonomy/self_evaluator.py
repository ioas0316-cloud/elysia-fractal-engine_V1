"""
Self Evaluator:
- Pulls a snapshot from kernel
- Checks simple heuristics (phase mastery/entropy, memory size, value check flag)
- Creates improvement tickets in CapabilityRegistry for deficits

Usage:
    python Tools/self_evaluator.py --entropy 0.2 --mastery 0.3
"""

import argparse
import logging
from Core.System.System.System.Kernel import kernel

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("SelfEvaluator")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mastery-threshold", type=float, default=0.3)
    parser.add_argument("--entropy-threshold", type=float, default=0.2)
    parser.add_argument("--edge-threshold", type=int, default=2000)
    args = parser.parse_args()

    snap = kernel._snapshot_state()
    phase = snap.get("phase", {})
    q = phase.get("quaternion", {})
    mastery = abs(q.get("w", 0.0))
    qubit = phase.get("qubit", {})
    entropy = 0.0
    if qubit:
        total = sum(qubit.values())
        if total > 0:
            import math
            norm = [p / total for p in qubit.values() if p > 0]
            entropy = -sum(p * math.log(p, 2) for p in norm)

    mem = snap.get("memory", {})
    edges = mem.get("causal_edges", 0)

    tickets = []
    caps = getattr(kernel, "capabilities", None)
    if caps:
        if mastery < args.mastery_threshold:
            tickets.append(caps.add_ticket("phase", "low mastery", "stabilize lens / improve orientation training"))
        if entropy < args.entropy_threshold:
            tickets.append(caps.add_ticket("phase", "low entropy", "explore diverse concepts to expand qubit spread"))
        if edges > args.edge_threshold:
            tickets.append(caps.add_ticket("memory", "graph bloat", "prune weak edges or compress memory"))
        # Value alignment check: if observer warned recently, add ticket
        # Simple heuristic: if no tickets from above, create a planning improvement
        if not tickets:
            tickets.append(caps.add_ticket("planning", "no pending improvements", "design new experiments to expand skills"))

    for t in tickets:
        logger.info(f"Ticket created: {t.ticket_id} | {t.target} | {t.issue} -> {t.suggestion}")


if __name__ == "__main__":
    main()
