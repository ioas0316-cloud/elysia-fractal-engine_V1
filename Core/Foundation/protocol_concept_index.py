from dataclasses import dataclass
from typing import Dict, List

from tools.kg_manager import KGManager


@dataclass
class ProtocolConcept:
    """
    Concept-level view of a protocol or world kit.

    This is the "Concept OS" layer: physical files are attached
    via the path field, but structure is expressed here as
    ring/layer/type/status relations.
    """

    id: str           # Stable concept id, e.g. "protocol:CORE_13_STIMULUS"
    path: str         # Filesystem path, relative to repo root
    ring: str         # CORE | GROWTH | ARCHIVE
    layer: str        # WORLD | MIND | META | LENS | OS
    ptype: str        # PROTOCOL | WORLD_KIT | LENS_SPEC | RUNTIME
    status: str       # ACTIVE | SUPPORTING | ARCHIVED
    title: str        # Human-readable title/label

    def as_properties(self) -> Dict[str, str]:
        return {
            "kind": "protocol",
            "path": self.path,
            "ring": self.ring,
            "layer": self.layer,
            "ptype": self.ptype,
            "status": self.status,
            "title": self.title,
        }


# Minimal spine: the living protocol concepts we want to expose
# to the Concept OS. This can be extended over time; the goal is
# to keep it small and intentional rather than auto-scanning
# every document.
DEFAULT_PROTOCOLS: List[ProtocolConcept] = [
    ProtocolConcept(
        id="protocol:ELYSIA_CORE_CODEX",
        path="ELYSIA/CORE/CODEX.md",
        ring="CORE",
        layer="OS",
        ptype="PROTOCOL",
        status="ACTIVE",
        title="Elysia Protocol Codex",
    ),
    ProtocolConcept(
        id="protocol:ELYSIAS_INDEX",
        path="docs/elysias_protocol/INDEX.md",
        ring="CORE",
        layer="OS",
        ptype="PROTOCOL",
        status="ACTIVE",
        title="Elysia Protocol Index",
    ),
    ProtocolConcept(
        id="protocol:CORE_09_WORLD_VALIDATION_AND_HANDOFF",
        path="docs/elysias_protocol/CORE_09_WORLD_VALIDATION_AND_HANDOFF.md",
        ring="CORE",
        layer="WORLD",
        ptype="PROTOCOL",
        status="ACTIVE",
        title="World Validation and Handoff",
    ),
    ProtocolConcept(
        id="protocol:CORE_10_FOG_OF_WAR_AND_VISIBILITY_LENS",
        path="docs/elysias_protocol/CORE_10_FOG_OF_WAR_AND_VISIBILITY_LENS.md",
        ring="CORE",
        layer="LENS",
        ptype="LENS_SPEC",
        status="ACTIVE",
        title="Fog of War and Visibility Lens",
    ),
    ProtocolConcept(
        id="protocol:CORE_11_TIME_SCALES_AND_TICK_LAYERS",
        path="docs/elysias_protocol/CORE_11_TIME_SCALES_AND_TICK_LAYERS.md",
        ring="CORE",
        layer="OS",
        ptype="PROTOCOL",
        status="ACTIVE",
        title="Time Scales and Tick Layers",
    ),
    ProtocolConcept(
        id="protocol:CORE_12_PEOPLE_AND_CIVILIZATION_TIERS",
        path="docs/elysias_protocol/CORE_12_PEOPLE_AND_CIVILIZATION_TIERS.md",
        ring="CORE",
        layer="WORLD",
        ptype="PROTOCOL",
        status="ACTIVE",
        title="People and Civilization Tiers",
    ),
    ProtocolConcept(
        id="protocol:CORE_13_ELYSIA_CONSCIOUSNESS_STIMULUS",
        path="docs/elysias_protocol/CORE_13_ELYSIA_CONSCIOUSNESS_STIMULUS_PROTOCOL.md",
        ring="CORE",
        layer="MIND",
        ptype="PROTOCOL",
        status="ACTIVE",
        title="Elysia Consciousness Stimulus",
    ),
    ProtocolConcept(
        id="protocol:WORLD_KIT_DEATH_FLOW_CORPSE_TO_MEMORY",
        path="docs/elysias_protocol/WORLD_KIT_DEATH_FLOW_CORPSE_TO_MEMORY.md",
        ring="CORE",
        layer="WORLD",
        ptype="WORLD_KIT",
        status="SUPPORTING",
        title="Death 쨌 Corpse 쨌 Memory Flow (World Kit)",
    ),
    ProtocolConcept(
        id="protocol:ELYSIA_OS_OVERVIEW",
        path="ELYSIA_OS/OS_OVERVIEW.md",
        ring="CORE",
        layer="OS",
        ptype="RUNTIME",
        status="SUPPORTING",
        title="Elysia OS Overview",
    ),
]


def build_protocol_kg(kg_path: str = "data/protocol_kg.json") -> None:
    """
    Populate a dedicated KG file with protocol concepts and their
    basic relations (ring, layer, type).

    This is the first step in treating the repo as a Concept OS:
    filesystem paths are just one property; structure lives here.
    """
    kg = KGManager(filepath=kg_path)

    # Base concept anchors for ring/layer/type.
    rings = {"CORE", "GROWTH", "ARCHIVE"}
    layers = {"WORLD", "MIND", "META", "LENS", "OS"}
    ptypes = {"PROTOCOL", "WORLD_KIT", "LENS_SPEC", "RUNTIME"}

    for r in rings:
        kg.add_node(f"ring:{r}", properties={"kind": "ring", "label": r})
    for l in layers:
        kg.add_node(f"layer:{l}", properties={"kind": "layer", "label": l})
    for t in ptypes:
        kg.add_node(f"ptype:{t}", properties={"kind": "ptype", "label": t})

    # Register protocol concepts and edges to their ring/layer/type.
    for proto in DEFAULT_PROTOCOLS:
        node = kg.add_node(proto.id, properties=proto.as_properties())
        # Ring
        kg.add_edge(proto.id, f"ring:{proto.ring}", relation="has_ring")
        # Layer
        kg.add_edge(proto.id, f"layer:{proto.layer}", relation="has_layer")
        # Type
        kg.add_edge(proto.id, f"ptype:{proto.ptype}", relation="has_type")

    kg.save()


