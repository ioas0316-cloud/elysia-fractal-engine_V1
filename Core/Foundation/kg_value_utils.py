"""
KG Value Utils

Helpers to add value-related relations with evidence and confidence
without changing the core KGManager API.
"""
from __future__ import annotations

from datetime import datetime
from typing import Iterable, Optional
from pathlib import Path
from kg_manager import KGManager


def _ts() -> str:
    return datetime.utcnow().isoformat() + "Z"


def add_value_relation(
    kg: KGManager,
    source: str,
    target: str,
    relation: str,  # e.g., 'supports' | 'refutes' | 'depends_on'
    confidence: float,
    evidence_paths: Optional[Iterable[str]] = None,
    note: str = "",
):
    props = {
        "confidence": float(confidence),
        "timestamp": _ts(),
        "evidence_paths": list(evidence_paths or []),
    }
    if note:
        props["note"] = note
    kg.add_edge(source, target, relation, properties=props)


# --- Value Mass helpers (09_VALUE_MASS_SPEC) ---
_TRACE_PATH = Path("data/value_mass_trace.json")


def _trace_mass(value_id: str, before: float, after: float, note: str = "") -> None:
    try:
        import json
        _TRACE_PATH.parent.mkdir(parents=True, exist_ok=True)
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "value": value_id,
            "before": before,
            "after": after,
            "note": note,
        }
        if _TRACE_PATH.exists():
            try:
                data = json.loads(_TRACE_PATH.read_text(encoding="utf-8"))
            except Exception:
                data = []
        else:
            data = []
        data.append(entry)
        _TRACE_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass


def update_value_mass(
    kg: KGManager,
    value_id: str,
    supports_inc: float = 0.0,
    refutes_inc: float = 0.0,
    decay: float = 0.0,
    alpha: float = 1.0,
    beta: float = 1.0,
    gamma: float = 0.0,
    note: str = "",
) -> float:
    """
    Minimal mass update consistent with 09_VALUE_MASS_SPEC.
    - mass <- (1 - decay)*mass + alpha*supports_inc - beta*refutes_inc + gamma
    Clamped at >= 0. Returns the new mass. Persists to KG node properties.
    """
    node = kg.get_node(value_id)
    if not node:
        node = kg.add_node(value_id, properties={"type": "value"})
    before = float(node.get("mass", 0.0) or 0.0)
    after = (1.0 - float(decay)) * before + float(alpha) * float(supports_inc) - float(beta) * float(refutes_inc) + float(gamma)
    if after < 0:
        after = 0.0
    kg.update_node_properties(value_id, {"mass": after, "mass_updated_at": datetime.utcnow().isoformat() + "Z"})
    try:
        kg.save()
    except Exception:
        pass
    _trace_mass(value_id, before, after, note)
    return after
