import re
import copy
from typing import List, Dict, Any, Optional

from kg_manager import KGManager
from world import World
from core.thought import Thought
from core.tensor_wave import Tensor3D

class LogicalReasoner:
    """
    Deduces logical facts from user input by interacting with the knowledge graph
    and running dynamic simulations in the Cellular World.
    """

    def __init__(self, kg_manager: Optional[KGManager] = None, cellular_world: Optional[World] = None):
        self.kg_manager = kg_manager or KGManager()
        self.cellular_world = cellular_world

    def _find_mentioned_entities(self, message: str) -> List[str]:
        """
        Finds entities from the KG mentioned in a message using a robust,
        length-sorted substring search to handle multi-word entities correctly.
        """
        mentioned_entities = []
        nodes = self.kg_manager.kg.get('nodes', [])
        if not nodes:
            return []

        node_ids = {node.get('id') for node in nodes if node.get('id')}

        # Sort by length descending to match longer names first (e.g., "black hole" before "hole")
        sorted_node_ids = sorted(list(node_ids), key=len, reverse=True)

        lower_message = message.lower()
        for entity_id in sorted_node_ids:
            if entity_id.lower() in lower_message:
                mentioned_entities.append(entity_id)

        return list(set(mentioned_entities))

    def _get_simulation_neighborhood(self, entity: str, depth: int = 1) -> List[str]:
        """
        Finds the central entity and its direct neighbors in the KG to define
        the "attention bubble" for the simulation.
        """
        if not self.kg_manager:
            return [entity]

        # Use a set to avoid duplicate entities
        neighbors = {entity}

        # Simple BFS-like expansion, but just for one level
        for edge in self.kg_manager.kg.get('edges', []):
            if edge.get('source') == entity:
                neighbors.add(edge.get('target'))
            elif edge.get('target') == entity:
                neighbors.add(edge.get('source'))

        return list(neighbors)

    def _run_causal_simulation(self, cause_entity: str, main_world: World, simulation_steps: int = 5) -> List[Thought]:
        """
        Runs a focused simulation within an "attention bubble" of relevant cells.
        """
        if not self.cellular_world: # This now refers to the empty sim_world
            return []

        # 1. Define the "attention bubble": the entity and its direct neighbors.
        sim_entities = self._get_simulation_neighborhood(cause_entity)

        # 2. Populate the simulation world (self.cellular_world) with only the relevant cells.
        #    We get their initial hp from the main_world's quantum state.
        initial_hps: Dict[str, float] = {}
        for entity_id in sim_entities:
            # Get the energy potential from the main world's quantum state
            hp = main_world.quantum_states.get(entity_id, {}).get('hp', 10.0)
            initial_hps[entity_id] = hp
            self.cellular_world.add_cell(entity_id, properties={'hp': hp, 'max_hp': hp * 2}) # Give buffer

        # 3. Add connections between the materialized cells based on the KG.
        #    This is crucial for the simulation to actually propagate energy.
        sim_entities_set = set(sim_entities)
        for edge in self.kg_manager.kg.get('edges', []):
            source, target = edge.get('source'), edge.get('target')
            if source in sim_entities_set and target in sim_entities_set:
                self.cellular_world.add_connection(source, target)

        # 4. Inject stimulus into the cause_entity in the simulation world.
        # [Fractal Upgrade] Instead of just HP, we should inject a tensor wave if possible.
        # For now, we keep the HP boost as the carrier wave for energy.
        self.cellular_world.inject_stimulus(cause_entity, energy_boost=100.0)

        # 5. Run simulation
        for _ in range(simulation_steps):
            self.cellular_world.run_simulation_step()

        # 5. Analyze results and generate thoughts.
        #    We iterate through the NumPy arrays as they represent the final state of all cells
        #    in the simulation, not just the ones that were explicitly materialized.
        simulation_thoughts: List[Thought] = []
        for i, cell_id in enumerate(self.cellular_world.cell_ids):
            # We only care about cells that were part of our initial attention bubble
            if cell_id not in initial_hps:
                continue

            initial_hp = initial_hps.get(cell_id, 0.0)
            final_hp = self.cellular_world.hp[i]

            # Consider a cell "activated" if its hp significantly increased
            # and it's not the cause_entity itself.
            if final_hp > initial_hp + 10.0 and cell_id != cause_entity:
                content = f"'{cause_entity}'의 영향으로 '{cell_id}' 개념이 활성화될 수 있습니다."

                # [Fractal Upgrade] Construct a Tensor3D representing this outcome using non-linear mapping
                # We map raw stats to the spectral axes using `distribute_frequency`.
                # - Wisdom (High Freq) -> Z-axis
                # - Emotion (Mid Freq) -> Y-axis
                # - Strength (Low Freq) -> X-axis

                # We calculate a 'dominant frequency' based on stats
                # Low stats = Low Freq, High stats = High Freq
                # This is a simplification but captures the user's intent

                base_freq = 0.0
                base_freq += (self.cellular_world.strength[i]) * 1.0 # Strength adds low freq (0-100)
                base_freq += (0.5 * 500.0) if self.cellular_world.emotions[i] != 'neutral' else 0 # Emotion adds mid freq
                base_freq += (self.cellular_world.wisdom[i]) * 10.0 # Wisdom adds high freq (0-1000)

                sim_tensor = Tensor3D.distribute_frequency(base_freq)

                # Add raw intensity
                intensity = final_hp / 100.0
                sim_tensor = sim_tensor * intensity

                thought = Thought(
                    content=content,
                    source='flesh',
                    confidence=0.7,
                    energy=final_hp,
                    evidence=[{'cell_id': cell_id, 'initial_hp': initial_hp, 'final_hp': final_hp}],
                    tensor=sim_tensor
                )
                simulation_thoughts.append(thought)

        # Sort by energy for relevance
        simulation_thoughts.sort(key=lambda t: t.energy, reverse=True)

        return simulation_thoughts


    def deduce_facts(self, message: str) -> List[Thought]:
        """
        Analyzes a message to deduce relevant facts from both the static KG
        and a dynamic simulation in the Cellular World.
        Returns a list of Thought objects.
        """
        all_thoughts: List[Thought] = []
        mentioned_entities = self._find_mentioned_entities(message)

        if not mentioned_entities:
            return []

        query_is_for_effect = "결과" in message or "영향" in message or "만약" in message

        for entity in mentioned_entities:
            # 1. Get static facts from KG
            static_thoughts = self._deduce_static_facts(entity)
            all_thoughts.extend(static_thoughts)

            # 2. Get dynamic insights from simulation if relevant
            if query_is_for_effect and self.cellular_world:
                # Instead of deep-copying, we create a new, lightweight world for each simulation.
                # This is the "observation" - we only materialize what we need to look at.
                sim_world = World(self.cellular_world.primordial_dna, self.cellular_world.wave_mechanics)

                # The simulation reasoner uses the same KG but the new, empty world.
                reasoner_for_sim = LogicalReasoner(self.kg_manager, sim_world)

                # The simulation method will now be responsible for populating the sim_world.
                dynamic_thoughts = reasoner_for_sim._run_causal_simulation(entity, self.cellular_world)
                all_thoughts.extend(dynamic_thoughts)

        # Remove duplicate thoughts based on content
        unique_thoughts_dict = {t.content: t for t in all_thoughts}
        return list(unique_thoughts_dict.values())


    def _deduce_static_facts(self, entity: str) -> List[Thought]:
        """Deduces facts from the static KG and returns them as Thought objects."""
        static_thoughts: List[Thought] = []
        for edge in self.kg_manager.kg.get('edges', []):
            thought = None
            if edge.get('source') == entity:
                relation, target = edge.get('relation', 'related_to'), edge.get('target')
                content = ""
                if relation == 'is_a':
                    content = f"'{entity}'은(는) '{target}'의 한 종류입니다."
                elif relation == 'causes':
                     content = f"'{entity}'은(는) '{target}'을(를) 유발할 수 있습니다."
                else:
                    content = f"'{entity}'은(는) '{target}'와(과) '{relation}' 관계입니다."

                if content:
                    # [Fractal Upgrade] Static thoughts carry the 'Bone' tensor
                    node_data = self.kg_manager.get_node(entity)
                    bone_tensor = Tensor3D.from_dict(node_data.get('tensor_state')) if node_data else Tensor3D(x=0.5, y=0.5, z=0.5)

                    thought = Thought(
                        content=content,
                        source='bone',  # '뼈'에서 비롯된 생각
                        confidence=0.95, # Static facts are highly confident
                        evidence=[edge],
                        tensor=bone_tensor
                    )

            elif edge.get('target') == entity:
                relation, source = edge.get('relation', 'related_to'), edge.get('source')
                content = ""
                if relation == 'is_a':
                    content = f"'{source}'은(는) '{entity}'의 한 예시입니다."
                elif relation == 'causes':
                    content = f"'{source}'은(는) '{entity}'의 원인이 될 수 있습니다."

                if content:
                    node_data = self.kg_manager.get_node(source)
                    bone_tensor = Tensor3D.from_dict(node_data.get('tensor_state')) if node_data else Tensor3D(x=0.5, y=0.5, z=0.5)

                    thought = Thought(
                        content=content,
                        source='bone',  # '뼈'에서 비롯된 생각
                        confidence=0.9, # Inferred relationships are slightly less confident
                        evidence=[edge],
                        tensor=bone_tensor
                    )

            if thought:
                static_thoughts.append(thought)

        return static_thoughts
