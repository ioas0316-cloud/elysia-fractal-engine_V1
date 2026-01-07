"""
Phase 5: The Evolutionary Universe (Enhanced with Phase 6 Meta-Consciousness)

Experience -> physical particles in CellWorld -> emergent Spiderweb.

Phase 6 Integration:
- MetaAwareness observes evolution cycles
- AutonomousDreamer generates goals from field gradients
- ParadoxResolver handles field contradictions
"""

import logging
from typing import List, Dict, Any, Optional, TYPE_CHECKING

import numpy as np

from core_memory import CoreMemory, Experience
from Legacy.Project_Sophia.spiderweb import Spiderweb
from world import World
from Legacy.Project_Sophia.wave_mechanics import WaveMechanics
from tensor_wave import Tensor3D, FrequencyWave

if TYPE_CHECKING:
    from Legacy.Project_Sophia.meta_awareness import MetaAwareness, ThoughtType
    from Legacy.Project_Sophia.autonomous_dreamer import AutonomousDreamer
    from Legacy.Project_Sophia.paradox_resolver import ParadoxResolver


class UniverseEvolutionEngine:
    """
    Evolves a universe by spawning experiences as particles and extracting Spiderweb.
    """

    def __init__(
        self,
        world: World,
        spiderweb: Spiderweb,
        meta_awareness: Optional['MetaAwareness'] = None,
        autonomous_dreamer: Optional['AutonomousDreamer'] = None,
        paradox_resolver: Optional['ParadoxResolver'] = None,
        logger: Optional[logging.Logger] = None
    ):
        self.world = world
        self.spiderweb = spiderweb
        self.meta_awareness = meta_awareness
        self.autonomous_dreamer = autonomous_dreamer
        self.paradox_resolver = paradox_resolver
        self.logger = logger or logging.getLogger("UniverseEvolution")
        
        if meta_awareness:
            self.logger.info("🧠 Meta-awareness enabled for universe evolution")
        if autonomous_dreamer:
            self.logger.info("🎯 Autonomous goal generation enabled")
        if paradox_resolver:
            self.logger.info("🌀 Paradox resolution enabled")

    def experience_to_particle(self, experience: Experience) -> Dict[str, Any]:
        """
        Map an Experience into a particle definition consumable by World.
        """
        if experience.emotional_state:
            valence = experience.emotional_state.valence
            arousal = experience.emotional_state.arousal
        else:
            valence = 0.5
            arousal = 0.5

        if experience.tensor and hasattr(experience.tensor, "x"):
            tensor = experience.tensor
        else:
            tensor = Tensor3D(x=0.5, y=valence, z=arousal)

        x = float(tensor.x * self.world.width * 0.8) + self.world.width * 0.1
        y = float(tensor.y * self.world.width * 0.8) + self.world.width * 0.1
        z = float(tensor.z * 10.0)

        energy = abs(valence - 0.5) * 500 + 500

        if experience.wave and hasattr(experience.wave, "frequency"):
            frequency = experience.wave.frequency
        else:
            content_hash = hash(experience.content) % 100
            frequency = content_hash + arousal * 50

        particle = {
            "concept_id": f"exp_{experience.timestamp}",
            "properties": {
                "element_type": "life",
                "label": "memory",
                "diet": "none",
                "energy": energy,
                "hp": energy,
                "max_hp": energy,
                "vitality": 50,
                "strength": int(abs(valence - 0.5) * 20) + 10,
                "intelligence": int(arousal * 20) + 10,
                "hunger": 100.0,
                "hydration": 100.0,
                "position": {"x": x, "y": y, "z": z},
            },
            "metadata": {
                "content": experience.content[:100],
                "timestamp": experience.timestamp,
                "frequency": frequency,
                "tensor": tensor,
            },
        }

        return particle

    def spawn_experience_universe(self, experiences: List[Experience]):
        """
        Spawn experiences into the World as particles.
        """
        self.logger.info(f"Spawning {len(experiences)} experiences as particles...")

        for exp in experiences:
            particle = self.experience_to_particle(exp)

            try:
                self.world.add_cell(concept_id=particle["concept_id"], properties=particle["properties"])
                self.logger.debug(f"Spawned: {particle['concept_id']}")
            except Exception as e:
                self.logger.error(f"Failed to spawn {particle['concept_id']}: {e}")

        alive_count = self.world.is_alive_mask.sum()
        self.logger.info(f"Universe spawned: {alive_count} particles alive")

    def extract_spiderweb_from_fields(self):
        """
        Extract Spiderweb nodes/edges from World field geometry.
        """
        self.logger.info("Extracting Spiderweb from Field geometry...")

        threshold = 0.6
        value_field = self.world.value_mass_field
        strong_regions = np.where(value_field > threshold)

        if len(strong_regions[0]) == 0:
            self.logger.warning("No strong value regions found")
            return

        concepts = []
        for y, x in zip(*strong_regions):
            concept_id = f"field_concept_{y}_{x}"
            value = float(value_field[y, x])

            self.spiderweb.add_node(
                concept_id,
                type="emergent_concept",
                metadata={
                    "position": (x, y),
                    "value": value,
                    "coherence": float(self.world.coherence_field[y, x]),
                    "will": float(self.world.will_field[y, x]),
                },
            )
            concepts.append((concept_id, x, y))

        for concept_id, x, y in concepts:
            direction = self.world.intentional_field[y, x]
            dx, dy = direction[0], direction[1]

            target_x = int(x + dx * 10) % self.world.width
            target_y = int(y + dy * 10) % self.world.width

            for other_id, ox, oy in concepts:
                if other_id == concept_id:
                    continue
                dist = np.sqrt((ox - target_x) ** 2 + (oy - target_y) ** 2)
                if dist < 20:
                    weight = float(self.world.will_field[y, x])
                    self.spiderweb.add_link(concept_id, other_id, relation="field_influence", weight=weight)

        node_count = self.spiderweb.graph.number_of_nodes()
        edge_count = self.spiderweb.graph.number_of_edges()
        self.logger.info(f"Spiderweb extracted: {node_count} nodes, {edge_count} edges")

    def evolve(
        self,
        cycles: int = 100000,
        extract_interval: int = 10000,
        sabbath_interval: int = 10000,
        sabbath_edge_fraction: float = 0.3,
        sabbath_node_fraction: float = 0.3,
        vcd=None,
        core_memory: CoreMemory = None,
    ):
        """
        Main evolution loop with periodic Spiderweb extraction and SABBATH pruning.
        """
        self.logger.info(f"Starting evolution for {cycles} cycles...")

        for cycle in range(cycles):
            self.world.run_simulation_step()
            
            # 🧠 Meta-awareness: Observe evolution cycle
            if self.meta_awareness and cycle % 1000 == 0:
                try:
                    from Legacy.Project_Sophia.meta_awareness import ThoughtType
                    self.meta_awareness.observe(
                        thought_type=ThoughtType.UNIVERSE_EVOLUTION,
                        input_state={"cycle": cycle, "alive": int(self.world.is_alive_mask.sum())},
                        output_state={
                            "max_value": float(self.world.value_mass_field.max()),
                            "max_coherence": float(self.world.coherence_field.max())
                        },
                        transformation=f"Universe evolved cycle {cycle}",
                        confidence=0.8,
                        metadata={"cycles_total": cycles}
                    )
                except Exception as e:
                    self.logger.warning(f"Meta-awareness observation failed: {e}")

            if cycle % extract_interval == 0:
                alive = self.world.is_alive_mask.sum()
                avg_energy = self.world.energy[self.world.is_alive_mask].mean() if alive > 0 else 0

                self.logger.info(f"Cycle {cycle}/{cycles}:")
                self.logger.info(f"  Alive particles: {alive}")
                self.logger.info(f"  Avg energy: {avg_energy:.2f}")
                self.logger.info(f"  Max value_field: {self.world.value_mass_field.max():.3f}")
                self.logger.info(f"  Max coherence: {self.world.coherence_field.max():.3f}")

                self.extract_spiderweb_from_fields()
                
                # 🎯 Autonomous goal generation from field gradients
                if self.autonomous_dreamer and cycle % (extract_interval * 2) == 0:
                    try:
                        goals = self.autonomous_dreamer.generate_goals(num_goals=2, min_priority=0.6)
                        if goals:
                            self.logger.info(f"  Generated {len(goals)} autonomous goals")
                    except Exception as e:
                        self.logger.warning(f"Autonomous goal generation failed: {e}")
                
                # 🌀 Detect and resolve paradoxes in emerged concepts
                if self.paradox_resolver and cycle % (extract_interval * 3) == 0:
                    try:
                        contradictions = self.paradox_resolver.detect_contradictions(min_opposition=0.7)
                        if contradictions:
                            self.logger.info(f"  Detected {len(contradictions)} contradictions")
                            # Resolve top contradiction
                            if contradictions:
                                c1, c2, strength = contradictions[0]
                                paradox = self.paradox_resolver.create_superposition(c1, c2)
                                self.paradox_resolver.resolve_paradox(paradox)
                    except Exception as e:
                        self.logger.warning(f"Paradox resolution failed: {e}")

            if sabbath_interval > 0 and cycle > 0 and cycle % sabbath_interval == 0:
                try:
                    self.spiderweb.prune_fraction(
                        edge_fraction=sabbath_edge_fraction,
                        node_fraction=sabbath_node_fraction,
                    )
                    if vcd and core_memory and hasattr(vcd, "update_core_value_from_history"):
                        vcd.update_core_value_from_history(core_memory, recent_ticks=sabbath_interval)
                    self.logger.info(
                        f"SABBATH: cycle {cycle} prune edges={sabbath_edge_fraction*100:.0f}% nodes={sabbath_node_fraction*100:.0f}%"
                    )
                except Exception as e:
                    self.logger.warning(f"SABBATH step failed at cycle {cycle}: {e}")

        self.extract_spiderweb_from_fields()
        self.logger.info("Evolution complete!")

        return self.spiderweb
