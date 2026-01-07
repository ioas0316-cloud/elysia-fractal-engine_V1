from dataclasses import dataclass, field
from typing import List, Dict, Any, Callable, Optional

from nano_core.bus import MessageBus
from nano_core.message import Message


@dataclass
class WisdomVirus:
    """
    A minimal, declarative container for a "unit of meaning" that can
    propagate through the concept graph (KG) and mutate by context.

    This is an offline, LLM-free mechanism aligned with the Protocol:
    - Propagation -> adds supports/depends_on edges and adjusts value mass.
    - Mutation    -> context-specific template transforms.
    - Safety      -> confidence thresholds + quarantine when refutes grow.
    """

    id: str
    statement: str
    seed_hosts: List[str]  # concept node ids to infect initially
    triggers: List[str] = field(default_factory=list)  # phrases to activate
    mutate: Optional[Callable[[str, str], str]] = None  # (host, statement)->str
    reinforce: float = 0.3  # alpha for supports
    decay: float = 0.02      # lambda (per propagation step)
    max_hops: int = 2        # propagation radius


class VirusEngine:
    """
    Applies a WisdomVirus to the KG via a small number of offline passes.
    Integrates with value mass (09_VALUE_MASS_SPEC) by calling an updater.
    """

    def __init__(self, bus: MessageBus, kg_manager=None, update_value_mass_fn=None):
        self.bus = bus
        self.kg = kg_manager
        self.update_value_mass = update_value_mass_fn

    def propagate(self, virus: WisdomVirus, context_tag: str = "virus:propagation"):
        """
        For each seed host, push the virus to neighbors up to max_hops.
        Adds `supports` edges with confidence proportional to distance.
        """
        from collections import deque

        for seed in virus.seed_hosts:
            if not self.kg:
                continue

            visited = {seed: 0}
            q = deque([seed])
            while q:
                cur = q.popleft()
                depth = visited[cur]
                if depth >= virus.max_hops:
                    continue
                # neighbors
                neighbors = self.kg.get_neighbors(cur) or []
                for nb in neighbors:
                    if nb in visited:
                        continue
                    visited[nb] = depth + 1
                    q.append(nb)

                # apply supports to neighbors
                for nb in neighbors:
                    if nb in visited and visited[nb] < depth + 1:
                        continue
                    conf = max(0.0, virus.reinforce * (1.0 - virus.decay * depth))
                    text = virus.statement
                    if virus.mutate:
                        try:
                            text = virus.mutate(nb, text)
                        except Exception:
                            pass

                    # --- Gravity Well ---
                    node1_mass = (self.kg.get_node(cur) or {}).get("mass", 0.0)
                    node2_mass = (self.kg.get_node(nb) or {}).get("mass", 0.0)
                    gravity_bonus = 0.5 * (node1_mass + node2_mass) # Factor can be tuned
                    final_strength = conf + gravity_bonus
                    # --- End Gravity Well ---

                    msg = Message(
                        verb="validate",
                        slots={
                            "subject": cur,
                            "object": nb,
                            "relation": "supports",
                            "confidence": conf,
                            "evidence_text": text
                        },
                        src="WisdomVirus",
                        strength=final_strength,
                    )
                    self.bus.post(msg)

    def _support_edge(self, source: str, target: str, confidence: float, evidence_text: str, context_tag: str):
        try:
            self.kg.add_edge(
                source=source,
                target=target,
                relation="supports",
                confidence=confidence,
                metadata={
                    "timestamp": None,
                    "evidence_paths": [f"{context_tag}:{source}->{target}"],
                    "statement": evidence_text,
                },
            )
        except Exception:
            pass

